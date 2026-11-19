"""
========================================================================
MYSG KPM: MODUL PENJANAAN LAPORAN BANDINGAN KESELURUHAN (A4 LANDSCAPE)
========================================================================
"""

import pandas as pd
from datetime import datetime, timedelta, timezone
from letterhead_template import get_official_letterhead, get_a4_print_css

def generate_detailed_comparison_html(df_staff, title="LAPORAN BEBAN KERJA KESELURUHAN WARGA SEKOLAH", school_info=None, session_state=None, *args, **kwargs):
    """Menjana LAPORAN BEBAN KERJA KESELURUHAN (Ambang 45 Jam JPA)."""
    if isinstance(title, dict):
        school_info = title
        title = "LAPORAN BEBAN KERJA KESELURUHAN WARGA SEKOLAH"
    elif isinstance(school_info, str):
        title = school_info
        school_info = session_state if isinstance(session_state, dict) else {}

    if not isinstance(school_info, dict):
        school_info = {}

    header_html = get_official_letterhead(school_info)
    css_theme = get_a4_print_css(orientation='landscape')

    nama_sekolah = str(school_info.get('nama_sekolah', 'SEKOLAH KEBANGSAAN BANDAR SANDAKAN')).upper()
    kod_sekolah = str(school_info.get('kod_sekolah', 'XBA2004')).upper()
    tahun_sesi = str(school_info.get('tahun_sesi', '2026/2027'))
    # Tetapan Zon Masa Malaysia (UTC+8)
    tz_malaysia = timezone(timedelta(hours=8))
    tarikh_hari = datetime.now(tz_malaysia).strftime("%d/%m/%Y %I:%M %p")
    
    jumlah_rekod = 0
    kpi_rows_html = ""
    grouped_rows_html = ""

    if isinstance(df_staff, pd.DataFrame) and not df_staff.empty:
        jumlah_rekod = len(df_staff)
        df_calc = df_staff.copy()
        
        # MENGAMBIL NILAI TERUS DARI ENJIN MYSG_CORE YANG TELAH DIKEMASKINI
        df_calc['Jam_PdP'] = df_calc.get('JUMLAH_JAM_PDP', 0.0).astype(float)
        df_calc['Jam_Port_H'] = df_calc.get('JUMLAH_JAM_PORTFOLIO_H', 0.0).astype(float)
        df_calc['Jam_Port_P'] = df_calc.get('JUMLAH_JAM_PORTFOLIO_P', 0.0).astype(float)
        df_calc['Jam_JK'] = df_calc.get('JUMLAH_JAM_JAWATANKUASA', 0.0).astype(float)
        df_calc['Jam_Total'] = df_calc['Jam_PdP'] + df_calc['Jam_Port_H'] + df_calc['Jam_Port_P'] + df_calc['Jam_JK']

        def classify_group(row):
            jawatan = str(row.get('Jawatan', '')).upper()
            kumpulan = str(row.get('Kumpulan', '')).upper()
            if 'GURU BESAR' in jawatan or 'GPK' in jawatan or 'PENGETUA' in jawatan:
                return '1. Pengurusan & Pentadbir'
            elif 'PERPUSTAKAAN' in jawatan or 'DATA' in jawatan or 'PEMULIHAN' in jawatan:
                return '3. Guru Lantikan Khusus'
            elif 'AKP' in kumpulan or 'PELAKSANA' in kumpulan or 'PEMBANTU' in jawatan:
                return '4. Anggota Pelaksana (AKP)'
            else:
                return '2. Guru Akademik / Subjek'

        df_calc['Kategori_Kumpulan'] = df_calc.apply(classify_group, axis=1)
        groups = sorted(df_calc['Kategori_Kumpulan'].unique())
        global_counter = 1

        for grp in groups:
            sub_df = df_calc[df_calc['Kategori_Kumpulan'] == grp]
            count = len(sub_df)
            pdp_avg = round(sub_df['Jam_PdP'].mean(), 1)
            port_avg = round((sub_df['Jam_Port_H'] + sub_df['Jam_Port_P']).mean(), 1)
            jk_avg = round(sub_df['Jam_JK'].mean(), 1)
            tot_avg = round(sub_df['Jam_Total'].mean(), 1)

            # JULAT IDEAL BAHARU SELARAS JPA (37.0 - 45.0 Jam)
            ideal_pct = round((len(sub_df[(sub_df['Jam_Total'] >= 37.0) & (sub_df['Jam_Total'] <= 45.0)]) / count) * 100, 1)
            status_grp = "🟢 SEIMBANG (MYSG)" if ideal_pct >= 50 else "🟡 PERLU SELARAS"

            kpi_rows_html += f"""
            <tr>
                <td style="font-weight: bold; text-align: left; font-size: 8pt;">{grp}</td>
                <td style="text-align: center; font-size: 8pt;">{count}</td>
                <td style="text-align: center; font-size: 8pt;">{pdp_avg} jam</td>
                <td style="text-align: center; font-size: 8pt;">{port_avg} jam</td>
                <td style="text-align: center; font-size: 8pt;">{jk_avg} jam</td>
                <td style="text-align: center; font-weight: bold; font-size: 8pt; background-color: #f2f2f2;">{tot_avg} jam</td>
                <td style="text-align: center; font-size: 8pt;">{ideal_pct}%</td>
                <td style="text-align: center; font-size: 8pt; font-weight: bold;">{status_grp}</td>
            </tr>
            """

            grouped_rows_html += f"""
            <tr style="background-color: #e0e0e0; font-weight: bold;">
                <td colspan="9" style="text-align: left; font-size: 8.5pt; padding: 5px 8px; text-transform: uppercase;">
                    📌 {grp} ({count} REKOD)
                </td>
            </tr>
            """

            for _, row in sub_df.iterrows():
                nama = str(row.get('Nama', '-')).strip().upper()
                jawatan = str(row.get('Jawatan', '-')).replace('(nan)', '').replace('nan', '').strip()
                gred = str(row.get('Gred', '-')).replace('(nan)', '').replace('nan', '').strip()
                jawatan_gred = f"{jawatan} ({gred})" if (gred and gred != '-') else jawatan

                jam_pdp = round(row['Jam_PdP'], 1)
                jam_port_h = round(row['Jam_Port_H'], 1)
                jam_port_p = round(row['Jam_Port_P'], 1)
                jam_jk = round(row['Jam_JK'], 1)
                total = round(row['Jam_Total'], 1)

                # AMBANG STATUS BAHARU SELARAS JPA 45 JAM
                if total > 45.0:
                    status_agihan = "<span style='color: #8b0000; font-weight: bold;'>🔴 TINGGI</span>"
                elif total >= 37.0:
                    status_agihan = "<span style='color: #2e7d32; font-weight: bold;'>🟢 SEIMBANG</span>"
                else:
                    status_agihan = "<span style='color: #1e429f; font-weight: bold;'>🔵 RINGAN</span>"

                grouped_rows_html += f"""
                <tr>
                    <td style="text-align: center; font-size: 8pt;">{global_counter}</td>
                    <td style="font-size: 8pt; white-space: nowrap; font-weight: bold;">{nama}</td>
                    <td style="font-size: 8pt; white-space: nowrap;">{jawatan_gred}</td>
                    <td style="text-align: center; font-size: 8pt;">{jam_pdp}</td>
                    <td style="text-align: center; font-size: 8pt; font-weight: bold; color: #0f4c81;">{jam_port_h}</td>
                    <td style="text-align: center; font-size: 8pt;">{jam_port_p}</td>
                    <td style="text-align: center; font-size: 8pt;">{jam_jk}</td>
                    <td style="text-align: center; font-weight: bold; font-size: 8pt; background-color: #f9f9f9;">{total}</td>
                    <td style="text-align: center; font-size: 8pt; white-space: nowrap;">{status_agihan}</td>
                </tr>
                """
                global_counter += 1

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
                padding: 4px 6px;
                font-size: 8pt !important;
                background-color: #f2f2f2;
                font-weight: bold;
                text-align: center;
            }}
            
            .landscape-table td {{
                border: 1px solid #000;
                padding: 3px 5px;
                font-size: 8pt !important;
            }}

            .kpi-table {{
                width: 100% !important;
                border-collapse: collapse;
                margin-bottom: 12px;
            }}

            .kpi-table th {{
                border: 1px solid #000;
                padding: 4px 6px;
                font-size: 8pt !important;
                background-color: #d9d9d9;
                font-weight: bold;
                text-align: center;
            }}

            .kpi-table td {{
                border: 1px solid #000;
                padding: 3px 5px;
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

        <!-- JADUAL 1: RINGKASAN KPI KUMPULAN -->
        <div style="font-size: 8.5pt; font-weight: bold; margin-bottom: 4px;">A. ANALISIS KPI BEBAN KERJA MENGIKUT KUMPULAN KAKITANGAN:</div>
        <table class="kpi-table">
            <thead>
                <tr>
                    <th style="width: 25%; text-align: left;">KUMPULAN KAKITANGAN</th>
                    <th style="width: 8%;">BIL ANGGOTA</th>
                    <th style="width: 12%;">PURATA PDP</th>
                    <th style="width: 14%;">PURATA PORTFOLIO (H+P)</th>
                    <th style="width: 12%;">PURATA JK (J)</th>
                    <th style="width: 13%;">PURATA JUMLAH BEBAN</th>
                    <th style="width: 8%;">% AGIHAN IDEAL</th>
                    <th style="width: 8%;">STATUS MYSG</th>
                </tr>
            </thead>
            <tbody>
                {kpi_rows_html}
            </tbody>
        </table>

        <!-- JADUAL 2: SENARAI KAKITANGAN TERKELAS MENGIKUT KUMPULAN -->
        <div style="font-size: 8.5pt; font-weight: bold; margin-bottom: 4px; margin-top: 10px;">B. SENARAI PERINCIAN BEBAN KERJA INDIVIDU WARGA SEKOLAH:</div>
        <table class="landscape-table">
            <thead>
                <tr>
                    <th style="width: 3%;">BIL</th>
                    <th style="width: 25%; text-align: left;">NAMA PEGAWAI</th>
                    <th style="width: 22%; text-align: left;">JAWATAN & GRED</th>
                    <th style="width: 8%;">PDP (JAM)</th>
                    <th style="width: 9%;">PORTFOLIO H / PERSEDIAAN (JAM)</th>
                    <th style="width: 9%;">PORTFOLIO P (JAM)</th>
                    <th style="width: 10%;">JAWATANKUASA J (JAM)</th>
                    <th style="width: 8%;">JUMLAH BEBAN</th>
                    <th style="width: 6%;">STATUS AGIHAN</th>
                </tr>
            </thead>
            <tbody>
                {grouped_rows_html}
            </tbody>
        </table>

        <!-- KOTAK GABUNGAN LENGKAP KETETAPAN MYSG KPM -->
        <div style="border: 1px dashed #0f4c81; background-color: #fcfdfe; border-radius: 4px; padding: 6px 10px; font-size: 7.5pt; line-height: 1.35; margin-top: 8px; color: #222; page-break-inside: avoid;">
            <div style="font-weight: bold; color: #c0392b; margin-bottom: 4px; text-transform: uppercase;">
                📌 KETETAPAN & GARIS PANDUAN PENGIRAAN BEBAN KERJA (MYSG KPM)
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2px 15px; border-bottom: 1px solid #e0e0e0; padding-bottom: 4px; margin-bottom: 4px; font-weight: 500;">
                <div>• <b>Masa Asas 45 Jam:</b> Ditetapkan JPA selaras dengan <i>International Labour Organization</i> (ILO).</div>
                <div>• <b>Pelaksanaan Masa 45 Jam (PGB & AKP):</b> Berdasarkan waktu bekerja pejabat (38 jam 30 minit bekerja + 6 jam 30 minit rehat).</div>
                <div>• <b>Pelaksanaan Masa 45 Jam (Guru):</b> Gabungan Waktu Persekolahan (PdP & Bukan PdP) + Luar Waktu Persekolahan (Kokurikulum & Lain-lain/Rencam).</div>
                <div>• <b>Tugasan Cuti Sekolah:</b> PGB boleh mengarahkan guru bertugas cuti sekolah maksimum separuh daripada jumlah hari cuti (Maks. 22 Hari/Tahun).</div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2px 15px;">
                <div>• <b>1. Pentadbir:</b> PdP minimum (3.0–6.0 Jam/Minggu). Fokus Portfolio Hakiki (Kod H) & Kepimpinan JK (Kod J).</div>
                <div>• <b>2. Guru Akademik:</b> Beban optimum (37.0 - 45.0 Jam/Minggu). Lebih 45 Jam dikira beban <b>TINGGI</b>.</div>
                <div>• <b>3. Guru Khusus (GPM/Data):</b> Pengurangan PdP untuk menampung masa pengurusan hakiki.</div>
                <div>• <b>4. AKP:</b> Masa kerja pejabat operasi (40.0 Jam/Minggu). Beban sampingan (Kod P/J) terhad.</div>
            </div>
        </div>

        <div class="print-footer-container">
            <div><i>Dokumen Rasmi Dijana Menerusi Sistem Pengurusan Beban Kerja MySG KPM ({kod_sekolah}) | Tarikh Cetakan: <b>{tarikh_cetak}</b></i></div>
            <div style="white-space: nowrap; font-weight: bold;">[ Halaman 1 daripada 1 ]</div>
        </div>

        <script>
            window.onload = function() {{ window.print(); }};
        </script>
    </body>
    </html>
    """
