from datetime import datetime
from typing import List, Dict
from database.mock_data import HISTORICAL_APPLICATIONS

async def run_historical_analysis(cargo_type: str, vessel_age: int, 
                                 departure: str, destination: str,
                                 risk_score: float) -> dict:
    """
    Analyze historical applications
    Find similar patterns
    Generate recommendations based on past decisions
    """
    timestamp = datetime.utcnow()
    
    # Thought
    thought = f"Need to analyze historical patterns for similar applications: {cargo_type} cargo, {vessel_age}yr vessel, {departure}-{destination} route"
    
    # Action
    action = "Querying historical database for similar applications and analyzing patterns"
    
    # Observation - Find similar applications
    similar_apps = []
    
    for app in HISTORICAL_APPLICATIONS:
        similarity_score = 0
        
        # Match cargo type
        if app.get("cargo_type") == cargo_type:
            similarity_score += 30
        
        # Match vessel age (within 5 years)
        if abs(app.get("vessel_age", 0) - vessel_age) <= 5:
            similarity_score += 20
        
        # Match route (exact or partial)
        if app.get("departure_port") == departure or app.get("destination_port") == destination:
            similarity_score += 25
        
        # Match risk score (within 20 points)
        if abs(app.get("risk_score", 0) - risk_score) <= 20:
            similarity_score += 25
        
        if similarity_score >= 50:  # Threshold for "similar"
            similar_apps.append({
                **app,
                "similarity_score": similarity_score
            })
    
    # Sort by similarity
    similar_apps.sort(key=lambda x: x["similarity_score"], reverse=True)
    top_similar = similar_apps[:10]
    
    observation = f"Found {len(similar_apps)} similar historical applications (out of {len(HISTORICAL_APPLICATIONS)} total)"
    
    # Calculate statistics
    if similar_apps:
        acceptance_rate = len([app for app in similar_apps if app.get("decision") == "Accept"]) / len(similar_apps)
        avg_risk_score = sum(app.get("risk_score", 0) for app in similar_apps) / len(similar_apps)
        avg_premium = sum(app.get("premium_adjustment", 1.0) for app in similar_apps) / len(similar_apps)
        
        # Decision distribution
        decisions = {}
        for app in similar_apps:
            decision = app.get("decision", "Unknown")
            decisions[decision] = decisions.get(decision, 0) + 1
    else:
        acceptance_rate = 0.5
        avg_risk_score = 50
        avg_premium = 1.10
        decisions = {}
    
    # Conclusion
    if len(similar_apps) >= 5:
        conclusion = f"Strong historical context: {len(similar_apps)} similar applications. Acceptance rate: {acceptance_rate:.0%}, Avg premium: +{(avg_premium-1.0)*100:.1f}%"
    elif len(similar_apps) >= 2:
        conclusion = f"Limited historical context: {len(similar_apps)} similar applications found. Proceed with caution."
    else:
        conclusion = f"Minimal historical context: No closely matching applications. Unique risk profile requires careful assessment."
    
    return {
        "agent": "HistoricalAgent",
        "status": "complete",
        "thought": thought,
        "action": action,
        "observation": observation,
        "conclusion": conclusion,
        "data": {
            "total_applications": len(HISTORICAL_APPLICATIONS),
            "similar_applications": len(similar_apps),
            "top_matches": top_similar[:5],
            "statistics": {
                "acceptance_rate": round(acceptance_rate, 3),
                "average_risk_score": round(avg_risk_score, 2),
                "average_premium": round(avg_premium, 3),
                "decision_distribution": decisions
            },
            "timestamp": timestamp.isoformat(),
            "reliability": 5
        }
    }
