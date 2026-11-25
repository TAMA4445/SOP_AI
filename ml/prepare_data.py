#!/usr/bin/env python3
"""
ml/prepare_data.py
Modul Kurasi dan Penyiapan Data Insiden K3 (SOP-GPT - Analisis Insiden K3).
Penanggung Jawab: Orang 1 (Data Curator)

Tugas:
1. Memuat CSV dataset dari ml/data/raw/ (Kaggle: Industrial Safety and Health Analytics Database).
2. Menampilkan dimensi data (shape), nama kolom, dan jumlah missing value per kolom.
3. Membersihkan data:
   - Strip whitespace pada nama kolom.
   - Hapus duplikat deskripsi.
   - Hapus entri Description yang kosong.
   - Rapikan spasi ganda / whitespace berlebih.
4. Memetakan label 'Potential Accident Level' ke representasi string standar 'I' sampai 'VI'.
5. Menyimpan data bersih ke ml/data/clean.csv (kolom: description, label).
6. Menangani kelas minoritas (< 2 sampel) dengan penggabungan ke kelas terdekat (VI -> V)
   agar dapat dilakukan stratifikasi data.
7. Membagi dataset 80/20 secara terstratifikasi (stratify=label, random_state=42),
   lalu menyimpan ke ml/data/train.csv dan ml/data/test.csv.
"""

import sys
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split


# Standardisasi pemetaan label Potential Accident Level ke string romawi I - VI
LABEL_MAPPING = {
    "I": "I",
    "II": "II",
    "III": "III",
    "IV": "IV",
    "V": "V",
    "VI": "VI",
    1: "I",
    2: "II",
    3: "III",
    4: "IV",
    5: "V",
    6: "VI",
    "1": "I",
    "2": "II",
    "3": "III",
    "4": "IV",
    "5": "V",
    "6": "VI",
}


def find_raw_csv_path(raw_dir: Path) -> Path:
    """Mencari file CSV mentah yang memuat kolom Description."""
    preferred = raw_dir / "IHMStefanini_industrial_safety_and_health_database_with_accidents_description.csv"
    if preferred.exists():
        return preferred
    
    # Fallback jika nama file berbeda
    csv_candidates = list(raw_dir.glob("*.csv"))
    for candidate in csv_candidates:
        with open(candidate, "r", encoding="utf-8", errors="replace") as f:
            first_line = f.readline()
            if "Description" in first_line:
                return candidate
                
    if csv_candidates:
        return csv_candidates[0]
        
    raise FileNotFoundError(f"Tidak ditemukan file CSV di folder: {raw_dir}")


def load_raw_data(file_path: Path) -> pd.DataFrame:
    """Memuat CSV mentah dan mencetak inspeksi awal."""
    print("=" * 70)
    print("1. MEMUAT DATASET RAW")
    print("=" * 70)
    print(f"Sumber file: {file_path}")
    
    df = pd.read_csv(file_path)
    # Strip spasi pada nama kolom
    df.columns = df.columns.str.strip()
    
    print(f"\n[Shape Data Awal]: {df.shape[0]} baris, {df.shape[1]} kolom")
    print(f"[Daftar Kolom]: {list(df.columns)}")
    
    print("\n[Jumlah Missing Value per Kolom]:")
    missing_counts = df.isna().sum()
    for col, count in missing_counts.items():
        print(f"  - {col or '(Unnamed Index)'}: {count} missing ({count / len(df) * 100:.2f}%)")
        
    return df


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Membersihkan dataset: teks, spasi, duplikat, dan standardisasi label."""
    print("\n" + "=" * 70)
    print("2. PEMBERSIHAN DATA (DATA CLEANING)")
    print("=" * 70)
    
    initial_count = len(df)
    
    # Validasi keberadaan kolom input & target
    input_col = "Description"
    target_col = "Potential Accident Level"
    
    if input_col not in df.columns or target_col not in df.columns:
        raise KeyError(f"Kolom wajib '{input_col}' atau '{target_col}' tidak ditemukan.")
    
    # 1. Hapus nilai Description kosong / NaN
    df_clean = df.dropna(subset=[input_col, target_col]).copy()
    dropped_nan = initial_count - len(df_clean)
    print(f"[Filter NaN]: {dropped_nan} baris dengan nilai kosong dihapus.")
    
    # 2. Rapikan spasi berlebih pada Description
    df_clean["description"] = (
        df_clean[input_col]
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )
    
    # Hapus jika hasil strip adalah string kosong
    df_clean = df_clean[df_clean["description"] != ""].copy()
    
    # 3. Standardisasi label Potential Accident Level ke string Romawi I - VI
    raw_labels = df_clean[target_col].astype(str).str.strip()
    df_clean["label"] = raw_labels.map(LABEL_MAPPING)
    
    unmapped = df_clean["label"].isna().sum()
    if unmapped > 0:
        print(f"[Peringatan]: {unmapped} baris label tidak dapat dipetakan ke I-VI, baris dihapus.")
        df_clean = df_clean.dropna(subset=["label"]).copy()
    
    # Ambil hanya kolom description dan label
    df_curated = df_clean[["description", "label"]].copy()
    
    # 4. Hapus duplikat berdasarkan teks deskripsi
    before_dedup = len(df_curated)
    df_curated = df_curated.drop_duplicates(subset=["description"]).reset_index(drop=True)
    duplicates_removed = before_dedup - len(df_curated)
    print(f"[Hapus Duplikat]: {duplicates_removed} baris duplikat deskripsi dihapus.")
    
    print(f"\n[Hasil Bersih]: {len(df_curated)} baris unik tersisa (dari {initial_count} baris awal).")
    print("\n[Distribusi Label pada Data Bersih]:")
    label_dist = df_curated["label"].value_counts().sort_index()
    for lbl, cnt in label_dist.items():
        print(f"  - Tingkat {lbl}: {cnt} insiden ({cnt / len(df_curated) * 100:.2f}%)")
        
    return df_curated


def split_and_save(
    df_clean: pd.DataFrame,
    clean_path: Path,
    train_path: Path,
    test_path: Path,
    test_size: float = 0.20,
    random_state: int = 42
):
    """
    Menyimpan clean.csv, menangani kelas minoritas (< 2 sampel),
    melakukan stratified 80/20 train/test split, dan menyimpan hasilnya.
    """
    print("\n" + "=" * 70)
    print("3. PENYIMPANAN DATA BERSIH & STRATIFIED SPLIT (80/20)")
    print("=" * 70)
    
    # Simpan clean.csv terlebih dahulu
    clean_path.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(clean_path, index=False, encoding="utf-8")
    print(f"[Disimpan]: Data bersih -> {clean_path} ({len(df_clean)} baris)")
    
    # Analisis frekuensi kelas untuk syarat stratifikasi
    counts = df_clean["label"].value_counts()
    print("\n[Pemeriksaan Syarat Stratifikasi (Sampel per Kelas >= 2)]:")
    rare_classes = counts[counts < 2].index.tolist()
    
    df_for_split = df_clean.copy()
    
    if rare_classes:
        print(f"  Peringatan: Ditemukan kelas dengan sampel < 2: {rare_classes}")
        for rare in rare_classes:
            cnt = counts[rare]
            if rare == "VI":
                target_merge = "V"
            else:
                # Fallback penggabungan kelas terdekat numerik
                target_merge = "V"
                
            print(f"  [Keputusan Kurasi]: Kelas '{rare}' (jumlah = {cnt}) digabungkan ke kelas terdekat '{target_merge}'.")
            print(f"                     Alasan: Algoritma stratifikasi train_test_split mensyaratkan setiap kelas")
            print(f"                     memiliki minimal 2 anggota agar dapat terdistribusi ke train dan test set.")
            
            df_for_split["label"] = df_for_split["label"].replace({rare: target_merge})
    else:
        print("  Semua kelas memiliki >= 2 sampel, tidak diperlukan penggabungan kelas.")
        
    # Lakukan Stratified Train/Test Split (80/20)
    train_df, test_df = train_test_split(
        df_for_split,
        test_size=test_size,
        stratify=df_for_split["label"],
        random_state=random_state
    )
    
    # Reset index
    train_df = train_df.reset_index(drop=True)
    test_df = test_df.reset_index(drop=True)
    
    # Simpan train.csv dan test.csv
    train_df.to_csv(train_path, index=False, encoding="utf-8")
    test_df.to_csv(test_path, index=False, encoding="utf-8")
    
    print(f"\n[Disimpan]: Data Latih (Train) -> {train_path} ({len(train_df)} baris - {len(train_df)/len(df_for_split)*100:.1f}%)")
    print(f"[Disimpan]: Data Uji (Test)    -> {test_path} ({len(test_df)} baris - {len(test_df)/len(df_for_split)*100:.1f}%)")
    
    print("\n[Distribusi Kelas Train Set]:")
    for lbl, cnt in train_df["label"].value_counts().sort_index().items():
        print(f"  - Kelas {lbl}: {cnt} ({cnt / len(train_df) * 100:.2f}%)")
        
    print("\n[Distribusi Kelas Test Set]:")
    for lbl, cnt in test_df["label"].value_counts().sort_index().items():
        print(f"  - Kelas {lbl}: {cnt} ({cnt / len(test_df) * 100:.2f}%)")
        
    return train_df, test_df


def main():
    base_dir = Path(__file__).resolve().parent
    data_dir = base_dir / "data"
    raw_dir = data_dir / "raw"
    
    raw_file = find_raw_csv_path(raw_dir)
    clean_file = data_dir / "clean.csv"
    train_file = data_dir / "train.csv"
    test_file = data_dir / "test.csv"
    
    # 1. Load data
    df_raw = load_raw_data(raw_file)
    
    # 2. Clean data & map labels
    df_clean = clean_dataset(df_raw)
    
    # 3. Save clean and split data
    train_df, test_df = split_and_save(
        df_clean=df_clean,
        clean_path=clean_file,
        train_path=train_file,
        test_path=test_file,
        test_size=0.20,
        random_state=42
    )
    
    print("\n" + "=" * 70)
    print("PROSES KURASI SELESAI DENGAN SUKSES!")
    print("=" * 70)


if __name__ == "__main__":
    main()

