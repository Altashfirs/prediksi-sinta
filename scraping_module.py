import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import json
import os
from datetime import datetime

def parse_metrics_page(html_content):
    """Parse the metrics page HTML content and extract data."""
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', class_='table')
    if not table:
        return None

    sections = {}
    current_section = None
    rows = table.find_all('tr')

    for row in rows:
        # Deteksi header section
        header = row.find('th', colspan=True, style=lambda x: x and 'border-left: 3px solid' in x)
        if header and 'Total' not in header.get_text():
            section_text = header.get_text(strip=True)
            if 'Score in' in section_text:
                current_section = section_text
                sections[current_section] = []
            continue

        # Deteksi total akhir (TOTAL ALL SCORE)
        total_all = row.find('th', style=lambda x: x and '#FF6B1A' in x)
        if total_all and 'TOTAL ALL SCORE' in total_all.get_text():
            total_score = row.find_all('th')[-1].get_text(strip=True)
            sections['TOTAL ALL SCORE'] = total_score
            continue

        # Deteksi subtotal section (Total Score Publication Ternormal, dll)
        italic_total = row.find('th', style=lambda x: x and 'font-style: italic' in x)
        if italic_total:
            text = italic_total.get_text(strip=True)
            if 'Total Score' in text:
                value = row.find_all('th')[-1].get_text(strip=True)
                sections.setdefault(current_section + ' (subtotal)', []).append({
                    'label': text,
                    'value': value
                })
            continue

        # Ambil data baris biasa (AI1, AN2, dll)
        cols = row.find_all(['th', 'td'])
        if len(cols) >= 5 and cols[0].get('style') and 'border-left: 3px solid' in cols[0]['style']:
            code = cols[1].get_text(strip=True)
            name = cols[2].get_text(strip=True)
            weight = cols[3].get_text(strip=True)
            value = cols[4].get_text(strip=True).replace(',', '.')
            total = cols[5].get_text(strip=True).replace(',', '.')

            if current_section:
                sections[current_section].append({
                    'code': code,
                    'name': name,
                    'weight': weight,
                    'value': value,
                    'total': total
                })

    return sections

def scrape_institution_data(sinta_id, nama, klaster, kode_pt):
    """Scrape data for a single institution."""
    url = f"https://sinta.kemdiktisaintek.go.id/affiliations/profile/{sinta_id}/?view=matricscluster2026"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            st.warning(f"Gagal akses {url}")
            return None

        metrics = parse_metrics_page(response.text)
        if metrics is None:
            st.warning(f"Tidak ada data metrics untuk {nama}")
            return None

        return {
            'Kode PT': kode_pt,
            'Nama Institusi': nama,
            'Klaster': klaster,
            'Sinta ID': sinta_id,
            'Metrics': metrics
        }

    except Exception as e:
        st.error(f"Error saat mengambil data untuk {nama}: {e}")
        return None

def perform_scraping(csv_input, delay=1):
    """Perform the scraping operation."""
    # Read CSV
    df = pd.read_csv(csv_input)
    
    results = []
    processed_count = 0
    total_count = len(df)
    
    # Create a progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, row in df.iterrows():
        sinta_id = row['Sinta ID Link']
        nama = row['Nama Institusi']
        klaster = row['Klaster']
        kode_pt = row['Kode PT']
        
        status_text.text(f"Scraping {nama} (ID: {sinta_id})... ({processed_count+1}/{total_count})")
        
        result = scrape_institution_data(sinta_id, nama, klaster, kode_pt)
        if result:
            results.append(result)
        
        processed_count += 1
        progress_bar.progress(processed_count / total_count)
        
        # Sleep to avoid overloading the server (only if not the last item)
        if processed_count < total_count:
            time.sleep(delay)
    
    # Generate filename with current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"sinta_metrics_cluster_{timestamp}.json"
    
    # Save to JSON file
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    status_text.text(f"✅ Selesai! Hasil disimpan di {output_filename}")
    
    return output_filename, results

def scraping_page():
    """The scraping functionality page."""
    st.title("🔄 SINTA Data Scraper")
    st.markdown("### Ambil data SINTA terbaru dari berbagai institusi")
    
    st.info("Fitur ini akan mengambil data terbaru dari sistem SINTA untuk berbagai institusi pendidikan.")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload file CSV dengan data institusi (harus memiliki kolom: Kode PT, Nama Institusi, Sinta ID Link, Klaster)",
        type=['csv']
    )
    
    # Use existing CSV if available
    use_existing_csv = False
    if os.path.exists("hasil_sinta_metric.csv"):
        use_existing_csv = st.checkbox("Gunakan file hasil_sinta_metric.csv yang sudah ada")
    
    if uploaded_file or use_existing_csv:
        if use_existing_csv:
            csv_input = "hasil_sinta_metric.csv"
            df = pd.read_csv(csv_input)
        else:
            # Save uploaded file temporarily
            df = pd.read_csv(uploaded_file)
            csv_input = uploaded_file.name
        
        st.success(f"File berhasil dimuat. Total institusi: {len(df)}")
        
        # Show preview of the data
        st.subheader("Pratinjau Data")
        st.dataframe(df.head())
        
        # Delay configuration
        delay = st.slider("Delay antar request (detik)", 0.5, 5.0, 1.0, 0.1)
        
        # Start scraping
        if st.button(" Mulai Scraping Data", type="primary"):
            with st.spinner("Sedang melakukan scraping... Proses ini mungkin memakan waktu beberapa menit."):
                output_filename, results = perform_scraping(csv_input, delay)
                
                if results:
                    st.success(f"Scraping selesai! Data telah disimpan ke {output_filename}")
                    
                    # Show download link
                    with open(output_filename, 'r', encoding='utf-8') as f:
                        st.download_button(
                            label="📥 Download Hasil Scraping",
                            data=f.read(),
                            file_name=output_filename,
                            mime="application/json"
                        )
                
                else:
                    st.error("Tidak ada data yang berhasil diambil")
    
    else:
        st.warning("Silakan upload file CSV atau gunakan file hasil_sinta_metric.csv yang sudah ada")
    
    st.divider()
    st.markdown("### Catatan:")
    st.markdown("""
    - File CSV harus memiliki kolom: `Kode PT`, `Nama Institusi`, `Sinta ID Link`, `Klaster`
    - Jika menggunakan file default, pastikan `hasil_sinta_metric.csv` tersedia di direktori utama
    - Gunakan delay yang cukup untuk menghindari pemblokiran dari server SINTA
    - Hasil akan disimpan dalam file JSON dengan penamaan otomatis berdasarkan tanggal dan waktu
    """)