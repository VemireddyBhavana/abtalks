import { useInterview } from '../context/InterviewContext';

export const useSession = () => {
  const { sessionId, isCompleted, currentQuestionIndex, totalQuestions, startSession, loading } = useInterview();

  return {
    sessionId,
    isCompleted,
    currentQuestionIndex,
    totalQuestions,
    startSession,
    loading,
  };
};
