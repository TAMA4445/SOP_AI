"""
Modul RAG untuk SOP-GPT.

Ekspor utama:
    - ingest(file_path)  → dict   (dari rag.ingest)
    - ask(question, ...)  → dict   (dari rag.retriever)
    - delete_document(doc_name) → bool (dari rag.ingest)
"""

from rag.ingest import ingest, delete_document
from rag.retriever import ask

__all__ = ["ingest", "ask", "delete_document"]
