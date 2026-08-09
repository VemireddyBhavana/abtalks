import apiClient from './apiClient';
import { API_ENDPOINTS } from '../constants/api';

/**
 * Fetches candidate profile and analytics data.
 */
export const getCandidateAnalytics = async (signal = null) => {
  const response = await apiClient.get(API_ENDPOINTS.CANDIDATE_ANALYTICS, { signal });
  return response.data;
};

/**
 * Fetches candidate profile.
 */
export const getCandidateProfile = async (signal = null) => {
  const response = await apiClient.get(API_ENDPOINTS.CANDIDATE_PROFILE, { signal });
  return response.data;
};

/**
 * Fetches curriculum details.
 */
export const getCurriculum = async (signal = null) => {
  const response = await apiClient.get(API_ENDPOINTS.CURRICULUM, { signal });
  return response.data;
};
