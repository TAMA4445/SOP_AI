#!/usr/bin/env python3
"""
ml/predict.py
Modul Inferensi Prediksi Tingkat Risiko Potensi Insiden K3 (Potential Accident Level).
Bagian dari Proyek SOP-AI / SOP-GPT.
"""

from __future__ import annotations

import os
from pathlib import Path
import joblib

MODEL_PATH_DEFAULT = Path(__file__).resolve().parent / "model.joblib"

# Deskripsi tingkatan risiko K3 untuk kemudahan interpretasi teknisi / manajemen
RISK_LEVEL_DESCRIPTIONS = {
    "I": "Tingkat I (Near Miss / Hampir Celaka): Potensi bahaya tanpa cedera atau hanya butuh P3K ringan.",
    "II": "Tingkat II (Minor Medical): Potensi cedera ringan dengan perawatan medis tanpa kehilangan hari kerja.",
    "III": "Tingkat III (Restricted Work): Potensi cedera sedang yang menyebabkan pembatasan kerja sementara.",
    "IV": "Tingkat IV (Lost Time Injury): Potensi cedera berat dengan kehilangan hari kerja permanen / cacat fungsi.",
    "V": "Tingkat V (Critical / Fatality Risk): Potensi cedera fatalitas tunggal atau kerusakan aset skala masif.",
}

_LOADED_MODEL = None


def load_model(model_path: str | Path | None = None):
    """Memuat model scikit-learn yang telah dilatih dari file joblib."""
    global _LOADED_MODEL
    path = Path(model_path) if model_path else MODEL_PATH_DEFAULT
    if not path.exists():
        raise FileNotFoundError(
            f"Model joblib tidak ditemukan di: {path}. "
            "Jalankan 'py ml/train_model.py' terlebih dahulu untuk melatih dan menyimpan model."
        )
    if _LOADED_MODEL is None or model_path is not None:
        _LOADED_MODEL = joblib.load(path)
    return _LOADED_MODEL


def predict_risk(description: str, model=None) -> dict:
    """Memprediksi tingkat potensi keparahan kecelakaan (Potential Accident Level)
    berdasarkan narasi kronologis insiden kerja.

    Catatan Skema Kelas:
    - Data latih dan evaluasi HANYA memiliki 5 kelas (I-V), TIDAK ADA kelas VI.
      Kelas minoritas VI pada dataset mentah telah digabungkan ke kelas 'V' selama
      tahap pra-pemrosesan data untuk menjaga keabsahan stratifikasi.
    - Daftar kelas target selalu diambil secara dinamis dari atribut `model.classes_`,
      sehingga TIDAK di-hardcode ke 'VI'.

    Args:
        description (str): Teks narasi insiden kecelakaan kerja atau nyaris celaka.
        model: Objek pipeline/estimator scikit-learn (opsional). Jika None, fungsi
               akan memuat model default dari 'ml/model.joblib'.

    Returns:
        dict: Hasil inferensi yang mencakup:
            - 'predicted_class': label kelas keparahan terpilih (misal: 'IV').
            - 'confidence': probabilitas tertinggi untuk kelas terpilih (0.0 - 1.0).
            - 'probabilities': pemetaan probabilitas untuk setiap kelas dari `model.classes_`.
            - 'classes': daftar kelas yang tersedia dari `model.classes_`.
            - 'description': teks input yang diuji.
            - 'risk_explanation': penjelasan tingkatan risiko keselamatan kerja.
    """
    if not description or not str(description).strip():
        raise ValueError("Deskripsi insiden tidak boleh kosong.")

    text = str(description).strip()
    estimator = model if model is not None else load_model()

    # Dapatkan daftar kelas secara dinamis dari model.classes_ (tanpa hardcode VI)
    classes = list(estimator.classes_)

    predicted_label = estimator.predict([text])[0]

    # Ambil probabilitas jika model mendukung predict_proba
    probabilities = {}
    confidence = 0.0
    if hasattr(estimator, "predict_proba"):
        probs = estimator.predict_proba([text])[0]
        for cls_name, prob in zip(classes, probs):
            probabilities[cls_name] = round(float(prob), 6)
        confidence = probabilities.get(predicted_label, 0.0)
    else:
        # Fallback jika model adalah decision function
        confidence = 1.0
        probabilities = {cls: (1.0 if cls == predicted_label else 0.0) for cls in classes}

    return {
        "predicted_level": str(predicted_label),
        "predicted_class": str(predicted_label),
        "confidence": confidence,
        "probabilities": probabilities,
        "classes": classes,
        "description": text,
        "risk_explanation": RISK_LEVEL_DESCRIPTIONS.get(
            str(predicted_label), f"Tingkat Risiko: {predicted_label}"
        ),
    }


if __name__ == "__main__":
    import sys

    sample_text = (
        sys.argv[1]
        if len(sys.argv) > 1
        else (
            "While removing the drill rod of the Jumbo 08 for maintenance, "
            "the bar slides and tightens the fingers of the mechanic between the drilling bar."
        )
    )

    print("=" * 70)
    print("INFERENSI PREDIKSI RISIKO INSIDEN K3 (SOP-AI)")
    print("=" * 70)
    try:
        result = predict_risk(sample_text)
        print(f"Teks Insiden    : {result['description'][:90]}...")
        print(f"Prediksi Kelas  : {result['predicted_class']}")
        print(f"Confidence      : {result['confidence'] * 100:.2f}%")
        print(f"Daftar Kelas    : {result['classes']} (diambil dari model.classes_)")
        print("\nProbabilitas per Kelas:")
        for cls_name, prob in result["probabilities"].items():
            print(f"  - Kelas {cls_name:3s}: {prob * 100:5.2f}%")
        print(f"\nKeterangan K3   : {result['risk_explanation']}")
    except Exception as exc:
        print(f"Error inferensi: {exc}")
