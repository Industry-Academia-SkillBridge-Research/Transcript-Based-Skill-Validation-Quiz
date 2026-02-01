import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add response interceptor for better error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error status
      console.error('API Error:', error.response.status, error.response.data);
    } else if (error.request) {
      // Request made but no response received
      console.error('Network Error: No response from server');
      error.message = 'Cannot connect to server. Please ensure the backend is running on http://localhost:8000';
    } else {
      // Something else happened
      console.error('Error:', error.message);
    }
    return Promise.reject(error);
  }
);

// Transcript endpoints
export const uploadTranscript = async (studentId, file) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('student_id', studentId);
  const response = await api.post(`/transcript/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getTranscript = async (studentId) => {
  const response = await api.get(`/transcript/${studentId}`);
  return response.data;
};

// Skills endpoints
export const getClaimedSkills = async (studentId) => {
  const response = await api.get(`/students/${studentId}/skills/parents/claimed`);
  return response.data;
};

export const getChildSkills = async (studentId) => {
  const response = await api.get(`/students/${studentId}/skills/claimed`);
  return response.data;
};

export const getParentSkills = async (studentId) => {
  const response = await api.get(`/students/${studentId}/skills/parent`);
  return response.data;
};

export const getChildSkillEvidence = async (studentId, skillName) => {
  const response = await api.get(`/students/${studentId}/skills/claimed/${encodeURIComponent(skillName)}/evidence`);
  return response.data;
};

export const getParentSkillEvidence = async (studentId, parentSkill) => {
  const response = await api.get(`/students/${studentId}/skills/parent/${encodeURIComponent(parentSkill)}/evidence`);
  return response.data;
};

// XAI endpoints
export const getSkillsSummary = async (studentId) => {
  const response = await api.get(`/students/${studentId}/xai/skills/summary`);
  return response.data;
};

export const getSkillExplanation = async (studentId, skillName, skillType = 'parent') => {
  const response = await api.get(`/students/${studentId}/xai/skills/${encodeURIComponent(skillName)}/explain`, {
    params: { skill_type: skillType }
  });
  return response.data;
};

// Quiz endpoints
export const planQuiz = async (studentId, selectedSkills) => {
  const response = await api.post(`/students/${studentId}/quiz/plan`, {
    selected_skills: selectedSkills,
  });
  return response.data;
};

export const generateQuizFromBank = async (studentId) => {
  const response = await api.post(`/students/${studentId}/quiz/from-bank`);
  return response.data;
};

export const submitQuiz = async (studentId, attemptId, answers) => {
  const response = await api.post(`/students/${studentId}/quiz/${attemptId}/submit`, {
    answers,
  });
  return response.data;
};

// Job Recommendation endpoints
export const getJobRecommendations = async (studentId, params = {}) => {
  const response = await api.get(`/students/${studentId}/jobs/recommend`, {
    params: {
      top_k: params.topK || 10,
      threshold: params.threshold || 70,
      role_key: params.roleKey || undefined
    }
  });
  return response.data;
};

export const getJobDetails = async (jobId) => {
  const response = await api.get(`/jobs/${jobId}`);
  return response.data;
};

// Portfolio endpoints
export const getStudentPortfolio = async (studentId) => {
  const response = await api.get(`/students/${studentId}/profile/portfolio`);
  return response.data;
};

export const getStudentProfile = async (studentId) => {
  const response = await api.get(`/students/${studentId}/profile`);
  return response.data;
};

export const updateStudentProfile = async (studentId, profileData) => {
  const response = await api.put(`/students/${studentId}/profile`, profileData);
  return response.data;
};

export const uploadProfilePhoto = async (studentId, file) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post(`/students/${studentId}/profile/photo`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export default api;
