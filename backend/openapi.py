"""Spesifikasi OpenAPI + halaman Swagger UI di /docs (spec di /openapi.json)."""

from __future__ import annotations

from flask import Blueprint, jsonify

docs_bp = Blueprint("docs", __name__)

_SEC = [{"bearerAuth": []}]
_ERR = {"description": "Error", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}}}


def _json(schema):
    return {"required": True, "content": {"application/json": {"schema": schema}}}


def _ok(schema, desc="OK"):
    return {"description": desc, "content": {"application/json": {"schema": schema}}}


def _obj(props: dict, required=()):
    return {"type": "object", "properties": props, "required": list(required)}


_S = {"type": "string"}
_I = {"type": "integer"}

SPEC = {
    "openapi": "3.0.3",
    "info": {
        "title": "SOP-GPT Backend API",
        "version": "1.0.0",
        "description": "REST API SOP-GPT. Login dulu di /api/auth/login, lalu klik **Authorize** dan tempel `access_token`.",
    },
    "components": {
        "securitySchemes": {"bearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}},
        "schemas": {
            "Error": _obj({"error": _S}),
            "User": _obj({"id": _S, "username": _S, "role": {"type": "string", "enum": ["admin", "teknisi"]}, "full_name": _S, "created_at": _S}),
            "Source": _obj({"doc": _S, "page": _I, "snippet": _S}),
            "Document": _obj({"id": _S, "name": _S, "size_bytes": _I, "total_chunks": _I, "uploaded_by": _S, "created_at": _S}),
        },
    },
    "paths": {
        "/api/health": {"get": {"tags": ["Sistem"], "summary": "Cek server & mode RAG (real/stub)", "responses": {"200": _ok(_obj({"status": _S, "rag_mode": _S}))}}},
        "/api/auth/login": {
            "post": {
                "tags": ["Auth"], "summary": "Login, dapatkan JWT",
                "requestBody": _json(_obj({"username": _S, "password": _S}, ["username", "password"])),
                "responses": {"200": _ok(_obj({"access_token": _S, "token_type": _S, "user": {"$ref": "#/components/schemas/User"}})), "401": _ERR},
            }
        },
        "/api/auth/me": {"get": {"tags": ["Auth"], "summary": "Profil user saat ini", "security": _SEC, "responses": {"200": _ok({"$ref": "#/components/schemas/User"}), "401": _ERR}}},
        "/api/users": {
            "get": {"tags": ["Auth"], "summary": "Daftar user (admin)", "security": _SEC, "responses": {"200": _ok(_obj({"users": {"type": "array", "items": {"$ref": "#/components/schemas/User"}}})), "403": _ERR}},
            "post": {
                "tags": ["Auth"], "summary": "Buat user baru (admin)", "security": _SEC,
                "requestBody": _json(_obj({"username": _S, "password": _S, "role": {"type": "string", "enum": ["admin", "teknisi"]}, "full_name": _S}, ["username", "password"])),
                "responses": {"201": _ok({"$ref": "#/components/schemas/User"}, "Dibuat"), "400": _ERR, "403": _ERR, "409": _ERR},
            },
        },
        "/api/chat": {
            "post": {
                "tags": ["Chat"], "summary": "Ajukan pertanyaan ke SOP-GPT", "security": _SEC,
                "description": "Jika `session_id` kosong, server membuat yang baru. Riwayat sesi ikut dikirim ke RAG sebagai konteks.",
                "requestBody": _json(_obj({"question": _S, "session_id": _S}, ["question"])),
                "responses": {
                    "200": _ok(_obj({"answer": _S, "sources": {"type": "array", "items": {"$ref": "#/components/schemas/Source"}}, "session_id": _S, "message_id": _S})),
                    "400": _ERR, "401": _ERR, "502": _ERR,
                },
            }
        },
        "/api/chat/sessions": {"get": {"tags": ["Chat"], "summary": "Daftar sesi chat milik saya", "security": _SEC, "responses": {"200": _ok(_obj({"sessions": {"type": "array", "items": _obj({"session_id": _S, "title": _S, "message_count": _I, "updated_at": _S})}}))}}},
        "/api/chat/sessions/{session_id}": {
            "delete": {"tags": ["Chat"], "summary": "Hapus satu sesi", "security": _SEC, "parameters": [{"name": "session_id", "in": "path", "required": True, "schema": _S}], "responses": {"200": _ok(_obj({"deleted": _I})), "404": _ERR}}
        },
        "/api/chat/history": {
            "get": {
                "tags": ["Chat"], "summary": "Riwayat pesan dalam satu sesi", "security": _SEC,
                "parameters": [{"name": "session_id", "in": "query", "required": True, "schema": _S}],
                "responses": {"200": _ok(_obj({"session_id": _S, "messages": {"type": "array", "items": _obj({"message_id": _S, "question": _S, "answer": _S, "sources": {"type": "array", "items": {"$ref": "#/components/schemas/Source"}}, "feedback": {"type": "string", "nullable": True, "enum": ["up", "down"]}, "created_at": _S})}})), "400": _ERR},
            }
        },
        "/api/documents": {
            "get": {"tags": ["Dokumen"], "summary": "Daftar dokumen", "security": _SEC, "responses": {"200": _ok(_obj({"documents": {"type": "array", "items": {"$ref": "#/components/schemas/Document"}}}))}},
            "post": {
                "tags": ["Dokumen"], "summary": "Upload PDF + ingest ke RAG (admin)", "security": _SEC,
                "description": "Nama file yang sama akan menimpa dokumen lama (200), nama baru menghasilkan 201.",
                "requestBody": {"required": True, "content": {"multipart/form-data": {"schema": _obj({"file": {"type": "string", "format": "binary"}}, ["file"])}}},
                "responses": {"201": _ok({"$ref": "#/components/schemas/Document"}, "Dokumen baru"), "200": _ok({"$ref": "#/components/schemas/Document"}, "Dokumen diganti"), "400": _ERR, "403": _ERR, "413": _ERR, "422": _ERR, "502": _ERR},
            },
        },
        "/api/documents/{doc_id}": {
            "delete": {"tags": ["Dokumen"], "summary": "Hapus dokumen (admin)", "security": _SEC, "parameters": [{"name": "doc_id", "in": "path", "required": True, "schema": _S}], "responses": {"200": _ok(_obj({"deleted": _S, "vectors_removed": {"type": "boolean"}})), "404": _ERR}}
        },
        "/api/feedback": {
            "post": {"tags": ["Feedback"], "summary": "Jempol atas/bawah untuk satu jawaban (bisa diubah)", "security": _SEC, "requestBody": _json(_obj({"message_id": _S, "rating": {"type": "string", "enum": ["up", "down"]}, "comment": _S}, ["message_id", "rating"])), "responses": {"200": _ok(_obj({"message_id": _S, "rating": _S, "comment": _S})), "400": _ERR, "404": _ERR}},
            "get": {"tags": ["Feedback"], "summary": "Daftar feedback (admin)", "security": _SEC, "parameters": [{"name": "rating", "in": "query", "schema": {"type": "string", "enum": ["up", "down"]}}], "responses": {"200": _ok(_obj({"feedback": {"type": "array", "items": {"type": "object"}}})), "403": _ERR}},
        },
        "/api/stats": {"get": {"tags": ["Dashboard"], "summary": "Statistik dashboard (admin)", "security": _SEC, "responses": {"200": _ok(_obj({"totals": {"type": "object"}, "top_questions": {"type": "array", "items": _obj({"question": _S, "count": _I})}, "top_documents": {"type": "array", "items": _obj({"doc": _S, "count": _I})}, "questions_per_day": {"type": "array", "items": _obj({"date": _S, "count": _I})}})), "403": _ERR}}},
    },
}

_PAGE = """<!doctype html>
<html lang="id"><head><meta charset="utf-8"><title>SOP-GPT API Docs</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.17.14/swagger-ui.css"></head>
<body><div id="ui"></div>
<script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.17.14/swagger-ui-bundle.js"></script>
<script>SwaggerUIBundle({url: "/openapi.json", dom_id: "#ui", persistAuthorization: true});</script>
</body></html>"""


@docs_bp.get("/openapi.json")
def openapi_json():
    return jsonify(SPEC)


@docs_bp.get("/docs")
def swagger_ui():
    return _PAGE
