import React, { useState, useRef, useEffect } from 'react';
import { Send, Menu, ShieldCheck, Loader2, Sparkles, HelpCircle } from 'lucide-react';
import ChatMessage from './ChatMessage';

const SUGGESTIONS = [
  'Bagaimana prosedur sistem kunci kelompok (Group Lockout)?',
  'Apa saja APD yang wajib digunakan saat menangani bahan kimia berbahaya?',
  'Bagaimana langkah darurat saat alarm kebakaran berbunyi di bengkel?',
  'Siapa yang berwenang memasang gembok LOTO pada mesin produksi?',
];

export default function ChatArea({
  messages,
  onSendMessage,
  loading,
  isDummyMode,
  onToggleSidebar,
}) {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;
    onSendMessage(input.trim());
    setInput('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <main className="flex-1 flex flex-col h-screen bg-slate-900 overflow-hidden font-sans">
      {/* Header Bar */}
      <header className="h-14 border-b border-slate-800 bg-slate-950/80 backdrop-blur-sm flex items-center justify-between px-4 z-10">
        <div className="flex items-center gap-3">
          <button
            onClick={onToggleSidebar}
            className="md:hidden p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800"
          >
            <Menu size={20} />
          </button>
          <div className="flex items-center gap-2.5">
            <span className="font-semibold text-sm text-slate-100 tracking-tight">
              Konsultasi Prosedur SOP & K3
            </span>
            <span className="hidden sm:inline-flex items-center gap-1 text-[11px] text-amber-300 bg-amber-950/40 border border-amber-800/50 px-2 py-0.5 rounded font-medium">
              <ShieldCheck size={13} />
              Basis Dokumen Resmi
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {isDummyMode ? (
            <span className="text-[11px] text-slate-300 bg-slate-800 border border-slate-700 px-2.5 py-1 rounded font-medium flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-amber-400" />
              Mode Demo
            </span>
          ) : (
            <span className="text-[11px] text-emerald-300 bg-emerald-950/50 border border-emerald-800/60 px-2.5 py-1 rounded font-medium flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
              Server API Terhubung
            </span>
          )}
        </div>
      </header>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center max-w-xl mx-auto py-10">
            <div className="w-12 h-12 rounded-xl bg-slate-800 border border-slate-700 text-amber-400 flex items-center justify-center mb-3.5 shadow-sm">
              <ShieldCheck size={26} strokeWidth={2.2} />
            </div>
            <h2 className="text-xl font-bold text-white mb-1.5 tracking-tight">Portal Asisten SOP-AI</h2>
            <p className="text-xs text-slate-400 leading-relaxed mb-6 max-w-md">
              Sistem tanya-jawab cerdas berbasis dokumen Prosedur Operasional Standar (SOP) dan manual keselamatan kerja resmi. Jawaban dilengkapi referensi dokumen dan nomor halaman.
            </p>

            <div className="w-full text-left">
              <div className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider mb-2.5 text-center">
                Topik Pertanyaan yang Sering Diajukan:
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {SUGGESTIONS.map((text, i) => (
                  <button
                    key={i}
                    onClick={() => onSendMessage(text)}
                    className="p-3 rounded-lg bg-slate-950 border border-slate-800 hover:border-slate-700 text-left text-xs text-slate-300 hover:text-white transition-colors cursor-pointer shadow-xs"
                  >
                    "{text}"
                  </button>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div className="max-w-3xl mx-auto">
            {messages.map((msg, index) => (
              <ChatMessage key={index} message={msg} />
            ))}

            {loading && (
              <div className="flex items-center gap-2 text-xs text-slate-400 my-4 p-3 bg-slate-950 rounded-lg border border-slate-800 w-fit">
                <Loader2 size={15} className="animate-spin text-amber-400" />
                <span>Memindai dokumen SOP dan menyusun jawaban...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input Box Footer */}
      <footer className="border-t border-slate-800 bg-slate-950/80 p-3 sm:p-4 backdrop-blur-sm">
        <div className="max-w-3xl mx-auto">
          <form onSubmit={handleSubmit} className="relative flex items-center gap-2">
            <textarea
              rows={1}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Tanyakan prosedur SOP, bahaya kerja, atau instruksi K3..."
              className="w-full resize-none bg-slate-900 border border-slate-700 rounded-lg py-2.5 pl-3.5 pr-12 text-sm text-slate-100 placeholder-slate-400 focus:outline-hidden focus:border-amber-500 focus:ring-1 focus:ring-amber-500 transition-colors max-h-32"
            />
            <button
              type="submit"
              disabled={!input.trim() || loading}
              className="absolute right-2 top-1/2 -translate-y-1/2 p-2 rounded-md bg-amber-500 hover:bg-amber-400 disabled:bg-slate-800 disabled:text-slate-400 text-slate-950 transition-colors cursor-pointer shadow-xs disabled:cursor-not-allowed"
            >
              <Send size={15} />
            </button>
          </form>

          <p className="text-[11px] text-center text-slate-400 mt-2">
            Tekan <kbd className="bg-slate-800 px-1 py-0.5 rounded text-[10px] text-slate-300">Enter</kbd> untuk mengirim • <kbd className="bg-slate-800 px-1 py-0.5 rounded text-[10px] text-slate-300">Shift+Enter</kbd> untuk baris baru.
          </p>
        </div>
      </footer>
    </main>
  );
}
