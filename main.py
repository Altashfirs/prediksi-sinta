import streamlit as st
import importlib
import pandas as pd

# Import our enhanced modules
from data_manager import get_val, reset_sinta_data, validate_sinta_data, get_data_manager
from cluster_prediction import calculate_cluster_score, predict_cluster_type, get_strategic_advice, calculate_advancement_path

# --- KONFIGURASI HALAMAN UTAMA ---
st.set_page_config(layout="wide", page_title="SINTA Master Simulator")

# ==============================================================================
# 1. PERSIAPAN DATA STORAGE & IMPROVED MONKEY PATCH
# ==============================================================================

# Initialize data manager
data_manager = get_data_manager()

# Simpan fungsi asli st.number_input untuk mengembalikannya nanti
_original_number_input = st.number_input

def _patched_number_input(label, *args, **kwargs):
    """
    Improved patched function for st.number_input.
    Every time user inputs a number, we also save it to SINTA_DB.
    """
    # Panggil fungsi asli untuk menampilkan widget
    val = _original_number_input(label, *args, **kwargs)

    # Tentukan ID untuk penyimpanan
    # Cek apakah modul menggunakan 'key' khusus (seperti publikasi.py)
    # Jika tidak ada key, gunakan label (seperti sdm.py yang pakai "v_R1")
    storage_key = kwargs.get("key", label)

    # Gunakan data_manager untuk menyimpan data
    data_manager.set_value(storage_key, val)

    return val

# ==============================================================================
# 2. IMPROVED UTILITIES
# ==============================================================================

def run_module_safely(module_name):
    """Menjalankan modul lain tanpa error double st.set_page_config"""
    # Hanya ganti st.number_input jika kita ingin menggunakan versi patched
    if st.session_state.get("use_patched_input", True):
        st.number_input = _patched_number_input

    original_set_page_config = st.set_page_config
    st.set_page_config = lambda *args, **kwargs: None

    try:
        # Import dan jalankan modul
        module = importlib.import_module(module_name)
        module.main()
    except Exception as e:
        st.error(f"Error pada modul {module_name}: {e}")
        st.info("Silakan pilih modul lain atau kembali ke dashboard utama.")
    finally:
        st.set_page_config = original_set_page_config

# ==============================================================================
# 3. ENHANCED MAIN NAVIGATION
# ==============================================================================

def main():
    # Sidebar dengan peningkatan
    with st.sidebar:
        st.title("🎛️ Navigasi SINTA")
        menu = st.radio("Pilih Modul", [
            "🏆 Dashboard Utama",
            "📊 Ringkasan Lengkap",
            "🎯 Strategi Peningkatan",
            "📚 Publikasi",
            "🔬 Research",
            "🤝 Abdimas",
            "💡 HKI",
            "👥 SDM",
            "🏛️ Kelembagaan",
            "🔄 Scraping Data",
            "⚙️ Pengaturan"
        ])

        # Tambahkan informasi tambahan di sidebar
        st.divider()

        # Preview skor kecil dengan penanganan error
        try:
            total_score, component_scores = calculate_cluster_score()
            st.metric("Total Score", f"{total_score:,.2f}")
            pred, color, icon = predict_cluster_type(total_score)
            st.success(f"{icon} {pred}")
            st.caption("Pindah ke Dashboard untuk hasil lengkap.")
        except:
            st.error("Error menghitung skor")

        st.divider()
        st.info("💡 Tips: Gunakan modul individual untuk mengisi data spesifik, lalu kembali ke dashboard untuk melihat total skor.")

    # --- ROUTING DENGAN PENINGKATAN ---
    if menu == "🏆 Dashboard Utama":
        st.title("🏆 Dashboard Prediksi Cluster SINTA")
        st.markdown("### Ringkasan prediksi cluster dan analisis komprehensif.")
        st.divider()

        # Hitung skor menggunakan fungsi yang ditingkatkan
        total_score, component_scores = calculate_cluster_score()

        # Tampilkan informasi prediksi cluster
        cluster_pred, color, icon = predict_cluster_type(total_score)
        st.subheader(f"{icon} Prediksi Cluster: {cluster_pred}")

        # Tambahkan ringkasan visual
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### 📊 Skor Total")
            st.markdown(f"<h1 style='text-align: center; color: #4F8BF9;'>{total_score:,.2f}</h1>", unsafe_allow_html=True)

        with col2:
            st.markdown("### 🎯 Target Cluster")
            advancement = calculate_advancement_path(total_score)
            if advancement['next_cluster'] != 'Maximum':
                st.markdown(f"<h1 style='text-align: center; color: #8C8C8C;'>{advancement['target_score']:.2f}</h1>", unsafe_allow_html=True)
                st.caption(f"Untuk {advancement['next_cluster']}")
            else:
                st.markdown(f"<h1 style='text-align: center; color: #4CAF50;'>Maksimal</h1>", unsafe_allow_html=True)

        with col3:
            st.markdown("### ⚡ Jarak ke Target")
            if advancement['next_cluster'] != 'Maximum':
                gap = advancement['gap']
                color_gap = "green" if gap <= 0 else "red"
                st.markdown(f"<h1 style='text-align: center; color: {color_gap};'>{'+' if gap >= 0 else ''}{gap:.2f}</h1>", unsafe_allow_html=True)
                st.caption("Poin yang dibutuhkan")
            else:
                st.markdown(f"<h1 style='text-align: center; color: #4CAF50;'>✅</h1>", unsafe_allow_html=True)
                st.caption("Target maksimal tercapai")

        # Tampilkan status kelulusan
        if total_score >= 50:  # Threshold for Mandiri cluster
            st.success(f"✅ **Lolos Cluster Mandiri!**  Skor: {total_score:.2f}")
        else:
            st.error(f"❌ **Belum Lolos Cluster Mandiri.**  Skor: {total_score:.2f} (butuh {30-total_score:.2f} poin lagi)")

        st.divider()

        # Tampilkan rincian skor dalam dua kolom
        col1, col2 = st.columns([1.5, 1])

        with col1:
            st.markdown("### 📈 Rincian Skor Ternormalisasi")
            # Convert dict to dataframe for nicer display
            rincian = {f"{k} ({'25%' if k == 'Publikasi' else '15%' if k in ['Research', 'SDM', 'Kelembagaan'] else '10%' if k == 'HKI' else '15%' if k == 'Abdimas' else '15%'})": v
                      for k, v in component_scores.items()}
            df_rincian = pd.DataFrame(list(rincian.items()), columns=["Komponen", "Skor Ternormalisasi"])

            # Tambahkan visualisasi berwarna
            df_rincian["Kategori"] = df_rincian["Skor Ternormalisasi"].apply(
                lambda x: "🟢 Baik" if x >= 50 else ("🟡 Cukup" if x >= 20 else "🔴 Perlu Perbaikan")
            )

            st.dataframe(
                df_rincian.style.format({"Skor Ternormalisasi": "{:.2f}"}),
                use_container_width=True,
                hide_index=True
            )

            # Visualisasi perbandingan
            st.markdown("### 📊 Perbandingan Komponen")
            st.bar_chart(df_rincian.set_index("Komponen")["Skor Ternormalisasi"])

        with col2:
            st.markdown("### 🎯 Rekomendasi Strategis")
            # Dapatkan rekomendasi strategis berdasarkan skor komponen
            recommendations = get_strategic_advice(component_scores)

            for rec in recommendations[:3]:  # Ambil 3 rekomendasi teratas
                priority_emoji = "🔴" if rec['priority'] == "TINGGI" else "🟡" if rec['priority'] == "SEDANG" else "🟢"
                st.write(f"{priority_emoji} **{rec['area']}** (Skor: {rec['current_score']:.2f})")
                st.write(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{rec['action']}")
                st.divider()

    elif menu == "📊 Ringkasan Lengkap":
        st.title("📊 Ringkasan Lengkap SINTA")
        st.markdown("### Analisis menyeluruh dari semua komponen penilaian.")
        st.divider()

        total_score, component_scores = calculate_cluster_score()

        # Tampilkan ringkasan dalam bentuk kartu
        cols = st.columns(3)
        komponen_utama = ["Publikasi", "Research", "SDM"]
        for i, komp in enumerate(komponen_utama):
            with cols[i]:
                skor = component_scores[komp]
                st.metric(
                    label=f"{komp} (25%/15%/15%)",
                    value=f"{skor:.2f}",
                    delta="+" + f"{skor:.1f}" if skor > 50 else f"{skor:.1f}",
                    delta_color="normal" if skor > 50 else "inverse"
                )

        cols2 = st.columns(3)
        komponen_lain = ["Abdimas", "HKI", "Kelembagaan"]
        for i, komp in enumerate(komponen_lain):
            with cols2[i]:
                skor = component_scores[komp]
                st.metric(
                    label=f"{komp} (15%/10%/15%)",
                    value=f"{skor:.2f}",
                    delta="+" + f"{skor:.1f}" if skor > 20 else f"{skor:.1f}",
                    delta_color="normal" if skor > 20 else "inverse"
                )

        # Tampilkan total dan prediksi cluster
        st.divider()
        st.subheader("Total Gabungan & Prediksi Cluster")

        cluster_pred, color, icon = predict_cluster_type(total_score)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Skor", f"{total_score:.2f}")
        with col2:
            st.metric("Prediksi Cluster", f"{icon} {cluster_pred}")
        with col3:
            advancement = calculate_advancement_path(total_score)
            if advancement['next_cluster'] != 'Maximum':
                st.metric("Gap ke Cluster", f"-{advancement['gap']:.2f}")
            else:
                st.metric("Status", "Max")

        # Tampilkan distribusi skor
        st.divider()
        st.subheader("Distribusi Skor Komponen")
        df_dist = pd.DataFrame.from_dict(component_scores, orient='index', columns=['Skor'])
        df_dist['Presentase dari Total'] = df_dist['Skor'] / df_dist['Skor'].sum() * 100
        st.bar_chart(df_dist['Skor'])

    elif menu == "🎯 Strategi Peningkatan":
        st.title("🎯 Strategi Peningkatan SINTA")
        st.markdown("### Rekomendasi strategis untuk peningkatan cluster.")
        st.divider()

        # Hitung skor terlebih dahulu
        total_score, component_scores = calculate_cluster_score()

        # Tampilkan rekomendasi strategis
        recommendations = get_strategic_advice(component_scores)

        st.subheader("Rekomendasi Berdasarkan Prioritas")

        for i, rec in enumerate(recommendations):
            priority_color = "red" if rec['priority'] == "TINGGI" else "orange" if rec['priority'] == "SEDANG" else "green"
            priority_emoji = "🔴" if rec['priority'] == "TINGGI" else "🟡" if rec['priority'] == "SEDANG" else "🟢"

            with st.container():
                st.markdown(f"### {i+1}. {priority_emoji} {rec['area']} (Skor: {rec['current_score']:.2f})")
                st.markdown(f"**Prioritas: {rec['priority']}**")
                st.info(rec['action'])

                # Tambahkan saran spesifik
                if rec['area'] == 'Publikasi':
                    st.write("- Tingkatkan jumlah publikasi internasional (Q1-Q4)")
                    st.write("- Fokus pada sitasi dan pengakuan (citations)")
                    st.write("- Lengkapi publikasi nasional terakreditasi")
                elif rec['area'] == 'Research':
                    st.write("- Ajukan lebih banyak hibah riset eksternal")
                    st.write("- Tingkatkan keterlibatan sebagai ketua peneliti")
                    st.write("- Tingkatkan nilai dana penelitian")
                elif rec['area'] == 'HKI':
                    st.write("- Ajukan lebih banyak paten dan HKI")
                    st.write("- Fokus pada HKI bernilai tinggi (Paten, Paten Sederhana)")
                    st.write("- Dokumentasikan kekayaan intelektual yang sudah ada")
                elif rec['area'] == 'SDM':
                    st.write("- Tingkatkan kualifikasi dosen (jabatan fungsional)")
                    st.write("- Dorong dosen menjadi reviewer jurnal internasional")
                    st.write("- Lengkapi sertifikasi dan pelatihan dosen")
                elif rec['area'] == 'Kelembagaan':
                    st.write("- Perbaiki akreditasi program studi")
                    st.write("- Tingkatkan jumlah jurnal terakreditasi")
                    st.write("- Optimalisasi struktur organisasi")
                elif rec['area'] == 'Abdimas':
                    st.write("- Tingkatkan kegiatan pengabdian masyarakat")
                    st.write("- Ajukan hibah pengabdian dari sumber eksternal")
                    st.write("- Lengkapi dokumentasi dan laporan pengabdian")

                st.divider()

        # Tampilkan rencana peningkatan ke cluster berikutnya
        st.subheader("Rencana Peningkatan ke Cluster Berikutnya")
        advancement = calculate_advancement_path(total_score)

        if advancement['next_cluster'] != 'Maximum':
            st.info(f"""
            📈 **Rencana Peningkatan:**
            - Cluster saat ini: {advancement['current_cluster']}
            - Target cluster: {advancement['next_cluster']}
            - Skor yang dibutuhkan: {advancement['target_score']:.2f}
            - Jarak yang harus ditutup: {advancement['gap']:.2f} poin
            - Rekomendasi: Fokus pada 3 komponen dengan skor terendah untuk efek maksimal terhadap total skor
            """)
        else:
            st.success("🎉 Selamat! Anda telah mencapai cluster tertinggi.")

    # --- MODUL INPUT (Jalankan file asli) ---
    elif menu == "📚 Publikasi":
        run_module_safely("publikasi")
    elif menu == "🔬 Research":
        run_module_safely("research")
    elif menu == "🤝 Abdimas":
        run_module_safely("abdimas")
    elif menu == "💡 HKI":
        run_module_safely("hki")
    elif menu == "👥 SDM":
        run_module_safely("sdm")
    elif menu == "🏛️ Kelembagaan":
        run_module_safely("kelembagaan")
    elif menu == "🔄 Scraping Data":
        # Import and run the scraping module
        try:
            from scraping_module import scraping_page
            scraping_page()
        except ImportError as e:
            st.error(f"Error importing scraping module: {e}")
            st.info("Pastikan file scraping_module.py ada di direktori utama.")
    elif menu == "⚙️ Pengaturan":
        st.title("⚙️ Pengaturan Aplikasi")
        st.info("Pengaturan untuk sistem prediksi SINTA")

        with st.expander("Data Simulasi"):
            summary = data_manager.get_data_summary()
            st.write(f"Jumlah input yang tersimpan: {summary['total_fields']}")
            st.write(f"Input dengan nilai > 0: {summary['non_zero_fields']}")
            st.write(f"Nilai total: {summary['total_value']:.2f}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Reset Data Simulasi"):
                    reset_sinta_data()
                    st.success("Data berhasil direset")
                    st.rerun()
            with col2:
                if st.button("Validasi Data"):
                    is_valid = validate_sinta_data()
                    if is_valid:
                        st.success("✅ Data valid - tidak ada masalah ditemukan")
                    else:
                        st.warning("⚠️ Ada masalah dengan data, lihat pesan di atas")

        with st.expander("Simpan/Muat Data"):
            st.info("Fitur untuk menyimpan dan memuat data SINTA")
            filename = st.text_input("Nama file untuk menyimpan/memuat:", "sinta_data.json")
            col1, col2 = st.columns(2)

            with col1:
                if st.button("💾 Simpan Data"):
                    if data_manager.save_to_file(filename):
                        st.success(f"Data berhasil disimpan ke {filename}")
                    else:
                        st.error("Gagal menyimpan data")

            with col2:
                if st.button("📂 Muat Data"):
                    if data_manager.load_from_file(filename):
                        st.success(f"Data berhasil dimuat dari {filename}")
                        st.rerun()
                    else:
                        st.error("Gagal memuat data")

        with st.expander("Informasi Sistem"):
            st.write("Sistem prediksi cluster SINTA versi terbaru")
            st.write("- Data persistence ditingkatkan")
            st.write("- Algoritma prediksi cluster ditingkatkan")
            st.write("- Rekomendasi strategis ditambahkan")
            st.write("- Validasi data ditambahkan")

if __name__ == "__main__":
    main()