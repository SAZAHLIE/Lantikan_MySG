"""
========================================================================
MYSG KPM: PREVIEW APP (MODE UJIAN DENGAN DATASET SEBENAR)
========================================================================
"""

import streamlit as st
import pandas as pd
import os
import time

# Tetapan Halaman
st.set_page_config(
    page_title="[PREVIEW MODE] MySG KPM - Data Sebenar",
    page_icon="🧪",
    layout="wide"
)

# Force reload module untuk elak cache lama
import importlib
import page_3_main_system
import mysg_core
importlib.reload(mysg_core)
importlib.reload(page_3_main_system)

from page_3_main_system import render_page_3
from mysg_core import calculate_workload_df

def inject_real_dataset():
    """Membaca dan memproses dataset KPM sebenar ke dalam session state."""
    
    # 1. PROFIL SEKOLAH
    if 'school_info' not in st.session_state or not st.session_state.school_info:
        st.session_state['school_info'] = {
            'nama_sekolah': 'SEKOLAH KEBANGSAAN BANDAR',
            'kod_sekolah': 'XBA2004',
            'jenis_sekolah': 'Sekolah Rendah',
            'tahun_sesi': '2027',
            'alamat_sekolah': 'W.D.T. NO. 297, 90009 SANDAKAN, SABAH',
            'no_tel': '089-000000',
            'email_sekolah': 'xba2004@moe.edu.my',
            'nama_gb': 'SAZAHLIE BIN SAPAR'
        }

    # 2. BACA FAIL DATASET SEBENAR CSV
    csv_file_path = 'Dataset_KPM_Terlaras_butir_15.csv'
    
    if 'staff_df' not in st.session_state or st.session_state.staff_df is None or st.session_state.staff_df.empty:
        if os.path.exists(csv_file_path):
            df_raw = pd.read_csv(csv_file_path)
            jenis_sek = st.session_state.school_info.get('jenis_sekolah', 'Sekolah Rendah')
            
            # Pengiraan beban kerja menggunakan enjin mysg_core
            df_processed = calculate_workload_df(df_raw, jenis_sek)
            st.session_state['staff_df'] = df_processed
            st.session_state['current_step'] = 3
            st.session_state['data_version'] = int(time.time())
        else:
            st.error(f"❌ Fail dataset `{csv_file_path}` tidak dijumpai dalam folder projek!")

def main():
    inject_real_dataset()
    
    st.sidebar.title("🧪 Mode Pratonton Data Sebenar")
    st.sidebar.info("Aplikasi sedang berjalan menggunakan **Dataset_KPM_Terlaras_butir_15.csv**.")
    
    if st.sidebar.button("🔄 Clear Cache & Reset Data Sebenar"):
        st.session_state.clear()
        st.cache_data.clear()
        st.rerun()

    render_page_3()

if __name__ == "__main__":
    main()