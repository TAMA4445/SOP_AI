from __future__ import annotations

from flask import Blueprint, g, jsonify, request
from werkzeug.security import check_password_hash

from backend.auth import ROLES, create_token, error, require_auth
from backend.db import create_user, get_db
from backend.utils import public_user

bp = Blueprint("auth", __name__, url_prefix="/api")


@bp.post("/auth/login")
def login():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip()
    password = str(data.get("password", ""))
    user = get_db().users.find_one({"username": username}) if username else None
    if user is None or not check_password_hash(user["password_hash"], password):
        return error("Username atau password salah.", 401)
    return jsonify({"access_token": create_token(user), "token_type": "Bearer", "user": public_user(user)})


@bp.get("/auth/me")
@require_auth()
def me():
    return jsonify(public_user(g.user))


@bp.get("/users")
@require_auth("admin")
def list_users():
    users = get_db().users.find({}).sort("created_at", 1)
    return jsonify({"users": [public_user(u) for u in users]})


@bp.post("/users")
@require_auth("admin")
def add_user():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip()
    password = str(data.get("password", ""))
    role = data.get("role", "teknisi")
    if not (3 <= len(username) <= 50):
        return error("Username harus 3-50 karakter.", 400)
    if len(password) < 6:
        return error("Password minimal 6 karakter.", 400)
    if role not in ROLES:
        return error(f"Role harus salah satu dari: {', '.join(ROLES)}.", 400)
    db = get_db()
    if db.users.find_one({"username": username}):
        return error("Username sudah dipakai.", 409)
    user = create_user(db, username, password, role, str(data.get("full_name", "")).strip())
    return jsonify(public_user(user)), 201
