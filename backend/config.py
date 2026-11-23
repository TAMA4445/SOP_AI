"""Konfigurasi backend SOP-GPT (dibaca dari .env / environment variable)."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

DEV_SECRET = "dev-secret-ganti-di-produksi"


def _bool(name: str, default: bool) -> bool:
    return os.getenv(name, str(default)).strip().lower() in ("1", "true", "yes", "on")


def load_config() -> dict:
    return {
        # mongo (default) | local = simpan ke file JSON, tanpa MongoDB
        "DB_MODE": os.getenv("DB_MODE", "mongo").lower(),
        "LOCAL_DB_PATH": os.getenv("LOCAL_DB_PATH", str(PROJECT_ROOT / "data" / "local_db.json")),
        "MONGO_URI": os.getenv("MONGO_URI", "mongodb://localhost:27017"),
        "MONGO_DB": os.getenv("MONGO_DB", "sopgpt"),
        "JWT_SECRET": os.getenv("JWT_SECRET", DEV_SECRET),
        "JWT_EXPIRE_HOURS": int(os.getenv("JWT_EXPIRE_HOURS", "8")),
        "UPLOAD_DIR": os.getenv("UPLOAD_DIR", str(PROJECT_ROOT / "data" / "uploads")),
        "MAX_UPLOAD_MB": int(os.getenv("MAX_UPLOAD_MB", "20")),
        # auto = pakai modul rag asli jika bisa di-import, kalau tidak pakai stub
        # stub = selalu jawaban palsu (untuk dev frontend) | real = wajib rag asli
        "RAG_MODE": os.getenv("RAG_MODE", "auto").lower(),
        "CORS_ORIGINS": [
            o.strip()
            for o in os.getenv(
                "CORS_ORIGINS", "http://localhost:5173,http://localhost:3000"
            ).split(",")
            if o.strip()
        ],
        "SEED_DEMO_USERS": _bool("SEED_DEMO_USERS", True),
        "CHAT_HISTORY_TURNS": int(os.getenv("CHAT_HISTORY_TURNS", "6")),
    }
