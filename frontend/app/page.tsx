'use client';

import { useState } from 'react';
import ChatInterface from './components/ChatInterface';
import YouTubeInterface from './components/YouTubeInterface';
import { MessageSquare, Youtube } from 'lucide-react';

export default function Home() {
  const [activeTab, setActiveTab] = useState<'chat' | 'youtube'>('youtube');

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-4 bg-[#1F1F1F]">
      <div className="w-full max-w-6xl h-[calc(100vh-2rem)]">
        {/* Tab Navigation */}
        <div className="flex space-x-4 mb-4">
          <button
            onClick={() => setActiveTab('youtube')}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
              activeTab === 'youtube'
                ? 'bg-[#FF2E63] text-white'
                : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
            }`}
          >
            <Youtube className="w-5 h-5" />
            YouTube
          </button>
          <button
            onClick={() => setActiveTab('chat')}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
              activeTab === 'chat'
                ? 'bg-[#FF2E63] text-white'
                : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
            }`}
          >
            <MessageSquare className="w-5 h-5" />
            Chat
          </button>
        </div>

        {/* Content Area */}
        <div className="h-[calc(100%-3rem)]">
          {activeTab === 'youtube' ? <YouTubeInterface /> : <ChatInterface />}
        </div>
      </div>
    </main>
  );
} 