import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { InterviewProvider } from './context/InterviewContext';
import { MainLayout } from './layouts/MainLayout';
import { Home } from './pages/Home';
import { CandidateDashboard } from './pages/CandidateDashboard';
import { InterviewLobby } from './pages/InterviewLobby';
import { InterviewSession } from './pages/InterviewSession';
import { LoadingScreen } from './pages/LoadingScreen';
import { ResultScreen } from './pages/ResultScreen';
import { InterviewHistory } from './pages/InterviewHistory';
import { NotFound } from './pages/NotFound';

export function App() {
  return (
    <InterviewProvider>
      <Router>
        <MainLayout>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/dashboard" element={<CandidateDashboard />} />
            <Route path="/lobby" element={<InterviewLobby />} />
            <Route path="/interview" element={<InterviewSession />} />
            <Route path="/loading" element={<LoadingScreen />} />
            <Route path="/result" element={<ResultScreen />} />
            <Route path="/history" element={<InterviewHistory />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </MainLayout>
      </Router>
    </InterviewProvider>
  );
}

export default App;
