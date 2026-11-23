"""
Modul RAG untuk SOP-GPT.

Ekspor utama:
    - ingest(file_path)  → dict   (dari rag.ingest)
    - ask(question, ...)  → dict   (dari rag.retriever)
"""

from rag.ingest import ingest
from rag.retriever import ask

__all__ = ["ingest", "ask"]

