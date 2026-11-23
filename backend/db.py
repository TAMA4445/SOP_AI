"""Koneksi MongoDB, index, dan seed akun demo.

Koleksi: users, documents, chat_history, feedback.
Semua ``_id`` memakai string uuid4 hex (bukan ObjectId) agar mudah di-JSON-kan.
"""

from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone

from flask import current_app
from werkzeug.security import generate_password_hash


def new_id() -> str:
    return uuid.uuid4().hex


def now() -> datetime:
    return datetime.now(timezone.utc)


def get_db():
    return current_app.extensions["db"]


def init_db(cfg: dict):
    if cfg.get("DB_MODE") == "local":
        from backend.memdb import LocalDB

        return LocalDB(cfg["LOCAL_DB_PATH"])
    from pymongo import MongoClient  # import lazy: hanya dibutuhkan saat jalan sungguhan

    client = MongoClient(cfg["MONGO_URI"], tz_aware=True, serverSelectionTimeoutMS=5000)
    db = client[cfg["MONGO_DB"]]
    ensure_indexes(db)
    return db


def ensure_indexes(db) -> None:
    db.users.create_index("username", unique=True)
    db.documents.create_index("name", unique=True)
    db.chat_history.create_index([("user_id", 1), ("session_id", 1), ("created_at", 1)])
    db.feedback.create_index([("user_id", 1), ("message_id", 1)], unique=True)


def create_user(db, username: str, password: str, role: str, full_name: str = "") -> dict:
    user = {
        "_id": new_id(),
        "username": username,
        "password_hash": generate_password_hash(password),
        "role": role,
        "full_name": full_name or username,
        "created_at": now(),
    }
    db.users.insert_one(user)
    return user


def seed_demo_users(db) -> list[str]:
    """Buat akun demo bila belum ada. Password bisa diubah lewat env."""
    demo = [
        ("admin", os.getenv("DEMO_ADMIN_PASSWORD", "admin123"), "admin", "Administrator"),
        ("teknisi", os.getenv("DEMO_TEKNISI_PASSWORD", "teknisi123"), "teknisi", "Teknisi Demo"),
    ]
    created = []
    for username, password, role, full_name in demo:
        if db.users.find_one({"username": username}) is None:
            create_user(db, username, password, role, full_name)
            created.append(username)
    return created
