"""Penghubung ke modul ``rag`` milik Orang 2.

Backend hanya butuh dua fungsi: ``ask(question, chat_history)`` dan ``ingest(path)``.
Kalau modul rag belum siap (atau dependensinya belum terpasang), mode "auto"
jatuh ke stub berisi jawaban hardcode, jadi backend & frontend tetap bisa jalan.
"""

from __future__ import annotations

import logging
import os

log = logging.getLogger("sopgpt.rag")


class StubRag:
    name = "stub"

    def ask(self, question: str, chat_history: list | None = None) -> dict:
        q = question.lower()

        # 1. Negative test / anti-halusinasi
        if any(w in q for w in ['kue', 'resep', 'saham', 'cuaca', 'presiden', 'film', 'lagu', 'game']):
            return {
                "answer": "Maaf, informasi tersebut tidak ditemukan dalam dokumen SOP atau manual yang tersedia.",
                "sources": [],
            }

        # 2. Topik LOTO (SOP-01)
        if any(w in q for w in ['loto', 'lockout', 'tagout', 'kunci', 'gembok', 'isolasi']):
            return {
                "answer": (
                    "Berdasarkan SOP-01 (Prosedur Lockout/Tagout pada Pemeliharaan Mesin), tahapan wajib isolasi energi adalah sebagai berikut:\n\n"
                    "1. Pemberitahuan: Menginformasikan kepada seluruh operator area bahwa mesin akan dinonaktifkan.\n"
                    "2. Pemadaman Mesin (Shutdown): Mematikan mesin sesuai urutan kontrol normal.\n"
                    "3. Isolasi Energi: Memutus sakelar daya utama, menutup katup pneumatik/hidrolik.\n"
                    "4. Pemasangan LOTO: Memasang gembok keselamatan (padlock) pribadi dan tag peringatan bertuliskan 'DILARANG DIOPERASIKAN'.\n"
                    "5. Pelepasan Energi Sisa: Membuang sisa tekanan udara/cairan dan memasang pentanahan (grounding) pada kapasitor.\n"
                    "6. Verifikasi Kondisi Nol (Zero Energy State): Menekan tombol start untuk memastikan mesin benar-benar tidak dapat menyala sebelum pekerjaan dimulai."
                ),
                "sources": [
                    {
                        "doc": "SOP_LOTO_v1.pdf",
                        "page": 3,
                        "snippet": "Bagian 3.2 Prosedur Pelaksanaan LOTO: Setiap teknisi yang bertugas wajib memasang gembok keselamatan pribadi dan memverifikasi kondisi nol energi sebelum memulai pekerjaan fisik."
                    },
                    {
                        "doc": "SOP_LOTO_v1.pdf",
                        "page": 4,
                        "snippet": "Bagian 4.1 Group Lockout: Pada pekerjaan kelompok, wajib digunakan hasp pengunci ganda dan master lockout box."
                    }
                ],
            }

        # 3. Topik APD (SOP-02)
        if any(w in q for w in ['apd', 'pelindung', 'helm', 'sepatu', 'sarung tangan', 'kacamata', 'masker']):
            return {
                "answer": (
                    "Berdasarkan SOP-02 (Standar Penggunaan dan Pemeliharaan APD):\n\n"
                    "• Area Mekanik & Produksi: Wajib menggunakan Safety Helmet (Standar ANSI Z89.1), Kacamata pelindung (Safety Goggles), dan Sepatu Safety dengan pelindung baja (Steel Toe Cap 200 Joule).\n"
                    "• Pekerjaan Kelistrikan: Wajib menggunakan sarung tangan isolasi karet kelas 0 (tahan 1000V) dan sepatu safety dielektrik tanpa logam terbuka.\n"
                    "• Bahan Kimia Korosif: Wajib mengenakan pelindung wajah (Face Shield), celemek karet tahan asam, dan sarung tangan berbahan nitril/neoprena.\n\n"
                    "Masa pakai helm keselamatan maksimal 5 tahun sejak tanggal produksi atau wajib diganti segera apabila pernah mengalami benturan keras."
                ),
                "sources": [
                    {
                        "doc": "SOP_APD_v1.pdf",
                        "page": 2,
                        "snippet": "Tabel 2.1 Matriks Wajib APD: Karyawan dan tamu dilarang memasuki zona operasional tanpa APD dasar (Helm, Kacamata, Sepatu)."
                    }
                ],
            }

        # 4. Topik Kebakaran (SOP-03)
        if any(w in q for w in ['kebakaran', 'api', 'apar', 'hidran', 'evakuasi', 'darurat']):
            return {
                "answer": (
                    "Berdasarkan SOP-03 (Pencegahan dan Penanggulangan Bahaya Kebakaran):\n\n"
                    "1. Prosedur Penggunaan APAR (Metode PASS):\n"
                    "   • P - Pull: Tarik pin pengaman tabung APAR.\n"
                    "   • A - Aim: Arahkan corong selang ke dasar nyala api (bukan ke lidah api).\n"
                    "   • S - Squeeze: Tekan tuas pemicu secara stabil.\n"
                    "   • S - Sweep: Sapukan corong dari sisi kiri ke kanan secara merata.\n\n"
                    "2. Prosedur Evakuasi:\n"
                    "   Segera tinggalkan tempat kerja mengikuti rute jalur hijau evakuasi, jangan gunakan lift, dan berkumpul di Titik Kumpul (Assembly Point) untuk proses penghitungan absensi oleh Floor Warden."
                ),
                "sources": [
                    {
                        "doc": "SOP_Kebakaran_v1.pdf",
                        "page": 4,
                        "snippet": "Bagian 4.3 Tanggap Darurat Kebakaran: Pemadaman mandiri hanya diperbolehkan untuk api awal (tahap mula). Jika api membesar, segera evakuasi menuju titik kumpul."
                    }
                ],
            }

        # 5. Jawaban umum SOP
        return {
            "answer": (
                f"Terkait pertanyaan Anda mengenai '{question}', seluruh personel diwajibkan selalu mematuhi instruksi kerja keselamatan dan SOP resmi pabrik. Pastikan izin kerja (Permit to Work) telah ditandatangani oleh supervisor K3 sebelum memulai aktivitas berisiko tinggi."
            ),
            "sources": [
                {
                    "doc": "SOP_Standar_Operasional_K3.pdf",
                    "page": 1,
                    "snippet": "Pedoman Umum K3: Keselamatan kerja adalah tanggung jawab bersama di seluruh lini manufaktur."
                }
            ],
        }

    def ingest(self, file_path: str) -> dict:
        return {"status": "success", "doc_name": os.path.basename(file_path), "total_chunks": 0}

    def delete_document(self, doc_name: str) -> bool:
        return True


class RealRag:
    name = "real"

    def __init__(self):
        import rag  # noqa: WPS433 (import lazy, bisa gagal bila dependensi belum ada)

        self._rag = rag

    def ask(self, question: str, chat_history: list | None = None) -> dict:
        return self._rag.ask(question, chat_history=chat_history)

    def ingest(self, file_path: str) -> dict:
        return self._rag.ingest(file_path)

    def delete_document(self, doc_name: str) -> bool:
        """Hapus vektor dokumen. Butuh ``rag.delete_document`` dari Orang 2 (belum ada)."""
        fn = getattr(self._rag, "delete_document", None)
        if fn is None:
            return False
        fn(doc_name)
        return True


def build_rag(mode: str):
    if mode == "stub":
        return StubRag()
    try:
        return RealRag()
    except Exception as exc:  # noqa: BLE001
        if mode == "real":
            raise
        log.warning("Modul rag tidak bisa dimuat (%s). Memakai STUB.", exc)
        return StubRag()
