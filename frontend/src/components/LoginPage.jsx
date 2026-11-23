import React, { useState } from 'react';
import { ShieldCheck, KeyRound, User, ArrowRight, Sparkles, AlertCircle, Building2 } from 'lucide-react';
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
        setError('Server Backend belum berjalan. Sebagai tim Frontend, kamu bisa langsung masuk via Mode Demo.');
      } else {
        setError(res.error || 'Autentikasi gagal. Periksa kembali username dan password.');
      }
    }
  };

  const handleQuickFill = (u, p) => {
    setUsername(u);
    setPassword(p);
    setError('');
  };

  return (
    <div
      className="min-h-screen w-full flex items-center justify-center p-4 relative bg-cover bg-center bg-no-repeat font-sans"
      style={{ backgroundImage: "url('/login-bg.jpg')" }}
    >
      {/* Dark Corporate Industrial Overlay */}
      <div className="absolute inset-0 bg-slate-950/78 backdrop-blur-[2px]" />

      {/* Decorative subtle corporate grid / vignette */}
      <div className="absolute inset-0 bg-radial from-transparent via-slate-950/40 to-slate-950/90 pointer-events-none" />

      {/* Main Login Card */}
      <div className="w-full max-w-md bg-slate-900/90 border border-slate-700/80 rounded-xl p-7 sm:p-8 shadow-2xl relative z-10 backdrop-blur-md">
        {/* Company / Brand Header */}
        <div className="text-center mb-6">
          <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-slate-800 border border-slate-700 text-amber-400 mb-3.5 shadow-md">
            <ShieldCheck size={26} strokeWidth={2.2} />
          </div>
          <div className="flex items-center justify-center gap-2 mb-1">
            <h1 className="text-2xl font-bold tracking-tight text-white font-sans">
              SOP-AI
            </h1>
            <span className="text-[10px] font-semibold uppercase tracking-wider bg-slate-800 text-amber-400 px-2 py-0.5 rounded border border-slate-700">
              Enterprise
            </span>
          </div>
          <p className="text-xs text-slate-400 font-medium">
            Sistem Prosedur Operasional & Keselamatan Kerja (K3)
          </p>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="mb-4 p-3 rounded-lg bg-red-950/70 border border-red-800/80 text-red-200 text-xs flex flex-col gap-2">
            <div className="flex items-start gap-2">
              <AlertCircle size={15} className="text-red-400 flex-shrink-0 mt-0.5" />
              <span className="leading-relaxed">{error}</span>
            </div>
            {error.includes('Mode Demo') && (
              <button
                type="button"
                onClick={onUseDummy}
                className="w-full py-1.5 px-3 rounded bg-amber-500 hover:bg-amber-400 text-slate-950 font-semibold text-xs transition-colors cursor-pointer text-center"
              >
                Masuk ke Mode Demo Sekarang
              </button>
            )}
          </div>
        )}

        {/* Form Login */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1.5 uppercase tracking-wide">
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
                placeholder="Masukkan username"
                className="w-full pl-9 pr-3 py-2.5 bg-slate-950/80 border border-slate-700 rounded-lg text-sm text-slate-100 placeholder-slate-400 focus:outline-hidden focus:border-amber-500 focus:ring-1 focus:ring-amber-500 transition-colors"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1.5 uppercase tracking-wide">
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
                className="w-full pl-9 pr-3 py-2.5 bg-slate-950/80 border border-slate-700 rounded-lg text-sm text-slate-100 placeholder-slate-400 focus:outline-hidden focus:border-amber-500 focus:ring-1 focus:ring-amber-500 transition-colors"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full mt-2 py-2.5 px-4 rounded-lg bg-amber-500 hover:bg-amber-400 disabled:bg-slate-700 text-slate-950 font-semibold text-sm transition-colors flex items-center justify-center gap-2 cursor-pointer shadow-md disabled:cursor-not-allowed"
          >
            {loading ? (
              <span className="inline-block w-4 h-4 border-2 border-slate-950/30 border-t-slate-950 rounded-full animate-spin" />
            ) : (
              <>
                <span>Masuk ke Portal</span>
                <ArrowRight size={16} />
              </>
            )}
          </button>
        </form>

        {/* Quick Demo Credentials */}
        <div className="mt-5 pt-4 border-t border-slate-800">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-2 text-center">
            Akun Akses Cepat (Testing)
          </div>
          <div className="grid grid-cols-2 gap-2">
            <button
              type="button"
              onClick={() => handleQuickFill('admin', 'admin123')}
              className="py-2 px-3 rounded-lg bg-slate-800/80 hover:bg-slate-800 border border-slate-700 text-xs text-slate-200 text-left transition-colors cursor-pointer"
            >
              <div className="font-semibold text-slate-100">Administrator</div>
              <div className="text-[11px] text-slate-400 font-mono">admin / admin123</div>
            </button>
            <button
              type="button"
              onClick={() => handleQuickFill('teknisi', 'teknisi123')}
              className="py-2 px-3 rounded-lg bg-slate-800/80 hover:bg-slate-800 border border-slate-700 text-xs text-slate-200 text-left transition-colors cursor-pointer"
            >
              <div className="font-semibold text-slate-100">Teknisi Lapangan</div>
              <div className="text-[11px] text-slate-400 font-mono">teknisi / teknisi123</div>
            </button>
          </div>
        </div>

        {/* Demo UI Bypass */}
        <div className="mt-3.5">
          <button
            type="button"
            onClick={onUseDummy}
            className="w-full py-2 px-3 rounded-lg bg-slate-950/70 hover:bg-slate-800 border border-slate-800 hover:border-slate-700 text-xs text-slate-300 transition-colors flex items-center justify-center gap-2 cursor-pointer"
          >
            <Sparkles size={14} className="text-amber-400" />
            <span>Akses Cepat: <strong>Mode Demo (Tanpa Backend)</strong></span>
          </button>
        </div>

        {/* Footer info */}
        <div className="mt-5 text-center">
          <p className="text-[11px] text-slate-400">
            Divisi Keselamatan, Kesehatan Kerja & Lingkungan Hidup (K3L)
          </p>
        </div>
      </div>
    </div>
  );
}
