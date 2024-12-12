/**
 * ChatArea Component
 * 
 * Displays the chat messages in a scrollable container.
 * This component is responsible for:
 * - Rendering messages from the chat history
 * - Managing scroll behavior
 * - Showing loading states
 * - Handling empty states
 * 
 * Features:
 * - Automatic scrolling to latest message
 * - Smooth scroll behavior
 * - Loading indicator
 * - Empty state handling
 * 
 * @component
 */

import React, { useRef, useEffect } from 'react';
import { Loader } from 'lucide-react';
import { useStore } from '../store';
import { ChatMessage } from './ChatMessage';

export const ChatArea: React.FC = () => {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { chats, activeChat, isProcessing } = useStore();
  
  // Get messages for active chat
  const activeMessages = activeChat 
    ? chats.find(c => c.id === activeChat)?.messages || []
    : [];
  
  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ 
      behavior: 'smooth', 
      block: 'nearest' 
    });
  }, [activeMessages]);
  
  // Empty state when no chat is selected
  if (!activeChat) {
    return (
      <div className="h-full flex items-center justify-center">
        <p className="text-gray-500 dark:text-gray-400">
          Select or create a chat to start
        </p>
      </div>
    );
  }
  
  return (
    <div className="h-full scroll-container">
      <div className="p-4 space-y-4">
        {/* Render chat messages */}
        {activeMessages.map((message) => (
          <ChatMessage
            key={message.id}
            {...message}
          />
        ))}

        {/* Loading indicator */}
        {isProcessing && (
          <div className="flex justify-start">
            <div className="bg-gray-100 dark:bg-gray-700 p-3 rounded-lg flex items-center gap-2">
              <Loader className="animate-spin" size={16} />
              <span className="dark:text-white">Thinking...</span>
            </div>
          </div>
        )}

        {/* Scroll anchor */}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};