from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Text
from datetime import datetime
from database.connection import Base

class Application(Base):
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    vessel_name = Column(String, index=True)
    imo_number = Column(String, index=True)
    owner = Column(String, index=True)
    country_of_registry = Column(String)
    departure_port = Column(String)
    destination_port = Column(String)
    cargo_type = Column(String)
    vessel_age = Column(Integer)
    risk_score = Column(Float)
    decision = Column(String)
    premium_adjustment = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)
    underwriter = Column(String)
    full_data = Column(JSON)

class Claim(Base):
    __tablename__ = "claims"
    
    id = Column(Integer, primary_key=True, index=True)
    owner = Column(String, index=True)
    vessel_name = Column(String)
    imo_number = Column(String)
    claim_amount = Column(Float)
    claim_type = Column(String)
    date = Column(DateTime)
    status = Column(String)
    description = Column(Text)
