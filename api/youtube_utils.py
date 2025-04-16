import os
import logging
from typing import Dict, Any, List, Optional
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def get_youtube_client():
    """
    Create and return an authenticated YouTube client.
    """
    try:
        api_key = os.getenv("YOUTUBE_API_KEY")
        if not api_key:
            raise ValueError("YOUTUBE_API_KEY environment variable is not set")
        
        return build("youtube", "v3", developerKey=api_key)
    except Exception as e:
        logger.error(f"Failed to create YouTube client: {str(e)}")
        raise

def format_number(num: int) -> str:
    """
    Format large numbers into readable strings (e.g., 1000000 -> 1M).
    """
    if num >= 1000000000:
        return f"{num/1000000000:.1f}B"
    elif num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num/1000:.1f}K"
    return str(num)

def extract_channel_name(query: str) -> Optional[str]:
    """
    Extract channel name from a query string.
    """
    query = query.lower()
    keywords = ["channel", "videos", "latest", "stats", "statistics", "info", "about"]
    
    # Remove common words and punctuation
    words = query.replace("'s", "").replace("?", "").replace(".", "").split()
    
    # Look for words that come after keywords
    for i, word in enumerate(words):
        if word in keywords and i + 1 < len(words):
            return words[i + 1]
            
    # If no keyword found, look for capitalized words in original query
    original_words = query.split()
    for word in original_words:
        if word[0].isupper():
            return word.lower()
            
    return None

def get_channel_info(channel_name: str) -> Optional[Dict[str, Any]]:
    """
    Get channel information including subscriber count and video statistics.
    """
    try:
        youtube = get_youtube_client()
        
        # Search for the channel
        search_response = youtube.search().list(
            q=channel_name,
            type="channel",
            part="id,snippet",
            maxResults=1
        ).execute()
        
        if not search_response.get("items"):
            logger.warning(f"No channel found for name: {channel_name}")
            return None
            
        channel_id = search_response["items"][0]["id"]["channelId"]
        
        # Get channel statistics
        channel_response = youtube.channels().list(
            part="statistics,snippet",
            id=channel_id
        ).execute()
        
        if not channel_response.get("items"):
            logger.warning(f"No statistics found for channel ID: {channel_id}")
            return None
            
        channel = channel_response["items"][0]
        stats = channel["statistics"]
        
        return {
            "name": channel["snippet"]["title"],
            "description": channel["snippet"]["description"],
            "subscriber_count": format_number(int(stats["subscriberCount"])),
            "video_count": format_number(int(stats["videoCount"])),
            "view_count": format_number(int(stats["viewCount"])),
            "channel_id": channel_id
        }
        
    except HttpError as e:
        logger.error(f"YouTube API error: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Error getting channel info: {str(e)}")
        return None

def get_latest_videos(channel_name: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Get the latest videos from a channel with detailed statistics.
    """
    try:
        youtube = get_youtube_client()
        
        # First get channel ID
        channel_info = get_channel_info(channel_name)
        if not channel_info:
            return []
            
        # Get latest videos
        videos_response = youtube.search().list(
            channelId=channel_info["channel_id"],
            order="date",
            part="id,snippet",
            maxResults=max_results,
            type="video"
        ).execute()
        
        if not videos_response.get("items"):
            return []
            
        # Get detailed video statistics
        video_ids = [item["id"]["videoId"] for item in videos_response["items"]]
        videos_stats = youtube.videos().list(
            part="statistics,contentDetails",
            id=",".join(video_ids)
        ).execute()
        
        # Combine video information
        videos = []
        for video, stats in zip(videos_response["items"], videos_stats["items"]):
            videos.append({
                "title": video["snippet"]["title"],
                "description": video["snippet"]["description"],
                "published_at": video["snippet"]["publishedAt"],
                "views": format_number(int(stats["statistics"]["viewCount"])),
                "likes": format_number(int(stats["statistics"].get("likeCount", 0))),
                "comments": format_number(int(stats["statistics"].get("commentCount", 0))),
                "duration": stats["contentDetails"]["duration"],
                "url": f"https://youtube.com/watch?v={video['id']['videoId']}"
            })
            
        return videos
        
    except HttpError as e:
        logger.error(f"YouTube API error: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Error getting latest videos: {str(e)}")
        return [] 