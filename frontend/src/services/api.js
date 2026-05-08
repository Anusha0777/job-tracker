import axios from 'axios';
const API_BASE_URL = "https://job-tracker-s5hl.onrender.com";


const REQUEST_TIMEOUT = 10000; // 10 seconds

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: REQUEST_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use((config) => {
  console.log(`[API] ${config.method.toUpperCase()} ${config.url}`);
  return config;
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message = error.response?.data?.detail || error.message || 'Unknown error occurred';
    const status = error.response?.status;

    console.error(`[API ERROR] Status: ${status}, Message: ${message}`);

    // Create a more helpful error message
    if (!error.response) {
      error.message = `Cannot connect to backend. Make sure the backend server is running at http://localhost:8000.`;
    } else if (status === 404) {
      error.message = `Resource not found (${message})`;
    } else if (status === 400) {
      error.message = `Invalid request: ${message}`;
    } else if (status === 500) {
      error.message = `Server error: ${message}`;
    }

    return Promise.reject(error);
  }
);

// Job Application endpoints
export const applicationService = {
  getAll: async () => {
    try {
      const response = await api.get('/applications');
      return response.data;
    } catch (error) {
      throw new Error(error.message || 'Failed to fetch applications');
    }
  },

  create: async (company, role, applicationDate, status = 'Applied') => {
    try {
      const response = await api.post('/applications', {
        company,
        role,
        application_date: applicationDate || new Date().toISOString(),
        status,
      });
      return response.data;
    } catch (error) {
      throw new Error(error.message || 'Failed to create application');
    }
  },

  updateStatus: async (id, status) => {
    try {
      const response = await api.patch(`/applications/${id}`, {
        status,
      });
      return response.data;
    } catch (error) {
      throw new Error(error.message || 'Failed to update application status');
    }
  },

  delete: async (id) => {
    try {
      const response = await api.delete(`/applications/${id}`);
      return response.data;
    } catch (error) {
      throw new Error(error.message || 'Failed to delete application');
    }
  },
};

// Stats endpoint
export const statsService = {
  getStats: async () => {
    try {
      const response = await api.get('/stats');
      return response.data;
    } catch (error) {
      throw new Error(error.message || 'Failed to fetch statistics');
    }
  },
};

// AI tip endpoint
export const aiService = {
  generateTip: async (jobDescription) => {
    try {
      const response = await api.post('/ai-tip', {
        job_description: jobDescription,
      });
      return response.data;
    } catch (error) {
      if (error.message.includes('Cannot connect')) {
        throw new Error('Backend server is not running. Please start it at http://localhost:8000.');
      }
      throw new Error(error.message || 'Failed to generate resume tips');
    }
  },
};

export default api;
