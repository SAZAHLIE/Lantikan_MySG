"""
========================================================================
MYSG KPM: SISTEM PENGURUSAN & ANALISIS BEBAN KERJA
MODULE: PAGE 3 - MAIN SYSTEM CONTROLLER (DENGAN SIDEBAR PROFIL)
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
import tab_7_org_chart

def render_page_3():
    """Membina navigasi Halaman 3 (Tab Utama sahaja, Footer dikendalikan oleh app.py)."""
    
    # Inisialisasi Data Sesi Utama Jika Kosong
    if 'staff_df' not in st.session_state:
        st.session_state['staff_df'] = pd.DataFrame()
    if 'school_info' not in st.session_state:
        st.session_state['school_info'] = {
            'nama_sekolah': 'SEKOLAH KEBANGSAAN BANDAR',
            'kod_sekolah': 'XBA2004',
            'jenis_sekolah': 'Sekolah Rendah',
            'tahun_sesi': '2027',
            'alamat_1': 'W.D.T. NO. 297',
            'alamat_2': '90009 SANDAKAN',
            'negeri_negara': 'SABAH',
            'alamat_sekolah': 'W.D.T. NO. 297, 90009 SANDAKAN, SABAH',
            'no_telefon': '0138847376',
            'no_faks': '',
            'emel_rasmi': 'xba2004@moe.edu.my',
            'nama_gb': 'SAZAHLIE BIN SAPAR',
            'admin_pin': '1234'
        }

    school_info = st.session_state['school_info']

    # -------------------------------------------------------------------
    # SIDEBAR: PENGURUSAN & TETAPAN PROFIL SEKOLAH 
    # -------------------------------------------------------------------
    with st.sidebar:
        st.markdown("### 🏢 Navigasi & Tetapan")
        
        # Menggunakan Expander agar Sidebar nampak kemas
        with st.expander("⚙️ Kemas Kini Profil Sekolah", expanded=False):
            st.caption("Ubah maklumat sekolah anda di sini. Perubahan akan terus terpapar pada surat lantikan dan sistem.")
            
            with st.form(key="sidebar_school_profile_form"):
                n_sek = st.text_input("Nama Sekolah:", value=school_info.get('nama_sekolah', ''))
                k_sek = st.text_input("Kod Sekolah:", value=school_info.get('kod_sekolah', ''))
                j_sek = st.selectbox("Peringkat Institusi:", options=["Sekolah Rendah", "Sekolah Menengah"], index=1 if "Menengah" in school_info.get('jenis_sekolah', '') else 0)
                
                sesi_opts = ["2027", "2028", "2029", "2030"]
                curr_sesi = str(school_info.get('tahun_sesi', '2027'))
                sesi_idx = sesi_opts.index(curr_sesi) if curr_sesi in sesi_opts else 0
                t_sesi = st.selectbox("Sesi Persekolahan:", options=sesi_opts, index=sesi_idx)
                
                gb_nama = st.text_input("Nama Pengetua / Guru Besar:", value=school_info.get('nama_gb', ''))
                
                a1 = st.text_input("Alamat Baris 1:", value=school_info.get('alamat_1', ''))
                a2 = st.text_input("Alamat Baris 2:", value=school_info.get('alamat_2', ''))
                neg = st.text_input("Negeri:", value=school_info.get('negeri_negara', ''))
                
                tel = st.text_input("No. Telefon:", value=school_info.get('no_telefon', ''))
                faks = st.text_input("No. Faks:", value=school_info.get('no_faks', ''))
                emel = st.text_input("Emel:", value=school_info.get('emel_rasmi', ''))
                
                ruj = st.text_input("No. Rujukan Lantikan:", value=school_info.get('no_rujukan', ''))
                
                new_logo = st.file_uploader("Kemas Kini Lencana (PNG/JPG)", type=['png', 'jpg', 'jpeg'])
                
                btn_save_profile = st.form_submit_button("💾 Simpan Perubahan Profil", type="primary", use_container_width=True)
                
                if btn_save_profile:
                    if not n_sek.strip() or not k_sek.strip() or not gb_nama.strip():
                        st.error("Sila isi Nama, Kod Sekolah & Nama GB.")
                    else:
                        existing_logo_b64 = school_info.get('logo_base64', '')
                        logo_b64 = existing_logo_b64
                        if new_logo is not None:
                            bytes_data = new_logo.read()
                            encoded = base64.b64encode(bytes_data).decode('utf-8')
                            mime = "png" if new_logo.name.lower().endswith('.png') else "jpeg"
                            logo_b64 = f"data:image/{mime};base64,{encoded}"
                            
                        alamat_penuh = f"{a1}, {a2}, {neg}".strip(', ')
                        
                        st.session_state['school_info'] = {
                            'nama_sekolah': n_sek.upper().strip(),
                            'kod_sekolah': k_sek.upper().strip(),
                            'jenis_sekolah': j_sek,
                            'tahun_sesi': t_sesi,
                            'alamat_1': a1.strip(),
                            'alamat_2': a2.strip(),
                            'negeri_negara': neg.upper().strip(),
                            'alamat_sekolah': alamat_penuh,
                            'no_telefon': tel.strip(),
                            'no_faks': faks.strip(),
                            'emel_rasmi': emel.strip(),
                            'nama_gb': gb_nama.upper().strip(),
                            'no_rujukan': ruj.strip(),
                            'admin_pin': '1234',
                            'logo_base64': logo_b64
                        }
                        st.toast("✅ Profil sekolah berjaya dikemas kini!")
                        st.rerun()
                        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; font-size: 11px; color: #888;'>Sistem Pengurusan Beban Kerja MySG KPM</div>", unsafe_allow_html=True)

    # Segarkan semula maklumat terkini selepas sebarang perubahan Sidebar
    info_sekolah = st.session_state.get('school_info', {})
    nama_sekolah_dinamik = info_sekolah.get('nama_sekolah', 'NAMA SEKOLAH BELUM DITETAPKAN')
    
    # -------------------------------------------------------------------
    # BANNER HEADER RASMI SEKOLAH (DINAMIK)
    # -------------------------------------------------------------------
    logo_data = None
    
    # Cari dalam school_info dahulu
    for key in ['logo_sekolah_url', 'logo_sekolah', 'logo', 'logo_base64', 'jata_sekolah', 'jata', 'school_logo', 'gambar']:
        if key in info_sekolah and info_sekolah[key]:
            logo_data = info_sekolah[key]
            break
            
    # Jika tiada, cari terus dalam seluruh memori session_state
    if not logo_data:
        for key, val in st.session_state.items():
            if isinstance(key, str) and ('logo' in key.lower() or 'jata' in key.lower()) and val:
                logo_data = val
                break

    # Penetapan Paparan Logo 
    logo_html = '<span style="font-size: 35px; vertical-align: middle; margin-right: 15px;">🏫</span>'
    
    if logo_data:
        try:
            if hasattr(logo_data, 'getvalue'):
                encoded = base64.b64encode(logo_data.getvalue()).decode()
                logo_html = f'<img src="data:image/png;base64,{encoded}" height="80" style="vertical-align: middle; object-fit: contain; margin-right: 18px;">'
            elif isinstance(logo_data, bytes):
                encoded = base64.b64encode(logo_data).decode()
                logo_html = f'<img src="data:image/png;base64,{encoded}" height="80" style="vertical-align: middle; object-fit: contain; margin-right: 18px;">'
            elif isinstance(logo_data, str):
                if logo_data.startswith('http') or logo_data.startswith('data:'):
                    logo_html = f'<img src="{logo_data}" height="80" style="vertical-align: middle; object-fit: contain; margin-right: 18px;">'
                else:
                    logo_html = f'<img src="data:image/png;base64,{logo_data}" height="80" style="vertical-align: middle; object-fit: contain; margin-right: 18px;">'
        except Exception:
            pass 

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

    # -------------------------------------------------------------------
    # PAPARAN TAB UTAMA SISTEM
    # -------------------------------------------------------------------
    t1, t2, t3, t4, t5, t6, t7 = st.tabs([
        "📊 Dashboard & Analisis",
        "👥 Jadual Agihan & Pemberatan Tugas",
        "📋 Laporan Perincian & Bandingan",
        "🔄 Pendaftaran Masuk / Keluar",
        "⚙️ Penetapan Semula Tugas",
        "📑 Penjana Surat Lantikan Tugas",
        "🏢 Carta Organisasi"
    ])

    with t1:
        tab_1_dashboard.render_tab_1(info_sekolah)

    with t2:
        tab_2_staff_management.render_tab_2(info_sekolah)

    with t3:
        tab_3_detailed_reports.render_tab_3(info_sekolah)

    with t4:
        tab_4_staff_registration.render_tab_4(info_sekolah)

    with t5:
        tab_5_reassign_workload.render_tab_5(info_sekolah)

    with t6:
        tab_6_appointment_letters.render_tab_6(info_sekolah)

    with t7:
        tab_7_org_chart.render_tab_7(info_sekolah)
