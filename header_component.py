"""
========================================================================
SISTEM PENGURUSAN & PENGIRAAN BEBAN KERJA KAKITANGAN SEKOLAH (MYSG KPM)
HEADER COMPONENT - KAD HEADER RASMI SEKOLAH DENGAN LENCANA
========================================================================
"""

import streamlit as st

def render_school_header():
    info_sec = st.session_state.get('school_info', {})
    raw_jenis = str(info_sec.get('jenis_sekolah', 'Sekolah Rendah'))
    jenis_sekolah = "Sekolah Menengah" if "Menengah" in raw_jenis else "Sekolah Rendah"
    
    # LOGIK PAPARAN LENCANA SEKOLAH BESAR & TEKS KEMAS SEBELAH KANAN
    logo_b64 = info_sec.get('logo_base64', '')
    if logo_b64:
        logo_header_html = f'<img src="{logo_b64}" style="height: 78px; width: auto; max-width: 95px; object-fit: contain;" alt="Lencana Sekolah">'
    else:
        logo_header_html = '<span style="font-size: 48px; line-height: 1;">🏫</span>'

    st.markdown(f"""
    <div style="
        background-color: #f8fafc; 
        padding: 20px 24px; 
        border-radius: 14px; 
        border: 1px solid #e2e8f0; 
        margin-bottom: 18px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        display: flex;
        align-items: center;
        gap: 20px;
    ">
        <div style="flex: 0 0 auto; display: flex; align-items: center; justify-content: center;">
            {logo_header_html}
        </div>
        <div style="flex: 1; min-width: 0;">
            <h2 style="margin: 0 0 6px 0; color: #0f172a; font-size: 22px; font-weight: 800; letter-spacing: -0.3px; line-height: 1.2;">
                {info_sec.get('nama_sekolah', 'NAMA SEKOLAH')} ({info_sec.get('kod_sekolah', 'KOD')})
            </h2>
            <p style="margin: 0 0 4px 0; color: #475569; font-size: 13.5px; line-height: 1.4;">
                📍 <b>Alamat:</b> {info_sec.get('alamat_sekolah', '-')} &nbsp;|&nbsp; 📞 <b>Tel:</b> {info_sec.get('no_telefon', '-')}
            </p>
            <p style="margin: 0; color: #64748b; font-size: 12.5px; line-height: 1.4;">
                <b>Peringkat:</b> {jenis_sekolah} &nbsp;|&nbsp; <b>Sesi:</b> {info_sec.get('tahun_sesi', '-')} &nbsp;|&nbsp; <b>Pentadbir:</b> {info_sec.get('nama_gb', '-')}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)