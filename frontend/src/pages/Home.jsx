import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Bot, Play, Activity, Server, ShieldCheck, Zap } from 'lucide-react';
import { checkBackendHealth, checkBackendV1Health } from '../services/api';
import Button from '../components/common/Button';
import Card from '../components/common/Card';
import Badge from '../components/ui/Badge';

export const Home = () => {
  const navigate = useNavigate();
  const [healthStatus, setHealthStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleHealthCheck = async () => {
    setLoading(true);
    try {
      const rootData = await checkBackendHealth();
      const v1Data = await checkBackendV1Health();
      setHealthStatus({ root: rootData, v1: v1Data });
    } catch (err) {
      setHealthStatus({ status: 'error', message: 'Backend API unreachable' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-10 py-4">
      {/* Hero Section */}
      <section className="text-center space-y-6 max-w-3xl mx-auto py-8">
        <Badge variant="emerald">
          <Zap className="w-3.5 h-3.5" />
          <span>ABTalks Hackathon Architecture Foundation</span>
        </Badge>

        <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight text-white leading-tight">
          Next-Generation <br className="hidden sm:inline" />
          <span className="bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-400 bg-clip-text text-transparent">
            AI Interview Agent
          </span>
        </h1>

        <p className="text-slate-400 text-base sm:text-lg leading-relaxed">
          Production-ready full-stack boilerplate built with React 19, Vite, Tailwind CSS, and FastAPI backend. Prepared for high-performance AI integration.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-2">
          <Button variant="primary" onClick={() => navigate('/interview')}>
            <Play className="w-5 h-5 fill-slate-950" />
            Launch Interview Session
          </Button>

          <Button variant="secondary" onClick={handleHealthCheck} disabled={loading}>
            <Activity className="w-5 h-5 text-emerald-400" />
            {loading ? 'Checking FastAPI...' : 'Test Backend Health'}
          </Button>
        </div>

        {/* Backend Health Status Display */}
        {healthStatus && (
          <Card className="max-w-md mx-auto text-left space-y-2">
            <div className="flex items-center space-x-2">
              <Server className="w-4 h-4 text-emerald-400" />
              <span className="text-xs font-semibold text-slate-300">FastAPI Health Response:</span>
            </div>
            <pre className="text-xs font-mono bg-slate-950 p-2.5 rounded-lg text-emerald-400 overflow-x-auto">
              {JSON.stringify(healthStatus, null, 2)}
            </pre>
          </Card>
        )}
      </section>

      {/* Feature Cards Grid */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card hover className="space-y-3">
          <div className="w-12 h-12 rounded-xl bg-slate-800/80 flex items-center justify-center text-emerald-400 border border-slate-700">
            <Bot className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-white">Modular Architecture</h3>
          <p className="text-slate-400 text-sm">
            Clean separation of concerns with React Router layouts, API client services, and FastAPI versioned routers.
          </p>
        </Card>

        <Card hover className="space-y-3">
          <div className="w-12 h-12 rounded-xl bg-slate-800/80 flex items-center justify-center text-emerald-400 border border-slate-700">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-white">Production Ready</h3>
          <p className="text-slate-400 text-sm">
            Configured with pytest backend suite, GitHub Actions CI, ESLint, environment tokens, and CORS middleware.
          </p>
        </Card>

        <Card hover className="space-y-3">
          <div className="w-12 h-12 rounded-xl bg-slate-800/80 flex items-center justify-center text-emerald-400 border border-slate-700">
            <Zap className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-white">Vite & React 19</h3>
          <p className="text-slate-400 text-sm">
            Ultra-fast build setup powered by Vite bundler, React 19 functional components, and custom hooks.
          </p>
        </Card>
      </section>
    </div>
  );
};

export default Home;
