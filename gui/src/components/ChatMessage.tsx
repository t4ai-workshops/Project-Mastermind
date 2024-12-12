/**
 * ChatMessage Component
 * 
 * This component renders individual chat messages in the chat interface.
 * It handles both user and assistant messages with appropriate styling.
 * 
 * Features:
 * - Different styling for user/assistant messages
 * - File attachment display
 * - Timestamp display using native Date API
 * - Dark mode support
 * 
 * @component
 */

import React from 'react';

interface FileAttachment {
  name: string;
  // Add other file properties as needed
}

interface ChatMessageProps {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: number;
  files?: FileAttachment[];
}

export const ChatMessage: React.FC<ChatMessageProps> = ({
  role,
  content,
  timestamp,
  files
}) => {
  // Determine message alignment and styling based on role
  const messageAlignment = role === 'user' ? 'justify-end' : 'justify-start';
  const messageStyle = role === 'user'
    ? 'bg-blue-500 text-white'
    : 'bg-gray-100 dark:bg-gray-700 dark:text-white';

  // Format timestamp to localized string
  const formattedTime = new Date(timestamp).toLocaleString('nl-NL', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  });

  return (
    <div className={`flex ${messageAlignment}`}>
      <div className={`message-container ${messageStyle}`}>
        {/* Message content */}
        <div className="whitespace-pre-wrap break-words">
          {content}
        </div>

        {/* File attachments if present */}
        {files && files.length > 0 && (
          <div className="mt-2 space-y-1">
            {files.map((file, index) => (
              <div key={index} className="text-sm opacity-75">
                📎 {file.name}
              </div>
            ))}
          </div>
        )}

        {/* Timestamp */}
        <div className="mt-1 text-xs opacity-50">
          {formattedTime}
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;