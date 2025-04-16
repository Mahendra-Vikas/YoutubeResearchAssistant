import os
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from agent import run_agent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Verify required environment variables
required_env_vars = [
    "GEMINI_API_KEY",
    "PINECONE_API_KEY",
    "YOUTUBE_API_KEY",
    "PINECONE_INDEX",
    "PINECONE_CLOUD",
    "PINECONE_REGION"
]

for var in required_env_vars:
    if not os.getenv(var):
        logger.error(f"Missing required environment variable: {var}")
        raise EnvironmentError(f"Missing required environment variable: {var}")

app = FastAPI()

# Configure CORS with more specific settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.post("/api/youtube")
async def youtube_question(request: Request):
    try:
        logger.info("Received YouTube question request")
        data = await request.json()
        question = data.get("question")
        if not question:
            raise HTTPException(status_code=400, detail="Question is required")
        
        result = run_agent(question, context="youtube")
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Error processing YouTube question: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat_question(request: Request):
    try:
        logger.info("Received chat question request")
        data = await request.json()
        question = data.get("question")
        if not question:
            raise HTTPException(status_code=400, detail="Question is required")
        
        result = run_agent(question)
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Error processing chat question: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"} 