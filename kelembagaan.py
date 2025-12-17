import streamlit as st
import pandas as pd
import plotly.express as px

# Import our enhanced modules
from data_manager import get_val, set_val

def main():
    # Set page config without conflicting with main app
    try:
        st.set_page_config(layout="wide", page_title="SINTA Kelembagaan Simulator")
    except:
        # If already set by main app, continue
        pass

    st.title("🏛️ SINTA Cluster Simulator: Kelembagaan")
    st.markdown("Masukkan nilai pada tabel di kiri. Perhitungan mencakup Total, Penyesuaian (30%), dan Normalisasi.")
    st.divider()

    # --- KONSTANTA RUMUS ---
    FAKTOR_PENYESUAIAN = 0.30       # 30%
    PEMBAGI_NORMALISASI = 2181.33   # Angka pembagi

    # --- DATA KELEMBAGAAN ---
    # Format: (Group, Kode, Nama Item, Bobot, Nilai Default from UPN Veteran Yogyakarta profile)
    # Grouping: APS (Akreditasi Prodi) & JO (Jurnal)
    data_kelembagaan = [
        ("Akreditasi", "APS1", "AKREDITASI PRODI A/UNGGUL/INTERNASIONAL", 40, 0.514),
        ("Akreditasi", "APS2", "AKREDITASI PRODI B/BAIK SEKALI", 30, 0.343),
        ("Akreditasi", "APS3", "AKREDITASI PRODI C/BAIK", 20, 0.114),
        ("Akreditasi", "APS4", "AKREDITASI PRODI D/TIDAK TERAKREDITASI", 0, 0.029),
        
        ("Jurnal", "JO1", "JUMLAH JURNAL TERAKREDITASI S1", 40, 0.000),
        ("Jurnal", "JO2", "JUMLAH JURNAL TERAKREDITASI S2", 30, 2.000),
        ("Jurnal", "JO3", "JUMLAH JURNAL TERAKREDITASI S3", 20, 2.000),
        ("Jurnal", "JO4", "JUMLAH JURNAL TERAKREDITASI S4", 10, 10.000),
        ("Jurnal", "JO5", "JUMLAH JURNAL TERAKREDITASI S5", 5, 2.000),
        ("Jurnal", "JO6", "JUMLAH JURNAL TERAKREDITASI S6", 2, 0.000),
    ]

    # --- LAYOUT SETUP ---
    col_left, col_right = st.columns([1.6, 1], gap="large")

    total_score_raw = 0
    chart_data = []

    # ==========================================
    # BAGIAN KIRI: TABEL INPUT
    # ==========================================
    with col_left:
        st.subheader("📝 Input Data Kelembagaan")

        # Header Table
        h1, h2, h3, h4, h5 = st.columns([0.6, 3.5, 0.6, 1.2, 1])
        h1.markdown("**Kode**")
        h2.markdown("**Item**")
        h3.markdown("**Bbt**")
        h4.markdown("**Value**")
        h5.markdown("**Total**")
        st.markdown("---")

        for group, kode, nama, bobot, default_val in data_kelembagaan:
            r1, r2, r3, r4, r5 = st.columns([0.6, 3.5, 0.6, 1.2, 1])

            with r1: st.write(f"**{kode}**")
            with r2: st.caption(nama)
            with r3: st.write(f"{bobot}")
            with r4:
                # Use data manager to get stored value or default
                current_val = get_val(f"v_{kode}", default_val)
                # Menggunakan step=0.001 agar presisi desimal APS bisa diinput
                val = st.number_input(
                    f"v_{kode}",
                    value=float(current_val),
                    step=0.001,
                    format="%.3f",
                    label_visibility="collapsed"
                )
                # Update the data manager with the new value
                set_val(f"v_{kode}", val)
            with r5:
                subtotal = val * bobot
                st.write(f"**{subtotal:,.2f}**") # 2 desimal cukup untuk total per item

                total_score_raw += subtotal
                if subtotal > 0:
                    chart_data.append({"Kode": kode, "Nama": nama, "Skor": subtotal, "Group": group})

    # ==========================================
    # BAGIAN KANAN: DASHBOARD ANALISIS
    # ==========================================
    with col_right:
        st.markdown("### 📊 Analisis Skor")

        # --- RUMUS PERHITUNGAN ---
        # 1. Total Score Kelembagaan (Sudah dihitung di loop)

        # 2. Total Score Penyesuaian (Total * 30%)
        score_penyesuaian = total_score_raw * FAKTOR_PENYESUAIAN

        # 3. Total Score Ternormal ((Penyesuaian / 2181.33) * 100)
        if score_penyesuaian > 0:
            score_ternormal = (score_penyesuaian / max(PEMBAGI_NORMALISASI, score_penyesuaian)) * 100
        else:
            score_ternormal = 0.0

        # --- TAMPILAN 3 KARTU SKOR (STACKED) ---

        # Card 1: Total Raw
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 10px;">
            <h3 style="color: #333; margin:0;">{total_score_raw:,.2f}</h3>
            <p style="margin:0; font-size: 14px; color: #666;">Total Score Kelembagaan</p>
        </div>
        """, unsafe_allow_html=True)

        # Card 2: Penyesuaian
        st.markdown(f"""
        <div style="background-color: #fff8e1; padding: 15px; border-radius: 8px; border: 1px solid #ffe0b2; margin-bottom: 10px;">
            <h3 style="color: #f57c00; margin:0;">{score_penyesuaian:,.2f}</h3>
            <p style="margin:0; font-size: 14px; color: #f57c00;">Score Penyesuaian (30%)</p>
        </div>
        """, unsafe_allow_html=True)

        # Card 3: Ternormalisasi (Hasil Akhir)
        st.markdown(f"""
        <div style="background-color: #e6fffa; padding: 15px; border-radius: 8px; border: 1px solid #4fd1c5; margin-bottom: 20px;">
            <h2 style="color: #234e52; margin:0;">{score_ternormal:,.2f}</h2>
            <p style="margin:0; font-size: 14px; color: #234e52;"><b>Total Score Ternormal</b></p>
            <p style="margin:0; font-size: 10px; color: #234e52; margin-top:5px;"><i>Rumus: (Score Penyesuaian / {PEMBAGI_NORMALISASI:,.2f}) x 100</i></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background-color: #e6fffa; padding: 15px; border-radius: 8px; border: 1px solid #4fd1c5; margin-bottom: 20px;">
            <h2 style="color: #234e52; margin:0;">{score_ternormal * 0.15:,.2f}</h2>
            <p style="margin:0; font-size: 14px; color: #234e52;"><b>Total Score Ternormal (15%)</b></p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Visualisasi Pie Chart
        if chart_data:
            df_chart = pd.DataFrame(chart_data)

            # Pie Chart
            fig = px.pie(
                df_chart,
                values='Skor',
                names='Kode',
                title='Komposisi Skor per Item',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_layout(margin=dict(t=40, b=0, l=0, r=0), height=250)
            st.plotly_chart(fig, use_container_width=True)

            # Rincian
            with st.expander("Lihat Rincian"):
                st.dataframe(
                    df_chart[['Kode', 'Nama', 'Skor']].sort_values(by="Skor", ascending=False),
                    hide_index=True,
                    use_container_width=True
                )
        else:
            st.info("Belum ada data.")

if __name__ == "__main__":
    main()