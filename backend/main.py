from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from dotenv import load_dotenv
import os

from database import SessionLocal, init_db
from routers import upload, analysis, results

load_dotenv()

app = FastAPI(
    title="Qualitative Data Analysis API",
    description="API for analyzing customer conversation data",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Include routers
app.include_router(upload.router, prefix="/api/upload", tags=["upload"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])
app.include_router(results.router, prefix="/api/results", tags=["results"])

@app.get("/")
async def root():
    return {"message": "Qualitative Data Analysis API", "status": "running"}

@app.get("/api/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/config")
async def get_config():
    """Get current LLM configuration"""
    provider = os.getenv("LLM_PROVIDER", "huggingface").lower()
    config = {
        "provider": provider,
    }
    
    if provider == "openai":
        config["model"] = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
        config["has_api_key"] = bool(os.getenv("OPENAI_API_KEY"))
    elif provider == "huggingface":
        config["model"] = os.getenv("HUGGINGFACE_MODEL", "microsoft/Phi-3-mini-4k-instruct")
        
    return config

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=True
    )

