from datetime import datetime
from typing import Dict
from tools.scrapers import scrape_maritime_news
from tools.calculators import calculate_reputation_risk
from database.models import Claim
from database.connection import SessionLocal

async def run_news_analysis(owner: str, vessel_name: str) -> Dict:
    """
    Scrape maritime news for owner/vessel
    Analyze sentiment
    Check historical claims
    """
    timestamp = datetime.utcnow()
    
    # Thought
    thought = f"Need to assess reputation of {owner} through maritime news and claims history"
    
    # Action
    action = "Scraping maritime news sources and querying claims database"
    
    # Observation - Get news data
    news_data = await scrape_maritime_news(owner, vessel_name)
    
    # Check claims history (from mock data for now)
    from database.mock_data import MOCK_CLAIMS
    claims_history = [claim for claim in MOCK_CLAIMS if claim["owner"] == owner or claim["vessel_name"] == vessel_name]
    
    observation = f"Found {len(news_data.get('articles', []))} articles with {news_data.get('sentiment')} sentiment. {len(claims_history)} historical claims."
    
    # Calculate reputation risk
    reputation_risk = calculate_reputation_risk(news_data, claims_history)
    
    # Conclusion
    sentiment = news_data.get("sentiment", "neutral")
    if sentiment == "negative" or len(claims_history) > 2:
        conclusion = f"CAUTION: {sentiment.title()} news sentiment with {len(claims_history)} claims. Increased reputation risk."
    elif sentiment == "positive":
        conclusion = f"Positive reputation indicators. {owner} has favorable news coverage and {len(claims_history)} claims."
    else:
        conclusion = f"Neutral reputation profile. Standard monitoring recommended."
    
    return {
        "agent": "NewsAgent",
        "status": "complete",
        "thought": thought,
        "action": action,
        "observation": observation,
        "conclusion": conclusion,
        "data": {
            "news_sentiment": news_data.get("sentiment"),
            "sentiment_score": news_data.get("score"),
            "articles": news_data.get("articles", []),
            "claims_history": claims_history,
            "risk_assessment": reputation_risk,
            "timestamp": timestamp.isoformat(),
            "reliability": news_data.get("reliability", 3)
        }
    }
