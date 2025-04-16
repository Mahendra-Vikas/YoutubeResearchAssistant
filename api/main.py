from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from agent.agent import run_agent, get_youtube_client
from typing import Optional, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000"
    ],  # Allow both development servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request and Response schemas
class Query(BaseModel):
    question: str

class YouTubeResponse(BaseModel):
    response: str
    data: Optional[Dict[str, Any]] = None
    success: bool = True
    error: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    success: bool = True
    error: Optional[str] = None

# Error handler for generic exceptions
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error processing request: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "success": False
        }
    )

# Route to process YouTube-related questions
@app.post("/youtube", response_model=YouTubeResponse)
async def youtube_question(query: Query):
    try:
        logger.info(f"Received YouTube question: {query.question}")
        
        # Call your main agent logic with YouTube-specific context
        result = run_agent(query.question, context="youtube")
        
        response = YouTubeResponse(
            response=result["response"],
            data=result.get("data", {}),
            success=True
        )
        
        logger.info("Successfully processed YouTube question")
        return response
        
    except Exception as e:
        logger.error(f"Error processing YouTube question: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# Route to process general chat questions
@app.post("/chat", response_model=ChatResponse)
async def chat_question(query: Query):
    try:
        logger.info(f"Received chat question: {query.question}")
        
        # Call your main agent logic with general context
        result = run_agent(query.question, context="general")
        
        response = ChatResponse(
            response=result["response"],
            success=True
        )
        
        logger.info("Successfully processed chat question")
        return response
        
    except Exception as e:
        logger.error(f"Error processing chat question: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# Test route for YouTube API
@app.get("/test-youtube")
async def test_youtube_api():
    try:
        youtube = get_youtube_client()
        # Try to get MrBeast's channel info as a test
        request = youtube.search().list(
            q="MrBeast",
            type='channel',
            part='id,snippet',
            maxResults=1
        )
        response = request.execute()
        
        if response and 'items' in response:
            return {
                "status": "success",
                "message": "YouTube API is working",
                "data": response['items'][0] if response['items'] else None
            }
        else:
            return {
                "status": "error",
                "message": "No results found"
            }
            
    except Exception as e:
        logger.error(f"YouTube API test failed: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }

# Root route for testing
@app.get("/")
def read_root():
    return {
        "status": "healthy",
        "message": "YouTube Research Assistant API is running"
    }
