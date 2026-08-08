export const generateUniqueId = (prefix = 'id') => {
  return `${prefix}_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
};

export const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
