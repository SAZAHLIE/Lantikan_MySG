"""
========================================================================
MYSG KPM: SISTEM PENGURUSAN & ANALISIS BEBAN KERJA
MODULE: TAB 6 - PENJANA SURAT LANTIKAN TUGAS RASMI (A4 PORTRAIT)
========================================================================
"""

import streamlit as st
import pandas as pd
from print_engine import generate_appointment_letter_html

def render_tab_6(school_info):
    """Menjana kandungan Tab 6: Penjana Surat Lantikan Tugas Rasmi."""
    st.subheader("📄 Penjanaan Surat Lantikan Tugas Rasmi")
    st.caption("Pilih nama kakitangan di bawah untuk menjana Surat Lantikan Tugas Rasmi berserta Kepala Surat Sekolah.")

    df_staff = st.session_state.get('staff_df', pd.DataFrame())

    if df_staff is not None and not df_staff.empty and 'Nama' in df_staff.columns:
        col_sel, col_btn = st.columns([2.5, 1.5])
        
        with col_sel:
            staf_selected_name = st.selectbox("Pilih Kakitangan / Pegawai:", options=df_staff['Nama'].tolist(), key="select_staf_letter_official")
        
        staf_row = df_staff[df_staff['Nama'] == staf_selected_name].iloc[0]

        with col_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            html_letter = generate_appointment_letter_html(staf_row, school_info, st.session_state)
            
            clean_name = str(staf_selected_name).replace(" ", "_").replace("/", "_")
            
            # BUTANG CETAK SURAT LANTIKAN TANPA NAMA PEGAWAI
            st.download_button(
                label="🖨️ Cetak Surat Lantikan",
                data=html_letter,
                file_name=f"Surat_Lantikan_{clean_name}.html",
                mime="text/html",
                type="primary",
                use_container_width=True,
                key=f"btn_print_letter_{clean_name}_{st.session_state.get('data_version', 1)}"
            )

        st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)

        st.markdown(f"#### 🔍 Pratonton Agihan Tugas: **{staf_selected_name}**")
        col_p1, col_p2 = st.columns(2)
        
        with col_p1:
            st.markdown(f"""
            * **Nama Pegawai:** {staf_row.get('Nama', '-')}
            * **Jawatan Hakiki:** {staf_row.get('Jawatan', '-')}
            * **Gred Perkhidmatan:** {staf_row.get('Gred', '-')}
            * **Kumpulan:** {staf_row.get('Kumpulan', '-')}
            """)

        with col_p2:
            jam_pdp = staf_row.get('JUMLAH_JAM_PDP', 0.0)
            jam_port = staf_row.get('JUMLAH_JAM_PORTFOLIO_H', 0.0) + staf_row.get('JUMLAH_JAM_PORTFOLIO_P', 0.0)
            jam_jk = staf_row.get('JUMLAH_JAM_JAWATANKUASA', 0.0)
            total_jam = staf_row.get('JUMLAH_BEBAN_KESELURAHAN', 0.0)

            st.markdown(f"""
            * **Jam PdP:** {round(jam_pdp, 1)} jam
            * **Jam Portfolio (H + P):** {round(jam_port, 1)} jam
            * **Jam Jawatankuasa (J):** {round(jam_jk, 1)} jam
            * **Jumlah Beban Keseluruhan:** **{round(total_jam, 1)} jam**
            """)

        st.info("💡 **Petua:** Klik butang merah **`🖨️ Cetak Surat Lantikan`** di atas. Fail `.html` yang dimuat turun akan terus membuka dialog cetakan A4 Portrait rasmi apabila dibuka!")

    else:
        st.warning("⚠️ Tiada data kakitangan ditemui. Sila muat naik CSV di Tab 1 atau buka Vault Terenkripsi di Halaman Utama.")