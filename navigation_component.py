"""
========================================================================
MYSG KPM: MODUL NAVIGASI SISTEM & KAWALAN POP-OVER
========================================================================
"""

import streamlit as st
import json
import base64
import os
import pandas as pd
import io
import datetime
from crypto_vault import encrypt_payload

def render_navigation():
    """Fungsi pembina bar kawalan navigasi di bawah skrin dan butang eksport Vault/Excel."""
    
    col_nav1, col_nav2 = st.columns([4, 1])

    with col_nav1:
        st.markdown("<div style='margin-top: 15px;'><i>Pastikan anda sentiasa menekan butang <b>Simpan</b> sebelum meninggalkan sistem untuk mengelakkan kehilangan data beban kerja terkini.</i></div>", unsafe_allow_html=True)

    with col_nav2:
        # POP-OVER SIMPAN & KELUAR
        with st.popover("💾 Simpan & Keluar", use_container_width=True):
            st.markdown("#### 🔒 Pengurusan Data & Sesi")
            st.caption("Pilih tindakan pengurusan fail Vault (.mysg) atau eksport data anda:")
            
            pilihan_keluar = st.radio(
                "Pilihan Tindakan:",
                [
                    "💾 Simpan Vault (.mysg) & Keluar",
                    "📥 Simpan Vault (.mysg) & Teruskan Kerja",
                    "📊 Eksport Dataset (Excel)",
                    "🧹 Keluar Tanpa Menyimpan"
                ],
                label_visibility="collapsed"
            )
            
            st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
            
            # ---------------------------------------------------------
            # TINDAKAN 1 & 2: SIMPAN VAULT (.mysg) (KINI TANPA KATA LALUAN)
            # ---------------------------------------------------------
            if pilihan_keluar in ["💾 Simpan Vault (.mysg) & Keluar", "📥 Simpan Vault (.mysg) & Teruskan Kerja"]:
                st.info("Sistem menggunakan penyulitan data automatik (Zero-Config). Klik butang di bawah untuk memuat turun fail keselamatan Vault anda.")
                
                try:
                    payload = {
                        'school_info': st.session_state.get('school_info', {}),
                        'staff_df_dict': st.session_state.get('staff_df', pd.DataFrame()).to_dict() if 'staff_df' in st.session_state else {},
                        'audit_log': st.session_state.get('audit_log', []),
                        'export_timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }

                    # Panggil fungsi yang kini akan menyulitkan data secara automatik (tanpa meminta kata laluan)
                    encrypted_data = encrypt_payload(payload)
                    
                    kod_sekolah = st.session_state.get('school_info', {}).get('kod_sekolah', 'SEKOLAH')
                    
                    if st.download_button(
                        label="⬇️ Muat Turun Fail Vault (.mysg)",
                        data=encrypted_data,
                        file_name=f"MySG_Data_{kod_sekolah}.mysg",
                        mime="application/octet-stream",
                        use_container_width=True,
                        type="primary"
                    ):
                        if "Keluar" in pilihan_keluar:
                            st.session_state.clear()
                            st.rerun()
                        else:
                            st.success("✅ Fail Vault berjaya dimuat turun. Anda boleh meneruskan kerja.")
                            
                except Exception as e:
                    st.error(f"❌ Ralat ketika membina fail vault: {str(e)}")

            # ---------------------------------------------------------
            # TINDAKAN 3: EKSPORT EXCEL 
            # ---------------------------------------------------------
            elif pilihan_keluar == "📊 Eksport Dataset (Excel)":
                st.info("Muat turun data semasa ke format Excel (.xlsx) untuk dikemas kini secara luar talian (offline). Anda boleh muat naik semula fail ini di Langkah 1 nanti.")
                
                if 'staff_df' in st.session_state and not st.session_state['staff_df'].empty:
                    df_export = st.session_state['staff_df'].copy()
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                        df_export.to_excel(writer, index=False, sheet_name='Data_Kakitangan')
                    
                    st.download_button(
                        label="📊 Klik Untuk Muat Turun Fail Excel",
                        data=buffer.getvalue(),
                        file_name="Dataset_Terkini_MySG.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                else:
                    st.warning("Tiada data kakitangan ditemui untuk dimuat turun.")
                    
            # ---------------------------------------------------------
            # TINDAKAN 4: KELUAR TANPA MENYIMPAN
            # ---------------------------------------------------------
            elif pilihan_keluar == "🧹 Keluar Tanpa Menyimpan":
                st.warning("⚠️ Amaran: Semua data kerja yang tidak dimuat turun akan hilang sepenuhnya.")
                if st.button("🔴 Sahkan & Padam Sesi", use_container_width=True):
                    st.session_state.clear()
                    st.rerun()
