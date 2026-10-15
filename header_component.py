"""
========================================================================
SISTEM PENGURUSAN & PENGIRAAN BEBAN KERJA KAKITANGAN SEKOLAH (MYSG KPM)
MODULE: HEADER & VISI INSPIRASI SISTEM
========================================================================
"""

import streamlit as st

def render_school_header():
    # BANNER HEADER UTAMA
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%);
            padding: 24px;
            border-radius: 12px;
            color: #ffffff;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        ">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <h2 style="margin:0; font-size: 22px; font-weight: 800; color: #ffffff;">
                        🏫 MySG KPM : Sistem Pengurusan & Pengiraan Beban Kerja
                    </h2>
                    <p style="margin: 6px 0 0 0; font-size: 13px; color: #93c5fd;">
                        Pemantauan Beban Kerja Saksama • Ketelusan Agihan Tugas • Penjanaan Surat Lantikan Rasmi
                    </p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_inspiration_card():
    """
    KAD INSPIRASI & MATLAMAT UTAMA PEMBINAAN SISTEM
    """
    st.markdown(
        """
        <div style="
            background-color: #f0fdf4;
            border-left: 5px solid #22c55e;
            padding: 16px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        ">
            <h4 style="margin: 0 0 6px 0; color: #15803d; font-size: 15px;">
                🌱 Matlamat & Visi Utama Pembinaan Sistem
            </h4>
            <p style="margin: 0; font-size: 13px; color: #166534; line-height: 1.6;">
                Sistem ini diilhamkan untuk <b>memelihara kesejahteraan warga pendidik</b> menerusi agihan tugas yang adil, telus, dan berasaskan garis panduan rasmi MySG KPM. Apabila beban kerja diurus dengan bijak, guru dapat menumpukan jiwa dan raga kepada kualiti pengajaran demi kemenjadian murid.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )