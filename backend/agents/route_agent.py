from datetime import datetime
from tools.calculators import calculate_route_risk
from database.mock_data import ROUTE_RISKS

async def run_route_analysis(departure: str, destination: str) -> dict:
    """
    Analyze route for piracy and geopolitical risks
    Check high-risk maritime areas
    """
    timestamp = datetime.utcnow()
    
    # Thought
    thought = f"Need to assess piracy and geopolitical risks for route {departure} to {destination}"
    
    # Action
    action = "Analyzing route segments for high-risk areas and piracy incidents"
    
    # Observation - Calculate route risk
    route_risk = calculate_route_risk(departure, destination)
    
    high_risk_areas = route_risk.get("high_risk_areas", [])
    observation = f"Route analysis complete. {len(high_risk_areas)} high-risk areas identified along potential route."
    
    # Conclusion
    risk_score = route_risk.get("score", 50)
    
    if risk_score >= 75:
        conclusion = f"HIGH route risk ({risk_score}/100). Multiple high-risk maritime areas: {', '.join([a['area'] for a in high_risk_areas[:2]])}. Enhanced security recommended."
    elif risk_score >= 50:
        conclusion = f"MODERATE route risk ({risk_score}/100). Some geopolitical concerns. Standard security protocols sufficient."
    else:
        conclusion = f"LOW route risk ({risk_score}/100). Well-established, secure trade route."
    
    # Detailed area analysis
    area_details = []
    for area in high_risk_areas:
        area_details.append({
            "name": area["area"],
            "piracy_incidents": area["incidents"],
            "risk_score": area["score"],
            "description": area["description"]
        })
    
    return {
        "agent": "RouteAgent",
        "status": "complete",
        "thought": thought,
        "action": action,
        "observation": observation,
        "conclusion": conclusion,
        "data": {
            "route": f"{departure} → {destination}",
            "risk_score": risk_score,
            "high_risk_areas": area_details,
            "risk_assessment": route_risk,
            "timestamp": timestamp.isoformat(),
            "reliability": 4
        }
    }
