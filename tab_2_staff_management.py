"""
========================================================================
MYSG KPM: SISTEM PENGURUSAN & ANALISIS BEBAN KERJA
MODULE: TAB 2 - JADUAL AGIHAN & PEMBERATAN TUGAS
========================================================================
"""

import streamlit as st
import pandas as pd
from print_engine import generate_printable_html

def render_tab_2(school_info):
    """Menjana kandungan Tab 2: Pengurusan Kakitangan & Jadual Agihan & Pemberatan Tugas."""
    st.subheader("👥 Jadual Agihan & Pemberatan Tugas")
    st.caption("Paparan analisis beban kerja mengikut kategori perkhidmatan kakitangan.")

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

        # SUB-TABS
        sub_tab1, sub_tab2, sub_tab3 = st.tabs([
            "🌐 Paparan Keseluruhan Kakitangan", 
            "🎓 Paparan Kumpulan Guru", 
            "🏢 Paparan Kumpulan AKP"
        ])

        cols_show = ['Nama', 'Jawatan', 'Waktu_PdP', 'Jam_PdP', 'Jam_Portfolio', 'Jam_Jawatankuasa', 'Jumlah_Jam_Beban', 'Status_Agihan']

        # SUB-TAB 1: KESELURAHAN
        with sub_tab1:
            col_h1, col_b1 = st.columns([3, 1])
            with col_h1:
                st.markdown("##### 📊 Senarai Beban Kerja Keseluruhan Warga Sekolah")
            with col_b1:
                html_all = generate_printable_html(df_display, "LAPORAN BEBAN KERJA KESELURUHAN WARGA SEKOLAH", school_info, st.session_state)
                st.download_button(
                    label="🖨️ Cetak Laporan Penuh (PDF/A4)",
                    data=html_all,
                    file_name="Laporan_Beban_Kerja_Keseluruhan.html",
                    mime="text/html",
                    type="primary",
                    key=f"btn_print_all_{data_ver}"
                )
            st.dataframe(df_display[[c for c in cols_show if c in df_display.columns]], use_container_width=True, key=f"tbl_all_v_{data_ver}")

        # SUB-TAB 2: GURU
        with sub_tab2:
            df_guru = df_display[df_display['Kumpulan'] == 'Guru']
            col_h2, col_b2 = st.columns([3, 1])
            with col_h2:
                st.markdown("##### 🎓 Analisis Beban Kerja Kumpulan Guru (PPP)")
            with col_b2:
                html_guru = generate_printable_html(df_guru, "ANALISIS BEBAN KERJA KUMPULAN GURU (PPP)", school_info, st.session_state)
                st.download_button(
                    label="🖨️ Cetak Laporan Guru (PDF/A4)",
                    data=html_guru,
                    file_name="Laporan_Beban_Kerja_Guru.html",
                    mime="text/html",
                    type="primary",
                    key=f"btn_print_guru_{data_ver}"
                )
            st.dataframe(df_guru[[c for c in cols_show if c in df_guru.columns]], use_container_width=True, key=f"tbl_guru_v_{data_ver}")

        # SUB-TAB 3: AKP
        with sub_tab3:
            df_akp = df_display[df_display['Kumpulan'] == 'Anggota Kumpulan Pelaksana']
            cols_akp = ['Nama', 'Jawatan', 'Jam_Portfolio', 'Jam_Jawatankuasa', 'Jumlah_Jam_Beban', 'Status_Agihan']
            col_h3, col_b3 = st.columns([3, 1])
            with col_h3:
                st.markdown("##### 🏢 Analisis Beban Kerja Anggota Kumpulan Pelaksana (AKP)")
            with col_b3:
                html_akp = generate_printable_html(df_akp, "ANALISIS BEBAN KERJA KUMPULAN AKP", school_info, st.session_state)
                st.download_button(
                    label="🖨️ Cetak Laporan AKP (PDF/A4)",
                    data=html_akp,
                    file_name="Laporan_Beban_Kerja_AKP.html",
                    mime="text/html",
                    type="primary",
                    key=f"btn_print_akp_{data_ver}"
                )
            if not df_akp.empty:
                st.dataframe(df_akp[[c for c in cols_akp if c in df_akp.columns]], use_container_width=True, key=f"tbl_akp_v_{data_ver}")
            else:
                st.info("ℹ️ Tiada rekod kakitangan AKP ditemui.")

        st.markdown("<br>", unsafe_allow_html=True)
        csv_data = df_latest.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Muat Turun Data Laporan Beban Kerja Keseluruhan (CSV)",
            data=csv_data,
            file_name="Laporan_Beban_Kerja_Kakitangan.csv",
            mime="text/csv",
            key=f"btn_dl_csv_v_{data_ver}"
        )
    else:
        st.warning("⚠️ Tiada data kakitangan ditemui. Sila muat naik CSV di Tab 1 atau buka Vault Terenkripsi di Halaman Utama.")