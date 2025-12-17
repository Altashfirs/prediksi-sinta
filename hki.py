import streamlit as st
import pandas as pd
import plotly.express as px

# Import our enhanced modules
from data_manager import get_val, set_val

def main():
    # Set page config without conflicting with main app
    try:
        st.set_page_config(layout="wide", page_title="SINTA HKI Simulator")
    except:
        # If already set by main app, continue
        pass

    st.title("💡 SINTA Cluster Simulator: HKI")
    st.markdown("Masukkan nilai pada tabel di kiri. Skor ternormalisasi dihitung menggunakan rumus terbaru.")
    st.divider()

    # --- KONFIGURASI DATA HKI ---
    # (Kode, Nama, Bobot, Default Value from UPN Veteran Yogyakarta profile)
    data_hki = [
        ("KI1", "HKI PATEN", 40, 0.000),
        ("KI2", "HKI PATEN SEDERHANA", 20, 0.015),
        ("KI3", "HKI MEREK", 1, 0.005),
        ("KI4", "HKI INDIKASI GEOGRAFIS", 10, 0.000),
        ("KI5", "HKI DESAIN INDUSTRI", 20, 0.000),
        ("KI6", "HKI DESAIN TATA LETAK SIRKUIT TERPADU", 20, 0.000),
        ("KI7", "HKI RAHASIA DAGANG", 0, 0.000),
        ("KI8", "HKI PERLINDUNGAN VARIETAS TANAMAN", 40, 0.003),
        ("KI9", "HKI HAK CIPTA", 1, 0.409),
        ("KI10", "HKI SELAIN TERDAFTAR / DIBERI / DITERIMA", 1, 0.000),
    ]

    # --- LAYOUT SETUP ---
    col_left, col_right = st.columns([1.6, 1], gap="large")

    total_score_raw = 0
    chart_data = []

    # ==========================================
    # BAGIAN KIRI: TABEL INPUT
    # ==========================================
    with col_left:
        st.subheader("📝 Input Data HKI")

        # Header Table
        h1, h2, h3, h4, h5 = st.columns([0.6, 3.5, 0.6, 1.2, 1])
        h1.markdown("**Kode**")
        h2.markdown("**Item HKI**")
        h3.markdown("**Bbt**")
        h4.markdown("**Value**")
        h5.markdown("**Total**")
        st.markdown("---")

        for kode, nama, bobot, default_val in data_hki:
            r1, r2, r3, r4, r5 = st.columns([0.6, 3.5, 0.6, 1.2, 1])

            with r1: st.write(f"**{kode}**")
            with r2: st.caption(nama)
            with r3: st.write(f"{bobot}")
            with r4:
                # Use data manager to get stored value or default
                current_val = get_val(f"v_{kode}", default_val)
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
                st.write(f"**{subtotal:,.3f}**")

                total_score_raw += subtotal
                if subtotal > 0:
                    chart_data.append({"Kode": kode, "Nama": nama, "Skor": subtotal})

    # ==========================================
    # BAGIAN KANAN: DASHBOARD ANALISIS
    # ==========================================
    with col_right:
        st.markdown("### 📊 Ringkasan Skor")

        # --- RUMUS BARU ---
        # (Total Score / 14.7) * 100
        if total_score_raw > 0:
            score_normalized = (total_score_raw / max(total_score_raw, 14.7)) * 100
        else:
            score_normalized = 0.0

        # Tampilan Kartu Skor
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 10px;">
            <h3 style="color: #333; margin:0;">{total_score_raw:,.2f}</h3>
            <p style="margin:0; font-size: 14px; color: #666;">Total Score HKI</p>
        </div>
        """, unsafe_allow_html=True)

        # Card 2: Penyesuaian
        st.markdown(f"""
        <div style="background-color: #fff8e1; padding: 15px; border-radius: 8px; border: 1px solid #ffe0b2; margin-bottom: 10px;">
            <h3 style="color: #f57c00; margin:0;">{score_normalized:,.2f}</h3>
            <p style="margin:0; font-size: 14px; color: #f57c00;">Total Score Ternormal</p>
        </div>
        """, unsafe_allow_html=True)

        # Card 3: Ternormalisasi (Hasil Akhir)
        st.markdown(f"""
        <div style="background-color: #e6fffa; padding: 15px; border-radius: 8px; border: 1px solid #4fd1c5; margin-bottom: 20px;">
            <h2 style="color: #234e52; margin:0;">{score_normalized * 0.10:,.2f}</h2>
            <p style="margin:0; font-size: 14px; color: #234e52;"><b>Total Score Ternormal (10%)</b></p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Visualisasi
        if chart_data:
            df_chart = pd.DataFrame(chart_data)

            # Pie Chart
            fig = px.pie(
                df_chart,
                values='Skor',
                names='Kode',
                title='Kontribusi Skor per Item',
                hole=0.5,
                color_discrete_sequence=px.colors.sequential.Teal
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(margin=dict(t=40, b=0, l=0, r=0), height=250)
            st.plotly_chart(fig, use_container_width=True)

            # Tabel Ringkas
            with st.expander("Lihat Rincian"):
                st.dataframe(
                    df_chart[['Kode', 'Nama', 'Skor']].sort_values(by="Skor", ascending=False),
                    hide_index=True,
                    use_container_width=True
                )
        else:
            st.info("Belum ada skor HKI.")

if __name__ == "__main__":
    main()