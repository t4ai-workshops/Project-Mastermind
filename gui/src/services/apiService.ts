import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const chatService = {
  async sendMessage(message: string, context: string = '') {
    try {
      const response = await axios.post(`${API_BASE_URL}/chat`, { 
        message, 
        context 
      });
      return response.data.response;
    } catch (error) {
      console.error('Chat API Error:', error);
      throw error;
    }
  },

  async generateCode(prompt: string, language: string = 'python') {
    try {
      const response = await axios.post(`${API_BASE_URL}/generate-code`, { 
        prompt, 
        language 
      });
      return response.data.code;
    } catch (error) {
      console.error('Code Generation API Error:', error);
      throw error;
    }
  }
};
