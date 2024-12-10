import React from 'react';
import { Database, Circle } from 'lucide-react';
import { useStore } from '../store';

export const MemoryPanel: React.FC = () => {
  const memories = useStore((state) => state.memories);
  
  return (
    <div className="w-64 bg-gray-50 dark:bg-gray-900 border-l dark:border-gray-700">
      <div className="p-4 border-b dark:border-gray-700">
        <h2 className="text-lg font-semibold dark:text-white flex items-center gap-2">
          <Database size={16} />
          Memory Context
        </h2>
      </div>
      
      <div className="p-2 space-y-2 overflow-y-auto">
        {memories.map((memory) => (
          <div
            key={memory.id}
            className="p-3 bg-white dark:bg-gray-800 rounded-lg shadow-sm"
          >
            <div className="flex items-center gap-2 mb-1">
              <Circle
                size={8}
                className={`fill-current ${
                  memory.importance > 0.7
                    ? 'text-red-500'
                    : memory.importance > 0.4
                    ? 'text-yellow-500'
                    : 'text-green-500'
                }`}
              />
              <span className="text-sm font-medium dark:text-white">
                {memory.category}
              </span>
            </div>
            
            <p className="text-sm text-gray-600 dark:text-gray-300">
              {memory.content}
            </p>
            
            <div className="mt-2 text-xs text-gray-400">
              {new Date(memory.timestamp).toLocaleString()}
            </div>
          </div>
        ))}
        
        {memories.length === 0 && (
          <div className="text-center text-gray-500 dark:text-gray-400 p-4">
            No memories yet
          </div>
        )}
      </div>
    </div>
  );
};