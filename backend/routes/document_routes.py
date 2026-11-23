from __future__ import annotations

import os

from flask import Blueprint, current_app, g, jsonify, request
from werkzeug.utils import secure_filename

from backend.auth import error, require_auth
from backend.db import get_db, new_id, now
from backend.utils import iso

bp = Blueprint("documents", __name__, url_prefix="/api")


def _public(d: dict) -> dict:
    return {
        "id": d["_id"],
        "name": d["name"],
        "size_bytes": d.get("size_bytes", 0),
        "total_chunks": d.get("total_chunks", 0),
        "uploaded_by": d.get("uploaded_by_name"),
        "created_at": iso(d["created_at"]),
    }


@bp.get("/documents")
@require_auth()
def list_documents():
    docs = get_db().documents.find({}).sort("created_at", -1)
    return jsonify({"documents": [_public(d) for d in docs]})


@bp.post("/documents")
@require_auth("admin")
def upload_document():
    f = request.files.get("file")
    if f is None or not f.filename:
        return error("Sertakan file PDF pada field 'file' (multipart/form-data).", 400)
    name = secure_filename(f.filename)
    if not name.lower().endswith(".pdf"):
        return error("Hanya file PDF yang diperbolehkan.", 400)
    head = f.stream.read(5)
    f.stream.seek(0)
    if head != b"%PDF-":
        return error("File bukan PDF yang valid.", 400)

    upload_dir = current_app.config["UPLOAD_DIR"]
    os.makedirs(upload_dir, exist_ok=True)
    path = os.path.join(upload_dir, name)
    f.save(path)

    try:
        result = current_app.extensions["rag"].ingest(path)
    except Exception as exc:  # noqa: BLE001
        current_app.logger.exception("RAG ingest gagal")
        os.remove(path)
        return error(f"Ingest gagal: {exc}", 502)
    if result.get("status") != "success":
        os.remove(path)
        return error(result.get("message", "Ingest gagal."), 422)

    db = get_db()
    existing = db.documents.find_one({"name": name})
    fields = {
        "path": path,
        "size_bytes": os.path.getsize(path),
        "total_chunks": result.get("total_chunks", 0),
        "uploaded_by": g.user["_id"],
        "uploaded_by_name": g.user["username"],
        "created_at": now(),
    }
    if existing:  # unggah ulang nama yang sama = ganti versi (rag menimpa chunk lama)
        db.documents.update_one({"_id": existing["_id"]}, {"$set": fields})
        doc = {**existing, **fields}
        status = 200
    else:
        doc = {"_id": new_id(), "name": name, **fields}
        db.documents.insert_one(doc)
        status = 201
    return jsonify(_public(doc)), status


@bp.delete("/documents/<doc_id>")
@require_auth("admin")
def delete_document(doc_id):
    db = get_db()
    doc = db.documents.find_one({"_id": doc_id})
    if doc is None:
        return error("Dokumen tidak ditemukan.", 404)
    vectors_removed = current_app.extensions["rag"].delete_document(doc["name"])
    path = doc.get("path")
    if path and os.path.isfile(path):
        os.remove(path)
    db.documents.delete_one({"_id": doc_id})
    return jsonify({"deleted": doc["name"], "vectors_removed": bool(vectors_removed)})
