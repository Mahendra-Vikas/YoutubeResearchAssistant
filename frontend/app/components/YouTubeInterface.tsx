'use client';

import { useState, useRef, useEffect } from 'react';
import { Send, Youtube, BarChart2, TrendingUp, Users } from 'lucide-react';

interface YouTubeMessage {
  role: 'user' | 'assistant';
  content: string;
  data?: {
    videoId?: string;
    channelId?: string;
    statistics?: {
      views?: number;
      likes?: number;
      comments?: number;
    };
    thumbnail?: string;
  };
}

export default function YouTubeInterface() {
  const [messages, setMessages] = useState<YouTubeMessage[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: YouTubeMessage = { role: 'user' as const, content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/youtube`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: input }),
      });

      const data = await response.json();
      const assistantMessage: YouTubeMessage = { 
        role: 'assistant' as const, 
        content: data.response,
        data: data.data
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const renderYouTubeData = (data: YouTubeMessage['data']) => {
    if (!data) return null;

    return (
      <div className="mt-4 space-y-4">
        {data.videoId && (
          <div className="aspect-video w-full max-w-2xl">
            <iframe
              src={`https://www.youtube.com/embed/${data.videoId}`}
              className="w-full h-full rounded-lg"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
          </div>
        )}
        {data.statistics && (
          <div className="grid grid-cols-3 gap-4 text-center">
            <div className="bg-gray-800 p-4 rounded-lg">
              <BarChart2 className="w-6 h-6 mx-auto mb-2" />
              <p className="text-2xl font-bold">{data.statistics.views?.toLocaleString()}</p>
              <p className="text-sm text-gray-400">Views</p>
            </div>
            <div className="bg-gray-800 p-4 rounded-lg">
              <Users className="w-6 h-6 mx-auto mb-2" />
              <p className="text-2xl font-bold">{data.statistics.likes?.toLocaleString()}</p>
              <p className="text-sm text-gray-400">Likes</p>
            </div>
            <div className="bg-gray-800 p-4 rounded-lg">
              <TrendingUp className="w-6 h-6 mx-auto mb-2" />
              <p className="text-2xl font-bold">{data.statistics.comments?.toLocaleString()}</p>
              <p className="text-sm text-gray-400">Comments</p>
            </div>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="flex flex-col h-full bg-[#1F1F1F]">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center space-y-4">
              <Youtube className="w-12 h-12 mx-auto text-[#FF2E63]" />
              <h2 className="text-2xl font-bold text-[#EAEAEA]">
                YouTube Research Assistant
              </h2>
              <p className="text-gray-400">
                Analyze channels, track video performance, and discover content insights!
              </p>
              <div className="grid grid-cols-2 gap-4 mt-8">
                <div className="bg-gray-800 p-4 rounded-lg">
                  <h3 className="font-semibold text-[#EAEAEA]">Try asking:</h3>
                  <p className="text-sm text-gray-400">&quot;Show me MrBeast&apos;s latest video stats&quot;</p>
                </div>
                <div className="bg-gray-800 p-4 rounded-lg">
                  <h3 className="font-semibold text-[#EAEAEA]">Or:</h3>
                  <p className="text-sm text-gray-400">&quot;Analyze PewDiePie&apos;s channel growth&quot;</p>
                </div>
              </div>
            </div>
          </div>
        ) : (
          messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${
                message.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              <div
                className={`max-w-[80%] rounded-lg p-4 shadow-lg animate-fadeIn ${
                  message.role === 'user'
                    ? 'bg-[#FF2E63] text-white'
                    : 'bg-gray-800 text-[#EAEAEA]'
                }`}
              >
                <div className="whitespace-pre-wrap">{message.content}</div>
                {message.role === 'assistant' && renderYouTubeData(message.data)}
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-800 text-[#EAEAEA] rounded-lg p-4 animate-pulse">
              Analyzing YouTube data...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-800 p-4">
        <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
          <div className="flex space-x-4">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about YouTube channels, videos, or trends..."
              className="flex-1 input-primary"
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="btn-primary disabled:opacity-50 flex items-center gap-2"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
} 