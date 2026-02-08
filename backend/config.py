import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://marineuser:marinepass@localhost:5432/marine_risk")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Risk scoring weights
RISK_WEIGHTS = {
    "regulatory": 0.15,
    "reputation": 0.20,
    "route": 0.30,
    "weather": 0.15,
    "vessel": 0.10,
    "cargo": 0.10
}

# Risk thresholds
RISK_THRESHOLDS = {
    "low": 40,
    "medium": 70,
    "high": 100
}

# Cache expiry times (seconds)
CACHE_EXPIRY = {
    "sanctions": 86400,  # 24 hours
    "weather": 3600,     # 1 hour
    "vessel": 43200      # 12 hours
}
