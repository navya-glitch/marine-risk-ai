from datetime import datetime
from tools.scrapers import scrape_sanctions
from tools.validators import validate_sanctions

async def run_sanctions_check(owner: str, imo_number: str) -> Dict:
    """
    Check OFAC/EU sanctions lists
    Cross-reference owner and IMO number
    """
    timestamp = datetime.utcnow()
    
    # Thought
    thought = f"Need to verify if {owner} or {imo_number} appears in sanctions databases"
    
    # Action
    action = "Scraping OFAC and EU sanctions lists"
    
    # Observation
    sanctions_result = await scrape_sanctions(owner, imo_number)
    
    # Validation
    validation = validate_sanctions(sanctions_result)
    
    observation = f"Sanctions check complete. Status: {validation['status']}"
    
    # Conclusion
    if sanctions_result.get("found"):
        conclusion = f"CRITICAL: {owner} found in sanctions database. Immediate rejection recommended."
        risk_score = 100
    else:
        conclusion = f"No sanctions found for {owner} or {imo_number}. Regulatory risk minimal."
        risk_score = 20
    
    return {
        "agent": "SanctionsAgent",
        "status": "complete",
        "thought": thought,
        "action": action,
        "observation": observation,
        "conclusion": conclusion,
        "data": {
            "sanctions_found": sanctions_result.get("found", False),
            "details": sanctions_result.get("details"),
            "sources": sanctions_result.get("sources", []),
            "risk_score": risk_score,
            "validation": validation,
            "timestamp": timestamp.isoformat(),
            "reliability": sanctions_result.get("reliability", 4)
        }
    }
