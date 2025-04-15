from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from agent.agent import run_agent

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
        return {"error": "No question provided"}
        
    result = run_agent(question, context="youtube")
    return result

@app.post("/api/chat")
async def chat_question(request: Request):
    data = await request.json()
    question = data.get("question")
    
    if not question:
        return {"error": "No question provided"}
        
    result = run_agent(question, context="general")
    return result

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

# Create handler for Vercel
handler = Mangum(app) 