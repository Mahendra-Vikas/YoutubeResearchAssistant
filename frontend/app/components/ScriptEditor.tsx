'use client';

import { useState } from 'react';
import { Copy, Save } from 'lucide-react';

interface ScriptEditorProps {
  initialScript?: string;
}

export default function ScriptEditor({ initialScript = '' }: ScriptEditorProps) {
  const [script, setScript] = useState(initialScript);
  const [isSaved, setIsSaved] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(script);
      alert('Script copied to clipboard!');
    } catch (err) {
      console.error('Failed to copy text:', err);
    }
  };

  const handleSave = () => {
    // Implement save functionality (e.g., to localStorage or backend)
    localStorage.setItem('savedScript', script);
    setIsSaved(true);
    setTimeout(() => setIsSaved(false), 2000);
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-4">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold">Video Script</h2>
        <div className="flex space-x-2">
          <button
            onClick={handleCopy}
            className="p-2 text-gray-600 hover:text-gray-900 rounded-lg hover:bg-gray-100"
            title="Copy to clipboard"
          >
            <Copy className="w-5 h-5" />
          </button>
          <button
            onClick={handleSave}
            className={`p-2 rounded-lg ${
              isSaved
                ? 'text-green-600 bg-green-50'
                : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
            }`}
            title="Save script"
          >
            <Save className="w-5 h-5" />
          </button>
        </div>
      </div>
      <textarea
        value={script}
        onChange={(e) => setScript(e.target.value)}
        placeholder="Your video script will appear here..."
        className="w-full h-[400px] p-4 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
      />
      {isSaved && (
        <p className="text-sm text-green-600 mt-2">Script saved successfully!</p>
      )}
    </div>
  );
} 