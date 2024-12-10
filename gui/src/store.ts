import create from 'zustand';
import { persist } from 'zustand/middleware';

interface Settings {
  apiKey: string;
  theme: 'light' | 'dark';
}

interface Chat {
  id: string;
  title: string;
  messages: ChatMessage[];
}

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: number;
  metadata?: {
    model?: string;
    context?: string[];
    processingTime?: number;
  };
}

interface Memory {
  id: string;
  content: string;
  category: string;
  importance: number;
  timestamp: number;
  metadata: Record<string, any>;
}

interface AppState {
  settings: Settings;
  chats: Chat[];
  activeChat?: string;
  memories: Memory[];
  isProcessing: boolean;
  
  // Settings actions
  setApiKey: (key: string) => void;
  setTheme: (theme: 'light' | 'dark') => void;
  
  // Chat actions
  createChat: () => void;
  setActiveChat: (id: string) => void;
  addMessage: (chatId: string, message: ChatMessage) => void;
  
  // Memory actions
  addMemory: (memory: Memory) => void;
  updateMemory: (id: string, updates: Partial<Memory>) => void;
  
  // Status actions
  setProcessing: (status: boolean) => void;
}

export const useStore = create<AppState>(
  persist(
    (set) => ({
      settings: {
        apiKey: '',
        theme: 'light',
      },
      chats: [],
      memories: [],
      isProcessing: false,

      setApiKey: (key) => 
        set((state) => ({
          settings: { ...state.settings, apiKey: key }
        })),

      setTheme: (theme) =>
        set((state) => ({
          settings: { ...state.settings, theme }
        })),

      createChat: () =>
        set((state) => ({
          chats: [
            ...state.chats,
            {
              id: Math.random().toString(36).substring(7),
              title: 'New Chat',
              messages: []
            }
          ]
        })),

      setActiveChat: (id) =>
        set(() => ({
          activeChat: id
        })),

      addMessage: (chatId, message) =>
        set((state) => ({
          chats: state.chats.map((chat) =>
            chat.id === chatId
              ? {
                  ...chat,
                  messages: [...chat.messages, message]
                }
              : chat
          )
        })),

      addMemory: (memory) =>
        set((state) => ({
          memories: [...state.memories, memory]
        })),

      updateMemory: (id, updates) =>
        set((state) => ({
          memories: state.memories.map((memory) =>
            memory.id === id
              ? { ...memory, ...updates }
              : memory
          )
        })),

      setProcessing: (status) =>
        set(() => ({
          isProcessing: status
        }))
    }),
    {
      name: 'mastermind-storage',
      getStorage: () => localStorage
    }
  )
);