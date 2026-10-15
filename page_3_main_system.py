"""
========================================================================
MYSG KPM: SISTEM PENGURUSAN & ANALISIS BEBAN KERJA
MODULE: PAGE 3 - MAIN SYSTEM CONTROLLER (BERSIH TANPA DUPLIKASI FOOTER)
========================================================================
"""

import streamlit as st
import pandas as pd

# IMPORT MODULE TAB UTAMA (MENGIKUT NAMA FAIL ASAL PROJEK)
import tab_1_dashboard
import tab_2_staff_management
import tab_3_detailed_reports
import tab_4_staff_registration
import tab_5_reassign_workload
import tab_6_appointment_letters

def render_page_3():
    """Membina navigasi Halaman 3 (Tab Utama sahaja, Footer dikendalikan oleh app.py)."""
    
    # -------------------------------------------------------------------
    # BANNER HEADER RASMI KPM
    # -------------------------------------------------------------------
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); 
        color: white; 
        padding: 16px 20px; 
        border-radius: 10px; 
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    ">
        <div style="font-size: 10px; font-weight: bold; letter-spacing: 1px; color: #93c5fd; text-transform: uppercase;">
            KEMENTERIAN PENDIDIKAN MALAYSIA
        </div>
        <h2 style="margin: 4px 0; color: white; font-size: 20px; font-weight: 800;">
            🏫 MySG KPM: Sistem Pengurusan & Analisis Beban Kerja
        </h2>
        <div style="font-size: 11px; color: #e0f2fe; margin-top: 2px;">
            Standard Panduan Pengurusan Sekolah & Agihan Beban Tugas Warga Sekolah
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Inisialisasi Data Sesi Utama Jika Kosong
    if 'staff_df' not in st.session_state:
        st.session_state['staff_df'] = pd.DataFrame()
    if 'school_info' not in st.session_state:
        st.session_state['school_info'] = {
            'nama_sekolah': 'SEKOLAH KEBANGSAAN BANDAR',
            'kod_sekolah': 'XBA2004',
            'jenis_sekolah': 'Sekolah Rendah',
            'tahun_sesi': '2027',
            'alamat_sekolah': 'W.D.T. NO. 297, 90009 SANDAKAN, SABAH',
            'no_tel': '0138847376',
            'email_sekolah': 'xba2004@moe.edu.my',
            'nama_gb': 'SAZAHLIE BIN SAPAR'
        }

    school_info = st.session_state['school_info']

    # -------------------------------------------------------------------
    # PAPARAN TAB UTAMA SISTEM
    # -------------------------------------------------------------------
    t1, t2, t3, t4, t5, t6 = st.tabs([
        "📊 Dashboard & Analisis",
        "👥 Jadual Agihan & Pemberatan Tugas",
        "📋 Laporan Perincian & Bandingan",
        "🔄 Pendaftaran Masuk / Keluar",
        "⚙️ Penetapan Semula Tugas",
        "📑 Penjana Surat Lantikan Tugas"
    ])

    with t1:
        tab_1_dashboard.render_tab_1(school_info)

    with t2:
        tab_2_staff_management.render_tab_2(school_info)

    with t3:
        tab_3_detailed_reports.render_tab_3(school_info)

    with t4:
        tab_4_staff_registration.render_tab_4(school_info)

    with t5:
        tab_5_reassign_workload.render_tab_5(school_info)

    with t6:
        tab_6_appointment_letters.render_tab_6(school_info)