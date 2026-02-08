import re
from typing import Dict
from datetime import datetime

def extract_entities(user_input: Dict) -> Dict:
    """
    Extract and validate entities from user input
    Provides confidence scores for each entity
    """
    entities = {}
    timestamp = datetime.utcnow()
    
    # Extract vessel name
    vessel_name = user_input.get("vessel_name", "").strip()
    entities["vessel_name"] = {
        "value": vessel_name,
        "confidence": 0.95 if len(vessel_name) > 3 else 0.60,
        "type": "VESSEL_NAME"
    }
    
    # Extract and validate IMO number
    imo_number = user_input.get("imo_number", "").strip()
    imo_pattern = r'^IMO\d{7}$'
    is_valid_imo = bool(re.match(imo_pattern, imo_number))
    entities["imo_number"] = {
        "value": imo_number,
        "confidence": 0.98 if is_valid_imo else 0.50,
        "type": "IMO_NUMBER",
        "valid_format": is_valid_imo
    }
    
    # Extract owner
    owner = user_input.get("owner", "").strip()
    entities["owner"] = {
        "value": owner,
        "confidence": 0.90 if len(owner) > 3 else 0.65,
        "type": "COMPANY_NAME"
    }
    
    # Extract country of registry
    country = user_input.get("country_of_registry", "").strip()
    entities["country_of_registry"] = {
        "value": country,
        "confidence": 0.95 if len(country) > 2 else 0.70,
        "type": "COUNTRY"
    }
    
    # Extract route
    departure = user_input.get("departure_port", "").strip()
    destination = user_input.get("destination_port", "").strip()
    entities["route"] = {
        "value": f"{departure} → {destination}",
        "departure": departure,
        "destination": destination,
        "confidence": 0.95 if (len(departure) > 2 and len(destination) > 2) else 0.70,
        "type": "ROUTE"
    }
    
    # Extract cargo type
    cargo_type = user_input.get("cargo_type", "").strip()
    valid_cargo_types = ["Container", "Bulk", "Tanker", "Reefer", "RoRo"]
    entities["cargo_type"] = {
        "value": cargo_type,
        "confidence": 0.98 if cargo_type in valid_cargo_types else 0.75,
        "type": "CARGO_TYPE"
    }
    
    # Calculate overall confidence
    confidences = [e["confidence"] for e in entities.values()]
    overall_confidence = sum(confidences) / len(confidences)
    
    return {
        "entities": entities,
        "overall_confidence": round(overall_confidence, 2),
        "timestamp": timestamp.isoformat(),
        "validation_issues": [
            f"IMO format invalid: {imo_number}" for imo_number in [imo_number] if not is_valid_imo
        ]
    }

async def run_entity_extraction(user_input: Dict) -> Dict:
    """
    Main entry point for entity extraction agent
    """
    result = extract_entities(user_input)
    
    return {
        "agent": "EntityExtractor",
        "status": "complete",
        "data": result,
        "thought": "Extracted entities from user input with confidence scores",
        "action": "Entity Recognition using NER patterns",
        "observation": f"Identified {len(result['entities'])} entities with {result['overall_confidence']:.0%} overall confidence"
    }
