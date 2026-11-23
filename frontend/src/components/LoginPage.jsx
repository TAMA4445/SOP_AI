import React, { useState } from 'react';
import { ShieldAlert, KeyRound, User, ArrowRight, Sparkles, CheckCircle2 } from 'lucide-react';
import { api, setStoredToken, setStoredUser } from '../services/api';

export default function LoginPage({ onLoginSuccess, onUseDummy }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!username.trim() || !password.trim()) {
      setError('Mohon isi username dan password');
      return;
    }

    setLoading(true);
    setError('');

    const res = await api.login(username, password);
    setLoading(false);

    if (res.data && res.data.access_token) {
      setStoredToken(res.data.access_token);
      setStoredUser(res.data.user);
      onLoginSuccess(res.data.user, false);
    } else {
      if (res.error?.includes('500') || res.error?.includes('fetch') || res.error?.includes('Failed')) {
        setError('Server Backend (port 5000) belum berjalan. Sebagai tim Frontend, kamu bisa langsung klik tombol "Mode Dummy (Demo UI)" di bawah!');
      } else {
        setError(res.error || 'Login gagal. Periksa username dan password.');
      }
    }
  };

  const handleQuickFill = (u, p) => {
    setUsername(u);
    setPassword(p);
    setError('');
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background Glow effects */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-indigo-600/10 rounded-full blur-3xl pointer-events-none" />

      <div className="w-full max-w-md bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8 shadow-2xl relative z-10">
        {/* Brand */}
        <div className="text-center mb-7">
          <div className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-blue-600 to-indigo-500 mx-auto flex items-center justify-center text-white shadow-xl shadow-blue-500/30 mb-3.5">
            <ShieldAlert size={30} />
          </div>
          <h2 className="text-2xl font-bold text-white tracking-tight">SOP-GPT System</h2>
          <p className="text-xs text-slate-400 mt-1 max-w-xs mx-auto">
            Sistem Tanya-Jawab Prosedur K3 & Manual Mesin Berbasis AI Dokumen
          </p>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="mb-4 p-3 rounded-xl bg-rose-950/60 border border-rose-800/80 text-rose-300 text-xs flex flex-col gap-1.5">
            <div className="flex items-start gap-2">
              <span className="font-bold">⚠️</span>
              <span>{error}</span>
            </div>
            {error.includes('Mode Dummy') && (
              <button
                type="button"
                onClick={onUseDummy}
                className="mt-1 w-full py-2 px-3 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 font-semibold text-xs transition-colors cursor-pointer text-center shadow-sm"
              >
                👉 Langsung Masuk ke Mode Demo Sekarang
              </button>
            )}
          </div>
        )}

        {/* Form Login */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1.5">
              Username
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                <User size={16} />
              </div>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="admin / teknisi"
                className="w-full pl-9 pr-3 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm text-slate-100 placeholder-slate-400 focus:outline-hidden focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1.5">
              Password
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                <KeyRound size={16} />
              </div>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-9 pr-3 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm text-slate-100 placeholder-slate-400 focus:outline-hidden focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full mt-2 py-2.5 px-4 rounded-xl bg-blue-600 hover:bg-blue-500 disabled:bg-blue-800 text-white font-medium text-sm transition-all shadow-lg shadow-blue-600/25 flex items-center justify-center gap-2 cursor-pointer active:scale-[0.98]"
          >
            {loading ? (
              <span className="inline-block w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : (
              <>
                <span>Masuk ke Sistem</span>
                <ArrowRight size={16} />
              </>
            )}
          </button>
        </form>

        {/* Quick Demo Credentials */}
        <div className="mt-6 pt-5 border-t border-slate-800/80">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-2.5 text-center">
            Pilihan Akun Demo (Praktis)
          </div>
          <div className="grid grid-cols-2 gap-2">
            <button
              type="button"
              onClick={() => handleQuickFill('admin', 'admin123')}
              className="py-2 px-3 rounded-lg bg-slate-800/80 hover:bg-slate-800 border border-slate-700/60 text-xs text-slate-200 text-left transition-colors cursor-pointer"
            >
              <div className="font-semibold text-blue-400">Akun Admin</div>
              <div className="text-[11px] text-slate-400">admin / admin123</div>
            </button>
            <button
              type="button"
              onClick={() => handleQuickFill('teknisi', 'teknisi123')}
              className="py-2 px-3 rounded-lg bg-slate-800/80 hover:bg-slate-800 border border-slate-700/60 text-xs text-slate-200 text-left transition-colors cursor-pointer"
            >
              <div className="font-semibold text-emerald-400">Akun Teknisi</div>
              <div className="text-[11px] text-slate-400">teknisi / teknisi123</div>
            </button>
          </div>
        </div>

        {/* Dummy Mode button (Target Minggu 1) */}
        <div className="mt-4">
          <button
            type="button"
            onClick={onUseDummy}
            className="w-full py-2 px-3 rounded-xl bg-slate-950 hover:bg-slate-800/60 border border-slate-800 text-xs text-slate-400 hover:text-slate-200 transition-colors flex items-center justify-center gap-2 cursor-pointer"
          >
            <Sparkles size={14} className="text-amber-400" />
            <span>Masuk Cepat dengan <strong>Mode Dummy (Demo UI)</strong></span>
          </button>
        </div>
      </div>
    </div>
  );
}

