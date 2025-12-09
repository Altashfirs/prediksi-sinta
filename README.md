# 🎓 SINTA Cluster Predictor & Simulator

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B)
![Status](https://img.shields.io/badge/Status-Active-success)

## 📋 Tentang Project

Repository ini berisi sekumpulan alat simulasi berbasis **Streamlit** yang dirancang untuk membantu Perguruan Tinggi dalam memprediksi dan mensimulasikan skor SINTA (Science and Technology Index).

Tujuan utama dari alat ini adalah untuk **merancang strategi pemeringkatan**, khususnya untuk membantu universitas menganalisis celah poin yang dibutuhkan agar dapat menempati posisi **Cluster Mandiri**. Dengan alat ini, pengguna dapat memanipulasi variabel input (seperti jumlah publikasi, hibah penelitian, atau HKI) untuk melihat dampaknya terhadap skor total yang telah dinormalisasi.

## 🚀 Fitur & Modul Simulasi

Saat ini, repository menyediakan simulasi perhitungan untuk 4 komponen utama penilaian SINTA. Setiap modul menghitung **Skor Raw** dan **Skor Ternormalisasi** berdasarkan rumus terbaru.

### 1. 📚 Simulasi Publikasi (`publikasi.py`)
Menghitung skor berdasarkan produktivitas publikasi ilmiah.
* **Indikator:** Artikel Jurnal Internasional (Q1-Q4, Non-Q), Jurnal Nasional (S1-S6), Prosiding, Sitasi, dan Buku.
* **Fitur:** Visualisasi breakdown skor antara Internasional, Nasional, dan Lainnya.
* **Normalisasi:** Menggunakan pembagi *1776.69*.

### 2. 🔬 Simulasi Research / Penelitian (`research.py`)
Menghitung skor kinerja penelitian dosen.
* **Indikator:** Hibah Luar Negeri, Hibah Eksternal, Hibah Internal, dan Total Dana Penelitian (Rupiah).
* **Fitur:** Input nilai rupiah dalam juta untuk presisi perhitungan.
* **Normalisasi:** Menggunakan pembagi *261,491.37*.

### 3. 💡 Simulasi HKI (`hki.py`)
Menghitung skor luaran Hak Kekayaan Intelektual.
* **Indikator:** Paten, Paten Sederhana, Hak Cipta, Desain Industri, Perlindungan Varietas Tanaman, dll.
* **Normalisasi:** Menggunakan pembagi *14.7*.

### 4. 🏛️ Simulasi Kelembagaan (`kelembagaan.py`)
Menghitung skor kinerja kelembagaan institusi.
* **Indikator:** Akreditasi Prodi (Unggul/A/Baik Sekali) dan Jumlah Jurnal Terakreditasi yang dikelola institusi.
* **Logika Khusus:** Menerapkan faktor penyesuaian (30%) sebelum normalisasi.
* **Normalisasi:** Menggunakan pembagi *2181.33*.

---

## 🛠️ Teknologi yang Digunakan

* **[Python](https://www.python.org/)**: Bahasa pemrograman utama.
* **[Streamlit](https://streamlit.io/)**: Framework untuk membuat dashboard interaktif web.
* **[Pandas](https://pandas.pydata.org/)**: Manipulasi data perhitungan.
* **[Plotly Express](https://plotly.com/python/)**: Visualisasi grafik (Pie Chart) interaktif.

---

## 💻 Cara Menjalankan (Installation)

Pastikan Anda sudah menginstall Python. Ikuti langkah berikut untuk menjalankan simulator di komputer lokal Anda:

1.  **Clone Repository**
    ```bash
    git clone [https://github.com/username-anda/prediksi-cluster-sinta.git](https://github.com/username-anda/prediksi-cluster-sinta.git)
    cd prediksi-cluster-sinta
    ```

2.  **Install Library yang Dibutuhkan**
    ```bash
    pip install streamlit pandas plotly
    ```

3.  **Jalankan Aplikasi**
    Pilih salah satu modul yang ingin disimulasikan, misalnya modul Publikasi:
    ```bash
    streamlit run publikasi.py
    ```
    *(Ganti nama file sesuai kebutuhan: `hki.py`, `research.py`, atau `kelembagaan.py`)*

---

## 🔮 Roadmap & Upcoming Features

Project ini terus dikembangkan untuk mencakup seluruh aspek penilaian SINTA. Rencana pengembangan selanjutnya meliputi:

- [ ] **Simulasi Pengabdian Masyarakat (Community Service):** Perhitungan skor kinerja pengabdian kepada masyarakat.
- [ ] **Simulasi SDM (Sumber Daya Manusia):** Perhitungan skor berdasarkan kualifikasi dosen (S3, Guru Besar, Lektor Kepala, dll).
- [ ] **Prediksi Persentase Cluster Mandiri:** Fitur pamungkas yang menggabungkan seluruh skor dari modul-modul di atas untuk memprediksi probabilitas (persentase) universitas masuk ke Cluster Mandiri secara *real-time*.

## 🤝 Kontribusi

Kontribusi sangat terbuka! Jika Anda memiliki pembaruan rumus SINTA terbaru atau ingin memperbaiki bug, silakan buat *Pull Request* atau buka *Issue*.

---
*Dibuat untuk keperluan simulasi strategis peningkatan pemeringkatan perguruan tinggi.*
