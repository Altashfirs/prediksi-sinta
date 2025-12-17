import streamlit as st
import pandas as pd
import plotly.express as px

# Import our enhanced modules
from data_manager import get_val, set_val

def main():
    # Set page config without conflicting with main app
    try:
        st.set_page_config(layout="wide", page_title="SINTA Publication Simulator")
    except:
        # If already set by main app, continue
        pass

    st.title("📚 SINTA Cluster Simulator: Publikasi")
    st.markdown("Masukkan nilai pada tabel di sebelah kiri. Skor ternormalisasi (sesuai rumus) akan muncul di kanan.")
    st.divider()

    # --- KONSTANTA & DATA ---
    NORMALIZER_PUB = 1776.69  # Pembagi Normalisasi (1.776,69)

    # Format Tuple: (Kategori Group, Kode, Nama Item, Bobot, Nilai Default dari Gambar)
    raw_data = [
        # --- INTERNASIONAL (AI) ---
        ("Intl", "AI1", "ARTIKEL JURNAL INTERNASIONAL Q1", 40, 0.136),
        ("Intl", "AI2", "ARTIKEL JURNAL INTERNASIONAL Q2", 35, 0.159),
        ("Intl", "AI3", "ARTIKEL JURNAL INTERNASIONAL Q3", 30, 0.147),
        ("Intl", "AI4", "ARTIKEL JURNAL INTERNASIONAL Q4", 25, 0.075),
        ("Intl", "AI5", "ARTIKEL JURNAL INTERNASIONAL NON Q", 20, 0.040),
        ("Intl", "AI6", "ARTIKEL NON JURNAL INTERNASIONAL", 15, 0.504),
        ("Intl", "AI7", "JUMLAH SITASI PUBLIKASI INTERNASIONAL", 1, 932.079),
        ("Intl", "AI8", "JUMLAH DOKUMEN PUBLIKASI INTERNASIONAL TERSITASI", 1, 0.588),
        
        # --- NASIONAL (AN) ---
        ("Nas", "AN1", "ARTIKEL JURNAL NASIONAL PERINGKAT 1", 25, 0.007),
        ("Nas", "AN2", "ARTIKEL JURNAL NASIONAL PERINGKAT 2", 20, 0.169),
        ("Nas", "AN3", "ARTIKEL JURNAL NASIONAL PERINGKAT 3", 15, 0.204),
        ("Nas", "AN4", "ARTIKEL JURNAL NASIONAL PERINGKAT 4", 10, 0.464),
        ("Nas", "AN5", "ARTIKEL JURNAL NASIONAL PERINGKAT 5", 5, 0.312),
        ("Nas", "AN6", "ARTIKEL JURNAL NASIONAL PERINGKAT 6", 2, 0.012),
        ("Nas", "AN8", "PROSIDING NASIONAL", 2, 0.104),
        ("Nas", "AN9", "JUMLAH SITASI PUBLIKASI NASIONAL PER DOSEN", 1, 0.000),
        
        # --- BUKU & LAINNYA (B & DGS) ---
        ("Other", "DGS2", "GS CITATION PER LECTURER", 1, 0.473),
        ("Other", "B1", "BUKU AJAR", 20, 0.070),
        ("Other", "B2", "BUKU REFERENSI", 40, 0.415),
        ("Other", "B3", "BUKU MONOGRAF", 20, 0.069),
    ]

    # --- LAYOUT SETUP ---
    col_left, col_right = st.columns([1.6, 1], gap="large")

    total_score_all = 0
    breakdown_scores = {"Intl": 0, "Nas": 0, "Other": 0}
    chart_data = []

    # ==========================================
    # BAGIAN KIRI: TABEL INPUT
    # ==========================================
    with col_left:
        st.subheader("📝 Input Data (Weight ≥ 1)")

        # Header Table
        h1, h2, h3, h4, h5 = st.columns([0.6, 3.5, 0.6, 1.2, 1])
        h1.markdown("**Code**")
        h2.markdown("**Name**")
        h3.markdown("**W**")
        h4.markdown("**Value**")
        h5.markdown("**Total**")
        st.markdown("---")

        # Looping Data
        for category, kode, nama, bobot, default_val in raw_data:
            r1, r2, r3, r4, r5 = st.columns([0.6, 3.5, 0.6, 1.2, 1])

            with r1:
                st.write(f"**{kode}**")
            with r2:
                st.caption(nama)
            with r3:
                st.write(f"{bobot}")
            with r4:
                # Use data manager to get stored value or default
                current_val = get_val(kode, default_val)
                val = st.number_input(
                    f"v_{kode}",
                    min_value=0.0,
                    value=float(current_val),
                    step=0.001,
                    format="%.3f",
                    label_visibility="collapsed",
                    key=kode
                )
                # Update the data manager with the new value
                set_val(kode, val)
            with r5:
                subtotal = val * bobot
                st.write(f"**{subtotal:,.2f}**")

                # Akumulasi Data
                total_score_all += subtotal
                breakdown_scores[category] += subtotal
                if subtotal > 0:
                    chart_data.append({"Kategori": kode, "Skor": subtotal, "Group": category})

    # ==========================================
    # BAGIAN KANAN: DASHBOARD ANALISIS
    # ==========================================
    with col_right:
        st.markdown("### 📊 Analisis Skor Publikasi")

        # --- HITUNG SKOR TERNORMALISASI ---
        normalized_score = (total_score_all / max(total_score_all, NORMALIZER_PUB)) * 100

        # 1. SCORE CARDS (TAMPILAN BARU: 2 KOLOM)
        # Card 1: Total Raw
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 10px;">
            <h3 style="color: #333; margin:0;">{total_score_all:,.2f}</h3>
            <p style="margin:0; font-size: 14px; color: #666;">Total Score Publikasi</p>
        </div>
        """, unsafe_allow_html=True)

        # Card 2: Penyesuaian
        st.markdown(f"""
        <div style="background-color: #fff8e1; padding: 15px; border-radius: 8px; border: 1px solid #ffe0b2; margin-bottom: 10px;">
            <h3 style="color: #f57c00; margin:0;">{normalized_score:,.2f}</h3>
            <p style="margin:0; font-size: 14px; color: #f57c00;">Total Score Ternormal</p>
        </div>
        """, unsafe_allow_html=True)

        # Card 3: Ternormalisasi (Hasil Akhir)
        st.markdown(f"""
        <div style="background-color: #e6fffa; padding: 15px; border-radius: 8px; border: 1px solid #4fd1c5; margin-bottom: 20px;">
            <h2 style="color: #234e52; margin:0;">{normalized_score * 0.25:,.2f}</h2>
            <p style="margin:0; font-size: 14px; color: #234e52;"><b>Total Score Ternormal (25%)</b></p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # 2. BREAKDOWN METRICS
        m1, m2, m3 = st.columns(3)
        m1.metric("Internasional", f"{breakdown_scores['Intl']:,.1f}")
        m2.metric("Nasional", f"{breakdown_scores['Nas']:,.1f}")
        m3.metric("Buku/Lainnya", f"{breakdown_scores['Other']:,.1f}")

        # 3. CHART VISUALISASI
        if chart_data:
            df_chart = pd.DataFrame(chart_data)

            # Pie Chart
            fig = px.pie(
                df_chart,
                values='Skor',
                names='Kategori',
                title='Komposisi Skor per Kode',
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            fig.update_layout(margin=dict(t=30, b=0, l=0, r=0), height=300)
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("Data kosong.")

        # 4. RINCIAN PERHITUNGAN & KETERANGAN
        with st.expander("Lihat Rincian Perhitungan"):
            if chart_data:
                st.dataframe(
                    pd.DataFrame(chart_data).sort_values(by="Skor", ascending=False),
                    use_container_width=True,
                    hide_index=True
                )

                st.markdown("---")
                st.markdown("##### ℹ️ Keterangan Kategori (Group)")
                st.caption("""
                - **Intl (Internasional):** Kode **AI** (Jurnal Internasional & Sitasi).
                - **Nas (Nasional):** Kode **AN** (Jurnal Nasional SINTA & Prosiding).
                - **Other (Lainnya):** Kode **B** (Buku) dan **DGS** (Google Scholar).
                """)

if __name__ == "__main__":
    main()