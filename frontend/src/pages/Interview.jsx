import React from 'react';
import { Mic, Video, Send, Info, UserCheck, MessageSquare } from 'lucide-react';

export const Interview = () => {
  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 glass-card p-6 rounded-2xl border border-slate-800">
        <div>
          <span className="text-xs font-semibold uppercase tracking-wider text-emerald-400">
            Session Workspace
          </span>
          <h1 className="text-2xl font-bold text-white">AI Interview Interface</h1>
          <p className="text-sm text-slate-400">
            Interactive candidate session view (Placeholder interface ready for business logic integration).
          </p>
        </div>

        <div className="flex items-center space-x-3 bg-slate-900/90 px-4 py-2 rounded-xl border border-slate-800">
          <div className="w-2.5 h-2.5 rounded-full bg-amber-400 animate-pulse"></div>
          <span className="text-xs font-medium text-slate-300">Foundation Mode</span>
        </div>
      </div>

      {/* Main Workspace Layout Mock */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left Column: AI Agent Video/Audio Avatar Mock */}
        <div className="lg:col-span-2 space-y-4">
          <div className="glass-card rounded-2xl p-6 h-96 flex flex-col items-center justify-center relative overflow-hidden border border-slate-800">
            <div className="w-24 h-24 rounded-full bg-gradient-to-tr from-brand-600 to-emerald-400 flex items-center justify-center shadow-2xl shadow-emerald-500/20 mb-4">
              <UserCheck className="w-12 h-12 text-slate-950" />
            </div>
            <h3 className="text-lg font-bold text-white">AI Interviewer Avatar</h3>
            <p className="text-xs text-slate-400 mt-1">Awaiting interview session start...</p>

            {/* Media controls placeholder */}
            <div className="absolute bottom-4 flex items-center space-x-3 bg-slate-900/80 px-4 py-2 rounded-full border border-slate-800">
              <button className="p-2 rounded-full bg-slate-800 hover:bg-slate-700 text-slate-300">
                <Mic className="w-4 h-4" />
              </button>
              <button className="p-2 rounded-full bg-slate-800 hover:bg-slate-700 text-slate-300">
                <Video className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Response Input Box Placeholder */}
          <div className="glass-card p-4 rounded-2xl flex items-center space-x-3 border border-slate-800">
            <input
              type="text"
              disabled
              placeholder="Interview responses will be transmitted here once active..."
              className="flex-1 bg-slate-950/60 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-400 cursor-not-allowed"
            />
            <button
              disabled
              className="p-2.5 rounded-xl bg-slate-800 text-slate-500 cursor-not-allowed"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Right Column: Live Transcript & Details Sidebar */}
        <div className="space-y-4">
          <div className="glass-card rounded-2xl p-6 space-y-4 border border-slate-800">
            <div className="flex items-center space-x-2 text-emerald-400">
              <MessageSquare className="w-5 h-5" />
              <h3 className="font-bold text-white">Session Transcript</h3>
            </div>
            
            <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 text-xs text-slate-400 space-y-2">
              <div className="flex items-center space-x-1.5 text-slate-500 font-medium">
                <Info className="w-3.5 h-3.5 text-emerald-400" />
                <span>System Notice</span>
              </div>
              <p>
                No interview logic or LLM calls are connected in this foundational phase.
              </p>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};

export default Interview;
