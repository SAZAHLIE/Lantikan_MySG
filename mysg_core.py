"""
========================================================================
SISTEM PENGURUSAN & PENGIRAAN BEBAN KERJA KAKITANGAN SEKOLAH (MYSG KPM)
MYSG CORE MODULE - PENGIRAAN TAPAK ASAS (BASE) + PDP + PEMBERATAN P/J
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
    "HR01": ("Guru Besar (PGB)", 37.5),
    "HR02": ("Guru Penolong Kanan Pentadbiran", 34.0),
    "HR03": ("Guru Penolong Kanan Hal Ehwal Murid", 34.0),
    "HR04": ("Guru Penolong Kanan Kokurikulum", 34.0),
    "HR05": ("Guru Penolong Kanan Petang", 34.0),
    "HR06": ("Guru Penolong Kanan Pendidikan Khas", 34.0),
    "HR07": ("Penyelaras Aktiviti Menengah (Model Khas K9)", 34.0),
    "HR08": ("Guru Penyelaras Bestari", 28.0),
    "HR09": ("Guru Perpustakaan dan Media (GPM)", 28.0),
    "HR10": ("Guru Data", 28.0),
    "HR11": ("Guru Prasekolah", 10.0),
    "HR12": ("Guru Akademik KSSR", 10.0),
    "HR13": ("Guru Akademik KSSM (K9)", 10.0),
    "HR14": ("Guru Amali (K9)", 10.0),
    "HR15": ("Guru Bahasa Cina", 10.0),
    "HR16": ("Guru Bahasa Tamil", 10.0),
    "HR17": ("Guru Pendidikan Islam", 10.0),
    "HR18": ("Guru Pemulihan / Pemulihan Khas", 10.0),
    "HR19": ("Guru Program Integrasi / Pendidikan Khas (PPKI)", 10.0),
    "HR20": ("Guru Kod Braille", 10.0),
    "HR21": ("Guru Kod Tangan", 10.0),
    "HR22": ("Guru Bimbingan (GBK)", 38.0), 
    "HR23": ("Guru Kaunseling (K9)", 38.0),
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
    "HR35": ("Pembantu Awam (K9)", 40.0),
    "HR36": ("Pembantu Makmal (K9)", 40.0),
    "HR37": ("Pembantu Kemahiran (SKPK)", 40.0)
}

# MAPPING PORTFOLIO HAKIKI (H) - SEKOLAH MENENGAH
MYSG_PORTFOLIO_H_SM = {
    "HM01": ("Pengetua (PGB)", 37.5),
    "HM02": ("Guru Penolong Kanan Pentadbiran", 34.0),
    "HM03": ("Guru Penolong Kanan Hal Ehwal Murid", 34.0),
    "HM04": ("Guru Penolong Kanan Kokurikulum", 34.0),
    "HM05": ("Guru Penolong Kanan Petang", 34.0),
    "HM06": ("Guru Penolong Kanan Pendidikan Khas", 34.0),
    "HM07": ("GPK Sukan (SSM)", 34.0),
    "HM08": ("GPK Seni (SSeM)", 34.0),
    "HM09": ("GPK Rendah (Model Khas)", 34.0),
    "HM10": ("GPK Tingkatan 6", 34.0),
    "HM11": ("GPK Prauniversiti (SSM)", 34.0),
    "HM12": ("Guru Kanan Mata Pelajaran (GKMP)", 30.0),
    "HM13": ("Ketua Bidang Sukan (SSM)", 30.0),
    "HM14": ("Ketua Bidang Seni (SSeM)", 30.0),
    "HM15": ("Guru Penyelaras Bestari", 28.0),
    "HM16": ("Guru Perpustakaan dan Media (GPM)", 28.0),
    "HM17": ("Guru Data", 28.0),
    "HM18": ("Guru Tingkatan 6 Akademik", 10.0),
    "HM19": ("Guru Tingkatan 6 Amali", 10.0),
    "HM20": ("Guru Tingkatan 6 Kokurikulum", 10.0),
    "HM21": ("Guru Prauniversiti Akademik (SSM)", 10.0),
    "HM22": ("Guru Prauniversiti Amali (SSM)", 10.0),
    "HM23": ("Guru Prauniversiti Kokurikulum (SSM)", 10.0),
    "HM24": ("Guru Akademik KSSM", 10.0),
    "HM25": ("Guru Akademik KSSR (Model Khas/SSM)", 10.0),
    "HM26": ("Guru MP Am (SMT)", 10.0),
    "HM27": ("Guru KBT (SABKM/TMUA)", 10.0),
    "HM28": ("Guru KBD (SABKM)", 10.0),
    "HM29": ("Guru Pendidikan Islam SR (Model Khas)", 10.0),
    "HM30": ("Guru Pendidikan Islam (SBP/SSM/SSeM)", 10.0),
    "HM31": ("Guru Dini", 10.0),
    "HM32": ("Guru Tahfiz", 10.0),
    "HM33": ("Guru al-Quran (KKQ)", 10.0),
    "HM34": ("Guru Bahasa Antarabangsa", 10.0),
    "HM35": ("Guru Bahasa Inggeris (SBP/SSM/SSeM)", 10.0),
    "HM36": ("Guru Muzik (SBP)", 10.0),
    "HM37": ("Guru Psikologi Sukan (SSM)", 10.0),
    "HM38": ("Guru Unit Sains Sukan (SSM)", 10.0),
    "HM39": ("Guru Program Integrasi / Pendidikan Khas (PPKI)", 10.0),
    "HM40": ("Guru Kod Braille", 10.0),
    "HM41": ("Guru Kod Tangan", 10.0),
    "HM42": ("Guru Amali Bengkel (Ting. 1-3)", 10.0),
    "HM43": ("Guru Amali (Ting. 4-5)", 10.0),
    "HM44": ("Guru MP Teknikal (SMT)", 10.0),
    "HM45": ("Guru MP Vokasional ICT", 10.0),
    "HM46": ("Guru MP Vokasional Rekacipta", 10.0),
    "HM47": ("Guru MP Vokasional (MPV)", 10.0),
    "HM48": ("Jurulatih Sukan Terbuka (SSM)", 10.0),
    "HM49": ("Jurulatih Sukan Tertutup (SSM)", 10.0),
    "HM50": ("Jurulatih Sukan (SSN)", 10.0),
    "HM51": ("Jurulatih Seni Terbuka (SSeM)", 10.0),
    "HM52": ("Guru Kaunseling / Guru Bimbingan", 38.0),
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

# MAPPING PORTFOLIO P DENGAN PEMBERAT ANALITIKAL
MYSG_PORTFOLIO_P = {
    "P01": ("Guru Kelas", 4.5),
    "P02": ("Guru Bertugas Harian", 3.0),
    "P03": ("Penyelaras PPKI Lantikan Dalaman", 5.0),
    "P04": ("Setiausaha Latihan dalam Perkhidmatan", 2.5),
    "P05": ("Penyelaras Tahun/Tingkatan", 2.5),
    "P06": ("Setiausaha Jawatankuasa", 1.5),
    "P07": ("Guru Bimbingan Lantikan Dalaman", 4.0),
    "P08": ("Ketua Panitia", 4.0),
    "P09": ("Setiausaha Peperiksaan Dalaman", 5.0),
    "P10": ("Setiausaha Peperiksaan Awam", 7.0),
    "P11": ("Penyelaras ICT Lantikan Dalaman", 3.5),
    "P12": ("Penyelaras Pusat Sumber Sekolah Lantikan Dalaman", 3.5),
    "P13": ("Guru Resos Masalah Penglihatan", 3.5),
    "P14": ("Ketua Guru Disiplin", 6.0),
    "P15": ("Penyelaras Skim Pinjaman Buku Teks", 4.0),
    "P16": ("Warden Asrama", 12.0),
    "P17": ("Setiausaha Sukan", 5.0),
    "P18": ("Penyelaras Unit-Unit Kokurikulum", 2.5),
    "P19": ("Guru Penasihat Unit-Unit Kokurikulum", 2.5),
    "P30": ("Penyelaras Unit-Unit Lain", 2.5)
}

# MAPPING JAWATANKUASA J DENGAN PEMBERAT ANALITIKAL
MYSG_JAWATANKUASA_J = {
    "J01": ("JK Pengurusan Sekolah", 2.0),
    "J02": ("JK Pengurusan Maklumat Sekolah", 1.5),
    "J03": ("JK Pengurusan Sumber Manusia", 1.5),
    "J04": ("JK Pengurusan Kewangan, Akaun dan Aset Sekolah", 2.0),
    "J05": ("JK Standard Kualiti Pendidikan Malaysia", 1.5),
    "J06": ("JK Pendidikan Khas Sekolah", 1.5),
    "J07": ("JK Pengurusan Prasekolah", 1.5),
    "J08": ("JK Pengurusan Bencana Sekolah", 1.0),
    "J09": ("JK Persatuan Ibu Bapa dan Guru (PIBG)", 1.5),
    "J10": ("JK Kelab Kebajikan Guru dan Kakitangan", 1.5),
    "J11": ("JK Pengurusan Murid Orang Asli", 1.5),
    "J12": ("JK Pengurusan Kurikulum", 2.0),
    "J13": ("JK Panitia Mata Pelajaran", 2.0),
    "J14": ("JK Pentaksiran", 2.0),
    "J15": ("JK Pengurusan Sumber dan Teknologi Pendidikan", 1.5),
    "J16": ("JK Pengurusan Hal Ehwal Murid (HEM)", 2.0),
    "J17": ("JK Pengurusan Disiplin Murid", 2.0),
    "J18": ("JK Pengurusan 3K (Kebersihan, Kesihatan dan Keselamatan)", 1.5),
    "J19": ("JK Bimbingan dan Kaunseling", 1.5),
    "J20": ("JK Pengurusan Asrama", 2.0),
    "J21": ("JK Pengurusan Kokurikulum", 2.0),
    "J22": ("JK Pembangunan Sukan Sekolah", 1.5),
    "J23": ("JK Sukan Tahunan Sekolah", 1.0)
}

# ========================================================================
# PEMETAAN AUTO-BINDING KOD P KEPADA KOD J (MENGELAKKAN DOUBLE-COUNTING)
# Berdasarkan format kod generik P dan J yang dikendalikan oleh enjin 
# ========================================================================
MYSG_P_TO_J_AUTO_MAP = {
    "P01": ["J16", "J19"],          # Guru Kelas -> JK HEM, JK B&K
    "P08": ["J04", "J08", "J15"],   # Ketua Panitia -> JK Kewangan, JK Bencana, JK PSS/Sumber
    "P18": ["J21", "J22"],          # Penyelaras Kokurikulum -> JK Koko, JK Sukan
    "P19": ["J21", "J22"]           # Penasihat Kokurikulum -> JK Koko, JK Sukan
}

def inject_auto_jawatankuasa(p_codes_list, current_j_codes_list):
    """
    Menyemak senarai Kod P semasa dan memasukkan Kod J yang berkaitan secara automatik
    jika ia belum wujud dalam senarai Kod J guru tersebut. Digunakan di borang UI.
    """
    updated_j_codes = list(current_j_codes_list)
    for p_code in p_codes_list:
        clean_p = p_code.replace('PR', 'P').replace('PM', 'P')
        if clean_p in MYSG_P_TO_J_AUTO_MAP:
            tied_j_codes = MYSG_P_TO_J_AUTO_MAP[clean_p]
            for j_code in tied_j_codes:
                if j_code not in updated_j_codes:
                    updated_j_codes.append(j_code)
                    
    updated_j_codes = [j for j in updated_j_codes if j]
    return updated_j_codes[:15]

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
            if num_code < 24:
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
    return str(val).split('|')[0].strip().upper()

def calculate_workload_df(df, jenis_sekolah="Sekolah Rendah"):
    if df is None or df.empty:
        return df

    df_out = df.copy()
    is_sm = "Menengah" in str(jenis_sekolah)
    kadar_pdp_jam = 40.0 / 60.0 if is_sm else 30.0 / 60.0
    mapping_h = MYSG_PORTFOLIO_H_SM if is_sm else MYSG_PORTFOLIO_H_SR

    # 1. Setkan lajur Kumpulan
    df_out['Kumpulan'] = df_out.apply(determine_kategori_staf, axis=1)

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

    # 3. Hitung Jam Portfolio H (Menggunakan Tapak Asas)
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
            mapped_kod = extract_code(kod_raw).replace('PR', 'P').replace('PM', 'P')
            if mapped_kod in MYSG_PORTFOLIO_P:
                total_p += MYSG_PORTFOLIO_P[mapped_kod][1]
            elif mapped_kod:
                total_p += 1.5
        return total_p

    df_out['JUMLAH_JAM_PORTFOLIO_P'] = df_out.apply(get_jam_p, axis=1) if p_cols else 0.0

    # 5. Hitung Jam Jawatankuasa J (Dengan Logik Anti-Double-Count)
    j_cols = [c for c in df_out.columns if c.startswith('Kod_J_')]
    def get_jam_j(row):
        total_j = 0.0
        
        # Dapatkan senarai Kod P generik semasa
        current_p_codes = []
        for pc in p_cols:
            p_raw = str(row.get(pc, '')).strip()
            if not is_empty_val(p_raw):
                mapped_p = extract_code(p_raw).replace('PR', 'P').replace('PM', 'P')
                current_p_codes.append(mapped_p)
                
        # Dapatkan senarai Kod J generik yang 'diserap' oleh Pakej Kod P
        absorbed_j_codes = []
        for p_code in current_p_codes:
            if p_code in MYSG_P_TO_J_AUTO_MAP:
                absorbed_j_codes.extend(MYSG_P_TO_J_AUTO_MAP[p_code])

        for jc in j_cols:
            kod_raw = str(row.get(jc, '')).strip()
            if is_empty_val(kod_raw):
                continue
            
            mapped_kod = extract_code(kod_raw).replace('JR', 'J').replace('JM', 'J')
            
            # LOGIK PENTING: Sifarkan jam jika Kod J diserap dalam pakej Kod P
            if mapped_kod in absorbed_j_codes:
                continue
                
            if mapped_kod in MYSG_JAWATANKUASA_J:
                total_j += MYSG_JAWATANKUASA_J[mapped_kod][1]
            elif mapped_kod:
                total_j += 1.0
        return total_j

    df_out['JUMLAH_JAM_JAWATANKUASA'] = df_out.apply(get_jam_j, axis=1) if j_cols else 0.0

    # 6. Hitung Jumlah Beban Keseluruhan (Gabungan PdP + Tapak Asas + P + J)
    df_out['JUMLAH_BEBAN_KESELURAHAN'] = (
        df_out['JUMLAH_JAM_PDP'] +
        df_out['JUMLAH_JAM_PORTFOLIO_H'] +
        df_out['JUMLAH_JAM_PORTFOLIO_P'] +
        df_out['JUMLAH_JAM_JAWATANKUASA']
    )

    # 7. Susun Semula
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
