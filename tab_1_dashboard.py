"""
========================================================================
MYSG KPM: SISTEM PENGURUSAN & ANALISIS BEBAN KERJA
MODULE: TAB 1 - DASHBOARD METRIK & UPLOAD CSV
========================================================================
"""

import streamlit as st
import pandas as pd
import time
from mysg_core import calculate_workload_df

def render_tab_1(school_info):
    """Menjana kandungan Tab 1: Dashboard Metrik & Muat Naik CSV Kakitangan."""
    df_staff = st.session_state.get('staff_df', pd.DataFrame())

    st.markdown("### 📈 Ringkasan Metrik Beban Kerja")

    if df_staff is not None and not df_staff.empty:
        total_staf = len(df_staff)
        df_guru = df_staff[df_staff['Kumpulan'] == 'Guru'] if 'Kumpulan' in df_staff.columns else df_staff
        df_akp = df_staff[df_staff['Kumpulan'] == 'Anggota Kumpulan Pelaksana'] if 'Kumpulan' in df_staff.columns else pd.DataFrame()

        total_guru = len(df_guru)
        total_akp = len(df_akp)

        # Pengiraan Purata Guru Selamat
        pdp_guru = df_guru['JUMLAH_JAM_PDP'].mean() if 'JUMLAH_JAM_PDP' in df_guru.columns and not df_guru.empty else 0.0
        port_h_guru = df_guru['JUMLAH_JAM_PORTFOLIO_H'] if 'JUMLAH_JAM_PORTFOLIO_H' in df_guru.columns else 0.0
        port_p_guru = df_guru['JUMLAH_JAM_PORTFOLIO_P'] if 'JUMLAH_JAM_PORTFOLIO_P' in df_guru.columns else 0.0
        port_guru = (port_h_guru + port_p_guru).mean() if not df_guru.empty else 0.0

        purata_pdp_guru = round(float(pdp_guru or 0.0), 1)
        purata_port_guru = round(float(port_guru or 0.0), 1)
        jumlah_purata_guru = round(purata_pdp_guru + purata_port_guru, 1)

        # Pengiraan Purata AKP Selamat
        port_h_akp = df_akp['JUMLAH_JAM_PORTFOLIO_H'] if 'JUMLAH_JAM_PORTFOLIO_H' in df_akp.columns else 0.0
        port_p_akp = df_akp['JUMLAH_JAM_PORTFOLIO_P'] if 'JUMLAH_JAM_PORTFOLIO_P' in df_akp.columns else 0.0
        port_akp = (port_h_akp + port_p_akp).mean() if not df_akp.empty else 0.0
        
        jk_akp = df_akp['JUMLAH_JAM_JAWATANKUASA'].mean() if 'JUMLAH_JAM_JAWATANKUASA' in df_akp.columns and not df_akp.empty else 0.0

        purata_port_akp = round(float(port_akp or 0.0), 1)
        purata_jk_akp = round(float(jk_akp or 0.0), 1)
        jumlah_purata_akp = round(purata_port_akp + purata_jk_akp, 1)

        purata_keseluruhan = round((jumlah_purata_guru * total_guru + jumlah_purata_akp * total_akp) / (total_staf if total_staf > 0 else 1), 1)

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("Jumlah Kakitangan", total_staf)
        col_m2.metric("Jumlah Guru", total_guru)
        col_m3.metric("Jumlah AKP", total_akp)
        col_m4.metric("Purata Beban Kakitangan (Jam)", purata_keseluruhan)

        st.markdown("<br>", unsafe_allow_html=True)
        col_p1, col_p2 = st.columns(2)

        with col_p1:
            st.markdown("#### 🎓 Purata Beban Kerja Guru")
            st.markdown(f"""
            * **Purata Jam PdP:** {purata_pdp_guru} jam
            * **Purata Jam Portfolio:** {purata_port_guru} jam
            * **Jumlah Purata Guru:** **{jumlah_purata_guru} jam**
            """)

        with col_p2:
            st.markdown("#### 🏢 Purata Beban Kerja AKP")
            st.markdown(f"""
            * **Purata Jam Portfolio:** {purata_port_akp} jam
            * **Purata Jam Jawatankuasa:** {purata_jk_akp} jam
            * **Jumlah Purata AKP:** **{jumlah_purata_akp} jam**
            """)

    else:
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("Jumlah Kakitangan", 0)
        col_m2.metric("Jumlah Guru", 0)
        col_m3.metric("Jumlah AKP", 0)
        col_m4.metric("Purata Beban Kakitangan (Jam)", 0)
        st.info("ℹ️ Sila muat naik fail CSV Kakitangan di bawah untuk memaparkan metrik beban kerja.")

    st.markdown("<hr style='margin: 30px 0 20px 0;'>", unsafe_allow_html=True)
    st.markdown("### 📂 Muat Naik / Kemaskini Data Kakitangan")
    
    uploaded_file = st.file_uploader("Upload CSV", type=['csv'], label_visibility="collapsed", key="tab1_csv_uploader_live")
    if uploaded_file is not None:
        csv_sig = f"{uploaded_file.name}_{uploaded_file.size}"
        if st.session_state.get('current_csv_sig') != csv_sig:
            try:
                # BACA DENGAN MEMAKSA DTYPE TEKS KEPADA STR BAGI MENGELAKKAN RALAT TYPE ERROR
                df_raw = pd.read_csv(uploaded_file, dtype=str)
                
                # Tukar lajur nombor semula kepada float/numeric
                num_prefixes = ('Waktu_', 'JUMLAH_WAKTU_PDP', 'JUMLAH_JAM_PDP', 'JUMLAH_JAM_PORTFOLIO_H', 'JUMLAH_JAM_PORTFOLIO_P', 'JUMLAH_JAM_JAWATANKUASA', 'JUMLAH_BEBAN_KESELURAHAN')
                for col in df_raw.columns:
                    if col.startswith(num_prefixes):
                        df_raw[col] = pd.to_numeric(df_raw[col], errors='coerce')

                jenis_sek = school_info.get('jenis_sekolah', 'Sekolah Rendah')
                df_processed = calculate_workload_df(df_raw, jenis_sek)
                
                st.session_state['staff_df'] = df_processed
                st.session_state['current_csv_sig'] = csv_sig
                st.session_state['data_version'] = int(time.time())
                
                st.toast(f"✅ {len(df_processed)} rekod kakitangan berjaya dikemas kini!", icon="✅")
                st.success(f"✅ {len(df_processed)} rekod kakitangan berjaya dikemas kini!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"❌ Ralat memproses fail CSV: {str(e)}")