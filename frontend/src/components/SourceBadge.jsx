import React, { useState } from 'react';
import { FileText, ChevronDown, ChevronUp, BookOpen } from 'lucide-react';

export default function SourceBadge({ sources }) {
  const [isOpen, setIsOpen] = useState(false);

  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-3 pt-3 border-t border-slate-700/60">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 text-xs font-medium text-emerald-400 hover:text-emerald-300 transition-colors bg-emerald-950/40 border border-emerald-800/50 px-2.5 py-1.5 rounded-lg"
      >
        <BookOpen size={14} />
        <span>{sources.length} Sumber Referensi SOP Ditemukan</span>
        {isOpen ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
      </button>

      {isOpen && (
        <div className="mt-2.5 space-y-2">
          {sources.map((src, idx) => (
            <div
              key={idx}
              className="p-3 rounded-lg bg-slate-900/90 border border-slate-700/70 text-xs text-slate-300 shadow-sm"
            >
              <div className="flex items-center justify-between mb-1.5 pb-1 border-b border-slate-800">
                <span className="font-semibold text-emerald-300 flex items-center gap-1.5">
                  <FileText size={13} />
                  {src.doc || 'Dokumen SOP'}
                </span>
                {src.page && (
                  <span className="bg-slate-800 text-slate-300 px-2 py-0.5 rounded text-[11px] font-mono">
                    Halaman {src.page}
                  </span>
                )}
              </div>
              <p className="italic text-slate-400 bg-slate-950/50 p-2 rounded border border-slate-800/80 leading-relaxed font-sans">
                "{src.snippet}"
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
