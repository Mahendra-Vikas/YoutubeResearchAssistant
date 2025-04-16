import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv
from youtube_utils import get_channel_info, get_latest_videos, extract_channel_name
import pinecone
from typing import Dict, Any, Optional

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Verify required environment variables
required_vars = [
    "GEMINI_API_KEY",
    "PINECONE_API_KEY",
    "PINECONE_INDEX",
    "PINECONE_CLOUD",
    "PINECONE_REGION"
]

for var in required_vars:
    if not os.getenv(var):
        logger.error(f"Missing required environment variable: {var}")
        raise EnvironmentError(f"Missing required environment variable: {var}")

# Initialize Gemini
try:
    logger.info("Initializing Gemini...")
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    logger.info("Gemini initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Gemini: {str(e)}")
    raise

# Initialize Pinecone
try:
    logger.info("Initializing Pinecone...")
    pinecone.init(
        api_key=os.getenv("PINECONE_API_KEY"),
        environment=f"{os.getenv('PINECONE_CLOUD')}-{os.getenv('PINECONE_REGION')}"
    )
    index = pinecone.Index(os.getenv("PINECONE_INDEX"))
    logger.info("Pinecone initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Pinecone: {str(e)}")
    raise

def analyze_youtube_query(query: str) -> Dict[str, Any]:
    """
    Analyze a YouTube-related query and fetch relevant information.
    """
    try:
        logger.info(f"Analyzing YouTube query: {query}")
        channel_name = extract_channel_name(query)
        if not channel_name:
            logger.warning(f"Could not extract channel name from query: {query}")
            return {"error": "Could not extract channel name from query"}

        logger.info(f"Extracted channel name: {channel_name}")
        channel_info = get_channel_info(channel_name)
        if not channel_info:
            logger.warning(f"Could not find channel information for: {channel_name}")
            return {"error": f"Could not find channel information for {channel_name}"}

        logger.info(f"Fetching latest videos for channel: {channel_name}")
        latest_videos = get_latest_videos(channel_name, max_results=5)
        
        result = {
            "channel_info": channel_info,
            "latest_videos": latest_videos,
            "query": query
        }
        logger.info("Successfully analyzed YouTube query")
        return result
    except Exception as e:
        logger.error(f"Error analyzing YouTube query: {str(e)}", exc_info=True)
        return {"error": f"Failed to analyze YouTube query: {str(e)}"}

def run_agent(question: str, context: str = "general") -> Dict[str, Any]:
    """
    Run the agent with the given question and context.
    """
    try:
        logger.info(f"Running agent with question: {question}, context: {context}")
        
        if context == "youtube":
            # Handle YouTube-specific queries
            youtube_data = analyze_youtube_query(question)
            if "error" in youtube_data:
                logger.warning(f"YouTube analysis error: {youtube_data['error']}")
                return youtube_data

            # Generate response using Gemini
            prompt = f"""
            Question: {question}
            Channel Info: {youtube_data['channel_info']}
            Latest Videos: {youtube_data['latest_videos']}
            Please provide a detailed analysis based on this information.
            """
            
            logger.info("Generating response with Gemini")
            response = model.generate_content(prompt)
            result = {
                "answer": response.text,
                "youtube_data": youtube_data
            }
            logger.info("Successfully generated response")
            return result
        else:
            # Handle general queries using Gemini
            logger.info("Processing general query with Gemini")
            response = model.generate_content(question)
            result = {"answer": response.text}
            logger.info("Successfully generated response")
            return result
            
    except Exception as e:
        logger.error(f"Error in run_agent: {str(e)}", exc_info=True)
        return {"error": f"Failed to process query: {str(e)}"} 