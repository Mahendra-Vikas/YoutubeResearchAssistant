'use client';

import { useState } from 'react';
import { MessageSquare, Youtube, Plus, Menu } from 'lucide-react';

interface ChatHistory {
  id: string;
  title: string;
  timestamp: string;
}

export default function Sidebar() {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [activeTab, setActiveTab] = useState<'chat' | 'youtube'>('chat');
  const [chatHistory] = useState<ChatHistory[]>([
    { id: '1', title: 'MrBeast Channel Analysis', timestamp: '2 hours ago' },
    { id: '2', title: 'Content Strategy Research', timestamp: '5 hours ago' },
  ]);

  return (
    <div
      className={`${
        isCollapsed ? 'w-16' : 'w-64'
      } bg-[#1F1F1F] border-r border-gray-800 flex flex-col transition-all duration-300 ease-in-out`}
    >
      {/* Header */}
      <div className="p-4 border-b border-gray-800 flex items-center justify-between">
        {!isCollapsed && (
          <h1 className="text-lg font-semibold text-[#EAEAEA]">Research Assistant</h1>
        )}
        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="p-1 hover:bg-gray-800 rounded-lg transition-colors"
        >
          <Menu className="w-5 h-5 text-[#EAEAEA]" />
        </button>
      </div>

      {/* New Chat Button */}
      <button className="m-4 p-2 bg-[#FF2E63] hover:bg-[#ff4778] text-white rounded-lg flex items-center justify-center gap-2 transition-colors">
        <Plus className="w-5 h-5" />
        {!isCollapsed && <span>New Chat</span>}
      </button>

      {/* Tab Switcher */}
      <div className="flex px-2 gap-1 mb-4">
        <button
          onClick={() => setActiveTab('chat')}
          className={`flex-1 p-2 rounded-lg flex items-center justify-center gap-2 transition-all ${
            activeTab === 'chat'
              ? 'bg-gray-800 text-[#08D9D6]'
              : 'hover:bg-gray-800 text-[#EAEAEA]'
          }`}
        >
          <MessageSquare className="w-5 h-5" />
          {!isCollapsed && <span>Chat</span>}
        </button>
        <button
          onClick={() => setActiveTab('youtube')}
          className={`flex-1 p-2 rounded-lg flex items-center justify-center gap-2 transition-all ${
            activeTab === 'youtube'
              ? 'bg-gray-800 text-[#FF2E63]'
              : 'hover:bg-gray-800 text-[#EAEAEA]'
          }`}
        >
          <Youtube className="w-5 h-5" />
          {!isCollapsed && <span>YouTube</span>}
        </button>
      </div>

      {/* Chat History */}
      <div className="flex-1 overflow-y-auto">
        {!isCollapsed &&
          chatHistory.map((chat) => (
            <button
              key={chat.id}
              className="w-full p-3 hover:bg-gray-800 text-left transition-colors group"
            >
              <div className="text-sm text-[#EAEAEA] truncate">{chat.title}</div>
              <div className="text-xs text-gray-500">{chat.timestamp}</div>
            </button>
          ))}
      </div>
    </div>
  );
} 