import asyncio
from datetime import datetime
from typing import Dict, List
from agents.entity_extractor import run_entity_extraction
from agents.sanctions_agent import run_sanctions_check
from agents.vessel_agent import run_vessel_verification
from agents.news_agent import run_news_analysis
from agents.weather_agent import run_weather_analysis
from agents.route_agent import run_route_analysis
from agents.historical_agent import run_historical_analysis
from tools.calculators import (
    calculate_overall_risk, 
    calculate_regulatory_risk,
    calculate_cargo_risk,
    calculate_confidence_score
)
from tools.explainers import (
    explain_confidence_score,
    explain_risk_category,
    generate_recommendations
)
from tools.validators import flag_for_manual_review
from database.mock_data import HISTORICAL_APPLICATIONS

class OrchestratorAgent:
    """
    Main coordinator using state machine pattern
    Orchestrates parallel execution of specialist agents
    Aggregates results and generates final recommendations
    """
    
    def __init__(self):
        self.timeline = []
        self.state = {}
        self.start_time = None
    
    def add_timeline_event(self, agent: str, event: Dict):
        """Add event to timeline with timestamp"""
        self.timeline.append({
            "agent": agent,
            "timestamp": datetime.utcnow().isoformat(),
            "thought": event.get("thought", ""),
            "action": event.get("action", ""),
            "observation": event.get("observation", ""),
            "conclusion": event.get("conclusion", "")
        })
    
    async def orchestrate(self, user_input: Dict) -> Dict:
        """
        Main orchestration workflow
        Returns comprehensive risk assessment
        """
        self.start_time = datetime.utcnow()
        
        # Step 1: Entity Extraction
        entity_result = await run_entity_extraction(user_input)
        self.add_timeline_event("EntityExtractor", entity_result)
        entities = entity_result["data"]["entities"]
        
        # Extract key values
        vessel_name = entities["vessel_name"]["value"]
        imo_number = entities["imo_number"]["value"]
        owner = entities["owner"]["value"]
        country = entities["country_of_registry"]["value"]
        departure = entities["route"]["departure"]
        destination = entities["route"]["destination"]
        cargo_type = entities["cargo_type"]["value"]
        
        # Step 2: Parallel execution of specialist agents
        tasks = [
            run_sanctions_check(owner, imo_number),
            run_vessel_verification(user_input, imo_number),
            run_news_analysis(owner, vessel_name),
            run_weather_analysis(departure, destination),
            run_route_analysis(departure, destination)
        ]
        
        results = await asyncio.gather(*tasks)
        
        # Unpack results
        sanctions_result = results[0]
        vessel_result = results[1]
        news_result = results[2]
        weather_result = results[3]
        route_result = results[4]
        
        # Add to timeline
        for result in results:
            self.add_timeline_event(result["agent"], result)
        
        # Step 3: Calculate risk scores for each category
        category_scores = {
            "regulatory": calculate_regulatory_risk(
                sanctions_result["data"]["sanctions_found"],
                country
            ),
            "reputation": news_result["data"]["risk_assessment"],
            "route": route_result["data"]["risk_assessment"],
            "weather": weather_result["data"]["risk_assessment"],
            "vessel": vessel_result["data"]["risk_assessment"],
            "cargo": calculate_cargo_risk(cargo_type)
        }
        
        # Step 4: Calculate overall risk score
        overall_result = calculate_overall_risk(category_scores)
        
        # Step 5: Run historical analysis (now that we have risk score)
        historical_result = await run_historical_analysis(
            cargo_type,
            vessel_result["data"].get("vessel_age", 10),
            departure,
            destination,
            overall_result["overall_score"]
        )
        self.add_timeline_event("HistoricalAgent", historical_result)
        
        # Step 6: Calculate confidence and data quality
        all_sources = []
        all_sources.extend(sanctions_result["data"].get("sources", []))
        all_sources.extend(vessel_result["data"].get("sources", []))
        
        data_quality = sum(s.get("reliability", 3) for s in all_sources) / len(all_sources) / 5.0 if all_sources else 0.7
        cross_ref_valid = vessel_result["data"]["cross_reference"].get("valid", True)
        
        confidence = calculate_confidence_score(data_quality, cross_ref_valid, len(all_sources))
        
        confidence_explanation = explain_confidence_score(confidence, {
            "data_quality": data_quality,
            "cross_ref_valid": cross_ref_valid,
            "sources_count": len(all_sources)
        })
        
        # Step 7: Generate recommendations
        recommendations = generate_recommendations(
            overall_result,
            category_scores,
            HISTORICAL_APPLICATIONS
        )
        
        # Step 8: Flag for manual review if needed
        manual_review_flags = flag_for_manual_review(
            overall_result["overall_score"],
            confidence,
            vessel_result["data"].get("vessel_age", 10),
            cargo_type,
            sanctions_result["data"]["sanctions_found"],
            vessel_result["data"]["cross_reference"].get("mismatches", [])
        )
        
        # Step 9: Generate category explanations
        category_explanations = {}
        for category, scores in category_scores.items():
            category_explanations[category] = explain_risk_category(
                category,
                scores.get("score", 50),
                scores
            )
        
        # Calculate execution time
        end_time = datetime.utcnow()
        execution_time = (end_time - self.start_time).total_seconds()
        
        # Compile final result
        final_result = {
            "success": True,
            "execution_time": round(execution_time, 2),
            "timestamp": end_time.isoformat(),
            
            # Entity recognition
            "entities": entity_result["data"],
            
            # Risk scores
            "overall_risk": {
                "score": overall_result["overall_score"],
                "decision": overall_result["decision"],
                "confidence": confidence,
                "confidence_explanation": confidence_explanation,
                "premium_adjustment": overall_result["premium_adjustment"],
                "breakdown": overall_result["breakdown"],
                "calculation_details": overall_result["calculation"]
            },
            
            # Category details
            "categories": {
                "regulatory": {
                    "score": category_scores["regulatory"]["score"],
                    "data": sanctions_result["data"],
                    "explanation": category_explanations["regulatory"]
                },
                "reputation": {
                    "score": category_scores["reputation"]["score"],
                    "data": news_result["data"],
                    "explanation": category_explanations["reputation"]
                },
                "route": {
                    "score": category_scores["route"]["score"],
                    "data": route_result["data"],
                    "explanation": category_explanations["route"]
                },
                "weather": {
                    "score": category_scores["weather"]["score"],
                    "data": weather_result["data"],
                    "explanation": category_explanations["weather"]
                },
                "vessel": {
                    "score": category_scores["vessel"]["score"],
                    "data": vessel_result["data"],
                    "explanation": category_explanations["vessel"]
                },
                "cargo": {
                    "score": category_scores["cargo"]["score"],
                    "data": {"type": cargo_type},
                    "explanation": category_explanations["cargo"]
                }
            },
            
            # Historical context
            "historical_analysis": historical_result["data"],
            
            # Recommendations
            "recommendations": recommendations,
            
            # Manual review flags
            "manual_review": manual_review_flags,
            
            # Complete timeline (ReAct pattern)
            "timeline": self.timeline,
            
            # Data sources
            "sources": all_sources,
            "data_quality": {
                "score": round(data_quality, 2),
                "sources_count": len(all_sources),
                "cross_reference_valid": cross_ref_valid
            }
        }
        
        return final_result

async def run_risk_assessment(user_input: Dict) -> Dict:
    """
    Main entry point for risk assessment
    """
    orchestrator = OrchestratorAgent()
    result = await orchestrator.orchestrate(user_input)
    return result
