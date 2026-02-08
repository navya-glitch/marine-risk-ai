from datetime import datetime
from typing import Dict
from tools.scrapers import scrape_weather_data
from tools.calculators import calculate_weather_risk

async def run_weather_analysis(departure: str, destination: str) -> Dict:
    """
    Analyze weather conditions for route
    Assess seasonal risks
    Calculate delay probability
    """
    timestamp = datetime.utcnow()
    
    # Thought
    thought = f"Need to assess weather risks for route {departure} to {destination}"
    
    # Action
    action = "Analyzing seasonal weather patterns and hazard data"
    
    # Observation - Get weather data
    route_str = f"{departure} to {destination}"
    weather_data = await scrape_weather_data(route_str)
    
    observation = f"Weather analysis complete. Conditions: {weather_data.get('conditions')}, Risk: {weather_data.get('risk_score')}/100"
    
    # Calculate weather risk
    weather_risk = calculate_weather_risk(weather_data)
    
    # Conclusion
    risk_score = weather_risk.get("score", 50)
    hazards = weather_risk.get("hazards", [])
    
    if risk_score >= 70:
        conclusion = f"HIGH weather risk ({risk_score}/100). {len(hazards)} hazards identified: {', '.join(hazards[:2])}. Consider schedule adjustment."
    elif risk_score >= 40:
        conclusion = f"MODERATE weather risk ({risk_score}/100). {len(hazards)} potential hazards. Standard monitoring recommended."
    else:
        conclusion = f"LOW weather risk ({risk_score}/100). Favorable conditions expected."
    
    return {
        "agent": "WeatherAgent",
        "status": "complete",
        "thought": thought,
        "action": action,
        "observation": observation,
        "conclusion": conclusion,
        "data": {
            "weather_conditions": weather_data.get("conditions"),
            "risk_score": weather_data.get("risk_score"),
            "hazards": hazards,
            "delay_probability": weather_data.get("delay_probability"),
            "risk_assessment": weather_risk,
            "timestamp": timestamp.isoformat(),
            "reliability": weather_data.get("reliability", 3)
        }
    }
