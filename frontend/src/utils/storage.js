export const getItem = (key, fallback = null) => {
  try {
    const item = window.localStorage.getItem(key);
    return item ? JSON.parse(item) : fallback;
  } catch (e) {
    console.error(`storage getItem error for key '${key}':`, e);
    return fallback;
  }
};

export const setItem = (key, value) => {
  try {
    window.localStorage.setItem(key, JSON.stringify(value));
  } catch (e) {
    console.error(`storage setItem error for key '${key}':`, e);
  }
};

export const removeItem = (key) => {
  try {
    window.localStorage.removeItem(key);
  } catch (e) {
    console.error(`storage removeItem error for key '${key}':`, e);
  }
};
