import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv
from youtube_utils import get_channel_info, get_latest_videos, extract_channel_name
import pinecone
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Gemini
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    logger.error(f"Failed to initialize Gemini: {str(e)}")
    raise

# Initialize Pinecone
try:
    pinecone.init(
        api_key=os.getenv("PINECONE_API_KEY"),
        environment=f"{os.getenv('PINECONE_CLOUD')}-{os.getenv('PINECONE_REGION')}"
    )
    index = pinecone.Index(os.getenv("PINECONE_INDEX"))
except Exception as e:
    logger.error(f"Failed to initialize Pinecone: {str(e)}")
    raise

def analyze_youtube_query(query: str) -> Dict[str, Any]:
    """
    Analyze a YouTube-related query and fetch relevant information.
    """
    try:
        channel_name = extract_channel_name(query)
        if not channel_name:
            return {"error": "Could not extract channel name from query"}

        channel_info = get_channel_info(channel_name)
        if not channel_info:
            return {"error": f"Could not find channel information for {channel_name}"}

        latest_videos = get_latest_videos(channel_name, max_results=5)
        
        return {
            "channel_info": channel_info,
            "latest_videos": latest_videos,
            "query": query
        }
    except Exception as e:
        logger.error(f"Error analyzing YouTube query: {str(e)}")
        return {"error": f"Failed to analyze YouTube query: {str(e)}"}

def run_agent(question: str, context: str = "general") -> Dict[str, Any]:
    """
    Run the agent with the given question and context.
    """
    try:
        if context == "youtube":
            # Handle YouTube-specific queries
            youtube_data = analyze_youtube_query(question)
            if "error" in youtube_data:
                return youtube_data

            # Generate response using Gemini
            prompt = f"""
            Question: {question}
            Channel Info: {youtube_data['channel_info']}
            Latest Videos: {youtube_data['latest_videos']}
            Please provide a detailed analysis based on this information.
            """
            
            response = model.generate_content(prompt)
            return {
                "answer": response.text,
                "youtube_data": youtube_data
            }
        else:
            # Handle general queries using Gemini
            response = model.generate_content(question)
            return {"answer": response.text}
            
    except Exception as e:
        logger.error(f"Error in run_agent: {str(e)}")
        return {"error": f"Failed to process query: {str(e)}"} 