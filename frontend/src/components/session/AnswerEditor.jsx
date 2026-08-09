import React, { useState } from 'react';
import { Send, Code, Sparkles, Mic, MicOff } from 'lucide-react';

export const AnswerEditor = ({ value, onChange, onSubmit, loading, disabled }) => {
  const [isListening, setIsListening] = useState(false);

  const toggleListening = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert('Speech recognition is not supported in this browser. Try Chrome or Edge.');
      return;
    }

    if (isListening) {
      setIsListening(false);
      return;
    }

    try {
      const recognition = new SpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = 'en-US';

      recognition.onstart = () => setIsListening(true);
      recognition.onend = () => setIsListening(false);

      recognition.onresult = (event) => {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          transcript += event.results[i][0].transcript;
        }
        if (transcript) {
          onChange(value ? `${value} ${transcript}` : transcript);
        }
      };

      recognition.start();
    } catch (err) {
      console.error('Speech recognition error:', err);
      setIsListening(false);
    }
  };

  return (
    <div className="glass-panel rounded-2xl p-6 border border-slate-700/50 flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 text-xs font-semibold text-slate-300">
          <Code className="w-4 h-4 text-blue-400" />
          <span>Technical Answer Workspace</span>
        </div>
        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={toggleListening}
            disabled={disabled || loading}
            className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-semibold border transition-all ${
              isListening
                ? 'bg-rose-500/20 text-rose-300 border-rose-500/40 animate-pulse'
                : 'bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-700'
            }`}
          >
            {isListening ? (
              <>
                <MicOff className="w-3.5 h-3.5 text-rose-400" />
                <span>Listening...</span>
              </>
            ) : (
              <>
                <Mic className="w-3.5 h-3.5 text-blue-400" />
                <span>Voice Input</span>
              </>
            )}
          </button>
          <span className="text-xs text-slate-500 font-mono">
            {value.length} characters
          </span>
        </div>
      </div>

      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled || loading}
        placeholder="Type your response here or click 'Voice Input' to dictate... (e.g., Explain architectural design decisions, framework APIs, error handling, and performance considerations)"
        rows={6}
        className="w-full bg-slate-900/80 border border-slate-700/60 rounded-xl p-4 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-blue-500/80 focus:ring-1 focus:ring-blue-500/80 transition-all font-mono resize-y"
      />

      <div className="flex items-center justify-between pt-2">
        <p className="text-xs text-slate-500 hidden sm:block">
          Press <kbd className="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">Submit Answer</kbd> when ready.
        </p>

        <button
          onClick={onSubmit}
          disabled={disabled || loading || !value.trim()}
          className={`flex items-center gap-2.5 px-6 py-3 rounded-xl font-semibold text-sm transition-all shadow-lg ${
            disabled || loading || !value.trim()
              ? 'bg-slate-800 text-slate-500 border border-slate-700/50 cursor-not-allowed'
              : 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white shadow-blue-500/20 active:scale-95'
          }`}
        >
          {loading ? (
            <>
              <Sparkles className="w-4 h-4 animate-spin text-blue-300" />
              <span>Evaluating Answer...</span>
            </>
          ) : (
            <>
              <span>Submit Answer</span>
              <Send className="w-4 h-4" />
            </>
          )}
        </button>
      </div>
    </div>
  );
};
