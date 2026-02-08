from typing import Dict, List, Any, Tuple
import re

def validate_imo_format(imo_number: str) -> Tuple[bool, str]:
    """
    Validate IMO number format (IMO + 7 digits)
    Returns (is_valid, message)
    """
    pattern = r'^IMO\d{7}$'
    if re.match(pattern, imo_number):
        return True, "Valid IMO format"
    return False, f"Invalid IMO format. Expected IMOxxxxxxx, got {imo_number}"

def cross_reference_vessel(user_data: Dict, registry_data: Dict) -> Dict:
    """
    Cross-reference user input with vessel registry data
    Flag mismatches for manual review
    """
    mismatches = []
    confidence = 1.0
    
    if not registry_data.get("found"):
        return {
            "valid": False,
            "confidence": 0.3,
            "message": "Vessel not found in registry",
            "mismatches": ["Vessel not in registry"],
            "requires_review": True
        }
    
    vessel_data = registry_data.get("vessel_data", {})
    
    # Check vessel name (fuzzy match)
    if "name" in vessel_data:
        registry_name = vessel_data["name"].lower().strip()
        user_name = user_data.get("vessel_name", "").lower().strip()
        if registry_name != user_name and registry_name not in user_name and user_name not in registry_name:
            mismatches.append(f"Name mismatch: User='{user_data.get('vessel_name')}', Registry='{vessel_data['name']}'")
            confidence -= 0.2
    
    # Check owner (if available)
    if "owner" in vessel_data and user_data.get("owner"):
        registry_owner = vessel_data["owner"].lower().strip()
        user_owner = user_data.get("owner", "").lower().strip()
        if registry_owner != user_owner and registry_owner not in user_owner and user_owner not in registry_owner:
            mismatches.append(f"Owner mismatch: User='{user_data.get('owner')}', Registry='{vessel_data['owner']}'")
            confidence -= 0.15
    
    # Check flag/registry (if available)
    if "flag" in vessel_data and user_data.get("country_of_registry"):
        registry_flag = vessel_data["flag"].lower().strip()
        user_flag = user_data.get("country_of_registry", "").lower().strip()
        if registry_flag != user_flag:
            mismatches.append(f"Flag mismatch: User='{user_data.get('country_of_registry')}', Registry='{vessel_data['flag']}'")
            confidence -= 0.1
    
    confidence = max(0.0, confidence)
    requires_review = confidence < 0.85 or len(mismatches) > 0
    
    return {
        "valid": len(mismatches) == 0,
        "confidence": round(confidence, 2),
        "message": "Cross-reference complete" if len(mismatches) == 0 else "Mismatches detected",
        "mismatches": mismatches,
        "requires_review": requires_review,
        "vessel_data": vessel_data
    }

def validate_sanctions(sanctions_result: Dict) -> Dict:
    """
    Validate and format sanctions check results
    """
    if sanctions_result.get("found"):
        return {
            "status": "SANCTIONED",
            "risk_level": "CRITICAL",
            "requires_review": True,
            "details": sanctions_result.get("details"),
            "sources": sanctions_result.get("sources", [])
        }
    
    return {
        "status": "CLEAR",
        "risk_level": "LOW",
        "requires_review": False,
        "details": "No sanctions found",
        "sources": sanctions_result.get("sources", [])
    }

def calculate_data_quality(sources: List[Dict]) -> Dict:
    """
    Calculate overall data quality score
    """
    if not sources:
        return {
            "score": 0.5,
            "reliability": "Medium",
            "confidence": 0.5
        }
    
    total_reliability = sum(s.get("reliability", 3) for s in sources)
    avg_reliability = total_reliability / len(sources)
    
    quality_score = avg_reliability / 5.0
    
    if quality_score >= 0.8:
        reliability_label = "High"
    elif quality_score >= 0.6:
        reliability_label = "Medium"
    else:
        reliability_label = "Low"
    
    return {
        "score": round(quality_score, 2),
        "reliability": reliability_label,
        "confidence": round(quality_score, 2),
        "sources_count": len(sources)
    }

def flag_for_manual_review(risk_score: float, confidence: float, vessel_age: int, 
                           cargo_value: str, sanctions_found: bool, mismatches: List) -> Dict:
    """
    Determine if application requires manual review
    """
    flags = []
    
    if confidence < 0.85:
        flags.append(f"Low confidence score: {confidence:.2%}")
    
    if len(mismatches) > 0:
        flags.append(f"Cross-reference mismatches detected: {len(mismatches)}")
    
    if sanctions_found:
        flags.append("Sanctions found - CRITICAL")
    
    if vessel_age > 20:
        flags.append(f"Vessel age exceeds 20 years: {vessel_age} years")
    
    if risk_score > 70:
        flags.append(f"High risk score: {risk_score}")
    
    # High-value cargo types
    high_value_cargo = ["Tanker", "Reefer"]
    if cargo_value in high_value_cargo:
        flags.append(f"High-value cargo type: {cargo_value}")
    
    requires_review = len(flags) > 0
    
    return {
        "requires_review": requires_review,
        "flags": flags,
        "priority": "HIGH" if sanctions_found or risk_score > 85 else "MEDIUM" if requires_review else "LOW"
    }
