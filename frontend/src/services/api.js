import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Job Application endpoints
export const applicationService = {
  getAll: async () => {
    const response = await api.get('/applications');
    return response.data;
  },

  create: async (company, role, applicationDate) => {
    const response = await api.post('/applications', {
      company,
      role,
      application_date: applicationDate || new Date().toISOString(),
    });
    return response.data;
  },

  updateStatus: async (id, status) => {
    const response = await api.patch(`/applications/${id}`, {
      status,
    });
    return response.data;
  },

  delete: async (id) => {
    const response = await api.delete(`/applications/${id}`);
    return response.data;
  },
};

// Stats endpoint
export const statsService = {
  getStats: async () => {
    const response = await api.get('/stats');
    return response.data;
  },
};

// AI tip endpoint
export const aiService = {
  generateTip: async (jobDescription) => {
    const response = await api.post('/ai-tip', {
      job_description: jobDescription,
    });
    return response.data;
  },
};

export default api;
