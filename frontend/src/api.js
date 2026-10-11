import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getProposals = async (status = null) => {
  const params = status && status !== 'all' ? { status } : {};
  const response = await api.get('/proposals/', { params });
  return response.data;
};

export const getProposalDetail = async (id) => {
  const response = await api.get(`/proposals/${id}`);
  return response.data;
};

export const createProposal = async (data) => {
  const response = await api.post('/proposals/', data);
  return response.data;
};

export const castVote = async (proposalId, data) => {
  const response = await api.post(`/proposals/${proposalId}/vote`, data);
  return response.data;
};

export const revokeVote = async (voteId) => {
  const response = await api.delete(`/votes/${voteId}`);
  return response.data;
};

export const closeProposal = async (proposalId, adminToken = 'karthi123') => {
  const token = adminToken || localStorage.getItem('voting_admin_token') || 'karthi123';
  const response = await api.patch(
    `/proposals/${proposalId}/close`,
    {},
    {
      headers: {
        'X-Admin-Token': token,
      },
    }
  );
  return response.data;
};

export default api;
