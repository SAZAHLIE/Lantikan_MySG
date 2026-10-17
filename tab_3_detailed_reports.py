"""
========================================================================
MYSG KPM: SISTEM PENGURUSAN & ANALISIS BEBAN KERJA
MODULE: TAB 3 - LAPORAN PERINCIAN BEBAN TUGAS DENGAN BANDINGAN KUMPULAN
========================================================================
"""

import streamlit as st
import pandas as pd
import importlib
import print_engine

# Paksa re-load layout print engine terkini untuk memastikan tiada cache lama
importlib.reload(print_engine)

from print_engine import generate_detailed_comparison_html, generate_individual_detailed_report_html

def render_tab_3(school_info):
    """Menjana kandungan Tab 3: Laporan Perincian & Bandingan Kumpulan Kakitangan."""
    st.subheader("📋 Laporan Perincian Beban Tugas dengan Bandingan Kumpulan")
    st.caption("Perbandingan metrik purata beban tugas antara Kumpulan Guru (PPP) dengan Kumpulan AKP berserta jadual perincian penuh.")

    df_latest = st.session_state.get('staff_df', pd.DataFrame())
    data_ver = st.session_state.get('data_version', 1)

    if df_latest is not None and not df_latest.empty:
        df_display = df_latest.copy()
        df_display['Waktu_PdP'] = df_display.get('JUMLAH_WAKTU_PDP', 0)
        df_display['Jam_PdP'] = df_display.get('JUMLAH_JAM_PDP', 0.0).round(1)

        jam_h = df_display.get('JUMLAH_JAM_PORTFOLIO_H', 0.0)
        jam_p = df_display.get('JUMLAH_JAM_PORTFOLIO_P', 0.0)
        df_display['Jam_Portfolio'] = (jam_h + jam_p).round(1)
        df_display['Jam_Jawatankuasa'] = df_display.get('JUMLAH_JAM_JAWATANKUASA', 0.0).round(1)

        df_display['Jumlah_Jam_Beban'] = df_display.get('JUMLAH_BEBAN_KESELURAHAN', 
            df_display['Jam_PdP'] + df_display['Jam_Portfolio'] + df_display['Jam_Jawatankuasa']
        ).round(1)

        df_display['Status_Agihan'] = df_display['Jumlah_Jam_Beban'].apply(
            lambda x: "🟢 SEIMBANG" if 35 <= x <= 50 else ("🔴 TINGGI" if x > 50 else "🟡 OPTIMUM")
        )

        # 1. BINA JADUAL BANDINGAN PURATA KUMPULAN
        df_guru = df_display[df_display['Kumpulan'] == 'Guru']
        df_akp = df_display[df_display['Kumpulan'] == 'Anggota Kumpulan Pelaksana']

        pdp_guru = round(df_guru['Jam_PdP'].mean(), 1) if not df_guru.empty else 0.0
        port_guru = round(df_guru['Jam_Portfolio'].mean(), 1) if not df_guru.empty else 0.0
        jk_guru = round(df_guru['Jam_Jawatankuasa'].mean(), 1) if not df_guru.empty else 0.0
        beban_guru = round(df_guru['Jumlah_Jam_Beban'].mean(), 1) if not df_guru.empty else 0.0

        pdp_akp = round(df_akp['Jam_PdP'].mean(), 1) if not df_akp.empty else 0.0
        port_akp = round(df_akp['Jam_Portfolio'].mean(), 1) if not df_akp.empty else 0.0
        jk_akp = round(df_akp['Jam_Jawatankuasa'].mean(), 1) if not df_akp.empty else 0.0
        beban_akp = round(df_akp['Jumlah_Jam_Beban'].mean(), 1) if not df_akp.empty else 0.0

        summary_comp_data = [
            {
                "Kumpulan Kakitangan": "🎓 Kumpulan Guru (PPP)",
                "Jumlah Anggota": len(df_guru),
                "Purata Jam PdP": pdp_guru,
                "Purata Jam Portfolio (H+P)": port_guru,
                "Purata Jam Jawatankuasa (J)": jk_guru,
                "Jumlah Purata Beban (Jam)": beban_guru
            },
            {
                "Kumpulan Kakitangan": "🏢 Anggota Kumpulan Pelaksana (AKP)",
                "Jumlah Anggota": len(df_akp),
                "Purata Jam PdP": pdp_akp,
                "Purata Jam Portfolio (H+P)": port_akp,
                "Purata Jam Jawatankuasa (J)": jk_akp,
                "Jumlah Purata Beban (Jam)": beban_akp
            }
        ]
        df_summary_comp = pd.DataFrame(summary_comp_data)

        # BAHAGIAN 1: RINGKASAN PERBANDINGAN KUMPULAN
        col_t3_title, col_t3_print = st.columns([2.5, 1.5])
        with col_t3_title:
            st.markdown("#### 1. Ringkasan Perbandingan Purata Beban Kerja Kumpulan")
        with col_t3_print:
            html_detail_comp = generate_detailed_comparison_html(df_display, "LAPORAN PERINCIAN BANDINGAN BEBAN TUGAS", school_info, st.session_state)
            st.download_button(
                label="🖨️ Cetak Laporan Bandingan Kumpulan",
                data=html_detail_comp,
                file_name="Laporan_Perincian_Bandingan_Beban_Tugas.html",
                mime="text/html",
                type="primary",
                use_container_width=True,
                key=f"btn_print_detail_comp_{data_ver}"
            )

        st.dataframe(df_summary_comp, use_container_width=True, key=f"tbl_tab3_comp_{data_ver}")

        st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)

        # BAHAGIAN 2: CARIAN & ANALISIS INDIVIDU
        st.markdown("#### 2. Carian & Analisis Perincian Beban Kerja Individu")
        col_search, col_ind_btn = st.columns([2.5, 1.5])

        with col_search:
            selected_staf_ind = st.selectbox(
                "Pilih Kakitangan untuk Memanggil Data Perincian:",
                options=df_display['Nama'].tolist(),
                key="select_ind_report_staf"
            )

        staf_ind_row = df_display[df_display['Nama'] == selected_staf_ind].iloc[0]
        kump_staf = staf_ind_row.get('Kumpulan', 'Guru')
        beban_ind = round(staf_ind_row.get('Jumlah_Jam_Beban', 0.0), 1)

        purata_kump = beban_guru if kump_staf == 'Guru' else beban_akp
        diff_jam = round(beban_ind - purata_kump, 1)

        with col_ind_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            
            # MEMANGGIL LAPORAN INDIVIDU A4 PORTRAIT BAHARU
            html_ind = generate_individual_detailed_report_html(
                staf_ind_row, 
                school_info, 
                df_display
            )
            
            clean_ind_name = str(selected_staf_ind).replace(" ", "_").replace("/", "_")
            
            # KEMASKINI PENAMAAN BUTANG: "Cetak Laporan Bandaingan Individu"
            st.download_button(
                label="🖨️ Cetak Laporan Bandaingan Individu",
                data=html_ind,
                file_name=f"Laporan_Individu_{clean_ind_name}.html",
                mime="text/html",
                type="primary",
                use_container_width=True,
                key=f"btn_print_bandaingan_indiv_{clean_ind_name}_{data_ver}"
            )

        # Paparan Kad Bandingan Individu vs Kumpulan
        m_c1, m_c2, m_c3, m_c4 = st.columns(4)
        m_c1.metric("Pegawai Dipilih", selected_staf_ind.split()[0])
        m_c2.metric("Jumlah Beban Individu", f"{beban_ind} Jam")
        m_c3.metric(f"Purata Kumpulan ({kump_staf})", f"{purata_kump} Jam")
        m_c4.metric("Perbezaan vs Purata", f"{'+' if diff_jam>=0 else ''}{diff_jam} Jam", delta_color="normal" if abs(diff_jam)<=5 else "inverse")

        st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
        st.markdown(f"#### 3. Perincian Individu Agihan Beban Tugas Kakitangan ({len(df_display)} Rekod)")

        cols_detailed_show = ['Nama', 'Kumpulan', 'Jawatan', 'Waktu_PdP', 'Jam_PdP', 'Jam_Portfolio', 'Jam_Jawatankuasa', 'Jumlah_Jam_Beban', 'Status_Agihan']
        st.dataframe(df_display[[c for c in cols_detailed_show if c in df_display.columns]], use_container_width=True, key=f"tbl_tab3_detailed_{data_ver}")

    else:
        st.warning("⚠️ Tiada data kakitangan ditemui. Sila muat naik CSV di Tab 1 atau buka Vault Terenkripsi di Halaman Utama.")