"""
========================================================================
MYSG KPM: MODUL PENJANAAN SURAT LANTIKAN & LAPORAN INDIVIDU (A4 PORTRAIT)
========================================================================
"""

import pandas as pd
from datetime import datetime
from letterhead_template import (
    get_official_letterhead, 
    get_a4_print_css
)
from letter_footer import get_appointment_letter_footer_html
from mysg_core import MYSG_PORTFOLIO_H_SM, MYSG_PORTFOLIO_H_SR, MYSG_PORTFOLIO_P, MYSG_JAWATANKUASA_J, MYSG_P_TO_J_AUTO_MAP

def get_malay_official_date():
    """Menjana tarikh rasmi format JPA/KPM Bahasa Melayu tanpa 'hb' dan bulan HURUF BESAR."""
    bulan_dict = {
        1: "JANUARI", 2: "FEBRUARI", 3: "MAC", 4: "APRIL",
        5: "MEI", 6: "JUN", 7: "JULAI", 8: "OGOS",
        9: "SEPTEMBER", 10: "OKTOBER", 11: "NOVEMBER", 12: "DISEMBER"
    }
    now = datetime.now()
    return f"{now.day} {bulan_dict[now.month]} {now.year}"

def extract_pdp_from_row(staf_row):
    new_list = []
    for i in range(1, 16):
        subjek = staf_row.get(f'Subjek_{i}')
        if pd.notna(subjek) and str(subjek).strip() != '' and str(subjek).strip() != '0':
            kelas = staf_row.get(f'Kelas_{i}', '-')
            waktu = staf_row.get(f'Waktu_{i}', '2')
            try:
                waktu_val = float(waktu)
            except (ValueError, TypeError):
                waktu_val = 0.0
            new_list.append({'subjek': str(subjek).strip(), 'kelas': str(kelas).strip(), 'waktu': str(waktu_val).replace('.0', '')})
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

def force_get_h_base_hours(staf_row, jenis_sekolah="Sekolah Rendah"):
    jam_h = staf_row.get('JUMLAH_JAM_PORTFOLIO_H', None)
    if pd.notna(jam_h):
        try:
            val = float(jam_h)
            if val > 0: return val
        except (ValueError, TypeError):
            pass
    is_sm = "Menengah" in str(jenis_sekolah)
    mapping_h = MYSG_PORTFOLIO_H_SM if is_sm else MYSG_PORTFOLIO_H_SR
    kod_h_raw = str(staf_row.get('Kod_H_1', '')).split('|')[0].strip().upper()
    return float(mapping_h.get(kod_h_raw, ('', 0.0))[1])

def generate_appointment_letter_html(staf_row, school_info, *args, **kwargs):
    if not isinstance(school_info, dict):
        school_info = {}

    header_html = get_official_letterhead(school_info)
    footer_garis_html = get_appointment_letter_footer_html(school_info)
    css_theme = get_a4_print_css(orientation='portrait')
    jenis_sek = school_info.get('jenis_sekolah', 'Sekolah Rendah')
    prefix_j = "JM" if "Menengah" in str(jenis_sek) else "JR"

    nama = str(staf_row.get('Nama', 'ABDUL SABAH @ MOHD SABA B MOHD')).upper()
    ic_no = str(staf_row.get('No_KP', '-')).replace('nan', '-').replace('None', '-')
    if not ic_no or ic_no == 'nan':
        ic_no = '-'

    tahun_sesi = str(school_info.get('tahun_sesi', '2027'))
    nama_gb = str(school_info.get('nama_gb', 'SAZAHLIE BIN SAPAR')).upper()
    jawatan_gb = str(school_info.get('jawatan_gb', 'Pengetua / Guru Besar'))
    nama_sekolah = str(school_info.get('nama_sekolah', 'SEKOLAH KEBANGSAAN BANDAR SANDAKAN')).upper()
    kod_sekolah = str(school_info.get('kod_sekolah', 'XBA2004')).upper()

    ruj_prefix = str(school_info.get('ruj_kami', f"KP/{kod_sekolah}/MYSG/{tahun_sesi.split('/')[0]}/"))
    ruj_kami_formatted = f"<span style='white-space: nowrap;'>{ruj_prefix}( &nbsp;&nbsp;&nbsp;&nbsp; )</span>"
    tarikh_rasmi = get_malay_official_date()
    jawatan_hakiki = str(staf_row.get('Kod_H_1', staf_row.get('Jawatan', 'HR24 | PEMBANTU TADBIR (P/O)'))).strip()

    # KUMPUL KOD JAWATANKUASA YANG DISERAP
    absorbed_j_codes = []
    for i in range(1, 16):
        p_kod = str(staf_row.get(f'Kod_P_{i}', '')).strip()
        if p_kod and p_kod.lower() not in ['nan', 'none', '-', '']:
            clean_p = p_kod.split('|')[0].strip().replace('PR', 'P').replace('PM', 'P')
            if clean_p in MYSG_P_TO_J_AUTO_MAP:
                absorbed_j_codes.extend(MYSG_P_TO_J_AUTO_MAP[clean_p])

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
            label_p = f"{kod_p} | {MYSG_PORTFOLIO_P.get(kod_p, (kod_p, 0))[0]}" if '|' not in kod_p else kod_p
            dtl_str = f": {perincian_p}" if perincian_p and perincian_p != label_p and perincian_p not in label_p else ""
            p_html_list += f"<div style='margin-bottom: 2px; padding-left: 20px;'>2.2.{idx}. {label_p}{dtl_str}</div>"
    else:
        p_html_list += f"<div style='margin-bottom: 2px; padding-left: 20px;'>2.2.1. Tiada Portfolio Ditetapkan</div>"

    # JAWATANKUASA (GABUNGAN DB & SUNTIKAN MAYA)
    j_html_list = ""
    j_count = 1
    printed_j_generics = set()
    j_list = extract_jk_from_row(staf_row)
    
    if len(j_list) > 0:
        for item in j_list:
            kod_j = item.get('kod', 'J')
            perincian_j = item.get('perincian', '-')
            kod_clean = kod_j.split('|')[0].strip().upper()
            kod_generik = kod_clean.replace('JR', 'J').replace('JM', 'J')
            printed_j_generics.add(kod_generik)
            
            name_only = MYSG_JAWATANKUASA_J.get(kod_generik, ("", 0))[0]
            label_j = f"{kod_clean} | {name_only}" if name_only else kod_j
            dtl_str = f": {perincian_j}" if perincian_j and str(perincian_j).lower() not in ["nan", "none", "-", "", name_only.lower(), label_j.lower()] else ""
            diserap_label = " <span style='color: #c0392b; font-style: italic; font-size: 9.5pt;'>(Diserap dalam tugas utama)</span>" if kod_generik in absorbed_j_codes else ""
            
            j_html_list += f"<div style='margin-bottom: 2px; padding-left: 20px;'>2.3.{j_count}. {label_j}{dtl_str}{diserap_label}</div>"
            j_count += 1
            
    # SUNTIKAN MAYA
    for j_clean in absorbed_j_codes:
        if j_clean not in printed_j_generics:
            printed_j_generics.add(j_clean)
            name_only = MYSG_JAWATANKUASA_J.get(j_clean, ("", 0))[0]
            kod_display = j_clean.replace('J', prefix_j)
            label_j = f"{kod_display} | {name_only}"
            diserap_label = " <span style='color: #c0392b; font-style: italic; font-size: 9.5pt;'>(Diserap dalam tugas utama)</span>"
            j_html_list += f"<div style='margin-bottom: 2px; padding-left: 20px;'>2.3.{j_count}. {label_j}{diserap_label}</div>"
            j_count += 1

    if j_count == 1:
        j_html_list += f"<div style='margin-bottom: 2px; padding-left: 20px;'>2.3.1. Tiada Jawatankuasa Ditetapkan</div>"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="ms">
    <head>
        <meta charset="UTF-8">
        <title>Surat Lantikan - {nama}</title>
        <style>
            {css_theme}
            @page {{ size: A4 portrait; margin: 1.8cm 2.2cm 1.8cm 2.2cm; }}
            html, body {{ font-family: Arial, Helvetica, sans-serif; font-size: 10.5pt; color: #000000; line-height: 1.35; margin: 0; padding: 0; }}
            .ref-block-table {{ width: 100%; margin-bottom: 11pt; font-size: 10.5pt; border-collapse: collapse; }}
            .ref-block-table td {{ padding: 1px 0; vertical-align: top; }}
            .title-box {{ font-weight: bold; font-size: 10.5pt; text-transform: uppercase; margin-top: 11pt; margin-bottom: 11pt; line-height: 1.35; }}
            .content-p {{ text-align: justify; margin-bottom: 11pt; line-height: 1.35; font-size: 10.5pt; }}
            .section-group {{ margin-bottom: 11pt; page-break-inside: avoid; }}
            .section-sub-title {{ font-weight: bold; margin-top: 2px; margin-bottom: 2px; text-transform: uppercase; }}
        </style>
    </head>
    <body>
        <div>
            {header_html}
            <table class="ref-block-table">
                <tr>
                    <td style="width: 45%;"></td>
                    <td style="width: 55%;">
                        <table style="width: 100%; border-collapse: collapse; font-size: 10.5pt; text-align: left;">
                            <tr><td style="width: 28%; white-space: nowrap; text-align: left;">Ruj. Kami</td><td style="width: 4%; text-align: center;">:</td><td style="width: 68%; text-align: left; font-weight: normal; white-space: nowrap;">{ruj_kami_formatted}</td></tr>
                            <tr><td style="text-align: left; white-space: nowrap;">Tarikh</td><td style="text-align: center;">:</td><td style="text-align: left; font-weight: normal; white-space: nowrap;">{tarikh_rasmi}</td></tr>
                        </table>
                    </td>
                </tr>
            </table>

            <div style="font-weight: bold; font-size: 10.5pt; line-height: 1.25; margin-bottom: 11pt;">
                {nama}<br><span style="font-weight: normal;">No. KP: {ic_no}</span>
            </div>
            <div style="font-size: 10.5pt; margin-bottom: 11pt;">Tuan/Puan,</div>
            <div class="title-box">SURAT LANTIKAN DAN AGIHAN TUGAS BAGI SESI PERSEKOLAHAN TAHUN {tahun_sesi}</div>

            <div class="content-p">Dengan segala hormatnya perkara di atas adalah dirujuk bersama perkara-perkara berkaitan di bawah Akta Pendidikan 1996, Surat-surat Pekeliling Ikhtisas (SPI), serta arahan dan garis panduan MySG KPM yang berkuat kuasa.</div>
            <div class="content-p">2. Sukacita dimaklumkan bahawa pihak sekolah melantik tuan/puan untuk memegang jawatan dan melaksanakan amanah seperti berikut berkuat kuasa mulai tarikh surat ini dikeluarkan:</div>

            <div class="section-group" style="margin-left: 10px;">
                <div class="section-sub-title">2.1. JAWATAN BERPORTFOLIO: {jawatan_hakiki}</div>
                {pdp_html_list}
            </div>
            <div class="section-group" style="margin-left: 10px;">
                <div class="section-sub-title">2.2. PORTFOLIO TANPA JAWATAN:</div>
                {p_html_list}
            </div>
            <div class="section-group" style="margin-left: 10px;">
                <div class="section-sub-title">2.3. JAWATANKUASA:</div>
                {j_html_list}
            </div>

            <div class="content-p">3. Sehubungan dengan itu, tuan/puan dinasihatkan untuk merujuk dan memahami tugas serta tanggungjawab yang ditetapkan selaras dengan Garis Panduan Tadbir Urus Sekolah (MySG KPM).</div>
            <div class="content-p">4. Semoga tuan/puan dapat menjalankan tugas yang diamanahkan dengan komitmen dan akauntabiliti yang tinggi.</div>
            <div class="content-p">Sekian, terima kasih.</div>

            <div style="font-weight: bold; text-transform: uppercase; font-size: 10.5pt; margin-bottom: 11pt;">"MALAYSIA MADANI"<br><br>"BERKHIDMAT UNTUK NEGARA"</div>
            <div style="font-size: 10.5pt; margin-bottom: 11pt;">Saya yang menjalankan amanah,</div>
            <div style="margin-top: 33pt; font-weight: bold; text-transform: uppercase; font-size: 10.5pt; margin-bottom: 15pt;">
                ({nama_gb})<br><span style="font-weight: normal; text-transform: none;">{jawatan_gb}<br>{nama_sekolah}</span>
            </div>
            
            <!-- NOTA KAKI PENJELASAN (DIPINDAHKAN KE BAWAH TANDATANGAN) -->
            <div style="font-size: 8.5pt; margin-bottom: 5pt; line-height: 1.35; text-align: justify; color: #222;">
                <b>Nota Penyelarasan Tugas:</b> Jawatankuasa yang bertanda <span style="color: #c0392b; font-style: italic;">(Diserap dalam tugas utama)</span> bermaksud tuan/puan turut dilantik secara rasmi sebagai Ahli Jawatankuasa (AJK) bagi jawatankuasa tersebut. Walau bagaimanapun, peruntukan jam beban tugas bagi jawatankuasa ini telah dirangkumkan di dalam portfolio utama tuan/puan bagi mengelakkan pengiraan beban tugas berganda.
            </div>
            
            {footer_garis_html}
        </div>
        <script>window.onload = function() {{ window.print(); }};</script>
    </body>
    </html>
    """
    return html_content

def generate_individual_detailed_report_html(staf_row, school_info=None, df_all_staff=None, *args, **kwargs):
    if not isinstance(school_info, dict):
        school_info = {}

    header_html = get_official_letterhead(school_info)
    css_theme = get_a4_print_css(orientation='portrait')
    jenis_sek = school_info.get('jenis_sekolah', 'Sekolah Rendah')
    prefix_j = "JM" if "Menengah" in str(jenis_sek) else "JR"

    nama = str(staf_row.get('Nama', '-')).upper()
    gred = str(staf_row.get('Gred', '-')).replace('(nan)', '').replace('nan', '').strip()
    gred_show = gred if gred else '-'

    kod_h = str(staf_row.get('Kod_H_1', '')).split('|')[0].strip().upper()
    detail_h = str(staf_row.get('Detail_H_1', '')).upper()
    jawatan_hakiki = f"{kod_h} | {detail_h}" if kod_h else str(staf_row.get('Jawatan', 'HR12 | Guru Akademik KSSR'))
    
    ic_no = str(staf_row.get('No_KP', '-')).replace('nan', '-').replace('None', '-')
    if not ic_no or ic_no == 'nan':
        ic_no = '-'
        
    kump_staf = str(staf_row.get('Kumpulan', 'Guru')).strip()
    tahun_sesi = str(school_info.get('tahun_sesi', '2027'))
    kod_sekolah = str(school_info.get('kod_sekolah', 'XBA2004')).upper()
    tarikh_hari = datetime.now().strftime("%d/%m/%Y %I:%M %p")

    try: total_jam = float(staf_row.get('JUMLAH_BEBAN_KESELURAHAN', 0.0) or 0.0)
    except: total_jam = 0.0
    total_jam = round(total_jam, 1)

    jam_tapak_asas = force_get_h_base_hours(staf_row, jenis_sek)

    purata_kumpulan = 38.0
    if isinstance(df_all_staff, pd.DataFrame) and not df_all_staff.empty and 'JUMLAH_BEBAN_KESELURAHAN' in df_all_staff.columns:
        df_safe = df_all_staff.copy()
        df_safe['JUMLAH_BEBAN_KESELURAHAN'] = pd.to_numeric(df_safe['JUMLAH_BEBAN_KESELURAHAN'], errors='coerce')
        sub_kump = df_safe[df_safe['Kumpulan'] == kump_staf] if 'Kumpulan' in df_safe.columns else df_safe
        if not sub_kump.empty:
            mean_val = sub_kump['JUMLAH_BEBAN_KESELURAHAN'].mean(skipna=True)
            if pd.notna(mean_val): purata_kumpulan = round(float(mean_val), 1)

    diff_jam = round(total_jam - purata_kumpulan, 1)
    diff_text = f"+{diff_jam} jam dari purata" if diff_jam >= 0 else f"{diff_jam} jam dari purata"
    color_diff = "#d9534f" if diff_jam > 0 else "#2e7d32"

    if float(total_jam) > 45.0:
        badge_status = '<span style="background-color: #fde8e8; color: #9b1c1c; padding: 2px 6px; border-radius: 10px; font-weight: bold; font-size: 7.5pt;">🔴 TINGGI</span>'
    elif float(total_jam) >= 37.0:
        badge_status = '<span style="background-color: #def7ec; color: #03543f; padding: 2px 6px; border-radius: 10px; font-weight: bold; font-size: 7.5pt;">🟢 SEIMBANG (IDEAL)</span>'
    else:
        badge_status = '<span style="background-color: #e1effe; color: #1e429f; padding: 2px 6px; border-radius: 10px; font-weight: bold; font-size: 7.5pt;">🔵 RINGAN</span>'

    rows_h_html = f"""<tr style="background-color: #fafafa;"><td style="padding-left: 12px;">• &nbsp; <b>{jawatan_hakiki}</b> <span style="color: #666; font-size: 7.5pt;">(Masa Pengurusan Hakiki / Persediaan)</span></td><td style="text-align: right; font-weight: bold; width: 20%; color: #0f4c81;">{jam_tapak_asas:.1f} jam</td></tr>"""
    
    pdp_list = extract_pdp_from_row(staf_row)
    kadar_pdp_jam = 40.0 / 60.0 if "Menengah" in jenis_sek else 30.0 / 60.0
    if len(pdp_list) > 0:
        for idx_p, item in enumerate(pdp_list):
            waktu_str = item.get('waktu', '2')
            try: jam_val = round(float(waktu_str) * kadar_pdp_jam, 1)
            except: jam_val = 0.0
            bg_color = "#ffffff" if idx_p % 2 == 0 else "#fbfcfd"
            rows_h_html += f"""<tr style="background-color: {bg_color};"><td style="padding-left: 12px;">• &nbsp; {item.get('subjek', '-')} ({item.get('kelas', '-')}) • <i style="color: #555;">{int(float(waktu_str)) if float(waktu_str).is_integer() else waktu_str} Waktu</i></td><td style="text-align: right; font-weight: bold; color: #2b579a;">{jam_val:.1f} jam</td></tr>"""
    else:
        rows_h_html += """<tr style="background-color: #ffffff;"><td style="padding-left: 12px; color: #888;">• &nbsp; <i>Tiada Rekod Pengajaran (PdP) Ditetapkan</i></td><td style="text-align: right; font-weight: bold; color: #888;">0.0 jam</td></tr>"""

    absorbed_j_codes = []
    rows_p_html = ""
    p_list = extract_portfolio_from_row(staf_row)
    if len(p_list) > 0:
        for idx_p, item in enumerate(p_list):
            kod_p = item.get('kod', 'P')
            clean_p = kod_p.split('|')[0].strip().replace('PR', 'P').replace('PM', 'P')
            if clean_p in MYSG_P_TO_J_AUTO_MAP:
                absorbed_j_codes.extend(MYSG_P_TO_J_AUTO_MAP[clean_p])
                
            jam_val = round(float(item.get('jam', 1.5)), 1)
            bg_color = "#ffffff" if idx_p % 2 == 0 else "#fbfcfd"
            label_p = f"{kod_p} | {MYSG_PORTFOLIO_P.get(clean_p, (kod_p, 0))[0]}" if '|' not in kod_p else kod_p
            dtl_str = f": {item.get('perincian', '-')}" if item.get('perincian', '-') and item.get('perincian', '-') != label_p and item.get('perincian', '-') not in label_p else ""
            rows_p_html += f"""<tr style="background-color: {bg_color};"><td style="padding-left: 12px;">• &nbsp; <b>{label_p}</b>{dtl_str}</td><td style="text-align: right; font-weight: bold; color: #2b579a;">{jam_val:.1f} jam</td></tr>"""
    else:
        rows_p_html += """<tr style="background-color: #ffffff;"><td style="padding-left: 12px; color: #888;">• &nbsp; <i>Tiada Portfolio (P) Ditetapkan</i></td><td style="text-align: right; font-weight: bold; color: #888;">0.0 jam</td></tr>"""

    rows_j_html = ""
    printed_j_generics = set()
    idx_j = 0
    j_list = extract_jk_from_row(staf_row)
    
    if len(j_list) > 0:
        for item in j_list:
            kod_j = item.get('kod', 'J')
            kod_clean = kod_j.split('|')[0].strip().upper()
            kod_generik = kod_clean.replace('JR', 'J').replace('JM', 'J')
            printed_j_generics.add(kod_generik)
            
            name_only = MYSG_JAWATANKUASA_J.get(kod_generik, ("", 1.0))[0]
            label_j = f"{kod_clean} | {name_only}" if name_only else kod_j
            dtl_str = f": {item.get('perincian', '-')}" if item.get('perincian', '-') and str(item.get('perincian', '-')).lower() not in ["nan", "none", "-", "", name_only.lower(), label_j.lower()] else ""
            
            nilai_asal = float(MYSG_JAWATANKUASA_J.get(kod_generik, ("", 1.0))[1])
            if kod_generik in absorbed_j_codes:
                paparan_jam_html = f"<span style='text-decoration: line-through; color: #888;'>{nilai_asal:.1f} jam</span><br><span style='color: #c0392b; font-weight: bold; font-size: 7.5pt;'>0.0 jam (Diserap)</span>"
            else:
                jam_val = round(float(item.get('jam', 1.0)), 1)
                paparan_jam_html = f"<span style='color: #2b579a; font-weight: bold;'>{jam_val:.1f} jam</span>"
                
            bg_color = "#ffffff" if idx_j % 2 == 0 else "#fbfcfd"
            rows_j_html += f"""<tr style="background-color: {bg_color}; border-bottom: 1px solid #f0f0f0;"><td style="padding: 4px 4px 4px 12px;">• &nbsp; <b>{label_j}</b>{dtl_str}</td><td style="text-align: right; padding: 4px 4px; width: 20%; line-height: 1.25;">{paparan_jam_html}</td></tr>"""
            idx_j += 1

    # SUNTIKAN MAYA 
    for j_clean in absorbed_j_codes:
        if j_clean not in printed_j_generics:
            printed_j_generics.add(j_clean)
            name_only = MYSG_JAWATANKUASA_J.get(j_clean, ("", 1.0))[0]
            kod_display = j_clean.replace('J', prefix_j)
            label_j = f"{kod_display} | {name_only}"
            nilai_asal = float(MYSG_JAWATANKUASA_J.get(j_clean, ("", 1.0))[1])
            
            paparan_jam_html = f"<span style='text-decoration: line-through; color: #888;'>{nilai_asal:.1f} jam</span><br><span style='color: #c0392b; font-weight: bold; font-size: 7.5pt;'>0.0 jam (Diserap)</span>"
            bg_color = "#ffffff" if idx_j % 2 == 0 else "#fbfcfd"
            rows_j_html += f"""<tr style="background-color: {bg_color}; border-bottom: 1px solid #f0f0f0;"><td style="padding: 4px 4px 4px 12px;">• &nbsp; <b>{label_j}</b></td><td style="text-align: right; padding: 4px 4px; width: 20%; line-height: 1.25;">{paparan_jam_html}</td></tr>"""
            idx_j += 1

    if idx_j == 0:
        rows_j_html += """<tr style="background-color: #ffffff;"><td style="padding-left: 12px; color: #888;">• &nbsp; <i>Tiada Jawatankuasa (J) Ditetapkan</i></td><td style="text-align: right; font-weight: bold; color: #888;">0.0 jam</td></tr>"""

    html_content = f"""
    <!DOCTYPE html>
    <html lang="ms">
    <head>
        <meta charset="UTF-8">
        <title>Laporan Perincian Beban Tugas Individu - {nama}</title>
        <style>
            {css_theme}
            @page {{ size: A4 portrait; margin: 0.5cm 1.0cm 0.5cm 1.0cm; }}
            html, body {{ height: 100%; font-family: Arial, Helvetica, sans-serif; font-size: 8.5pt; color: #222; margin: 0; padding: 0; }}
            .page-container {{ display: flex; flex-direction: column; justify-content: space-between; min-height: 98vh; box-sizing: border-box; page-break-inside: avoid; }}
            .doc-title {{ border: 1.5px solid #0f4c81; border-radius: 4px; font-weight: bold; font-size: 10pt; text-align: center; text-transform: uppercase; padding: 4px; margin-bottom: 6px; background-color: #f0f4f8; color: #0f4c81; letter-spacing: 0.5px; }}
            .header-info-table {{ width: 100%; border-collapse: collapse; font-size: 8.5pt; margin-bottom: 6px; }}
            .header-info-table td {{ padding: 2px 4px; vertical-align: top; }}
            .metric-container {{ display: flex; border: 1px solid #d0e1fd; background-color: #f8fbff; border-radius: 4px; margin-bottom: 8px; padding: 4px 0; }}
            .metric-box {{ flex: 1; text-align: center; border-right: 1px solid #d0e1fd; }}
            .metric-box:last-child {{ border-right: none; }}
            .metric-label {{ font-size: 7.5pt; color: #555; font-weight: bold; margin-bottom: 1px; text-transform: uppercase; }}
            .metric-value {{ font-size: 11.5pt; font-weight: bold; color: #0f4c81; }}
            .section-bar {{ background-color: #e8f1f5; color: #0f4c81; font-weight: bold; font-size: 8pt; padding: 3px 8px; border-top: 1px solid #b8d4e3; border-bottom: 1px solid #b8d4e3; border-radius: 2px; text-transform: uppercase; display: flex; justify-content: space-between; margin-top: 2px; }}
            .detail-table {{ width: 100%; border-collapse: collapse; font-size: 8pt; margin-bottom: 4px; page-break-inside: avoid; }}
            .print-footer-container {{ margin-top: 12px; border-top: 1px solid #ccc; padding-top: 4px; font-size: 8pt; color: #555; display: flex; justify-content: space-between; font-family: Arial, sans-serif; }}
        </style>
    </head>
    <body>
        <div class="page-container">
            <div>
                {header_html}
                <div class="doc-title">LAPORAN PERINCIAN BEBAN TUGAS INDIVIDU</div>
                <table class="header-info-table">
                    <tr><td style="width: 58%; text-align: left;"><b>Nama Pegawai:</b> {nama}<br><b>No. KP:</b> {ic_no}<br><b>Jawatan Hakiki:</b> {jawatan_hakiki}<br><b>Gred Perkhidmatan:</b> {gred_show}</td>
                    <td style="width: 42%; text-align: left;"><b>Kumpulan:</b> {kump_staf}<br><b>Sesi Persekolahan:</b> {tahun_sesi}<br><b>Tarikh Cetakan:</b> {tarikh_hari}</td></tr>
                </table>
                <div class="metric-container">
                    <div class="metric-box"><div class="metric-label">Beban Kerja Pegawai</div><div class="metric-value">{total_jam:.1f} Jam</div><div style="margin-top: 1px;">{badge_status}</div></div>
                    <div class="metric-box"><div class="metric-label">Purata Kumpulan ({kump_staf})</div><div class="metric-value" style="color: #2b579a;">{purata_kumpulan:.1f} Jam</div><div style="font-size: 7pt; color: #777;">Penanda Aras Ideal MySG</div></div>
                    <div class="metric-box"><div class="metric-label">Kedudukan / Perbezaan</div><div class="metric-value" style="color: {color_diff};">{diff_text}</div><div style="font-size: 7pt; color: #777;">Variasi Agihan Tugas</div></div>
                </div>
                <div style="font-weight: bold; font-size: 8pt; margin-bottom: 2px; color: #0f4c81; text-transform: uppercase;">📋 SENARAI PERINCIAN AGIHAN TUGAS & PEMBERAT (JAM):</div>
                <div class="section-bar"><span>1. PORTFOLIO BERJAWATAN HAKIKI (KOD H) & PENGAJARAN DAN PEMBELAJARAN (PDP)</span><span>PEMBERAT JAM</span></div>
                <table class="detail-table"><tbody>{rows_h_html}</tbody></table>
                <div class="section-bar"><span>2. PORTFOLIO TANPA JAWATAN (KOD P)</span><span>PEMBERAT JAM</span></div>
                <table class="detail-table"><tbody>{rows_p_html}</tbody></table>
                <div class="section-bar"><span>3. JAWATANKUASA SEKOLAH (KOD J)</span><span>PEMBERAT JAM</span></div>
                <table class="detail-table"><tbody>{rows_j_html}</tbody></table>
                <table style="width: 100%; font-size: 8.5pt; font-weight: bold; margin-top: 3px; margin-bottom: 4px; border-top: 1.5px solid #0f4c81; padding-top: 2px;">
                    <tr><td style="text-align: right; padding-right: 15px; color: #0f4c81;">JUMLAH BEBAN KERJA KESELURUHAN:</td><td style="width: 22%; text-align: right; color: #0f4c81; font-size: 9.5pt;">{total_jam:.1f} JAM</td></tr>
                </table>
            </div>
            <div>
                <div style="border: 1px dashed #0f4c81; background-color: #fcfdfe; border-radius: 4px; padding: 6px 10px; font-size: 7.5pt; line-height: 1.35; margin-top: 8px; color: #222; page-break-inside: avoid;">
                    <div style="font-weight: bold; color: #c0392b; margin-bottom: 4px; text-transform: uppercase;">📌 KETETAPAN & GARIS PANDUAN PENGIRAAN BEBAN KERJA (MYSG KPM)</div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2px 15px; border-bottom: 1px solid #e0e0e0; padding-bottom: 4px; margin-bottom: 4px; font-weight: 500;">
                        <div>• <b>Masa Asas 45 Jam:</b> Ditetapkan JPA selaras dengan <i>International Labour Organization</i> (ILO).</div>
                        <div>• <b>Pelaksanaan Masa (PGB & AKP):</b> Berdasarkan waktu bekerja pejabat (38 jam 30 min bekerja + 6 jam 30 min rehat).</div>
                        <div>• <b>Pelaksanaan Masa (Guru):</b> Gabungan Waktu Persekolahan (PdP & Bukan) + Luar Waktu (Kokurikulum & Lain-lain).</div>
                        <div>• <b>Tugasan Cuti Sekolah:</b> PGB boleh mengarahkan guru bertugas cuti sekolah maks separuh dari cuti (Maks. 22 Hari/Tahun).</div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2px 15px;">
                        <div>• <b>1. Pentadbir:</b> PdP minimum (3.0–6.0 Jam/Minggu). Fokus Portfolio Hakiki (Kod H) & Kepimpinan JK (Kod J).</div>
                        <div>• <b>2. Guru Akademik:</b> Beban optimum (37.0 - 45.0 Jam/Minggu). Lebih 45 Jam dikira beban <b>TINGGI</b>.</div>
                        <div>• <b>3. Guru Khusus (GPM/Data):</b> Pengurangan PdP untuk menampung masa pengurusan hakiki.</div>
                        <div>• <b>4. AKP:</b> Masa kerja pejabat operasi (40.0 Jam/Minggu). Beban sampingan (Kod P/J) terhad.</div>
                    </div>
                    <div style="margin-top: 6px; padding-top: 4px; border-top: 1px dotted #ccc; font-style: italic; color: #c0392b;">
                        * <b>Penyelarasan Jam (Diserap):</b> Label <b>0.0 jam (Diserap)</b> bermaksud peruntukan masa bagi jawatankuasa tersebut telah pun dirangkumkan secara automatik di dalam pakej jam portfolio utama (seperti Guru Kelas / Ketua Panitia / Penyelaras) bagi mengelakkan pengiraan beban berganda (double-counting).
                    </div>
                </div>
                <div class="print-footer-container">
                    <div><i>Dokumen Rasmi Dijana Menerusi Sistem Pengurusan Beban Kerja MySG KPM ({kod_sekolah}) | Tarikh Cetakan: <b>{tarikh_hari}</b></i></div>
                    <div style="white-space: nowrap; font-weight: bold;">[ Halaman 1 daripada 1 ]</div>
                </div>
            </div>
        </div>
        <script>window.onload = function() {{ window.print(); }};</script>
    </body>
    </html>
    """
    return html_content
