import React, { useState, useRef, useEffect } from 'react';
import { Send, Menu, Sparkles, AlertCircle, ShieldCheck, Loader2 } from 'lucide-react';
import ChatMessage from './ChatMessage';

const SUGGESTIONS = [
  'Bagaimana prosedur sistem kunci kelompok (Group Lockout)?',
  'Apa saja APD yang wajib digunakan saat menangani bahan kimia?',
  'Bagaimana langkah evakuasi darurat saat terjadi kebakaran?',
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
    <main className="flex-1 flex flex-col h-screen bg-slate-900 overflow-hidden">
      {/* Header Bar */}
      <header className="h-14 border-b border-slate-800 bg-slate-950/60 backdrop-blur-md flex items-center justify-between px-4 z-10">
        <div className="flex items-center gap-3">
          <button
            onClick={onToggleSidebar}
            className="md:hidden p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800"
          >
            <Menu size={20} />
          </button>
          <div className="flex items-center gap-2">
            <span className="font-semibold text-sm text-slate-100">Ruang Tanya-Jawab SOP K3</span>
            <span className="hidden sm:inline-flex items-center gap-1 text-[11px] text-emerald-400 bg-emerald-950/60 border border-emerald-800/50 px-2 py-0.5 rounded-full font-medium">
              <ShieldCheck size={12} />
              Anti-Halusinasi Aktif
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {isDummyMode ? (
            <span className="text-[11px] text-amber-400 bg-amber-950/50 border border-amber-800/60 px-2.5 py-1 rounded-full font-medium flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse" />
              Mode Dummy (Demo)
            </span>
          ) : (
            <span className="text-[11px] text-emerald-400 bg-emerald-950/50 border border-emerald-800/60 px-2.5 py-1 rounded-full font-medium flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              API Server Aktif
            </span>
          )}
        </div>
      </header>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center max-w-xl mx-auto py-10">
            <div className="w-16 h-16 rounded-2xl bg-blue-600/10 border border-blue-500/20 text-blue-400 flex items-center justify-center mb-4 shadow-lg shadow-blue-500/10">
              <Sparkles size={28} />
            </div>
            <h2 className="text-xl font-bold text-white mb-2">Selamat Datang di SOP-GPT</h2>
            <p className="text-xs text-slate-400 leading-relaxed mb-6">
              Sistem ini akan mencari jawaban langsung dari dokumen SOP & manual resmi pabrik menggunakan teknologi RAG. Jawaban dilengkapi sitasi nama dokumen dan nomor halaman.
            </p>

            <div className="w-full text-left">
              <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-2.5 text-center">
                Contoh Pertanyaan yang Bisa Anda Coba:
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {SUGGESTIONS.map((text, i) => (
                  <button
                    key={i}
                    onClick={() => onSendMessage(text)}
                    className="p-3 rounded-xl bg-slate-950/80 hover:bg-slate-800/80 border border-slate-800 hover:border-slate-700 text-left text-xs text-slate-300 hover:text-white transition-all cursor-pointer shadow-sm active:scale-[0.99]"
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
              <div className="flex items-center gap-2 text-xs text-slate-400 my-4 p-3 bg-slate-950/50 rounded-xl border border-slate-800/80 w-fit">
                <Loader2 size={16} className="animate-spin text-blue-400" />
                <span>Mencari dokumen SOP terkait & merumuskan jawaban...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input Box Footer */}
      <footer className="border-t border-slate-800 bg-slate-950/80 p-3 sm:p-4 backdrop-blur-md">
        <div className="max-w-3xl mx-auto">
          <form onSubmit={handleSubmit} className="relative flex items-center gap-2">
            <textarea
              rows={1}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ketik pertanyaan terkait SOP K3 atau manual mesin..."
              className="w-full resize-none bg-slate-900 border border-slate-700/80 rounded-2xl py-3 pl-4 pr-12 text-sm text-slate-100 placeholder-slate-400 focus:outline-hidden focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all max-h-32"
            />
            <button
              type="submit"
              disabled={!input.trim() || loading}
              className="absolute right-2.5 top-1/2 -translate-y-1/2 p-2 rounded-xl bg-blue-600 hover:bg-blue-500 disabled:bg-slate-800 disabled:text-slate-400 text-white transition-all cursor-pointer shadow-md disabled:cursor-not-allowed"
            >
              <Send size={16} />
            </button>
          </form>

          <p className="text-[11px] text-center text-slate-400 mt-2">
            Tekan <kbd className="bg-slate-800 px-1 py-0.5 rounded text-[10px]">Enter</kbd> untuk mengirim, <kbd className="bg-slate-800 px-1 py-0.5 rounded text-[10px]">Shift+Enter</kbd> untuk baris baru.
          </p>
        </div>
      </footer>
    </main>
  );
}

