from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./qualitative_analysis.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)  # gong, salesforce, planhat, etc.
    conversation_id = Column(String, unique=True, index=True)
    transcript = Column(Text)
    additional_data = Column(JSON)  # Additional data like date, participants, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    
class AnalysisResult(Base):
    __tablename__ = "analysis_results"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, index=True)
    pain_points = Column(JSON)  # List of pain points
    media_consumption = Column(JSON)  # List of media sources mentioned
    compelling_points = Column(JSON)  # List of compelling points
    summary = Column(Text)
    confidence_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

