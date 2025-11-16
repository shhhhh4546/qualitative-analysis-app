from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import SessionLocal, Conversation
import pandas as pd
import json
from typing import List
import uuid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/csv")
async def upload_csv(file: UploadFile = File(...), source: str = "unknown", db: Session = Depends(get_db)):
    """Upload and process CSV file with conversation data"""
    try:
        # Read CSV file
        contents = await file.read()
        df = pd.read_csv(pd.io.common.BytesIO(contents))
        
        # Expected columns: transcript, conversation_id (optional), metadata (optional)
        if "transcript" not in df.columns:
            raise HTTPException(status_code=400, detail="CSV must contain 'transcript' column")
        
        uploaded_count = 0
        skipped_count = 0
        errors = []
        conversations_to_add = []
        
        # Generate conversation IDs for all rows
        conversation_ids = []
        for idx, row in df.iterrows():
            conversation_id = row.get("conversation_id") or f"{source}_{uuid.uuid4().hex[:8]}"
            conversation_ids.append(conversation_id)
        
        # Batch check for existing conversations (single query instead of N queries)
        existing_ids = set(
            db.query(Conversation.conversation_id)
            .filter(Conversation.conversation_id.in_(conversation_ids))
            .all()
        )
        existing_ids = {row[0] for row in existing_ids}
        
        # Process rows and prepare for bulk insert
        for idx, row in df.iterrows():
            try:
                conversation_id = conversation_ids[idx]
                
                # Skip if already exists
                if conversation_id in existing_ids:
                    skipped_count += 1
                    continue
                
                transcript = str(row["transcript"])
                
                # Extract metadata
                additional_data = {}
                for col in df.columns:
                    if col not in ["transcript", "conversation_id"]:
                        additional_data[col] = str(row[col]) if pd.notna(row[col]) else None
                
                conversation = Conversation(
                    source=source,
                    conversation_id=conversation_id,
                    transcript=transcript,
                    additional_data=additional_data
                )
                
                conversations_to_add.append(conversation)
                uploaded_count += 1
                
            except Exception as e:
                errors.append(f"Row {idx}: {str(e)}")
        
        # Bulk insert all conversations at once (much faster)
        if conversations_to_add:
            db.add_all(conversations_to_add)
            db.commit()
        
        return {
            "message": f"Successfully uploaded {uploaded_count} conversations. Skipped {skipped_count} existing conversations.",
            "uploaded": uploaded_count,
            "skipped": skipped_count,
            "errors": errors if errors else None
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")

@router.post("/json")
async def upload_json(file: UploadFile = File(...), source: str = "unknown", db: Session = Depends(get_db)):
    """Upload and process JSON file with conversation data"""
    try:
        contents = await file.read()
        data = json.loads(contents)
        
        # Handle both single object and array
        if isinstance(data, dict):
            data = [data]
        
        uploaded_count = 0
        skipped_count = 0
        errors = []
        conversations_to_add = []
        
        # Generate conversation IDs and validate transcripts
        conversation_ids = []
        valid_items = []
        for idx, item in enumerate(data):
            try:
                conversation_id = item.get("conversation_id") or f"{source}_{uuid.uuid4().hex[:8]}"
                transcript = item.get("transcript") or item.get("text") or item.get("content")
                
                if not transcript:
                    errors.append(f"Item {idx}: Missing transcript field")
                    continue
                
                conversation_ids.append(conversation_id)
                valid_items.append((idx, item, conversation_id))
            except Exception as e:
                errors.append(f"Item {idx}: {str(e)}")
        
        # Batch check for existing conversations (single query instead of N queries)
        if conversation_ids:
            existing_ids = set(
                db.query(Conversation.conversation_id)
                .filter(Conversation.conversation_id.in_(conversation_ids))
                .all()
            )
            existing_ids = {row[0] for row in existing_ids}
            
            # Process valid items
            for idx, item, conversation_id in valid_items:
                try:
                    # Skip if already exists
                    if conversation_id in existing_ids:
                        skipped_count += 1
                        continue
                    
                    transcript = item.get("transcript") or item.get("text") or item.get("content")
                    
                    # Extract metadata (everything except transcript and conversation_id)
                    additional_data = {k: v for k, v in item.items() if k not in ["transcript", "text", "content", "conversation_id"]}
                    
                    conversation = Conversation(
                        source=source,
                        conversation_id=conversation_id,
                        transcript=str(transcript),
                        additional_data=additional_data
                    )
                    
                    conversations_to_add.append(conversation)
                    uploaded_count += 1
                    
                except Exception as e:
                    errors.append(f"Item {idx}: {str(e)}")
        
        # Bulk insert all conversations at once (much faster)
        if conversations_to_add:
            db.add_all(conversations_to_add)
            db.commit()
        
        return {
            "message": f"Successfully uploaded {uploaded_count} conversations. Skipped {skipped_count} existing conversations.",
            "uploaded": uploaded_count,
            "skipped": skipped_count,
            "errors": errors if errors else None
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing JSON: {str(e)}")

@router.get("/stats")
async def get_upload_stats(db: Session = Depends(get_db)):
    """Get statistics about uploaded conversations"""
    total = db.query(Conversation).count()
    by_source = db.query(Conversation.source, func.count(Conversation.id)).group_by(Conversation.source).all()
    
    return {
        "total_conversations": total,
        "by_source": {source: count for source, count in by_source}
    }

