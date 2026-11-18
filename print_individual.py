"""
========================================================================
MYSG KPM: MODUL PENJANAAN SURAT LANTIKAN & LAPORAN INDIVIDU (A4 PORTRAIT)
========================================================================
"""

import pandas as pd
import re
from datetime import datetime
from letterhead_template import (
    get_official_letterhead, 
    get_official_letter_footer, 
    get_a4_print_css
)
from letter_footer import get_appointment_letter_footer_html
from mysg_core import MYSG_PORTFOLIO_H_SM, MYSG_PORTFOLIO_H_SR, MYSG_PORTFOLIO_P, MYSG_JAWATANKUASA_J

def get_malay_official_date():
    """Menjana tarikh rasmi format JPA/KPM Bahasa Melayu tanpa 'hb' dan bulan HURUF BESAR."""
    bulan_dict = {
        1: "JANUARI", 2: "FEBRUARI", 3: "MAC", 4: "APRIL",
        5: "MEI", 6: "JUN", 7: "JULAI", 8: "OGOS",
        9: "SEPTEMBER", 10: "OKTOBER", 11: "NOVEMBER", 12: "DISEMBER"
    }
    now = datetime.now()
    return f"{now.day} {bulan_dict[now.month]} {now.year}"

# -------------------------------------------------------------------
# HELPER FUNCTION: EKSTRAK DATA TERUS DARI LAJUR CSV 
# -------------------------------------------------------------------
def extract_pdp_from_row(staf_row):
    new_list = []
    for i in range(1, 16):
        subjek = staf_row.get(f'Subjek_{i}')
        if pd.notna(subjek) and str(subjek).strip() != '' and str(subjek).strip() != '0':
            kelas = staf_row.get(f'Kelas_{i}', '-')
            waktu = staf_row.get(f'Waktu_{i}', '2')
            new_list.append({'subjek': str(subjek).strip(), 'kelas': str(kelas).strip(), 'waktu': str(waktu).strip()})
    return new_list

def extract_portfolio_from_row(staf_row):
    new_list = []
    for i in range(1, 16):
        kod = staf_row.get(f'Kod_P_{i}')
        if pd.notna(kod) and str(kod).strip() != '' and str(kod).strip() != '0':
            perincian = staf_row.get(f'Detail_P_{i}', '-')
            kod_raw = str(kod).split('|')[0].strip().upper().replace('PR', 'P').replace('PM', 'P')
            jam_val = MYSG_PORTFOLIO_P.get(kod_raw, ('', 1.5))[1]
            new_list.append({'kod': str(kod).strip(), 'perincian': str(perincian).strip(), 'jam': jam_val})
    return new_list

def extract_jk_from_row(staf_row):
    new_list = []
    for i in range(1, 16):
        kod = staf_row.get(f'Kod_J_{i}')
        if pd.notna(kod) and str(kod).strip() != '' and str(kod).strip() != '0':
            perincian = staf_row.get(f'Detail_J_{i}', '-')
            kod_raw = str(kod).split('|')[0].strip().upper().replace('JR', 'J').replace('JM', 'J')
            jam_val = MYSG_JAWATANKUASA_J.get(kod_raw, ('', 1.0))[1]
            new_list.append({'kod': str(kod).strip(), 'perincian': str(perincian).strip(), 'jam': jam_val})
    return new_list

def get_h_portfolio_base_hours(staf_row, jenis_sekolah="Sekolah Rendah"):
    """Dapatkan nilai jam 'Tapak Asas' bagi Portfolio Hakiki (Kod H) dari pangkalan data."""
    is_sm = "Menengah" in str(jenis_sekolah)
    mapping_h = MYSG_PORTFOLIO_H_SM if is_sm else MYSG_PORTFOLIO_H_SR
    
    kod_h_raw = str(staf_row.get('Kod_H_1', '')).split('|')[0].strip().upper()
    
    # PENGECAMAN PINTAR: Fallback jika Kod_H_1 kosong tetapi wujud dalam lajur Jawatan
    if kod_h_raw in ["", "NAN", "NONE", "NULL", "-"]:
        m = re.search(r'(HR|HM)(\d{2})', str(staf_row.get('Jawatan', '')))
        if m:
            kod_h_raw = f"{m.group(1)}{m.group(2)}"
            
    return mapping_h.get(kod_h_raw, ('', 0.0))[1]

def generate_appointment_letter_html(staf_row, school_info, *args, **kwargs):
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
    jawatan_hakiki = str(staf_row.get('Kod_H_1', staf_row.get('Jawatan', 'HR24 | PEMBANTU TADBIR (P/O)'))).strip()

    pdp_html_list = ""
    pdp_list = extract_pdp_from_row(staf_row)
    if len(pdp_list) > 0:
        for idx, item in enumerate(pdp_list, start=1):
            subjek = item.get('subjek', '-')
            kelas = item.get('kelas', '-')
            waktu = item.get('waktu', '2')
            pdp_html_list += f"<div style='margin-bottom: 2px; padding-left: 20px;'>2.1.{idx}. Mengajar {subjek}, {kelas} ({waktu} Waktu)</div>"
    else:
        pdp_html_list += f"<div style='margin-bottom: 2px; padding-left: 20px;'>2.1.1. Tiada Rekod Pengajaran (PdP)</div>"

    p_html_list = ""
    p_list = extract_portfolio_from_row(staf_row)
    if len(p_list) > 0:
        for idx, item in enumerate(p_list, start=1):
            kod_p = item.get('kod', 'P')
            perincian_p = item.get('perincian', '-')
            p_html_list += f"<div style='margin-bottom: 2px; padding-left: 20px;'>2.2.{idx}. {kod_p} | {perincian_p}</div>"
    else:
        p_html_list += f"<div style='margin-bottom: 2px; padding-left: 20px;'>2.2.1. Tiada Portfolio Ditetapkan</div>"

    j_html_list = ""
    j_list = extract_jk_from_row(staf_row)
    if len(j_list) > 0:
        for idx, item in enumerate(j_list, start=1):
            kod_j = item.get('kod', 'J')
            perincian_j = item.get('perincian', '-')
            j_html_list += f"<div style='margin-bottom: 2px; padding-left: 20px;'>2.3.{idx}. {kod_j} | {perincian_j}</div>"
    else:
        j_html_list += f"<div style='margin-bottom: 2px; padding-left: 20px;'>2.3.1. Tiada Jawatankuasa Ditetapkan</div>"

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
                page-break-inside: avoid;
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
    jenis_sek = school_info.get('jenis_sekolah', 'Sekolah Rendah')

    nama = str(staf_row.get('Nama', '-')).upper()
    gred = str(staf_row.get('Gred', '-')).replace('(nan)', '').replace('nan', '').strip()
    gred_show = gred if gred else '-'

    kod_h = str(staf_row.get('Kod_H_1', '')).split('|')[0].strip().upper()
    detail_h = str(staf_row.get('Detail_H_1', '')).upper()
    
    # PENGECAMAN PINTAR UNTUK PAPARAN TAJUK
    if kod_h in ["", "NAN", "NONE", "NULL", "-"]:
        m = re.search(r'(HR|HM)(\d{2})', str(staf_row.get('Jawatan', '')))
        if m:
            kod_h = f"{m.group(1)}{m.group(2)}"
            # Sekadar estetik sekiranya nama jawatan ada di CSV
            detail_h = str(staf_row.get('Jawatan', '')).replace(kod_h, '').replace('|', '').strip().upper()

    jawatan_hakiki = f"{kod_h} | {detail_h}" if (kod_h and kod_h not in ["NAN", "NONE", ""]) else str(staf_row.get('Jawatan', 'HR12 | Guru Akademik KSSR'))
    
    kump_staf = str(staf_row.get('Kumpulan', 'Guru')).strip()
    tahun_sesi = str(school_info.get('tahun_sesi', '2027'))
    kod_sekolah = str(school_info.get('kod_sekolah', 'XBA2004')).upper()
    tarikh_hari = datetime.now().strftime("%d/%m/%Y")

    # MENDAPATKAN NILAI JAM TAPAK ASAS DARI PANGKALAN DATA (FUNGSI HELPER)
    jam_tapak_asas = get_h_portfolio_base_hours(staf_row, jenis_sek)

    # JUMLAH KESELURUHAN & PURATA
    total_jam = round(float(staf_row.get('JUMLAH_BEBAN_KESELURAHAN', 27.0) or 0.0), 1)
    purata_kumpulan = 38.0

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

    if total_jam > 35.0 if 'AKP' in kump_staf.upper() or 'PELAKSANA' in kump_staf
