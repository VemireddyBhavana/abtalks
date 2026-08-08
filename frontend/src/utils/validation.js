export const isValidAnswerText = (text) => {
  return typeof text === 'string' && text.trim().length >= 5;
};

export const isValidCandidateId = (candidateId) => {
  return typeof candidateId === 'string' && candidateId.trim().length > 0;
};
