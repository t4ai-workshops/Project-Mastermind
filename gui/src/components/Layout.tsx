/**
 * Layout Component
 * 
 * Main layout component that structures the application interface.
 * Uses CSS Grid for a responsive three-column layout with fixed sidebars.
 * 
 * Structure:
 * - Sidebar (fixed width)
 * - Main content area (flexible)
 *   - Chat area (scrollable)
 *   - Message input (fixed)
 * - Memory panel (fixed width)
 * 
 * Features:
 * - Responsive grid layout
 * - macOS window controls integration
 * - Dark mode support
 * - Overflow handling
 * 
 * @component
 */

import React, { useEffect } from 'react';
import { Sidebar } from './Sidebar';
import { ChatArea } from './ChatArea';
import { MemoryPanel } from './MemoryPanel';
import { useStore } from '../store';
import { appWindow } from '@tauri-apps/api/window';
import { MessageInput } from './MessageInput';

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
    <div className="grid grid-cols-[256px_1fr_256px] h-screen overflow-hidden bg-white dark:bg-gray-900">
      {/* Left sidebar */}
      <Sidebar />

      {/* Main content area */}
      <div className="grid grid-rows-[1fr_auto] overflow-hidden">
        <ChatArea />
        <MessageInput />
      </div>

      {/* Right memory panel */}
      <MemoryPanel />
    </div>
  );
};