import React from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

export class ApiErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasApiError: false, errorMessage: '' };
  }

  static getDerivedStateFromError(error) {
    return { hasApiError: true, errorMessage: error.message || 'API Communication Error' };
  }

  componentDidCatch(error, errorInfo) {
    console.error('[ApiErrorBoundary]: Intercepted API error:', error, errorInfo);
  }

  handleRetry = () => {
    this.setState({ hasApiError: false, errorMessage: '' });
    if (this.props.onRetry) {
      this.props.onRetry();
    } else {
      window.location.reload();
    }
  };

  render() {
    if (this.state.hasApiError) {
      return (
        <div className="glass-panel border-rose-500/30 bg-rose-950/20 rounded-2xl p-8 text-center my-6 max-w-lg mx-auto">
          <div className="w-12 h-12 rounded-xl bg-rose-500/10 border border-rose-500/20 flex items-center justify-center text-rose-400 mx-auto mb-3">
            <AlertTriangle className="w-6 h-6" />
          </div>
          <h3 className="text-base font-bold text-slate-100 mb-1">API Communication Failure</h3>
          <p className="text-xs text-slate-400 mb-6">{this.state.errorMessage}</p>
          <button
            onClick={this.handleRetry}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-semibold text-xs transition-all shadow-lg shadow-rose-500/20"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Retry Connection</span>
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
