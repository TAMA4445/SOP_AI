#!/usr/bin/env python3
"""
ml/test_predict.py
Pengujian Unit (pytest) untuk Fungsi predict_risk.

Mencakup 3 kasus uji utama:
1. Input normal: format output valid, confidence [0, 1], sum(probabilities) ~= 1, predicted_level in classes.
2. Input kosong: melempar ValueError jika string kosong atau spasi saja.
3. Input sangat panjang (>= 5000 karakter): berjalan lancar tanpa error dan menghasilkan output valid.
"""

import sys
from pathlib import Path
import pytest

# Pastikan root direktori repositori terdaftar di sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ml.predict import predict_risk


def test_predict_risk_normal_input():
    """Kasus 1: Input normal.
    Memastikan output memiliki key predicted_level, confidence, probabilities;
    confidence bernilai antara 0 dan 1;
    jumlah seluruh nilai probabilities mendekati 1;
    predicted_level termasuk dalam daftar classes.
    """
    sample_text = (
        "While replacing the hydraulic valve of the drilling machine, "
        "the pressure hose released remaining oil and injured the technician's arm."
    )
    result = predict_risk(sample_text)

    # 1. Pastikan key wajib ada
    assert "predicted_level" in result, "Key 'predicted_level' harus ada dalam hasil"
    assert "confidence" in result, "Key 'confidence' harus ada dalam hasil"
    assert "probabilities" in result, "Key 'probabilities' harus ada dalam hasil"

    # 2. Confidence berada di antara 0 dan 1
    assert 0.0 <= result["confidence"] <= 1.0, (
        f"Confidence harus antara 0 dan 1, didapat {result['confidence']}"
    )

    # 3. Jumlah seluruh probabilitas mendekati 1.0
    total_prob = sum(result["probabilities"].values())
    assert total_prob == pytest.approx(1.0, abs=0.01), (
        f"Jumlah probabilities harus mendekati 1, didapat {total_prob}"
    )

    # 4. predicted_level harus termasuk dalam classes
    classes = result.get("classes", [])
    assert len(classes) == 5, f"Classes harus berjumlah 5 kelas (I-V), didapat: {classes}"
    assert result["predicted_level"] in classes, (
        f"predicted_level '{result['predicted_level']}' harus ada di classes {classes}"
    )


def test_predict_risk_empty_input():
    """Kasus 2: Input kosong ("" dan spasi saja).
    Harus melempar exception ValueError.
    """
    # String kosong murni
    with pytest.raises(ValueError):
        predict_risk("")

    # Hanya spasi
    with pytest.raises(ValueError):
        predict_risk("   ")

    # Karakter whitespace lain (tab & newline)
    with pytest.raises(ValueError):
        predict_risk(" \t \n \r ")


def test_predict_risk_very_long_input():
    """Kasus 3: Input sangat panjang (misalnya 5000 karakter).
    Tidak boleh error dan tetap mengembalikan hasil inferensi yang valid.
    """
    base_phrase = "The maintenance operator inspected the electrical switchboard and circuit breaker. "
    # Ulangi frasa hingga panjang karakter melebihi 5000 karakter
    long_text = base_phrase * (5000 // len(base_phrase) + 5)
    assert len(long_text) >= 5000, f"Panjang teks harus >= 5000, didapat {len(long_text)}"

    result = predict_risk(long_text)

    # Pastikan tidak error dan output tetap terstruktur dengan benar
    assert isinstance(result, dict)
    assert "predicted_level" in result
    assert "confidence" in result
    assert "probabilities" in result
    assert result["predicted_level"] in result["classes"]
    assert 0.0 <= result["confidence"] <= 1.0
    assert sum(result["probabilities"].values()) == pytest.approx(1.0, abs=0.01)
