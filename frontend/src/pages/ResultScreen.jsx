import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useInterview } from '../context/InterviewContext';
import { ScoreCard } from '../components/results/ScoreCard';
import { FeedbackCard } from '../components/results/FeedbackCard';
import { RecommendationCard } from '../components/results/RecommendationCard';
import { KnowledgeGapCard } from '../components/results/KnowledgeGapCard';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { RotateCcw, Home, Download } from 'lucide-react';

export const ResultScreen = () => {
  const navigate = useNavigate();
  const { feedbackReport, loading, startSession } = useInterview();

  if (loading) {
    return <LoadingSpinner label="Generating Final Evaluation Report..." size="lg" />;
  }

  if (!feedbackReport) {
    return (
      <div className="text-center py-16">
        <p className="text-slate-400 mb-4">No completed interview feedback report available.</p>
        <button
          onClick={() => navigate('/lobby')}
          className="px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-sm transition-all"
        >
          Start New Interview
        </button>
      </div>
    );
  }

  const handleRetake = async () => {
    try {
      await startSession();
      navigate('/interview');
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="flex flex-col gap-8 py-4 max-w-5xl mx-auto">
      {/* Scorecard */}
      <ScoreCard overallScore={feedbackReport.overall_score} />

      {/* Summary & Feedback */}
      <FeedbackCard
        strengths={feedbackReport.strengths}
        weaknesses={feedbackReport.weaknesses}
        summary={feedbackReport.summary}
      />

      {/* Knowledge Gaps */}
      <KnowledgeGapCard knowledgeGaps={feedbackReport.knowledge_gaps} />

      {/* Recommendations */}
      <RecommendationCard recommendations={feedbackReport.recommendations} />

      {/* Bottom Action Bar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 glass-panel p-6 rounded-2xl">
        <button
          onClick={() => navigate('/')}
          className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-sm transition-all"
        >
          <Home className="w-4 h-4" />
          <span>Return Home</span>
        </button>

        <div className="flex items-center gap-3">
          <button
            onClick={() => window.print()}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-slate-800/90 hover:bg-slate-700 text-slate-200 font-semibold text-sm border border-slate-700 transition-all"
          >
            <Download className="w-4 h-4 text-emerald-400" />
            <span>Export Scorecard PDF</span>
          </button>

          <button
            onClick={handleRetake}
            className="flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold text-sm shadow-xl shadow-blue-500/20 transition-all"
          >
            <RotateCcw className="w-4 h-4" />
            <span>Retake AI Interview</span>
          </button>
        </div>
      </div>
    </div>
  );
};
