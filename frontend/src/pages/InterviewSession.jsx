import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useInterview } from '../context/InterviewContext';
import { QuestionCard } from '../components/session/QuestionCard';
import { AnswerEditor } from '../components/session/AnswerEditor';
import { ProgressTracker } from '../components/session/ProgressTracker';
import { Timer } from '../components/session/Timer';
import { LoadingSpinner } from '../components/common/LoadingSpinner';

export const InterviewSession = () => {
  const navigate = useNavigate();
  const {
    sessionId,
    currentQuestion,
    currentQuestionIndex,
    totalQuestions,
    answerText,
    setAnswerText,
    submitTurnAnswer,
    isCompleted,
    loading,
  } = useInterview();

  useEffect(() => {
    if (isCompleted) {
      navigate('/result');
    }
  }, [isCompleted, navigate]);

  if (!sessionId) {
    return (
      <div className="text-center py-16">
        <p className="text-slate-400 mb-4">No active interview session found.</p>
        <button
          onClick={() => navigate('/lobby')}
          className="px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-sm transition-all"
        >
          Go to Lobby
        </button>
      </div>
    );
  }

  if (loading && !currentQuestion) {
    return <LoadingSpinner label="Loading Next Question..." />;
  }

  return (
    <div className="flex flex-col gap-6 max-w-4xl mx-auto py-4">
      {/* Session Top Bar */}
      <div className="glass-panel rounded-2xl p-4 border border-slate-700/50 flex flex-col sm:flex-row items-center justify-between gap-4">
        <ProgressTracker
          currentQuestionIndex={currentQuestionIndex}
          totalQuestions={totalQuestions}
        />
        <Timer initialSeconds={300} />
      </div>

      {/* Question Card */}
      {currentQuestion && <QuestionCard question={currentQuestion} />}

      {/* Answer Workspace */}
      <AnswerEditor
        value={answerText}
        onChange={setAnswerText}
        onSubmit={submitTurnAnswer}
        loading={loading}
        disabled={isCompleted}
      />
    </div>
  );
};
