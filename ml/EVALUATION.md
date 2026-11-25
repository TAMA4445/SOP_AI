# Evaluasi Model Prediksi Level Insiden K3

**Model:** TF-IDF (ngram 1-2, sublinear TF) + Random Forest (250 pohon, class_weight balanced)
**Data:** train 328 baris, test 83 baris
**Kelas:** I sampai V (level VI pada data asli digabung ke V saat pembersihan data)
**Artefak:** `ml/model.joblib` | **Fungsi:** `ml/predict.py` -> `predict_risk()`
**Evaluasi:** `ml/evaluate.py` -> `ml/reports/metrics.json` dan `confusion_matrix.png`

## Cara Pembuatan Model
Hanya satu konfigurasi yang dilatih, yaitu TF-IDF + Random Forest. Tidak ada
perbandingan dengan algoritma lain, tidak ada cross-validation, dan tidak ada
pencarian hyperparameter. Dengan demikian angka pada test set tidak dipakai
untuk memilih atau menyetel model, tetapi juga belum ada bukti bahwa Random
Forest adalah pilihan terbaik untuk data ini.

## Hasil di Test Set (83 baris)

| Metrik | Model | Baseline (selalu tebak IV) |
|---|---|---|
| Accuracy | 0.434 | 0.337 |
| F1 macro | 0.447 | 0.101 |
| Akurasi dalam toleransi +-1 level | 0.759 | - |

Model lebih baik dari baseline, tetapi data uji hanya 83 baris sehingga selisih
ini belum stabil secara statistik.

## Hasil per Kelas

| Level | Jumlah uji | Recall | F1 baseline | F1 model |
|---|---|---|---|---|
| I | 9 | 0.56 | 0.000 | 0.714 |
| II | 19 | 0.63 | 0.000 | 0.471 |
| III | 21 | 0.38 | 0.000 | 0.340 |
| IV | 28 | 0.36 | 0.505 | 0.426 (turun dari baseline) |
| V | 6 | 0.17 | 0.000 | 0.286 |

## Confusion Matrix (baris = aktual, kolom = prediksi)

|  | Pred I | Pred II | Pred III | Pred IV | Pred V |
|---|---|---|---|---|---|
| Aktual I | 5 | 0 | 3 | 1 | 0 |
| Aktual II | 0 | 12 | 4 | 3 | 0 |
| Aktual III | 0 | 10 | 8 | 3 | 0 |
| Aktual IV | 0 | 10 | 8 | 10 | 0 |
| Aktual V | 0 | 0 | 3 | 2 | 1 |

## Catatan Penting
- **Level V hanya terdeteksi 1 dari 6 kasus (recall 17%).** Kasus pada level
  tertinggi banyak terlewat. F1 0.286 berasal dari satu tebakan benar.
- Level IV justru turun F1-nya dibanding baseline.
- Akurasi +-1 level (75.9%) berarti prediksi sering meleset maksimal satu
  tingkat, bukan salah jauh. Ini relevan karena level berurutan.

## Keterbatasan
- Data kecil (328 latih, 83 uji); kelas V hanya 23 data latih.
- Kelas tidak seimbang; hasil per kelas naik-turun antar pembagian data.
- Hanya satu model yang dicoba, tanpa validasi silang.
- Input berbahasa Inggris (sesuai dataset).
- Hasil bersifat indikatif dan **bukan pengganti penilaian ahli K3**.
