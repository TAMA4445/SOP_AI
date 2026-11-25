# Exploratory Data Analysis (EDA) - Dataset Insiden K3

**Proyek:** SOP-GPT  
**Fitur:** Analisis Insiden K3 (Machine Learning Classification)  
**Peran:** Orang 1 (Data Curator)  
**Dokumen:** `ml/data/EDA.md`  
**Dataset Terkurasi:** `ml/data/clean.csv` (411 baris)  

---

## 1. Ringkasan Eksekutif
Eksplorasi data ini bertujuan untuk memetakan karakteristik teks deskripsi insiden kerja dan sebaran target klasifikasi **Potential Accident Level** (tingkat keparahan potensi kecelakaan kerja). Data berasal dari database operasional industri manufaktur dan pertambangan multi-nasional (IHM Stefanini).

Setelah proses kurasi (penghapusan 14 baris duplikat, normalisasi whitespace, dan filtering teks kosong), dataset bersih memiliki **411 sampel unik**.

---

## 2. Distribusi Kelas (Potential Accident Level)

Tingkat potensi kecelakaan diklasifikasikan dari skala **I (Paling Ringan)** hingga **VI (Paling Parah / Fatal)**:

| Label Tingkat | Jumlah Sampel | Persentase (%) | Interpretasi Risiko K3 |
|:---:|:---:|:---:|:---|
| **I** | 43 | 10.46% | Hampir Celaka (*Near Miss*) / Potensi cedera pertolongan pertama (P3K ringan). |
| **II** | 95 | 23.11% | Potensi cedera ringan dengan perawatan medis tanpa hari kerja hilang (*Minor Medical*). |
| **III** | 106 | 25.79% | Potensi cedera sedang yang menyebabkan hari kerja hilang terbatas (*Restricted Work*). |
| **IV** | 138 | 33.58% | Potensi cedera berat dengan kehilangan hari kerja permanen / cacat fungsi (*Lost Time Injury*). |
| **V** | 28 | 6.81% | Potensi cedera fatalitas tunggal / kerusakan aset skala masif (*Critical / Fatality Risk*). |
| **VI** | 1 | 0.24% | Potensi insiden katastropik multi-fatalitas (*Catastrophic Disaster*). |
| **TOTAL** | **411** | **100.00%** | |

### Visualisasi Distribusi Sampel:
```text
IV  [138] ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■ 33.58%
III [106] ■■■■■■■■■■■■■■■■■■■■■■■■■■ 25.79%
II  [95]  ■■■■■■■■■■■■■■■■■■■■■■■■ 23.11%
I   [43]  ■■■■■■■■■■■ 10.46%
V   [28]  ■■■■■■■ 6.81%
VI  [1]   ▏ 0.24%
```

---

## 3. Karakteristik Panjang Deskripsi (Text Length Statistics)

Statistik panjang teks deskripsi insiden dihitung berdasarkan jumlah karakter dan jumlah kata:

| Metrik | Panjang Karakter | Panjang Kata |
|:---|:---:|:---:|
| **Rata-rata (Mean)** | **363.40** | **64.72** |
| **Median (Nilai Tengah)** | **331.00** | **60.00** |
| **Minimum** | 94 | 16 |
| **Maksimum** | 1,029 | 183 |
| **Standar Deviasi (Std)** | 176.74 | 31.92 |

### Panjang Rata-rata per Kelas Tingkat Keparahan:
- **Kelas I:** Rata-rata 74.7 kata (424.6 karakter)
- **Kelas II:** Rata-rata 53.4 kata (297.2 karakter)
- **Kelas III:** Rata-rata 54.1 kata (304.6 karakter)
- **Kelas IV:** Rata-rata 73.6 kata (413.3 karakter)
- **Kelas V:** Rata-rata 83.8 kata (469.6 karakter)
- **Kelas VI:** Rata-rata 73.0 kata (395.0 karakter)

> **Observasi:** Insiden dengan potensi risiko tinggi (Kelas IV, V, dan VI) cenderung memiliki narasi laporan investigasi yang lebih panjang dan detail karena melibatkan investigasi formal lintas bagian.

---

## 4. 5 Contoh Sampel Deskripsi Insiden

Berikut adalah 5 contoh representatif teks deskripsi dari berbagai tingkat keparahan:

### Contoh 1 - Label: `I` (Potensi Ringan / Ergonomi Kunci Perkakas)
> *"Being 9:45 am. approximately in the Nv. 1880 CX-695 OB7, the personnel begins the task of unlocking the Soquet bolts of the BHB machine, when they were in the penultimate bolt they identified that the hexagonal head was worn, proceeding Mr. Cristóbal - Auxiliary assistant to climb to the platform to exert pressure with your hand on the "DADO" key, to prevent it from coming out of the bolt; in those moments two collaborators rotate with the lever in anti-clockwise direction, leaving the key of the bolt, hitting the palm of the left hand, causing the injury."*

### Contoh 2 - Label: `II` (Percikan Cairan Kimia ke APD Mata)
> *"At the moment the forklift operator went to manipulate big bag of bioxide in section 70 and just in front of the ladder that leads to the area of ​​manual displacement, he splashed spent at the height of his forehead from a fissure in pipe G -069, subsequently spilling to his left eye. The collaborator went to the nearby eyewash for cleaning and immediately to the medical center."*

### Contoh 3 - Label: `III` (Pekerjaan Penggalian & Benturan Perkakas Manual)
> *"In the sub-station MILPO located at level +170 when the collaborator was doing the excavation work with a pick (hand tool), hitting a rock with the flat part of the beak, it bounces off hitting the steel tip of the safety shoe and then the metatarsal area of ​​the left foot of the collaborator causing the injury."*

### Contoh 4 - Label: `IV` (Penjepitan Jari pada Lini Mesin Bor Jumbo)
> *"While removing the drill rod of the Jumbo 08 for maintenance, the supervisor proceeds to loosen the support of the intermediate centralizer to facilitate the removal, seeing this the mechanic supports one end on the drill of the equipment to pull with both hands the bar and accelerate the removal from this, at this moment the bar slides from its point of support and tightens the fingers of the mechanic between the drilling bar and the beam of the jumbo."*

### Contoh 5 - Label: `V` (Arc Flash / Hubungan Singkat Kelistrikan 440V 400A)
> *"In moments that the operator of the Jumbo 2, tried energize your equipment to proceed to the installation of 4 split set at intersection 544 of Nv 3300, remove the lock and opening the electric board of 440V and 400A, and when lifting the thermomagnetic key This makes phase to ground - phase contact with the panel shell - producing a flash which reaches the operator causing the injury described."*

---

## 5. Catatan Masalah Data & Mitigasi Kurasi (Data Quality Issues)

Selama proses inspeksi dan kurasi data, ditemukan beberapa anomali kualitas data yang perlu diperhatikan oleh tim Machine Learning:

1. **Ketimpangan Kelas Ekstrem (*Severe Class Imbalance*):**
   - Kelas IV, III, dan II mendominasi lebih dari **82.4%** keseluruhan dataset.
   - Kelas V hanya 6.81% (28 sampel), dan Kelas VI hanya 0.24% (1 sampel).
   - *Rekomendasi Pemodelan:* Gunakan *class weighting* (`class_weight='balanced'`), algoritma focal loss, atau metrik evaluasi seperti **Macro-F1 Score** daripada sekadar Akurasi.

2. **Kendala Stratifikasi Kelas Tunggal (*Single-Sample Class VI*):**
   - Kelas VI hanya memiliki tepat 1 sampel dalam dataset mentah.
   - Algoritma `train_test_split(stratify=...)` memerlukan minimal 2 anggota per kelas agar dapat membagi secara proporsional.
   - *Keputusan Kurasi:* Sampel kelas VI digabungkan ke kelas terdekat **V** untuk pembentukan `train.csv` dan `test.csv`. Keputusan ini tepat secara domain industri karena kedua kelas merepresentasikan insiden berisiko fatal/katastropik (*high-severity events*).

3. **Duplikasi Data dan Label Ambigu (*Duplicate & Conflicting Labels*):**
   - Ditemukan **14 baris duplikat** pada dataset mentah (misalnya insiden di hopper OP5 tercatat 3 kali).
   - Terdapat **1 kasus kontradiksi label**: Deskripsi mengenai insiden truk MAPERU bernomor plat F1T 878 memiliki 2 baris dengan label berbeda (satu diberi label `IV`, satu lagi diberi label `V`).
   - *Mitigasi:* Duplikasi telah dibersihkan dengan mempertahankan entri pertama unik pada `clean.csv`.

4. **Karakteristik Linguistik & Kosakata Campuran:**
   - Dataset merupakan terjemahan dokumen investigasi lapangan industri tambang di Amerika Latin (Brasil/Peru).
   - Terdapat istilah teknis campuran bahasa Portugis/Spanyol seperti *"chuteo"*, *"colaborador"*, *"DADO key"*, serta kode lokasi tambang seperti *"Nv. 1880 CX-695"*.
   - *Rekomendasi Tokenisasi:* Gunakan subword tokenizer (seperti BPE/WordPiece pada BERT/RoBERTa) atau TF-IDF dengan n-gram karakter untuk menangkap istilah khusus ini.

5. **Panjang Teks Maksimum (Max Sequence Length):**
   - Deskripsi terpanjang mencapai 183 kata (~1.029 karakter).
   - Untuk model klasifikasi berbasis Transformer/LLM embedding, panjang sequence `max_length = 256` token sudah mencakup 100% informasi tanpa pemotongan (*truncation*).

