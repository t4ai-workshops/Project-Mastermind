import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader, Paperclip, X } from 'lucide-react';
import { useStore } from '../store';

export const ChatArea: React.FC = () => {
  const [input, setInput] = useState('');
  const [files, setFiles] = useState<File[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  const { 
    chats, 
    activeChat, 
    addMessage, 
    isProcessing,
    processMessage 
  } = useStore();
  
  const activeMessages = activeChat 
    ? chats.find(c => c.id === activeChat)?.messages || []
    : [];
  
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [activeMessages]);
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() && files.length === 0 || !activeChat || isProcessing) return;
    
    // Add user message
    const userMessage = {
      id: Math.random().toString(36).substr(2, 9),
      role: 'user' as const,
      content: input,
      timestamp: Date.now(),
      files: files
    };
    
    addMessage(activeChat, userMessage);
    setInput('');
    setFiles([]);
    
    // Process message with AI
    await processMessage(activeChat, userMessage);
  };
  
  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = Array.from(e.target.files || []);
    setFiles(prev => [...prev, ...selectedFiles]);
  };
  
  const removeFile = (index: number) => {
    setFiles(prev => prev.filter((_, i) => i !== index));
  };
  
  if (!activeChat) {
    return (
      <div className="flex-1 flex items-center justify-center bg-white dark:bg-gray-800">
        <p className="text-gray-500 dark:text-gray-400">
          Select or create a chat to start
        </p>
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
              {message.files && message.files.length > 0 && (
                <div className="mt-2 space-y-1">
                  {message.files.map((file, index) => (
                    <div key={index} className="text-sm opacity-75">
                      📎 {file.name}
                    </div>
                  ))}
                </div>
              )}
              <div className="mt-1 text-xs opacity-50">
                {new Date(message.timestamp).toLocaleTimeString()}
              </div>
            </div>
          </div>
        ))}
        {isProcessing && (
          <div className="flex justify-start">
            <div className="bg-gray-100 dark:bg-gray-700 p-3 rounded-lg flex items-center gap-2">
              <Loader className="animate-spin" size={16} />
              <span className="dark:text-white">Thinking...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      {/* Input */}
      <form onSubmit={handleSubmit} className="p-4 border-t dark:border-gray-700">
        {files.length > 0 && (
          <div className="mb-2 flex flex-wrap gap-2">
            {files.map((file, index) => (
              <div 
                key={index}
                className="bg-gray-100 dark:bg-gray-700 rounded px-2 py-1 flex items-center gap-1"
              >
                <span className="text-sm dark:text-white">{file.name}</span>
                <button
                  type="button"
                  onClick={() => removeFile(index)}
                  className="hover:text-red-500"
                >
                  <X size={14} />
                </button>
              </div>
            ))}
          </div>
        )}
        
        <div className="flex gap-2">
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileSelect}
            className="hidden"
            multiple
          />
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded"
          >
            <Paperclip size={20} className="dark:text-white" />
          </button>
          
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 p-2 border dark:border-gray-700 rounded-lg 
                     dark:bg-gray-700 dark:text-white"
          />
          
          <button
            type="submit"
            disabled={(!input.trim() && files.length === 0) || isProcessing}
            className="p-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 
                     disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send size={20} />
          </button>
        </div>
      </form>
    </div>
  );
};