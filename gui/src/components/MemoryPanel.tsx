import React, { useState } from 'react';
import { Database, Circle, ChevronRight, ChevronLeft, Star, StarOff } from 'lucide-react';
import { useStore } from '../store';

export const MemoryPanel: React.FC = () => {
  const [collapsed, setCollapsed] = useState(false);
  const { memories, updateMemoryImportance } = useStore();
  
  // Group memories by category
  const groupedMemories = memories.reduce((groups, memory) => {
    const category = memory.category;
    if (!groups[category]) {
      groups[category] = [];
    }
    groups[category].push(memory);
    return groups;
  }, {} as Record<string, typeof memories>);
  
  const toggleImportance = (memoryId: string, currentImportance: number) => {
    // Toggle between high importance (0.9) and normal importance (0.5)
    updateMemoryImportance(memoryId, currentImportance > 0.7 ? 0.5 : 0.9);
  };
  
  return (
    <div 
      className={`${
        collapsed ? 'w-16' : 'w-64'
      } bg-gray-50 dark:bg-gray-900 border-l dark:border-gray-700 flex flex-col transition-all duration-200 ease-in-out relative`}
    >
      {/* Collapse button */}
      <button
        onClick={() => setCollapsed(!collapsed)}
        className="absolute -left-3 top-1/2 transform -translate-y-1/2 z-10
                   w-6 h-6 rounded-full bg-gray-200 dark:bg-gray-700
                   flex items-center justify-center hover:bg-gray-300 dark:hover:bg-gray-600"
      >
        {collapsed ? <ChevronRight size={14} /> : <ChevronLeft size={14} />}
      </button>
      
      {/* Header */}
      <div className="p-4 border-b dark:border-gray-700 flex items-center gap-2">
        <Database size={16} className="dark:text-white" />
        {!collapsed && (
          <h2 className="text-lg font-semibold dark:text-white">Memory Context</h2>
        )}
      </div>
      
      {/* Memory List */}
      <div className="flex-1 overflow-y-auto">
        {Object.entries(groupedMemories).map(([category, categoryMemories]) => (
          <div key={category} className="p-2">
            {/* Category Header */}
            {!collapsed && (
              <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
                {category}
              </h3>
            )}
            
            {/* Memory Items */}
            <div className="space-y-2">
              {categoryMemories.map((memory) => (
                <div
                  key={memory.id}
                  className="p-3 bg-white dark:bg-gray-800 rounded-lg shadow-sm"
                >
                  {/* Importance Indicator and Toggle */}
                  <div className="flex items-center justify-between mb-1">
                    <div className="flex items-center gap-2">
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
                      {!collapsed && (
                        <button
                          onClick={() => toggleImportance(memory.id, memory.importance)}
                          className="hover:bg-gray-100 dark:hover:bg-gray-700 p-1 rounded"
                        >
                          {memory.importance > 0.7 ? (
                            <Star size={14} className="text-yellow-500" />
                          ) : (
                            <StarOff size={14} className="text-gray-400" />
                          )}
                        </button>
                      )}
                    </div>
                  </div>
                  
                  {/* Content */}
                  {!collapsed && (
                    <>
                      <p className="text-sm text-gray-600 dark:text-gray-300">
                        {memory.content}
                      </p>
                      
                      <div className="mt-2 text-xs text-gray-400">
                        {new Date(memory.timestamp).toLocaleString()}
                      </div>
                    </>
                  )}
                </div>
              ))}
            </div>
          </div>
        ))}
        
        {memories.length === 0 && !collapsed && (
          <div className="text-center text-gray-500 dark:text-gray-400 p-4">
            No memories yet
          </div>
        )}
      </div>
    </div>
  );
};