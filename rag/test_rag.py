#!/usr/bin/env python
"""
Skrip CLI untuk menguji pipeline RAG (ingest + tanya-jawab).

Cara pakai:
    # Ingest satu file PDF
    python -m rag.test_rag --ingest path/ke/dokumen.pdf

    # Tanya jawab interaktif
    python -m rag.test_rag --ask

    # Ingest lalu langsung tanya jawab
    python -m rag.test_rag --ingest path/ke/dokumen.pdf --ask
"""

import argparse
import json
import sys

from rag.ingest import ingest
from rag.retriever import ask


def run_ingest(file_path: str) -> None:
    """Jalankan proses ingest dan tampilkan hasilnya."""
    print(f"\n{'='*60}")
    print(f"  INGEST: {file_path}")
    print(f"{'='*60}")

    result = ingest(file_path)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if result["status"] == "success":
        print(f"\n✅ Berhasil ingest {result['doc_name']} → {result['total_chunks']} chunks")
    else:
        print(f"\n❌ Gagal: {result.get('message', 'Unknown error')}")


def run_ask() -> None:
    """Jalankan sesi tanya-jawab interaktif."""
    print(f"\n{'='*60}")
    print("  TANYA-JAWAB SOP-GPT (ketik 'exit' untuk keluar)")
    print(f"{'='*60}\n")

    chat_history: list[dict] = []

    while True:
        try:
            question = input("📝 Pertanyaan: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n👋 Selesai.")
            break

        if not question:
            continue
        if question.lower() in ("exit", "quit", "q"):
            print("\n👋 Selesai.")
            break

        result = ask(question, chat_history=chat_history)

        # Tampilkan jawaban
        print(f"\n💬 Jawaban:\n{result['answer']}\n")

        # Tampilkan sumber
        if result["sources"]:
            print("📚 Sumber:")
            for src in result["sources"]:
                print(f"   • {src['doc']} — Hal. {src['page']}")
                print(f"     \"{src['snippet'][:100]}...\"")
            print()

        # Simpan ke chat_history untuk konteks percakapan
        chat_history.append({"role": "user", "parts": [question]})
        chat_history.append({"role": "model", "parts": [result["answer"]]})


def main() -> None:
    parser = argparse.ArgumentParser(
        description="CLI untuk menguji pipeline RAG SOP-GPT",
    )
    parser.add_argument(
        "--ingest",
        type=str,
        metavar="FILE",
        help="Path ke file PDF yang akan di-ingest",
    )
    parser.add_argument(
        "--ask",
        action="store_true",
        help="Masuk ke mode tanya-jawab interaktif",
    )

    args = parser.parse_args()

    if not args.ingest and not args.ask:
        parser.print_help()
        print("\n⚠️  Gunakan --ingest FILE dan/atau --ask")
        sys.exit(1)

    if args.ingest:
        run_ingest(args.ingest)

    if args.ask:
        run_ask()


if __name__ == "__main__":
    main()

