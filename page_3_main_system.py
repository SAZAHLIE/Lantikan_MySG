"""
========================================================================
MYSG KPM: SISTEM PENGURUSAN & ANALISIS BEBAN KERJA
MODULE: PAGE 3 - MAIN SYSTEM CONTROLLER (BERSIH TANPA DUPLIKASI FOOTER)
========================================================================
"""

import streamlit as st
import pandas as pd
import base64

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
    # BANNER HEADER RASMI SEKOLAH (DINAMIK)
    # -------------------------------------------------------------------
    info_sekolah = st.session_state.get('school_info', {})
    nama_sekolah_dinamik = info_sekolah.get('nama_sekolah', 'NAMA SEKOLAH BELUM DITETAPKAN')
    
    # --- FUNGSI PENCARIAN LOGO PINTAR (SUPER SMART SEARCH) ---
    logo_data = None
    
    # 1. Cari dalam school_info dahulu (Semak pelbagai kemungkinan kata kunci)
    for key in ['logo_sekolah_url', 'logo_sekolah', 'logo', 'logo_base64', 'jata_sekolah', 'jata', 'school_logo', 'gambar']:
        if key in info_sekolah and info_sekolah[key]:
            logo_data = info_sekolah[key]
            break
            
    # 2. Jika tiada, cari terus dalam seluruh memori session_state
    if not logo_data:
        for key, val in st.session_state.items():
            if isinstance(key, str) and ('logo' in key.lower() or 'jata' in key.lower()) and val:
                logo_data = val
                break

    # --- PENETAPAN PAPARAN LOGO (SAIZ PENUH) ---
    # Emoji lalai jika benar-benar tiada gambar
    logo_html = '<span style="font-size: 35px; vertical-align: middle; margin-right: 15px;">🏫</span>'
    
    if logo_data:
        try:
            # Jika fail masih dalam bentuk memori fail muat naik Streamlit (UploadedFile)
            if hasattr(logo_data, 'getvalue'):
                encoded = base64.b64encode(logo_data.getvalue()).decode()
                logo_html = f'<img src="data:image/png;base64,{encoded}" height="80" style="vertical-align: middle; object-fit: contain; margin-right: 18px;">'
            # Jika data adalah bait mentah (bytes)
            elif isinstance(logo_data, bytes):
                encoded = base64.b64encode(logo_data).decode()
                logo_html = f'<img src="data:image/png;base64,{encoded}" height="80" style="vertical-align: middle; object-fit: contain; margin-right: 18px;">'
            # Jika data adalah teks (URL atau Base64 mentah)
            elif isinstance(logo_data, str):
                if logo_data.startswith('http') or logo_data.startswith('data:'):
                    logo_html = f'<img src="{logo_data}" height="80" style="vertical-align: middle; object-fit: contain; margin-right: 18px;">'
                else:
                    logo_html = f'<img src="data:image/png;base64,{logo_data}" height="80" style="vertical-align: middle; object-fit: contain; margin-right: 18px;">'
        except Exception:
            pass # Kekalkan ikon 🏫 jika format gambar rosak

    # Paparkan banner dinamik
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); 
        color: white; 
        padding: 16px 20px; 
        border-radius: 10px; 
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    ">
        <p style="font-size: 12px; font-weight: bold; text-transform: uppercase; margin-bottom: 0px;">{nama_sekolah_dinamik}</p>
        <h2 style="color: white; margin-top: 5px; margin-bottom: 5px; display: flex; align-items: center;">
            {logo_html}
            <span style="line-height: 1.2;">MySG KPM: Sistem Pengurusan & Analisis Beban Kerja</span>
        </h2>
        <p style="font-size: 12px; margin-bottom: 0px;">Standard Panduan Pengurusan Sekolah & Agihan Beban Tugas Warga Sekolah</p>
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
