import React, { useEffect } from 'react';
import { Sidebar } from './Sidebar';
import { ChatArea } from './ChatArea';
import { MemoryPanel } from './MemoryPanel';
import { useStore } from '../store';
import { appWindow } from '@tauri-apps/api/window';

export const Layout: React.FC = () => {
  const theme = useStore((state) => state.settings.theme);
  
  // Set up macOS window controls
  useEffect(() => {
    const setupWindow = async () => {
      try {
        // Enable window controls and dragging on titlebar
        document.getElementById('titlebar')?.addEventListener('mousedown', () => {
          appWindow.startDragging();
        });
      } catch (error) {
        console.error('Failed to setup window controls:', error);
      }
    };
    
    setupWindow();
  }, []);
  
  return (
    <div className="h-screen flex flex-col bg-white dark:bg-gray-900">
      {/* Titlebar for macOS */}
      <div 
        id="titlebar" 
        className="h-8 bg-transparent fixed inset-x-0 top-0 z-50"
        data-tauri-drag-region
      />
      
      {/* Main content */}
      <div className={`flex flex-1 ${theme === 'dark' ? 'dark' : ''}`}>
        <Sidebar />
        <div className="flex flex-1 pt-8"> {/* Add padding-top for titlebar */}
          <ChatArea />
          <MemoryPanel />
        </div>
      </div>
    </div>
  );
};