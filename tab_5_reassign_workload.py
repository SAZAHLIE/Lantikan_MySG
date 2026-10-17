"""
========================================================================
MYSG KPM: SISTEM PENGURUSAN & ANALISIS BEBAN KERJA
MODULE: TAB 5 - PENETAPAN SEMULA AGIHAN TUGAS (PDP, KOD P & KOD J)
========================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import time
import datetime
from mysg_core import (
    calculate_workload_df, 
    MYSG_PORTFOLIO_H_SR, 
    MYSG_PORTFOLIO_H_SM,
    MYSG_PORTFOLIO_P,
    MYSG_JAWATANKUASA_J
)

# SENARAI SUBJEK RASMI KPM MENGIKUT PERINGKAT
SUBJEK_KPM_SR = [
    "", "Bahasa Melayu", "Bahasa Inggeris", "Matematik", "Sains",
    "Pendidikan Islam", "Pend. Agama Islam", "Pendidikan Moral", 
    "Bahasa Arab", "Bahasa Cina", "Bahasa Tamil",
    "Pend. Jasmani Pend. Kesihatan", "Pendidikan Jasmani", "Pendidikan Kesihatan",
    "Pend. Seni Visual", "Pendidikan Seni Visual", "Pend. Muzik", "Pendidikan Muzik",
    "Sejarah", "Reka Bentuk Teknologi", "Reka Bentuk & Teknologi (RBT)",
    "TASMIK", "Al-Quran", "PRA Sekolah", "Lain-Lain Subjek"
]

SUBJEK_KPM_SM = [
    "", "Bahasa Melayu", "Bahasa Inggeris", "Matematik", "Matematik Tambahan",
    "Sains", "Fizik", "Kimia", "Biologi",
    "Pendidikan Islam", "Pendidikan Moral", "Sejarah", "Geografi",
    "Reka Bentuk & Teknologi (RBT)", "Asas Sains Komputer (ASK)", "Sains Komputer",
    "Prinsip Perakaunan", "Ekonomi", "Perniagaan",
    "Pend. Jasmani Pend. Kesihatan", "Pendidikan Seni Visual", "Pendidikan Muzik",
    "Bahasa Arab", "Bahasa Cina", "Bahasa Tamil",
    "Tasawwur Islam", "Pend. Al-Quran & Al-Sunnah", "Pend. Syariah Islamiah",
    "Lain-Lain Subjek"
]

def to_clean_str(val):
    if val is None or pd.isna(val):
        return ""
    s = str(val).strip()
    return "" if s.lower() in ["nan", "none", "null", "none | none"] else s

def to_clean_int(val):
    if val is None or pd.isna(val):
        return 0
    try:
        return int(float(val))
    except Exception:
        return 0

def render_tab_5(school_info):
    """Menjana kandungan Tab 5: Penyelarasan Agihan Tugas Kakitangan."""
    st.subheader("⚙️ Penetapan Semula Agihan Tugas & Transisi Sesi Baharu")
    st.caption("Kemaskini dan selaraskan agihan Subjek PdP, Portfolio Tanpa Jawatan (P), dan Jawatankuasa Sekolah (J) bagi kakitangan sedia ada. PIN Pengesahan diperlukan.")

    raw_df = st.session_state.get('staff_df', pd.DataFrame())
    data_ver = st.session_state.get('data_version', 1)
    jenis_sek = school_info.get('jenis_sekolah', 'Sekolah Rendah')
    is_sm = "Menengah" in str(jenis_sek)

    list_subjek_kpm = SUBJEK_KPM_SM if is_sm else SUBJEK_KPM_SR

    if raw_df is None or raw_df.empty or 'Nama' not in raw_df.columns:
        st.warning("⚠️ Tiada data kakitangan ditemui. Sila muat naik CSV di Tab 1 terlebih dahulu.")
        return

    # PASTIKAN LAJUR TEKS BERJENIS 'OBJECT' UNTUK MENGELAKKAN LOSS-SETITEM ERROR PADA CSV ASAL
    df_staff = raw_df.copy()
    for col in df_staff.columns:
        if str(col).startswith(('Subjek_', 'Kelas_', 'Kod_P_', 'Detail_P_', 'Kod_J_', 'Detail_J_')):
            df_staff[col] = df_staff[col].astype(object)

    selected_staf_name = st.selectbox(
        "Pilih Kakitangan untuk Kemaskini Tugas:",
        options=df_staff['Nama'].tolist(),
        key=f"select_reassign_staf_{data_ver}"
    )

    staf_row = df_staff[df_staff['Nama'] == selected_staf_name].iloc[0]
    staf_index = df_staff[df_staff['Nama'] == selected_staf_name].index[0]

    # RINGKASAN PROFIL & BEBAN KERJA SEMASA
    col_info, col_metrics = st.columns(2)

    with col_info:
        st.markdown("##### 👤 Maklumat Pegawai:")
        st.write(f"• **Nama:** {staf_row.get('Nama', '-')}")
        st.write(f"• **Jawatan Hakiki:** {staf_row.get('Jawatan', '-')}")
        st.write(f"• **Kumpulan:** {staf_row.get('Kumpulan', 'Guru')}")
        st.write(f"• **Gred:** {staf_row.get('Gred', '-')}")

    with col_metrics:
        st.markdown("##### 📊 Beban Kerja Semasa:")
        waktu_pdp = float(staf_row.get('JUMLAH_WAKTU_PDP', 0.0) or 0.0)
        jam_pdp = float(staf_row.get('JUMLAH_JAM_PDP', 0.0) or 0.0)
        jam_h = float(staf_row.get('JUMLAH_JAM_PORTFOLIO_H', 0.0) or 0.0)
        jam_p = float(staf_row.get('JUMLAH_JAM_PORTFOLIO_P', 0.0) or 0.0)
        jam_j = float(staf_row.get('JUMLAH_JAM_JAWATANKUASA', 0.0) or 0.0)
        total_jam = float(staf_row.get('JUMLAH_BEBAN_KESELURAHAN', jam_pdp + jam_h + jam_p + jam_j) or 0.0)

        st.write(f"• **Waktu PdP:** {int(waktu_pdp)} waktu ({jam_pdp:.1f} jam)")
        st.write(f"• **Jam Portfolio Hakiki (H):** {jam_h:.1f} jam")
        st.write(f"• **Jam Portfolio (P):** {jam_p:.1f} jam")
        st.write(f"• **Jam Jawatankuasa (J):** {jam_j:.1f} jam")
        status_tag = "🟢 SEIMBANG" if 35 <= total_jam <= 50 else ("🔴 TINGGI" if total_jam > 50 else "🟡 OPTIMUM")
        st.write(f"• **Jumlah Beban Keseluruhan:** **{total_jam:.1f} JAM** ({status_tag})")

    st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
    st.markdown("##### 📝 Kemaskini Perincian Agihan Tugas Baharu")

    if 're_pdp_batch' not in st.session_state:
        st.session_state['re_pdp_batch'] = 5
    if 're_p_batch' not in st.session_state:
        st.session_state['re_p_batch'] = 5
    if 're_j_batch' not in st.session_state:
        st.session_state['re_j_batch'] = 5

    with st.form(key=f"form_reassign_{staf_index}_{data_ver}", clear_on_submit=False):

        # A. PDP
        pdp_re_inputs = {}
        if staf_row.get('Kumpulan') == "Guru":
            max_pdp = st.session_state['re_pdp_batch']
            with st.expander(f"📖 A. Pengajaran & Pembelajaran (PdP) — (Paparan 1 hingga {max_pdp})", expanded=True):
                st.caption("Kemaskini Subjek, Kelas, dan Bilangan Waktu (Nombor Bulat sahaja).")
                for i in range(1, max_pdp + 1):
                    c1, c2, c3 = st.columns([2, 1.5, 1])
                    existing_subj = to_clean_str(staf_row.get(f'Subjek_{i}'))
                    existing_kelas = to_clean_str(staf_row.get(f'Kelas_{i}'))
                    existing_waktu = to_clean_int(staf_row.get(f'Waktu_{i}'))

                    idx_subj = list_subjek_kpm.index(existing_subj) if existing_subj in list_subjek_kpm else 0

                    with c1:
                        pdp_re_inputs[f'Subjek_{i}'] = st.selectbox(f"Subjek {i}:", options=list_subjek_kpm, index=idx_subj, key=f"re_subj_{staf_index}_{i}")
                    with c2:
                        pdp_re_inputs[f'Kelas_{i}'] = st.text_input(f"Kelas {i}:", value=existing_kelas, key=f"re_kelas_{staf_index}_{i}")
                    with c3:
                        pdp_re_inputs[f'Waktu_{i}'] = st.number_input(f"Waktu {i}:", min_value=0, step=1, value=existing_waktu, key=f"re_waktu_{staf_index}_{i}")

        # B. KOD P
        p_re_inputs = {}
        max_p = st.session_state['re_p_batch']
        opts_p = [""] + [f"{k} | {v[0]}" for k, v in MYSG_PORTFOLIO_P.items()]

        with st.expander(f"💼 B. Portfolio Tanpa Jawatan (Kod P) — (Paparan 1 hingga {max_p})", expanded=True):
            st.caption("Pilih Kod P dan perincian tugas.")
            for i in range(1, max_p + 1):
                cp1, cp2 = st.columns([2, 2])
                raw_kp = to_clean_str(staf_row.get(f'Kod_P_{i}'))
                raw_dp = to_clean_str(staf_row.get(f'Detail_P_{i}'))

                idx_p = 0
                if raw_kp:
                    kod_only = raw_kp.split('|')[0].strip()
                    for opt_idx, opt_val in enumerate(opts_p):
                        if opt_val.startswith(kod_only):
                            idx_p = opt_idx
                            break

                with cp1:
                    p_re_inputs[f'Kod_P_{i}'] = st.selectbox(f"Kod P_{i}:", options=opts_p, index=idx_p, key=f"re_kod_p_{staf_index}_{i}")
                with cp2:
                    p_re_inputs[f'Detail_P_{i}'] = st.text_input(f"Butiran Detail P_{i}:", value=raw_dp, key=f"re_det_p_{staf_index}_{i}")

        # C. KOD J
        j_re_inputs = {}
        max_j = st.session_state['re_j_batch']
        opts_j = [""] + [f"{k} | {v[0]}" for k, v in MYSG_JAWATANKUASA_J.items()]

        with st.expander(f"🏛️ C. Jawatankuasa Sekolah (Kod J) — (Paparan 1 hingga {max_j})", expanded=True):
            st.caption("Pilih Kod J dan perincian jawatankuasa.")
            for i in range(1, max_j + 1):
                cj1, cj2 = st.columns([2, 2])
                raw_kj = to_clean_str(staf_row.get(f'Kod_J_{i}'))
                raw_dj = to_clean_str(staf_row.get(f'Detail_J_{i}'))

                idx_j = 0
                if raw_kj:
                    kod_j_only = raw_kj.split('|')[0].strip()
                    for opt_idx, opt_val in enumerate(opts_j):
                        if opt_val.startswith(kod_j_only):
                            idx_j = opt_idx
                            break

                with cj1:
                    j_re_inputs[f'Kod_J_{i}'] = st.selectbox(f"Kod J_{i}:", options=opts_j, index=idx_j, key=f"re_kod_j_{staf_index}_{i}")
                with cj2:
                    j_re_inputs[f'Detail_J_{i}'] = st.text_input(f"Butiran Detail J_{i}:", value=raw_dj, key=f"re_det_j_{staf_index}_{i}")

        st.markdown("<br>", unsafe_allow_html=True)
        
        # KAWALAN AKSES (RBAC) - PIN PENGESAHAN
        pin_pengesahan_3 = st.text_input("🔑 Masukkan PIN Pengesahan Pentadbir untuk menyimpan perubahan:", type="password", key="pin_kemaskini_staf")
        btn_save_reassign = st.form_submit_button("💾 Simpan & Kemaskini Penyelarasan Tugas Kakitangan", type="primary", use_container_width=True)

        if btn_save_reassign:
            if pin_pengesahan_3 != "1234":
                st.error("🔒 PIN Pengesahan salah! Akses ditolak. Hanya pentadbir yang sah dibenarkan merombak tugas.")
            else:
                # PENUKARAN KEPADA SENARAI DIKSIONARI UNTUK ELAK MENGGANTI LANGSUNG SEL FLOAT64 DATAFRAME
                df_dict_list = df_staff.to_dict(orient='records')
                target_dict = df_dict_list[staf_index]

                total_waktu_calc = 0
                if staf_row.get('Kumpulan') == "Guru":
                    for i in range(1, 16):
                        if i <= max_pdp:
                            s_val = to_clean_str(pdp_re_inputs.get(f'Subjek_{i}'))
                            k_val = to_clean_str(pdp_re_inputs.get(f'Kelas_{i}'))
                            w_val = to_clean_int(pdp_re_inputs.get(f'Waktu_{i}'))
                        else:
                            s_val = to_clean_str(target_dict.get(f'Subjek_{i}'))
                            k_val = to_clean_str(target_dict.get(f'Kelas_{i}'))
                            w_val = to_clean_int(target_dict.get(f'Waktu_{i}'))

                        target_dict[f'Subjek_{i}'] = s_val if s_val else None
                        target_dict[f'Kelas_{i}'] = k_val if k_val else None
                        target_dict[f'Waktu_{i}'] = float(w_val) if (s_val and w_val > 0) else None
                        if s_val and w_val > 0:
                            total_waktu_calc += w_val

                target_dict['JUMLAH_WAKTU_PDP'] = float(total_waktu_calc)

                for i in range(1, 16):
                    if i <= max_p:
                        kp_val = to_clean_str(p_re_inputs.get(f'Kod_P_{i}'))
                        dp_val = to_clean_str(p_re_inputs.get(f'Detail_P_{i}'))
                    else:
                        kp_val = to_clean_str(target_dict.get(f'Kod_P_{i}'))
                        dp_val = to_clean_str(target_dict.get(f'Detail_P_{i}'))

                    target_dict[f'Kod_P_{i}'] = kp_val if kp_val else None
                    target_dict[f'Detail_P_{i}'] = dp_val if dp_val else None

                for i in range(1, 16):
                    if i <= max_j:
                        kj_val = to_clean_str(j_re_inputs.get(f'Kod_J_{i}'))
                        dj_val = to_clean_str(j_re_inputs.get(f'Detail_J_{i}'))
                    else:
                        kj_val = to_clean_str(target_dict.get(f'Kod_J_{i}'))
                        dj_val = to_clean_str(target_dict.get(f'Detail_J_{i}'))

                    target_dict[f'Kod_J_{i}'] = kj_val if kj_val else None
                    target_dict[f'Detail_J_{i}'] = dj_val if dj_val else None

                try:
                    # BINA DATAFRAME BARU DARIPADA REKOD DIKSIONARI
                    df_updated_new = pd.DataFrame(df_dict_list)
                    df_recalculated = calculate_workload_df(df_updated_new, jenis_sek)
                    st.session_state['staff_df'] = df_recalculated
                    st.session_state['data_version'] = int(time.time())
                    
                    # REKOD LOG AKTIVITI
                    if 'audit_log' not in st.session_state:
                        st.session_state['audit_log'] = []
                    st.session_state['audit_log'].append({
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "action": "KEMASKINI TUGAS",
                        "staff_name": selected_staf_name
                    })

                    st.toast(f"💾 Agihan tugas {selected_staf_name} berjaya dikemaskini!", icon="✅")
                    st.success(f"✅ Agihan tugas bagi **{selected_staf_name}** telah berjaya dikemaskini dan diselaraskan!")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.toast("❌ Ralat dikemaskini tugas!", icon="🚨")
                    st.error(f"❌ Ralat semasa mengemaskini agihan tugas: {str(e)}")

    # BUTANG TAMBAH RUANG DINAMIK
    st.markdown("##### ➕ Tambah Ruang Input Tambahan Penyelarasan (Jika Perlu)")
    col_rb1, col_rb2, col_rb3 = st.columns(3)

    with col_rb1:
        if st.session_state['re_pdp_batch'] < 15:
            next_pdp = st.session_state['re_pdp_batch'] + 5
            if st.button(f"➕ Buka Ruang PdP ({next_pdp-4} - {next_pdp})", use_container_width=True, key="btn_re_add_pdp"):
                st.session_state['re_pdp_batch'] = next_pdp
                st.toast(f"📖 Ruang PdP ({next_pdp-4} - {next_pdp}) dibuka!", icon="🔓")
                st.rerun()

    with col_rb2:
        if st.session_state['re_p_batch'] < 15:
            next_p = st.session_state['re_p_batch'] + 5
            if st.button(f"➕ Buka Ruang Kod P ({next_p-4} - {next_p})", use_container_width=True, key="btn_re_add_p"):
                st.session_state['re_p_batch'] = next_p
                st.toast(f"💼 Ruang Kod P ({next_p-4} - {next_p}) dibuka!", icon="🔓")
                st.rerun()

    with col_rb3:
        if st.session_state['re_j_batch'] < 15:
            next_j = st.session_state['re_j_batch'] + 5
            if st.button(f"➕ Buka Ruang Kod J ({next_j-4} - {next_j})", use_container_width=True, key="btn_re_add_j"):
                st.session_state['re_j_batch'] = next_j
                st.toast(f"🏛️ Ruang Kod J ({next_j-4} - {next_j}) dibuka!", icon="🔓")
                st.rerun()