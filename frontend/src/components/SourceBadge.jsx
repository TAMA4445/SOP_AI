import React, { useState } from 'react';
import { FileText, ChevronDown, ChevronUp, BookOpen } from 'lucide-react';

export default function SourceBadge({ sources }) {
  const [isOpen, setIsOpen] = useState(false);

  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-2.5 pt-2.5 border-t border-slate-700/60 font-sans">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-1.5 text-xs font-medium text-amber-300 hover:text-amber-200 transition-colors bg-slate-900 border border-slate-700/80 px-2.5 py-1 rounded-md cursor-pointer"
      >
        <BookOpen size={13} className="text-amber-400" />
        <span>{sources.length} Referensi Dokumen Terlampir</span>
        {isOpen ? <ChevronUp size={13} /> : <ChevronDown size={13} />}
      </button>

      {isOpen && (
        <div className="mt-2 space-y-1.5">
          {sources.map((src, idx) => (
            <div
              key={idx}
              className="p-2.5 rounded-lg bg-slate-950/90 border border-slate-700 text-xs text-slate-300"
            >
              <div className="flex items-center justify-between mb-1 pb-1 border-b border-slate-800">
                <span className="font-semibold text-slate-200 flex items-center gap-1.5">
                  <FileText size={12} className="text-amber-400" />
                  {src.doc || 'Dokumen SOP'}
                </span>
                {src.page && (
                  <span className="bg-slate-800 text-slate-300 px-1.5 py-0.5 rounded text-[10px] font-mono">
                    Halaman {src.page}
                  </span>
                )}
              </div>
              <p className="text-slate-400 bg-slate-900/60 p-2 rounded border border-slate-800 leading-relaxed font-sans text-[11px]">
                "{src.snippet}"
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
