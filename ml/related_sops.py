"""Stub SOP terkait untuk fitur Analisis Insiden.

TODO: ganti dengan retrieval RAG milik rag/ setelah modul RAG siap.
"""


def get_related_sops(description: str, level: str) -> list[dict]:
    """Kembalikan daftar SOP terkait (sementara data dummy).

    Format sesuai kontrak API: [{"doc": str, "page": int}, ...]
    """
    return [
        {"doc": "SOP_LOTO.pdf", "page": 3},
        {"doc": "SOP_K3_Umum.pdf", "page": 1},
    ]