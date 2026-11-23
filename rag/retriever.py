"""
Pipeline retrieval + generation: question → ChromaDB → Gemini → answer.

Fungsi utama:
    ask(question: str, chat_history: list = None) -> dict
"""

from __future__ import annotations

from langchain_google_genai import GoogleGenerativeAIEmbeddings
import chromadb
from google import genai
from google.genai import types

from rag.config import (
    GOOGLE_API_KEY,
    CHROMA_DIR,
    EMBEDDING_MODEL,
    LLM_MODEL,
    TOP_K,
)

# ── System prompt anti-halusinasi ────────────────────────────────────────────
_SYSTEM_PROMPT = """\
Kamu adalah asisten ahli K3 (Keselamatan dan Kesehatan Kerja) bernama SOP-GPT.

ATURAN WAJIB:
1. Jawab HANYA berdasarkan konteks dokumen yang disediakan di bawah ini.
2. DILARANG KERAS menggunakan pengetahuan di luar konteks dokumen.
3. Jika jawaban tidak ditemukan di dalam konteks dokumen, kamu WAJIB menjawab \
PERSIS dengan kalimat berikut tanpa mengubah satu kata pun:
   "Maaf, informasi tersebut tidak ditemukan dalam dokumen SOP atau manual yang tersedia."
4. Jika jawaban berupa prosedur atau langkah-langkah, sajikan dalam format \
poin bernomor yang jelas dan berurutan.
5. Gunakan bahasa Indonesia yang formal dan profesional.
6. Sertakan referensi halaman jika relevan.
"""


def _get_chroma_collection() -> chromadb.Collection | None:
    """Ambil collection ChromaDB. Return None jika belum ada data."""
    try:
        client = chromadb.PersistentClient(path=CHROMA_DIR)
        collection = client.get_or_create_collection(
            name="sop_docs",
            metadata={"hnsw:space": "cosine"},
        )
        if collection.count() == 0:
            return None
        return collection
    except Exception:
        return None


def _search(question: str, top_k: int = TOP_K) -> list[dict]:
    """Lakukan similarity search ke ChromaDB.

    Returns
    -------
    list[dict]
        Tiap dict berisi keys: ``doc``, ``page``, ``snippet``, ``text``.
    """
    collection = _get_chroma_collection()
    if collection is None:
        return []

    # Embed query
    embedder = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=GOOGLE_API_KEY,
    )
    query_embedding = embedder.embed_query(question)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas"],
    )

    hits: list[dict] = []
    if not results or not results.get("documents"):
        return hits

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    for doc_text, meta in zip(documents, metadatas):
        hits.append(
            {
                "doc": meta.get("doc", "unknown"),
                "page": int(meta.get("page", 0)),
                "snippet": doc_text[:200].strip(),
                "text": doc_text,
            }
        )

    return hits


def _build_context(hits: list[dict]) -> str:
    """Gabungkan hit menjadi blok konteks untuk prompt LLM."""
    if not hits:
        return "(Tidak ada dokumen yang relevan ditemukan.)"

    parts: list[str] = []
    for i, h in enumerate(hits, 1):
        parts.append(
            f"[Sumber {i}] Dokumen: {h['doc']}, Halaman: {h['page']}\n{h['text']}"
        )
    return "\n\n---\n\n".join(parts)


def _deduplicate_sources(hits: list[dict]) -> list[dict]:
    """Hilangkan duplikasi berdasarkan pasangan (doc, page)."""
    seen: set[tuple[str, int]] = set()
    unique: list[dict] = []
    for h in hits:
        key = (h["doc"], h["page"])
        if key not in seen:
            seen.add(key)
            unique.append(
                {
                    "doc": h["doc"],
                    "page": h["page"],
                    "snippet": h["snippet"],
                }
            )
    return unique


def ask(question: str, chat_history: list | None = None) -> dict:
    """Jawab pertanyaan berdasarkan dokumen SOP yang sudah di-ingest.

    Parameters
    ----------
    question : str
        Pertanyaan pengguna.
    chat_history : list, optional
        Riwayat percakapan sebelumnya (list of dict ``{"role": ..., "parts": ...}``).

    Returns
    -------
    dict
        ``{"answer": "...", "sources": [{"doc": ..., "page": ..., "snippet": ...}, ...]}``
    """
    # ── Validasi API key ─────────────────────────────────────────────────
    if not GOOGLE_API_KEY:
        return {
            "answer": "Error: GOOGLE_API_KEY belum diset. Tambahkan ke file .env atau environment variable.",
            "sources": [],
        }

    try:
        # ── 1. Retrieval ─────────────────────────────────────────────────
        hits = _search(question)

        # Jika tidak ada hit, langsung kembalikan jawaban default
        if not hits:
            return {
                "answer": "Maaf, informasi tersebut tidak ditemukan dalam dokumen SOP atau manual yang tersedia.",
                "sources": [],
            }

        # ── 2. Bangun konteks ────────────────────────────────────────────
        context = _build_context(hits)

        user_prompt = (
            f"KONTEKS DOKUMEN:\n{context}\n\n"
            f"PERTANYAAN PENGGUNA:\n{question}"
        )

        # ── 3. Siapkan riwayat percakapan ────────────────────────────────
        client = genai.Client(api_key=GOOGLE_API_KEY)

        contents: list[types.Content] = []

        # Tambahkan chat_history jika ada
        if chat_history:
            for entry in chat_history:
                role = entry.get("role", "user")
                text = entry.get("parts", "")
                if isinstance(text, list):
                    text = "\n".join(str(p) for p in text)
                contents.append(
                    types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=str(text))],
                    )
                )

        # Tambahkan pertanyaan saat ini
        contents.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_prompt)],
            )
        )

        # ── 4. Generate jawaban ──────────────────────────────────────────
        response = client.models.generate_content(
            model=LLM_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=_SYSTEM_PROMPT,
            ),
        )
        answer_text = response.text.strip()

        # ── 5. Susun sources (deduplicated) ──────────────────────────────
        # Jika informasi tidak ditemukan dalam dokumen, kosongkan sources
        not_found_phrases = [
            "tidak ditemukan dalam dokumen",
            "tidak ditemukan di dalam dokumen",
            "informasi tersebut tidak ditemukan",
        ]
        answer_lower = answer_text.lower()
        if any(phrase in answer_lower for phrase in not_found_phrases):
            sources = []
        else:
            sources = _deduplicate_sources(hits)

        return {
            "answer": answer_text,
            "sources": sources,
        }

    except Exception as exc:
        return {
            "answer": f"Error saat memproses pertanyaan: {exc}",
            "sources": [],
        }
