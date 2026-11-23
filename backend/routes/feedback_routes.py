from __future__ import annotations

from flask import Blueprint, g, jsonify, request

from backend.auth import error, require_auth
from backend.db import get_db, new_id, now
from backend.utils import iso

bp = Blueprint("feedback", __name__, url_prefix="/api")


@bp.post("/feedback")
@require_auth()
def submit_feedback():
    data = request.get_json(silent=True) or {}
    message_id = str(data.get("message_id", "")).strip()
    rating = data.get("rating")
    comment = str(data.get("comment", "")).strip()[:1000]
    if rating not in ("up", "down"):
        return error("rating harus 'up' atau 'down'.", 400)
    db = get_db()
    turn = db.chat_history.find_one({"_id": message_id, "user_id": g.user["_id"]})
    if turn is None:
        return error("Pesan tidak ditemukan.", 404)
    db.feedback.update_one(
        {"user_id": g.user["_id"], "message_id": message_id},
        {
            "$set": {"rating": rating, "comment": comment, "updated_at": now()},
            "$setOnInsert": {"_id": new_id(), "created_at": now()},
        },
        upsert=True,
    )
    return jsonify({"message_id": message_id, "rating": rating, "comment": comment})


@bp.get("/feedback")
@require_auth("admin")
def list_feedback():
    rating = request.args.get("rating")
    query = {"rating": rating} if rating in ("up", "down") else {}
    db = get_db()
    items = []
    for f in db.feedback.find(query).sort("updated_at", -1).limit(200):
        turn = db.chat_history.find_one({"_id": f["message_id"]}) or {}
        items.append(
            {
                "message_id": f["message_id"],
                "rating": f["rating"],
                "comment": f.get("comment", ""),
                "question": turn.get("question"),
                "answer": turn.get("answer"),
                "updated_at": iso(f.get("updated_at")),
            }
        )
    return jsonify({"feedback": items})
