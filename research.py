import streamlit as st
import pandas as pd
import plotly.express as px

# Import our enhanced modules
from data_manager import get_val, set_val

def main():
    # Set page config without conflicting with main app
    try:
        st.set_page_config(layout="wide", page_title="SINTA Research Simulator")
    except:
        # If already set by main app, continue
        pass

    st.title("🔬 SINTA Cluster Simulator: Research (Penelitian)")
    st.markdown("Masukkan data penelitian pada tabel di kiri. Nilai P7 (Rupiah) dalam satuan Juta.")
    st.divider()

    # --- KONSTANTA RUMUS ---
    PEMBAGI_NORMALISASI = 261491.37   # Angka pembagi sesuai request

    # --- DATA RESEARCH ---
    # Format: (Kode, Nama Item, Bobot, Nilai Default from UPN Veteran Yogyakarta profile)
    data_research = [
        ("P1", "JUMLAH PENELITIAN HIBAH LUAR NEGERI (KETUA)", 40, 0.0),
        ("P2", "JUMLAH PENELITIAN HIBAH LUAR NEGERI (ANGGOTA)", 10, 0.0),
        ("P3", "JUMLAH PENELITIAN HIBAH EKSTERNAL (KETUA)", 30, 51.0),
        ("P4", "JUMLAH PENELITIAN HIBAH EKSTERNAL (ANGGOTA)", 10, 25.0),
        ("P5", "JUMLAH PENELITIAN INTERNAL INSTITUSI (KETUA)", 15, 523.0),
        ("P6", "JUMLAH PENELITIAN INTERNAL INSTITUSI (ANGGOTA)", 5, 32.0),
        ("P7", "JUMLAH RUPIAH PENELITIAN (JUTA RUPIAH)", 0.05, 37077.71),
    ]

    # --- LAYOUT SETUP ---
    col_left, col_right = st.columns([1.6, 1], gap="large")

    total_score_raw = 0
    chart_data = []

    # ==========================================
    # BAGIAN KIRI: TABEL INPUT
    # ==========================================
    with col_left:
        st.subheader("📝 Input Data Research")

        # Header Table
        h1, h2, h3, h4, h5 = st.columns([0.6, 3.5, 0.6, 1.2, 1])
        h1.markdown("**Kode**")
        h2.markdown("**Item**")
        h3.markdown("**Bbt**")
        h4.markdown("**Value**")
        h5.markdown("**Total**")
        st.markdown("---")

        for kode, nama, bobot, default_val in data_research:
            r1, r2, r3, r4, r5 = st.columns([0.6, 3.5, 0.6, 1.2, 1])

            with r1: st.write(f"**{kode}**")
            with r2: st.caption(nama)
            with r3: st.write(f"{bobot}")
            with r4:
                # Use data manager to get stored value or default
                current_val = get_val(f"v_{kode}", default_val)
                # Format %.2f karena rupiah biasanya 2 desimal
                val = st.number_input(
                    f"v_{kode}",
                    value=float(current_val),
                    step=1.0,
                    format="%.2f",
                    label_visibility="collapsed"
                )
                # Update the data manager with the new value
                set_val(f"v_{kode}", val)
            with r5:
                subtotal = val * bobot
                st.write(f"**{subtotal:,.2f}**")

                total_score_raw += subtotal
                if subtotal > 0:
                    chart_data.append({"Kode": kode, "Nama": nama, "Skor": subtotal})

    # ==========================================
    # BAGIAN KANAN: DASHBOARD ANALISIS
    # ==========================================
    with col_right:
        st.markdown("### 📊 Analisis Skor")

        # --- RUMUS PERHITUNGAN ---
        # (Total Score / 261.491,37) * 100
        if total_score_raw > 0:
            score_ternormal = (total_score_raw / max(PEMBAGI_NORMALISASI, total_score_raw)) * 100
        else:
            score_ternormal = 0.0

        # --- TAMPILAN 2 KARTU SKOR (STACKED) ---

        # Card 1: Total Raw
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 10px;">
            <h3 style="color: #333; margin:0;">{total_score_raw:,.2f}</h3>
            <p style="margin:0; font-size: 14px; color: #666;">Total Score Research</p>
        </div>
        """, unsafe_allow_html=True)

        # Card 2: Penyesuaian
        st.markdown(f"""
        <div style="background-color: #fff8e1; padding: 15px; border-radius: 8px; border: 1px solid #ffe0b2; margin-bottom: 10px;">
            <h3 style="color: #f57c00; margin:0;">{score_ternormal:,.2f}</h3>
            <p style="margin:0; font-size: 14px; color: #f57c00;">Total Score Ternormal</p>
        </div>
        """, unsafe_allow_html=True)

        # Card 3: Ternormalisasi (Hasil Akhir)
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
                color_discrete_sequence=px.colors.sequential.Purples_r
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