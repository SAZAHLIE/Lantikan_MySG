"""
========================================================================
MYSG KPM: MODUL PENJANAAN LAPORAN BEBAN KERJA (A4 LANDSCAPE)
========================================================================
Modul khas untuk menjana Laporan Beban Kerja terus tanpa pengelompokan kumpulan
(Sesuai untuk Cetakan Keseluruhan, Cetakan Guru, dan Cetakan AKP).
"""

import pandas as pd
from datetime import datetime
from letterhead_template import get_official_letterhead, get_a4_print_css

def generate_simple_workload_report_html(df_staff, title="LAPORAN BEBAN KERJA WARGA SEKOLAH", school_info=None, *args, **kwargs):
    """Menjana Laporan Beban Kerja Jadual Terus (A4 Landscape) Tanpa Pengelompokan Kumpulan."""
    if not isinstance(school_info, dict):
        school_info = {}

    header_html = get_official_letterhead(school_info)
    css_theme = get_a4_print_css(orientation='landscape')

    nama_sekolah = str(school_info.get('nama_sekolah', 'SEKOLAH KEBANGSAAN BANDAR SANDAKAN')).upper()
    kod_sekolah = str(school_info.get('kod_sekolah', 'XBA2004')).upper()
    tahun_sesi = str(school_info.get('tahun_sesi', '2026/2027'))
    tarikh_cetak = datetime.now().strftime("%d/%m/%Y %I:%M %p")

    jumlah_rekod = 0
    table_rows_html = ""

    if isinstance(df_staff, pd.DataFrame) and not df_staff.empty:
        jumlah_rekod = len(df_staff)
        
        df_calc = df_staff.copy()
        df_calc['Jam_PdP'] = df_calc.get('JUMLAH_JAM_PDP', 0.0).astype(float)
        df_calc['Jam_Port_H'] = df_calc.get('JUMLAH_JAM_PORTFOLIO_H', 0.0).astype(float)
        df_calc['Jam_Port_P'] = df_calc.get('JUMLAH_JAM_PORTFOLIO_P', 0.0).astype(float)
        df_calc['Jam_JK'] = df_calc.get('JUMLAH_JAM_JAWATANKUASA', 0.0).astype(float)
        df_calc['Jam_Total'] = df_calc.get('JUMLAH_BEBAN_KESELURAHAN', df_calc['Jam_PdP'] + df_calc['Jam_Port_H'] + df_calc['Jam_Port_P'] + df_calc['Jam_JK']).astype(float)

        for idx, (_, row) in enumerate(df_calc.iterrows(), start=1):
            nama = str(row.get('Nama', '-')).strip().upper()
            jawatan = str(row.get('Jawatan', '-')).replace('(nan)', '').replace('nan', '').strip()
            gred = str(row.get('Gred', '-')).replace('(nan)', '').replace('nan', '').strip()
            jawatan_gred = f"{jawatan} ({gred})" if (gred and gred != '-') else jawatan

            jam_pdp = round(row['Jam_PdP'], 1)
            jam_port_h = round(row['Jam_Port_H'], 1)
            jam_port_p = round(row['Jam_Port_P'], 1)
            jam_jk = round(row['Jam_JK'], 1)
            total = round(row['Jam_Total'], 1)

            if total > 35.0:
                status_agihan = "<span style='color: #8b0000; font-weight: bold;'>🔴 TINGGI</span>"
            elif total >= 20.0:
                status_agihan = "<span style='color: #2e7d32; font-weight: bold;'>🟢 SEIMBANG</span>"
            else:
                status_agihan = "<span style='color: #f57c00; font-weight: bold;'>🟡 OPTIMUM</span>"

            table_rows_html += f"""
            <tr>
                <td style="text-align: center; font-size: 8.5pt;">{idx}</td>
                <td style="font-size: 8.5pt; white-space: nowrap; font-weight: bold;">{nama}</td>
                <td style="font-size: 8.5pt; white-space: nowrap;">{jawatan_gred}</td>
                <td style="text-align: center; font-size: 8.5pt;">{jam_pdp}</td>
                <td style="text-align: center; font-size: 8.5pt;">{jam_port_h}</td>
                <td style="text-align: center; font-size: 8.5pt;">{jam_port_p}</td>
                <td style="text-align: center; font-size: 8.5pt;">{jam_jk}</td>
                <td style="text-align: center; font-weight: bold; font-size: 8.5pt; background-color: #f9f9f9;">{total}</td>
                <td style="text-align: center; font-size: 8.5pt; white-space: nowrap;">{status_agihan}</td>
            </tr>
            """
    else:
        table_rows_html = "<tr><td colspan='9' style='text-align:center; padding:10px;'>Tiada rekod data kakitangan.</td></tr>"

    return f"""
    <!DOCTYPE html>
    <html lang="ms">
    <head>
        <meta charset="UTF-8">
        <title>{title} - {nama_sekolah}</title>
        <style>
            {css_theme}
            
            @page {{
                @bottom-right {{
                    content: "[ Halaman " counter(page) " daripada " counter(pages) " ]";
                    font-size: 8pt;
                    font-weight: bold;
                    font-family: Arial, sans-serif;
                }}
                @bottom-left {{
                    content: "Dokumen Rasmi Dijana Menerusi Sistem Pengurusan Beban Kerja MySG KPM ({kod_sekolah}) | Tarikh Cetakan: {tarikh_cetak}";
                    font-size: 8pt;
                    font-style: italic;
                    color: #555;
                    font-family: Arial, sans-serif;
                }}
            }}

            .title-box {{ 
                font-weight: bold; 
                font-size: 11pt; 
                text-align: center; 
                text-transform: uppercase; 
                margin: 6px 0 10px 0; 
                line-height: 1.3;
            }}
            
            .landscape-table {{
                width: 100% !important;
                border-collapse: collapse;
                margin-top: 6px;
                margin-bottom: 12px;
                table-layout: auto;
            }}
            
            .landscape-table th {{
                border: 1px solid #000;
                padding: 5px 6px;
                font-size: 8.5pt !important;
                background-color: #f2f2f2;
                font-weight: bold;
                text-align: center;
            }}
            
            .landscape-table td {{
                border: 1px solid #000;
                padding: 4px 5px;
                font-size: 8.5pt !important;
            }}

            .print-footer-container {{
                margin-top: 12px;
                border-top: 1px solid #ccc;
                padding-top: 4px;
                font-size: 8pt;
                color: #555;
                display: flex;
                justify-content: space-between;
                font-family: Arial, sans-serif;
            }}
        </style>
    </head>
    <body>
        {header_html}

        <div class="title-box">
            {title}<br>
            SESI AKADEMIK {tahun_sesi} <br>
            <span style="font-size: 9.5pt; font-weight: normal; text-transform: none;">(Jumlah Rekod: <b>{jumlah_rekod}</b>)</span>
        </div>

        <table class="landscape-table">
            <thead>
                <tr>
                    <th style="width: 3%;">BIL</th>
                    <th style="width: 25%; text-align: left;">NAMA PEGAWAI</th>
                    <th style="width: 22%; text-align: left;">JAWATAN & GRED</th>
                    <th style="width: 8%;">PDP (JAM)</th>
                    <th style="width: 9%;">PORTFOLIO H (JAM)</th>
                    <th style="width: 9%;">PORTFOLIO P (JAM)</th>
                    <th style="width: 10%;">JAWATANKUASA J (JAM)</th>
                    <th style="width: 8%;">JUMLAH BEBAN</th>
                    <th style="width: 6%;">STATUS AGIHAN</th>
                </tr>
            </thead>
            <tbody>
                {table_rows_html}
            </tbody>
        </table>

        <!-- KOTAK MYSG KPM GUIDELINE -->
        <div style="border: 1px dashed #0f4c81; background-color: #fcfdfe; border-radius: 4px; padding: 6px 10px; font-size: 7.5pt; line-height: 1.35; margin-top: 8px; color: #222;">
            <div style="font-weight: bold; color: #c0392b; margin-bottom: 4px; text-transform: uppercase;">
                📌 KETETAPAN & GARIS PANDUAN PENETAPAN BEBAN KERJA WARGA SEKOLAH (MYSG KPM):
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2px 15px; font-weight: 500;">
                <div>• <b>Asas Pengiraan PdP:</b> 1 Waktu PdP = 0.5 Jam (30 Minit)</div>
                <div>• <b>Beban Kerja Seimbang:</b> 20.0 – 32.0 Jam/Minggu (PPP) / 40.0 Jam (AKP)</div>
            </div>
        </div>

        <div class="print-footer-container">
            <div><i>Dokumen Rasmi Dijana Menerusi Sistem Pengurusan Beban Kerja MySG KPM ({kod_sekolah}) | Tarikh Cetakan: <b>{tarikh_cetak}</b></i></div>
        </div>

        <script>
            window.onload = function() {{ window.print(); }};
        </script>
    </body>
    </html>
    """
