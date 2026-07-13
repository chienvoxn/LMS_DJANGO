import api from './client';

export const ragAPI = {
  health: () => api.get('/rag/health/'),

  getDocuments: () => api.get('/rag/documents/'),
  uploadDocument: (file, name = '') => {
    const formData = new FormData();
    formData.append('file', file);
    if (name) formData.append('name', name);
    return api.post('/rag/documents/', formData);
  },
  deleteDocument: (id) => api.delete(`/rag/documents/${id}/`),
  reindexDocument: (id) => api.post(`/rag/documents/${id}/reindex/`),

  getConversations: () => api.get('/rag/conversations/'),
  createConversation: (payload = {}) => api.post('/rag/conversations/', payload),
  getConversation: (id) => api.get(`/rag/conversations/${id}/`),
  updateConversation: (id, payload) =>
    api.patch(`/rag/conversations/${id}/`, payload),
  deleteConversation: (id) => api.delete(`/rag/conversations/${id}/`),
  ask: (id, payload) =>
    api.post(`/rag/conversations/${id}/messages/`, payload),
};

export default ragAPI;
