from __future__ import annotations

import uuid

from flask import Blueprint, current_app, g, jsonify, request

from backend.auth import error, require_auth
from backend.db import get_db, new_id, now
from backend.utils import iso

bp = Blueprint("chat", __name__, url_prefix="/api")

MAX_QUESTION = 2000
MAX_SESSION_ID = 100


@bp.post("/chat")
@require_auth()
def chat():
    data = request.get_json(silent=True) or {}
    question = str(data.get("question", "")).strip()
    session_id = str(data.get("session_id") or "").strip() or uuid.uuid4().hex
    if not question:
        return error("Pertanyaan tidak boleh kosong.", 400)
    if len(question) > MAX_QUESTION:
        return error(f"Pertanyaan maksimal {MAX_QUESTION} karakter.", 400)
    if len(session_id) > MAX_SESSION_ID:
        return error("session_id terlalu panjang.", 400)

    db = get_db()
    n = current_app.config["CHAT_HISTORY_TURNS"]
    prev = list(
        db.chat_history.find({"user_id": g.user["_id"], "session_id": session_id})
        .sort("created_at", -1)
        .limit(n)
    )[::-1]
    chat_history = []
    for t in prev:
        chat_history.append({"role": "user", "parts": [t["question"]]})
        chat_history.append({"role": "model", "parts": [t["answer"]]})

    try:
        result = current_app.extensions["rag"].ask(question, chat_history=chat_history)
    except Exception as exc:  # noqa: BLE001
        current_app.logger.exception("RAG ask gagal")
        return error(f"Layanan AI gagal memproses pertanyaan: {exc}", 502)

    answer = str(result.get("answer", ""))
    sources = result.get("sources") or []
    turn = {
        "_id": new_id(),
        "user_id": g.user["_id"],
        "session_id": session_id,
        "question": question,
        "answer": answer,
        "sources": sources,
        "created_at": now(),
    }
    db.chat_history.insert_one(turn)
    return jsonify(
        {"answer": answer, "sources": sources, "session_id": session_id, "message_id": turn["_id"]}
    )


@bp.get("/chat/sessions")
@require_auth()
def sessions():
    turns = get_db().chat_history.find({"user_id": g.user["_id"]}).sort("created_at", 1)
    by_session: dict[str, dict] = {}
    for t in turns:
        s = by_session.setdefault(
            t["session_id"],
            {"session_id": t["session_id"], "title": t["question"][:80], "message_count": 0},
        )
        s["message_count"] += 1
        s["updated_at"] = iso(t["created_at"])
    out = sorted(by_session.values(), key=lambda s: s["updated_at"], reverse=True)
    return jsonify({"sessions": out})


@bp.get("/chat/history")
@require_auth()
def history():
    session_id = request.args.get("session_id", "").strip()
    if not session_id:
        return error("Parameter session_id wajib diisi.", 400)
    db = get_db()
    turns = list(
        db.chat_history.find({"user_id": g.user["_id"], "session_id": session_id}).sort("created_at", 1)
    )
    ratings = {
        f["message_id"]: f["rating"]
        for f in db.feedback.find({"user_id": g.user["_id"]})
    }
    return jsonify(
        {
            "session_id": session_id,
            "messages": [
                {
                    "message_id": t["_id"],
                    "question": t["question"],
                    "answer": t["answer"],
                    "sources": t.get("sources", []),
                    "feedback": ratings.get(t["_id"]),
                    "created_at": iso(t["created_at"]),
                }
                for t in turns
            ],
        }
    )


@bp.delete("/chat/sessions/<session_id>")
@require_auth()
def delete_session(session_id):
    db = get_db()
    turns = list(db.chat_history.find({"user_id": g.user["_id"], "session_id": session_id}))
    if not turns:
        return error("Sesi tidak ditemukan.", 404)
    db.chat_history.delete_many({"user_id": g.user["_id"], "session_id": session_id})
    db.feedback.delete_many({"user_id": g.user["_id"], "message_id": {"$in": [t["_id"] for t in turns]}})
    return jsonify({"deleted": len(turns)})
