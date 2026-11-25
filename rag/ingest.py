"""
Pipeline ingestion: PDF → chunks → ChromaDB (embedding persisten).

Fungsi utama:
    ingest(file_path: str) -> dict
"""

import os
from pathlib import Path

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import chromadb

from rag.config import (
    GOOGLE_API_KEY,
    CHROMA_DIR,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBEDDING_MODEL,
)


def _get_chroma_collection() -> tuple[chromadb.ClientAPI, chromadb.Collection]:
    """Buat/ambil client dan collection ChromaDB persisten."""
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_or_create_collection(
        name="sop_docs",
        metadata={"hnsw:space": "cosine"},
    )
    return client, collection


def _embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed daftar teks menggunakan Google Generative AI Embeddings."""
    embedder = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=GOOGLE_API_KEY,
    )
    return embedder.embed_documents(texts)


def delete_document(doc_name: str) -> bool:
    """Hapus seluruh chunk vektor dokumen dari ChromaDB berdasarkan nama file.

    Parameters
    ----------
    doc_name : str
        Nama file dokumen (misal: 'SOP_LOTO.pdf' atau path).

    Returns
    -------
    bool
        True jika berhasil (atau dokumen memang tidak ada), False jika error.
    """
    try:
        clean_name = Path(doc_name).name
        _, collection = _get_chroma_collection()
        existing = collection.get(where={"doc": clean_name})
        if existing and existing["ids"]:
            collection.delete(ids=existing["ids"])
        return True
    except Exception:
        return False


def ingest(file_path: str) -> dict:
    """Ingest satu file PDF ke ChromaDB.

    Parameters
    ----------
    file_path : str
        Path absolut atau relatif ke file PDF.

    Returns
    -------
    dict
        ``{"status": "success", "doc_name": "<nama>.pdf", "total_chunks": N}``
        atau ``{"status": "error", "message": "..."}`` jika gagal.
    """
    # ── Validasi awal ────────────────────────────────────────────────────
    if not GOOGLE_API_KEY:
        return {
            "status": "error",
            "message": "GOOGLE_API_KEY belum diset. Tambahkan ke file .env atau environment variable.",
        }

    file_path = str(Path(file_path).resolve())
    if not os.path.isfile(file_path):
        return {
            "status": "error",
            "message": f"File tidak ditemukan: {file_path}",
        }

    doc_name = Path(file_path).name  # contoh: "SOP_LOTO.pdf"

    try:
        # ── 1. Load PDF ──────────────────────────────────────────────────
        loader = PyMuPDFLoader(file_path)
        raw_docs = loader.load()

        if not raw_docs:
            return {
                "status": "error",
                "message": f"Tidak ada konten yang bisa dibaca dari {doc_name}.",
            }

        # ── 2. Chunking ─────────────────────────────────────────────────
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " ", ""],
        )
        chunks = splitter.split_documents(raw_docs)

        if not chunks:
            return {
                "status": "error",
                "message": f"Hasil chunking kosong untuk {doc_name}.",
            }

        # ── 3. Siapkan metadata bersih ───────────────────────────────────
        texts: list[str] = []
        metadatas: list[dict] = []
        ids: list[str] = []

        for idx, chunk in enumerate(chunks):
            # PyMuPDFLoader menyimpan halaman di metadata["page"] (0-based)
            raw_page = chunk.metadata.get("page", 0)
            page_number = int(raw_page) + 1  # konversi ke 1-based

            texts.append(chunk.page_content)
            metadatas.append({"doc": doc_name, "page": page_number})
            ids.append(f"{doc_name}::chunk_{idx}")

        # ── 4. Hapus data lama untuk doc yang sama (anti-duplikasi) ───────
        _, collection = _get_chroma_collection()

        existing = collection.get(where={"doc": doc_name})
        if existing and existing["ids"]:
            collection.delete(ids=existing["ids"])

        # ── 5. Embed & simpan ke ChromaDB ────────────────────────────────
        embeddings = _embed_texts(texts)

        # ChromaDB membatasi jumlah per-batch; kita batch per 500
        batch_size = 500
        for start in range(0, len(ids), batch_size):
            end = start + batch_size
            collection.add(
                ids=ids[start:end],
                embeddings=embeddings[start:end],
                documents=texts[start:end],
                metadatas=metadatas[start:end],
            )

        return {
            "status": "success",
            "doc_name": doc_name,
            "total_chunks": len(ids),
        }

    except Exception as exc:
        return {
            "status": "error",
            "message": f"Gagal ingest {doc_name}: {exc}",
        }

