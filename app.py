"""
========================================================================
SISTEM PENGURUSAN & PENGIRAAN BEBAN KERJA KAKITANGAN SEKOLAH (MYSG KPM)
APP UTAMA - STREAMLIT ENTRY POINT (PRODUCTION READY)
========================================================================
"""

import streamlit as st
import os

st.set_page_config(
    page_title="Sistem Pengurusan & Pengiraan Beban Kerja Kakitangan Sekolah (MySG KPM)",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# SEKSYEN IMPORT MODULE
from mysg_core import SYSTEM_NAME, SYSTEM_VERSION, calculate_workload_df
from page_1_requirements import render_page_1
from page_2_school_profile import render_page_2
from page_3_main_system import render_page_3
from navigation_component import render_navigation_bar

def main():
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1

    current = st.session_state.current_step

    # PAPARKAN HALAMAN MENGIKUT LANGKAH
    if current == 1:
        render_page_1()
    elif current == 2:
        render_page_2()
    elif current == 3:
        render_page_3()

    # PAPARKAN BAR NAVIGASI (SEBELUM, SIMPAN & KELUAR, LANJUT) DI BAHAGIAN BAWAH
    render_navigation_bar(current_step=current, total_steps=3)

if __name__ == "__main__":
    main()