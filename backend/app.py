"""Entry point backend SOP-GPT.

Jalankan dari root proyek:
    flask --app "backend.app:create_app" run --port 5000
atau:
    python -m backend.app
"""

from __future__ import annotations

import logging

from flask import Flask, jsonify, request

from backend.config import DEV_SECRET, load_config
from backend.db import init_db, seed_demo_users
from backend.openapi import docs_bp
from backend.rag_adapter import build_rag
from backend.routes import auth_routes, chat_routes, document_routes, feedback_routes, stats_routes

log = logging.getLogger("sopgpt")


def create_app(config: dict | None = None, db=None, rag=None) -> Flask:
    app = Flask(__name__)
    cfg = load_config()
    cfg.update(config or {})
    app.config.update(cfg)
    app.config["MAX_CONTENT_LENGTH"] = cfg["MAX_UPLOAD_MB"] * 1024 * 1024
    app.json.ensure_ascii = False

    if cfg["JWT_SECRET"] == DEV_SECRET:
        log.warning("JWT_SECRET belum diset di .env, memakai secret dev. JANGAN dipakai di produksi.")

    app.extensions["db"] = db if db is not None else init_db(cfg)
    app.extensions["rag"] = rag if rag is not None else build_rag(cfg["RAG_MODE"])

    if cfg["SEED_DEMO_USERS"]:
        created = seed_demo_users(app.extensions["db"])
        if created:
            log.info("Akun demo dibuat: %s", ", ".join(created))

    for bp in (auth_routes.bp, chat_routes.bp, document_routes.bp, feedback_routes.bp, stats_routes.bp, docs_bp):
        app.register_blueprint(bp)

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok", "rag_mode": app.extensions["rag"].name})

    @app.after_request
    def cors(resp):
        origin = request.headers.get("Origin")
        allowed = app.config["CORS_ORIGINS"]
        if origin and ("*" in allowed or origin in allowed):
            resp.headers["Access-Control-Allow-Origin"] = origin
            resp.headers["Vary"] = "Origin"
            resp.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
            resp.headers["Access-Control-Allow-Methods"] = "GET, POST, DELETE, OPTIONS"
        return resp

    @app.errorhandler(404)
    def not_found(_):
        return jsonify({"error": "Endpoint tidak ditemukan."}), 404

    @app.errorhandler(405)
    def method_not_allowed(_):
        return jsonify({"error": "Method tidak diizinkan."}), 405

    @app.errorhandler(413)
    def too_large(_):
        return jsonify({"error": f"Ukuran file melebihi {cfg['MAX_UPLOAD_MB']} MB."}), 413

    @app.errorhandler(500)
    def server_error(_):
        return jsonify({"error": "Terjadi kesalahan pada server."}), 500

    return app


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    create_app().run(host="0.0.0.0", port=5000, debug=False)
