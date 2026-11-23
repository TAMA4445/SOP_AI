# PROSEDUR STANDAR OPERASIONAL (SOP)
## SISTEM PENGENDALIAN ENERGI BERBAHAYA (LOCKOUT / TAGOUT - LOTO)
**Nomor Dokumen:** SOP-K3-LOTO-001  
**Revisi:** 01  
**Tanggal Efektif:** 15 Januari 2026  
**Klasifikasi:** Dokumen Internal Terkendali (K3LH & Pemeliharaan)  
**Target Halaman:** 2 - 5 Halaman PDF Standar ISO 45001 / SMK3  

---

### LEMBAR KONTROL DOKUMEN

| Aktivitas | Nama Pejabat | Jabatan | Tanda Tangan | Tanggal |
|---|---|---|---|---|
| **Disusun Oleh** | Hendra Kusuma, S.T. | Senior Electrical & Automation Engineer | *(Signed)* | 05 Januari 2026 |
| **Ditinjau Oleh** | Ir. Bambang Soedjarwo | HSE & Risk Management Department Head | *(Signed)* | 09 Januari 2026 |
| **Disetujui Oleh** | Raden Mas Arya, M.Eng. | Plant & Manufacturing Operations Director | *(Signed)* | 15 Januari 2026 |

---

### 1. TUJUAN (PURPOSE)
1.1. Menjamin keselamatan, kesehatan, dan perlindungan optimal bagi seluruh teknisi pemeliharaan (*maintenance*), operator produksi, dan personel kontraktor dari bahaya pelepasan energi tidak terduga (*unexpected energization*) atau penyalaan mesin secara mendadak saat perbaikan, penyetelan (*setup*), inspeksi, pembersihan, maupun pembongkaran peralatan.  
1.2. Mencapai dan memverifikasi Kondisi Nol Energi (*Zero Energy State - ZES*) pada seluruh instalasi manufaktur, meliputi energi listrik (hingga 380–690 VAC), mekanik (potensial dan kinetik), hidrolik (hingga tekanan 210 bar), pneumatik (hingga tekanan 7–10 bar), termal (uap steam 165°C pada 6 bar), dan kimiawi.  
1.3. Memenuhi kewajiban perundang-undangan Republik Indonesia dan standar keselamatan internasional, termasuk UU No. 1 Tahun 1970, Permenaker No. 12 Tahun 2015, Permenaker No. 38 Tahun 2016, serta standar teknis OSHA 29 CFR 1910.147 dan ANSI/ASSE Z244.1.

---

### 2. RUANG LINGKUP (SCOPE)
2.1. Prosedur ini berlaku penuh di seluruh area pabrik PT Industri Presisi Nusantara, mencakup:
- **Lini Stamping Press Otomatis** (Unit Aida & Komatsu kapasitas 200–500 Ton).
- **Unit Injection Molding** (Mesin Engel & Sumitomo 150–850 Ton).
- **Lini Robotik Welding & Assembly** (Cell Fanuc & Yaskawa Motoman).
- **Utilitas Pusat Pabrik** (Kompresor Udara Screw Ingersoll Rand 75 kW, Bejana Uap Boiler Miura 2 Ton/Jam, dan Gardu Trafo Listrik 20 kV/380 V).  
2.2. Prosedur ini mencakup semua pekerjaan servis terencana (*Preventive Maintenance*), penanganan kerusakan darurat (*Breakdown Maintenance*), penggantian dies/cetakan mould, penanganan kemacetan material (*jam clearing*), pekerjaan ruang terbatas yang terhubung transmisi fluida, serta modifikasi elektrikal.  
2.3. Pengecualian terbatas: Pekerjaan operasional ringan seperti penggantian mata bor atau pisau potong portabel tidak memerlukan prosedur penuh LOTO ini *hanya jika* steker kabel daya dicabut langsung dari stopkontak dan berada di bawah pengawasan fisik langsung teknisi secara eksklusif.

---

### 3. DEFINISI OPERASIONAL (DEFINITIONS)
3.1. **Lockout (Penguncian Fisik):** Penempatan perangkat pengunci (*padlock*) pada alat pemutus energi (*Energy Isolating Device*) sesuai prosedur tertulis untuk memastikan bahwa alat dan peralatan yang dikendalikan tidak dapat dioperasikan sebelum gembok dibuka.  
3.2. **Tagout (Pelabelan Peringatan):** Pemasangan label peringatan tanda bahaya mencolok (*Danger Tag*) berbahan vinil tahan cuaca yang dikaitkan kuat pada perangkat isolasi energi untuk mengindikasikan bahwa peralatan sedang dikunci dan dilarang dioperasikan.  
3.3. **Zero Energy State (ZES):** Kondisi fisik mutlak di mana semua energi utama telah diputus secara mekanis dan seluruh energi sisa (*residual energy*) yang tersimpan dalam sistem telah dibuang, dinetralisasi, didisipasi, atau ditahan secara mekanis hingga bernilai nol.  
3.4. **Authorized Person (Personel Berwenang):** Karyawan departemen pemeliharaan atau pihak ketiga yang telah lulus asesmen kompetensi internal, memiliki sertifikat resmi LOTO, dan ditunjuk tertulis untuk mengunci dan melabeli peralatan kerja.  
3.5. **Affected Person (Personel Terdampak):** Personel (seperti Operator Produksi, Material Handler, Leader Shift) yang bertugas mengoperasikan peralatan yang sedang diservis atau bekerja di area sekitar mesin yang sedang diisolasi.  
3.6. **Energy Isolating Device (EID):** Sakelar pemutus beban mekanis (*Molded Case Circuit Breaker - MCCB*), sakelar pemisah (*isolator switch*), katup pipa (*ball valve, gate valve, butterfly valve*), sumbat buta (*blind flange*), atau ganjal mekanis (*die safety blocks*). Tombol tekan *Emergency Stop*, sakelar selector PLC, dan sensor interlock pintu **TIDAK TERMASUK** sebagai EID.  
3.7. **Group Lockout Box:** Kotak baja portabel berpemberat ganda yang digunakan untuk menyimpan satu-satunya anak kunci isolasi primer dari berbagai titik pemutus energi dalam proyek multi-disiplin.

---

### 4. PERALATAN DAN ALAT PELINDUNG DIRI (APD)

#### 4.1. Perangkat Keras LOTO Resmi (Standar Master Lock / Brady)
- **Safety Padlock Standar (Master Lock 410 Series):**
  - Warna Merah (Master Lock 410RED): Khusus Teknisi Mekanik & Elektrik internal berlisensi.
  - Warna Biru (Master Lock 410BLU): Khusus Pengawas Operasional / Supervisor Produksi.
  - Warna Kuning (Master Lock 410YLW): Khusus Petugas Keselamatan (HSE Officer).
  - Karakteristik: Kunci bersifat *Keyed-Different* (KD), silinder penahan kunci saat gembok terbuka (*key retaining*), bodi dielektrik non-konduktif tahan benturan dan suhu -57°C hingga +177°C.  
- **Steel Safety Hasp (Brady 1-inch Jaw):** Pengait ganda baja berlapis vinil isolator dengan 6 lubang gembok, memungkinkan hingga 6 personel memasang kunci pengaman secara simultan pada satu titik isolasi.  
- **Clamp-on Circuit Breaker Lockout (Brady No. 65396 & 65397):** Alat pengunci sakelar pemutus sirkuit tegangan 120/277V hingga 480/600V tipe MCCB tanpa memerlukan modifikasi panel.  
- **Rotating Gate Valve Lockout (Master Lock 480–484):** Selubung polimer termoplastik untuk katup ulir diameter pipa 25 mm (1") hingga 330 mm (13").  
- **Ball Valve Lockout (Master Lock S3920):** Pengunci tuas katup bola manual bahan baja nirkarat tahan korosi kimiawi.  
- **Heavy-Duty Danger Tagout:** Label vinil tebal 0,5 mm ukuran 146 mm x 76 mm, berlubang mata ayam kuningan tahan tarikan beban minimal 22,5 kg (50 lbs), memuat teks bilingual, foto teknisi, tanggal instalasi, estimasi durasi pekerjaan, nama unit, dan nomor kontak darurat.  
- **Mechanical Safety Block (Die Block Press):** Blok penopang struktural aluminium die-cast tempa berdaya dukung tekan statis 50 ton dengan kabel interlock kelistrikan mikro ke sirkuit keselamatan kontrol press.  

#### 4.2. Instrumen Pengujian dan Verifikasi Energi
- **Digital Multimeter Industri:** Fluke 87V True-RMS Industrial Multimeter dengan sertifikasi keselamatan CAT IV 600V / CAT III 1000V dan probe berinsulasi ganda TL175.  
- **Non-Contact Voltage Detector:** Fluke 1AC-II VoltAlert (rentang deteksi 90 VAC hingga 1000 VAC).  
- **Manometer Terkalibrasi (Pressure Gauge):** WIKA Model 232.50 bahan stainless steel berisi gliserin dengan sertifikat kalibrasi KAN aktif (rentang ukur 0–25 bar untuk pneumatik, 0–250 bar untuk hidrolik).  
- **Infrared Thermometer:** Testo 830-T2 resolusi optik 12:1 dengan laser marker ganda, rentang ukur -30°C hingga +400°C untuk pemindaian temperatur permukaan pipa steam/oli.  

#### 4.3. Alat Pelindung Diri (APD) Wajib
- Helm Keselamatan (*Safety Helmet*): MSA V-Gard Tipe 1 Kelas E (ketahanan isolasi tegangan hingga 20.000 Volt).  
- Pelindung Mata: Kacamata safety ANSI Z87.1 anti-gores dan anti-kabut dengan pelindung samping (*side shields*).  
- Pelindung Tangan:
  - Pekerjaan Kelistrikan: Sarung tangan karet isolasi dielektrik Kelas 0 (daya tahan uji 1.000V AC) bersertifikat ASTM D120, dilapisi sarung tangan pelindung kulit luar (*leather protector*) goatskin.
  - Pekerjaan Mekanik/Fluida: Sarung tangan sintetis nitril tahan tusuk dan sayatan (ANSI/ISEA 105 Level A4).  
- Sepatu Keselamatan (*Safety Boots*): Bata Industrials Traxx 213 dengan pelindung jari komposit 200 Joule, tahan tusukan sol *Kevlar midsole*, dan berstandar isolasi listrik statis / *Electrical Hazard* (ASTM F2413-18 EH).  
- Arc Flash Protection: Pelindung wajah (*Arc Flash Face Shield*) rating 8 cal/cm² NFPA 70E saat membuka pintu kabinet panel distribusi utama (*Main Distribution Board - MDB*).

---

### 5. PROSEDUR OPERASIONAL TERPERINCI (DETAILED PROCEDURES)

```
[Tahap 1: Persiapan & Izin] ──> [Tahap 2: Notifikasi & Shutdown] ──> [Tahap 3: Isolasi EID]
                                                                            │
                                                                            ▼
[Tahap 6: Pemulihan Energi] <── [Tahap 5: Pekerjaan Servis] <── [Tahap 4: Disipasi & Zero Energy]
```

#### FASE 1: PERSIAPAN DAN NOTIFIKASI
**5.1. Penerbitan Izin Kerja Resmi (Permit to Work):**
- Minimal dua (2) jam sebelum pekerjaan pemeliharaan dimulai, Teknisi Authorized wajib mengisi Formulir Izin Kerja LOTO (Form No: **FRM-K3-LOTO-01**) dan Formulir Izin Kerja Umum (Form No: **FRM-K3-PTW-04**).
- Dokumen harus diserahkan kepada Supervisor Maintenance dan Safety Officer untuk diverifikasi kelengkapan mitigasi risikonya.

**5.2. Analisis Sumber Energi Mesin (*Energy Control Matrix*):**
- Teknisi Authorized mengambil lembar panduan isolasi spesifik mesin (*Machine-Specific LOTO Procedure Plaque*) yang tertempel di sisi kabinet kontrol mesin.
- Contoh pada Mesin Hydraulic Stamping Press 500-Ton Aida (Unit No: **PRS-500-03**), identifikasi 4 sumber energi bahaya:
  1. *Listrik:* 380 VAC, 3-Fasa, 50 Hz pada Panel Breaker **MDB-PRS-03** (arus beban penuh 220 A).
  2. *Pneumatik (Clutch/Brake):* Tekanan udara 6,8 bar pada pipa suplai **PN-LINE-02**.
  3. *Hidrolik (Main Ram):* Tekanan oli 210 bar pada manifold blok katup **HYD-BLK-01**.
  4. *Mekanik Gravitasi:* Berat statis *Slide Ram* 4.500 kg pada posisi titik mati atas (*Top Dead Center - TDC*).

**5.3. Notifikasi Personel Terdampak (*Affected Persons*):**
- Teknisi Authorized menginformasikan Supervisor Produksi dan operator mesin bersangkutan bahwa unit akan dihentikan untuk perbaikan.
- Pasang pita barikade kuning-hitam (*Safety Barricade Tape*) pada radius minimal 3 meter mengelilingi mesin dengan papan informasi bertuliskan: *"AREA DALAM PERBAIKAN - DILARANG MASUK KECUALI PERSONEL BERWENANG"*.

---

#### FASE 2: PENGHENTIAN DAN ISOLASI FISIK (SHUTDOWN & ISOLATION)
**5.4. Penghentian Operasi Normal (Normal Equipment Shutdown):**
- Turunkan kecepatan mesin secara bertahap melalui panel HMI touchscreen ke mode *Jogging*, lalu tekan tombol *Cycle Stop*.
- Tunggu hingga putaran flywheel dan motor utama turun ke 0 RPM. Tekan tombol darurat merah berputar (*Emergency Stop*) pada konsol kontrol.
- Putar sakelar pemilih (*Main Key Selector Switch*) ke posisi "OFF", cabut anak kuncinya, dan simpan di kantung alat teknisi.

**5.5. Isolasi Pemutus Sirkuit Listrik (Electrical Isolation):**
- Kenakan APD lengkap (kacamata, sarung tangan dielektrik, dan helm). Buka pintu panel sub-distribusi daya.
- Pindahkan tuas sakelar utama *Molded Case Circuit Breaker (MCCB)* 380V dari posisi "ON" ke posisi "OFF" dengan gerakan tegas satu kali ayunan.
- Pasang alat pengunci *Brady Clamp-on Circuit Breaker Lockout* pada bilah sakelar, kencangkan baut ibu jari pengunci hingga kokoh, lalu tutup penutup geser alat.
- Masukkan *Steel Safety Hasp* 1-inci pada lubang pengunci.
- Pasang gembok keselamatan merah (*Master Lock 410RED*) milik teknisi pada lubang hasp pertama, kunci gembok hingga berbunyi "klik", lalu cabut anak kuncinya.
- Tempelkan *Danger Tagout* vinil yang telah diisi tinta tahan luntur: Nama: *Hendra Kusuma*, ID: *TECH-882*, Bagian: *Maintenance*, Nomor HP: *0811-9876-XXXX*, Estimasi Selesai: *Pukul 16.00 WIB*.

**5.6. Isolasi Jalur Suplai Fluida (Pneumatik dan Hidrolik):**
- Putar tuas katup bola suplai pneumatik utama (*Main Pneumatic Ball Valve*) 90 derajat searah jarum jam hingga tegak lurus dengan aliran pipa.
- Pasang *Ball Valve Lockout Master Lock S3920* yang menutupi tuas, jepit pengunci pada pipa, dan gembok dengan Padlock Merah dan Tagout.
- Putar handwheel katup gerbang hidrolik (*Gate Valve Isolator*) searah jarum jam hingga tertutup rapat (torsi tangan penuh).
- Pasang cangkang penutup *Rotating Gate Valve Lockout Master Lock 480*, kunci dengan hasp, gembok, dan tagout.

---

#### FASE 3: PELEPASAN DAN PENGENDALIAN ENERGI SISA (DISSIPATION OF STORED ENERGY)
**5.7. Pengurasan Udara Pneumatik Residual:**
- Buka katup pembuangan manual (*exhaust bleed valve*) pada filter-regulator udara di unit FRL (*Filter-Regulator-Lubricator*).
- Amati jarum manometer terkalibrasi WIKA: pastikan jarum tekanan turun secara bertahap dari 6,8 bar hingga mencapai angka tepat **0,00 bar (0 psi)**.
- Biarkan katup pembuangan dalam posisi terbuka penuh (*cracked open*) selama pekerjaan berlangsung untuk mencegah akumulasi tekanan udara balik.

**5.8. Pembuangan Tekanan Hidrolik Akumulator:**
- Buka katup pelepas tekanan solenoid manual (*manual pressure relief valve*) pada sirkuit akumulator piston *Hydac 20 Liter*.
- Arahkan buangan fluida oli ISO VG 46 kembali ke tangki penampung cadangan (*reservoir tank*).
- Pastikan pembacaan tekanan pada manometer blok hidrolik turun dari 210 bar menjadi tepat **0 bar**. Pastikan tidak ada getaran mendesis pada selang fleksibel bertekanan tinggi (*hydraulic hoses*).

**5.9. Pemasangan Ganjal Mekanik Anti-Gravitasi (Die Safety Blocks):**
- Masukkan dua (2) unit *Mechanical Safety Blocks* berbahan aluminium padat berdaya tahan 50 ton di antara dudukan die bagian bawah (*bolster*) dan pelat ram atas press.
- Turunkan ram secara perlahan melalui mekanisme pengoperasian manual (*inch/crank manual*) hingga pelat ram bersandar stabil di atas die block.
- Cabut konektor rantai interlock listrik dari safety block dan pasang gembok keselamatan pada soket bypass interlock mesin.

**5.10. Disipasi Muatan Listrik Kapasitor:**
- Pada panel pengendali inverter (*Variable Frequency Drive - VFD Yaskawa GA700*), muatan kapasitor DC-bus tegangan tinggi tetap tersimpan setelah daya utama mati.
- Tunggu periode disipasi internal (*discharge holding time*) selama minimal **10 menit penuh**.
- Amati lampu indikator LED merah bertanda *"CHARGE"* pada motherboard VFD hingga padam total.

---

#### FASE 4: VERIFIKASI ZERO ENERGY STATE (TESTING & TRYOUT)
Setiap isolasi wajib diverifikasi sebelum bagian tubuh teknisi menyentuh atau masuk ke dalam zona bahaya mesin:

**5.11. Pengujian Ketiadaan Tegangan Listrik (Metode Tiga Langkah: Live-Dead-Live):**
- **Langkah 1 (Live Check):** Atur selektor Fluke 87V ke mode AC Voltage. Uji probe pada sumber stopkontak 220 VAC aktif yang terverifikasi. Pastikan display instrumen menunjukkan angka tegangan hidup (contoh: 224,5 VAC).
- **Langkah 2 (Dead Check):** Masukkan probe multimeter ke terminal beban bawah MCCB yang telah diisolasi. Lakukan pengukuran menyeluruh pada 6 kombinasi kutub:
  - Fase ke Fase: L1–L2, L2–L3, L1–L3 (Harus menunjukkan **0,00 VAC / < 3 Volt induksi residual**).
  - Fase ke Ground: L1–PE, L2–PE, L3–PE (Harus menunjukkan **0,00 VAC**).
- **Langkah 3 (Live Re-Check):** Uji kembali Fluke 87V ke sumber daya aktif yang sama pada Langkah 1 untuk memastikan sekring internal atau kabel probe instrumen tidak putus saat pengujian dilakukan.

**5.12. Uji Coba Pengaktifan Fisik (Physical Tryout Method):**
- Pastikan tidak ada personel di dalam radius berbahaya pergerakan mesin.
- Tekan tombol hijau "POWER START" pada panel kontrol utama mesin dan tahan selama minimal 5 detik.
- Periksa bahwa motor penggerak tidak berputar, konveyor tidak bergerak, dan lampu indikator alarm daya tidak merespons.
- Putar tombol selector lokal dan pedal kaki (*foot pedal*) untuk memastikan tidak ada respons mekanis.
- **PENTING:** Kembalikan semua tombol start/run ke posisi netral/mati ("OFF") segera setelah verifikasi selesai agar mesin tidak langsung menyala saat energi dihubungkan kembali di kemudian hari.

**5.13. Penandatanganan Lembar Verifikasi:**
- Teknisi Authorized, Supervisor Maintenance, dan HSE Officer menandatangani bagian B pada Formulir **FRM-K3-LOTO-01** yang menyatakan bahwa mesin secara sah telah mencapai *Zero Energy State*.

---

#### FASE 5: SISTEM KUNCI KELOMPOK (GROUP LOCKOUT)
Apabila pekerjaan pemeliharaan melibatkan multi-disiplin ilmu (Mekanik, Elektrik, Otomasi) atau tim kontraktor luar:
5.14. Setiap titik isolasi primer dipasang satu gembok isolasi terpusat.  
5.15. Seluruh anak kunci dari gembok-gembok isolasi primer tersebut dimasukkan ke dalam *Portable Group Lockout Box (Master Lock S1010)*.  
5.16. Setiap personel teknisi pelaksana (tanpa terkecuali) wajib mengaitkan gembok keselamatan pribadinya (*Personal Padlock*) pada lubang pengaman luar kotak group box.  
5.17. Kotak group box tidak akan bisa dibuka untuk mengambil kunci isolasi primer selama masih ada satu orang teknisi yang memasang gembok pribadinya di luar kotak.

---

#### FASE 6: PELEPASAN LOTO DAN NORMALISASI ENERGI (RESTORATION PROCEDURE)
Setelah seluruh pekerjaan servis, perakitan, dan inspeksi selesai dilakukan:

**5.18. Pemeriksaan Area dan Housekeeping Mesin:**
- Periksa bagian dalam mesin: singkirkan seluruh perkakas kerja, dongkrak portabel, kabel tester, kain majun (*cleaning rags*), dan komponen bekas penggantian.
- Pasang kembali semua penutup pengaman (*machine guarding*), jeruji pelindung (*interlock mesh guard*), dan sensor tirai cahaya (*light curtain safety sensor*). Pastikan baut struktural telah dikencangkan sesuai torsi standar pabrikan.
- Lepaskan *Die Safety Blocks* aluminium penahan ram press dan kembalikan ke gantungan dinding resminya. Sambungkan kembali kabel interlock pengamannya.

**5.19. Verifikasi Keberadaan Personel (Head Count & Clearance):**
- Lakukan penyisiran fisik di sekeliling mesin. Pastikan seluruh kru teknisi dan kontraktor telah berada di luar zona jangkauan mesin (zona aman dengan jarak minimum 1,5 meter dari komponen bergerak).

**5.20. Pelepasan Gembok dan Label (Padlock & Tag Removal):**
- Setiap teknisi pelaksana melepaskan gembok keselamatan pribadi dan label miliknya sendiri dari peralatan atau kotak group box.  
- **DILARANG KERAS** melepas gembok milik personel lain dalam situasi biasa.

**5.21. Prosedur Darurat Pelepasan Gembok Paksa (*Emergency Lock Removal Procedure*):**
- Jika seorang teknisi berhalangan hadir atau pulang meninggalkan pabrik dengan gembok masih terpasang pada mesin:
  1. Supervisor Maintenance wajib menelepon dan mengonfirmasi secara verbal bahwa teknisi tersebut telah berada di luar area pabrik dan selamat.
  2. Apabila tidak dapat dihubungi, Supervisor bersama Safety Officer wajib melakukan pencarian fisik menyeluruh di seluruh area pabrik untuk memastikan yang bersangkutan tidak berada di area bahaya.
  3. Pengisian Formulir Pelepasan Kunci Darurat (Form No: **FRM-K3-LOTO-03**).
  4. Pemotongan gembok dengan gunting beton hidrolik (*bolt cutter*) hanya boleh dieksekusi setelah mendapatkan otorisasi tanda tangan basah langsung dari **Plant & Manufacturing Operations Director**.
  5. Teknisi yang bersangkutan harus diwawancarai dan diberikan pembinaan K3 sebelum diizinkan bekerja kembali pada shift berikutnya.

**5.22. Pemberitahuan Operasi dan Pemberian Energi Bertahap (*Energizing Sequence*):**
- Beritahukan kepada Supervisor Produksi bahwa mesin siap dialiri energi kembali.
- Lepas *Breaker Lockout*, naikkan tuas MCCB listrik ke posisi "ON".
- Buka katup hidrolik utama.
- Buka katup isolasi pneumatik secara perlahan (*slow ramp-up*) selama 30 detik untuk menghindari lonjakan tekanan tiba-tiba (*pneumatic hammer shock*) yang dapat merusak seal silinder.
- Lakukan pengujian jalan tanpa beban (*dry run test*) selama minimal 3–5 menit di bawah pengawasan bersama Tim Pemeliharaan dan Tim Produksi.
- Tanda tangani Formulir Berita Acara Serah Terima Mesin (Form No: **FRM-MNT-WR-12**).

---

### 6. TANGGUNG JAWAB (ROLES & RESPONSIBILITIES)

| Peran / Jabatan | Tanggung Jawab Utama K3L & Operasional |
|---|---|
| **Plant Director** | Memberikan komitmen anggaran untuk penyediaan perangkat LOTO berkualitas, menyetujui kebijakan prosedur K3 level korporat, dan mengevaluasi laporan insiden fatalitas / *near-miss*. |
| **HSE & Risk Management Head** | Melakukan audit kepatuhan implementasi LOTO secara komprehensif setiap enam (6) bulan sekali, menyelenggarakan program sertifikasi/resertifikasi tahunan personel berwenang, dan memelihara dokumentasi formulir kepatuhan. |
| **Maintenance Dept. Head** | Memastikan ketersediaan dan kalibrasi rutin seluruh perangkat LOTO, gembok terstandarisasi, dan instrumen uji (multimeter, manometer). Menetapkan jadwal *Preventive Maintenance* yang memprioritaskan keselamatan kerja. |
| **Supervisor Maintenance (Mek/Elk)** | Melakukan verifikasi lapangan, menerbitkan dan menandatangani izin kerja LOTO (**FRM-K3-LOTO-01**), memastikan pengujian *Live-Dead-Live* dilakukan dengan benar, serta memimpin penanganan *Group Lockout*. |
| **Authorized Person (Teknisi K3/MNT)** | Mematuhi seluruh butir prosedur operasional, menjaga kunci gembok pribadi (tidak menduplikasi atau menyerahkan kunci kepada siapapun), melakukan verifikasi *Zero Energy State*, dan merapikan area kerja usai servis. |
| **Production Shift Supervisor** | Menolak pengoperasian mesin yang belum selesai proses pemeliharaannya atau belum dilepas LOTO-nya secara resmi, mengatur jadwal produksi saat mesin diisolasi, serta mengawasi operator. |
| **Affected Person (Operator Produksi)** | Dilarang memanipulasi, memaksa berputar, atau membuka gembok dan label LOTO yang terpasang pada mesin. Wajib segera melapor ke atasan jika melihat indikasi kebocoran energi atau gembok rusak. |

---

### 7. REFERENSI REGULASI DAN STANDAR TEKNIS (REFERENCES)
7.1. **Undang-Undang Republik Indonesia No. 1 Tahun 1970** tentang Keselamatan Kerja (Lembaran Negara No. 1 Tahun 1970).  
7.2. **Peraturan Menteri Tenaga Kerja RI No. Per.08/MEN/VII/2010** tentang Alat Pelindung Diri.  
7.3. **Peraturan Menteri Ketenagakerjaan RI No. 12 Tahun 2015** tentang Keselamatan dan Kesehatan Kerja Listrik di Tempat Kerja.  
7.4. **Peraturan Menteri Ketenagakerjaan RI No. 38 Tahun 2016** tentang Keselamatan dan Kesehatan Kerja Pesawat Tenaga dan Produksi.  
7.5. **Standar Nasional Indonesia SNI 0225:2020:** Persyaratan Umum Instalasi Listrik 2020 (PUIL 2020) Bagian 1 & 4.  
7.6. **Occupational Safety and Health Administration (OSHA):** 29 CFR 1910.147 - *The Control of Hazardous Energy (Lockout/Tagout)*, General Industry Standards, United States Department of Labor.  
7.7. **American National Standards Institute (ANSI):** ANSI/ASSP Z244.1-2016 (R2020) - *The Control of Hazardous Energy: Lockout, Tagout and Alternative Methods*.  
7.8. **International Electrotechnical Commission (IEC):** IEC 60204-1 (2016) - *Safety of Machinery - Electrical Equipment of Machines - Part 1: General Requirements*.

---

### 8. CATATAN REVISI DAN RIWAYAT DOKUMEN (REVISION HISTORY)

| No. Rev. | Tanggal Terbit | Bagian / Klausul | Uraian Perubahan | Disusun Oleh | Disetujui Oleh |
|---|---|---|---|---|---|
| **00** | 10 Juni 2023 | Semua Dokumen | Penerbitan perdana prosedur keselamatan Lockout/Tagout untuk fasilitas baru pabrik. | Tim K3 Internal | Ir. Bambang S. |
| **01** | 15 Januari 2026 | Klausul 4, 5, dan 7 | 1. Integrasi metode verifikasi listrik tiga langkah (*Live-Dead-Live*) menggunakan instrumen Fluke CAT IV.<br>2. Standardisasi perangkat isolasi wajib Master Lock 410 Series *Keyed-Different* dan ganjal mekanik 50 ton.<br>3. Pembaruan klausul acuan ke regulasi terbaru PUIL 2020 dan ANSI Z244.1-2020.<br>4. Penambahan prosedur pelepasan gembok paksa darurat (*Emergency Lock Removal*) form **FRM-K3-LOTO-03**. | Hendra Kusuma | R.M. Arya |

---

### LAMPIRAN: DAFTAR FORMULIR DAN LOGBOOK TERKAIT
1. **FRM-K3-LOTO-01:** Formulir Permohonan Izin Kerja dan Checklist Verifikasi Zero Energy State (LOTO Permit).  
2. **FRM-K3-PTW-04:** Formulir Izin Kerja Umum Risiko Tinggi (*General High-Risk Permit to Work*).  
3. **FRM-K3-LOTO-03:** Berita Acara Otorisasi Pelepasan Gembok Darurat (*Emergency Lock Removal Form*).  
4. **FRM-MNT-WR-12:** Formulir Serah Terima dan Hasil Uji Jalan Komisioning Mesin (*Handover & Commissioning Log*).  
5. **LOG-K3-LOTO-00:** Buku Log Peminjaman dan Penyerahan Gembok Stasiun LOTO Induk (*Master Lockout Station Registry*).

