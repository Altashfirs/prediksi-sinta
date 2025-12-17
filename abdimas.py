import streamlit as st
import pandas as pd
import plotly.express as px

# Import our enhanced modules
from data_manager import get_val, set_val

def main():
    # Set page config without conflicting with main app
    try:
        st.set_page_config(layout="wide", page_title="SINTA Community Service Simulator")
    except:
        # If already set by main app, continue
        pass

    st.title("🤝 SINTA Cluster Simulator: Community Service (Abdimas)")
    st.markdown("Masukkan data pengabdian pada tabel di kiri. Input PM7 dalam Juta Rupiah.")
    st.divider()

    # --- KONSTANTA RUMUS ---
    PEMBAGI_NORMALISASI_COM = 447937.99   # Angka pembagi sesuai request

    # --- DATA COMMUNITY SERVICE ---
    # Format: (Kode, Nama Item, Bobot, Nilai Default from UPN Veteran Yogyakarta profile)
    data_com = [
        ("PM1", "JUMLAH PENGABDIAN MASYARAKAT INTERNASIONAL (KETUA)", 40, 0.0),
        ("PM2", "JUMLAH PENGABDIAN MASYARAKAT INTERNASIONAL (ANGGOTA)", 10, 0.0),
        ("PM3", "JUMLAH PENGABDIAN MASYARAKAT NASIONAL/EKSTERNAL (KETUA)", 30, 9.0),
        ("PM4", "JUMLAH PENGABDIAN MASYARAKAT NASIONAL/EKSTERNAL (ANGGOTA)", 10, 0.0),
        ("PM5", "JUMLAH PENGABDIAN MASYARAKAT LOKAL/INTERNAL INSTITUSI (KETUA)", 15, 96.0),
        ("PM6", "JUMLAH PENGABDIAN MASYARAKAT LOKAL/INTERNAL INSTITUSI (ANGGOTA)", 5, 8.0),
        ("PM7", "JUMLAH RUPIAH PENGABDIAN MASYARAKAT (JUTA RUPIAH)", 0.05, 3351.79),
    ]

    # --- LAYOUT SETUP ---
    col_left, col_right = st.columns([1.6, 1], gap="large")

    total_score_raw = 0
    chart_data = []

    # ==========================================
    # BAGIAN KIRI: TABEL INPUT
    # ==========================================
    with col_left:
        st.subheader("📝 Input Data Abdimas")

        # Header Table
        h1, h2, h3, h4, h5 = st.columns([0.6, 3.5, 0.6, 1.2, 1])
        h1.markdown("**Kode**")
        h2.markdown("**Item**")
        h3.markdown("**Bbt**")
        h4.markdown("**Value**")
        h5.markdown("**Total**")
        st.markdown("---")

        for kode, nama, bobot, default_val in data_com:
            r1, r2, r3, r4, r5 = st.columns([0.6, 3.5, 0.6, 1.2, 1])

            with r1: st.write(f"**{kode}**")
            with r2: st.caption(nama)
            with r3: st.write(f"{bobot}")
            with r4:
                # Use data manager to get stored value or default
                current_val = get_val(f"v_{kode}", default_val)
                # Menggunakan step=0.01 untuk mengakomodir nilai Rupiah yang desimal
                val = st.number_input(
                    f"v_{kode}",
                    value=float(current_val),
                    step=1.0 if kode != "PM7" else 0.01, # Step kecil khusus Rupiah
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
        # (Total Score / 447.937,99) * 100
        if total_score_raw > 0:
            score_ternormal = (total_score_raw / PEMBAGI_NORMALISASI_COM) * 100
        else:
            score_ternormal = 0.0

        # --- TAMPILAN KARTU SKOR ---

        # Card 1: Total Raw
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 10px;">
            <h3 style="color: #333; margin:0;">{total_score_raw:,.2f}</h3>
            <p style="margin:0; font-size: 14px; color: #666;">Total Score Abdimas</p>
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
                color_discrete_sequence=px.colors.sequential.Oranges_r
            )
            fig.update_layout(margin=dict(t=40, b=0, l=0, r=0), height=250)
            st.plotly_chart(fig, use_container_width=True)

            # Rincian Dataframe
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