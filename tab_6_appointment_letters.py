"""
========================================================================
MYSG KPM: SISTEM PENGURUSAN & ANALISIS BEBAN KERJA
MODULE: TAB 6 - PENJANA SURAT LANTIKAN TUGAS RASMI (PDF INDIVIDU & PUKAL)
========================================================================
"""

import streamlit as st
import pandas as pd
import io
import time
from pdf_generator import generate_appointment_letter_pdf

# Cuba import PyPDF2 atau pypdf untuk penggabungan PDF pukal jika wujud
try:
    from PyPDF2 import PdfMerger
    HAS_PDF_MERGER = True
except ImportError:
    try:
        from pypdf import PdfMerger
        HAS_PDF_MERGER = True
    except ImportError:
        HAS_PDF_MERGER = False

def render_tab_6(school_info):
    """Menjana kandungan Tab 6: Penjana Surat Lantikan Tugas Rasmi PDF (Individu & Keseluruhan)."""
    st.subheader("📄 Penjanaan Surat Lantikan Tugas Rasmi (Format PDF KPM)")
    st.caption("Jana dan muat turun Surat Lantikan Rasmi berformat PDF standard JPA/KPM mengikut individu atau secara pukal untuk keseluruhan warga sekolah.")

    df_staff = st.session_state.get('staff_df', pd.DataFrame())
    data_ver = st.session_state.get('data_version', 1)

    if df_staff is not None and not df_staff.empty and 'Nama' in df_staff.columns:
        
        # BAHAGIAN 1: MUAT TURUN PUKAL (KESELURAHAN SEKOAH)
        with st.expander("📦 **Muat Turun Surat Lantikan Pukal (Keseluruhan Warga Sekolah)**", expanded=True):
            st.markdown("Muat turun fail PDF gabungan yang mengandungi Surat Lantikan bagi **semua kakitangan** untuk memudahkan urusan pencetakan sekali gus.")
            
            if st.button("🔄 Jana & Sediakan PDF Keseluruhan Staf", type="primary", key=f"btn_prep_all_pdf_{data_ver}"):
                with st.spinner("Sedang menjana fail PDF Surat Lantikan untuk semua kakitangan... Sila tunggu sebentar."):
                    try:
                        if HAS_PDF_MERGER:
                            merger = PdfMerger()
                            for _, row in df_staff.iterrows():
                                pdf_bytes = generate_appointment_letter_pdf(row, school_info)
                                merger.append(io.BytesIO(pdf_bytes))
                            
                            output_merged = io.BytesIO()
                            merger.write(output_merged)
                            merger.close()
                            merged_bytes = output_merged.getvalue()
                            
                            kod_sek = school_info.get('kod_sekolah', 'SEKOLAH')
                            file_name_all = f"Surat_Lantikan_Keseluruhan_{kod_sek}.pdf"

                            st.success(f"✅ Berjaya menjana PDF bagi {len(df_staff)} orang kakitangan!")
                            st.download_button(
                                label=f"📥 Muat Turun Fail PDF Keseluruhan ({file_name_all})",
                                data=merged_bytes,
                                file_name=file_name_all,
                                mime="application/pdf",
                                type="primary",
                                key=f"btn_dl_all_pdf_{data_ver}"
                            )
                        else:
                            st.warning("⚠️ Pustaka `PyPDF2` / `pypdf` tidak ditemui di dalam pelayan. Sila pastikan `pypdf` ditambah ke dalam `requirements.txt` untuk fungsi gabungan pukal.")
                    except Exception as e:
                        st.error(f"❌ Ralat semasa menjana PDF Pukal: {str(e)}")

        st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)

        # BAHAGIAN 2: MUAT TURUN INDIVIDU
        st.markdown("#### 👤 Penjanaan & Pratonton Surat Lantikan Individu")
        col_sel, col_btn = st.columns([2.5, 1.5])
        
        with col_sel:
            staf_selected_name = st.selectbox(
                "Pilih Kakitangan / Pegawai:", 
                options=df_staff['Nama'].tolist(), 
                key=f"select_staf_letter_pdf_{data_ver}"
            )
        
        staf_row = df_staff[df_staff['Nama'] == staf_selected_name].iloc[0]

        with col_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            try:
                pdf_bytes_ind = generate_appointment_letter_pdf(staf_row, school_info)
                clean_name = str(staf_selected_name).replace(" ", "_").replace("/", "_")
                file_name_ind = f"Surat_Lantikan_{clean_name}.pdf"

                st.download_button(
                    label="📥 Muat Turun Surat (PDF)",
                    data=pdf_bytes_ind,
                    file_name=file_name_ind,
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True,
                    key=f"btn_dl_ind_pdf_{clean_name}_{data_ver}"
                )
            except Exception as e:
                st.error(f"❌ Ralat PDF: {str(e)}")

        st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)

        # PRATONTON MAKLUMAT STAF
        st.markdown(f"#### 🔍 Perincian Tugas Dalam Surat: **{staf_selected_name}**")
        col_p1, col_p2 = st.columns(2)
        
        with col_p1:
            st.markdown(f"""
            * **Nama Pegawai:** {staf_row.get('Nama', '-')}
            * **Jawatan Hakiki:** {staf_row.get('Jawatan', '-')}
            * **Gred Perkhidmatan:** {staf_row.get('Gred', '-')}
            * **Kumpulan:** {staf_row.get('Kumpulan', '-')}
            """)

        with col_p2:
            jam_pdp = float(staf_row.get('JUMLAH_JAM_PDP', 0.0) or 0.0)
            jam_port = float(staf_row.get('JUMLAH_JAM_PORTFOLIO_H', 0.0) or 0.0) + float(staf_row.get('JUMLAH_JAM_PORTFOLIO_P', 0.0) or 0.0)
            jam_jk = float(staf_row.get('JUMLAH_JAM_JAWATANKUASA', 0.0) or 0.0)
            total_jam = float(staf_row.get('JUMLAH_BEBAN_KESELURAHAN', 0.0) or 0.0)

            st.markdown(f"""
            * **Jam PdP:** {round(jam_pdp, 1)} jam
            * **Jam Portfolio (H + P):** {round(jam_port, 1)} jam
            * **Jam Jawatankuasa (J):** {round(jam_jk, 1)} jam
            * **Jumlah Beban Keseluruhan:** **{round(total_jam, 1)} jam**
            """)

        st.info("💡 **Makluman:** Dokumen PDF yang dimuat turun akan mematuhi format rasmi KPM berserta penomboran halaman automatik dan Kaki Surat yang tepat.")

    else:
        st.warning("⚠️ Tiada data kakitangan ditemui. Sila muat naik CSV di Tab 1 atau buka Vault Terenkripsi di Halaman Utama.")
