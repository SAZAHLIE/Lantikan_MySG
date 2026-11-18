"""
========================================================================
MYSG KPM: TAB 3 - LAPORAN PERINCIAN BEBAN KERJA INDIVIDU
========================================================================
"""

import streamlit as st
import pandas as pd
import io
from print_engine import generate_individual_detailed_report_html

def render_tab_3(school_info):
    st.subheader("2. Carian & Analisis Perincian Beban Kerja Individu")
    
    df_staff = st.session_state.get('staff_df', pd.DataFrame())

    if df_staff is not None and not df_staff.empty and 'Nama' in df_staff.columns:
        
        # --- TAMBAHAN BARU: CETAK PUKAL KESELURUHAN STAF ---
        st.markdown("#### 📦 Cetakan Pukal (Keseluruhan Staf)")
        st.caption("Jana dan muat turun gabungan Laporan Perincian Beban Tugas (A4 Portrait) bagi semua warga sekolah dalam satu fail.")
        
        data_ver = st.session_state.get('data_version', 1)
        
        if st.button("🔄 Jana & Sediakan Laporan Individu Pukal", type="primary", key=f"btn_prep_all_reports_bulk_{data_ver}"):
            with st.spinner("Sedang menjana fail laporan untuk semua kakitangan... Fungsi ini mungkin mengambil masa sebentar."):
                try:
                    # Menjana satu gabungan HTML besar dengan pemisah page-break
                    combined_html = ""
                    
                    for i, row in df_staff.iterrows():
                        html_ind = generate_individual_detailed_report_html(
                            row, 
                            school_info, 
                            df_staff, 
                            st.session_state
                        )
                        
                        # Buang tags <body> & <html> luaran untuk membolehkan penggabungan blok yang kemas
                        if "<body>" in html_ind and "</body>" in html_ind:
                            body_content = html_ind.split("<body>")[1].split("</body>")[0]
                        else:
                            body_content = html_ind
                            
                        if i == 0 and "<head>" in html_ind:
                             head_content = html_ind.split("<head>")[1].split("</head>")[0]
                             combined_html += f"<!DOCTYPE html><html lang='ms'><head>{head_content}</head><body>"
                        
                        combined_html += body_content
                        
                        # Pemisah Muka Surat antara laporan
                        if i < len(df_staff) - 1:
                            combined_html += "<div style='page-break-after: always;'></div>"
                    
                    combined_html += "</body></html>"
                    
                    kod_sek = school_info.get('kod_sekolah', 'SEKOLAH')
                    file_name_all = f"Laporan_Individu_Pukal_{kod_sek}.html"

                    st.success(f"✅ Berjaya menjana laporan pukal bagi {len(df_staff)} orang kakitangan!")
                    st.download_button(
                        label=f"📥 Muat Turun Fail Laporan Pukal (HTML)",
                        data=combined_html,
                        file_name=file_name_all,
                        mime="text/html",
                        type="primary",
                        use_container_width=True,
                        key=f"btn_dl_all_reports_bulk_{data_ver}"
                    )
                except Exception as e:
                    st.error(f"❌ Ralat semasa menjana laporan Pukal: {str(e)}")

        st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)

        # --- CETAKAN INDIVIDU (Sedia Ada) ---
        st.markdown("#### 👤 Cetakan Individu")
        col_sel, col_btn = st.columns([2.5, 1.5])
        
        with col_sel:
            staf_selected_name = st.selectbox(
                "Pilih Kakitangan untuk Memanggil Data Perincian:", 
                options=df_staff['Nama'].tolist(), 
                key="select_staf_report_individual"
            )
        
        staf_ind_row = df_staff[df_staff['Nama'] == staf_selected_name].iloc[0]

        with col_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            
            html_ind = generate_individual_detailed_report_html(
                staf_ind_row, 
                school_info, 
                df_staff, 
                st.session_state
            )
            
            clean_name = str(staf_selected_name).replace(" ", "_").replace("/", "_")
            
            st.download_button(
                label="🖨️ Cetak Laporan Individu",
                data=html_ind,
                file_name=f"Laporan_Individu_{clean_name}.html",
                mime="text/html",
                type="primary",
                use_container_width=True,
                key=f"btn_print_ind_report_{clean_name}_{st.session_state.get('data_version', 1)}"
            )
