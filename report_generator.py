"""
========================================================================
SISTEM PENGURUSAN & PENGIRAAN BEBAN KERJA KAKITANGAN SEKOLAH (MYSG KPM)
MYSG REPORT GENERATOR - MODUL PENJANAAN HTML PENYATA INDIVIDU
========================================================================
"""

import pandas as pd
from mysg_core import SYSTEM_VERSION, SYSTEM_NAME

def clean_str_val(val, default="-"):
    if pd.isna(val) or val is None:
        return default
    s_val = str(val).strip()
    if s_val.lower() in ['nan', 'none', '', 'null']:
        return default
    return s_val

def generate_individual_report_html(staf_row, info_sec, metrics=None):
    kat_staf = staf_row.get('Kategori_Staf', 'Guru')
    jenis_sekolah = info_sec.get('jenis_sekolah', 'Sekolah Rendah')
    is_sm = "Menengah" in str(jenis_sekolah)
    
    pdp_ind = float(staf_row.get('JUMLAH_JAM_PDP', 0))
    port_ind = float(staf_row.get('JUMLAH_JAM_PORTFOLIO', 0))
    jawat_ind = float(staf_row.get('JUMLAH_JAM_JAWATANKUASA', 0))
    beban_ind = float(staf_row.get('JUMLAH_BEBAN_KESELURAHAN', 0))

    if metrics:
        if kat_staf == 'Guru':
            pdp_avg = metrics.get('avg_pdp_guru', 0.0)
            port_avg = metrics.get('avg_port_guru', 0.0)
            beban_avg = metrics.get('avg_beban_guru', 0.0)
        else:
            pdp_avg = 0.0
            port_avg = metrics.get('avg_port_akp', 0.0)
            beban_avg = metrics.get('avg_beban_akp', 0.0)
    else:
        beban_avg = 0.0

    max_scale = max(beban_ind, beban_avg, 35.0)
    pct_ind = min((beban_ind / max_scale) * 100, 100)
    pct_avg = min((beban_avg / max_scale) * 100, 100)
    
    diff_beban = beban_ind - beban_avg
    if diff_beban > 0.5:
        status_text = f"<b>+{diff_beban:.1f} Jam</b> (Atas Purata Sekolah)"
        status_color = "#047857"
        bg_card = "#f0fdf4"
        border_card = "#a7f3d0"
    elif diff_beban < -0.5:
        status_text = f"<b>{diff_beban:.1f} Jam</b> (Bawah Purata Sekolah)"
        status_color = "#b45309"
        bg_card = "#fffbeb"
        border_card = "#fde68a"
    else:
        status_text = f"<b>Seimbang</b> (Mengikut Purata Sekolah)"
        status_color = "#1d4ed8"
        bg_card = "#eff6ff"
        border_card = "#bfdbfe"

    pdp_rows = []
    pdp_count = 0
    for i in range(1, 16):
        subj = clean_str_val(staf_row.get(f'Subjek_{i}'), default="")
        wkt = staf_row.get(f'Waktu_{i}')
        if subj != "" and pd.notna(wkt) and float(wkt) > 0:
            pdp_count += 1
            pdp_rows.append(
                f"<tr>"
                f"<td style='padding:6px; border:1px solid #cbd5e1;'>{pdp_count}</td>"
                f"<td style='padding:6px; border:1px solid #cbd5e1;'>{subj}</td>"
                f"<td style='padding:6px; border:1px solid #cbd5e1; text-align:center;'>{wkt} Waktu</td>"
                f"</tr>"
            )

    pdp_rows_html = "".join(pdp_rows) if pdp_rows else "<tr><td colspan='3' style='text-align:center; color:#888; padding:8px;'>Tiada Jadual Waktu PdP Didaftarkan</td></tr>"

    p_rows = []
    for i in range(1, 16):
        kod = clean_str_val(staf_row.get(f'Kod_P_{i}'), default="")
        detail = clean_str_val(staf_row.get(f'Detail_P_{i}'), default="-")
        if kod != "":
            p_rows.append(
                f"<tr>"
                f"<td style='padding:5px; border:1px solid #cbd5e1; font-weight:bold;'>{kod}</td>"
                f"<td style='padding:5px; border:1px solid #cbd5e1;'>{detail}</td>"
                f"</tr>"
            )

    p_rows_html = "".join(p_rows) if p_rows else "<tr><td colspan='2' style='text-align:center; color:#888; padding:8px;'>Tiada Portfolio Diberikan</td></tr>"

    j_rows = []
    for i in range(1, 16):
        kod = clean_str_val(staf_row.get(f'Kod_J_{i}'), default="")
        detail = clean_str_val(staf_row.get(f'Detail_J_{i}'), default="-")
        if kod != "":
            j_rows.append(
                f"<tr>"
                f"<td style='padding:5px; border:1px solid #cbd5e1; font-weight:bold;'>{kod}</td>"
                f"<td style='padding:5px; border:1px solid #cbd5e1;'>{detail}</td>"
                f"</tr>"
            )

    j_rows_html = "".join(j_rows) if j_rows else "<tr><td colspan='2' style='text-align:center; color:#888; padding:8px;'>Tiada Jawatankuasa Diberikan</td></tr>"

    nama_staf = clean_str_val(staf_row.get('Nama'))
    no_kp = clean_str_val(staf_row.get('No_KP'))
    gred_jawatan = clean_str_val(staf_row.get('Gred'))
    gelaran_jawatan = clean_str_val(staf_row.get('Jawatan'))
    tahun_sesi = clean_str_val(info_sec.get('tahun_sesi'), default='2026')
    nama_sekolah = clean_str_val(info_sec.get('nama_sekolah'), default='NAMA SEKOLAH')
    alamat_sekolah = clean_str_val(info_sec.get('alamat_sekolah'))
    no_tel = clean_str_val(info_sec.get('no_telefon'))
    nama_gb = clean_str_val(info_sec.get('nama_gb'), default='PENGETUA / GURU BESAR')
    tarikh_cetak = pd.Timestamp.now().strftime('%d %B %Y')
    
    logo_b64 = info_sec.get('logo_base64', '')
    pendarab_teks = "40 Minit / Waktu (0.6667 Jam)" if is_sm else "30 Minit / Waktu (0.5000 Jam)"

    if logo_b64:
        header_html = (
            f"<div style='display:flex; align-items:center; border-bottom:2px solid #0f172a; padding-bottom:12px; margin-bottom:18px;'>"
            f"<div style='flex:0 0 90px; text-align:center;'><img src='{logo_b64}' style='max-height:80px; max-width:80px;'></div>"
            f"<div style='flex:1; text-align:center; padding-right:90px;'>"
            f"<h3 style='margin:0; font-size:18px; text-transform:uppercase;'>{nama_sekolah}</h3>"
            f"<p style='margin:2px 0 0 0; font-size:12px;'>{alamat_sekolah} | Tel: {no_tel}</p>"
            f"<h4 style='margin:8px 0 0 0; font-size:14px; color:#1e3a8a; text-transform:uppercase;'>PENYATA AGIHAN BEBAN KERJA KAKITANGAN SEKOLAH (MYSG KPM)</h4>"
            f"</div>"
            f"</div>"
        )
    else:
        header_html = (
            f"<div style='text-align:center; border-bottom:2px solid #0f172a; padding-bottom:12px; margin-bottom:18px;'>"
            f"<h3 style='margin:0; font-size:18px; text-transform:uppercase;'>{nama_sekolah}</h3>"
            f"<p style='margin:2px 0 0 0; font-size:12px;'>{alamat_sekolah} | Tel: {no_tel}</p>"
            f"<h4 style='margin:10px 0 0 0; font-size:14px; color:#1e3a8a; text-transform:uppercase;'>PENYATA AGIHAN BEBAN KERJA KAKITANGAN SEKOLAH (MYSG KPM)</h4>"
            f"</div>"
        )

    html_content = (
        f"<div id='mysgReportContent' style='background-color:#ffffff; padding:25px; border:1px solid #cbd5e1; border-radius:8px; font-family:Arial, sans-serif; color:#0f172a; font-size:11pt;'>"
        f"{header_html}"
        f"<table style='width:100%; border-collapse:collapse; margin-bottom:15px; font-size:11pt;'>"
        f"<tr>"
        f"<td style='padding:4px; width:18%;'><b>Nama Staf</b></td>"
        f"<td style='padding:4px; width:32%;'>: <b>{nama_staf}</b></td>"
        f"<td style='padding:4px; width:20%;'><b>No. Kad Pengenalan</b></td>"
        f"<td style='padding:4px; width:30%;'>: {no_kp}</td>"
        f"</tr>"
        f"<tr>"
        f"<td style='padding:4px;'><b>Gred Jawatan</b></td>"
        f"<td style='padding:4px;'>: {gred_jawatan}</td>"
        f"<td style='padding:4px;'><b>Sesi Persekolahan</b></td>"
        f"<td style='padding:4px;'>: {tahun_sesi}</td>"
        f"</tr>"
        f"<tr>"
        f"<td style='padding:4px;'><b>Gelaran Jawatan</b></td>"
        f"<td style='padding:4px;' colspan='3'>: {gelaran_jawatan}</td>"
        f"</tr>"
        f"</table>"
        f"<div style='background-color:{bg_card}; border:1px solid {border_card}; border-radius:6px; padding:12px; margin-bottom:18px;'>"
        f"<div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; font-size:10pt;'>"
        f"<span style='font-weight:bold; color:#1e293b;'>📊 ANALISIS PERBANDINGAN BEBAN KERJA INDIVIDU VS PURATA {kat_staf.upper()}</span>"
        f"<span style='color:{status_color}; font-size:10pt;'>Status: {status_text}</span>"
        f"</div>"
        f"<table style='width:100%; border-collapse:collapse; font-size:10pt;'>"
        f"<tr>"
        f"<td style='width:28%; padding:3px 0;'><b>Beban Staf Ini:</b> {beban_ind:.1f} Jam</td>"
        f"<td style='width:72%;'>"
        f"<div style='background-color:#cbd5e1; border-radius:4px; height:12px; width:100%; overflow:hidden;'>"
        f"<div style='background-color:#2563eb; height:100%; width:{pct_ind:.1f}%;'></div>"
        f"</div>"
        f"</td>"
        f"</tr>"
        f"<tr>"
        f"<td style='padding:3px 0; color:#475569;'>Purata Sekolah ({kat_staf}): {beban_avg:.1f} Jam</td>"
        f"<td>"
        f"<div style='background-color:#cbd5e1; border-radius:4px; height:12px; width:100%; overflow:hidden;'>"
        f"<div style='background-color:#64748b; height:100%; width:{pct_avg:.1f}%;'></div>"
        f"</div>"
        f"</td>"
        f"</tr>"
        f"</table>"
        f"</div>"
        f"<table style='width:100%; border-collapse:collapse; margin-bottom:18px; font-size:11pt; text-align:center; background-color:#f8fafc; border:1px solid #cbd5e1;'>"
        f"<tr style='background-color:#e2e8f0; font-weight:bold;'>"
        f"<td style='padding:6px; border:1px solid #cbd5e1;'>Jam PdP (Waktu)</td>"
        f"<td style='padding:6px; border:1px solid #cbd5e1;'>Jam Portfolio (P)</td>"
        f"<td style='padding:6px; border:1px solid #cbd5e1;'>Jam Jawatankuasa (J)</td>"
        f"<td style='padding:6px; border:1px solid #cbd5e1;'>JUMLAH BEBAN KERJA MINGGUAN</td>"
        f"</tr>"
        f"<tr>"
        f"<td style='padding:8px; border:1px solid #cbd5e1; font-weight:bold;'>{pdp_ind:.1f} Jam</td>"
        f"<td style='padding:8px; border:1px solid #cbd5e1; font-weight:bold;'>{port_ind:.1f} Jam</td>"
        f"<td style='padding:8px; border:1px solid #cbd5e1; font-weight:bold;'>{jawat_ind:.1f} Jam</td>"
        f"<td style='padding:8px; border:1px solid #cbd5e1; font-weight:bold; color:#1e40af;'>{beban_ind:.1f} Jam</td>"
        f"</tr>"
        f"</table>"
        f"<h5 style='margin:10px 0 5px 0; font-size:11pt; color:#1e293b;'>1. Jadual Mengajar Subjek & Kelas (PdP)</h5>"
        f"<table style='width:100%; border-collapse:collapse; margin-bottom:15px; font-size:10pt; border:1px solid #cbd5e1;'>"
        f"<thead>"
        f"<tr style='background-color:#f1f5f9; text-align:left;'>"
        f"<th style='padding:6px; border:1px solid #cbd5e1; width:8%;'>No.</th>"
        f"<th style='padding:6px; border:1px solid #cbd5e1;'>Mata Pelajaran & Kelas Diajar</th>"
        f"<th style='padding:6px; border:1px solid #cbd5e1; text-align:center; width:20%;'>Peruntukan Waktu</th>"
        f"</tr>"
        f"</thead>"
        f"<tbody>{pdp_rows_html}</tbody>"
        f"</table>"
        f"<div style='display:flex; gap:15px;'>"
        f"<div style='flex:1;'>"
        f"<h5 style='margin:5px 0; font-size:11pt; color:#1e293b;'>2. Senarai Portfolio (P)</h5>"
        f"<table style='width:100%; border-collapse:collapse; font-size:10pt; border:1px solid #cbd5e1;'>"
        f"<thead><tr style='background-color:#f1f5f9;'><th style='padding:5px; border:1px solid #cbd5e1; width:25%;'>Kod P</th><th style='padding:5px; border:1px solid #cbd5e1;'>Perincian Tugas</th></tr></thead>"
        f"<tbody>{p_rows_html}</tbody>"
        f"</table>"
        f"</div>"
        f"<div style='flex:1;'>"
        f"<h5 style='margin:5px 0; font-size:11pt; color:#1e293b;'>3. Senarai Jawatankuasa (J)</h5>"
        f"<table style='width:100%; border-collapse:collapse; font-size:10pt; border:1px solid #cbd5e1;'>"
        f"<thead><tr style='background-color:#f1f5f9;'><th style='padding:5px; border:1px solid #cbd5e1; width:25%;'>Kod J</th><th style='padding:5px; border:1px solid #cbd5e1;'>Perincian Tugas</th></tr></thead>"
        f"<tbody>{j_rows_html}</tbody>"
        f"</table>"
        f"</div>"
        f"</div>"
        f"<br>"
        f"<div style='background-color:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:10px; margin-top:15px; font-size:9pt; color:#475569;'>"
        f"<b>📌 Ketetapan & Rujukan Rasmi MySG KPM:</b><br>"
        f"1. <b>Kadar Masa PdP:</b> Ditetapkan berdasarkan institusi {jenis_sekolah} iaitu <b>{pendarab_teks}</b>.<br>"
        f"2. <b>Pemberatan Portfolio (P) & Jawatankuasa (J):</b> Dikira mengikut Kod Standard MySG KPM (P01–P15 dan J01–J15).<br>"
        f"3. Penyata ini dijana secara automatik oleh {SYSTEM_NAME} untuk kegunaan pengurusan, dialog prestasi, dan penilaian perkhidmatan."
        f"</div>"
        f"<br><br>"
        f"<table style='width:100%; border-collapse:collapse; font-size:11pt; margin-top:10px;'>"
        f"<tr>"
        f"<td style='width:60%;'>"
        f"<p style='margin:0;'>Disahkan Oleh:</p>"
        f"<br><br><br>"
        f"<p style='margin:0;'><b>({nama_gb})</b></p>"
        f"<p style='margin:0; color:#475569;'>Pengetua / Guru Besar</p>"
        f"<p style='margin:0; color:#475569;'>{nama_sekolah}</p>"
        f"</td>"
        f"<td style='width:40%; text-align:right; vertical-align:bottom;'>"
        f"<p style='margin:0; color:#64748b;'>Tarikh Cetakan: <b>{tarikh_cetak}</b></p>"
        f"<p style='margin:2px 0 0 0; color:#94a3b8; font-size:9pt;'>Versi Sistem: <b>{SYSTEM_VERSION}</b></p>"
        f"</td>"
        f"</tr>"
        f"</table>"
        f"</div>"
    )
    return html_content