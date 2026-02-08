from typing import Dict, List
from datetime import datetime
from config import RISK_WEIGHTS, RISK_THRESHOLDS
from database.mock_data import ROUTE_RISKS

def calculate_vessel_risk(vessel_age: int, vessel_type: str = None) -> Dict:
    """
    Calculate vessel risk based on age and type
    """
    # Age-based risk (higher for older vessels)
    if vessel_age <= 5:
        age_score = 20
    elif vessel_age <= 10:
        age_score = 30
    elif vessel_age <= 15:
        age_score = 50
    elif vessel_age <= 20:
        age_score = 70
    else:
        age_score = 90
    
    return {
        "score": age_score,
        "factors": {
            "age": vessel_age,
            "age_risk": age_score
        },
        "reasoning": f"Vessel age {vessel_age} years corresponds to {'low' if age_score < 40 else 'medium' if age_score < 70 else 'high'} risk"
    }

def calculate_route_risk(departure: str, destination: str) -> Dict:
    """
    Calculate route risk based on piracy and geopolitical factors
    """
    # Check if route passes through high-risk areas
    risk_areas = []
    total_score = 0
    
    for area, data in ROUTE_RISKS.items():
        # Simple heuristic: check if area name is in departure/destination or common routes
        risk_areas.append({
            "area": area,
            "score": data["score"],
            "incidents": data.get("piracy_incidents", 0),
            "description": data.get("description", "")
        })
        total_score += data["score"]
    
    # Average risk across potentially affected areas (simplified)
    avg_score = min(85, total_score // len(ROUTE_RISKS) + 10)
    
    return {
        "score": avg_score,
        "high_risk_areas": [a for a in risk_areas if a["score"] > 60][:3],
        "reasoning": f"Route from {departure} to {destination} has moderate geopolitical and piracy risks"
    }

def calculate_cargo_risk(cargo_type: str) -> Dict:
    """
    Calculate cargo risk based on type
    """
    cargo_scores = {
        "Container": 35,
        "Bulk": 40,
        "Tanker": 60,
        "Reefer": 45,
        "RoRo": 50
    }
    
    score = cargo_scores.get(cargo_type, 50)
    
    return {
        "score": score,
        "type": cargo_type,
        "reasoning": f"{cargo_type} cargo has {'low' if score < 40 else 'medium' if score < 60 else 'high'} inherent risk"
    }

def calculate_reputation_risk(news_sentiment: Dict, claims_history: List = None) -> Dict:
    """
    Calculate reputation risk based on news sentiment and claims
    """
    sentiment_score = news_sentiment.get("score", 0.5)
    
    # Convert sentiment to risk (inverse relationship)
    # Positive sentiment (0.7-1.0) = Low risk (20-40)
    # Neutral sentiment (0.4-0.7) = Medium risk (40-60)
    # Negative sentiment (0.0-0.4) = High risk (60-90)
    
    if sentiment_score >= 0.7:
        risk_score = 20 + (1.0 - sentiment_score) * 66
    elif sentiment_score >= 0.4:
        risk_score = 40 + (0.7 - sentiment_score) * 66
    else:
        risk_score = 60 + (0.4 - sentiment_score) * 75
    
    # Adjust for claims history
    if claims_history and len(claims_history) > 0:
        risk_score += len(claims_history) * 10
    
    risk_score = min(95, risk_score)
    
    return {
        "score": int(risk_score),
        "sentiment": news_sentiment.get("sentiment", "neutral"),
        "articles_count": len(news_sentiment.get("articles", [])),
        "claims_count": len(claims_history) if claims_history else 0,
        "reasoning": f"{'Positive' if sentiment_score > 0.6 else 'Neutral' if sentiment_score > 0.4 else 'Negative'} sentiment with {len(claims_history) if claims_history else 0} historical claims"
    }

def calculate_regulatory_risk(sanctions_found: bool, flag_country: str = None) -> Dict:
    """
    Calculate regulatory risk based on sanctions and registry
    """
    if sanctions_found:
        return {
            "score": 100,
            "factors": ["Sanctions found"],
            "reasoning": "CRITICAL: Entity found in sanctions database"
        }
    
    # Low-risk registries
    reputable_flags = ["Panama", "Liberia", "Marshall Islands", "Singapore", "Hong Kong", "Malta", "Bahamas"]
    
    if flag_country in reputable_flags:
        base_score = 20
    else:
        base_score = 40
    
    return {
        "score": base_score,
        "factors": [f"Flag: {flag_country}"],
        "reasoning": f"Vessel registered in {flag_country} - {'reputable' if base_score < 30 else 'standard'} registry"
    }

def calculate_weather_risk(weather_data: Dict) -> Dict:
    """
    Calculate weather risk from weather data
    """
    score = weather_data.get("risk_score", 50)
    
    return {
        "score": score,
        "conditions": weather_data.get("conditions", "Unknown"),
        "hazards": weather_data.get("hazards", []),
        "delay_probability": weather_data.get("delay_probability", 0.2),
        "reasoning": f"Weather risk: {score}/100 with {len(weather_data.get('hazards', []))} identified hazards"
    }

def calculate_overall_risk(category_scores: Dict) -> Dict:
    """
    Calculate weighted overall risk score
    Returns score, breakdown, and decision recommendation
    """
    # Extract scores
    regulatory_score = category_scores.get("regulatory", {}).get("score", 50)
    reputation_score = category_scores.get("reputation", {}).get("score", 50)
    route_score = category_scores.get("route", {}).get("score", 50)
    weather_score = category_scores.get("weather", {}).get("score", 50)
    vessel_score = category_scores.get("vessel", {}).get("score", 50)
    cargo_score = category_scores.get("cargo", {}).get("score", 50)
    
    # Calculate weighted score
    overall_score = (
        regulatory_score * RISK_WEIGHTS["regulatory"] +
        reputation_score * RISK_WEIGHTS["reputation"] +
        route_score * RISK_WEIGHTS["route"] +
        weather_score * RISK_WEIGHTS["weather"] +
        vessel_score * RISK_WEIGHTS["vessel"] +
        cargo_score * RISK_WEIGHTS["cargo"]
    )
    
    # Determine decision
    if overall_score < RISK_THRESHOLDS["low"]:
        decision = "Accept"
        confidence = 0.95
        premium_adjustment = 1.0
    elif overall_score < RISK_THRESHOLDS["medium"]:
        decision = "Accept with conditions"
        confidence = 0.85
        premium_adjustment = 1.0 + (overall_score - RISK_THRESHOLDS["low"]) * 0.006
    else:
        decision = "Manual review"
        confidence = 0.70
        premium_adjustment = 1.20 + (overall_score - RISK_THRESHOLDS["medium"]) * 0.003
    
    # Create detailed breakdown
    breakdown = {
        "regulatory": {
            "score": regulatory_score,
            "weight": RISK_WEIGHTS["regulatory"],
            "contribution": round(regulatory_score * RISK_WEIGHTS["regulatory"], 2)
        },
        "reputation": {
            "score": reputation_score,
            "weight": RISK_WEIGHTS["reputation"],
            "contribution": round(reputation_score * RISK_WEIGHTS["reputation"], 2)
        },
        "route": {
            "score": route_score,
            "weight": RISK_WEIGHTS["route"],
            "contribution": round(route_score * RISK_WEIGHTS["route"], 2)
        },
        "weather": {
            "score": weather_score,
            "weight": RISK_WEIGHTS["weather"],
            "contribution": round(weather_score * RISK_WEIGHTS["weather"], 2)
        },
        "vessel": {
            "score": vessel_score,
            "weight": RISK_WEIGHTS["vessel"],
            "contribution": round(vessel_score * RISK_WEIGHTS["vessel"], 2)
        },
        "cargo": {
            "score": cargo_score,
            "weight": RISK_WEIGHTS["cargo"],
            "contribution": round(cargo_score * RISK_WEIGHTS["cargo"], 2)
        }
    }
    
    return {
        "overall_score": round(overall_score, 2),
        "decision": decision,
        "confidence": confidence,
        "premium_adjustment": round(premium_adjustment, 3),
        "breakdown": breakdown,
        "calculation": f"({regulatory_score}*{RISK_WEIGHTS['regulatory']}) + ({reputation_score}*{RISK_WEIGHTS['reputation']}) + ({route_score}*{RISK_WEIGHTS['route']}) + ({weather_score}*{RISK_WEIGHTS['weather']}) + ({vessel_score}*{RISK_WEIGHTS['vessel']}) + ({cargo_score}*{RISK_WEIGHTS['cargo']}) = {round(overall_score, 2)}"
    }

def calculate_confidence_score(data_quality: float, cross_ref_valid: bool, sources_count: int) -> float:
    """
    Calculate overall confidence in the assessment
    """
    base_confidence = 0.85
    
    # Adjust for data quality
    base_confidence *= data_quality
    
    # Penalize for cross-reference failures
    if not cross_ref_valid:
        base_confidence *= 0.8
    
    # Reward for multiple sources
    if sources_count >= 3:
        base_confidence *= 1.05
    elif sources_count >= 2:
        base_confidence *= 1.02
    
    return min(0.99, max(0.50, base_confidence))
