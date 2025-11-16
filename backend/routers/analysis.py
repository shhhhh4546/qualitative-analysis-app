from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from database import SessionLocal, Conversation, AnalysisResult
from services.analyzer import ConversationAnalyzer
from typing import Optional, List
import os

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/analyze/{conversation_id}")
async def analyze_conversation(
    conversation_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Analyze a single conversation"""
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Check if analysis already exists
    existing = db.query(AnalysisResult).filter(
        AnalysisResult.conversation_id == conversation_id
    ).first()
    
    if existing:
        return {
            "message": "Analysis already exists",
            "result_id": existing.id,
            "analysis": {
                "pain_points": existing.pain_points,
                "media_consumption": existing.media_consumption,
                "compelling_points": existing.compelling_points,
                "summary": existing.summary
            }
        }
    
    # Perform analysis
    try:
        analyzer = ConversationAnalyzer()
        result = analyzer.analyze(conversation.transcript)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Analysis failed: {str(e)}. Check your LLM configuration in .env file."
        )
    
    # Save result
    analysis_result = AnalysisResult(
        conversation_id=conversation_id,
        pain_points=result["pain_points"],
        media_consumption=result["media_consumption"],
        compelling_points=result["compelling_points"],
        summary=result["summary"],
        confidence_score=result.get("confidence_score", 0.0)
    )
    
    db.add(analysis_result)
    db.commit()
    db.refresh(analysis_result)
    
    return {
        "message": "Analysis completed",
        "result_id": analysis_result.id,
        "analysis": {
            "pain_points": analysis_result.pain_points,
            "media_consumption": analysis_result.media_consumption,
            "compelling_points": analysis_result.compelling_points,
            "summary": analysis_result.summary
        }
    }

@router.post("/analyze-batch")
async def analyze_batch(
    conversation_ids: Optional[List[int]] = None,
    source: Optional[str] = None,
    limit: int = 100,
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """Analyze multiple conversations in batch"""
    # Get conversations to analyze
    query = db.query(Conversation)
    
    if conversation_ids:
        query = query.filter(Conversation.id.in_(conversation_ids))
    elif source:
        query = query.filter(Conversation.source == source)
    
    conversations = query.limit(limit).all()
    
    if not conversations:
        raise HTTPException(status_code=404, detail="No conversations found")
    
    # Initialize analyzer once (creates/reuses model)
    try:
        analyzer = ConversationAnalyzer()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initialize analyzer: {str(e)}. Check your LLM configuration in .env file."
        )
    
    results = []
    errors = []
    
    for conversation in conversations:
        try:
            # Check if analysis already exists
            existing = db.query(AnalysisResult).filter(
                AnalysisResult.conversation_id == conversation.id
            ).first()
            
            if existing:
                results.append({
                    "conversation_id": conversation.id,
                    "status": "already_analyzed",
                    "result_id": existing.id
                })
                continue
            
            # Perform analysis
            analysis = analyzer.analyze(conversation.transcript)
            
            # Save result
            analysis_result = AnalysisResult(
                conversation_id=conversation.id,
                pain_points=analysis["pain_points"],
                media_consumption=analysis["media_consumption"],
                compelling_points=analysis["compelling_points"],
                summary=analysis["summary"],
                confidence_score=analysis.get("confidence_score", 0.0)
            )
            
            db.add(analysis_result)
            results.append({
                "conversation_id": conversation.id,
                "status": "analyzed",
                "result_id": analysis_result.id
            })
            
        except Exception as e:
            errors.append({
                "conversation_id": conversation.id,
                "error": str(e)
            })
    
    db.commit()
    
    return {
        "message": f"Analyzed {len(results)} conversations",
        "analyzed": len([r for r in results if r["status"] == "analyzed"]),
        "already_analyzed": len([r for r in results if r["status"] == "already_analyzed"]),
        "results": results,
        "errors": errors if errors else None
    }

@router.get("/status/{conversation_id}")
async def get_analysis_status(conversation_id: int, db: Session = Depends(get_db)):
    """Check if a conversation has been analyzed"""
    result = db.query(AnalysisResult).filter(
        AnalysisResult.conversation_id == conversation_id
    ).first()
    
    if not result:
        return {"analyzed": False}
    
    return {
        "analyzed": True,
        "result_id": result.id,
        "created_at": result.created_at.isoformat()
    }

