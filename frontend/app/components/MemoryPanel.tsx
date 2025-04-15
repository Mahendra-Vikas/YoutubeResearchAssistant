'use client';

import { useState } from 'react';
import { Edit2, Save, X } from 'lucide-react';

interface Memory {
  content: string;
  type: string;
  timestamp: string;
}

interface MemoryPanelProps {
  memories: Memory[];
}

export default function MemoryPanel({ memories }: MemoryPanelProps) {
  const [editingChannelFocus, setEditingChannelFocus] = useState(false);
  const [newChannelFocus, setNewChannelFocus] = useState('');
  const [channelFocusMemories, setChannelFocusMemories] = useState(
    memories.filter(m => m.type === 'Channel Focus')
  );

  const handleSaveChannelFocus = () => {
    if (newChannelFocus.trim()) {
      const newMemory = {
        content: newChannelFocus,
        type: 'Channel Focus',
        timestamp: new Date().toLocaleString(),
      };
      setChannelFocusMemories([...channelFocusMemories, newMemory]);
      setNewChannelFocus('');
      setEditingChannelFocus(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-4 h-full">
      <h2 className="text-xl font-semibold mb-4">Memory Panel</h2>

      {/* Channel Focus Section */}
      <div className="mb-6">
        <div className="flex justify-between items-center mb-2">
          <h3 className="text-lg font-medium text-gray-800">Channel Focus</h3>
          <button
            onClick={() => setEditingChannelFocus(true)}
            className="text-blue-500 hover:text-blue-600"
          >
            <Edit2 className="w-4 h-4" />
          </button>
        </div>

        {editingChannelFocus ? (
          <div className="space-y-2">
            <input
              type="text"
              value={newChannelFocus}
              onChange={(e) => setNewChannelFocus(e.target.value)}
              placeholder="Enter new channel focus..."
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <div className="flex space-x-2">
              <button
                onClick={handleSaveChannelFocus}
                className="px-3 py-1 bg-blue-500 text-white rounded-lg hover:bg-blue-600 flex items-center space-x-1"
              >
                <Save className="w-4 h-4" />
                <span>Save</span>
              </button>
              <button
                onClick={() => {
                  setEditingChannelFocus(false);
                  setNewChannelFocus('');
                }}
                className="px-3 py-1 bg-gray-500 text-white rounded-lg hover:bg-gray-600 flex items-center space-x-1"
              >
                <X className="w-4 h-4" />
                <span>Cancel</span>
              </button>
            </div>
          </div>
        ) : (
          <div className="space-y-2">
            {channelFocusMemories.map((memory, index) => (
              <div
                key={index}
                className="p-3 bg-gray-50 rounded-lg"
              >
                <p className="text-gray-800">{memory.content}</p>
                <p className="text-xs text-gray-500 mt-1">{memory.timestamp}</p>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Other Memories Section */}
      <div>
        <h3 className="text-lg font-medium text-gray-800 mb-2">Recent Memories</h3>
        <div className="space-y-2">
          {memories
            .filter(memory => memory.type !== 'Channel Focus')
            .map((memory, index) => (
              <div
                key={index}
                className="p-3 bg-gray-50 rounded-lg"
              >
                <p className="text-gray-800">{memory.content}</p>
                <p className="text-xs text-gray-500 mt-1">
                  {memory.type} - {memory.timestamp}
                </p>
              </div>
            ))}
        </div>
      </div>
    </div>
  );
} 