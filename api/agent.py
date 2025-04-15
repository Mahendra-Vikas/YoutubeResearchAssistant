import os
import logging
from dotenv import load_dotenv
from typing import Dict, Any
import google.generativeai as genai
from googleapiclient.discovery import build
from langchain_google_genai import ChatGoogleGenerativeAI
from youtube_utils import extract_channel_name, get_latest_videos, get_video_info

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Verify required environment variables
required_env_vars = ["GEMINI_API_KEY", "PINECONE_API_KEY"]
for var in required_env_vars:
    if not os.getenv(var):
        raise EnvironmentError(f"Missing required environment variable: {var}")

# Map GEMINI_API_KEY to what LangChain expects
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

# Initialize models
try:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")
except Exception as e:
    logger.error(f"Failed to initialize AI models: {str(e)}")
    raise

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def analyze_youtube_query(question: str) -> Dict[str, Any]:
    """Analyze if the question is about YouTube data"""
    try:
        question = question.lower()
        
        # Extract channel name from the question
        channel_name = extract_channel_name(question)
        
        if channel_name:
            # Get channel's latest videos and stats
            result = get_latest_videos(channel_name)
            
            if result["success"]:
                return {
                    "type": "channel",
                    "data": result,
                    "response": result["formatted_response"]
                }
            else:
                return {
                    "type": "error",
                    "error": result["error"],
                    "response": f"I encountered an error while fetching data for {channel_name}: {result['error']}"
                }
        
        return {
            "type": "unknown",
            "response": "I couldn't identify a specific YouTube channel in your question. Try asking about a specific channel, for example: 'Show me MrBeast's latest videos' or 'What are PewDiePie's channel stats?'"
        }
        
    except Exception as e:
        logger.error(f"Error analyzing YouTube query: {str(e)}")
        return {
            "type": "error",
            "error": str(e),
            "response": "I encountered an error while processing your request. Please try again or rephrase your question."
        }

def run_agent(question: str, context: str = "general") -> Dict[str, Any]:
    """Run the agent with the given question and context"""
    try:
        if context == "youtube":
            # Analyze YouTube-specific questions
            result = analyze_youtube_query(question)
            
            if result["type"] == "channel":
                return {
                    "response": result["response"],
                    "data": result["data"]
                }
            elif result["type"] == "error":
                return {
                    "response": result["response"],
                    "error": result.get("error")
                }
            else:
                return {
                    "response": result["response"]
                }
            
        # For general chat or unknown contexts, use the LLM
        response = llm.invoke(question).content
        return {"response": response}
            
    except Exception as e:
        logger.error(f"Error running agent: {str(e)}")
        return {
            "response": "I apologize, but I encountered an error processing your request. Please try again or rephrase your question.",
            "error": str(e)
        } 