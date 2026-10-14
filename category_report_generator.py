"""
========================================================================
SISTEM PENGURUSAN & PENGIRAAN BEBAN KERJA KAKITANGAN SEKOLAH (MYSG KPM)
CATEGORY REPORT GENERATOR - MODUL PENJANAAN LAPORAN RINGKASAN BERKATEGORI
========================================================================
Modul khas menjana Laporan Ringkasan Cetakan bagi Kategori Sekolah, Guru & AKP
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

def generate_category_report_html(df_category, category_name, info_sec, metrics=None):
    nama_sekolah = clean_str_val(info_sec.get('nama_sekolah'), default='NAMA SEKOLAH')
    alamat_sekolah = clean_str_val(info_sec.get('alamat_sekolah'))
    no_tel = clean_str_val(info_sec.get('no_telefon'))
    tahun_sesi = clean_str_val(info_sec.get('tahun_sesi'), default='2026')
    nama_gb = clean_str_val(info_sec.get('nama_gb'), default='PENGETUA / GURU BESAR')
    logo_b64 = info_sec.get('logo_base64', '')
    tarikh_cetak = pd.Timestamp.now().strftime('%d %B %Y')

    if logo_b64:
        header_html = (
            f"<div style='display:flex; align-items:center; border-bottom:2px solid #0f172a; padding-bottom:12px; margin-bottom:15px;'>"
            f"<div style='flex:0 0 80px; text-align:center;'><img src='{logo_b64}' style='max-height:70px; max-width:70px;'></div>"
            f"<div style='flex:1; text-align:center; padding-right:80px;'>"
            f"<h3 style='margin:0; font-size:16px; text-transform:uppercase;'>{nama_sekolah}</h3>"
            f"<p style='margin:2px 0 0 0; font-size:11px;'>{alamat_sekolah} | Tel: {no_tel}</p>"
            f"<h4 style='margin:6px 0 0 0; font-size:13px; color:#1e3a8a; text-transform:uppercase;'>LAPORAN RINGKASAN AGIHAN BEBAN KERJA — {category_name.upper()} ({tahun_sesi})</h4>"
            f"</div>"
            f"</div>"
        )
    else:
        header_html = (
            f"<div style='text-align:center; border-bottom:2px solid #0f172a; padding-bottom:12px; margin-bottom:15px;'>"
            f"<h3 style='margin:0; font-size:16px; text-transform:uppercase;'>{nama_sekolah}</h3>"
            f"<p style='margin:2px 0 0 0; font-size:11px;'>{alamat_sekolah} | Tel: {no_tel}</p>"
            f"<h4 style='margin:8px 0 0 0; font-size:13px; color:#1e3a8a; text-transform:uppercase;'>LAPORAN RINGKASAN AGIHAN BEBAN KERJA — {category_name.upper()} ({tahun_sesi})</h4>"
            f"</div>"
        )

    table_rows = []
    for idx, (_, row) in enumerate(df_category.iterrows(), 1):
        nama = clean_str_val(row.get('Nama'))
        gred = clean_str_val(row.get('Gred'))
        jawatan = clean_str_val(row.get('Jawatan'))
        pdp = float(row.get('JUMLAH_JAM_PDP', 0))
        port = float(row.get('JUMLAH_JAM_PORTFOLIO', 0))
        jawat = float(row.get('JUMLAH_JAM_JAWATANKUASA', 0))
        total = float(row.get('JUMLAH_BEBAN_KESELURAHAN', 0))

        table_rows.append(
            f"<tr>"
            f"<td style='padding:5px; border:1px solid #cbd5e1; text-align:center;'>{idx}</td>"
            f"<td style='padding:5px; border:1px solid #cbd5e1; font-weight:bold;'>{nama}</td>"
            f"<td style='padding:5px; border:1px solid #cbd5e1; text-align:center;'>{gred}</td>"
            f"<td style='padding:5px; border:1px solid #cbd5e1;'>{jawatan}</td>"
            f"<td style='padding:5px; border:1px solid #cbd5e1; text-align:center;'>{pdp:.1f}</td>"
            f"<td style='padding:5px; border:1px solid #cbd5e1; text-align:center;'>{port:.1f}</td>"
            f"<td style='padding:5px; border:1px solid #cbd5e1; text-align:center;'>{jawat:.1f}</td>"
            f"<td style='padding:5px; border:1px solid #cbd5e1; text-align:center; font-weight:bold; color:#1e40af;'>{total:.1f}</td>"
            f"</tr>"
        )

    rows_html = "".join(table_rows) if table_rows else "<tr><td colspan='8' style='text-align:center; padding:10px;'>Tiada rekod data.</td></tr>"

    html_content = (
        f"<div id='mysgCategoryReportContent' style='background-color:#ffffff; padding:20px; border:1px solid #cbd5e1; border-radius:8px; font-family:Arial, sans-serif; color:#0f172a; font-size:11pt;'>"
        f"{header_html}"
        f"<table style='width:100%; border-collapse:collapse; font-size:10pt; margin-bottom:15px; border:1px solid #cbd5e1;'>"
        f"<thead>"
        f"<tr style='background-color:#f1f5f9; text-align:center; font-weight:bold;'>"
        f"<th style='padding:6px; border:1px solid #cbd5e1; width:4%;'>Bil</th>"
        f"<th style='padding:6px; border:1px solid #cbd5e1; text-align:left;'>Nama Staf</th>"
        f"<th style='padding:6px; border:1px solid #cbd5e1; width:8%;'>Gred</th>"
        f"<th style='padding:6px; border:1px solid #cbd5e1; text-align:left;'>Gelaran Jawatan</th>"
        f"<th style='padding:6px; border:1px solid #cbd5e1; width:10%;'>Jam PdP</th>"
        f"<th style='padding:6px; border:1px solid #cbd5e1; width:10%;'>Jam Portfolio</th>"
        f"<th style='padding:6px; border:1px solid #cbd5e1; width:10%;'>Jam J'kuasa</th>"
        f"<th style='padding:6px; border:1px solid #cbd5e1; width:12%;'>Jumlah Jam</th>"
        f"</tr>"
        f"</thead>"
        f"<tbody>{rows_html}</tbody>"
        f"</table>"
        f"<br>"
        f"<table style='width:100%; border-collapse:collapse; font-size:11pt;'>"
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