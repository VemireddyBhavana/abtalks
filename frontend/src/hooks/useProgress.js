export const useProgress = (currentIndex = 0, total = 8) => {
  const percentage = Math.round(((currentIndex + 1) / total) * 100);
  const remaining = total - (currentIndex + 1);

  return {
    percentage: Math.min(100, Math.max(0, percentage)),
    currentStep: currentIndex + 1,
    totalSteps: total,
    remainingSteps: Math.max(0, remaining),
    isCompleted: currentIndex + 1 >= total,
  };
};
