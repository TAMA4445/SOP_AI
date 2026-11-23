import React from 'react';
import {
  MessageSquarePlus,
  MessageSquare,
  ShieldAlert,
  LogOut,
  User,
  Trash2,
  Sliders,
  CheckCircle2,
  AlertCircle
} from 'lucide-react';

export default function Sidebar({
  sessions,
  activeSessionId,
  onSelectSession,
  onNewChat,
  currentUser,
  onLogout,
  isDummyMode,
  onToggleDummy,
  isOpen,
  onClose
}) {
  return (
    <>
      {/* Overlay untuk mobile */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/60 z-20 md:hidden backdrop-blur-xs"
          onClick={onClose}
        />
      )}

      <aside
        className={`fixed md:static inset-y-0 left-0 z-30 w-72 bg-slate-950 border-r border-slate-800 flex flex-col transition-transform duration-200 ease-in-out ${
          isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
        }`}
      >
        {/* Header Logo */}
        <div className="p-4 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center text-white shadow-lg shadow-blue-500/25">
              <ShieldAlert size={20} />
            </div>
            <div>
              <h1 className="font-bold text-base tracking-tight text-white flex items-center gap-1.5">
                SOP-GPT
                <span className="text-[10px] bg-blue-500/20 text-blue-400 font-medium px-1.5 py-0.5 rounded border border-blue-500/30">
                  K3 RAG
                </span>
              </h1>
              <p className="text-[11px] text-slate-400">Asisten Prosedur & K3</p>
            </div>
          </div>
        </div>

        {/* Tombol Chat Baru */}
        <div className="p-3">
          <button
            onClick={() => {
              onNewChat();
              if (onClose) onClose();
            }}
            className="w-full flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-medium text-sm transition-all shadow-md shadow-blue-600/20 cursor-pointer active:scale-[0.98]"
          >
            <MessageSquarePlus size={18} />
            <span>Percakapan Baru</span>
          </button>
        </div>

        {/* Riwayat Sesi Percakapan */}
        <div className="flex-1 overflow-y-auto px-3 py-2 space-y-1">
          <div className="px-2 pb-1 text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Riwayat Sesi
          </div>

          {sessions.length === 0 ? (
            <div className="px-3 py-6 text-center text-xs text-slate-400">
              Belum ada percakapan. Mulai tanya mengenai prosedur SOP K3.
            </div>
          ) : (
            sessions.map((sess) => {
              const isActive = sess.session_id === activeSessionId;
              return (
                <button
                  key={sess.session_id}
                  onClick={() => {
                    onSelectSession(sess.session_id);
                    if (onClose) onClose();
                  }}
                  className={`w-full flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-xs text-left transition-colors group cursor-pointer ${
                    isActive
                      ? 'bg-slate-800 text-white font-medium border border-slate-700/80'
                      : 'text-slate-400 hover:bg-slate-900 hover:text-slate-200'
                  }`}
                >
                  <MessageSquare
                    size={15}
                    className={`flex-shrink-0 ${isActive ? 'text-blue-400' : 'text-slate-400 group-hover:text-slate-400'}`}
                  />
                  <span className="truncate flex-1">{sess.title || 'Sesi Percakapan'}</span>
                </button>
              );
            })
          )}
        </div>

        {/* Mode Backend vs Dummy Switcher */}
        <div className="p-3 border-t border-slate-800/80 bg-slate-950/50">
          <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
            <span className="flex items-center gap-1.5 font-medium">
              <Sliders size={13} /> Sumber Data
            </span>
            <button
              onClick={onToggleDummy}
              className={`text-[11px] px-2 py-0.5 rounded font-medium transition-colors ${
                isDummyMode
                  ? 'bg-amber-950/80 text-amber-300 border border-amber-800/60'
                  : 'bg-emerald-950/80 text-emerald-300 border border-emerald-800/60'
              }`}
            >
              {isDummyMode ? 'Mode Dummy' : 'Backend API'}
            </button>
          </div>
          <p className="text-[10px] text-slate-400 leading-tight">
            {isDummyMode
              ? 'Menggunakan simulasi respons lokal (cocok untuk demo UI tanpa server).'
              : 'Terhubung ke Flask API port 5000 & Google Gemini RAG.'}
          </p>
        </div>

        {/* User Profile & Logout */}
        <div className="p-3 border-t border-slate-800 flex items-center justify-between bg-slate-900/60">
          <div className="flex items-center gap-2.5 min-w-0">
            <div className="w-8 h-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-300 flex-shrink-0">
              <User size={16} />
            </div>
            <div className="min-w-0">
              <div className="text-xs font-semibold text-slate-200 truncate">
                {currentUser?.full_name || currentUser?.username || 'Pengguna'}
              </div>
              <div className="text-[10px] text-slate-400 capitalize">
                Role: <span className="text-blue-400 font-medium">{currentUser?.role || 'User'}</span>
              </div>
            </div>
          </div>

          <button
            onClick={onLogout}
            className="p-1.5 text-slate-400 hover:text-rose-400 hover:bg-slate-800 rounded-lg transition-colors cursor-pointer"
            title="Keluar"
          >
            <LogOut size={16} />
          </button>
        </div>
      </aside>
    </>
  );
}
