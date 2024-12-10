import React from 'react';
import { Sidebar } from './Sidebar';
import { ChatArea } from './ChatArea';
import { MemoryPanel } from './MemoryPanel';
import { useStore } from '../store';

export const Layout: React.FC = () => {
  const theme = useStore((state) => state.settings.theme);
  
  return (
    <div className={`h-screen flex bg-white ${theme === 'dark' ? 'dark' : ''}`}>
      <Sidebar />
      <div className="flex flex-1">
        <ChatArea />
        <MemoryPanel />
      </div>
    </div>
  );
};