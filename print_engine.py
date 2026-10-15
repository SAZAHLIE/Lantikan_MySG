"""
========================================================================
MYSG KPM: SISTEM PENGURUSAN & ANALISIS BEBAN KERJA
MODULE: PRINT ENGINE (ENJIN CETAKAN BERPUSAT A4, JATA NEGARA & LENCANA SEKOLAH)
========================================================================
"""

import os
import json
import glob
import base64
import time
import pandas as pd
from mysg_core import MYSG_PORTFOLIO_H_SR, MYSG_PORTFOLIO_H_SM, MYSG_PORTFOLIO_P, MYSG_JAWATANKUASA_J

# JATA NEGARA STANDARD BASE64 (SVG EMBEDDED UNTUK CETAKAN RASMI KPM)
JATA_NEGARA_BASE64 = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA1MDAgNTAwIj48Y2lyY2xlIGN4PSIyNTAiIGN5PSIyNTAiIHI9IjI0MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjMDAwIiBzdHJva2Utd2lkdGg9IjIiLz48dGV4dCB4PSIyNTAiIHk9IjI2MCIgZm9udC1zaXplPSI0MCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC13ZWlnaHQ9ImJvbGQiIGZvbnQtZmFtaWx5PSJTZXJpZiI+SkFUQSBORUdBUkE8L3RleHQ+PC9zdmc+"

def is_empty_val(val):
    """Fungsi semakan ketat untuk mengesahkan entri kosong / tiada nilai."""
    if val is None or pd.isna(val):
        return True
    s = str(val).strip().lower()
    return s in ["", "none", "nan", "null", "none | none", "none|none", "-", "select option", "choose option"]

def extract_school_details(school_info, session_state_ref=None):
    """Mengekstrak maklumat sekolah secara dinamik daripada dictionary, session state & fail json tempatan."""
    merged = {}
    
    # 1. Semak fail json jika wujud
    for json_file in glob.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as jf:
                data = json.load(jf)
                target = data.get('school_info', data)
                if isinstance(target, dict):
                    merged.update(target)
        except Exception:
            pass

    # 2. Semak Session State
    if session_state_ref:
        if isinstance(session_state_ref, dict):
            merged.update(session_state_ref)
        ss_info = getattr(session_state_ref, 'get', lambda k, d=None: None)('school_info', {})
        if isinstance(ss_info, dict):
            merged.update(ss_info)

    # 3. Semak parameter school_info
    if isinstance(school_info, dict):
        merged.update(school_info)

    nama_sek = (
        merged.get('nama_sekolah') or 
        merged.get('nama_sek') or 
        merged.get('school_name') or 
        merged.get('Nama Sekolah') or 
        'SEKOLAH KEBANGSAAN BANDAR'
    )
    
    kod_sek = (
        merged.get('kod_sekolah') or 
        merged.get('kod_sek') or 
        merged.get('school_code') or 
        merged.get('Kod Sekolah') or 
        'XBA2004'
    )
    
    sesi = (
        merged.get('tahun_sesi') or 
        merged.get('sesi') or 
        merged.get('tahun') or 
        merged.get('Sesi') or 
        '2027'
    )
    
    alamat = (
        merged.get('alamat_sekolah') or 
        merged.get('alamat') or 
        merged.get('address') or 
        merged.get('Alamat Sekolah') or 
        'W.D.T. NO. 297, 90009 SANDAKAN, SABAH'
    )
    
    no_tel = (
        merged.get('no_tel') or 
        merged.get('no_telefon') or 
        merged.get('no_telefon_sekolah') or 
        merged.get('No. Telefon') or 
        merged.get('No Telefon') or 
        merged.get('telefon') or 
        merged.get('tel') or 
        merged.get('phone') or 
        ''
    )
    
    no_faks = (
        merged.get('no_faks') or 
        merged.get('faks') or 
        merged.get('No. Faks') or 
        merged.get('No Faks') or 
        ''
    )

    email_sek = (
        merged.get('email_sekolah') or 
        merged.get('email') or 
        merged.get('emel') or 
        merged.get('emel_sekolah') or 
        merged.get('Emel') or 
        'xba2004@moe.edu.my'
    )
    
    gb = (
        merged.get('nama_gb') or 
        merged.get('nama_pengetua') or 
        merged.get('pengetua_gb') or 
        merged.get('gb') or 
        merged.get('Nama Pengetua / GB') or 
        'SAZAHLIE BIN SAPAR'
    )

    return {
        'nama_sekolah': str(nama_sek).strip(),
        'kod_sekolah': str(kod_sek).strip(),
        'tahun_sesi': str(sesi).strip(),
        'alamat_sekolah': str(alamat).strip(),
        'no_tel': str(no_tel).strip(),
        'no_faks': str(no_faks).strip(),
        'email_sekolah': str(email_sek).strip(),
        'nama_gb': str(gb).strip()
    }

def parse_to_base64_uri(val):
    """Menukar data gambar ke Data URI standard."""
    if not val or pd.isna(val):
        return None

    if isinstance(val, str):
        val_str = val.strip()
        if val_str.startswith('data:image'):
            return val_str
        if len(val_str) > 100 and ('/' in val_str or '+' in val_str or val_str.endswith('=')):
            return f"data:image/png;base64,{val_str}"
        if os.path.exists(val_str) and not val_str.endswith("logo.png"):
            try:
                with open(val_str, 'rb') as f:
                    b64 = base64.b64encode(f.read()).decode('utf-8')
                    return f"data:image/png;base64,{b64}"
            except Exception:
                pass

    if isinstance(val, (bytes, bytearray)):
        try:
            b64 = base64.b64encode(val).decode('utf-8')
            return f"data:image/png;base64,{b64}"
        except Exception:
            pass

    return None

def get_school_badge_base64(school_info, session_state_ref=None):
    """Mengambil data Lencana Sekolah rasmi daripada data JSON / Session State."""
    badge_keys = [
        'logo_base64', 'lencana_base64', 'logo_b64', 'lencana_b64',
        'logo_sekolah', 'lencana_sekolah', 'lencana', 'logo',
        'logo_bytes', 'lencana_bytes', 'badge_base64', 'school_logo'
    ]

    if isinstance(school_info, dict):
        for key in badge_keys:
            if key in school_info and school_info[key]:
                uri = parse_to_base64_uri(school_info[key])
                if uri:
                    return uri

    if session_state_ref:
        for key in badge_keys:
            val = session_state_ref.get(key) if isinstance(session_state_ref, dict) else getattr(session_state_ref, 'get', lambda k, d=None: None)(key)
            if val:
                uri = parse_to_base64_uri(val)
                if uri:
                    return uri

    for json_file in glob.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as jf:
                data = json.load(jf)
                target_dict = data.get('school_info', data)
                if isinstance(target_dict, dict):
                    for key in badge_keys:
                        if key in target_dict and target_dict[key]:
                            uri = parse_to_base64_uri(target_dict[key])
                            if uri:
                                return uri
        except Exception:
            pass

    possible_badge_paths = [
        "lencana.png", "lencana_sekolah.png", "lencana.jpg", 
        "lencana_sekolah.jpg", "school_logo.png", "school_badge.png"
    ]
    for path in possible_badge_paths:
        if os.path.exists(path):
            try:
                with open(path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    return f"data:image/png;base64,{encoded_string}"
            except Exception:
                pass

    return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVOR5CYII="

def generate_printable_html(df, title, school_info, session_state_ref=None):
    """Menjana templat HTML Laporan Beban Kerja A4 Landscape."""
    s_det = extract_school_details(school_info, session_state_ref)
    nama_sek, kod_sek, sesi = s_det['nama_sekolah'], s_det['kod_sekolah'], s_det['tahun_sesi']
    alamat, no_tel, no_faks, email_sek, gb = s_det['alamat_sekolah'], s_det['no_tel'], s_det['no_faks'], s_det['email_sekolah'], s_det['nama_gb']

    logo_b64 = get_school_badge_base64(school_info, session_state_ref)
    
    contact_parts = []
    if no_tel:
        contact_parts.append(f"<b>Tel:</b> {no_tel}")
    if no_faks and no_faks.upper() != 'NIL':
        contact_parts.append(f"<b>Faks:</b> {no_faks}")
    if email_sek:
        contact_parts.append(f"<b>Emel:</b> {email_sek}")
    contact_str = " &bull; ".join(contact_parts)

    rows_html = ""
    for idx, row in enumerate(df.to_dict(orient='records'), 1):
        status_color = "#16a34a" if "SEIMBANG" in str(row.get('Status_Agihan', '')) else ("#dc2626" if "TINGGI" in str(row.get('Status_Agihan', '')) else "#ca8a04")
        rows_html += f"""
        <tr>
            <td style="text-align:center;">{idx}</td>
            <td><b>{row.get('Nama', '')}</b></td>
            <td>{row.get('Jawatan', '')}</td>
            <td style="text-align:center;">{row.get('Waktu_PdP', 0)}</td>
            <td style="text-align:center;">{row.get('Jam_PdP', 0.0)}</td>
            <td style="text-align:center;">{row.get('Jam_Portfolio', 0.0)}</td>
            <td style="text-align:center;">{row.get('Jam_Jawatankuasa', 0.0)}</td>
            <td style="text-align:center; font-weight:bold;">{row.get('Jumlah_Jam_Beban', 0.0)}</td>
            <td style="text-align:center; color:{status_color}; font-weight:bold;">{row.get('Status_Agihan', '')}</td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{title} - {nama_sek}</title>
    <style>
        @page {{ size: A4 landscape; margin: 10mm; }}
        body {{ font-family: Arial, sans-serif; color: #0f172a; margin: 0; padding: 5px; font-size: 11px; }}
        .header-container {{ display: flex; align-items: center; justify-content: space-between; border-bottom: 3px double #1e3a8a; padding-bottom: 8px; margin-bottom: 12px; }}
        .header-logo {{ flex: 0 0 75px; text-align: center; }}
        .header-logo img {{ max-height: 65px; width: auto; object-fit: contain; }}
        .header-details {{ flex: 1; text-align: center; padding: 0 10px; }}
        .header-details h2 {{ margin: 0 0 3px 0; font-size: 16px; color: #1e3a8a; text-transform: uppercase; font-weight: 800; letter-spacing: 0.5px; }}
        .header-details p {{ margin: 2px 0; font-size: 10px; color: #334155; line-height: 1.3; }}
        .report-title {{ text-align: center; font-size: 12.5px; font-weight: bold; margin: 10px 0 12px 0; text-transform: uppercase; letter-spacing: 0.5px; background-color: #f8fafc; padding: 6px; border: 1px solid #e2e8f0; border-radius: 4px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 5px; }}
        th, td {{ border: 1px solid #cbd5e1; padding: 5px 6px; }}
        th {{ background-color: #f1f5f9; font-weight: bold; text-align: center; color: #1e293b; font-size: 10.5px; }}
        tr:nth-child(even) {{ background-color: #f8fafc; }}
        .footer {{ margin-top: 20px; display: flex; justify-content: space-between; font-size: 9.5px; color: #64748b; border-top: 1px solid #e2e8f0; padding-top: 6px; }}
        @media print {{ .no-print {{ display: none; }} }}
    </style>
</head>
<body onload="window.print()">
    <div class="header-container">
        <div class="header-logo"><img src="{logo_b64}" alt="Lencana Sekolah"></div>
        <div class="header-details">
            <h2>{nama_sek} ({kod_sek})</h2>
            <p>{alamat}</p>
            <p>{contact_str}</p>
            <p><b>Sesi Persekolahan:</b> {sesi} | <b>Pengetua / Guru Besar:</b> {gb}</p>
        </div>
        <div class="header-logo" style="visibility: hidden;"><img src="{logo_b64}" alt="Spacer"></div>
    </div>
    <div class="report-title">{title} (JUMLAH REKOD: {len(df)})</div>
    <table>
        <thead>
            <tr>
                <th style="width: 30px;">Bil</th>
                <th>Nama Pegawai / Kakitangan</th>
                <th>Jawatan Hakiki</th>
                <th style="width: 65px;">Waktu PdP</th>
                <th style="width: 65px;">Jam PdP</th>
                <th style="width: 75px;">Jam Portfolio</th>
                <th style="width: 75px;">Jam Jawatankuasa</th>
                <th style="width: 75px;">Jumlah Beban (Jam)</th>
                <th style="width: 90px;">Status Agihan</th>
            </tr>
        </thead>
        <tbody>{rows_html}</tbody>
    </table>
    <div class="footer">
        <div>MySG KPM: Sistem Pengurusan & Analisis Beban Kerja &bull; Dicetak pada: {time.strftime('%d/%m/%Y %H:%M')}</div>
        <div>Muka Surat 1 daripada 1</div>
    </div>
</body>
</html>"""

def generate_detailed_comparison_html(df, school_info, df_summary_comp, session_state_ref=None):
    """Menjana templat HTML Laporan Perincian & Bandingan Kumpulan Kakitangan (A4 Landscape)."""
    s_det = extract_school_details(school_info, session_state_ref)
    nama_sek, kod_sek, sesi = s_det['nama_sekolah'], s_det['kod_sekolah'], s_det['tahun_sesi']
    alamat, no_tel, no_faks, email_sek, gb = s_det['alamat_sekolah'], s_det['no_tel'], s_det['no_faks'], s_det['email_sekolah'], s_det['nama_gb']

    logo_b64 = get_school_badge_base64(school_info, session_state_ref)

    contact_parts = []
    if no_tel:
        contact_parts.append(f"<b>Tel:</b> {no_tel}")
    if no_faks and no_faks.upper() != 'NIL':
        contact_parts.append(f"<b>Faks:</b> {no_faks}")
    if email_sek:
        contact_parts.append(f"<b>Emel:</b> {email_sek}")
    contact_str = " &bull; ".join(contact_parts)

    summary_rows_html = ""
    for row in df_summary_comp.to_dict(orient='records'):
        summary_rows_html += f"""
        <tr>
            <td><b>{row.get('Kumpulan Kakitangan', '')}</b></td>
            <td style="text-align:center;">{row.get('Jumlah Anggota', 0)}</td>
            <td style="text-align:center;">{row.get('Purata Jam PdP', 0.0)}</td>
            <td style="text-align:center;">{row.get('Purata Jam Portfolio (H+P)', 0.0)}</td>
            <td style="text-align:center;">{row.get('Purata Jam Jawatankuasa (J)', 0.0)}</td>
            <td style="text-align:center; font-weight:bold; background-color:#f1f5f9;">{row.get('Jumlah Purata Beban (Jam)', 0.0)}</td>
        </tr>
        """

    rows_html = ""
    for idx, row in enumerate(df.to_dict(orient='records'), 1):
        status_color = "#16a34a" if "SEIMBANG" in str(row.get('Status_Agihan', '')) else ("#dc2626" if "TINGGI" in str(row.get('Status_Agihan', '')) else "#ca8a04")
        kumpulan_badge = '<span style="background-color:#eff6ff; color:#1e40af; padding:2px 6px; border-radius:4px; font-weight:bold;">GURU</span>' if row.get('Kumpulan', '') == 'Guru' else '<span style="background-color:#fef3c7; color:#92400e; padding:2px 6px; border-radius:4px; font-weight:bold;">AKP</span>'
        
        rows_html += f"""
        <tr>
            <td style="text-align:center;">{idx}</td>
            <td><b>{row.get('Nama', '')}</b></td>
            <td style="text-align:center;">{kumpulan_badge}</td>
            <td>{row.get('Jawatan', '')}</td>
            <td style="text-align:center;">{row.get('Waktu_PdP', 0)}</td>
            <td style="text-align:center;">{row.get('Jam_PdP', 0.0)}</td>
            <td style="text-align:center;">{row.get('Jam_Portfolio', 0.0)}</td>
            <td style="text-align:center;">{row.get('Jam_Jawatankuasa', 0.0)}</td>
            <td style="text-align:center; font-weight:bold;">{row.get('Jumlah_Jam_Beban', 0.0)}</td>
            <td style="text-align:center; color:{status_color}; font-weight:bold;">{row.get('Status_Agihan', '')}</td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Laporan Perincian & Bandingan Beban Tugas - {nama_sek}</title>
    <style>
        @page {{ size: A4 landscape; margin: 10mm; }}
        body {{ font-family: Arial, sans-serif; color: #0f172a; margin: 0; padding: 5px; font-size: 11px; }}
        .header-container {{ display: flex; align-items: center; justify-content: space-between; border-bottom: 3px double #1e3a8a; padding-bottom: 8px; margin-bottom: 12px; }}
        .header-logo {{ flex: 0 0 75px; text-align: center; }}
        .header-logo img {{ max-height: 65px; width: auto; object-fit: contain; }}
        .header-details {{ flex: 1; text-align: center; padding: 0 10px; }}
        .header-details h2 {{ margin: 0 0 3px 0; font-size: 16px; color: #1e3a8a; text-transform: uppercase; font-weight: 800; letter-spacing: 0.5px; }}
        .header-details p {{ margin: 2px 0; font-size: 10px; color: #334155; line-height: 1.3; }}
        .report-title {{ text-align: center; font-size: 12.5px; font-weight: bold; margin: 10px 0 12px 0; text-transform: uppercase; letter-spacing: 0.5px; background-color: #f8fafc; padding: 6px; border: 1px solid #e2e8f0; border-radius: 4px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 5px; margin-bottom: 15px; }}
        th, td {{ border: 1px solid #cbd5e1; padding: 5px 6px; }}
        th {{ background-color: #f1f5f9; font-weight: bold; text-align: center; color: #1e293b; font-size: 10.5px; }}
        tr:nth-child(even) {{ background-color: #f8fafc; }}
        .section-header {{ font-size: 12px; font-weight: bold; color: #1e3a8a; margin-top: 10px; margin-bottom: 5px; text-transform: uppercase; }}
        .footer {{ margin-top: 20px; display: flex; justify-content: space-between; font-size: 9.5px; color: #64748b; border-top: 1px solid #e2e8f0; padding-top: 6px; }}
        @media print {{ .no-print {{ display: none; }} }}
    </style>
</head>
<body onload="window.print()">
    <div class="header-container">
        <div class="header-logo"><img src="{logo_b64}" alt="Lencana Sekolah"></div>
        <div class="header-details">
            <h2>{nama_sek} ({kod_sek})</h2>
            <p>{alamat}</p>
            <p>{contact_str}</p>
            <p><b>Sesi Persekolahan:</b> {sesi} | <b>Pengetua / Guru Besar:</b> {gb}</p>
        </div>
        <div class="header-logo" style="visibility: hidden;"><img src="{logo_b64}" alt="Spacer"></div>
    </div>

    <div class="report-title">LAPORAN PERINCIAN BEBAN TUGAS KAKITANGAN DENGAN BANDINGAN KUMPULAN</div>

    <div class="section-header">1. ANALISIS PERBANDINGAN PURATA BEBAN KERJA MENGIKUT KUMPULAN</div>
    <table>
        <thead>
            <tr>
                <th>Kumpulan Kakitangan</th>
                <th style="width: 100px;">Jumlah Anggota</th>
                <th style="width: 110px;">Purata Jam PdP</th>
                <th style="width: 150px;">Purata Jam Portfolio (H+P)</th>
                <th style="width: 160px;">Purata Jam Jawatankuasa (J)</th>
                <th style="width: 150px;">Jumlah Purata Beban (Jam)</th>
            </tr>
        </thead>
        <tbody>{summary_rows_html}</tbody>
    </table>

    <div class="section-header">2. PERINCIAN INDIVIDU AGIHAN BEBAN TUGAS KAKITANGAN ({len(df)} REKOD)</div>
    <table>
        <thead>
            <tr>
                <th style="width: 30px;">Bil</th>
                <th>Nama Pegawai / Kakitangan</th>
                <th style="width: 70px;">Kumpulan</th>
                <th>Jawatan Hakiki</th>
                <th style="width: 60px;">Waktu PdP</th>
                <th style="width: 60px;">Jam PdP</th>
                <th style="width: 70px;">Jam Portfolio</th>
                <th style="width: 70px;">Jam Jawatankuasa</th>
                <th style="width: 70px;">Jumlah Beban (Jam)</th>
                <th style="width: 85px;">Status Agihan</th>
            </tr>
        </thead>
        <tbody>{rows_html}</tbody>
    </table>

    <div class="footer">
        <div>MySG KPM: Sistem Pengurusan & Analisis Beban Kerja &bull; Dicetak pada: {time.strftime('%d/%m/%Y %H:%M')}</div>
        <div>Muka Surat 1 daripada 1</div>
    </div>
</body>
</html>"""

def generate_individual_detailed_report_html(staf_row, school_info, df_summary_comp, session_state_ref=None):
    """Menjana templat HTML Laporan Perincian Individu & Bandingan Kumpulan (A4 Portrait) DENGAN PENAPISAN KETAT ENTRI KOSONG."""
    s_det = extract_school_details(school_info, session_state_ref)
    nama_sek, kod_sek, sesi = s_det['nama_sekolah'], s_det['kod_sekolah'], s_det['tahun_sesi']
    alamat, no_tel, no_faks, email_sek = s_det['alamat_sekolah'], s_det['no_tel'], s_det['no_faks'], s_det['email_sekolah']

    logo_b64 = get_school_badge_base64(school_info, session_state_ref)

    contact_parts = []
    if no_tel:
        contact_parts.append(f"Tel: {no_tel}")
    if no_faks and no_faks.upper() != 'NIL':
        contact_parts.append(f"Faks: {no_faks}")
    if email_sek:
        contact_parts.append(f"Emel: {email_sek}")
    contact_str = " | ".join(contact_parts)

    nama_staf = staf_row.get('Nama', '-')
    jawatan_staf = staf_row.get('Jawatan', '-')
    gred_raw = str(staf_row.get('Gred', '-'))
    gred_staf = '-' if is_empty_val(gred_raw) else gred_raw
    kumpulan_staf = staf_row.get('Kumpulan', 'Guru')

    is_sm = "Menengah" in str(school_info.get('jenis_sekolah', 'Sekolah Rendah'))
    mapping_h = MYSG_PORTFOLIO_H_SM if is_sm else MYSG_PORTFOLIO_H_SR

    # KIRA JUMLAH JAM & PURATA KUMPULAN
    jam_pdp = round(float(staf_row.get('JUMLAH_JAM_PDP', 0.0) or 0.0), 1)
    jam_h = round(float(staf_row.get('JUMLAH_JAM_PORTFOLIO_H', 0.0) or 0.0), 1)
    jam_p = round(float(staf_row.get('JUMLAH_JAM_PORTFOLIO_P', 0.0) or 0.0), 1)
    jam_j = round(float(staf_row.get('JUMLAH_JAM_JAWATANKUASA', 0.0) or 0.0), 1)
    total_jam = round(float(staf_row.get('JUMLAH_BEBAN_KESELURAHAN', jam_pdp + jam_h + jam_p + jam_j) or 0.0), 1)

    row_comp = df_summary_comp[df_summary_comp['Kumpulan Kakitangan'].str.contains(kumpulan_staf, case=False, na=False)]
    purata_kumpulan = round(float(row_comp['Jumlah Purata Beban (Jam)'].values[0]), 1) if not row_comp.empty else 0.0
    perbezaan = round(total_jam - purata_kumpulan, 1)
    diff_label = f"+{perbezaan} jam dari purata" if perbezaan >= 0 else f"{perbezaan} jam dari purata"

    rows_tugas = []

    # =========================================================================
    # KAD 1: PORTFOLIO BERJAWATAN HAKIKI (KOD H) & PENGAJARAN DAN PEMBELAJARAN (PDP)
    # =========================================================================
    rows_tugas.append("""
    <tr style="background-color: #1e3a8a; color: #ffffff; font-weight: bold;">
        <td colspan="2" style="padding: 6px 10px; font-size: 11px;">
            1. PORTFOLIO BERJAWATAN HAKIKI (KOD H) & PENGAJARAN DAN PEMBELAJARAN (PDP)
        </td>
        <td style="text-align: center; font-size: 11px; padding: 6px 10px;">PEMBERAT JAM</td>
    </tr>
    """)

    # A. Jawatan Hakiki Kod H
    kod_h_raw = str(staf_row.get('Kod_H_1', staf_row.get('Jawatan', ''))).strip()
    kod_h = kod_h_raw.split('|')[0].strip() if '|' in kod_h_raw else kod_h_raw[:4].strip()
    
    if kod_h in mapping_h:
        nama_h, jam_val_h = mapping_h[kod_h]
        rows_tugas.append(f"""
        <tr>
            <td style="text-align:center; width: 35px;">•</td>
            <td><b>{kod_h}</b> | {nama_h} (Jawatan Hakiki)</td>
            <td style="text-align:center; width: 120px;">{jam_val_h} jam</td>
        </tr>
        """)
    else:
        rows_tugas.append(f"""
        <tr>
            <td style="text-align:center; width: 35px;">•</td>
            <td>{jawatan_staf} (Jawatan Hakiki)</td>
            <td style="text-align:center; width: 120px;">{jam_h} jam</td>
        </tr>
        """)

    # B. Subjek + Kelas + Waktu PdP (Hanya paparkan jika subjek ADA)
    has_pdp = False
    for i in range(1, 16):
        subj = staf_row.get(f'Subjek_{i}')
        kelas = staf_row.get(f'Kelas_{i}')
        waktu = staf_row.get(f'Waktu_{i}')

        if not is_empty_val(subj):
            has_pdp = True
            subj_clean = str(subj).strip()
            kelas_str = f" ({str(kelas).strip()})" if not is_empty_val(kelas) else ""
            waktu_num = float(waktu) if not is_empty_val(waktu) else 0.0
            jam_subj = round(waktu_num * 0.5, 1)
            rows_tugas.append(f"""
            <tr>
                <td style="text-align:center;">•</td>
                <td>{subj_clean}{kelas_str} &bull; <i>{int(waktu_num) if waktu_num.is_integer() else waktu_num} Waktu</i></td>
                <td style="text-align:center;">{jam_subj} jam</td>
            </tr>
            """)

    if not has_pdp and jam_pdp > 0:
        waktu_tot = staf_row.get('JUMLAH_WAKTU_PDP', 0)
        rows_tugas.append(f"""
        <tr>
            <td style="text-align:center;">•</td>
            <td>Tugas Hakiki Pengajaran & Pembelajaran ({waktu_tot} Waktu)</td>
            <td style="text-align:center;">{jam_pdp} jam</td>
        </tr>
        """)

    # =========================================================================
    # KAD 2: PORTFOLIO TANPA JAWATAN (KOD P)
    # =========================================================================
    p_cols = [c for c in staf_row.index if str(c).startswith('Kod_P_')]
    has_p_items = False
    p_rows_temp = []

    for pc in p_cols:
        val_p_raw = staf_row.get(pc)
        if is_empty_val(val_p_raw):
            continue

        val_p_str = str(val_p_raw).strip()
        kod_p = val_p_str.split('|')[0].strip() if '|' in val_p_str else val_p_str[:4].strip()
        idx_num = pc.replace('Kod_P_', '')
        detail_val = staf_row.get(f'Detail_P_{idx_num}')

        if kod_p in MYSG_PORTFOLIO_P:
            has_p_items = True
            nama_p, jam_val_p = MYSG_PORTFOLIO_P[kod_p]
            detail_str = f" &bull; <i style='color:#1e40af;'>{str(detail_val).strip()}</i>" if not is_empty_val(detail_val) else ""
            p_rows_temp.append(f"""
            <tr>
                <td style="text-align:center;">•</td>
                <td><b>{kod_p}</b> | {nama_p}{detail_str}</td>
                <td style="text-align:center;">{jam_val_p} jam</td>
            </tr>
            """)
        elif len(val_p_str) >= 2 and not is_empty_val(val_p_str):
            has_p_items = True
            detail_str = f" &bull; <i style='color:#1e40af;'>{str(detail_val).strip()}</i>" if not is_empty_val(detail_val) else ""
            p_rows_temp.append(f"""
            <tr>
                <td style="text-align:center;">•</td>
                <td>{val_p_str}{detail_str}</td>
                <td style="text-align:center;">1.0 jam</td>
            </tr>
            """)

    rows_tugas.append("""
    <tr style="background-color: #0284c7; color: #ffffff; font-weight: bold;">
        <td colspan="2" style="padding: 6px 10px; font-size: 11px;">
            2. PORTFOLIO TANPA JAWATAN (KOD P)
        </td>
        <td style="text-align: center; font-size: 11px; padding: 6px 10px;">PEMBERAT JAM</td>
    </tr>
    """)

    if has_p_items:
        rows_tugas.extend(p_rows_temp)
    else:
        rows_tugas.append("""
        <tr>
            <td style="text-align:center;">-</td>
            <td style="color: #64748b; font-style: italic;">Tiada Agihan Portfolio Tanpa Jawatan (Kod P)</td>
            <td style="text-align:center;">0.0 jam</td>
        </tr>
        """)

    # =========================================================================
    # KAD 3: JAWATANKUASA SEKOLAH (KOD J)
    # =========================================================================
    j_cols = [c for c in staf_row.index if str(c).startswith('Kod_J_')]
    has_j_items = False
    j_rows_temp = []

    for jc in j_cols:
        val_j_raw = staf_row.get(jc)
        if is_empty_val(val_j_raw):
            continue

        val_j_str = str(val_j_raw).strip()
        kod_j = val_j_str.split('|')[0].strip() if '|' in val_j_str else val_j_str[:4].strip()
        idx_num = jc.replace('Kod_J_', '')
        detail_val = staf_row.get(f'Detail_J_{idx_num}')

        if kod_j in MYSG_JAWATANKUASA_J:
            has_j_items = True
            nama_j, jam_val_j = MYSG_JAWATANKUASA_J[kod_j]
            detail_str = f" &bull; <i style='color:#065f46;'>{str(detail_val).strip()}</i>" if not is_empty_val(detail_val) else ""
            j_rows_temp.append(f"""
            <tr>
                <td style="text-align:center;">•</td>
                <td><b>{kod_j}</b> | {nama_j}{detail_str}</td>
                <td style="text-align:center;">{jam_val_j} jam</td>
            </tr>
            """)
        elif len(val_j_str) >= 2 and not is_empty_val(val_j_str):
            has_j_items = True
            detail_str = f" &bull; <i style='color:#065f46;'>{str(detail_val).strip()}</i>" if not is_empty_val(detail_val) else ""
            j_rows_temp.append(f"""
            <tr>
                <td style="text-align:center;">•</td>
                <td>{val_j_str}{detail_str}</td>
                <td style="text-align:center;">1.0 jam</td>
            </tr>
            """)

    rows_tugas.append("""
    <tr style="background-color: #059669; color: #ffffff; font-weight: bold;">
        <td colspan="2" style="padding: 6px 10px; font-size: 11px;">
            3. JAWATANKUASA SEKOLAH (KOD J)
        </td>
        <td style="text-align: center; font-size: 11px; padding: 6px 10px;">PEMBERAT JAM</td>
    </tr>
    """)

    if has_j_items:
        rows_tugas.extend(j_rows_temp)
    else:
        rows_tugas.append("""
        <tr>
            <td style="text-align:center;">-</td>
            <td style="color: #64748b; font-style: italic;">Tiada Agihan Jawatankuasa Sekolah (Kod J)</td>
            <td style="text-align:center;">0.0 jam</td>
        </tr>
        """)

    rows_tugas_html = "".join(rows_tugas)

    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Laporan Perincian Beban Tugas - {nama_staf}</title>
    <style>
        @page {{ size: A4 portrait; margin: 12mm; }}
        body {{ font-family: Arial, sans-serif; color: #0f172a; margin: 0; padding: 5px; font-size: 10.5px; }}
        .header-container {{ display: flex; align-items: center; justify-content: space-between; border-bottom: 2px solid #1e3a8a; padding-bottom: 8px; margin-bottom: 12px; }}
        .header-logo {{ flex: 0 0 70px; text-align: center; }}
        .header-logo img {{ max-height: 60px; width: auto; object-fit: contain; }}
        .header-details {{ flex: 1; text-align: center; padding: 0 10px; }}
        .header-details h2 {{ margin: 0; font-size: 14px; color: #1e3a8a; text-transform: uppercase; font-weight: bold; }}
        .header-details p {{ margin: 2px 0; font-size: 9.5px; color: #334155; }}
        .report-title {{ text-align: center; font-size: 12px; font-weight: bold; margin: 8px 0; text-transform: uppercase; background-color: #f1f5f9; padding: 6px; border-radius: 4px; border: 1px solid #cbd5e1; }}
        .info-box {{ display: flex; justify-content: space-between; background-color: #f8fafc; border: 1px solid #e2e8f0; padding: 8px 12px; border-radius: 5px; margin-bottom: 10px; font-size: 10px; }}
        .comp-card {{ display: flex; justify-content: space-around; background-color: #eff6ff; border: 1px solid #bfdbfe; padding: 8px; border-radius: 5px; margin-bottom: 12px; text-align: center; }}
        .comp-card div {{ flex: 1; }}
        .comp-card h3 {{ margin: 2px 0; font-size: 15px; color: #1e40af; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 5px; }}
        th, td {{ border: 1px solid #cbd5e1; padding: 5px 7px; }}
        th {{ background-color: #f1f5f9; font-weight: bold; text-align: center; color: #1e293b; font-size: 10px; }}
        .footer {{ margin-top: 20px; display: flex; justify-content: space-between; font-size: 9px; color: #64748b; border-top: 1px solid #e2e8f0; padding-top: 5px; }}
        @media print {{ .no-print {{ display: none; }} }}
    </style>
</head>
<body onload="window.print()">
    <div class="header-container">
        <div class="header-logo"><img src="{logo_b64}" alt="Lencana Sekolah"></div>
        <div class="header-details">
            <h2>{nama_sek}</h2>
            <p>Kod: {kod_sek} | {alamat}</p>
            <p>{contact_str}</p>
        </div>
        <div class="header-logo" style="visibility: hidden;"><img src="{logo_b64}" alt="Spacer"></div>
    </div>

    <div class="report-title">LAPORAN PERINCIAN BEBAN TUGAS INDIVIDU</div>

    <div class="info-box">
        <div>
            <b>Nama Pegawai:</b> {nama_staf}<br>
            <b>Jawatan Hakiki:</b> {jawatan_staf}<br>
            <b>Gred Perkhidmatan:</b> {gred_staf}
        </div>
        <div style="text-align: right;">
            <b>Kumpulan:</b> {kumpulan_staf}<br>
            <b>Sesi Persekolahan:</b> {sesi}<br>
            <b>Tarikh Cetakan:</b> {time.strftime('%d/%m/%Y')}
        </div>
    </div>

    <div class="comp-card">
        <div>
            <span style="font-size: 9.5px; color: #475569;">Beban Kerja Pegawai</span>
            <h3>{total_jam} Jam</h3>
        </div>
        <div style="border-left: 1px solid #bfdbfe; border-right: 1px solid #bfdbfe;">
            <span style="font-size: 9.5px; color: #475569;">Purata Kumpulan ({kumpulan_staf})</span>
            <h3>{purata_kumpulan} Jam</h3>
        </div>
        <div>
            <span style="font-size: 9.5px; color: #475569;">Kedudukan / Perbezaan</span>
            <h3 style="color: {'#dc2626' if perbezaan > 5 else '#16a34a'};">{diff_label}</h3>
        </div>
    </div>

    <div style="font-weight: bold; margin-bottom: 4px; font-size: 10.5px;">SENARAI PERINCIAN AGIHAN TUGAS & PEMBERAT (JAM):</div>
    <table>
        <tbody>
            {rows_tugas_html}
            <tr style="background-color: #f8fafc; font-weight: bold;">
                <td colspan="2" style="text-align: right; padding: 8px 10px;">JUMLAH BEBAN KERJA KESELURUHAN:</td>
                <td style="text-align: center; color: #1e3a8a; font-size: 12px; padding: 8px 10px;">{total_jam} JAM</td>
            </tr>
        </tbody>
    </table>

    <!-- KOTAK KETETAPAN & GARIS PANDUAN MYSG KPM -->
    <div style="margin-top: 12px; border: 1px solid #cbd5e1; background-color: #f8fafc; padding: 8px; border-radius: 4px; font-size: 9px; line-height: 1.4;">
        <div style="font-weight: bold; color: #1e3a8a; border-bottom: 1px solid #cbd5e1; padding-bottom: 3px; margin-bottom: 4px; text-transform: uppercase;">
            📌 KETETAPAN & GARIS PANDUAN BEBAN KERJA WARGA SEKOLAH (MYSG KPM):
        </div>
        <table style="width: 100%; border: none; font-size: 8.5px; margin: 0;">
            <tr style="background: transparent;">
                <td style="border: none; padding: 2px;">• <b>Beban Kerja Seimbang:</b> 35.0 – 50.0 Jam / Minggu</td>
                <td style="border: none; padding: 2px;">• <b>Asas Pengiraan PdP:</b> 1 Waktu PdP = 0.5 Jam (30 Minit)</td>
            </tr>
            <tr style="background: transparent;">
                <td style="border: none; padding: 2px;">• <b>Portfolio Berjawatan Hakiki (Kod H):</b> Berdasarkan Deskripsi Tugas Jawatan Rasmi</td>
                <td style="border: none; padding: 2px;">• <b>Prinsip Kesaksamaan:</b> Agihan Portfolio (P) & Jawatankuasa (J) dilaksanakan secara adil mengikut purata beban kumpulan.</td>
            </tr>
        </table>
    </div>

    <div class="footer">
        <div>MySG KPM System &bull; Dokumen Analisis Beban Kerja Rasmi</div>
        <div>Dicetak pada: {time.strftime('%d/%m/%Y %H:%M')}</div>
    </div>
</body>
</html>"""

def generate_appointment_letter_html(staf_row, school_info, session_state_ref=None):
    """Menjana templat HTML Surat Lantikan Tugas Rasmi A4 Portrait dengan Header Rasmi DUAL-LOGO (Jata Negara & Lencana Sekolah)."""
    s_det = extract_school_details(school_info, session_state_ref)
    nama_sek, kod_sek, sesi = s_det['nama_sekolah'], s_det['kod_sekolah'], s_det['tahun_sesi']
    alamat, no_tel, no_faks, email_sek, gb = s_det['alamat_sekolah'], s_det['no_tel'], s_det['no_faks'], s_det['email_sekolah'], s_det['nama_gb']

    logo_b64 = get_school_badge_base64(school_info, session_state_ref)
    tarikh_hari_ini = time.strftime('%d %B %Y')

    contact_parts = []
    if no_tel:
        contact_parts.append(f"No. Tel: {no_tel}")
    if no_faks and no_faks.upper() != 'NIL':
        contact_parts.append(f"No. Faks: {no_faks}")
    if email_sek:
        contact_parts.append(f"Emel: {email_sek}")
    contact_str = " | ".join(contact_parts)

    nama_staf = staf_row.get('Nama', 'NAMA PEGAWAI')
    jawatan_staf = staf_row.get('Jawatan', 'GURU / AKP')
    gred_staf = staf_row.get('Gred', '-')

    is_sm = "Menengah" in str(school_info.get('jenis_sekolah', 'Sekolah Rendah'))
    mapping_h = MYSG_PORTFOLIO_H_SM if is_sm else MYSG_PORTFOLIO_H_SR

    tugas_h = []
    kod_h = str(staf_row.get('Kod_H_1', '')).strip()
    if kod_h in mapping_h:
        tugas_h.append(f"{mapping_h[kod_h][0]} ({mapping_h[kod_h][1]} jam)")
    else:
        tugas_h.append(f"{jawatan_staf}")

    tugas_p = []
    p_cols = [c for c in staf_row.index if str(c).startswith('Kod_P_')]
    for pc in p_cols:
        val_p_raw = staf_row.get(pc)
        if is_empty_val(val_p_raw):
            continue
        val_p = str(val_p_raw).strip()
        kod = val_p.split('|')[0].strip() if '|' in val_p else val_p[:4].strip()
        idx_num = pc.replace('Kod_P_', '')
        detail_val = staf_row.get(f'Detail_P_{idx_num}')
        detail_str = f" &bull; <i>{detail_val}</i>" if not is_empty_val(detail_val) else ""

        if kod in MYSG_PORTFOLIO_P:
            tugas_p.append(f"{kod} | {MYSG_PORTFOLIO_P[kod][0]}{detail_str} ({MYSG_PORTFOLIO_P[kod][1]} jam)")
        elif len(val_p) >= 2:
            tugas_p.append(f"{val_p}{detail_str} (1.0 jam)")

    tugas_j = []
    j_cols = [c for c in staf_row.index if str(c).startswith('Kod_J_')]
    for jc in j_cols:
        val_j_raw = staf_row.get(jc)
        if is_empty_val(val_j_raw):
            continue
        val_j = str(val_j_raw).strip()
        kod = val_j.split('|')[0].strip() if '|' in val_j else val_j[:4].strip()
        idx_num = jc.replace('Kod_J_', '')
        detail_val = staf_row.get(f'Detail_J_{idx_num}')
        detail_str = f" &bull; <i>{detail_val}</i>" if not is_empty_val(detail_val) else ""

        if kod in MYSG_JAWATANKUASA_J:
            tugas_j.append(f"{kod} | {MYSG_JAWATANKUASA_J[kod][0]}{detail_str} ({MYSG_JAWATANKUASA_J[kod][1]} jam)")
        elif len(val_j) >= 2:
            tugas_j.append(f"{val_j}{detail_str} (1.0 jam)")

    h_list_html = "".join([f"<li>{item}</li>" for item in tugas_h])
    p_list_html = "".join([f"<li>{item}</li>" for item in tugas_p]) if tugas_p else "<li><i>Tiada Agihan Portfolio Tanpa Jawatan</i></li>"
    j_list_html = "".join([f"<li>{item}</li>" for item in tugas_j]) if tugas_j else "<li><i>Tiada Agihan Jawatankuasa Sekolah</i></li>"

    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Surat Lantikan Tugas - {nama_staf}</title>
    <style>
        @page {{ size: A4 portrait; margin: 15mm; }}
        body {{ font-family: 'Times New Roman', Times, serif; color: #000000; margin: 0; padding: 10px; font-size: 11.5pt; line-height: 1.4; }}
        .header-container {{ display: flex; align-items: center; justify-content: space-between; border-bottom: 2px solid #000000; padding-bottom: 8px; margin-bottom: 15px; }}
        .header-logo {{ flex: 0 0 70px; text-align: center; }}
        .header-logo img {{ max-height: 65px; width: auto; object-fit: contain; }}
        .header-details {{ flex: 1; text-align: center; padding: 0 10px; }}
        .header-details h2 {{ margin: 0; font-size: 13pt; font-weight: bold; text-transform: uppercase; }}
        .header-details p {{ margin: 2px 0; font-size: 9.5pt; font-family: Arial, sans-serif; }}
        .ref-table {{ width: 100%; margin-bottom: 15px; font-size: 10.5pt; }}
        .ref-table td {{ padding: 2px 0; vertical-align: top; }}
        .title-box {{ text-align: center; font-size: 12pt; font-weight: bold; text-decoration: underline; margin: 12px 0; text-transform: uppercase; }}
        .content-p {{ text-align: justify; margin-bottom: 10px; }}
        .section-title {{ font-weight: bold; margin-top: 8px; margin-bottom: 4px; font-size: 10.5pt; }}
        ul {{ margin-top: 2px; margin-bottom: 8px; padding-left: 20px; font-size: 10.5pt; }}
        li {{ margin-bottom: 3px; }}
        .signature-box {{ margin-top: 30px; page-break-inside: avoid; }}
        .footer-note {{ margin-top: 25px; font-size: 8.5pt; font-style: italic; color: #555555; border-top: 1px solid #ccc; padding-top: 4px; }}
        @media print {{ .no-print {{ display: none; }} }}
    </style>
</head>
<body onload="window.print()">
    <!-- HEADER RASMI KPM (DUAL LOGO: JATA NEGARA & LENCANA SEKOLAH) -->
    <div class="header-container">
        <div class="header-logo">
            <img src="{JATA_NEGARA_BASE64}" alt="Jata Negara">
        </div>
        <div class="header-details">
            <div style="font-size: 9pt; font-weight: bold; font-family: Arial, sans-serif; text-transform: uppercase; letter-spacing: 0.5px;">KEMENTERIAN PENDIDIKAN MALAYSIA</div>
            <h2>{nama_sek}</h2>
            <p>Kod Sekolah: {kod_sek} | {alamat}</p>
            <p>{contact_str}</p>
        </div>
        <div class="header-logo">
            <img src="{logo_b64}" alt="Lencana Sekolah">
        </div>
    </div>

    <table class="ref-table">
        <tr>
            <td style="width: 60%;"><b>Kepada:</b><br><b>{nama_staf}</b><br>{jawatan_staf} (Gred: {gred_staf})<br>{nama_sek}</td>
            <td style="width: 40%; text-align: right;"><b>Ruj. Kami:</b> {kod_sek}/100-1/4<br><b>Tarikh:</b> {tarikh_hari_ini}</td>
        </tr>
    </table>

    <p>Tuan/Puan,</p>

    <div class="title-box">SURAT LANTIKAN TUGAS RASMI MYSG KPM SESI PERSEKOLAHAN {sesi}</div>

    <div class="content-p">
        Dengan segala hormatnya perkara di atas adalah dirujuk.
    </div>

    <div class="content-p">
        2. Sukacita dimaklumkan bahawa Pengurusan Sekolah dengan rasminya melantik tuan/puan untuk menjalankan tugas-tugas rasmi mengikut Standard Panduan Pengurusan Sekolah (MySG KPM) bagi Sesi Persekolahan <b>{sesi}</b> seperti senarai berikut:
    </div>

    <div style="margin-left: 10px;">
        <div class="section-title">A. PORTFOLIO BERJAWATAN HAKIKI (H):</div>
        <ul>{h_list_html}</ul>

        <div class="section-title">B. PORTFOLIO TANPA JAWATAN (P):</div>
        <ul>{p_list_html}</ul>

        <div class="section-title">C. JAWATANKUASA SEKOLAH (J):</div>
        <ul>{j_list_html}</ul>
    </div>

    <div class="content-p" style="margin-top: 12px;">
        3. Diharapkan tuan/puan dapat melaksanakan amanah dan tanggungjawab ini dengan penuh dedikasi, integriti, serta profesionalisme demi meningkatkan kecemerlangan sekolah.
    </div>

    <div class="content-p">
        Sekian, terima kasih.
    </div>

    <div style="margin-top: 15px; font-weight: bold;">
        "MALAYSIA MADANI"<br>
        "BERKHIDMAT UNTUK NEGARA"
    </div>

    <div class="signature-box">
        Saya yang menjalankan amanah,<br><br><br><br>
        __________________________________<br>
        <b>({gb})</b><br>
        Pengetua / Guru Besar<br>
        {nama_sek}
    </div>

    <div class="footer-note">
        * Surat ini dijana secara automatik menerusi MySG KPM System &bull; Dicetak pada: {time.strftime('%d/%m/%Y %H:%M')}
    </div>
</body>
</html>"""