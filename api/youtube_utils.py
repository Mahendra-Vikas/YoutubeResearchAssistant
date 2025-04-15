import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

logger = logging.getLogger(__name__)

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', 'AIzaSyATUUbrkJyOuMp_RimQatbsM0fhviZtWJU')

def get_youtube_client():
    """Get authenticated YouTube client"""
    try:
        return build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    except Exception as e:
        logger.error(f"Error creating YouTube client: {str(e)}")
        return None

def format_number(num: int) -> str:
    """Format large numbers in a readable way"""
    if num >= 1000000000:
        return f"{num/1000000000:.1f}B"
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    if num >= 1000:
        return f"{num/1000:.1f}K"
    return str(num)

def extract_channel_name(query: str) -> Optional[str]:
    """Extract channel name from query"""
    query = query.lower()
    
    # Try different patterns
    patterns = [
        ("channel", "channel"),
        ("from", "from"),
        ("by", "by")
    ]
    
    for keyword, pattern in patterns:
        if pattern in query:
            parts = query.split(pattern)
            if len(parts) > 1:
                # Get the part after the pattern and clean it
                channel = parts[1].strip().strip('"').strip("'").strip()
                # Remove common words that might follow the channel name
                stop_words = ["latest", "video", "videos", "content", "and", "show", "me", "the"]
                for word in stop_words:
                    if f" {word} " in channel:
                        channel = channel.split(f" {word} ")[0].strip()
                return channel
    
    return None

def get_channel_info(channel_name: str) -> Dict[str, Any]:
    """Get channel information using YouTube Data API"""
    try:
        youtube = get_youtube_client()
        if not youtube:
            return {"success": False, "error": "Could not initialize YouTube client"}

        # Search for the channel
        search_response = youtube.search().list(
            q=channel_name,
            type='channel',
            part='id,snippet',
            maxResults=1
        ).execute()

        if not search_response.get('items'):
            return {"success": False, "error": f"Channel '{channel_name}' not found"}

        channel_id = search_response['items'][0]['id']['channelId']
        channel_title = search_response['items'][0]['snippet']['title']

        # Get channel statistics
        channel_response = youtube.channels().list(
            part='statistics',
            id=channel_id
        ).execute()

        if not channel_response.get('items'):
            return {"success": False, "error": "Could not fetch channel statistics"}

        stats = channel_response['items'][0]['statistics']

        return {
            "success": True,
            "channel_id": channel_id,
            "channel_name": channel_title,
            "subscriber_count": int(stats.get('subscriberCount', 0)),
            "video_count": int(stats.get('videoCount', 0)),
            "view_count": int(stats.get('viewCount', 0))
        }

    except HttpError as e:
        logger.error(f"YouTube API error: {str(e)}")
        return {"success": False, "error": f"YouTube API error: {str(e)}"}
    except Exception as e:
        logger.error(f"Error fetching channel info: {str(e)}")
        return {"success": False, "error": str(e)}

def get_latest_videos(channel_name: str, max_results: int = 5) -> Dict[str, Any]:
    """Get latest videos from a channel using YouTube Data API"""
    try:
        channel_info = get_channel_info(channel_name)
        if not channel_info["success"]:
            return channel_info

        youtube = get_youtube_client()
        if not youtube:
            return {"success": False, "error": "Could not initialize YouTube client"}

        # Get channel's latest videos
        videos_response = youtube.search().list(
            channelId=channel_info["channel_id"],
            order="date",
            part="id,snippet",
            type="video",
            maxResults=max_results
        ).execute()

        if not videos_response.get('items'):
            return {
                "success": False,
                "error": f"No videos found for channel '{channel_name}'"
            }

        # Get video IDs
        video_ids = [item['id']['videoId'] for item in videos_response['items']]

        # Get detailed video statistics
        videos_stats = youtube.videos().list(
            part="statistics,snippet",
            id=','.join(video_ids)
        ).execute()

        videos = []
        for video in videos_stats['items']:
            stats = video['statistics']
            snippet = video['snippet']
            
            video_data = {
                "title": snippet['title'],
                "videoId": video['id'],
                "view_count": int(stats.get('viewCount', 0)),
                "like_count": int(stats.get('likeCount', 0)),
                "comment_count": int(stats.get('commentCount', 0)),
                "publish_date": snippet['publishedAt'],
                "thumbnail": snippet['thumbnails']['high']['url'],
                "description": snippet['description']
            }
            videos.append(video_data)

        # Format response with emojis and readable numbers
        formatted_videos = []
        for video in videos:
            stats_parts = [
                f"👁️ {format_number(video['view_count'])} views",
                f"👍 {format_number(video['like_count'])} likes",
                f"💬 {format_number(video['comment_count'])} comments"
            ]
            formatted_videos.append(
                f"📺 {video['title']}\n   {' • '.join(stats_parts)}"
            )

        return {
            "success": True,
            "channel_name": channel_info["channel_name"],
            "channel_stats": {
                "subscribers": format_number(channel_info["subscriber_count"]),
                "total_views": format_number(channel_info["view_count"]),
                "video_count": channel_info["video_count"]
            },
            "videos": videos,
            "formatted_response": "\n\n".join([
                f"📊 Channel Stats for {channel_info['channel_name']}:",
                f"👥 {format_number(channel_info['subscriber_count'])} subscribers",
                f"👁️ {format_number(channel_info['view_count'])} total views",
                f"📼 {channel_info['video_count']} videos\n",
                "Latest Videos:",
                *formatted_videos
            ])
        }

    except HttpError as e:
        logger.error(f"YouTube API error: {str(e)}")
        return {"success": False, "error": f"YouTube API error: {str(e)}"}
    except Exception as e:
        logger.error(f"Error fetching videos: {str(e)}")
        return {"success": False, "error": str(e)} 