import { useState, useEffect } from 'react';

export const useTimer = (initialSeconds = 300, onExpire = null) => {
  const [secondsLeft, setSecondsLeft] = useState(initialSeconds);
  const [isRunning, setIsRunning] = useState(true);

  useEffect(() => {
    if (!isRunning || secondsLeft <= 0) {
      if (secondsLeft === 0 && onExpire) onExpire();
      return;
    }

    const interval = setInterval(() => {
      setSecondsLeft((prev) => prev - 1);
    }, 1000);

    return () => clearInterval(interval);
  }, [secondsLeft, isRunning, onExpire]);

  const mins = Math.floor(secondsLeft / 60);
  const secs = secondsLeft % 60;
  const formattedTime = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;

  return {
    secondsLeft,
    formattedTime,
    isRunning,
    startTimer: () => setIsRunning(true),
    pauseTimer: () => setIsRunning(false),
    resetTimer: (newSecs = initialSeconds) => {
      setSecondsLeft(newSecs);
      setIsRunning(true);
    },
  };
};
