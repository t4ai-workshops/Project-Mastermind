import axios from 'axios';

// Use environment variable or default to localhost
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface ChatResponse {
  response: string;
}

export interface CodeResponse {
  code: string;
}

export const apiService = {
  async sendMessage(message: string, context: string = '') {
    try {
      const response = await axios.post<ChatResponse>(`${API_BASE_URL}/chat`, {
        message,
        context
      });
      return response.data.response;
    } catch (error) {
      console.error('Chat API Error:', error);
      throw new Error(error instanceof Error ? error.message : 'Failed to send message');
    }
  },

  async generateCode(prompt: string, language: string = 'python') {
    try {
      const response = await axios.post<CodeResponse>(`${API_BASE_URL}/generate-code`, {
        prompt,
        language
      });
      return response.data.code;
    } catch (error) {
      console.error('Code Generation API Error:', error);
      throw new Error(error instanceof Error ? error.message : 'Failed to generate code');
    }
  },

  async checkHealth() {
    try {
      const response = await axios.get(`${API_BASE_URL}/health`);
      return response.data.status === 'healthy';
    } catch (error) {
      console.error('Health Check Error:', error);
      return false;
    }
  }
};