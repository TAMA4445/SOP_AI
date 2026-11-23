from __future__ import annotations

import re
from collections import Counter
from datetime import timedelta

from flask import Blueprint, jsonify

from backend.auth import require_auth
from backend.db import get_db, now

bp = Blueprint("stats", __name__, url_prefix="/api")


def _norm(q: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", "", q.lower())).strip()


@bp.get("/stats")
@require_auth("admin")
def stats():
    db = get_db()
    turns = list(db.chat_history.find({}))
    top_q: Counter = Counter()
    first_form: dict[str, str] = {}
    top_docs: Counter = Counter()
    per_day: Counter = Counter()
    for t in turns:
        key = _norm(t["question"])
        top_q[key] += 1
        first_form.setdefault(key, t["question"])
        for doc in {s["doc"] for s in t.get("sources", []) if s.get("doc")}:
            top_docs[doc] += 1
        per_day[t["created_at"].date().isoformat()] += 1

    today = now().date()
    days = [(today - timedelta(days=i)).isoformat() for i in range(6, -1, -1)]
    fb = list(db.feedback.find({}))
    return jsonify(
        {
            "totals": {
                "users": db.users.count_documents({}),
                "documents": db.documents.count_documents({}),
                "questions": len(turns),
                "feedback_up": sum(1 for f in fb if f["rating"] == "up"),
                "feedback_down": sum(1 for f in fb if f["rating"] == "down"),
            },
            "top_questions": [
                {"question": first_form[k], "count": c} for k, c in top_q.most_common(10)
            ],
            "top_documents": [{"doc": d, "count": c} for d, c in top_docs.most_common(10)],
            "questions_per_day": [{"date": d, "count": per_day.get(d, 0)} for d in days],
        }
    )
