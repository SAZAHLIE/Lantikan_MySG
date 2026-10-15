"""
========================================================================
MODUL ENJIN PENGIRAAN BEBAN KERJA MYSG KPM (15 SUBJEK, 15P, 15J)
------------------------------------------------------------------------
Menyokong format rasmi (Subjek_i, Waktu_i, Kod_P_i, Detail_P_i, Kod_J_i, Detail_J_i)
serta format generik (JAM_i, P1..15, J1..15).
========================================================================
"""

import pandas as pd

def calculate_workload_df(df):
    """
    Mengira jumlah jam PdP, Waktu Portfolio (P), dan Jawatankuasa (J)
    mengikut garis panduan MySG KPM.
    """
    df = df.copy()

    # 1. Kenal pasti lajur Subjek / Jam / Waktu PdP
    pdp_cols = [col for col in df.columns if any(kw in col.upper() for kw in ['WAKTU', 'JAM', 'MINIT', 'PDP'])]
    
    # 2. Pengiraan Jam PdP
    if pdp_cols:
        df['JUMLAH_JAM_PDP'] = df[pdp_cols].apply(pd.to_numeric, errors='coerce').fillna(0).sum(axis=1)
    else:
        df['JUMLAH_JAM_PDP'] = 0

    # 3. Pengiraan Bilangan Portfolio (Kod P)
    p_cols = [col for col in df.columns if col.upper().startswith('KOD_P') or (col.upper().startswith('P') and col[1:].isdigit())]
    if p_cols:
        df['JUMLAH_JAM_PORTFOLIO'] = df[p_cols].notna().sum(axis=1) * 1.5
    else:
        df['JUMLAH_JAM_PORTFOLIO'] = 0

    # 4. Pengiraan Bilangan Jawatankuasa (Kod J)
    j_cols = [col for col in df.columns if col.upper().startswith('KOD_J') or (col.upper().startswith('J') and col[1:].isdigit())]
    if j_cols:
        df['JUMLAH_JAM_JAWATANKUASA'] = df[j_cols].notna().sum(axis=1) * 1.0
    else:
        df['JUMLAH_JAM_JAWATANKUASA'] = 0

    # 5. Jumlah Beban Keseluruhan
    df['JUMLAH_BEBAN_KESELURAHAN'] = (
        df['JUMLAH_JAM_PDP'] + 
        df['JUMLAH_JAM_PORTFOLIO'] + 
        df['JUMLAH_JAM_JAWATANKUASA']
    )

    return df