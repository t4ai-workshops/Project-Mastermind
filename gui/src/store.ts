/**
 * Mastermind AI Store
 * 
 * Central state management using Zustand.
 * Handles:
 * - Chat management
 * - API communication
 * - Memory management
 * - Settings and configuration
 * - Message processing
 * 
 * Features:
 * - Persistent storage
 * - Immer integration for immutable updates
 * - Type safety
 * - Error handling
 * - Fallback API communication
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';
import { invoke } from '@tauri-apps/api/tauri';
import axios from 'axios';

// Type definitions
declare global {
  interface Window {
    __TAURI_IPC__: (message: any) => void;
    __TAURI_METADATA__?: any;
  }
}

/** Model types for different use cases */
type ModelStrategist = 'claude-3-opus' | 'claude-3-sonnet';
type ModelWorker = 'claude-3-haiku' | 'claude-3-sonnet';
type Theme = 'light' | 'dark';

/** Settings interface */
interface Settings {
  apiKey: string;
  theme: Theme;
  model: {
    strategist: ModelStrategist;
    worker: ModelWorker;
  };
}

/** Chat message interface */
export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: number;
  metadata?: {
    model?: string;
    context?: string[];
    processingTime?: number;
  };
  files?: File[];
  error?: string;
}

/** Chat interface */
export interface Chat {
  id: string;
  title: string;
  messages: ChatMessage[];
  created: number;
  lastUpdated: number;
}

/** Memory interface */
export interface Memory {
  id: string;
  content: string;
  category: string;
  importance: number;
  timestamp: number;
  metadata: Record<string, any>;
  source?: {
    chatId: string;
    messageId: string;
  };
}

/** Main application state interface */
interface AppState {
  settings: Settings;
  chats: Chat[];
  activeChat?: string;
  memories: Memory[];
  isProcessing: boolean;
  
  // Settings actions
  setApiKey: (key: string) => void;
  setTheme: (theme: Theme) => void;
  setModel: (role: 'strategist' | 'worker', model: ModelStrategist | ModelWorker) => void;
  
  // Chat actions
  createChat: () => void;
  setActiveChat: (id: string) => void;
  addMessage: (chatId: string, message: ChatMessage) => void;
  deleteChat: (id: string) => void;
  renameChat: (id: string, newTitle: string) => void;
  
  // Memory actions
  addMemory: (memory: Memory) => void;
  updateMemoryImportance: (id: string, importance: number) => void;
  deleteMemory: (id: string) => void;
  
  // Message processing
  processMessage: (chatId: string, message: ChatMessage) => Promise<void>;
}

/** Check if Tauri is available */
const isTauriAvailable = (): boolean => {
  return typeof window.__TAURI_IPC__ === 'function';
};

/**
 * Safe invoke function that falls back to HTTP if Tauri is not available
 * @param cmd Command to invoke
 * @param args Arguments for the command
 */
const safeTauriInvoke = async (cmd: string, args: any) => {
  try {
    if (isTauriAvailable()) {
      return await invoke(cmd, args);
    }
  } catch (tauriError) {
    console.error('Tauri invoke failed:', tauriError);
    throw new Error(`Tauri Error: ${tauriError}`);
  }

  try {
    const response = await axios.post(`http://localhost:8000/${cmd}`, args);
    return response.data;
  } catch (httpError) {
    console.error('HTTP fallback failed:', httpError);
    if (axios.isAxiosError(httpError) && httpError.response) {
      throw new Error(`API Error: ${httpError.response.data.detail || httpError.message}`);
    }
    throw httpError;
  }
};

// Default settings
const defaultSettings: Settings = {
  apiKey: '',
  theme: 'light',
  model: {
    strategist: 'claude-3-sonnet',
    worker: 'claude-3-haiku'
  }
};

// Create store with persistence
export const useStore = create<AppState>()(
  persist(
    immer((set, get) => ({
      // State
      settings: { ...defaultSettings },
      chats: [],
      memories: [],
      isProcessing: false,

      // Settings actions
      setApiKey: (key) => set((state) => {
        state.settings.apiKey = key;
      }),

      setTheme: (theme) => set((state) => {
        if (theme === 'dark') {
          document.documentElement.classList.add('dark');
        } else {
          document.documentElement.classList.remove('dark');
        }
        state.settings.theme = theme;
      }),

      setModel: (role, model) => set((state) => {
        if (role === 'strategist') {
          state.settings.model.strategist = model as ModelStrategist;
        } else {
          state.settings.model.worker = model as ModelWorker;
        }
      }),

      // Chat actions
      createChat: () => set((state) => {
        state.chats.push({
          id: Math.random().toString(36).substring(7),
          title: 'New Chat',
          messages: [],
          created: Date.now(),
          lastUpdated: Date.now()
        });
      }),

      setActiveChat: (id) => set((state) => {
        state.activeChat = id;
      }),

      addMessage: (chatId, message) => set((state) => {
        const chat = state.chats.find(c => c.id === chatId);
        if (chat) {
          chat.messages.push(message);
          chat.lastUpdated = Date.now();
        }
      }),

      deleteChat: (id) => set((state) => {
        state.chats = state.chats.filter((chat) => chat.id !== id);
        state.activeChat = state.activeChat === id ? undefined : state.activeChat;
      }),

      renameChat: (id, newTitle) => set((state) => {
        const chat = state.chats.find(c => c.id === id);
        if (chat) {
          chat.title = newTitle;
        }
      }),

      // Memory actions
      addMemory: (memory) => set((state) => {
        state.memories.push(memory);
      }),

      updateMemoryImportance: (id, importance) => set((state) => {
        const memory = state.memories.find(m => m.id === id);
        if (memory) {
          memory.importance = importance;
        }
      }),

      deleteMemory: (id) => set((state) => {
        state.memories = state.memories.filter((memory) => memory.id !== id);
      }),

      // Message processing
      processMessage: async (chatId, message) => {
        set((state) => {
          state.isProcessing = true;
        });

        try {
          const state = get();
          const modelStrategist = state.settings?.model?.strategist ?? 'claude-3-sonnet';

          // Get relevant memories for context
          const relevantMemories = state.memories
            .filter(m => m.importance > 0.5)
            .map(m => m.content)
            .join('\n');

          // Process message through Tauri/API
          const response = await safeTauriInvoke('process_message', {
            apiKey: state.settings.apiKey,
            message: message.content,
            context: relevantMemories,
            model: modelStrategist
          });

          // Create AI response message
          const aiMessage: ChatMessage = {
            id: Math.random().toString(36).substr(2, 9),
            role: 'assistant',
            content: response.content,
            timestamp: Date.now(),
            metadata: {
              model: modelStrategist
            }
          };

          // Update state with response
          set((state) => {
            const chat = state.chats.find(c => c.id === chatId);
            if (chat) {
              chat.messages.push(aiMessage);
              chat.lastUpdated = Date.now();
            }
            state.isProcessing = false;
          });

          // Handle any new memories from response
          if (response.memories && response.memories.length > 0) {
            set((state) => {
              state.memories.push(...response.memories);
            });
          }
        } catch (error) {
          console.error('Error processing message:', error);
          
          // Add error message to chat
          const errorMessage: ChatMessage = {
            id: Math.random().toString(36).substr(2, 9),
            role: 'assistant',
            content: 'Sorry, er is een fout opgetreden bij het verwerken van je bericht.',
            timestamp: Date.now(),
            error: error instanceof Error ? error.message : 'Unknown error'
          };

          set((state) => {
            const chat = state.chats.find(c => c.id === chatId);
            if (chat) {
              chat.messages.push(errorMessage);
            }
            state.isProcessing = false;
          });
        }
      }
    })),
    {
      name: 'mastermind-storage',
      migrate: (persistedState: any) => {
        return {
          ...defaultSettings,
          ...persistedState,
          settings: {
            ...defaultSettings,
            ...persistedState?.settings
          }
        };
      }
    }
  )
);