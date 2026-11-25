# Katalog Dataset Insiden K3 (SOP-GPT)

Direktori ini berisi dataset insiden Keselamatan dan Kesehatan Kerja (K3) industri yang telah dikurasi dan dipersiapkan untuk pelatihan model Machine Learning pada proyek **SOP-GPT** (fitur **Analisis Insiden K3**).

**Penanggung Jawab:** Orang 1 (Data Curator)  
**Terakhir Diperbarui:** 25 November 2026  

---

## 1. Sumber Dataset
- **Nama Dataset:** *Industrial Safety and Health Analytics Database*
- **Penyedia / Sumber:** Kaggle ([IHM Stefanini Industrial Safety and Health Database](https://www.kaggle.com/datasets/ihmstefanini/industrial-safety-and-health-analytics-database))
- **Penyusun Asli:** IHM Stefanini (data riil dari 12 fasilitas manufaktur dan pertambangan di 3 negara).
- **Fitur Kunci:**
  - `Description`: Narasi faktual kronologis insiden kecelakaan kerja atau nyaris celaka (*input feature*).
  - `Potential Accident Level`: Tingkat potensi keparahan kecelakaan (*target label*).

---

## 2. Cara Memperoleh Dataset Mentah
Jika perlu memperbarui atau mengunduh ulang file mentah:

### Cara 1: Menggunakan Kaggle CLI
Pastikan file kredensial `~/.kaggle/kaggle.json` telah dikonfigurasi, lalu jalankan:
```bash
kaggle datasets download -d ihmstefanini/industrial-safety-and-health-analytics-database -p ml/data/raw/ --unzip
```

### Cara 2: Unduhan Manual melalui Browser
1. Buka tautan Kaggle di atas.
2. Unduh arsip zip dataset.
3. Ekstrak file `IHMStefanini_industrial_safety_and_health_database_with_accidents_description.csv` ke dalam direktori:
   ```text
   ml/data/raw/
   ```

---

## 3. Cara Menjalankan Pipeline Pembersihan Data
Untuk menjalankan ulang kurasi data, pembersihan, dan pembagian train/test set terstratifikasi:
```bash
# Dari root repository (SOP_AI/)
python ml/prepare_data.py
```

Skrip ini akan secara otomatis:
1. Memuat CSV mentah dari `ml/data/raw/`.
2. Melakukan audit shape, kolom, dan missing value.
3. Menghapus duplikat teks, memotong spasi liar, dan memetakan label ke romawi I–VI.
4. Menyimpan data bersih ke `ml/data/clean.csv`.
5. Menggabungkan kelas minoritas `VI -> V` untuk memenuhi syarat stratifikasi.
6. Membagi 80/20 secara terstratifikasi (`random_state=42`) dan menyimpan ke `train.csv` serta `test.csv`.

---

## 4. Deskripsi Struktur & Isi Tiap File

```
ml/data/
├── raw/                      # Dataset mentah dari Kaggle
│   ├── IHMStefanini_industrial_safety_and_health_database.csv
│   └── IHMStefanini_industrial_safety_and_health_database_with_accidents_description.csv
├── clean.csv                 # Dataset bersih setelah dedup & sanitasi (411 baris)
├── train.csv                 # Data latih 80% terstratifikasi (328 baris)
├── test.csv                  # Data uji 20% terstratifikasi (83 baris)
├── EDA.md                    # Laporan Exploratory Data Analysis mendalam
└── README.md                 # Dokumentasi katalog dataset ini
```

### Rincian File:

| Nama File | Jumlah Baris | Kolom | Keterangan & Tujuan |
|---|:---:|---|---|
| [`raw/...description.csv`](file:///c:/Users/LOQ/sop_ai/SOP_AI/ml/data/raw/) | 425 baris | 11 kolom | File CSV mentah asli dari Kaggle. Berisi kolom `Description`, `Potential Accident Level`, tanggal, lokasi, sektor industri, dan metadata lain. |
| [`clean.csv`](file:///c:/Users/LOQ/sop_ai/SOP_AI/ml/data/clean.csv) | 411 baris | `description`, `label` | Dataset bersih hasil dedup dan sanitasi spasi. Kolom `label` berisi string Romawi `I`, `II`, `III`, `IV`, `V`, `VI`. |
| [`train.csv`](file:///c:/Users/LOQ/sop_ai/SOP_AI/ml/data/train.csv) | 328 baris | `description`, `label` | Porsi 80% dari dataset untuk pelatihan model (Orang 2 - Model Engineer). Kelas minoritas VI digabungkan ke V agar seimbang. |
| [`test.csv`](file:///c:/Users/LOQ/sop_ai/SOP_AI/ml/data/test.csv) | 83 baris | `description`, `label` | Porsi 20% dari dataset untuk evaluasi model independen (Orang 3 - Evaluator / QA). Distribusi kelas proporsional dengan train set. |
| [`EDA.md`](file:///c:/Users/LOQ/sop_ai/SOP_AI/ml/data/EDA.md) | - | Markdown | Laporan lengkap Exploratory Data Analysis: sebaran kelas, statistik kata/karakter, 5 contoh teks sampel, dan catatan anomali data. |
| [`README.md`](file:///c:/Users/LOQ/sop_ai/SOP_AI/ml/data/README.md) | - | Markdown | Panduan katalog dataset, cara memperoleh data, dan struktur direktori. |

---

## 5. Metadata Skema Data (`clean.csv`, `train.csv`, `test.csv`)

| Nama Kolom | Tipe Data | Deskripsi | Contoh Nilai |
|---|---|---|---|
| `description` | `string` | Teks narasi insiden kecelakaan kerja atau insiden nyaris celaka di lapangan manufaktur/tambang. | *"While removing the drill rod of the Jumbo 08 for maintenance..."* |
| `label` | `string` | Tingkat potensi keparahan kecelakaan terstandarisasi (`I`, `II`, `III`, `IV`, `V`). | `"IV"` |

