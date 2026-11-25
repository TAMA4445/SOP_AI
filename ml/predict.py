"""Prediksi level insiden K3 dari deskripsi kejadian.

Model: TF-IDF + Random Forest (ml/model.joblib).
Kelas diambil dari model.classes_ (saat ini I sampai V; level VI pada data
asli sudah digabung ke V saat pembersihan data).
Hasil bersifat indikatif, bukan pengganti penilaian ahli K3.
"""
from functools import lru_cache
from pathlib import Path

import joblib

MODEL_PATH = Path(__file__).resolve().parent / "model.joblib"


@lru_cache(maxsize=1)
def load_model():
    """Muat model sekali saja, lalu dipakai ulang."""
    return joblib.load(MODEL_PATH)


def predict_risk(description: str) -> dict:
    """Prediksi level insiden dari teks deskripsi.

    Returns:
        dict dengan key: predicted_level, confidence, probabilities,
        classes, risk_explanation.

    Raises:
        ValueError: jika deskripsi kosong atau bukan string.
    """
    if not isinstance(description, str) or not description.strip():
        raise ValueError("Deskripsi tidak boleh kosong.")

    text = description.strip()
    model = load_model()
    classes = [str(c) for c in model.classes_]
    proba = model.predict_proba([text])[0]

    best = int(proba.argmax())
    level = classes[best]

    return {
        "predicted_level": level,
        "confidence": round(float(proba[best]), 3),
        "probabilities": {
            c: round(float(p), 3) for c, p in zip(classes, proba)
        },
        "classes": classes,
        "risk_explanation": (
            f"Level {level} dari skala {classes[0]}-{classes[-1]} pada dataset. "
            "Prediksi indikatif, bukan pengganti penilaian ahli K3."
        ),
    }
