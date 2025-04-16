import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from dotenv import load_dotenv
from agent import run_agent

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
        raise EnvironmentError(f"Missing required environment variable: {var}")

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/youtube")
async def youtube_question(request: Request):
    data = await request.json()
    question = data.get("question")
    
    if not question:
        raise HTTPException(status_code=400, detail="Question is required")
        
    result = run_agent(question, context="youtube")
    return result

@app.post("/api/chat")
async def chat_question(request: Request):
    data = await request.json()
    question = data.get("question")
    
    if not question:
        raise HTTPException(status_code=400, detail="Question is required")
        
    result = run_agent(question, context="general")
    return result

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

# Create handler for AWS Lambda
handler = Mangum(app) 