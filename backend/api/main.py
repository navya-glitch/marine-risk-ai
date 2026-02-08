from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from contextlib import asynccontextmanager
import asyncio
from datetime import datetime

from agents.orchestrator import run_risk_assessment
from database.connection import init_db, get_db
from database.models import Application
from database.mock_data import HISTORICAL_APPLICATIONS
import config

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events"""
    # Startup
    try:
        init_db()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"⚠️  Database initialization warning: {e}")
    
    yield
    
    # Shutdown (if needed)
    pass

# Initialize FastAPI app
app = FastAPI(
    title="Marine Risk AI API",
    description="Agentic AI system for ocean marine insurance risk assessment",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class RiskAssessmentRequest(BaseModel):
    vessel_name: str
    imo_number: str
    owner: str
    country_of_registry: str
    departure_port: str
    destination_port: str
    cargo_type: str

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    ollama_connected: bool
    database_connected: bool

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "🚢 Marine Risk AI - 360° External Risk Insight",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    Verifies Ollama and database connectivity
    """
    import requests
    
    # Check Ollama
    ollama_connected = False
    try:
        response = requests.get(f"{config.OLLAMA_HOST}/api/tags", timeout=2)
        ollama_connected = response.status_code == 200
    except:
        pass
    
    # Check database
    database_connected = False
    try:
        from database.connection import engine
        with engine.connect() as conn:
            database_connected = True
    except:
        pass
    
    return {
        "status": "healthy" if (ollama_connected or database_connected) else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "ollama_connected": ollama_connected,
        "database_connected": database_connected
    }

@app.post("/api/analyze")
async def analyze_risk(request: RiskAssessmentRequest):
    """
    Main risk assessment endpoint
    Returns comprehensive analysis in <60 seconds
    """
    try:
        # Convert request to dict
        user_input = request.dict()
        
        # Run risk assessment
        result = await run_risk_assessment(user_input)
        
        return {
            "success": True,
            "data": result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Risk assessment failed: {str(e)}")

@app.websocket("/ws/analyze")
async def websocket_analyze(websocket: WebSocket):
    """
    WebSocket endpoint for real-time updates
    Streams progress as agents complete
    """
    await websocket.accept()
    
    try:
        # Receive request data
        data = await websocket.receive_json()
        
        # Send initial acknowledgment
        await websocket.send_json({
            "type": "started",
            "message": "Risk assessment started",
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Import agents
        from agents.entity_extractor import run_entity_extraction
        from agents.sanctions_agent import run_sanctions_check
        from agents.vessel_agent import run_vessel_verification
        from agents.news_agent import run_news_analysis
        from agents.weather_agent import run_weather_analysis
        from agents.route_agent import run_route_analysis
        from agents.historical_agent import run_historical_analysis
        
        # Step 1: Entity extraction
        entity_result = await run_entity_extraction(data)
        await websocket.send_json({
            "type": "agent_complete",
            "agent": "EntityExtractor",
            "data": entity_result,
            "progress": 15
        })
        
        entities = entity_result["data"]["entities"]
        vessel_name = entities["vessel_name"]["value"]
        imo_number = entities["imo_number"]["value"]
        owner = entities["owner"]["value"]
        country = entities["country_of_registry"]["value"]
        departure = entities["route"]["departure"]
        destination = entities["route"]["destination"]
        cargo_type = entities["cargo_type"]["value"]
        
        # Step 2: Run agents in parallel with progress updates
        agents_tasks = {
            "sanctions": run_sanctions_check(owner, imo_number),
            "vessel": run_vessel_verification(data, imo_number),
            "news": run_news_analysis(owner, vessel_name),
            "weather": run_weather_analysis(departure, destination),
            "route": run_route_analysis(departure, destination)
        }
        
        # Execute and stream results
        progress = 15
        results = {}
        for name, task in agents_tasks.items():
            result = await task
            results[name] = result
            progress += 12
            await websocket.send_json({
                "type": "agent_complete",
                "agent": result["agent"],
                "data": result,
                "progress": progress
            })
        
        # Complete analysis
        result = await run_risk_assessment(data)
        
        await websocket.send_json({
            "type": "complete",
            "data": result,
            "progress": 100
        })
    
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": str(e)
        })
    finally:
        await websocket.close()

@app.get("/api/historical")
async def get_historical_data():
    """
    Get historical applications data
    """
    return {
        "success": True,
        "total": len(HISTORICAL_APPLICATIONS),
        "applications": HISTORICAL_APPLICATIONS
    }

@app.get("/api/statistics")
async def get_statistics():
    """
    Get system statistics
    """
    total_apps = len(HISTORICAL_APPLICATIONS)
    accepted = len([a for a in HISTORICAL_APPLICATIONS if a.get("decision") == "Accept"])
    conditional = len([a for a in HISTORICAL_APPLICATIONS if a.get("decision") == "Accept with conditions"])
    manual = len([a for a in HISTORICAL_APPLICATIONS if a.get("decision") == "Manual review"])
    
    avg_risk = sum(a.get("risk_score", 0) for a in HISTORICAL_APPLICATIONS) / total_apps
    
    return {
        "success": True,
        "statistics": {
            "total_applications": total_apps,
            "decisions": {
                "accept": accepted,
                "conditional": conditional,
                "manual_review": manual
            },
            "average_risk_score": round(avg_risk, 2),
            "acceptance_rate": round(accepted / total_apps, 2)
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
