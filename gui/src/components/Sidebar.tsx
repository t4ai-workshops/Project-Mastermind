import React, { useState } from 'react';
import { 
  MessageSquare, 
  Plus, 
  Settings, 
  Moon, 
  Sun, 
  ChevronLeft, 
  ChevronRight 
} from 'lucide-react';
import { useStore } from '../store';

export const Sidebar: React.FC = () => {
  const { 
    chats, 
    activeChat, 
    createChat, 
    setActiveChat, 
    settings, 
    setTheme,
    deleteChat,
    renameChat 
  } = useStore();
  
  const [collapsed, setCollapsed] = useState(false);
  const [editingChatId, setEditingChatId] = useState<string | null>(null);
  const [editValue, setEditValue] = useState('');
  
  const handleRename = (chatId: string, newName: string) => {
    renameChat(chatId, newName);
    setEditingChatId(null);
    setEditValue('');
  };
  
  const startEditing = (chatId: string, currentName: string) => {
    setEditingChatId(chatId);
    setEditValue(currentName);
  };
  
  return (
    <div 
      className={`${
        collapsed ? 'w-16' : 'w-64'
      } bg-gray-50 dark:bg-gray-900 flex flex-col transition-all duration-200 ease-in-out relative`}
    >
      {/* Collapse button */}
      <button
        onClick={() => setCollapsed(!collapsed)}
        className="absolute -right-3 top-1/2 transform -translate-y-1/2 z-10
                   w-6 h-6 rounded-full bg-gray-200 dark:bg-gray-700
                   flex items-center justify-center hover:bg-gray-300 dark:hover:bg-gray-600"
      >
        {collapsed ? <ChevronRight size={14} /> : <ChevronLeft size={14} />}
      </button>
      
      {/* Header */}
      <div className="p-4 border-b dark:border-gray-700">
        <h1 className={`text-xl font-bold dark:text-white ${collapsed ? 'hidden' : ''}`}>
          MasterMind
        </h1>
      </div>
      
      {/* Chat List */}
      <div className="flex-1 overflow-y-auto p-2">
        <button
          onClick={createChat}
          className={`w-full p-2 mb-2 flex items-center gap-2 bg-blue-500 text-white rounded 
                     hover:bg-blue-600 ${collapsed ? 'justify-center' : ''}`}
        >
          <Plus size={16} />
          {!collapsed && 'New Chat'}
        </button>
        
        {chats.map((chat) => (
          <div key={chat.id} className="relative group">
            {editingChatId === chat.id ? (
              <input
                type="text"
                value={editValue}
                onChange={(e) => setEditValue(e.target.value)}
                onBlur={() => handleRename(chat.id, editValue)}
                onKeyPress={(e) => e.key === 'Enter' && handleRename(chat.id, editValue)}
                className="w-full p-2 mb-1 bg-white dark:bg-gray-800 rounded border"
                autoFocus
              />
            ) : (
              <button
                onClick={() => setActiveChat(chat.id)}
                onDoubleClick={() => startEditing(chat.id, chat.title)}
                className={`w-full p-2 mb-1 flex items-center gap-2 rounded ${
                  activeChat === chat.id
                    ? 'bg-gray-200 dark:bg-gray-700'
                    : 'hover:bg-gray-100 dark:hover:bg-gray-800'
                } ${collapsed ? 'justify-center' : ''}`}
              >
                <MessageSquare size={16} />
                {!collapsed && (
                  <span className="truncate flex-1 text-left">{chat.title}</span>
                )}
              </button>
            )}
            
            {!collapsed && !editingChatId && (
              <div className="absolute right-2 top-1/2 -translate-y-1/2 hidden group-hover:flex gap-1">
                <button
                  onClick={() => startEditing(chat.id, chat.title)}
                  className="p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded"
                >
                  ✎
                </button>
                <button
                  onClick={() => deleteChat(chat.id)}
                  className="p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded text-red-500"
                >
                  ×
                </button>
              </div>
            )}
          </div>
        ))}
      </div>
      
      {/* Footer */}
      <div className="p-4 border-t dark:border-gray-700">
        <button
          onClick={() => setTheme(settings.theme === 'light' ? 'dark' : 'light')}
          className={`w-full p-2 mb-2 flex items-center gap-2 hover:bg-gray-100 
                     dark:hover:bg-gray-800 rounded ${collapsed ? 'justify-center' : ''}`}
        >
          {settings.theme === 'light' ? <Moon size={16} /> : <Sun size={16} />}
          {!collapsed && (settings.theme === 'light' ? 'Dark Mode' : 'Light Mode')}
        </button>
        
        <button className={`w-full p-2 flex items-center gap-2 hover:bg-gray-100 
                         dark:hover:bg-gray-800 rounded ${collapsed ? 'justify-center' : ''}`}>
          <Settings size={16} />
          {!collapsed && 'Settings'}
        </button>
      </div>
    </div>
  );
};