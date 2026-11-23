import React from 'react';
import {
  MessageSquarePlus,
  MessageSquare,
  ShieldCheck,
  LogOut,
  User,
  Sliders,
  CheckCircle2,
  Building2
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
        className={`fixed md:static inset-y-0 left-0 z-30 w-72 bg-slate-950 border-r border-slate-800 flex flex-col transition-transform duration-200 ease-in-out font-sans ${
          isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
        }`}
      >
        {/* Header Logo */}
        <div className="p-4 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-lg bg-slate-900 border border-slate-700 flex items-center justify-center text-amber-400 shadow-sm">
              <ShieldCheck size={20} strokeWidth={2.2} />
            </div>
            <div>
              <h1 className="font-bold text-base tracking-tight text-white flex items-center gap-1.5">
                SOP-AI
                <span className="text-[10px] bg-slate-800 text-amber-400 font-semibold px-1.5 py-0.2 rounded border border-slate-700">
                  K3
                </span>
              </h1>
              <p className="text-[11px] text-slate-400">Portal Prosedur Pabrik</p>
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
            className="w-full flex items-center justify-center gap-2 py-2 px-4 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-100 font-medium text-xs transition-colors border border-slate-700 cursor-pointer active:scale-[0.99]"
          >
            <MessageSquarePlus size={16} className="text-amber-400" />
            <span>Sesi Baru</span>
          </button>
        </div>

        {/* Riwayat Sesi Percakapan */}
        <div className="flex-1 overflow-y-auto px-3 py-2 space-y-1">
          <div className="px-2 pb-1.5 text-[10px] font-semibold text-slate-400 uppercase tracking-wider">
            Riwayat Percakapan
          </div>

          {sessions.length === 0 ? (
            <div className="px-3 py-6 text-center text-xs text-slate-400">
              Belum ada riwayat. Ajukan pertanyaan seputar SOP atau K3.
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
                  className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs text-left transition-colors group cursor-pointer ${
                    isActive
                      ? 'bg-slate-800/90 text-white font-medium border border-slate-700'
                      : 'text-slate-400 hover:bg-slate-900 hover:text-slate-200'
                  }`}
                >
                  <MessageSquare
                    size={14}
                    className={`flex-shrink-0 ${isActive ? 'text-amber-400' : 'text-slate-400'}`}
                  />
                  <span className="truncate flex-1">{sess.title || 'Sesi Percakapan'}</span>
                </button>
              );
            })
          )}
        </div>

        {/* Switcher Mode Data */}
        <div className="p-3 border-t border-slate-800 bg-slate-900/40">
          <div className="flex items-center justify-between text-xs text-slate-400 mb-1.5">
            <span className="flex items-center gap-1.5 font-medium text-[11px]">
              <Sliders size={12} /> Status Mode
            </span>
            <button
              onClick={onToggleDummy}
              className={`text-[10px] px-2 py-0.5 rounded font-medium transition-colors ${
                isDummyMode
                  ? 'bg-amber-950/70 text-amber-300 border border-amber-800/60'
                  : 'bg-emerald-950/70 text-emerald-300 border border-emerald-800/60'
              }`}
            >
              {isDummyMode ? 'Mode Demo' : 'Backend Aktif'}
            </button>
          </div>
          <p className="text-[10px] text-slate-400 leading-tight">
            {isDummyMode
              ? 'Menampilkan data simulasi lokal untuk pengujian antarmuka.'
              : 'Terhubung langsung ke API Flask port 5000.'}
          </p>
        </div>

        {/* User Profile & Logout */}
        <div className="p-3 border-t border-slate-800 flex items-center justify-between bg-slate-900/80">
          <div className="flex items-center gap-2.5 min-w-0">
            <div className="w-8 h-8 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-300 flex-shrink-0">
              <User size={15} />
            </div>
            <div className="min-w-0">
              <div className="text-xs font-semibold text-slate-200 truncate">
                {currentUser?.full_name || currentUser?.username || 'User'}
              </div>
              <div className="text-[10px] text-slate-400 capitalize">
                Role: <span className="text-amber-400 font-medium">{currentUser?.role || 'Pengguna'}</span>
              </div>
            </div>
          </div>

          <button
            onClick={onLogout}
            className="p-1.5 text-slate-400 hover:text-red-400 hover:bg-slate-800 rounded-lg transition-colors cursor-pointer"
            title="Keluar"
          >
            <LogOut size={15} />
          </button>
        </div>
      </aside>
    </>
  );
}
