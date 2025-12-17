# 🎓 SINTA Cluster Predictor & Simulator

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B)
![Status](https://img.shields.io/badge/Status-Active-success)

## 📋 Tentang Project

Repository ini berisi sekumpulan alat simulasi berbasis **Streamlit** yang dirancang untuk membantu Perguruan Tinggi dalam memprediksi dan mensimulasikan skor SINTA (Science and Technology Index).

Tujuan utama dari alat ini adalah untuk **merancang strategi pemeringkatan**, khususnya untuk membantu universitas menganalisis celah poin yang dibutuhkan agar dapat menempati posisi **Cluster Mandiri**. Dengan alat ini, pengguna dapat memanipulasi variabel input untuk melihat dampaknya terhadap skor total yang telah dinormalisasi.

## 🚀 Fitur & Modul Simulasi

Saat ini, repository menyediakan simulasi perhitungan untuk seluruh komponen utama penilaian SINTA. Setiap modul menghitung **Skor Raw** dan **Skor Ternormalisasi** berdasarkan rumus terbaru.

### 1. 📚 Simulasi Publikasi (`publikasi.py`)
Menghitung skor berdasarkan produktivitas publikasi ilmiah.
* **Indikator:** Artikel Jurnal Internasional (Q1-Q4, Non-Q), Jurnal Nasional (S1-S6), Prosiding, Sitasi, dan Buku.
* **Normalisasi:** Menggunakan pembagi *1776.69*.

### 2. 🔬 Simulasi Research / Penelitian (`research.py`)
Menghitung skor kinerja penelitian dosen.
* **Indikator:** Hibah Luar Negeri, Hibah Eksternal, Hibah Internal, dan Total Dana Penelitian (Rupiah).
* **Normalisasi:** Menggunakan pembagi *261,491.37*.

### 3. 💡 Simulasi HKI (`hki.py`)
Menghitung skor luaran Hak Kekayaan Intelektual.
* **Indikator:** Paten, Paten Sederhana, Hak Cipta, Desain Industri, Perlindungan Varietas Tanaman, dll.
* **Normalisasi:** Menggunakan pembagi *14.7*.

### 4. 🏛️ Simulasi Kelembagaan (`kelembagaan.py`)
Menghitung skor kinerja kelembagaan institusi.
* **Indikator:** Akreditasi Prodi (Unggul/A/Baik Sekali) dan Jumlah Jurnal Terakreditasi.
* **Logika Khusus:** Menerapkan faktor penyesuaian (30%) sebelum normalisasi.
* **Normalisasi:** Menggunakan pembagi *2181.33*.

### 5. 🤝 Simulasi Pengabdian Masyarakat (`abdimas.py`)
Menghitung skor kinerja pengabdian kepada masyarakat (Community Service).
* **Indikator:** Pengabdian Internasional, Nasional, Lokal, dan Jumlah Dana (Juta Rupiah).
* **Normalisasi:** Menggunakan pembagi *447,937.99*.

### 6. 👥 Simulasi SDM (`sdm.py`)
Menghitung skor berdasarkan kualifikasi Sumber Daya Manusia.
* **Indikator:** Reviewer Jurnal (Internasional/Nasional) dan Jabatan Fungsional Dosen (Guru Besar s.d. Non JAFA).
* **Normalisasi:** Menggunakan pembagi *2.443*.

### 7. 🏆 Main Dashboard (`main.py`) - *[STABLE]*
Navigasi terpusat yang menggabungkan seluruh modul di atas untuk melihat prediksi total skor akhir.
* **Status:** *Stable* - Integrasi state antar halaman telah diperbaiki.
* **Fitur:**
  * Navigasi Sidebar dan kalkulasi prediksi cluster
  * Dashboard analisis komprehensif
  * Rekomendasi strategis untuk peningkatan
  * Penyimpanan dan muat data SINTA

---

## 🛠️ Teknologi yang Digunakan

* **[Python](https://www.python.org/)**: Bahasa pemrograman utama.
* **[Streamlit](https://streamlit.io/)**: Framework untuk membuat dashboard interaktif web.
* **[Pandas](https://pandas.pydata.org/)**: Manipulasi data perhitungan.
* **[Plotly Express](https://plotly.com/python/)**: Visualisasi grafik (Pie Chart) interaktif.

---

## 💻 Cara Menjalankan (Installation)

Pastikan Anda sudah menginstall Python. Ikuti langkah berikut:

1.  **Clone Repository**
    ```bash
    git clone https://github.com/Altashfirs/prediksi-sinta.git
    cd prediksi-sinta
    ```

2.  **Install Library yang Dibutuhkan**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Jalankan Aplikasi**
   
    *Dashboard Utama:*
    ```bash
    streamlit run main.py
    ```
---

## 🎯 Fitur Baru & Penyempurnaan

### ✅ **Perbaikan utama:**
- **Data Persistence:** Sistem penyimpanan data yang lebih robust dan konsisten di semua modul
- **Integrasi Halaman:** Perbaikan bug state antar halaman dengan sistem data manager terpusat
- **Cluster Prediction:** Algoritma prediksi cluster lengkap dengan rekomendasi strategis
- **Validasi Data:** Fitur validasi input data untuk memastikan konsistensi
- **Penyimpanan Data:** Fitur simpan dan muat data SINTA untuk analisis berkelanjutan

### ✅ **Fitur lanjutan:**
- **Dashboard Komprehensif:** Analisis menyeluruh dengan visualisasi dan rekomendasi
- **Rencana Peningkatan:** Strategi peningkatan cluster berdasarkan analisis komponen
- **Manajemen Data:** Sistem penyimpanan data yang terintegrasi dan persisten
- **Validasi Input:** Cek otomatis untuk data yang valid dan konsisten

---

## 🔮 Roadmap

- [x] **Simulasi Publikasi**
- [x] **Simulasi Penelitian (Research)**
- [x] **Simulasi HKI**
- [x] **Simulasi Kelembagaan**
- [x] **Simulasi Pengabdian Masyarakat (Community Service)**
- [x] **Simulasi SDM (Sumber Daya Manusia)**
- [x] **Stabilisasi Main Dashboard (`main.py`):** Perbaikan bug integrasi state antar halaman.
- [x] **Prediksi Cluster Lengkap:** Implementasi algoritma prediksi cluster dan rekomendasi strategis.
- [x] **Manajemen Data Terpusat:** Sistem data manager untuk konsistensi dan persistensi.
- [ ] **Ekspor Laporan:** Kemampuan ekspor hasil analisis dalam berbagai format.

---

## 📅 Update Log

**[2025-12-11] - Penyempurnaan Komprehensif**
* ✅ **Fixed:** Integrasi state antar halaman menggunakan sistem data manager terpusat.
* ✅ **Added:** Modul `data_manager.py` untuk manajemen data persisten.
* ✅ **Added:** Modul `cluster_prediction.py` untuk prediksi dan rekomendasi strategis.
* ✅ **Added:** Fitur rekomendasi strategis dan rencana peningkatan cluster.
* ✅ **Added:** Fitur validasi data dan ekspor/muat data SINTA.
* ✅ **Enhanced:** Dashboard utama dengan tampilan dan fungsionalitas lengkap.
* ✅ **Fixed:** Konsistensi input data di semua modul simulasi.

---
## 🤝 Kontribusi

Kontribusi sangat terbuka! Jika Anda memiliki perbaikan untuk `main.py` atau pembaruan rumus, silakan buat *Pull Request* atau buka *Issue*.
