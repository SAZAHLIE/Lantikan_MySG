"""
========================================================================
MYSG KPM: SISTEM PENGURUSAN & ANALISIS BEBAN KERJA
MODULE: NAVIGATION COMPONENT - MUKTAMAD SAVE & EXIT (1-CLICK DOWNLOAD)
========================================================================
"""

import streamlit as st
import pandas as pd
import io
from crypto_vault import encrypt_payload

def go_to_previous_step():
    """Fungsi kembali ke langkah sebelumnya secara selamat."""
    if st.session_state.get('current_step', 1) > 1:
        st.session_state.current_step -= 1

def go_to_next_step():
    """Fungsi maju ke langkah seterusnya secara selamat."""
    if st.session_state.get('current_step', 1) < 3:
        st.session_state.current_step += 1

def render_navigation_bar(current_step=1, total_steps=3):
    """
    Menjana bar navigasi berpusat lengkap berserta borang Simpan & Keluar yang stabil.
    """
    st.markdown("<br><hr style='border:none; border-top:1px dashed #cbd5e1; margin: 20px 0;'>", unsafe_allow_html=True)
    
    col_nav1, col_nav2, col_nav3, col_nav4 = st.columns([1.5, 2, 1.5, 1.5])

    # -------------------------------------------------------------------
    # 1. BUTANG LANGKAH SEBELUMNYA
    # -------------------------------------------------------------------
    with col_nav1:
        if current_step > 1:
            st.button(
                "⬅️ Langkah Sebelumnya", 
                type="secondary",
                use_container_width=True, 
                key=f"nav_btn_back_step_{current_step}",
                on_click=go_to_previous_step
            )
        else:
            st.button("⬅️ Langkah Sebelumnya", disabled=True, use_container_width=True, key="nav_btn_back_disabled")

    # -------------------------------------------------------------------
    # 2. STATUS HALAMAN
    # -------------------------------------------------------------------
    with col_nav2:
        st.markdown(
            f"""
            <div style="padding-top: 6px; text-align: center; font-size: 13px; color: #475569;">
                📌 <b>Status Navigasi:</b> Halaman {current_step} daripada {total_steps}
            </div>
            """, 
            unsafe_allow_html=True
        )

    # -------------------------------------------------------------------
    # 3. BUTANG LANGKAH SETERUSNYA
    # -------------------------------------------------------------------
    with col_nav3:
        if current_step < total_steps:
            st.button(
                "Langkah Seterusnya ➡️", 
                type="primary",
                use_container_width=True, 
                key=f"nav_btn_next_step_{current_step}",
                on_click=go_to_next_step
            )
        else:
            st.button("Selesai (Halaman Akhir) ✅", disabled=True, use_container_width=True, key="nav_btn_next_disabled")

    # -------------------------------------------------------------------
    # 4. BUTANG SIMPAN & KELUAR (DIRECT EXPORT VAULT)
    # -------------------------------------------------------------------
    with col_nav4:
        with st.popover("💾 Simpan & Keluar", use_container_width=True):
            st.markdown("### 🔒 Pengurusan Data & Sesi")
            st.caption("Pilih tindakan pengurusan fail Vault (.mysg) atau eksport data anda:")

            pilihan_keluar = st.radio(
                "Pilihan Tindakan:",
                [
                    "💾 Simpan Vault (.mysg) & Keluar", 
                    "📥 Simpan Vault (.mysg) & Teruskan Kerja", 
                    "📊 Eksport Dataset (Excel)", 
                    "🧹 Keluar Tanpa Menyimpan"
                ],
                key=f"popover_pilihan_keluar_{current_step}"
            )

            # ---------------------------------------------------------
            # TINDAKAN 1 & 2: SIMPAN VAULT (.mysg) - KOD ASAL
            # ---------------------------------------------------------
            if pilihan_keluar in ["💾 Simpan Vault (.mysg) & Keluar", "📥 Simpan Vault (.mysg) & Teruskan Kerja"]:
                passphrase = st.text_input(
                    "Tetapkan Kata Laluan Vault (Min 4 Aksara):", 
                    type="password", 
                    key=f"passphrase_input_{current_step}"
                )

                st.markdown("<br>", unsafe_allow_html=True)

                if passphrase and len(passphrase) >= 4:
                    try:
                        # 1. Sediakan Data & Enkrip Serta-merta
                        school_info = st.session_state.get('school_info', {})
                        staff_df = st.session_state.get('staff_df', pd.DataFrame())
                        staff_dict = staff_df.to_dict(orient='records') if isinstance(staff_df, pd.DataFrame) and not staff_df.empty else []
                        audit_log = st.session_state.get('audit_log', [])

                        # Sertakan Log Audit (MAMPU ICT Standard)
                        payload = {'school_info': school_info, 'staff_df_dict': staff_dict, 'audit_log': audit_log}
                        encrypted_bytes = encrypt_payload(payload, passphrase)
                        
                        kod_sek = school_info.get('kod_sekolah', 'SEKOLAH')
                        if not kod_sek:
                            kod_sek = 'SEKOLAH'
                        file_name = f"Vault_MySG_{kod_sek}_backup.mysg"

                        # 2. PAPARKAN BUTANG MUAT TURUN UTAMA SECARA DIRECT
                        st.success(f"✅ Kata laluan sedia! Sila klik butang muat turun di bawah:")
                        
                        st.download_button(
                            label=f"📥 Muat Turun Fail Vault ({file_name})",
                            data=encrypted_bytes,
                            file_name=file_name,
                            mime="application/octet-stream",
                            type="primary",
                            use_container_width=True,
                            key=f"btn_direct_download_vault_{current_step}"
                        )
                        
                        if pilihan_keluar == "💾 Simpan Vault (.mysg) & Keluar":
                            st.info("⚠️ Sila pastikan muat turun selesai sepenuhnya terlebih dahulu. Kemudian klik butang di bawah untuk memadam memori sesi secara selamat.")
                            if st.button("🧹 Selesai Muat Turun & Bersihkan Memori", use_container_width=True, key=f"btn_clear_exit_{current_step}"):
                                st.session_state.clear()
                                st.rerun()
                        else:
                            st.info("💡 Anda boleh teruskan kerja seperti biasa selepas muat turun fail Vault ini sebagai salinan keselamatan (backup).")

                    except Exception as e:
                        st.error(f"❌ Ralat menjana Vault: {str(e)}")
                else:
                    st.info("ℹ️ Sila taip kata laluan (sekurang-kurangnya 4 aksara) di atas untuk memaparkan butang Muat Turun Vault.")

            # ---------------------------------------------------------
            # TINDAKAN 3: EKSPORT EXCEL (FUNGSI BAHARU)
            # ---------------------------------------------------------
            elif pilihan_keluar == "📊 Eksport Dataset (Excel)":
                st.markdown("<br>", unsafe_allow_html=True)
                st.info("Muat turun data semasa ke format Excel (.xlsx) untuk disemak atau dikemas kini di luar sistem.")
                
                staff_df = st.session_state.get('staff_df', pd.DataFrame())
                if not staff_df.empty:
                    # Salin dan jana fail Excel di dalam memori
                    df_export = staff_df.copy()
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                        df_export.to_excel(writer, index=False, sheet_name='Data_Kakitangan')
                    
                    st.download_button(
                        label="📊 Klik Untuk Muat Turun Fail Excel",
                        data=buffer.getvalue(),
                        file_name="Dataset_Terkini_MySG.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True,
                        key=f"btn_export_excel_{current_step}"
                    )
                else:
                    st.warning("Tiada data kakitangan ditemui untuk dimuat turun.")

            # ---------------------------------------------------------
            # TINDAKAN 4: KELUAR TANPA MENYIMPAN
            # ---------------------------------------------------------
            elif pilihan_keluar == "🧹 Keluar Tanpa Menyimpan":
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🔴 Pengesahan Keluar Tanpa Menyimpan", type="primary", use_container_width=True, key=f"popover_btn_no_save_{current_step}"):
                    st.session_state.clear()
                    st.rerun()
