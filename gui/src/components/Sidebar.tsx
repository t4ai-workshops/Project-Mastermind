import React from 'react';
import { MessageSquare, Plus, Settings, Moon, Sun } from 'lucide-react';
import { useStore } from '../store';

export const Sidebar: React.FC = () => {
  const { chats, activeChat, createChat, setActiveChat, settings, setTheme } = useStore();
  
  return (
    <div className="w-64 bg-gray-50 dark:bg-gray-900 flex flex-col">
      {/* Header */}
      <div className="p-4 border-b dark:border-gray-700">
        <h1 className="text-xl font-bold dark:text-white">MasterMind</h1>
      </div>
      
      {/* Chat List */}
      <div className="flex-1 overflow-y-auto p-2">
        <button
          onClick={createChat}
          className="w-full p-2 mb-2 flex items-center gap-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          <Plus size={16} />
          New Chat
        </button>
        
        {chats.map((chat) => (
          <button
            key={chat.id}
            onClick={() => setActiveChat(chat.id)}
            className={`w-full p-2 mb-1 flex items-center gap-2 rounded ${
              activeChat === chat.id
                ? 'bg-gray-200 dark:bg-gray-700'
                : 'hover:bg-gray-100 dark:hover:bg-gray-800'
            }`}
          >
            <MessageSquare size={16} />
            <span className="truncate">{chat.title}</span>
          </button>
        ))}
      </div>
      
      {/* Footer */}
      <div className="p-4 border-t dark:border-gray-700">
        <button
          onClick={() => setTheme(settings.theme === 'light' ? 'dark' : 'light')}
          className="w-full p-2 mb-2 flex items-center gap-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded"
        >
          {settings.theme === 'light' ? <Moon size={16} /> : <Sun size={16} />}
          {settings.theme === 'light' ? 'Dark Mode' : 'Light Mode'}
        </button>
        
        <button className="w-full p-2 flex items-center gap-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded">
          <Settings size={16} />
          Settings
        </button>
      </div>
    </div>
  );
};