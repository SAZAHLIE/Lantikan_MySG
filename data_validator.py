"""
========================================================================
SISTEM PENGURUSAN & PENGIRAAN BEBAN KERJA KAKITANGAN SEKOLAH (MYSG KPM)
MODULE: DATA VALIDATOR & SANITIZER (FASA 1)
========================================================================
"""

import pandas as pd
import re
import io

# MAPPING NAMA LAJUR STANDARD MYSG KPM
COLUMN_MAPPING = {
    'NAMA': 'Nama',
    'NAMA STAF': 'Nama',
    'NAMA GURU': 'Nama',
    'NO KP': 'No_KP',
    'NO. KP': 'No_KP',
    'NO_KTP': 'No_KP',
    'NOKP': 'No_KP',
    'GRED': 'Gred',
    'GRED JAWATAN': 'Gred',
    'JAWATAN': 'Jawatan',
    'GELARAN JAWATAN': 'Jawatan',
    'KUMPULAN': 'Kumpulan',
    'KATEGORI': 'Kumpulan',
    'KOD H': 'Kod_H_1',
    'KOD_H': 'Kod_H_1',
    'DETAIL H': 'Detail_H_1',
    'DETAIL_H': 'Detail_H_1'
}

def validate_and_clean_csv(uploaded_file):
    """
    Membaca, memvalidasi, dan membersihkan fail CSV yang dimuat naik pengguna.
    Mengembalikan: (is_success, dataframe_or_error_msg, warning_list)
    """
    warnings = []
    
    # 1. BACA FAIL DENGAN ENKOD BERBEZA (PREVENT UNICODE DECODE ERROR)
    try:
        if hasattr(uploaded_file, 'getvalue'):
            bytes_data = uploaded_file.getvalue()
        elif hasattr(uploaded_file, 'read'):
            bytes_data = uploaded_file.read()
        else:
            bytes_data = uploaded_file
    except Exception as e:
        return False, f"❌ Ralat semasa membaca fail: {str(e)}", []

    df = None
    encodings_to_try = ['utf-8-sig', 'utf-8', 'cp1252', 'latin-1', 'iso-8859-1']
    
    for enc in encodings_to_try:
        try:
            df = pd.read_csv(io.BytesIO(bytes_data), encoding=enc, dtype=str)
            break
        except Exception:
            continue
            
    if df is None:
        return False, "❌ Fail CSV tidak dapat dibaca. Sila pastikan fail tersimpan dalam format CSV (Comma Delimited) yang sah.", []

    if df.empty:
        return False, "⚠️ Fail CSV yang dimuat naik adalah kosong.", []

    # 2. SANITIZE & NORMALIKAN NAMA LAJUR (HEADER)
    new_columns = {}
    for col in df.columns:
        clean_col = str(col).strip().upper()
        if clean_col in COLUMN_MAPPING:
            new_columns[col] = COLUMN_MAPPING[clean_col]
        else:
            formatted_col = re.sub(r'[\s\.\-]+', '_', str(col).strip())
            new_columns[col] = formatted_col

    df.rename(columns=new_columns, inplace=True)

    # 3. SEMAK LAJUR MANDATORI
    mandatory_cols = ['Nama', 'Gred', 'Jawatan']
    missing_cols = [c for c in mandatory_cols if c not in df.columns]
    
    if missing_cols:
        return False, f"❌ Fail CSV kekurangan lajur mandatori berikut: <b>{', '.join(missing_cols)}</b>. Sila semak templat rasmi MySG KPM.", []

    # 4. PEMBERSIHAN DATA ROW-LEVEL
    # A. Bersihkan Nama Staf
    df['Nama'] = df['Nama'].fillna('-').astype(str).str.strip().str.upper()
    
    # B. Bersihkan No_KP
    if 'No_KP' in df.columns:
        df['No_KP'] = df['No_KP'].fillna('-').astype(str).apply(lambda x: re.sub(r'[^0-9\-]', '', x))
    else:
        df['No_KP'] = '-'
        warnings.append("⚠️ Lajur 'No_KP' tidak ditemui. Nilai lalai '-' telah digunakan.")

    # C. Bersihkan Lajur Waktu PdP (Tukar teks '12 waktu' -> 12)
    waktu_cols = [c for c in df.columns if c.startswith('Waktu_')]
    for w_col in waktu_cols:
        def clean_waktu_val(val):
            if pd.isna(val) or val is None:
                return 0
            nums = re.findall(r'\d+', str(val))
            if nums:
                return int(nums[0])
            return 0
            
        df[w_col] = df[w_col].apply(clean_waktu_val)

    # D. Padamkan baris yang benar-benar kosong
    df.dropna(how='all', inplace=True)

    if len(df) == 0:
        return False, "❌ Tiada rekod staf yang sah dijumpai di dalam fail CSV.", []

    return True, df, warnings