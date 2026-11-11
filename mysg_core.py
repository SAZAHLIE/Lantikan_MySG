"""
========================================================================
SISTEM PENGURUSAN & PENGIRAAN BEBAN KERJA KAKITANGAN SEKOLAH (MYSG KPM)
MYSG CORE MODULE - PENYELESAIAN NONE DAN SEL KOSONG
========================================================================
"""

import pandas as pd
import numpy as np

SYSTEM_NAME = "MySG KPM: Sistem Pengurusan & Analisis Beban Kerja"
SYSTEM_VERSION = "1.0.0"
SYSTEM_RELEASE_DATE = "18 Oktober 2026"

# GRED RASMI KPM
GRED_RASMI_KPM = [
    "DG54", "DG52", "DG48", "DG44", "DG42", "DG41", "DG38", "DG34", "DG32", "DG29",
    "N36", "N32", "N29", "N22", "N19", "N11",
    "FA32", "FA29", "FT29", "FT19",
    "W29", "W19", "H19", "N1"
]

# JAWATAN RASMI KPM
JAWATAN_RASMI_KPM = [
    "PENGETUA", "GURU BESAR", "PENOLONG KANAN PENTADBIRAN", "PENOLONG KANAN HEM",
    "PENOLONG KANAN KOKURIKULUM", "PENOLONG KANAN PETANG", "PENOLONG KANAN TINGKATAN 6",
    "PENOLONG KANAN KHAS / PPKI", "GURU AKADEMIK", "GURU BIMBINGAN DAN KAUNSELING",
    "GURU MEDIA / PERPUSTAKAAN", "GURU DATA", "PEMBANTU TADBIR (P/O)",
    "PEMBANTU PENGURUSAN MURID", "JURUTEKNIK KOMPUTER", "PEMBANTU OPERASI"
]

# MAPPING PORTFOLIO HAKIKI (H) - SEKOLAH RENDAH
MYSG_PORTFOLIO_H_SR = {
    "HR01": ("Guru Akademik Biasa", 0.0),
    "HR02": ("Guru Pemulihan Khas", 0.0),
    "HR03": ("Guru Prasekolah", 0.0),
    "HR04": ("Guru Pendidikan Khas (PPKI)", 0.0),
    "HR05": ("Guru Bimbingan dan Kaunseling (GBK)", 0.0),
    "HR06": ("Guru Perpustakaan dan Media (GPM)", 0.0),
    "HR07": ("Guru Data", 0.0),
    "HR08": ("Penolong Kanan Pentadbiran", 0.0),
    "HR09": ("Penolong Kanan HEM", 0.0),
    "HR10": ("Penolong Kanan Kokurikulum", 0.0),
    "HR11": ("Penolong Kanan Petang", 0.0),
    "HR12": ("Penolong Kanan PPKI", 0.0),
    "HR13": ("Guru Besar", 0.0),
    "HR17": ("Pembantu Tadbir (P/O)", 40.0),
    "HR18": ("Pembantu Pengurusan Murid (PPM)", 40.0),
    "HR19": ("Juruteknik Komputer", 40.0),
    "HR20": ("Pembantu Operasi", 40.0),
    "HR24": ("Pembantu Tadbir (P/O) Lanjutan", 40.0)
}

# MAPPING PORTFOLIO HAKIKI (H) - SEKOLAH MENENGAH
MYSG_PORTFOLIO_H_SM = {
    "HM01": ("Guru Akademik Biasa", 0.0),
    "HM02": ("Guru Bimbingan dan Kaunseling (GBK)", 0.0),
    "HM03": ("Guru Perpustakaan dan Media (GPM)", 0.0),
    "HM04": ("Guru Data", 0.0),
    "HM05": ("Guru Tingkatan 6", 0.0),
    "HM06": ("Guru Pendidikan Khas (PPKI)", 0.0),
    "HM07": ("Penolong Kanan Pentadbiran", 0.0),
    "HM08": ("Penolong Kanan HEM", 0.0),
    "HM09": ("Penolong Kanan Kokurikulum", 0.0),
    "HM10": ("Penolong Kanan Petang", 0.0),
    "HM11": ("Penolong Kanan Tingkatan 6", 0.0),
    "HM12": ("Penolong Kanan PPKI", 0.0),
    "HM13": ("Pengetua", 0.0),
    "HM17": ("Pembantu Tadbir (P/O)", 40.0),
    "HM18": ("Pembantu Pengurusan Murid (PPM)", 40.0),
    "HM19": ("Juruteknik Komputer", 40.0),
    "HM20": ("Pembantu Operasi", 40.0)
}

# MAPPING PORTFOLIO P
MYSG_PORTFOLIO_P = {
    "P01": ("Guru Kelas", 2.0),
    "P02": ("Ketua Panitia Mata Pelajaran", 2.0),
    "P03": ("Setiausaha Peperiksaan / Pentaksiran", 3.0),
    "P04": ("Guru Sukan / Permainan", 2.0),
    "P05": ("Guru Penyelaras Kelab / Persatuan", 2.0),
    "P06": ("Guru Penyelaras Badan Beruniform", 2.0),
    "P07": ("Penyelaras Bilik-Bilik Khas", 1.5),
    "P08": ("Guru SPBT", 2.0),
    "P09": ("Guru Disiplin / Pengawas", 2.5),
    "P10": ("Guru 3K (Kebersihan, Kesihatan, Keselamatan)", 2.0)
}

# MAPPING JAWATANKUASA J
MYSG_JAWATANKUASA_J = {
    "J01": ("AJK Pengurusan & Pentadbiran Sekolah", 1.0),
    "J02": ("AJK Kurikulum Sekolah", 1.0),
    "J03": ("AJK Hal Ehwal Murid (HEM)", 1.0),
    "J04": ("AJK Kokurikulum Sekolah", 1.0),
    "J05": ("AJK Kewangan & Aset Sekolah", 1.0),
    "J06": ("AJK Pembangunan & Penyelenggaraan Fizikal", 1.0),
    "J07": ("AJK Bencana & Keselamatan Sekolah", 1.0),
    "J08": ("AJK PIBG / KSIB", 1.0)
}

def determine_kategori_staf(row):
    """
    Mengenal pasti sama ada staf ialah 'Guru' atau 'Anggota Kumpulan Pelaksana'
    """
    kumpulan_input = str(row.get('Kumpulan', '')).strip()
    if kumpulan_input in ['Guru', 'Anggota Kumpulan Pelaksana']:
        return kumpulan_input

    gred = str(row.get('Gred', '')).upper().strip()
    jawatan = str(row.get('Jawatan', '')).upper().strip()
    kod_h = str(row.get('Kod_H_1', '')).upper().strip()
    detail_h = str(row.get('Detail_H_1', '')).upper().strip()

    if any(gred.startswith(prefix) for prefix in ['DG', 'DC', 'UD']):
        return 'Guru'

    kata_kunci_guru = ['GURU', 'PENGETUA', 'GURU BESAR', 'PENOLONG KANAN', 'PK ', 'GDM', 'GAB', 'GBK', 'GPM']
    if any(k in jawatan or k in detail_h for k in kata_kunci_guru):
        return 'Guru'

    if (kod_h.startswith('HR') or kod_h.startswith('HM')):
        try:
            num_code = int(kod_h.replace('HR', '').replace('HM', '').strip())
            if num_code < 17:
                return 'Guru'
        except ValueError:
            pass

    return 'Anggota Kumpulan Pelaksana'

def is_empty_val(val):
    v = str(val).strip().lower()
    return v in ["", "nan", "none", "null", "-"]

def extract_code(val):
    if is_empty_val(val):
        return ""
    # Extract just the code part like PR01 or JR01 before the pipe |
    return str(val).split('|')[0].strip().upper()

def calculate_workload_df(df, jenis_sekolah="Sekolah Rendah"):
    if df is None or df.empty:
        return df

    df_out = df.copy()
    is_sm = "Menengah" in str(jenis_sekolah)
    kadar_pdp_jam = 40.0 / 60.0 if is_sm else 30.0 / 60.0
    mapping_h = MYSG_PORTFOLIO_H_SM if is_sm else MYSG_PORTFOLIO_H_SR

    # 1. Setkan lajur Kumpulan sahaja
    df_out['Kumpulan'] = df_out.apply(determine_kategori_staf, axis=1)

    # Padamkan lajur Kategori_Staf jika wujud dari fail lama
    if 'Kategori_Staf' in df_out.columns:
        df_out.drop(columns=['Kategori_Staf'], inplace=True)

    # 2. Hitung Jam PdP
    pdp_cols = [c for c in df_out.columns if c.startswith('Waktu_')]
    if pdp_cols:
        for col in pdp_cols:
            df_out[col] = pd.to_numeric(df_out[col], errors='coerce').fillna(0)
        df_out['JUMLAH_WAKTU_PDP'] = df_out[pdp_cols].sum(axis=1)
        df_out['JUMLAH_JAM_PDP'] = df_out['JUMLAH_WAKTU_PDP'] * kadar_pdp_jam
    else:
        df_out['JUMLAH_WAKTU_PDP'] = 0
        df_out['JUMLAH_JAM_PDP'] = 0.0

    # 3. Hitung Jam Portfolio H
    def get_jam_h(row):
        kod_raw = extract_code(row.get('Kod_H_1', ''))
        if kod_raw in mapping_h:
            return mapping_h[kod_raw][1]
        return 0.0

    df_out['JUMLAH_JAM_PORTFOLIO_H'] = df_out.apply(get_jam_h, axis=1)

    # 4. Hitung Jam Portfolio P
    p_cols = [c for c in df_out.columns if c.startswith('Kod_P_')]
    def get_jam_p(row):
        total_p = 0.0
        for pc in p_cols:
            kod_raw = str(row.get(pc, '')).strip()
            if is_empty_val(kod_raw):
                continue
            # Jika ia ada kod seperti PR01 dalam MYSG_PORTFOLIO_P
            # Convert PR01 -> P01 for dictionary matching
            mapped_kod = kod_raw.split('|')[0].strip().upper().replace('PR', 'P').replace('PM', 'P')
            if mapped_kod in MYSG_PORTFOLIO_P:
                total_p += MYSG_PORTFOLIO_P[mapped_kod][1]
            elif mapped_kod:
                # Fallback: if there is some valid non-empty text, give default 1.5 jam
                total_p += 1.5
        return total_p

    df_out['JUMLAH_JAM_PORTFOLIO_P'] = df_out.apply(get_jam_p, axis=1) if p_cols else 0.0

    # 5. Hitung Jam Jawatankuasa J
    j_cols = [c for c in df_out.columns if c.startswith('Kod_J_')]
    def get_jam_j(row):
        total_j = 0.0
        for jc in j_cols:
            kod_raw = str(row.get(jc, '')).strip()
            if is_empty_val(kod_raw):
                continue
            # If it's something like PR06 that leaked into Kod J, don't count it or give fallback
            mapped_kod = kod_raw.split('|')[0].strip().upper().replace('JR', 'J').replace('JM', 'J')
            if mapped_kod in MYSG_JAWATANKUASA_J:
                total_j += MYSG_JAWATANKUASA_J[mapped_kod][1]
            elif mapped_kod:
                # Only add if it's a valid non-empty string that isn't found
                total_j += 1.0
        return total_j

    df_out['JUMLAH_JAM_JAWATANKUASA'] = df_out.apply(get_jam_j, axis=1) if j_cols else 0.0

    # 6. Hitung Jumlah Beban Keseluruhan
    df_out['JUMLAH_BEBAN_KESELURAHAN'] = (
        df_out['JUMLAH_JAM_PDP'] +
        df_out['JUMLAH_JAM_PORTFOLIO_H'] +
        df_out['JUMLAH_JAM_PORTFOLIO_P'] +
        df_out['JUMLAH_JAM_JAWATANKUASA']
    )

    # 7. SUSUN LAJUR: SELIPKAN 'Kumpulan' TEPAT SELEPAS 'No_KP'
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
