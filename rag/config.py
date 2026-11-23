"""
Konfigurasi terpusat untuk modul RAG SOP-GPT.
Semua parameter dibaca dari file .env (jika ada) lalu dari environment variable.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Muat .env dari root proyek (satu level di atas folder rag/)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_PROJECT_ROOT / ".env")

# ── API Key ──────────────────────────────────────────────────────────────────
GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")

# ── ChromaDB ─────────────────────────────────────────────────────────────────
CHROMA_DIR: str = str(_PROJECT_ROOT / "chroma_db")

# ── Chunking ─────────────────────────────────────────────────────────────────
CHUNK_SIZE: int = 900
CHUNK_OVERLAP: int = 150

# ── Retrieval ────────────────────────────────────────────────────────────────
TOP_K: int = 4

# ── Model ────────────────────────────────────────────────────────────────────
EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "models/gemini-embedding-001")
LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-3.5-flash-lite")

