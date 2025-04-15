# agent.py

import os
import logging
from dotenv import load_dotenv
from typing import Dict, Any
import google.generativeai as genai
from googleapiclient.discovery import build
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from .youtube_utils import extract_channel_name, get_latest_videos, get_video_info

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env
load_dotenv()

# Verify required environment variables
required_env_vars = ["GEMINI_API_KEY", "PINECONE_API_KEY"]
for var in required_env_vars:
    if not os.getenv(var):
        raise EnvironmentError(f"Missing required environment variable: {var}")

# Map GEMINI_API_KEY to what LangChain expects
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

from langchain_core.prompts import PromptTemplate
from .memory import store_memory, retrieve_memory

# Initialize models
try:
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")
except Exception as e:
    logger.error(f"Failed to initialize AI models: {str(e)}")
    raise

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', 'AIzaSyATUUbrkJyOuMp_RimQatbsM0fhviZtWJU')

# Initialize Gemini model
GEMINI_MODEL = 'gemini-1.5-pro'

def get_youtube_client():
    return build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def get_channel_id(youtube, channel_name: str) -> str:
    """Get channel ID from channel name"""
    try:
        request = youtube.search().list(
            q=channel_name,
            type='channel',
            part='id',
            maxResults=1
        )
        response = request.execute()
        if response['items']:
            return response['items'][0]['id']['channelId']
    except Exception as e:
        logger.error(f"Error getting channel ID: {str(e)}")
    return None

def get_channel_videos(youtube, channel_id: str, max_results: int = 10):
    """Get latest videos from a channel"""
    try:
        request = youtube.search().list(
            channelId=channel_id,
            type='video',
            part='id,snippet',
            order='date',
            maxResults=max_results
        )
        response = request.execute()
        video_ids = [item['id']['videoId'] for item in response['items']]
        
        # Get video statistics
        stats_request = youtube.videos().list(
            part='statistics',
            id=','.join(video_ids)
        )
        stats_response = stats_request.execute()
        
        videos = []
        for video, stats in zip(response['items'], stats_response['items']):
            videos.append({
                'title': video['snippet']['title'],
                'videoId': video['id']['videoId'],
                'views': int(stats['statistics'].get('viewCount', 0)),
                'likes': int(stats['statistics'].get('likeCount', 0)),
                'comments': int(stats['statistics'].get('commentCount', 0)),
                'publishedAt': video['snippet']['publishedAt']
            })
        return videos
    except Exception as e:
        logger.error(f"Error getting channel videos: {str(e)}")
        return []

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
