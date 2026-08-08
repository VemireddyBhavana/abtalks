import api from '../config/api';

/**
 * Fetches candidate profile and analytics data.
 */
export const getCandidateAnalytics = async () => {
  const response = await api.get('/api/v1/candidate/analytics');
  return response.data;
};

/**
 * Fetches candidate profile.
 */
export const getCandidateProfile = async () => {
  const response = await api.get('/api/v1/candidate');
  return response.data;
};

/**
 * Fetches curriculum details.
 */
export const getCurriculum = async () => {
  const response = await api.get('/api/v1/curriculum');
  return response.data;
};
