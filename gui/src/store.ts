import create from 'zustand';
import { persist } from 'zustand/middleware';
import { invoke } from '@tauri-apps/api/tauri';

interface Settings {
  apiKey: string;
  theme: 'light' | 'dark';
  model: {
    strategist: 'claude-3-sonnet' | 'claude-3-opus';
    worker: 'claude-3-haiku' | 'claude-3-sonnet';
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
  
  // Settings actions
  setApiKey: (key: string) => void;
  setTheme: (theme: 'light' | 'dark') => void;
  setModel: (role: 'strategist' | 'worker', model: string) => void;
  
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
  
  // Processing actions
  processMessage: (chatId: string, message: ChatMessage) => Promise<void>;
}

export const useStore = create<AppState>(
  persist(
    (set, get) => ({
      settings: {
        apiKey: '',
        theme: 'light',
        model: {
          strategist: 'claude-3-sonnet',
          worker: 'claude-3-haiku'
        }
      },
      chats: [],
      memories: [],
      isProcessing: false,

      setApiKey: (key) => 
        set((state) => ({
          settings: { ...state.settings, apiKey: key }
        })),

      setTheme: (theme) => {
        if (theme === 'dark') {
          document.documentElement.classList.add('dark');
        } else {
          document.documentElement.classList.remove('dark');
        }
        set((state) => ({
          settings: { ...state.settings, theme }
        }));
      },

      setModel: (role, model) =>
        set((state) => ({
          settings: { 
            ...state.settings, 
            model: { 
              ...state.settings.model,
              [role]: model 
            } 
          }
        })),

      createChat: () =>
        set((state) => ({
          chats: [
            ...state.chats,
            {
              id: Math.random().toString(36).substring(7),
              title: 'New Chat',
              messages: [],
              created: Date.now(),
              lastUpdated: Date.now()
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
                  messages: [...chat.messages, message],
                  lastUpdated: Date.now()
                }
              : chat
          )
        })),

      deleteChat: (id) =>
        set((state) => ({
          chats: state.chats.filter((chat) => chat.id !== id),
          activeChat: state.activeChat === id ? undefined : state.activeChat
        })),

      renameChat: (id, newTitle) =>
        set((state) => ({
          chats: state.chats.map((chat) =>
            chat.id === id
              ? { ...chat, title: newTitle }
              : chat
          )
        })),

      addMemory: (memory) =>
        set((state) => ({
          memories: [...state.memories, memory]
        })),

      updateMemoryImportance: (id, importance) =>
        set((state) => ({
          memories: state.memories.map((memory) =>
            memory.id === id
              ? { ...memory, importance }
              : memory
          )
        })),

      deleteMemory: (id) =>
        set((state) => ({
          memories: state.memories.filter((memory) => memory.id !== id)
        })),

      processMessage: async (chatId, message) => {
        set({ isProcessing: true });
        try {
          // Get relevant memories for context
          const state = get();
          const relevantMemories = state.memories
            .filter(m => m.importance > 0.5)
            .map(m => m.content)
            .join('\n');

          // Process with AI
          const response = await invoke<{
            content: string;
            memories: Memory[];
          }>('process_message', {
            apiKey: state.settings.apiKey,
            message: message.content,
            context: relevantMemories,
            model: state.settings.model.strategist
          });

          // Add AI response
          const aiMessage: ChatMessage = {
            id: Math.random().toString(36).substring(7),
            role: 'assistant',
            content: response.content,
            timestamp: Date.now(),
            metadata: {
              model: state.settings.model.strategist,
              processingTime: Date.now() - message.timestamp
            }
          };
          state.addMessage(chatId, aiMessage);

          // Store new memories
          response.memories.forEach(memory => {
            state.addMemory({
              ...memory,
              source: {
                chatId,
                messageId: message.id
              }
            });
          });
        } catch (error) {
          console.error('Error processing message:', error);
          // Add error message
          const errorMessage: ChatMessage = {
            id: Math.random().toString(36).substring(7),
            role: 'assistant',
            content: 'Sorry, there was an error processing your message.',
            timestamp: Date.now()
          };
          get().addMessage(chatId, errorMessage);
        } finally {
          set({ isProcessing: false });
        }
      }
    }),
    {
      name: 'mastermind-storage',
      getStorage: () => localStorage,
      partialize: (state) => ({
        settings: state.settings,
        chats: state.chats,
        memories: state.memories
      })
    }
  )
);