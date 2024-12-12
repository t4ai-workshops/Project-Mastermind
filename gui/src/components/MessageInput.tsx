/**
 * MessageInput Component
 * 
 * Handles user input for sending messages and file attachments.
 * This component is responsible for:
 * - Text input handling
 * - File attachment handling
 * - Message submission
 * - Loading states
 * 
 * Features:
 * - Text input with auto-resize
 * - File attachment support
 * - Loading state handling
 * - Error handling
 * - Dark mode support
 * 
 * @component
 */

import React, { useState, useRef } from 'react';
import { Send, Paperclip, X } from 'lucide-react';
import { useStore } from '../store';

export const MessageInput: React.FC = () => {
  const [input, setInput] = useState('');
  const [files, setFiles] = useState<File[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { activeChat, addMessage, processMessage, isProcessing } = useStore();

  /**
   * Handles the submission of a new message
   * Creates a message object and processes it through the AI
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() && files.length === 0 || !activeChat || isProcessing) return;
    
    const userMessage = {
      id: Math.random().toString(36).substr(2, 9),
      role: 'user' as const,
      content: input,
      timestamp: Date.now(),
      files: files
    };
    
    // Clean up input state
    setInput('');
    setFiles([]);
    
    // Send message and process response
    try {
      addMessage(activeChat, userMessage);
      await processMessage(activeChat, userMessage);
    } catch (error) {
      console.error('Error sending message:', error);
      // Error handling could be enhanced here
    }
  };

  /**
   * Handles file selection from the system dialog
   */
  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = Array.from(e.target.files || []);
    setFiles(prev => [...prev, ...selectedFiles]);
  };

  /**
   * Removes a file from the attachments list
   */
  const removeFile = (index: number) => {
    setFiles(prev => prev.filter((_, i) => i !== index));
  };

  // Don't render input if no chat is active
  if (!activeChat) {
    return null;
  }

  return (
    <div className="border-t dark:border-gray-700 bg-white dark:bg-gray-800">
      <form onSubmit={handleSubmit} className="p-4">
        {/* File attachments display */}
        {files.length > 0 && (
          <div className="mb-2 flex flex-wrap gap-2">
            {files.map((file, index) => (
              <div key={index} 
                   className="bg-gray-100 dark:bg-gray-700 rounded px-2 py-1 flex items-center gap-1">
                <span className="text-sm dark:text-white">{file.name}</span>
                <button
                  type="button"
                  onClick={() => removeFile(index)}
                  className="hover:text-red-500 transition-colors"
                  aria-label="Remove file"
                >
                  <X size={14} />
                </button>
              </div>
            ))}
          </div>
        )}
        
        {/* Input controls */}
        <div className="flex gap-2">
          {/* Hidden file input */}
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileSelect}
            className="hidden"
            multiple
            aria-label="Attach files"
          />
          
          {/* File attachment button */}
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
            aria-label="Add attachment"
          >
            <Paperclip size={20} className="dark:text-white" />
          </button>
          
          {/* Message input */}
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 p-2 border dark:border-gray-700 rounded-lg 
                     dark:bg-gray-700 dark:text-white focus:outline-none 
                     focus:ring-2 focus:ring-blue-500"
            disabled={isProcessing}
          />
          
          {/* Send button */}
          <button
            type="submit"
            disabled={(!input.trim() && files.length === 0) || isProcessing}
            className="p-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 
                     disabled:opacity-50 disabled:cursor-not-allowed
                     transition-colors"
            aria-label="Send message"
          >
            <Send size={20} />
          </button>
        </div>
      </form>
    </div>
  );
};