const YOUTUBE_API_KEY = 'AIzaSyATUUbrkJyOuMp_RimQatbsM0fhviZtWJU';
const YOUTUBE_API_BASE_URL = 'https://www.googleapis.com/youtube/v3';

export interface YouTubeVideo {
  id: string;
  title: string;
  description: string;
  thumbnail: string;
  viewCount: string;
  likeCount: string;
  publishedAt: string;
  channelTitle: string;
}

export interface YouTubeChannel {
  id: string;
  title: string;
  description: string;
  thumbnail: string;
  subscriberCount: string;
  videoCount: string;
}

export const youtubeService = {
  async searchVideos(query: string): Promise<YouTubeVideo[]> {
    const response = await fetch(
      `${YOUTUBE_API_BASE_URL}/search?part=snippet&maxResults=10&q=${encodeURIComponent(
        query
      )}&type=video&key=${YOUTUBE_API_KEY}`
    );
    const data = await response.json();
    
    // Get video statistics in a separate call
    const videoIds = data.items.map((item: any) => item.id.videoId).join(',');
    const statsResponse = await fetch(
      `${YOUTUBE_API_BASE_URL}/videos?part=statistics&id=${videoIds}&key=${YOUTUBE_API_KEY}`
    );
    const statsData = await statsResponse.json();

    return data.items.map((item: any, index: number) => ({
      id: item.id.videoId,
      title: item.snippet.title,
      description: item.snippet.description,
      thumbnail: item.snippet.thumbnails.medium.url,
      viewCount: statsData.items[index]?.statistics.viewCount || '0',
      likeCount: statsData.items[index]?.statistics.likeCount || '0',
      publishedAt: item.snippet.publishedAt,
      channelTitle: item.snippet.channelTitle,
    }));
  },

  async getTrendingVideos(): Promise<YouTubeVideo[]> {
    const response = await fetch(
      `${YOUTUBE_API_BASE_URL}/videos?part=snippet,statistics&chart=mostPopular&maxResults=10&key=${YOUTUBE_API_KEY}`
    );
    const data = await response.json();

    return data.items.map((item: any) => ({
      id: item.id,
      title: item.snippet.title,
      description: item.snippet.description,
      thumbnail: item.snippet.thumbnails.medium.url,
      viewCount: item.statistics.viewCount,
      likeCount: item.statistics.likeCount,
      publishedAt: item.snippet.publishedAt,
      channelTitle: item.snippet.channelTitle,
    }));
  },

  async getChannelInfo(channelId: string): Promise<YouTubeChannel> {
    const response = await fetch(
      `${YOUTUBE_API_BASE_URL}/channels?part=snippet,statistics&id=${channelId}&key=${YOUTUBE_API_KEY}`
    );
    const data = await response.json();
    const channel = data.items[0];

    return {
      id: channel.id,
      title: channel.snippet.title,
      description: channel.snippet.description,
      thumbnail: channel.snippet.thumbnails.medium.url,
      subscriberCount: channel.statistics.subscriberCount,
      videoCount: channel.statistics.videoCount,
    };
  },

  async getVideoDetails(videoId: string): Promise<YouTubeVideo> {
    const response = await fetch(
      `${YOUTUBE_API_BASE_URL}/videos?part=snippet,statistics&id=${videoId}&key=${YOUTUBE_API_KEY}`
    );
    const data = await response.json();
    const video = data.items[0];

    return {
      id: video.id,
      title: video.snippet.title,
      description: video.snippet.description,
      thumbnail: video.snippet.thumbnails.medium.url,
      viewCount: video.statistics.viewCount,
      likeCount: video.statistics.likeCount,
      publishedAt: video.snippet.publishedAt,
      channelTitle: video.snippet.channelTitle,
    };
  },
}; 