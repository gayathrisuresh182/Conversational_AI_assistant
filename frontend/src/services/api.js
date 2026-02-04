import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const sendMessage = async (data) => {
  const response = await api.post('/api/chat/message', data);
  return response.data;
};

export const getConversations = async (userId) => {
  const response = await api.get(`/api/chat/conversations/${userId}`);
  return response.data;
};

export const getMessages = async (conversationId) => {
  const response = await api.get(`/api/chat/conversations/${conversationId}/messages`);
  return response.data;
};

export const uploadDocument = async (userId, file) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('user_id', userId);
  
  const response = await axios.post(
    `${API_URL}/api/documents/upload`,
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }
  );
  return response.data;
};

export const getDocuments = async (userId) => {
  const response = await api.get(`/api/documents/${userId}`);
  return response.data;
};

