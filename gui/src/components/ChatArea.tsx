import React, { useState } from 'react';
import { Send, Loader } from 'lucide-react';
import { useStore } from '../store';

export const ChatArea: React.FC = () => {
  const [input, setInput] = useState('');
  const { chats, activeChat, addMessage, isProcessing } = useStore();
  
  const activeMessages = activeChat 
    ? chats.find(c => c.id === activeChat)?.messages || []
    : [];
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || !activeChat) return;
    
    // Add user message
    const userMessage = {
      id: Math.random().toString(36).substr(2, 9),
      role: 'user' as const,
      content: input,
      timestamp: Date.now()
    };
    addMessage(activeChat, userMessage);
    setInput('');
    
    // TODO: Process with AI
    // For now, just add a mock response
    const assistantMessage = {
      id: Math.random().toString(36).substr(2, 9),
      role: 'assistant' as const,
      content: `Processing your message: "${input}"`,
      timestamp: Date.now()
    };
    addMessage(activeChat, assistantMessage);
  };
  
  if (!activeChat) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <p className="text-gray-500">Select or create a chat to start</p>
      </div>
    );
  }
  
  return (
    <div className="flex-1 flex flex-col bg-white dark:bg-gray-800">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {activeMessages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[70%] p-3 rounded-lg ${
                message.role === 'user'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-100 dark:bg-gray-700 dark:text-white'
              }`}
            >
              {message.content}
            </div>
          </div>
        ))}
        {isProcessing && (
          <div className="flex justify-start">
            <div className="bg-gray-100 dark:bg-gray-700 p-3 rounded-lg flex items-center gap-2">
              <Loader className="animate-spin" size={16} />
              <span>Thinking...</span>
            </div>
          </div>
        )}
      </div>
      
      {/* Input */}
      <form onSubmit={handleSubmit} className="p-4 border-t dark:border-gray-700">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 p-2 border dark:border-gray-700 rounded-lg dark:bg-gray-700 dark:text-white"
          />
          <button
            type="submit"
            disabled={!input.trim() || isProcessing}
            className="p-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50"
          >
            <Send size={20} />
          </button>
        </div>
      </form>
    </div>
  );
};