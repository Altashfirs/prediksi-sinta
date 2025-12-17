import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import json
import os

# Konfigurasi
CSV_INPUT = "hasil_sinta_metric.csv"
OUTPUT_JSON = "sinta_metrics_cluster_full.json"
DELAY = 1  # detik antar request

# Fungsi untuk parsing satu halaman
def parse_metrics_page(html_content):
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

# Baca CSV
df = pd.read_csv(CSV_INPUT)

# List hasil
results = []

# Proses tiap universitas
for idx, row in df.iterrows():
    sinta_id = row['Sinta ID Link']
    nama = row['Nama Institusi']
    klaster = row['Klaster']

    print(f"[{idx+1}/{len(df)}] Scraping {nama} (ID: {sinta_id})...")
    
    url = f"https://sinta.kemdiktisaintek.go.id/affiliations/profile/{sinta_id}/?view=matricscluster2026"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            print(f"  ❌ Gagal akses {url}")
            continue

        metrics = parse_metrics_page(response.text)
        if metrics is None:
            print(f"  ⚠️ Tidak ada data metrics")
            continue

        results.append({
            'Kode PT': row['Kode PT'],
            'Nama Institusi': nama,
            'Klaster': klaster,
            'Sinta ID': sinta_id,
            'Metrics': metrics
        })

        time.sleep(DELAY)

    except Exception as e:
        print(f"  ❌ Error: {e}")
        continue

# Simpan ke JSON
with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n✅ Selesai! Hasil disimpan di {OUTPUT_JSON}")