import React, { useState } from 'react';
import { User, Bot, ThumbsUp, ThumbsDown, Check, Copy } from 'lucide-react';
import SourceBadge from './SourceBadge';
import { api } from '../services/api';

export default function ChatMessage({ message, onFeedback }) {
  const isUser = message.role === 'user';
  const [feedback, setFeedback] = useState(message.feedback || null);
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(message.text || message.answer || '');
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleFeedback = async (rating) => {
    if (feedback === rating) return;
    setFeedback(rating);
    if (message.message_id) {
      await api.sendFeedback(message.message_id, rating);
    }
    if (onFeedback) onFeedback(message.message_id, rating);
  };

  return (
    <div className={`flex gap-3.5 my-4 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {!isUser && (
        <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center flex-shrink-0 text-white shadow-md shadow-blue-500/20">
          <Bot size={18} />
        </div>
      )}

      <div
        className={`max-w-[85%] sm:max-w-[75%] rounded-2xl px-4 py-3 shadow-sm ${
          isUser
            ? 'bg-blue-600 text-white rounded-tr-xs'
            : 'bg-slate-800/90 text-slate-100 border border-slate-700/70 rounded-tl-xs backdrop-blur-xs'
        }`}
      >
        {/* Nama / Role */}
        <div className="flex items-center justify-between text-xs font-semibold mb-1 opacity-70">
          <span>{isUser ? 'Anda' : 'SOP-GPT Assistant'}</span>
          {message.timestamp && <span className="font-normal text-[11px]">{message.timestamp}</span>}
        </div>

        {/* Isi Pesan */}
        <div className="text-sm leading-relaxed whitespace-pre-wrap break-words">
          {message.text || message.answer}
        </div>

        {/* Sumber SOP (Jika ada dari RAG) */}
        {!isUser && message.sources && message.sources.length > 0 && (
          <SourceBadge sources={message.sources} />
        )}

        {/* Tombol aksi (Copy & Feedback) untuk jawaban bot */}
        {!isUser && (
          <div className="flex items-center gap-3 mt-3 pt-2 border-t border-slate-700/40 text-slate-400 text-xs">
            <button
              onClick={handleCopy}
              className="flex items-center gap-1 hover:text-slate-200 transition-colors"
              title="Salin teks"
            >
              {copied ? <Check size={14} className="text-emerald-400" /> : <Copy size={14} />}
              <span>{copied ? 'Tersalin' : 'Salin'}</span>
            </button>

            <div className="flex items-center gap-1.5 ml-auto">
              <button
                onClick={() => handleFeedback('up')}
                className={`p-1 rounded hover:bg-slate-700/60 transition-colors ${
                  feedback === 'up' ? 'text-emerald-400 bg-emerald-950/60' : 'hover:text-slate-200'
                }`}
                title="Jawaban membantu"
              >
                <ThumbsUp size={14} />
              </button>
              <button
                onClick={() => handleFeedback('down')}
                className={`p-1 rounded hover:bg-slate-700/60 transition-colors ${
                  feedback === 'down' ? 'text-rose-400 bg-rose-950/60' : 'hover:text-slate-200'
                }`}
                title="Jawaban kurang tepat"
              >
                <ThumbsDown size={14} />
              </button>
            </div>
          </div>
        )}
      </div>

      {isUser && (
        <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center flex-shrink-0 text-slate-200 shadow-sm">
          <User size={18} />
        </div>
      )}
    </div>
  );
}
