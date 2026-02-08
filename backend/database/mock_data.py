from datetime import datetime, timedelta
import random

# Sanctioned entities
SANCTIONED_ENTITIES = [
    "Crimea Shipping Corp",
    "Iran Maritime Lines",
    "DPRK Vessels Inc",
    "Syria Ocean Transport",
    "Venezuela Marine Co"
]

# Mock vessel registry
MOCK_VESSELS = {
    "IMO9547821": {
        "name": "MV Neptune Star",
        "type": "Container Ship",
        "built": 2015,
        "dwt": 40000,
        "flag": "Panama",
        "owner": "Neptune Maritime Corp"
    },
    "IMO9123456": {
        "name": "Atlantic Voyager",
        "type": "Bulk Carrier",
        "built": 2010,
        "dwt": 75000,
        "flag": "Liberia",
        "owner": "Atlantic Shipping Ltd"
    },
    "IMO9234567": {
        "name": "Pacific Princess",
        "type": "Tanker",
        "built": 2018,
        "dwt": 50000,
        "flag": "Singapore",
        "owner": "Pacific Oil Transport"
    },
    "IMO9345678": {
        "name": "Mediterranean Express",
        "type": "Container Ship",
        "built": 2012,
        "dwt": 35000,
        "flag": "Malta",
        "owner": "Med Line Shipping"
    },
    "IMO9456789": {
        "name": "Indian Ocean Star",
        "type": "Reefer",
        "built": 2016,
        "dwt": 25000,
        "flag": "Marshall Islands",
        "owner": "Fresh Cargo Intl"
    }
}

# Route risk data
ROUTE_RISKS = {
    "Malacca Strait": {
        "piracy_incidents": 12,
        "score": 75,
        "description": "High traffic area with moderate piracy risk"
    },
    "Gulf of Aden": {
        "piracy_incidents": 3,
        "score": 65,
        "description": "Improved security but historical piracy concerns"
    },
    "South China Sea": {
        "piracy_incidents": 8,
        "score": 80,
        "description": "Geopolitical tensions and moderate piracy"
    },
    "Suez Canal": {
        "piracy_incidents": 0,
        "score": 30,
        "description": "Well-protected trade route"
    },
    "Panama Canal": {
        "piracy_incidents": 0,
        "score": 25,
        "description": "Secure international waterway"
    },
    "Strait of Hormuz": {
        "piracy_incidents": 2,
        "score": 85,
        "description": "Geopolitical tensions, critical oil route"
    }
}

# Weather risk data
WEATHER_RISKS = {
    "North Atlantic": {
        "season": "Winter",
        "risk_score": 70,
        "hazards": ["Heavy storms", "Rough seas"],
        "delay_probability": 0.35
    },
    "North Pacific": {
        "season": "Typhoon Season",
        "risk_score": 80,
        "hazards": ["Typhoons", "Heavy rain"],
        "delay_probability": 0.45
    },
    "Indian Ocean": {
        "season": "Monsoon",
        "risk_score": 65,
        "hazards": ["Monsoon winds", "Heavy rain"],
        "delay_probability": 0.30
    },
    "Mediterranean": {
        "season": "All Year",
        "risk_score": 30,
        "hazards": ["Occasional storms"],
        "delay_probability": 0.10
    }
}

# Historical applications (47+ samples)
def generate_historical_applications():
    routes = [
        ("Rotterdam", "Shanghai"),
        ("Singapore", "Los Angeles"),
        ("Dubai", "New York"),
        ("Hamburg", "Tokyo"),
        ("Shanghai", "Rotterdam"),
        ("Busan", "Long Beach"),
        ("Antwerp", "Singapore"),
        ("Santos", "Hamburg"),
        ("Mumbai", "Rotterdam"),
        ("Jebel Ali", "Singapore")
    ]
    
    cargo_types = ["Container", "Bulk", "Tanker", "Reefer", "RoRo"]
    owners = [
        "Maersk Line", "MSC Shipping", "CMA CGM", "Hapag-Lloyd",
        "Ocean Network Express", "Evergreen Marine", "COSCO",
        "Yang Ming Marine", "HMM Co", "ZIM Integrated Shipping",
        "Pacific International Lines", "Wan Hai Lines"
    ]
    
    decisions = ["Accept", "Accept with conditions", "Manual review"]
    
    applications = []
    base_date = datetime.now() - timedelta(days=1800)  # Start from ~5 years ago
    
    for i in range(50):
        route = random.choice(routes)
        cargo = random.choice(cargo_types)
        owner = random.choice(owners)
        vessel_age = random.randint(3, 22)
        
        # Calculate risk score based on factors
        base_risk = 35
        age_risk = vessel_age * 1.5
        route_risk = random.randint(10, 30)
        cargo_risk = {"Container": 5, "Bulk": 10, "Tanker": 15, "Reefer": 8, "RoRo": 12}[cargo]
        
        risk_score = min(95, base_risk + age_risk + route_risk + cargo_risk + random.randint(-10, 10))
        
        # Determine decision
        if risk_score < 40:
            decision = "Accept"
            premium = 1.0
        elif risk_score < 70:
            decision = "Accept with conditions"
            premium = 1.05 + (risk_score - 40) * 0.006
        else:
            decision = "Manual review"
            premium = 1.20 + (risk_score - 70) * 0.003
        
        app = {
            "vessel_name": f"{random.choice(['MV', 'SS', 'MS'])} {random.choice(['Ocean', 'Sea', 'Marine', 'Atlantic', 'Pacific'])} {random.choice(['Star', 'Pride', 'Glory', 'Spirit', 'Venture'])}",
            "imo_number": f"IMO{random.randint(9000000, 9999999)}",
            "owner": owner,
            "country_of_registry": random.choice(["Panama", "Liberia", "Marshall Islands", "Hong Kong", "Singapore", "Malta"]),
            "departure_port": route[0],
            "destination_port": route[1],
            "cargo_type": cargo,
            "vessel_age": vessel_age,
            "risk_score": round(risk_score, 2),
            "decision": decision,
            "premium_adjustment": round(premium, 3),
            "date": base_date + timedelta(days=i * 35),
            "underwriter": random.choice(["John Smith", "Sarah Johnson", "Michael Chen", "Emma Wilson"])
        }
        applications.append(app)
    
    return applications

# Mock claims data
MOCK_CLAIMS = [
    {
        "owner": "Ocean Freight LLC",
        "vessel_name": "MV Storm Runner",
        "imo_number": "IMO9876543",
        "claim_amount": 2500000.00,
        "claim_type": "Weather Damage",
        "date": datetime(2023, 8, 15),
        "status": "Settled",
        "description": "Severe storm damage to cargo containers during North Atlantic crossing"
    },
    {
        "owner": "Global Shipping Inc",
        "vessel_name": "SS Trade Wind",
        "imo_number": "IMO9765432",
        "claim_amount": 1200000.00,
        "claim_type": "Piracy Incident",
        "date": datetime(2023, 11, 3),
        "status": "Under Investigation",
        "description": "Attempted piracy in Gulf of Aden, crew safe but minor damage"
    },
    {
        "owner": "Neptune Maritime Corp",
        "vessel_name": "MV Neptune Star",
        "imo_number": "IMO9547821",
        "claim_amount": 450000.00,
        "claim_type": "Mechanical Failure",
        "date": datetime(2024, 2, 20),
        "status": "Approved",
        "description": "Engine failure requiring port repairs and cargo delay"
    }
]

# Maritime news sentiment data
NEWS_SENTIMENT = {
    "Neptune Maritime Corp": {
        "sentiment": "positive",
        "score": 0.75,
        "articles": [
            {"title": "Neptune Maritime Expands Fleet with Eco-Friendly Vessels", "date": "2024-01-15", "source": "Maritime News Today"},
            {"title": "Strong Safety Record Maintained by Neptune Maritime", "date": "2023-12-10", "source": "Shipping Gazette"}
        ]
    },
    "Atlantic Shipping Ltd": {
        "sentiment": "neutral",
        "score": 0.55,
        "articles": [
            {"title": "Atlantic Shipping Reports Steady Q4 Performance", "date": "2024-01-20", "source": "Trade Weekly"}
        ]
    }
}

# Port information
PORT_INFO = {
    "Rotterdam": {"country": "Netherlands", "risk_level": "Low", "congestion": "Medium"},
    "Shanghai": {"country": "China", "risk_level": "Low", "congestion": "High"},
    "Singapore": {"country": "Singapore", "risk_level": "Low", "congestion": "Medium"},
    "Los Angeles": {"country": "USA", "risk_level": "Low", "congestion": "High"},
    "Dubai": {"country": "UAE", "risk_level": "Low", "congestion": "Low"},
    "Hamburg": {"country": "Germany", "risk_level": "Low", "congestion": "Medium"},
    "Tokyo": {"country": "Japan", "risk_level": "Low", "congestion": "Medium"}
}

# Initialize historical applications
HISTORICAL_APPLICATIONS = generate_historical_applications()
