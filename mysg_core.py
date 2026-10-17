"""
========================================================================
MYSG KPM: SISTEM PENGURUSAN & ANALISIS BEBAN KERJA
MODULE: CORE ENGINE & CONSTANTS (PENGELASAN TEPAT HR/HM & BEBAN KERJA)
========================================================================
"""

import pandas as pd
import numpy as np
import re

# NAMA RASMI, VERSI PEMBANGUNAN & TARIKH KEMASKINI RASMI
SYSTEM_NAME = "MySG KPM: Sistem Pengurusan & Analisis Beban Kerja"
SYSTEM_VERSION = "1.0.0"
SYSTEM_RELEASE_DATE = "18 Oktober 2026"

# GRED RASMI KPM (PPP DAN AKP)
GRED_RASMI_KPM = [
    "DG54", "DG52", "DG48", "DG44", "DG42", "DG41", "DG38", "DG34", "DG32", "DG29",
    "N36", "N32", "N29", "N22", "N19", "N11",
    "FA32", "FA29", "FT29", "FT19", "C26", "C22", "C19",
    "W29", "W19", "H19", "N1"
]

# PORTFOLIO BERJAWATAN HAKIKI (H) - SEKOLAH RENDAH (HR01 - HR37)
MYSG_PORTFOLIO_H_SR = {
    "HR01": ("Guru Besar (PGB)", 2.5),
    "HR02": ("Guru Penolong Kanan Pentadbiran", 6.0),
    "HR03": ("Guru Penolong Kanan Hal Ehwal Murid", 6.0),
    "HR04": ("Guru Penolong Kanan Kokurikulum", 6.0),
    "HR05": ("Guru Penolong Kanan Petang", 6.0),
    "HR06": ("Guru Penolong Kanan Pendidikan Khas", 6.0),
    "HR07": ("Penyelaras Aktiviti Menengah (SR Model Khas K9)", 6.0),
    "HR08": ("Guru Penyelaras Bestari", 4.0),
    "HR09": ("Guru Perpustakaan dan Media", 4.0),
    "HR10": ("Guru Data", 8.0),
    "HR11": ("Guru Prasekolah", 10.0),
    "HR12": ("Guru Akademik KSSR", 0.0),
    "HR13": ("Guru Akademik KSSM (SR K9)", 0.0),
    "HR14": ("Guru Amali (SR K9)", 0.0),
    "HR15": ("Guru Bahasa Cina", 0.0),
    "HR16": ("Guru Bahasa Tamil", 0.0),
    "HR17": ("Guru Pendidikan Islam", 0.0),
    "HR18": ("Guru Pemulihan / Pemulihan Khas", 0.0),
    "HR19": ("Guru Program Integrasi (PPKI)", 0.0),
    "HR20": ("Guru Kod Braille", 5.0),
    "HR21": ("Guru Kod Tangan", 5.0),
    "HR22": ("Guru Bimbingan (GBK)", 3.0),
    "HR23": ("Guru Kaunseling (SR K9)", 3.0),
    "HR24": ("Pembantu Tadbir (P/O)", 40.0),
    "HR25": ("Pembantu Tadbir (Kewangan)", 40.0),
    "HR26": ("Juruteknik Komputer", 40.0),
    "HR27": ("Pembantu Pengurusan Murid (Prasekolah)", 40.0),
    "HR28": ("Pembantu Pengurusan Murid (PPKI)", 40.0),
    "HR29": ("Pembantu Pengurusan Murid (Asrama)", 40.0),
    "HR30": ("Pembantu Operasi", 40.0),
    "HR31": ("Penyelia Asrama", 40.0),
    "HR32": ("Pemandu Kenderaan", 40.0),
    "HR33": ("Pembantu Laut", 40.0),
    "HR34": ("Pembantu Penyediaan Makanan", 40.0),
    "HR35": ("Pembantu Awam (SR K9)", 40.0),
    "HR36": ("Pembantu Makmal (SR K9)", 40.0),
    "HR37": ("Pembantu Kemahiran (SKPK)", 40.0)
}

# PORTFOLIO BERJAWATAN HAKIKI (H) - SEKOLAH MENENGAH (HM01 - HM75)
MYSG_PORTFOLIO_H_SM = {
    "HM01": ("Pengetua (PGB)", 3.33),
    "HM02": ("Guru Penolong Kanan Pentadbiran", 8.0),
    "HM03": ("Guru Penolong Kanan Hal Ehwal Murid", 8.0),
    "HM04": ("Guru Penolong Kanan Kokurikulum", 8.0),
    "HM05": ("Guru Penolong Kanan Petang", 8.0),
    "HM06": ("Guru Penolong Kanan Pendidikan Khas", 8.0),
    "HM07": ("Guru Penolong Kanan Sukan (SSM)", 8.0),
    "HM08": ("Guru Penolong Kanan Seni (SSeM)", 8.0),
    "HM09": ("Guru Penolong Kanan Rendah (Model Khas)", 8.0),
    "HM10": ("Guru Penolong Kanan Tingkatan 6", 5.33),
    "HM11": ("Guru Penolong Kanan PraUniversiti", 5.33),
    "HM12": ("Guru Kanan Mata Pelajaran (GKMP)", 14.67),
    "HM13": ("Ketua Bidang Sukan (SSM)", 14.67),
    "HM14": ("Ketua Bidang Seni (SSeM)", 14.67),
    "HM15": ("Guru Penyelaras Bestari", 4.0),
    "HM16": ("Guru Perpustakaan dan Media", 4.0),
    "HM17": ("Guru Data", 8.0),
    "HM18": ("Guru Tingkatan Enam Akademik", 10.67),
    "HM19": ("Guru Tingkatan Enam Amali", 10.67),
    "HM20": ("Guru Tingkatan Enam Kokurikulum", 10.67),
    "HM21": ("Guru Pra-U Akademik", 10.67),
    "HM22": ("Guru Pra-U Amali", 10.67),
    "HM23": ("Guru Pra-U Kokurikulum", 10.67),
    "HM24": ("Guru Akademik KSSM", 0.0),
    "HM25": ("Guru Akademik KSSR (Model Khas/SSM)", 0.0),
    "HM26": ("Guru Akademik / MP Am (SMT)", 0.0),
    "HM27": ("Guru Akademik KBT (SABKM/TMUA)", 0.0),
    "HM28": ("Guru Akademik KBD (SABKM)", 0.0),
    "HM29": ("Guru Pendidikan Islam SR (Model Khas)", 0.0),
    "HM30": ("Guru Pendidikan Islam (SBP/SSM/SSeM)", 8.0),
    "HM31": ("Guru Dini (KBD)", 0.0),
    "HM32": ("Guru Tahfiz (KBT/TMUA)", 0.0),
    "HM33": ("Guru al-Quran (KKQ)", 2.0),
    "HM34": ("Guru Bahasa Antarabangsa", 0.0),
    "HM35": ("Guru Bahasa Inggeris (SBP/SSM/SSeM)", 0.0),
    "HM36": ("Guru Muzik (SBP)", 0.0),
    "HM37": ("Guru Psikologi Sukan (SSM)", 0.0),
    "HM38": ("Guru Unit Sains Sukan (SSM)", 0.0),
    "HM39": ("Guru Program Integrasi (PPKI)", 0.0),
    "HM40": ("Guru Kod Braille", 5.33),
    "HM41": ("Guru Kod Tangan", 5.33),
    "HM42": ("Guru Amali Bengkel (Ting 1-3)", 0.0),
    "HM43": ("Guru Amali (Ting 4-5 SSM/SSeM)", 0.0),
    "HM44": ("Guru MP Teknikal (SMT)", 0.0),
    "HM45": ("Guru MP Vokasional ICT", 0.0),
    "HM46": ("Guru MP Vokasional Rekacipta", 0.0),
    "HM47": ("Guru MP Vokasional (MPV)", 0.0),
    "HM48": ("Jurulatih Sukan Terbuka (SSM)", 0.0),
    "HM49": ("Jurulatih Sukan Tertutup (SSM)", 0.0),
    "HM50": ("Jurulatih Sukan (SSN)", 0.0),
    "HM51": ("Jurulatih Seni Terbuka (SSeM)", 0.0),
    "HM52": ("Guru Kaunseling (GBK)", 4.0),
    "HM53": ("Pembantu Tadbir (P/O)", 40.0),
    "HM54": ("Pembantu Tadbir (Kewangan)", 40.0),
    "HM55": ("Juruteknik Komputer", 40.0),
    "HM56": ("Pembantu Pengurusan Murid (PPKI)", 40.0),
    "HM57": ("Pembantu Pengurusan Murid (Asrama)", 40.0),
    "HM58": ("Pembantu Operasi", 40.0),
    "HM59": ("Penyelia Asrama", 40.0),
    "HM60": ("Pemandu Kenderaan", 40.0),
    "HM61": ("Pembantu Laut", 40.0),
    "HM62": ("Pembantu Penyediaan Makanan", 40.0),
    "HM63": ("Pembantu Awam", 40.0),
    "HM64": ("Pembantu Makmal", 40.0),
    "HM65": ("Pembantu Kemahiran", 40.0),
    "HM66": ("Juru Audio Visual", 40.0),
    "HM67": ("Jurupulih Perubatan", 40.0),
    "HM68": ("Operator Loji", 40.0),
    "HM69": ("Pembantu Perawatan Kesihatan", 40.0),
    "HM70": ("Penolong Pustakawan", 40.0),
    "HM71": ("Juru Fotografi", 40.0),
    "HM72": ("Jururawat Terlatih", 40.0),
    "HM73": ("Penolong Jurutera", 40.0),
    "HM74": ("Penolong Pegawai Perubatan", 40.0),
    "HM75": ("Pegawai Dietetik", 40.0)
}

# PORTFOLIO TANPA JAWATAN (P)
MYSG_PORTFOLIO_P = {
    "PR01": ("Guru Kelas", 2.0),
    "PR02": ("Guru Bertugas Harian", 1.5),
    "PR03": ("Penyelaras PPKI Lantikan Dalaman", 2.0),
    "PR04": ("Penyelaras LDP (SULDP)", 1.5),
    "PR05": ("Penyelaras Tahun", 1.5),
    "PR06": ("Setiausaha Jawatankuasa", 1.5),
    "PR07": ("Guru Bimbingan Lantikan Dalaman", 2.0),
    "PR08": ("Ketua Panitia Mata Pelajaran", 2.0),
    "PR09": ("Setiausaha Peperiksaan Dalaman", 2.5),
    "PR10": ("Setiausaha Peperiksaan Awam", 3.0),
    "PR11": ("Penyelaras ICT Lantikan Dalaman", 2.0),
    "PR12": ("Penyelaras PSS Lantikan Dalaman", 2.0),
    "PR13": ("Guru Resos Masalah Penglihatan", 2.0),
    "PR14": ("Ketua Guru Disiplin", 2.5),
    "PR15": ("Penyelaras SPBT", 2.5),
    "PR16": ("Warden Asrama", 4.0),
    "PR17": ("Setiausaha Sukan", 2.5),
    "PR18": ("Penyelaras Unit Kokurikulum", 2.0),
    "PR19": ("Guru Penasihat Unit Kokurikulum", 1.5),
    "PM01": ("Guru Kelas", 2.0),
    "PM02": ("Guru Bertugas Harian", 1.5),
    "PM03": ("Penyelaras PPKI Lantikan Dalaman", 2.0),
    "PM04": ("Setiausaha LDP (SULDP)", 1.5),
    "PM05": ("Penyelaras Tingkatan", 1.5),
    "PM06": ("Setiausaha Jawatankuasa", 1.5),
    "PM07": ("Ketua Panitia Mata Pelajaran", 2.5),
    "PM08": ("Setiausaha Peperiksaan Dalaman", 2.5),
    "PM09": ("Setiausaha Peperiksaan Awam (SPM/STPM)", 3.5),
    "PM10": ("Penyelaras ICT Lantikan Dalaman", 2.0),
    "PM11": ("Penyelaras Program PIMA", 2.0),
    "PM12": ("Guru Resos Masalah Penglihatan", 2.0),
    "PM13": ("Ketua Guru Disiplin", 3.0),
    "PM14": ("Penyelaras SPBT", 2.5),
    "PM15": ("Warden Asrama", 4.0),
    "PM16": ("Setiausaha Sukan", 3.0),
    "PM17": ("Penyelaras Unit Kokurikulum", 2.0),
    "PM18": ("Guru Penasihat Unit Kokurikulum", 1.5)
}

# JAWATANKUASA (J)
MYSG_JAWATANKUASA_J = {
    "JR01": ("JK Pengurusan Sekolah", 1.0),
    "JR02": ("JK Pengurusan Maklumat Sekolah (JKPMS)", 1.0),
    "JR03": ("JK Pengurusan Sumber Manusia", 1.0),
    "JR04": ("JK Pengurusan Kewangan, Akaun & Aset (JKPKAS)", 1.0),
    "JR05": ("JK Standard Kualiti Pendidikan Malaysia (SKPM)", 1.0),
    "JR06": ("JK Pendidikan Khas Sekolah", 1.0),
    "JR07": ("JK Pengurusan Prasekolah", 1.0),
    "JR08": ("JK Pengurusan Bencana Sekolah", 1.0),
    "JR09": ("JK Persatuan Ibu Bapa dan Guru (PIBG)", 1.0),
    "JR10": ("JK Kelab Kebajikan Guru & Kakitangan (KGK)", 1.0),
    "JR11": ("JK Pengurusan Murid Orang Asal", 1.0),
    "JR12": ("JK Pengurusan Kurikulum", 1.0),
    "JR13": ("JK Panitia Mata Pelajaran", 1.0),
    "JR14": ("JK Pentaksiran & Peperiksaan", 1.0),
    "JR15": ("JK Pusat Sumber Sekolah (PSS)", 1.0),
    "JR16": ("JK Pengurusan Hal Ehwal Murid (HEM)", 1.0),
    "JR17": ("JK Pengurusan Disiplin Murid", 1.0),
    "JR18": ("JK Pengurusan 3K", 1.0),
    "JR19": ("JK Bimbingan dan Kaunseling", 1.0),
    "JR20": ("JK Pengurusan Asrama", 1.5),
    "JR21": ("JK Pengurusan Kokurikulum", 1.0),
    "JR22": ("JK Pembangunan Sukan Sekolah", 1.0),
    "JR23": ("JK Sukan Tahunan Sekolah", 1.5),
    "JM01": ("JK Pengurusan Sekolah", 1.0),
    "JM02": ("JK Pengurusan Maklumat Sekolah (JKPMS)", 1.0),
    "JM03": ("JK Pengurusan Sumber Manusia", 1.0),
    "JM04": ("JK Pengurusan Kewangan, Akaun & Aset (JKPKAS)", 1.0),
    "JM05": ("JK Standard Kualiti Pendidikan Malaysia (SKPM)", 1.0),
    "JM06": ("JK Pendidikan Khas Sekolah", 1.0),
    "JM07": ("JK Pengurusan Bencana Sekolah", 1.0),
    "JM08": ("JK Persatuan Ibu Bapa dan Guru (PIBG)", 1.0),
    "JM09": ("JK Kelab Kebajikan Guru & Kakitangan (KGK)", 1.0),
    "JM10": ("JK Pengurusan Murid Orang Asal", 1.0),
    "JM11": ("JK Pengurusan Tingkatan 6", 1.0),
    "JM12": ("JK Pensijilan Kemahiran Malaysia", 1.0),
    "JM13": ("JK Program PIMA", 1.0),
    "JM14": ("JK Kesetiausahaan Sukan (SSM)", 1.0),
    "JM15": ("JK Kejurulatihan Sukan (SSM)", 1.0),
    "JM16": ("JK Sains Sukan Gunaan (SSM)", 1.0),
    "JM17": ("JK Promosi & Sesi Serlahan Seni (SSeM)", 1.0),
    "JM18": ("JK Pembangunan Fizikal Seni (SSeM)", 1.0),
    "JM19": ("JK Pameran Seni (SSeM)", 1.0),
    "JM20": ("JK Persembahan Seni (SSeM)", 1.0),
    "JM21": ("JK Pengurusan Kurikulum", 1.0),
    "JM22": ("JK Panitia Mata Pelajaran", 1.0),
    "JM23": ("JK Pentaksiran & Peperiksaan", 1.0),
    "JM24": ("JK Pusat Sumber Sekolah (PSS)", 1.0),
    "JM25": ("JK Pengurusan Hal Ehwal Murid (HEM)", 1.0),
    "JM26": ("JK Pengurusan Disiplin Murid", 1.0),
    "JM27": ("JK Pengurusan 3K", 1.0),
    "JM28": ("JK Bimbingan dan Kaunseling", 1.0),
    "JM29": ("JK Pengurusan Asrama", 1.5),
    "JM30": ("JK Pengurusan Kokurikulum", 1.0),
    "JM31": ("JK Pembangunan Sukan Sekolah", 1.0),
    "JM32": ("JK Sukan Tahunan Sekolah", 1.5),
    "JM33": ("JK Koperasi Sekolah", 1.5)
}

def determine_kategori_staf(row):
    """
    Mengenal pasti kategori staf (Guru vs AKP).
    Pemeriksaan kod hakiki MySG (HR/HM) diutamakan untuk membetulkan ketidaktetapan input.
    """
    jawatan = str(row.get('Jawatan', '')).upper().strip()
    detail_h = str(row.get('Detail_H_1', '')).upper().strip()
    gred = str(row.get('Gred', '')).upper().strip()

    # 1. SEMAKAN KOD HR / HM (UTAMA - MENGATASI KESILAPAN LABEL CSV)
    kod_match = re.search(r'(HR|HM)(\d{2})', jawatan) or re.search(r'(HR|HM)(\d{2})', detail_h)
    if kod_match:
        prefix, num_str = kod_match.groups()
        num_code = int(num_str)
        if prefix == 'HR':
            return 'Guru' if num_code <= 23 else 'Anggota Kumpulan Pelaksana'
        elif prefix == 'HM':
            return 'Guru' if num_code <= 52 else 'Anggota Kumpulan Pelaksana'

    # 2. SEMAKAN KATA KUNCI AKP JELAS
    if any(k in jawatan for k in ['PEMBANTU', 'JURUTEKNIK', 'OPERASI', 'PENYELIA', 'PEMANDU', 'TADBIR']):
        return 'Anggota Kumpulan Pelaksana'

    # 3. SEMAKAN GRED PERKHIDMATAN
    if any(gred.startswith(prefix) for prefix in ['DG', 'DC', 'UD']):
        return 'Guru'
    if any(gred.startswith(prefix) for prefix in ['N', 'FA', 'FT', 'C', 'W', 'H']):
        return 'Anggota Kumpulan Pelaksana'

    # 4. SEMAKAN KATA KUNCI GURU
    kata_kunci_guru = ['GURU', 'PENGETUA', 'GURU BESAR', 'PENOLONG KANAN', 'GKMP', 'GBK', 'GAB', 'GPM']
    if any(k in jawatan for k in kata_kunci_guru):
        return 'Guru'

    # 5. SEMAKAN INPUT CSV
    kumpulan_input = str(row.get('Kumpulan', '')).strip()
    if kumpulan_input.upper() in ['GURU', 'PPP']:
        return 'Guru'
    if kumpulan_input.upper() in ['AKP', 'ANGGOTA KUMPULAN PELAKSANA']:
        return 'Anggota Kumpulan Pelaksana'

    return 'Anggota Kumpulan Pelaksana'

def calculate_workload_df(df, jenis_sekolah="Sekolah Rendah"):
    """
    Kalkulator Beban Kerja Rasmi MySG KPM:
    SR: 1 Waktu = 30 Minit (0.50 Jam)
    SM: 1 Waktu = 40 Minit (0.6667 Jam)
    """
    if df is None or df.empty:
        return df

    df_out = df.copy()
    is_sm = "Menengah" in str(jenis_sekolah)
    kadar_pdp_jam = (40.0 / 60.0) if is_sm else (30.0 / 60.0)
    mapping_h = MYSG_PORTFOLIO_H_SM if is_sm else MYSG_PORTFOLIO_H_SR

    # 1. Kategori Staf
    df_out['Kumpulan'] = df_out.apply(determine_kategori_staf, axis=1)
    if 'Kategori_Staf' in df_out.columns:
        df_out.drop(columns=['Kategori_Staf'], inplace=True)

    # 2. Hitung Jam PdP secara dinamik
    pdp_cols = [c for c in df_out.columns if c.startswith('Waktu_')]
    if pdp_cols:
        for col in pdp_cols:
            df_out[col] = pd.to_numeric(df_out[col], errors='coerce').fillna(0)
        df_out['JUMLAH_WAKTU_PDP'] = df_out[pdp_cols].sum(axis=1)
        df_out['JUMLAH_JAM_PDP'] = df_out['JUMLAH_WAKTU_PDP'] * kadar_pdp_jam
    else:
        df_out['JUMLAH_WAKTU_PDP'] = 0
        df_out['JUMLAH_JAM_PDP'] = 0.0

    # 3. Hitung Jam Portfolio Hakiki H
    def get_jam_h(row):
        kod = str(row.get('Kod_H_1', '')).strip()
        if not kod:
            m = re.search(r'(HR|HM)(\d{2})', str(row.get('Jawatan', '')))
            if m:
                kod = f"{m.group(1)}{m.group(2)}"
        if kod in mapping_h:
            return mapping_h[kod][1]
        return 0.0

    df_out['JUMLAH_JAM_PORTFOLIO_H'] = df_out.apply(get_jam_h, axis=1)

    # 4. Hitung Jam Portfolio Tanpa Jawatan P (Dinamik & Sanitized)
    p_cols = [c for c in df_out.columns if c.startswith('Kod_P_')]
    def get_jam_p(row):
        total_p = 0.0
        for pc in p_cols:
            kod_raw = str(row.get(pc, '')).strip()
            kod_clean = kod_raw.split('|')[0].strip() if '|' in kod_raw else kod_raw
            
            if kod_clean in MYSG_PORTFOLIO_P:
                total_p += MYSG_PORTFOLIO_P[kod_clean][1]
            elif kod_raw.lower() not in ['', '-', 'nan', 'none', 'null']:
                total_p += 1.5
        return total_p

    df_out['JUMLAH_JAM_PORTFOLIO_P'] = df_out.apply(get_jam_p, axis=1) if p_cols else 0.0

    # 5. Hitung Jam Jawatankuasa J (Dinamik & Sanitized)
    j_cols = [c for c in df_out.columns if c.startswith('Kod_J_')]
    def get_jam_j(row):
        total_j = 0.0
        for jc in j_cols:
            kod_raw = str(row.get(jc, '')).strip()
            kod_clean = kod_raw.split('|')[0].strip() if '|' in kod_raw else kod_raw
            
            if kod_clean in MYSG_JAWATANKUASA_J:
                total_j += MYSG_JAWATANKUASA_J[kod_clean][1]
            elif kod_raw.lower() not in ['', '-', 'nan', 'none', 'null']:
                total_j += 1.0
        return total_j

    df_out['JUMLAH_JAM_JAWATANKUASA'] = df_out.apply(get_jam_j, axis=1) if j_cols else 0.0

    # 6. Jumlah Beban Keseluruhan
    df_out['JUMLAH_BEBAN_KESELURAHAN'] = (
        df_out['JUMLAH_JAM_PDP'] +
        df_out['JUMLAH_JAM_PORTFOLIO_H'] +
        df_out['JUMLAH_JAM_PORTFOLIO_P'] +
        df_out['JUMLAH_JAM_JAWATANKUASA']
    )

    # 7. Susunan Lajur Tepat
    cols = list(df_out.columns)
    if 'Kumpulan' in cols:
        cols.remove('Kumpulan')

    if 'No_KP' in cols:
        idx = cols.index('No_KP') + 1
        cols.insert(idx, 'Kumpulan')
    else:
        cols.insert(1, 'Kumpulan')

    return df_out[cols]

def calculate_summary_metrics(df):
    if df is None or df.empty:
        return {
            'total_staf': 0, 'total_guru': 0, 'total_akp': 0,
            'avg_beban_staf': 0.0, 'avg_pdp_guru': 0.0,
            'avg_port_guru': 0.0, 'avg_beban_guru': 0.0,
            'avg_port_akp': 0.0, 'avg_jawat_akp': 0.0, 'avg_beban_akp': 0.0
        }

    total_staf = len(df)
    kategori_col = 'Kumpulan' if 'Kumpulan' in df.columns else 'Kategori_Staf'
    
    df_guru = df[df[kategori_col] == 'Guru']
    df_akp = df[df[kategori_col] == 'Anggota Kumpulan Pelaksana']

    total_guru = len(df_guru)
    total_akp = len(df_akp)

    avg_beban_staf = df['JUMLAH_BEBAN_KESELURAHAN'].mean() if total_staf > 0 else 0.0

    avg_pdp_guru = df_guru['JUMLAH_JAM_PDP'].mean() if total_guru > 0 else 0.0
    avg_port_guru = (df_guru['JUMLAH_JAM_PORTFOLIO_H'] + df_guru['JUMLAH_JAM_PORTFOLIO_P']).mean() if total_guru > 0 else 0.0
    avg_beban_guru = df_guru['JUMLAH_BEBAN_KESELURAHAN'].mean() if total_guru > 0 else 0.0

    avg_port_akp = (df_akp['JUMLAH_JAM_PORTFOLIO_H'] + df_akp['JUMLAH_JAM_PORTFOLIO_P']).mean() if total_akp > 0 else 0.0
    avg_jawat_akp = df_akp['JUMLAH_JAM_JAWATANKUASA'].mean() if total_akp > 0 else 0.0
    avg_beban_akp = df_akp['JUMLAH_BEBAN_KESELURAHAN'].mean() if total_akp > 0 else 0.0

    return {
        'total_staf': total_staf,
        'total_guru': total_guru,
        'total_akp': total_akp,
        'avg_beban_staf': float(avg_beban_staf),
        'avg_pdp_guru': float(avg_pdp_guru),
        'avg_port_guru': float(avg_port_guru),
        'avg_beban_guru': float(avg_beban_guru),
        'avg_port_akp': float(avg_port_akp),
        'avg_jawat_akp': float(avg_jawat_akp),
        'avg_beban_akp': float(avg_beban_akp)
    }

def get_senarai_subjek(jenis_sekolah="Sekolah Rendah"):
    if "Menengah" in str(jenis_sekolah):
        return [
            "", "Bahasa Melayu", "Bahasa Inggeris", "Matematik", "Matematik Tambahan",
            "Sains", "Fizik", "Kimia", "Biologi", "Sejarah", "Pendidikan Islam",
            "Pendidikan Moral", "Geografi", "Reka Bentuk & Teknologi", "Perniagaan",
            "Prinsip Perakaunan", "Ekonomi", "Pendidikan Seni Visual", "PJK"
        ]
    return [
        "", "Bahasa Melayu", "Bahasa Inggeris", "Matematik", "Sains",
        "Pendidikan Islam", "Pendidikan Moral", "Sejarah", "Reka Bentuk & Teknologi",
        "Pendidikan Seni Visual", "Pendidikan Muzik", "PJK", "Bahasa Arab"
    ]
