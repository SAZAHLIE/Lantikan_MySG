"""
========================================================================
MYSG KPM: MODUL PENJANAAN SURAT LANTIKAN & LAPORAN INDIVIDU (A4 PORTRAIT)
========================================================================
"""

import pandas as pd
from datetime import datetime
from letterhead_template import (
    get_official_letterhead, 
    get_official_letter_footer, 
    get_a4_print_css
)
from letter_footer import get_appointment_letter_footer_html

def get_malay_official_date():
    """Menjana tarikh rasmi format JPA/KPM Bahasa Melayu tanpa 'hb' dan bulan HURUF BESAR."""
    bulan_dict = {
        1: "JANUARI", 2: "FEBRUARI", 3: "MAC", 4: "APRIL",
        5: "MEI", 6: "JUN", 7: "JULAI", 8: "OGOS",
        9: "SEPTEMBER", 10: "OKTOBER", 11: "NOVEMBER", 12: "DISEMBER"
    }
    now = datetime.now()
    return f"{now.day} {bulan_dict[now.month]} {now.year}"

def generate_appointment_letter_html(staf_row, school_info, *args, **kwargs):
    """Menjana HTML Surat Lantikan Tugas Rasmi."""
    if not isinstance(school_info, dict):
        school_info = {}

    header_html = get_official_letterhead(school_info)
    footer_garis_html = get_appointment_letter_footer_html(school_info)
    css_theme = get_a4_print_css(orientation='portrait')

    nama = str(staf_row.get('Nama', 'ABDUL SABAH @ MOHD SABA B MOHD')).upper()
    ic_no = str(staf_row.get('No_KP', '-')).replace('nan', '-').replace('None', '-')
    if not ic_no or ic_no == 'nan':
        ic_no = '-'

    tahun_sesi = str(school_info.get('tahun_sesi', '2027'))
    nama_gb = str(school_info.get('nama_gb', 'SAZAHLIE BIN SAPAR')).upper()
    jawatan_gb = str(school_info.get('jawatan_gb', 'Pengetua / Guru Besar'))
    nama_sekolah = str(school_info.get('nama_sekolah', 'SEKOLAH KEBANGSAAN BANDAR SANDAKAN')).upper()
    kod_sekolah = str(school_info.get('kod_sekolah', 'XBA2004')).upper()

    ruj_prefix = school_info.get('ruj_kami_prefix', f"KP/{kod_sekolah}/MYSG/{tahun_sesi.split('/')[0]}/")
    if not ruj_prefix.endswith('/'):
        ruj_prefix += '/'
    
    ruj_kami_formatted = f"<span style='white-space: nowrap;'>{ruj_prefix}( &nbsp;&nbsp;&nbsp;&nbsp; )</span>"

    tarikh_rasmi = get_malay_official_date()
    jawatan_hakiki = str(staf_row.get('Tugas_Hakiki', staf_row.get('Jawatan', 'HR24 | PEMBANTU TADBIR (P/O)'))).strip()

    # 1. PDP LIST (2.1.X)
    pdp_html_list = ""
    pdp_list = staf_row.get('SENARAI_DETAIL_PDP', [])
    if isinstance(pdp_list, list) and len(pdp_list) > 0:
        for idx, item in enumerate(pdp_list, start=1):
            subjek = item.get('subjek', '-')
            kelas = item.get('kelas', '-')
            waktu = item.get('waktu', '2')
            pdp_html_list += f"<div style='margin-bottom: 2px; padding-left: 20px;'>2.1.{idx}. Mengajar {subjek}, {kelas} ({waktu} Waktu)</div>"
    else:
        default_pdp_items = [
            "Pend. Seni Visual, 1B (2 Waktu)",
            "Pend. Seni Visual, 2B (2 Waktu)",
            "Pend. Seni Visual, 2C (2 Waktu)",
            "Sains, 1A (3 Waktu)",
            "Sains, 1B (3 Waktu)",
            "Sains, 1C (3 Waktu)",
            "Sains, 2A (3 Waktu)",
            "Sains, 2B (3 Waktu)",
            "Sains, 2C (9 Waktu)"
        ]
        for idx, item_str in enumerate(default_pdp_items, start=1):
            pdp_html_list += f"<div style='margin-bottom: 2px; padding-left: 20px;'>2.1.{idx}. Mengajar {item_str}</div>"

    # 2. PORTFOLIO TANPA JAWATAN (2.2.X)
    p_html_list = ""
    p_list = staf_row.get('SENARAI_DETAIL_PORTFOLIO_P', [])
    if isinstance(p_list, list) and len(p_list) > 0:
        for idx, item in enumerate(p_list, start=1):
            kod_p = item.get('kod', 'P')
            perincian_p = item.get('perincian', '-')
            p_html_list += f"<div style='margin-bottom: 2px; padding-left: 20px;'>2.2.{idx}. {kod_p} | {perincian_p}</div>"
    else:
        default_p_items = [
            "PR01 | Guru Kelas: Pembantu Tahun 1C",
            "PR02 | Guru Bertugas Harian: K2 (Sesi Petang)",
            "PR08 | Ketua Panitia: Pendidikan Seni Visual",
            "PR19 | Guru Penasihat Unit-Unit Kokurikulum: Guru Penasihat BSMM",
            "PR19 | Guru Penasihat Unit-Unit Kokurikulum: Guru Penasihat Kelab Pencegah Jenayah / PPDa",
            "PR19 | Guru Penasihat Unit-Unit Kokurikulum: Guru Penasihat Kelab Permainan Dalam"
        ]
        for idx, item_str in enumerate(default_p_items, start=1):
            p_html_list += f"<div style='margin-bottom: 2px; padding-left: 20px;'>2.2.{idx}. {item_str}</div>"

    # 3. JAWATANKUASA (2.3.X)
    j_html_list = ""
    j_list = staf_row.get('SENARAI_DETAIL_JAWATANKUASA', [])
    if isinstance(j_list, list) and len(j_list) > 0:
        for idx, item in enumerate(j_list, start=1):
            kod_j = item.get('kod', 'J')
            perincian_j = item.get('perincian', '-')
            j_html_list += f"<div style='margin-bottom: 2px; padding-left: 20px;'>2.3.{idx}. {kod_j} | {perincian_j}</div>"
    else:
        default_j_items = [
            "JR01 | JK Pengurusan Sekolah: Penyelaras Bilik PSV",
            "JR12 | JK Pengurusan Kurikulum: Penyelaras PBD",
            "JR16 | JK Pengurusan Hal Ehwal Murid (HEM): AJK Unit Kantin",
            "JR16 | JK Pengurusan Hal Ehwal Murid (HEM): AJK Unit Pengawas",
            "JR16 | JK Pengurusan Hal Ehwal Murid (HEM): Ketua Unit PIBKS"
        ]
        for idx, item_str in enumerate(default_j_items, start=1):
            j_html_list += f"<div style='margin-bottom: 2px; padding-left: 20px;'>2.3.{idx}. {item_str}</div>"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="ms">
    <head>
        <meta charset="UTF-8">
        <title>Surat Lantikan - {nama}</title>
        <style>
            {css_theme}
            
            @page {{
                size: A4 portrait;
                margin: 1.8cm 2.2cm 1.8cm 2.2cm;
            }}

            html, body {{
                font-family: Arial, Helvetica, sans-serif;
                font-size: 10.5pt;
                color: #000000;
                line-height: 1.35;
                margin: 0;
                padding: 0;
            }}

            .ref-block-table {{
                width: 100%;
                margin-bottom: 11pt;
                font-size: 10.5pt;
                border-collapse: collapse;
            }}
            .ref-block-table td {{
                padding: 1px 0;
                vertical-align: top;
            }}

            .title-box {{ 
                font-weight: bold; 
                font-size: 10.5pt; 
                text-transform: uppercase; 
                margin-top: 11pt;
                margin-bottom: 11pt;
                line-height: 1.35;
            }}

            .content-p {{ 
                text-align: justify; 
                margin-bottom: 11pt;
                line-height: 1.35; 
                font-size: 10.5pt; 
            }}

            .section-group {{
                margin-bottom: 11pt;
                page-break-inside: avoid; /* Mengelakkan senarai terpotong ke halaman baru */
            }}

            .section-sub-title {{
                font-weight: bold;
                margin-top: 2px;
                margin-bottom: 2px;
                text-transform: uppercase;
            }}

            .page-continuation {{
                text-align: right;
                font-size: 9.5pt;
                font-family: Arial, sans-serif;
                margin-top: 11pt;
                margin-bottom: 11pt;
            }}

            /* TEKS PENAFIAN SEBAGAI ISI SURAT (SAIZ FON 5PT) */
            .letter-disclaimer-content {{
                margin-top: 18pt;
                padding-top: 2pt;
                font-size: 5pt !important;
                color: #555555;
                font-family: Arial, sans-serif;
                text-align: left;
            }}
        </style>
    </head>
    <body>
        <div>
            {header_html}

            <!-- BLOK RUJUKAN & TARIKH RASMI -->
            <table class="ref-block-table">
                <tr>
                    <td style="width: 45%;"></td>
                    <td style="width: 55%;">
                        <table style="width: 100%; border-collapse: collapse; font-size: 10.5pt; text-align: left;">
                            <tr>
                                <td style="width: 28%; white-space: nowrap; text-align: left;">Ruj. Kami</td>
                                <td style="width: 4%; text-align: center;">:</td>
                                <td style="width: 68%; text-align: left; font-weight: normal; white-space: nowrap;">{ruj_kami_formatted}</td>
                            </tr>
                            <tr>
                                <td style="text-align: left; white-space: nowrap;">Tarikh</td>
                                <td style="text-align: center;">:</td>
                                <td style="text-align: left; font-weight: normal; white-space: nowrap;">{tarikh_rasmi}</td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>

            <!-- MAKLUMAT PEGAWAI -->
            <div style="font-weight: bold; font-size: 10.5pt; line-height: 1.25; margin-bottom: 11pt;">
                {nama}<br>
                <span style="font-weight: normal;">No. KP: {ic_no}</span>
            </div>

            <div style="font-size: 10.5pt; margin-bottom: 11pt;">Tuan/Puan,</div>

            <!-- TAJUK SURAT -->
            <div class="title-box">
                SURAT LANTIKAN DAN AGIHAN TUGAS BAGI SESI PERSEKOLAHAN TAHUN {tahun_sesi}
            </div>

            <div class="content-p">
                Dengan segala hormatnya perkara di atas adalah dirujuk bersama perkara-perkara berkaitan di bawah Akta Pendidikan 1996, Surat-surat Pekeliling Ikhtisas (SPI), serta arahan dan garis panduan MySG KPM yang berkuat kuasa.
            </div>
            
            <div class="content-p">
                2. Sukacita dimaklumkan bahawa pihak sekolah melantik tuan/puan untuk memegang jawatan dan melaksanakan amanah seperti berikut berkuat kuasa mulai tarikh surat ini dikeluarkan:
            </div>

            <!-- 2.1. JAWATAN BERPORTFOLIO -->
            <div class="section-group" style="margin-left: 10px;">
                <div class="section-sub-title">2.1. JAWATAN BERPORTFOLIO: {jawatan_hakiki}</div>
                {pdp_html_list}
            </div>

            <!-- 2.2. PORTFOLIO TANPA JAWATAN -->
            <div class="section-group" style="margin-left: 10px;">
                <div class="section-sub-title">2.2. PORTFOLIO TANPA JAWATAN:</div>
                {p_html_list}
            </div>

            <!-- 2.3. JAWATANKUASA -->
            <div class="section-group" style="margin-left: 10px;">
                <div class="section-sub-title">2.3. JAWATANKUASA:</div>
                {j_html_list}
            </div>

            <!-- PENOMBORAN MUKA SURAT SAMBUNGAN PERTAMA -->
            <div class="page-continuation">
                ...2
            </div>

            <div class="content-p">
                3. Sehubungan dengan itu, tuan/puan dinasihatkan untuk merujuk dan memahami tugas serta tanggungjawab yang ditetapkan selaras dengan Garis Panduan Tadbir Urus Sekolah (MySG KPM).
            </div>

            <div class="content-p">
                4. Semoga tuan/puan dapat menjalankan tugas yang diamanahkan dengan komitmen dan akauntabiliti yang tinggi.
            </div>

            <div class="content-p">
                Sekian, terima kasih.
            </div>

            <!-- MOTTO/SLOGAN: 1 BARIS LANGKAU -->
            <div style="font-weight: bold; text-transform: uppercase; font-size: 10.5pt; margin-top: 11pt; margin-bottom: 11pt;">
                "MALAYSIA MADANI"<br><br>
                "BERKHIDMAT UNTUK NEGARA"
            </div>

            <div style="font-size: 10.5pt; margin-bottom: 11pt;">Saya yang menjalankan amanah,</div>

            <!-- LANGKAU 3 BARIS UNTUK TANDATANGAN -->
            <div style="margin-top: 33pt; font-weight: bold; text-transform: uppercase; font-size: 10.5pt;">
                ({nama_gb})<br>
                <span style="font-weight: normal; text-transform: none;">
                    {jawatan_gb}<br>
                    {nama_sekolah}
                </span>
            </div>

            <!-- TEKS PENAFIAN MYSG KPM (SAIZ FONT 5PT SEBAGAI ISI SURAT) -->
            <div class="letter-disclaimer-content">
                <i>Dokumen Rasmi Dijana Menerusi MySG KPM: Sistem Pengurusan & Analisis Beban Kerja ({kod_sekolah})</i>
            </div>

            <!-- KAKI SURAT (GARISAN HITAM LURUS) -->
            {footer_garis_html}
        </div>

        <script>
            window.onload = function() {{ window.print(); }};
        </script>
    </body>
    </html>
    """
    return html_content

def generate_individual_detailed_report_html(staf_row, school_info=None, df_all_staff=None, *args, **kwargs):
    """Menjana LAPORAN PERINCIAN BEBAN TUGAS INDIVIDU (Strict Fit 1 Page A4 Portrait)."""
    if not isinstance(school_info, dict):
        school_info = {}

    header_html = get_official_letterhead(school_info)
    footer_html = get_official_letter_footer(school_info)
    css_theme = get_a4_print_css(orientation='portrait')

    nama = str(staf_row.get('Nama', '-')).upper()
    gred = str(staf_row.get('Gred', '-')).replace('(nan)', '').replace('nan', '').strip()
    gred_show = gred if gred else '-'

    jawatan_hakiki = str(staf_row.get('Tugas_Hakiki', staf_row.get('Jawatan', 'HR12 | Guru Akademik KSSR'))).strip()
    kump_staf = str(staf_row.get('Kumpulan', 'Guru')).strip()
    
    tahun_sesi = str(school_info.get('tahun_sesi', '2027'))
    kod_sekolah = str(school_info.get('kod_sekolah', 'XBA2004')).upper()
    
    tarikh_hari = datetime.now().strftime("%d/%m/%Y")

    total_jam = round(float(staf_row.get('JUMLAH_BEBAN_KESELURAHAN', 27.0) or 0.0), 1)
    purata_kumpulan = 21.9

    # Penyelesaian Isu KeyError / Crash pada df_all_staff
    if isinstance(df_all_staff, pd.DataFrame) and not df_all_staff.empty and 'JUMLAH_BEBAN_KESELURAHAN' in df_all_staff.columns:
        if 'Kumpulan' in df_all_staff.columns:
            sub_kump = df_all_staff[df_all_staff['Kumpulan'] == kump_staf]
        else:
            sub_kump = df_all_staff
            
        if not sub_kump.empty:
            purata_kumpulan = round(float(sub_kump['JUMLAH_BEBAN_KESELURAHAN'].mean()), 1)

    diff_jam = round(total_jam - purata_kumpulan, 1)
    diff_text = f"+{diff_jam} jam dari purata" if diff_jam >= 0 else f"{diff_jam} jam dari purata"
    color_diff = "#d9534f" if diff_jam > 0 else "#2e7d32"

    if total_jam > 35.0 if 'AKP' in kump_staf.upper() or 'PELAKSANA' in kump_staf.upper() else total_jam > 32.0:
        badge_status = '<span style="background-color: #fde8e8; color: #9b1c1c; padding: 2px 6px; border-radius: 10px; font-weight: bold; font-size: 7.5pt;">🔴 AGIHAN TINGGI</span>'
    elif total_jam >= 20.0:
        badge_status = '<span style="background-color: #def7ec; color: #03543f; padding: 2px 6px; border-radius: 10px; font-weight: bold; font-size: 7.5pt;">🟢 SEIMBANG (IDEAL)</span>'
    else:
        badge_status = '<span style="background-color: #e1effe; color: #1e429f; padding: 2px 6px; border-radius: 10px; font-weight: bold; font-size: 7.5pt;">🔵 RINGAN</span>'

    rows_h_html = f"""
    <tr style="background-color: #fafafa;">
        <td style="padding-left: 12px;">• &nbsp; <b>{jawatan_hakiki}</b> <span style="color: #666; font-size: 7.5pt;">(Jawatan Hakiki Rasmi)</span></td>
        <td style="text-align: right; font-weight: bold; width: 20%; color: #0f4c81;">0.0 jam</td>
    </tr>
    """
    
    pdp_list = staf_row.get('SENARAI_DETAIL_PDP', [])
    if isinstance(pdp_list, list) and len(pdp_list) > 0:
        for idx_p, item in enumerate(pdp_list):
            subjek = item.get('subjek', '-')
            kelas = item.get('kelas', '-')
            waktu = item.get('waktu', '2')
            jam_val = round(float(waktu) * 0.5, 1)
            bg_color = "#ffffff" if idx_p % 2 == 0 else "#fbfcfd"
            rows_h_html += f"""
            <tr style="background-color: {bg_color};">
                <td style="padding-left: 12px;">• &nbsp; {subjek} ({kelas}) • <i style="color: #555;">{waktu} Waktu</i></td>
                <td style="text-align: right; font-weight: bold; color: #2b579a;">{jam_val:.1f} jam</td>
            </tr>
            """
    else:
        default_pdp = [
            ("Pend. Seni Visual (4A)", "2 Waktu", 1.0),
            ("Pend. Seni Visual (4B)", "2 Waktu", 1.0),
            ("Pend. Seni Visual (4C)", "2 Waktu", 1.0),
            ("Pend. Seni Visual (5B)", "2 Waktu", 1.0),
            ("Pend. Seni Visual (6A)", "2 Waktu", 1.0),
            ("Pend. Seni Visual (6B)", "2 Waktu", 1.0),
            ("Sains (6A)", "4 Waktu", 2.0),
            ("Sains (6B)", "4 Waktu", 2.0),
            ("Sains (6C)", "4 Waktu", 2.0),
        ]
        for idx_p, (sbj, wk, jm) in enumerate(default_pdp):
            bg_color = "#ffffff" if idx_p % 2 == 0 else "#fbfcfd"
            rows_h_html += f"""
            <tr style="background-color: {bg_color};">
                <td style="padding-left: 12px;">• &nbsp; {sbj} • <i style="color: #555;">{wk}</i></td>
                <td style="text-align: right; font-weight: bold; color: #2b579a;">{jm:.1f} jam</td>
            </tr>
            """

    rows_p_html = ""
    p_list = staf_row.get('SENARAI_DETAIL_PORTFOLIO_P', [])
    if isinstance(p_list, list) and len(p_list) > 0:
        for idx_p, item in enumerate(p_list):
            kod_p = item.get('kod', 'P')
            perincian_p = item.get('perincian', '-')
            jam_val = round(float(item.get('jam', 1.5)), 1)
            bg_color = "#ffffff" if idx_p % 2 == 0 else "#fbfcfd"
            rows_p_html += f"""
            <tr style="background-color: {bg_color};">
                <td style="padding-left: 12px;">• &nbsp; <b>{kod_p}</b> | {perincian_p}</td>
                <td style="text-align: right; font-weight: bold; color: #2b579a;">{jam_val:.1f} jam</td>
            </tr>
            """
    else:
        default_p = [
            ("PR01 | Guru Kelas", "Pembantu Tahun 5B", 2.0),
            ("PR08 | Ketua Panitia Mata Pelajaran", "Sains", 2.0),
            ("PR02 | Guru Bertugas Harian", "K1 (Sesi Pagi)", 1.5),
            ("PR19 | Guru Penasihat Unit Kokurikulum", "Guru Penasihat Bola Jaring", 1.5),
            ("PR19 | Guru Penasihat Unit Kokurikulum", "Guru Penasihat PPIM", 1.5),
            ("PR19 | Guru Penasihat Unit Kokurikulum", "Guru Penasihat Sains Dan Matematik", 1.5),
        ]
        for idx_p, (kd, dsc, jm) in enumerate(default_p):
            bg_color = "#ffffff" if idx_p % 2 == 0 else "#fbfcfd"
            rows_p_html += f"""
            <tr style="background-color: {bg_color};">
                <td style="padding-left: 12px;">• &nbsp; <b>{kd}</b> • <i style="color: #555;">{dsc}</i></td>
                <td style="text-align: right; font-weight: bold; color: #2b579a;">{jm:.1f} jam</td>
            </tr>
            """

    rows_j_html = ""
    j_list = staf_row.get('SENARAI_DETAIL_JAWATANKUASA', [])
    if isinstance(j_list, list) and len(j_list) > 0:
        for idx_j, item in enumerate(j_list):
            kod_j = item.get('kod', 'J')
            perincian_j = item.get('perincian', '-')
            jam_val = round(float(item.get('jam', 1.0)), 1)
            bg_color = "#ffffff" if idx_j % 2 == 0 else "#fbfcfd"
            rows_j_html += f"""
            <tr style="background-color: {bg_color};">
                <td style="padding-left: 12px;">• &nbsp; <b>{kod_j}</b> | {perincian_j}</td>
                <td style="text-align: right; font-weight: bold; color: #2b579a;">{jam_val:.1f} jam</td>
            </tr>
            """
    else:
        default_j = [
            ("JR01 | JK Pengurusan Sekolah", "Penyelaras Bilik Sains", 1.0),
            ("JR01 | JK Pengurusan Sekolah", "Penyelaras EKSA", 1.0),
            ("JR01 | JK Pengurusan Sekolah", "PR06", 1.0),
            ("JR16 | JK Pengurusan Hal Ehwal Murid (HEM)", "AJK Unit Kantin", 1.0),
            ("JR18 | JK Pengurusan 3K", "AJK Unit Kesihatan", 1.0),
            ("JR18 | JK Pengurusan 3K", "Ketua Unit Keceriaan & Kebersihan", 1.0),
        ]
        for idx_j, (kd, dsc, jm) in enumerate(default_j):
            bg_color = "#ffffff" if idx_j % 2 == 0 else "#fbfcfd"
            rows_j_html += f"""
            <tr style="background-color: {bg_color};">
                <td style="padding-left: 12px;">• &nbsp; <b>{kd}</b> • <i style="color: #555;">{dsc}</i></td>
                <td style="text-align: right; font-weight: bold; color: #2b579a;">{jm:.1f} jam</td>
            </tr>
            """

    html_content = f"""
    <!DOCTYPE html>
    <html lang="ms">
    <head>
        <meta charset="UTF-8">
        <title>Laporan Perincian Beban Tugas Individu - {nama}</title>
        <style>
            {css_theme}
            
            @page {{
                size: A4 portrait;
                margin: 0.5cm 1.0cm 0.5cm 1.0cm;
            }}

            html, body {{
                height: 100%;
                font-family: Arial, Helvetica, sans-serif;
                font-size: 8.5pt;
                color: #222;
                margin: 0;
                padding: 0;
            }}

            .page-container {{
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                min-height: 98vh;
                box-sizing: border-box;
                page-break-inside: avoid;
            }}

            .doc-title {{
                border: 1.5px solid #0f4c81;
                border-radius: 4px;
                font-weight: bold;
                font-size: 10pt;
                text-align: center;
                text-transform: uppercase;
                padding: 4px;
                margin-bottom: 6px;
                background-color: #f0f4f8;
                color: #0f4c81;
                letter-spacing: 0.5px;
            }}

            .header-info-table {{
                width: 100%;
                border-collapse: collapse;
                font-size: 8.5pt;
                margin-bottom: 6px;
            }}
            .header-info-table td {{
                padding: 2px 4px;
                vertical-align: top;
            }}

            .metric-container {{
                display: flex;
                border: 1px solid #d0e1fd;
                background-color: #f8fbff;
                border-radius: 4px;
                margin-bottom: 8px;
                padding: 4px 0;
            }}
            .metric-box {{
                flex: 1;
                text-align: center;
                border-right: 1px solid #d0e1fd;
            }}
            .metric-box:last-child {{
                border-right: none;
            }}
            .metric-label {{
                font-size: 7.5pt;
                color: #555;
                font-weight: bold;
                margin-bottom: 1px;
                text-transform: uppercase;
            }}
            .metric-value {{
                font-size: 11.5pt;
                font-weight: bold;
                color: #0f4c81;
            }}

            .section-bar {{
                background-color: #e8f1f5;
                color: #0f4c81;
                font-weight: bold;
                font-size: 8pt;
                padding: 3px 8px;
                border-top: 1px solid #b8d4e3;
                border-bottom: 1px solid #b8d4e3;
                border-radius: 2px;
                text-transform: uppercase;
                display: flex;
                justify-content: space-between;
                margin-top: 2px;
            }}

            .detail-table {{
                width: 100%;
                border-collapse: collapse;
                font-size: 8pt;
                margin-bottom: 4px;
                page-break-inside: avoid; /* Mengelakkan jadual terpotong ke muka surat baru */
            }}
            .detail-table td {{
                padding: 2px 4px;
                border-bottom: 1px solid #f0f0f0;
            }}

            .guideline-box {{
                border: 1px dashed #0f4c81;
                background-color: #fcfdfe;
                border-radius: 4px;
                padding: 5px 8px;
                font-size: 7pt;
                line-height: 1.35;
                margin-top: 6px;
                color: #222;
            }}
            .guideline-title {{
                font-weight: bold;
                color: #c0392b;
                margin-bottom: 3px;
                text-transform: uppercase;
            }}
        </style>
    </head>
    <body>
        <div class="page-container">
            <div>
                {header_html}

                <div class="doc-title">
                    LAPORAN PERINCIAN BEBAN TUGAS INDIVIDU
                </div>

                <table class="header-info-table">
                    <tr>
                        <td style="width: 58%; text-align: left;">
                            <b>Nama Pegawai:</b> {nama}<br>
                            <b>Jawatan Hakiki:</b> {jawatan_hakiki}<br>
                            <b>Gred Perkhidmatan:</b> {gred_show}
                        </td>
                        <td style="width: 42%; text-align: left;">
                            <b>Kumpulan:</b> {kump_staf}<br>
                            <b>Sesi Persekolahan:</b> {tahun_sesi}<br>
                            <b>Tarikh Cetakan:</b> {tarikh_hari}
                        </td>
                    </tr>
                </table>

                <div class="metric-container">
                    <div class="metric-box">
                        <div class="metric-label">Beban Kerja Pegawai</div>
                        <div class="metric-value">{total_jam:.1f} Jam</div>
                        <div style="margin-top: 1px;">{badge_status}</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Purata Kumpulan ({kump_staf})</div>
                        <div class="metric-value" style="color: #2b579a;">{purata_kumpulan:.1f} Jam</div>
                        <div style="font-size: 7pt; color: #777;">Penanda Aras Ideal MySG</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Kedudukan / Perbezaan</div>
                        <div class="metric-value" style="color: {color_diff};">{diff_text}</div>
                        <div style="font-size: 7pt; color: #777;">Variasi Agihan Tugas</div>
                    </div>
                </div>

                <div style="font-weight: bold; font-size: 8pt; margin-bottom: 2px; color: #0f4c81; text-transform: uppercase;">
                    📋 SENARAI PERINCIAN AGIHAN TUGAS & PEMBERAT (JAM):
                </div>

                <!-- 1. PORTFOLIO HAKIKI & PDP -->
                <div class="section-bar">
                    <span>1. PORTFOLIO BERJAWATAN HAKIKI (KOD H) & PENGAJARAN DAN PEMBELAJARAN (PDP)</span>
                    <span>PEMBERAT JAM</span>
                </div>
                <table class="detail-table">
                    <tbody>
                        {rows_h_html}
                    </tbody>
                </table>

                <!-- 2. PORTFOLIO TANPA JAWATAN -->
                <div class="section-bar">
                    <span>2. PORTFOLIO TANPA JAWATAN (KOD P)</span>
                    <span>PEMBERAT JAM</span>
                </div>
                <table class="detail-table">
                    <tbody>
                        {rows_p_html}
                    </tbody>
                </table>

                <!-- 3. JAWATANKUASA SEKOLAH -->
                <div class="section-bar">
                    <span>3. JAWATANKUASA SEKOLAH (KOD J)</span>
                    <span>PEMBERAT JAM</span>
                </div>
                <table class="detail-table">
                    <tbody>
                        {rows_j_html}
                    </tbody>
                </table>

                <!-- JUMLAH BEBAN KERJA KESELURUHAN -->
                <table style="width: 100%; font-size: 8.5pt; font-weight: bold; margin-top: 3px; margin-bottom: 4px; border-top: 1.5px solid #0f4c81; padding-top: 2px;">
                    <tr>
                        <td style="text-align: right; padding-right: 15px; color: #0f4c81;">JUMLAH BEBAN KERJA KESELURUHAN:</td>
                        <td style="width: 22%; text-align: right; color: #0f4c81; font-size: 9.5pt;">{total_jam:.1f} JAM</td>
                    </tr>
                </table>
            </div>

            <div>
                <!-- MYSG KPM GUIDELINE BOX -->
                <div class="guideline-box">
                    <div class="guideline-title">
                        📌 KETETAPAN & GARIS PANDUAN PENETAPAN BEBAN KERJA WARGA SEKOLAH (MYSG KPM):
                    </div>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1px 10px; border-bottom: 1px solid #e0e0e0; padding-bottom: 3px; margin-bottom: 3px; font-weight: 500;">
                        <div>• <b>Asas Pengiraan PdP:</b> 1 Waktu PdP = 0.5 Jam (30 Minit)</div>
                        <div>• <b>Portfolio Hakiki (Kod H):</b> Berdasarkan Deskripsi Tugas Jawatan Rasmi</div>
                        <div>• <b>Beban Kerja Seimbang:</b> 20.0 – 32.0 Jam/Minggu (PPP) / 40.0 Jam (AKP)</div>
                        <div>• <b>Prinsip Kesaksamaan:</b> Agihan Portfolio (P) & JK (J) dilaksanakan secara adil mengikut purata kumpulan</div>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1px 10px;">
                        <div>• <b>1. Pentadbir:</b> PdP minimum (3.0–6.0 Jam/Minggu). Fokus Portfolio Hakiki (Kod H) & Kepimpinan JK (Kod J).</div>
                        <div>• <b>2. Guru Akademik:</b> Beban seimbang 20.0–32.0 Jam/Minggu (PdP + Portfolio H/P + Maksimum 3–5 Kod J).</div>
                        <div>• <b>3. Guru Khusus (GPM/Data):</b> Pengurangan PdP diberi bagi menampung peruntukan masa pengurusan hakiki.</div>
                        <div>• <b>4. AKP:</b> Masa kerja rasmi operasi pejabat (40.0 Jam/Minggu) tanpa PdP. Penglibatan JK dihadkan (Maksimum 1–2 Kod J).</div>
                    </div>
                </div>

                {footer_html}
            </div>
        </div>

        <script>
            window.onload = function() {{ window.print(); }};
        </script>
    </body>
    </html>
    """
    return html_content