'use client';

import { useState, useEffect } from 'react';
import { youtubeService, YouTubeVideo } from '../services/youtube';
import { Search } from 'lucide-react';

export default function YouTubePanel() {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<YouTubeVideo[]>([]);
  const [trendingVideos, setTrendingVideos] = useState<YouTubeVideo[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'search' | 'trending'>('trending');

  useEffect(() => {
    loadTrendingVideos();
  }, []);

  const loadTrendingVideos = async () => {
    try {
      setIsLoading(true);
      const videos = await youtubeService.getTrendingVideos();
      setTrendingVideos(videos);
    } catch (error) {
      console.error('Error loading trending videos:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    try {
      setIsLoading(true);
      const results = await youtubeService.searchVideos(searchQuery);
      setSearchResults(results);
      setActiveTab('search');
    } catch (error) {
      console.error('Error searching videos:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const formatCount = (count: string) => {
    const num = parseInt(count);
    if (num >= 1000000) {
      return `${(num / 1000000).toFixed(1)}M`;
    }
    if (num >= 1000) {
      return `${(num / 1000).toFixed(1)}K`;
    }
    return count;
  };

  const VideoCard = ({ video }: { video: YouTubeVideo }) => (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <img
        src={video.thumbnail}
        alt={video.title}
        className="w-full h-48 object-cover"
      />
      <div className="p-4">
        <h3 className="font-semibold text-gray-800 mb-2 line-clamp-2">
          {video.title}
        </h3>
        <p className="text-sm text-gray-600 mb-2">{video.channelTitle}</p>
        <div className="flex justify-between text-sm text-gray-500">
          <span>{formatCount(video.viewCount)} views</span>
          <span>{formatCount(video.likeCount)} likes</span>
        </div>
      </div>
    </div>
  );

  return (
    <div className="bg-white rounded-lg shadow-lg p-4 h-full overflow-hidden flex flex-col">
      <h2 className="text-xl font-semibold mb-4">YouTube Explorer</h2>
      
      {/* Search Form */}
      <form onSubmit={handleSearch} className="mb-4">
        <div className="flex space-x-2">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search YouTube videos..."
            className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            disabled={isLoading}
            className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 disabled:opacity-50"
          >
            <Search className="w-5 h-5" />
          </button>
        </div>
      </form>

      {/* Tabs */}
      <div className="flex space-x-4 mb-4">
        <button
          onClick={() => setActiveTab('trending')}
          className={`px-4 py-2 rounded-lg ${
            activeTab === 'trending'
              ? 'bg-red-600 text-white'
              : 'bg-gray-100 text-gray-800'
          }`}
        >
          Trending
        </button>
        <button
          onClick={() => setActiveTab('search')}
          className={`px-4 py-2 rounded-lg ${
            activeTab === 'search'
              ? 'bg-red-600 text-white'
              : 'bg-gray-100 text-gray-800'
          }`}
        >
          Search Results
        </button>
      </div>

      {/* Video Grid */}
      <div className="flex-1 overflow-y-auto">
        {isLoading ? (
          <div className="flex justify-center items-center h-full">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-red-600"></div>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4">
            {activeTab === 'trending'
              ? trendingVideos.map((video) => (
                  <VideoCard key={video.id} video={video} />
                ))
              : searchResults.map((video) => (
                  <VideoCard key={video.id} video={video} />
                ))}
          </div>
        )}
      </div>
    </div>
  );
} 