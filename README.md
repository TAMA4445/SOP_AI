# SOP-GPT (RAG Pipeline)

Sistem tanya-jawab cerdas berbasis dokumen SOP (Standar Operasional Prosedur) K3 dan manual mesin menggunakan Retrieval-Augmented Generation (RAG) dengan ChromaDB dan Google Gemini API.

---

## 📁 Struktur Direktori

```
SOP_AI/
├── data/                  # Dokumen PDF SOP / Manual
├── rag/
│   ├── __init__.py        # Ekspor modul: ingest, ask
│   ├── config.py          # Konfigurasi terpusat (.env)
│   ├── ingest.py          # Pipeline PDF Loader -> Chunking -> Vector Store
│   ├── retriever.py       # Pipeline Similarity Search -> Anti-Hallucination Prompt -> Gemini
│   └── test_rag.py        # CLI tool untuk ingest & tanya-jawab langsung
├── .env.example           # Template environment variable
├── .gitignore             # File yang diabaikan Git (.env, chroma_db/, dll.)
└── requirements.txt       # Daftar dependency Python
```

---

## 🚀 Setup & Instalasi

### 1. Clone Repository & Install Dependency
```bash
git clone https://github.com/TAMA4445/SOP_AI.git
cd SOP_AI
pip install -r requirements.txt
```

### 2. Konfigurasi API Key
Salin `.env.example` menjadi `.env` dan masukkan API Key dari [Google AI Studio](https://aistudio.google.com/apikey):
```bash
cp .env.example .env
```
Isi file `.env`:
```env
GOOGLE_API_KEY=your_actual_api_key_here
```

---

## 🛠️ Cara Penggunaan

### 1. Ingest Dokumen PDF via CLI
```bash
python -m rag.test_rag --ingest "data/SOP_LOTO_v1.pdf"
```

### 2. Tanya-Jawab Interaktif via CLI
```bash
python -m rag.test_rag --ask
```

### 3. Digunakan oleh Backend API
```python
from rag import ingest, ask

# 1. Ingest dokumen baru
result = ingest("data/SOP_LOTO_v1.pdf")
print(result)
# Output: {"status": "success", "doc_name": "SOP_LOTO_v1.pdf", "total_chunks": 34}

# 2. Ajukan pertanyaan
response = ask("Bagaimana prosedur sistem kunci kelompok atau Group Lockout?")
print(response["answer"])
print(response["sources"])
# Output:
# {
#   "answer": "...",
#   "sources": [{"doc": "SOP_LOTO_v1.pdf", "page": 4, "snippet": "..."}]
# }
```

---

## 🔒 Fitur Anti-Halusinasi
- LLM hanya menjawab berdasarkan konteks dokumen SOP yang ditemukan.
- Jika informasi tidak ada di dalam dokumen, sistem secara tegas mengembalikan:
  `"Maaf, informasi tersebut tidak ditemukan dalam dokumen SOP atau manual yang tersedia."`
- Jika informasi tidak ditemukan, key `"sources"` otomatis dikembalikan sebagai list kosong `[]`.
