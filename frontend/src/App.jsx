import React, { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import { InterviewProvider } from './context/InterviewContext';
import { ErrorBoundary } from './components/common/ErrorBoundary';
import { MainLayout } from './layouts/MainLayout';
import { LoadingSpinner } from './components/common/LoadingSpinner';

// Lazy loaded page components
const HomePage = lazy(() => import('./features/home/HomePage').then(m => ({ default: m.HomePage })));
const DashboardPage = lazy(() => import('./features/dashboard/DashboardPage').then(m => ({ default: m.DashboardPage })));
const LobbyPage = lazy(() => import('./features/interview/LobbyPage').then(m => ({ default: m.LobbyPage })));
const SessionPage = lazy(() => import('./features/interview/SessionPage').then(m => ({ default: m.SessionPage })));
const LoadingScreen = lazy(() => import('./pages/LoadingScreen').then(m => ({ default: m.LoadingScreen })));
const ResultPage = lazy(() => import('./features/results/ResultPage').then(m => ({ default: m.ResultPage })));
const HistoryPage = lazy(() => import('./features/history/HistoryPage').then(m => ({ default: m.HistoryPage })));
const NotFound = lazy(() => import('./pages/NotFound').then(m => ({ default: m.NotFound })));

export function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider>
        <InterviewProvider>
          <Router>
            <MainLayout>
              <Suspense fallback={<LoadingSpinner label="Loading Page..." size="lg" />}>
                <Routes>
                  <Route path="/" element={<HomePage />} />
                  <Route path="/dashboard" element={<DashboardPage />} />
                  <Route path="/lobby" element={<LobbyPage />} />
                  <Route path="/interview" element={<SessionPage />} />
                  <Route path="/loading" element={<LoadingScreen />} />
                  <Route path="/result" element={<ResultPage />} />
                  <Route path="/history" element={<HistoryPage />} />
                  <Route path="*" element={<NotFound />} />
                </Routes>
              </Suspense>
            </MainLayout>
          </Router>
        </InterviewProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;
