from datetime import datetime
from typing import Dict
from tools.scrapers import scrape_vessel_registry
from tools.validators import cross_reference_vessel
from tools.calculators import calculate_vessel_risk

async def run_vessel_verification(user_data: Dict, imo_number: str) -> Dict:
    """
    Verify vessel details with registry
    Calculate vessel age risk
    Cross-reference with user input
    """
    timestamp = datetime.utcnow()
    
    # Thought
    thought = f"Need to verify vessel {imo_number} in maritime registry and validate user input"
    
    # Action
    action = "Scraping Equasis vessel registry and cross-referencing data"
    
    # Observation - Get registry data
    registry_result = await scrape_vessel_registry(imo_number)
    
    # Cross-reference with user input
    cross_ref = cross_reference_vessel(user_data, registry_result)
    
    observation = f"Vessel registry check complete. Found: {registry_result.get('found')}. Cross-reference valid: {cross_ref.get('valid')}"
    
    # Calculate vessel age risk
    vessel_age = None
    if registry_result.get("found") and registry_result.get("vessel_data"):
        vessel_data = registry_result["vessel_data"]
        built_year = vessel_data.get("built")
        if built_year:
            vessel_age = datetime.now().year - built_year
            vessel_risk = calculate_vessel_risk(vessel_age, vessel_data.get("type"))
        else:
            vessel_risk = {"score": 50, "reasoning": "Vessel age unknown"}
    else:
        vessel_risk = {"score": 60, "reasoning": "Vessel not found in registry - increased risk"}
        vessel_age = user_data.get("vessel_age", 10)  # fallback
    
    # Conclusion
    if not registry_result.get("found"):
        conclusion = f"WARNING: Vessel {imo_number} not found in registry. Manual verification required."
    elif not cross_ref.get("valid"):
        conclusion = f"WARNING: Cross-reference mismatches detected. {len(cross_ref.get('mismatches', []))} discrepancies found."
    else:
        conclusion = f"Vessel verified successfully. Age: {vessel_age} years, Risk score: {vessel_risk.get('score')}"
    
    return {
        "agent": "VesselAgent",
        "status": "complete",
        "thought": thought,
        "action": action,
        "observation": observation,
        "conclusion": conclusion,
        "data": {
            "registry_found": registry_result.get("found", False),
            "vessel_data": registry_result.get("vessel_data"),
            "vessel_age": vessel_age,
            "cross_reference": cross_ref,
            "risk_assessment": vessel_risk,
            "sources": registry_result.get("sources", []),
            "timestamp": timestamp.isoformat(),
            "reliability": registry_result.get("reliability", 4)
        }
    }
