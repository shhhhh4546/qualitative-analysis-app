from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from database import SessionLocal, AnalysisResult, Conversation
from typing import Optional, List
from sqlalchemy import func

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{result_id}")
async def get_result(result_id: int, db: Session = Depends(get_db)):
    """Get a specific analysis result"""
    result = db.query(AnalysisResult).filter(AnalysisResult.id == result_id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    
    conversation = db.query(Conversation).filter(Conversation.id == result.conversation_id).first()
    
    return {
        "result_id": result.id,
        "conversation_id": result.conversation_id,
        "conversation_source": conversation.source if conversation else None,
        "pain_points": result.pain_points,
        "media_consumption": result.media_consumption,
        "compelling_points": result.compelling_points,
        "summary": result.summary,
        "confidence_score": result.confidence_score,
        "created_at": result.created_at.isoformat()
    }

@router.get("/conversation/{conversation_id}")
async def get_result_by_conversation(conversation_id: int, db: Session = Depends(get_db)):
    """Get analysis result for a specific conversation"""
    result = db.query(AnalysisResult).filter(
        AnalysisResult.conversation_id == conversation_id
    ).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Analysis not found for this conversation")
    
    return {
        "result_id": result.id,
        "conversation_id": result.conversation_id,
        "pain_points": result.pain_points,
        "media_consumption": result.media_consumption,
        "compelling_points": result.compelling_points,
        "summary": result.summary,
        "confidence_score": result.confidence_score,
        "created_at": result.created_at.isoformat()
    }

@router.get("/aggregate/summary")
async def get_aggregate_summary(
    source: Optional[str] = None,
    limit: int = Query(default=1000, le=10000),
    db: Session = Depends(get_db)
):
    """Get aggregated insights across all analyzed conversations"""
    query = db.query(AnalysisResult)
    
    if source:
        # Join with conversations to filter by source
        query = query.join(Conversation).filter(Conversation.source == source)
    
    results = query.limit(limit).all()
    
    if not results:
        return {
            "total_analyzed": 0,
            "pain_points": {},
            "media_consumption": {},
            "compelling_points": {},
            "top_insights": []
        }
    
    # Aggregate pain points
    pain_points_count = {}
    media_count = {}
    compelling_points_count = {}
    
    for result in results:
        # Count pain points
        if result.pain_points:
            for pain_point in result.pain_points:
                if isinstance(pain_point, dict):
                    text = pain_point.get("point", pain_point.get("text", str(pain_point)))
                else:
                    text = str(pain_point)
                pain_points_count[text] = pain_points_count.get(text, 0) + 1
        
        # Count media consumption
        if result.media_consumption:
            for media in result.media_consumption:
                if isinstance(media, dict):
                    name = media.get("name", media.get("source", str(media)))
                else:
                    name = str(media)
                media_count[name] = media_count.get(name, 0) + 1
        
        # Count compelling points
        if result.compelling_points:
            for point in result.compelling_points:
                if isinstance(point, dict):
                    text = point.get("point", point.get("text", str(point)))
                else:
                    text = str(point)
                compelling_points_count[text] = compelling_points_count.get(text, 0) + 1
    
    # Sort and get top items
    top_pain_points = sorted(pain_points_count.items(), key=lambda x: x[1], reverse=True)[:20]
    top_media = sorted(media_count.items(), key=lambda x: x[1], reverse=True)[:20]
    top_compelling = sorted(compelling_points_count.items(), key=lambda x: x[1], reverse=True)[:20]
    
    return {
        "total_analyzed": len(results),
        "pain_points": {
            "total_unique": len(pain_points_count),
            "top": [{"point": point, "count": count} for point, count in top_pain_points]
        },
        "media_consumption": {
            "total_unique": len(media_count),
            "top": [{"media": media, "count": count} for media, count in top_media]
        },
        "compelling_points": {
            "total_unique": len(compelling_points_count),
            "top": [{"point": point, "count": count} for point, count in top_compelling]
        }
    }

@router.get("/list/all")
async def list_all_results(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, le=1000),
    source: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all analysis results with pagination"""
    query = db.query(AnalysisResult)
    
    if source:
        query = query.join(Conversation).filter(Conversation.source == source)
    
    total = query.count()
    results = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "results": [
            {
                "result_id": r.id,
                "conversation_id": r.conversation_id,
                "summary": r.summary[:200] + "..." if r.summary and len(r.summary) > 200 else r.summary,
                "created_at": r.created_at.isoformat()
            }
            for r in results
        ]
    }

