"""
========================================================================
SISTEM PENGURUSAN & PENGIRAAN BEBAN KERJA KAKITANGAN SEKOLAH (MYSG KPM)
PAGE 3 - MODUL UTAMA (PENGURUSAN DATA, ANALISIS & PENJANAAN LAPORAN)
========================================================================
"""

import streamlit as st
import pandas as pd
import os
import json
from mysg_core import (
    calculate_workload_df, 
    calculate_summary_metrics, 
    get_senarai_subjek,
    SYSTEM_VERSION
)
from header_component import render_school_header
from footer_component import render_footer
from letter_generator import generate_appointment_letter_html
from category_report_generator import generate_category_report_html
from data_validator import validate_and_clean_csv
from pdf_generator import generate_appointment_letter_pdf

def get_target_storage_dir():
    """Mengembalikan laluan storan folder selamat"""
    path = st.session_state.get('dataset_storage_path', 'DEFAULT_DOWNLOADS')
    if path == "DEFAULT_DOWNLOADS" or not str(path).strip():
        return os.getcwd()
    return path

def render_page_3():
    render_school_header()

    info_sec = st.session_state.get('school_info', {})
    jenis_sekolah = info_sec.get('jenis_sekolah', 'Sekolah Rendah')

    # BUTANG NAVIGASI ATAS
    col_nav1, col_nav2 = st.columns([1, 4])
    with col_nav1:
        if st.button("⬅️ Kembali ke Profil", use_container_width=True):
            st.session_state.current_step = 2
            st.rerun()

    st.markdown("<hr style='margin: 10px 0 20px 0;'>", unsafe_allow_html=True)

    # TAB UTAMA SISTEM
    tab_labels = [
        "📊 Dashboard & Analisis", 
        "👥 Pengurusan Staf & Beban Kerja", 
        "📄 Laporan Ringkasan Berkategori", 
        "✉️ Penjana Surat Lantikan Tugas"
    ]
    
    if hasattr(st, "stabs"):
        tab1, tab2, tab3, tab4 = st.stabs(tab_labels)
    else:
        tab1, tab2, tab3, tab4 = st.tabs(tab_labels)

    # -------------------------------------------------------------------
    # TAB 1: DASHBOARD & MUAT NAIK DATA
    # -------------------------------------------------------------------
    with tab1:
        st.subheader("📁 Muat Naik / Kemaskini Data Staf")
        uploaded_file = st.file_uploader("Muat naik fail CSV Staf (Standard MySG KPM)", type=["csv"])

        if uploaded_file is not None:
            is_valid, result, warnings_list = validate_and_clean_csv(uploaded_file)
            
            if not is_valid:
                st.error(result, unsafe_allow_html=True)
            else:
                for warn in warnings_list:
                    st.warning(warn)
                    
                df_processed = calculate_workload_df(result, jenis_sekolah)
                st.session_state.staff_df = df_processed
                st.success(f"✅ Fail CSV berjaya dimuat naik, dibersihkan dan dihitung untuk {len(df_processed)} staf!")

        df = st.session_state.get('staff_df', None)

        if df is not None and not df.empty:
            metrics = calculate_summary_metrics(df)
            
            st.markdown("---")
            st.subheader("📈 Ringkasan Metrik Beban Kerja")
            
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            col_m1.metric("Jumlah Staf", metrics['total_staf'])
            col_m2.metric("Jumlah Guru", metrics['total_guru'])
            col_m3.metric("Jumlah AKP", metrics['total_akp'])
            col_m4.metric("Purata Beban Staf (Jam)", f"{metrics['avg_beban_staf']:.1f}")

            st.markdown("<br>", unsafe_allow_html=True)
            
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                st.markdown("#### 🎓 Purata Beban Kerja Guru")
                st.write(f"- **Purata Jam PdP:** {metrics['avg_pdp_guru']:.1f} jam")
                st.write(f"- **Purata Jam Portfolio:** {metrics['avg_port_guru']:.1f} jam")
                st.write(f"- **Jumlah Purata Guru:** **{metrics['avg_beban_guru']:.1f} jam**")

            with col_g2:
                st.markdown("#### 🏢 Purata Beban Kerja AKP")
                st.write(f"- **Purata Jam Portfolio:** {metrics['avg_port_akp']:.1f} jam")
                st.write(f"- **Purata Jam Jawatankuasa:** {metrics['avg_jawat_akp']:.1f} jam")
                st.write(f"- **Jumlah Purata AKP:** **{metrics['avg_beban_akp']:.1f} jam**")
        else:
            st.info("ℹ️ Sila muat naik fail CSV staf untuk memulakan analisis dan penjanaan laporan.")

    # -------------------------------------------------------------------
    # TAB 2: PENGURUSAN STAF & JADUAL
    # -------------------------------------------------------------------
    with tab2:
        df = st.session_state.get('staff_df', None)
        if df is not None and not df.empty:
            st.subheader("👥 Senarai Staf & Agihan Beban Kerja")
            
            search_query = st.text_input("🔍 Carian Nama Staf / No. KP / Jawatan:", "")
            if search_query:
                df_display = df[df.apply(lambda r: search_query.lower() in str(r).lower(), axis=1)]
            else:
                df_display = df

            st.dataframe(df_display, use_container_width=True)
            
            st.download_button(
                label="📥 Muat Turun Data Beban Kerja Terkini (CSV)",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name=f"Beban_Kerja_Staf_{info_sec.get('kod_sekolah', 'MySG')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠️ Tiada data staf dipaparkan. Sila muat naik fail data di Tab 1.")

    # -------------------------------------------------------------------
    # TAB 3: LAPORAN RINGKASAN BERKATEGORI
    # -------------------------------------------------------------------
    with tab3:
        df = st.session_state.get('staff_df', None)
        if df is not None and not df.empty:
            st.subheader("📄 Laporan Ringkasan Cetakan Berkategori")
            
            kat_pilihan = st.selectbox("Pilih Kategori Laporan:", ["Semua Staf", "Guru", "Anggota Kumpulan Pelaksana"])
            
            kategori_col = 'Kumpulan' if 'Kumpulan' in df.columns else 'Kategori_Staf'
            if kat_pilihan == "Guru":
                df_filtered = df[df[kategori_col] == 'Guru']
            elif kat_pilihan == "Anggota Kumpulan Pelaksana":
                df_filtered = df[df[kategori_col] == 'Anggota Kumpulan Pelaksana']
            else:
                df_filtered = df

            report_html = generate_category_report_html(df_filtered, kat_pilihan, info_sec)
            st.components.v1.html(report_html, height=600, scrolling=True)
        else:
            st.warning("⚠️ Tiada data untuk menjana laporan.")

    # -------------------------------------------------------------------
    # TAB 4: PENJANA SURAT LANTIKAN TUGAS (DENGAN NATIVE PDF)
    # -------------------------------------------------------------------
    with tab4:
        df = st.session_state.get('staff_df', None)
        if df is not None and not df.empty:
            st.subheader("✉️ Penjana Surat Lantikan Tugas Rasmi")
            
            senarai_nama = df['Nama'].tolist() if 'Nama' in df.columns else []
            selected_staf_name = st.selectbox("Pilih Staf untuk Surat Lantikan:", senarai_nama)

            if selected_staf_name:
                staf_row = df[df['Nama'] == selected_staf_name].iloc[0]
                no_ruj = st.text_input("No. Rujukan Surat (Opsional):", f"KP/{info_sec.get('kod_sekolah', 'SEK')}/MYSG/2026/01")
                
                # Pratonton HTML di Skrin
                letter_html = generate_appointment_letter_html(staf_row, info_sec, no_rujukan=no_ruj)
                st.components.v1.html(letter_html, height=550, scrolling=True)
                
                # Muat Turun PDF A4 Tulin
                pdf_bytes = generate_appointment_letter_pdf(staf_row, info_sec, no_rujukan=no_ruj)
                st.download_button(
                    label="📄 Muat Turun Surat Lantikan Rasmi (PDF A4)",
                    data=pdf_bytes,
                    file_name=f"Surat_Lantikan_{selected_staf_name.replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True
                )
        else:
            st.warning("⚠️ Tiada data staf untuk menjana surat lantikan.")

    render_footer()