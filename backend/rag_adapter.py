"""Penghubung ke modul ``rag`` milik Orang 2.

Backend hanya butuh dua fungsi: ``ask(question, chat_history)`` dan ``ingest(path)``.
Kalau modul rag belum siap (atau dependensinya belum terpasang), mode "auto"
jatuh ke stub berisi jawaban hardcode, jadi backend & frontend tetap bisa jalan.
"""

from __future__ import annotations

import logging
import os

log = logging.getLogger("sopgpt.rag")


class StubRag:
    name = "stub"

    def ask(self, question: str, chat_history: list | None = None) -> dict:
        return {
            "answer": (
                "[STUB] Ini jawaban contoh. Modul RAG belum terhubung. "
                f"Pertanyaan Anda: {question}"
            ),
            "sources": [
                {"doc": "SOP_LOTO_v1.pdf", "page": 3, "snippet": "Contoh potongan teks sumber..."}
            ],
        }

    def ingest(self, file_path: str) -> dict:
        return {"status": "success", "doc_name": os.path.basename(file_path), "total_chunks": 0}

    def delete_document(self, doc_name: str) -> bool:
        return True


class RealRag:
    name = "real"

    def __init__(self):
        import rag  # noqa: WPS433 (import lazy, bisa gagal bila dependensi belum ada)

        self._rag = rag

    def ask(self, question: str, chat_history: list | None = None) -> dict:
        return self._rag.ask(question, chat_history=chat_history)

    def ingest(self, file_path: str) -> dict:
        return self._rag.ingest(file_path)

    def delete_document(self, doc_name: str) -> bool:
        """Hapus vektor dokumen. Butuh ``rag.delete_document`` dari Orang 2 (belum ada)."""
        fn = getattr(self._rag, "delete_document", None)
        if fn is None:
            return False
        fn(doc_name)
        return True


def build_rag(mode: str):
    if mode == "stub":
        return StubRag()
    try:
        return RealRag()
    except Exception as exc:  # noqa: BLE001
        if mode == "real":
            raise
        log.warning("Modul rag tidak bisa dimuat (%s). Memakai STUB.", exc)
        return StubRag()
