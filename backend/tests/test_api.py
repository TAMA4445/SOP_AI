import io

import pytest

from backend.app import create_app
from backend.memdb import LocalDB as FakeDB


class FakeRag:
    name = "fake"

    def __init__(self):
        self.ask_calls = []
        self.deleted = []

    def ask(self, question, chat_history=None):
        self.ask_calls.append((question, chat_history))
        if "ngawur" in question:
            return {"answer": "Maaf, informasi tersebut tidak ditemukan dalam dokumen SOP atau manual yang tersedia.", "sources": []}
        return {"answer": f"jawab:{question}", "sources": [{"doc": "SOP_LOTO_v1.pdf", "page": 2, "snippet": "x"}]}

    def ingest(self, path):
        if path.endswith("rusak.pdf"):
            return {"status": "error", "message": "Tidak ada konten"}
        return {"status": "success", "doc_name": path.split("/")[-1], "total_chunks": 7}

    def delete_document(self, name):
        self.deleted.append(name)
        return True


@pytest.fixture
def rag():
    return FakeRag()


@pytest.fixture
def client(tmp_path, rag):
    app = create_app({"UPLOAD_DIR": str(tmp_path / "up"), "JWT_SECRET": "test-secret-yang-cukup-panjang-32-byte!!", "MAX_UPLOAD_MB": 1}, db=FakeDB(), rag=rag)
    return app.test_client()


def login(client, user="teknisi", pw="teknisi123"):
    r = client.post("/api/auth/login", json={"username": user, "password": pw})
    assert r.status_code == 200, r.get_data(as_text=True)
    return {"Authorization": "Bearer " + r.get_json()["access_token"]}


def pdf(name="SOP_Baru.pdf", body=b"%PDF-1.4 fake"):
    return {"file": (io.BytesIO(body), name)}


def test_health(client):
    assert client.get("/api/health").get_json() == {"status": "ok", "rag_mode": "fake"}


def test_login_ok_and_bad(client):
    h = login(client)
    me = client.get("/api/auth/me", headers=h).get_json()
    assert me["username"] == "teknisi" and me["role"] == "teknisi" and "password_hash" not in me
    assert client.post("/api/auth/login", json={"username": "teknisi", "password": "salah"}).status_code == 401
    assert client.post("/api/auth/login", json={}).status_code == 401


def test_auth_required(client):
    assert client.post("/api/chat", json={"question": "a"}).status_code == 401
    assert client.get("/api/documents", headers={"Authorization": "Bearer abc"}).status_code == 401


def test_chat_contract_and_history_passed_to_rag(client, rag):
    h = login(client)
    r1 = client.post("/api/chat", json={"question": "Apa itu LOTO?", "session_id": "s1"}, headers=h)
    assert r1.status_code == 200
    body = r1.get_json()
    assert body["answer"] == "jawab:Apa itu LOTO?"
    assert body["sources"][0] == {"doc": "SOP_LOTO_v1.pdf", "page": 2, "snippet": "x"}
    assert body["session_id"] == "s1" and body["message_id"]
    client.post("/api/chat", json={"question": "Langkah?", "session_id": "s1"}, headers=h)
    _, hist = rag.ask_calls[1]
    assert hist == [{"role": "user", "parts": ["Apa itu LOTO?"]}, {"role": "model", "parts": ["jawab:Apa itu LOTO?"]}]


def test_chat_validation_and_generated_session(client):
    h = login(client)
    assert client.post("/api/chat", json={"question": "  "}, headers=h).status_code == 400
    assert client.post("/api/chat", json={"question": "x" * 2001}, headers=h).status_code == 400
    r = client.post("/api/chat", json={"question": "halo"}, headers=h).get_json()
    assert len(r["session_id"]) == 32


def test_chat_rag_failure_returns_502(client, rag):
    rag.ask = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom"))
    h = login(client)
    r = client.post("/api/chat", json={"question": "x"}, headers=h)
    assert r.status_code == 502 and "boom" in r.get_json()["error"]


def test_sessions_history_isolation_delete(client):
    t, a = login(client), login(client, "admin", "admin123")
    client.post("/api/chat", json={"question": "q1", "session_id": "s1"}, headers=t)
    client.post("/api/chat", json={"question": "q2", "session_id": "s1"}, headers=t)
    client.post("/api/chat", json={"question": "q3", "session_id": "s2"}, headers=t)
    s = client.get("/api/chat/sessions", headers=t).get_json()["sessions"]
    assert {x["session_id"]: x["message_count"] for x in s} == {"s1": 2, "s2": 1}
    msgs = client.get("/api/chat/history?session_id=s1", headers=t).get_json()["messages"]
    assert [m["question"] for m in msgs] == ["q1", "q2"]
    assert client.get("/api/chat/history?session_id=s1", headers=a).get_json()["messages"] == []
    assert client.get("/api/chat/history", headers=t).status_code == 400
    assert client.delete("/api/chat/sessions/s1", headers=a).status_code == 404
    assert client.delete("/api/chat/sessions/s1", headers=t).get_json() == {"deleted": 2}
    assert len(client.get("/api/chat/sessions", headers=t).get_json()["sessions"]) == 1


def test_documents_admin_only_upload(client, tmp_path):
    t, a = login(client), login(client, "admin", "admin123")
    assert client.post("/api/documents", data=pdf(), headers=t, content_type="multipart/form-data").status_code == 403
    r = client.post("/api/documents", data=pdf(), headers=a, content_type="multipart/form-data")
    assert r.status_code == 201 and r.get_json()["total_chunks"] == 7
    assert (tmp_path / "up" / "SOP_Baru.pdf").exists()
    again = client.post("/api/documents", data=pdf(), headers=a, content_type="multipart/form-data")
    assert again.status_code == 200
    docs = client.get("/api/documents", headers=t).get_json()["documents"]
    assert [d["name"] for d in docs] == ["SOP_Baru.pdf"]


def test_document_rejections(client, tmp_path):
    a = login(client, "admin", "admin123")
    post = lambda data: client.post("/api/documents", data=data, headers=a, content_type="multipart/form-data")
    assert post({}).status_code == 400
    assert post(pdf("catatan.txt")).status_code == 400
    assert post(pdf("palsu.pdf", b"bukan pdf")).status_code == 400
    r = post(pdf("rusak.pdf"))
    assert r.status_code == 422 and not (tmp_path / "up" / "rusak.pdf").exists()
    assert post(pdf("besar.pdf", b"%PDF-" + b"0" * (2 * 1024 * 1024))).status_code == 413
    assert client.get("/api/documents", headers=a).get_json()["documents"] == []


def test_document_delete(client, rag, tmp_path):
    a = login(client, "admin", "admin123")
    doc = client.post("/api/documents", data=pdf(), headers=a, content_type="multipart/form-data").get_json()
    r = client.delete(f"/api/documents/{doc['id']}", headers=a)
    assert r.get_json() == {"deleted": "SOP_Baru.pdf", "vectors_removed": True}
    assert rag.deleted == ["SOP_Baru.pdf"] and not (tmp_path / "up" / "SOP_Baru.pdf").exists()
    assert client.delete(f"/api/documents/{doc['id']}", headers=a).status_code == 404


def test_feedback_upsert_and_ownership(client):
    t, a = login(client), login(client, "admin", "admin123")
    mid = client.post("/api/chat", json={"question": "q", "session_id": "s"}, headers=t).get_json()["message_id"]
    assert client.post("/api/feedback", json={"message_id": mid, "rating": "meh"}, headers=t).status_code == 400
    assert client.post("/api/feedback", json={"message_id": mid, "rating": "up"}, headers=a).status_code == 404
    assert client.post("/api/feedback", json={"message_id": mid, "rating": "up"}, headers=t).status_code == 200
    client.post("/api/feedback", json={"message_id": mid, "rating": "down", "comment": "kurang"}, headers=t)
    h = client.get("/api/chat/history?session_id=s", headers=t).get_json()["messages"]
    assert h[0]["feedback"] == "down"
    fb = client.get("/api/feedback", headers=a).get_json()["feedback"]
    assert len(fb) == 1 and fb[0]["rating"] == "down" and fb[0]["question"] == "q"
    assert client.get("/api/feedback?rating=up", headers=a).get_json()["feedback"] == []
    assert client.get("/api/feedback", headers=t).status_code == 403


def test_stats(client):
    t, a = login(client), login(client, "admin", "admin123")
    for q in ["Apa itu LOTO?", "apa itu loto", "Cara APD?", "ngawur"]:
        client.post("/api/chat", json={"question": q, "session_id": "s"}, headers=t)
    mid = client.get("/api/chat/history?session_id=s", headers=t).get_json()["messages"][0]["message_id"]
    client.post("/api/feedback", json={"message_id": mid, "rating": "up"}, headers=t)
    assert client.get("/api/stats", headers=t).status_code == 403
    s = client.get("/api/stats", headers=a).get_json()
    assert s["totals"] == {"users": 2, "documents": 0, "questions": 4, "feedback_up": 1, "feedback_down": 0}
    assert s["top_questions"][0] == {"question": "Apa itu LOTO?", "count": 2}
    assert s["top_documents"] == [{"doc": "SOP_LOTO_v1.pdf", "count": 3}]  # "ngawur" tanpa sumber
    assert len(s["questions_per_day"]) == 7 and s["questions_per_day"][-1]["count"] == 4


def test_user_management(client):
    t, a = login(client), login(client, "admin", "admin123")
    body = {"username": "budi", "password": "rahasia1", "role": "teknisi"}
    assert client.post("/api/users", json=body, headers=t).status_code == 403
    assert client.post("/api/users", json=body, headers=a).status_code == 201
    assert client.post("/api/users", json=body, headers=a).status_code == 409
    assert client.post("/api/users", json={**body, "username": "x"}, headers=a).status_code == 400
    assert client.post("/api/users", json={**body, "username": "cc", "password": "123"}, headers=a).status_code == 400
    assert client.post("/api/users", json={**body, "username": "dd", "role": "bos"}, headers=a).status_code == 400
    login(client, "budi", "rahasia1")
    assert len(client.get("/api/users", headers=a).get_json()["users"]) == 3


def test_docs_endpoints_and_json_errors(client):
    spec = client.get("/openapi.json").get_json()
    assert "/api/chat" in spec["paths"] and "/api/stats" in spec["paths"]
    assert b"SwaggerUIBundle" in client.get("/docs").data
    assert client.get("/api/tidak-ada").get_json() == {"error": "Endpoint tidak ditemukan."}


def test_cors_headers(client):
    r = client.options("/api/chat", headers={"Origin": "http://localhost:5173"})
    assert r.headers["Access-Control-Allow-Origin"] == "http://localhost:5173"
    r = client.options("/api/chat", headers={"Origin": "http://jahat.example"})
    assert "Access-Control-Allow-Origin" not in r.headers


def test_local_db_persists_to_file(tmp_path):
    path = str(tmp_path / "db.json")
    cfg = {"DB_MODE": "local", "LOCAL_DB_PATH": path, "UPLOAD_DIR": str(tmp_path / "up"), "JWT_SECRET": "test-secret-yang-cukup-panjang-32-byte!!"}
    c1 = create_app(cfg, rag=FakeRag()).test_client()
    h = login(c1)
    sid = c1.post("/api/chat", json={"question": "simpan ini", "session_id": "p"}, headers=h).get_json()["session_id"]
    # "restart": app baru membaca file yang sama
    c2 = create_app(cfg, rag=FakeRag()).test_client()
    msgs = c2.get(f"/api/chat/history?session_id={sid}", headers=login(c2)).get_json()["messages"]
    assert [m["question"] for m in msgs] == ["simpan ini"]
    assert c2.get("/api/auth/me", headers=h).status_code == 200  # token lama tetap valid, user sama
