"""
========================================================================
MYSG KPM: SISTEM PENGURUSAN & ANALISIS BEBAN KERJA
MODULE: TAB 7 - CARTA ORGANISASI SEKOLAH (AUTO-JANA)
========================================================================
"""

import streamlit as st
import pandas as pd

def render_tab_7(school_info):
    """Menjana paparan Carta Organisasi Automatik berasaskan kod Jawatan dan Portfolio."""
    st.subheader("🏢 Carta Organisasi Sekolah (Janaan Automatik MySG)")
    st.caption("Carta ini dijana secara automatik berdasarkan Jawatan Hakiki (Kod H) dan Portfolio Tanpa Jawatan (Kod P) yang telah ditetapkan dalam sistem.")

    df_staff = st.session_state.get('staff_df', pd.DataFrame())
    
    if df_staff is None or df_staff.empty:
        st.warning("⚠️ Tiada data kakitangan ditemui. Sila muat naik CSV di Tab 1 terlebih dahulu.")
        return

    # Pembersihan Data: Pastikan tiada nilai NA untuk proses saringan
    df_clean = df_staff.copy()
    for col in df_clean.columns:
        if df_clean[col].dtype == object:
            df_clean[col] = df_clean[col].fillna("")

    # --- 1. MENGENAL PASTI PUNCAK PIMPINAN (PGB) ---
    # Mencari PGB: Kod H bermula dengan 'HR01' atau 'HM01'
    pgb_df = df_clean[df_clean['Kod_H_1'].astype(str).str.startswith(('HR01', 'HM01'))]
    
    # --- 2. MENGENAL PASTI BARISAN GURU PENOLONG KANAN (GPK) ---
    # Mencari GPK: Kod H bermula dari 'HR02' hingga 'HR06' atau 'HM02' hingga 'HM11'
    gpk_codes = tuple([f"HR0{i}" for i in range(2, 7)] + [f"HM{i:02d}" for i in range(2, 12)])
    gpk_df = df_clean[df_clean['Kod_H_1'].astype(str).str.startswith(gpk_codes)]

    # --- 3. MENGENAL PASTI KETUA PANITIA / GURU KANAN MATA PELAJARAN ---
    # Mengesan melalui Kod P untuk Ketua Panitia (PR02 atau PM02) dan GKMP (HM12)
    kp_gkmp_list = []
    for idx, row in df_clean.iterrows():
        is_kp_gkmp = False
        jawatan_semasa = ""
        
        # Periksa Kod H (Untuk SM - GKMP)
        if str(row.get('Kod_H_1')).startswith('HM12'):
            is_kp_gkmp = True
            jawatan_semasa = str(row.get('Jawatan', 'Guru Kanan Mata Pelajaran'))
            
        # Periksa semua Kod P (Untuk Ketua Panitia)
        for i in range(1, 16):
            if str(row.get(f'Kod_P_{i}')).startswith(('PR02', 'PM02')):
                is_kp_gkmp = True
                jawatan_semasa = f"Ketua Panitia {str(row.get(f'Detail_P_{i}', ''))}"
                break
                
        if is_kp_gkmp:
            kp_gkmp_list.append({
                'Nama': row['Nama'],
                'Jawatan': jawatan_semasa,
                'Kumpulan': row['Kumpulan']
            })
    df_kp_gkmp = pd.DataFrame(kp_gkmp_list)

    # --- 4. MENGENAL PASTI KUMPULAN GURU AKADEMIK (GAB) ---
    # Semua guru selain PGB, GPK, dan KP/GKMP
    gab_df = df_clean[
        (df_clean['Kumpulan'] == 'Guru') & 
        (~df_clean['Kod_H_1'].astype(str).str.startswith(('HR01', 'HM01') + gpk_codes)) &
        (~df_clean['Nama'].isin(df_kp_gkmp['Nama'] if not df_kp_gkmp.empty else []))
    ]

    # --- 5. MENGENAL PASTI ANGGOTA KUMPULAN PELAKSANA (AKP) ---
    akp_df = df_clean[df_clean['Kumpulan'] == 'Anggota Kumpulan Pelaksana']


    # ================= PAPARAN CARTA =================
    
    # KOTAK PGB
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<h4 style='text-align: center; color: #1e3a8a; margin-bottom: 5px;'>PENGURUSAN TERTINGGI SEKOLAH</h4>", unsafe_allow_html=True)
        if not pgb_df.empty:
            pgb_row = pgb_df.iloc[0]
            st.markdown(f"<div style='text-align: center; background-color: #f1f5f9; padding: 10px; border-radius: 8px; border: 2px solid #3b82f6;'><b>{pgb_row['Nama']}</b><br><span style='color: #475569;'>{pgb_row['Jawatan']}</span></div>", unsafe_allow_html=True)
        else:
            st.info("📌 Rekod Pengetua / Guru Besar (Kod HR01 / HM01) belum ditetapkan.")

    # KOTAK GPK
    st.markdown("<div style='text-align: center; font-size: 24px; color: #cbd5e1;'>⬇</div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<h5 style='text-align: center; color: #0284c7; margin-bottom: 15px;'>BARISAN GURU PENOLONG KANAN (GPK)</h5>", unsafe_allow_html=True)
        if not gpk_df.empty:
            # Paparan grid yang responsif
            gpk_cols = st.columns(len(gpk_df)) if len(gpk_df) <= 4 else st.columns(4)
            for i, (_, row) in enumerate(gpk_df.iterrows()):
                col_idx = i % 4
                with gpk_cols[col_idx]:
                    st.markdown(f"<div style='text-align: center; background-color: #f8fafc; padding: 10px; border-radius: 8px; border: 1px solid #bae6fd; font-size: 14px;'><b>{row['Nama']}</b><br><span style='font-size: 12px; color: #64748b;'>{row['Jawatan']}</span></div>", unsafe_allow_html=True)
        else:
            st.info("📌 Tiada rekod Guru Penolong Kanan (Kod HR02-HR06 / HM02-HM11) ditemui.")

    # KOTAK KETUA PANITIA / GURU KANAN
    st.markdown("<div style='text-align: center; font-size: 24px; color: #cbd5e1;'>⬇</div>", unsafe_allow_html=True)
    with st.expander("📂 KETUA PANITIA / GURU KANAN MATA PELAJARAN", expanded=True):
        if not df_kp_gkmp.empty:
            for _, row in df_kp_gkmp.iterrows():
                st.markdown(f"• **{row['Nama']}** — <span style='color: #64748b;'>{row['Jawatan']}</span>", unsafe_allow_html=True)
        else:
            st.info("📌 Tiada rekod Ketua Panitia (Kod PR02/PM02) atau Guru Kanan (HM12) ditemui.")

    # KOTAK GURU AKADEMIK & AKP
    col_gab, col_akp = st.columns(2)
    with col_gab:
        with st.expander(f"🎓 GURU AKADEMIK BIASA ({len(gab_df)} Orang)", expanded=False):
            if not gab_df.empty:
                for _, row in gab_df.iterrows():
                    st.write(f"• {row['Nama']}")
            else:
                st.write("Tiada rekod.")
                
    with col_akp:
        with st.expander(f"🏢 ANGGOTA KUMPULAN PELAKSANA ({len(akp_df)} Orang)", expanded=False):
            if not akp_df.empty:
                for _, row in akp_df.iterrows():
                    st.write(f"• {row['Nama']}")
            else:
                st.write("Tiada rekod.")
