from __future__ import annotations

from datetime import datetime


def iso(value):
    return value.isoformat() if isinstance(value, datetime) else value


def public_user(user: dict) -> dict:
    return {
        "id": user["_id"],
        "username": user["username"],
        "role": user["role"],
        "full_name": user.get("full_name", user["username"]),
        "created_at": iso(user.get("created_at")),
    }
