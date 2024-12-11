import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';
import { invoke } from '@tauri-apps/api/tauri';
import axios from 'axios';

// Extend Window interface to include Tauri-specific properties
declare global {
  interface Window {
    __TAURI_IPC__: (message: any) => void;
    __TAURI_METADATA__?: any;
  }
}

// Type guard to check Tauri IPC availability
const isTauriAvailable = (): boolean => {
  return typeof window.__TAURI_IPC__ === 'function';
};

// Fallback function for invoke when in browser
const safeTauriInvoke = async (cmd: string, args: any) => {
  try {
    // Try Tauri invoke first
    if (isTauriAvailable()) {
      return await invoke(cmd, args);
    }
  } catch (tauriError) {
    console.error('Tauri invoke failed:', tauriError);
    throw tauriError;
  }

  // Fallback to HTTP request
  try {
    const response = await axios.post(`http://localhost:8000/${cmd}`, args);
    return response.data;
  } catch (httpError) {
    console.error('HTTP fallback failed:', httpError);
    throw httpError;
  }
};

// Define more precise types
type ModelStrategist = 'claude-3-sonnet' | 'claude-3-opus';
type ModelWorker = 'claude-3-haiku' | 'claude-3-sonnet';
type Theme = 'light' | 'dark';

interface Settings {
  apiKey: string;
  theme: Theme;
  model: {
    strategist: ModelStrategist;
    worker: ModelWorker;
  };
}

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
}

export interface Chat {
  id: string;
  title: string;
  messages: ChatMessage[];
  created: number;
  lastUpdated: number;
}

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

interface AppState {
  settings: Settings;
  chats: Chat[];
  activeChat?: string;
  memories: Memory[];
  isProcessing: boolean;
  
  setApiKey: (key: string) => void;
  setTheme: (theme: Theme) => void;
  setModel: (role: 'strategist' | 'worker', model: ModelStrategist | ModelWorker) => void;
  
  createChat: () => void;
  setActiveChat: (id: string) => void;
  addMessage: (chatId: string, message: ChatMessage) => void;
  deleteChat: (id: string) => void;
  renameChat: (id: string, newTitle: string) => void;
  
  addMemory: (memory: Memory) => void;
  updateMemoryImportance: (id: string, importance: number) => void;
  deleteMemory: (id: string) => void;
  
  processMessage: (chatId: string, message: ChatMessage) => Promise<void>;
}

// Safe default settings
const defaultSettings: Settings = {
  apiKey: '',
  theme: 'light',
  model: {
    strategist: 'claude-3-sonnet',
    worker: 'claude-3-haiku'
  }
};

export const useStore = create<AppState>()(
  persist(
    immer((set, get) => ({
      settings: { ...defaultSettings },
      chats: [],
      memories: [],
      isProcessing: false,

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

      processMessage: async (chatId, message) => {
        set((state) => {
          state.isProcessing = true;
        });

        try {
          const state = get();
          const modelStrategist = state.settings?.model?.strategist ?? 'claude-3-sonnet';

          const relevantMemories = state.memories
            .filter(m => m.importance > 0.5)
            .map(m => m.content)
            .join('\n');

          const response = await safeTauriInvoke('process_message', {
            apiKey: state.settings.apiKey,
            message: message.content,
            context: relevantMemories,
            model: modelStrategist
          });

          const aiMessage: ChatMessage = {
            id: Math.random().toString(36).substr(2, 9),
            role: 'assistant',
            content: response.content,
            timestamp: Date.now(),
            metadata: {
              model: modelStrategist
            }
          };

          set((state) => {
            const chat = state.chats.find(c => c.id === chatId);
            if (chat) {
              chat.messages.push(aiMessage);
              chat.lastUpdated = Date.now();
            }
            state.isProcessing = false;
          });

          if (response.memories && response.memories.length > 0) {
            set((state) => {
              state.memories.push(...response.memories);
            });
          }
        } catch (error) {
          console.error('Error processing message:', error);
          set((state) => {
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