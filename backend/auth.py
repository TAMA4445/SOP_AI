"""JWT + pengecekan role."""

from __future__ import annotations

from datetime import timedelta
from functools import wraps

import jwt
from flask import current_app, g, jsonify, request

from backend.db import get_db, now

ROLES = ("admin", "teknisi")


def error(message: str, status: int):
    return jsonify({"error": message}), status


def create_token(user: dict) -> str:
    cfg = current_app.config
    payload = {
        "sub": user["_id"],
        "username": user["username"],
        "role": user["role"],
        "iat": now(),
        "exp": now() + timedelta(hours=cfg["JWT_EXPIRE_HOURS"]),
    }
    return jwt.encode(payload, cfg["JWT_SECRET"], algorithm="HS256")


def require_auth(*roles: str):
    """Decorator: wajib login. Bila ``roles`` diisi, role user harus termasuk di dalamnya."""

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            header = request.headers.get("Authorization", "")
            if not header.startswith("Bearer "):
                return error("Token tidak ditemukan. Login terlebih dahulu.", 401)
            try:
                payload = jwt.decode(
                    header[7:], current_app.config["JWT_SECRET"], algorithms=["HS256"]
                )
            except jwt.ExpiredSignatureError:
                return error("Token sudah kedaluwarsa. Silakan login ulang.", 401)
            except jwt.InvalidTokenError:
                return error("Token tidak valid.", 401)

            user = get_db().users.find_one({"_id": payload["sub"]})
            if user is None:
                return error("Akun tidak ditemukan.", 401)
            if roles and user["role"] not in roles:
                return error("Anda tidak memiliki akses ke fitur ini.", 403)

            g.user = user
            return fn(*args, **kwargs)

        return wrapper

    return decorator
