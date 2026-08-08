/**
 * @typedef {Object} InterviewQuestion
 * @property {string} id - Question ID
 * @property {string} text - Question text
 * @property {string} category - Skill domain category
 */

/**
 * @typedef {Object} InterviewConfig
 * @property {string} id - Interview config ID
 * @property {string} roleTitle - Target position title
 * @property {number} durationMinutes - Estimated session duration
 */

export const InterviewPlaceholder = {
  id: '',
  roleTitle: '',
  durationMinutes: 30,
};

export default InterviewPlaceholder;
