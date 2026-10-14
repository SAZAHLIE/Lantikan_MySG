"""
========================================================================
SISTEM PENGURUSAN & PENGIRAAN BEBAN KERJA KAKITANGAN SEKOLAH (MYSG KPM)
MODULE: NAVIGATION & SYSTEM CONTROL BAR (LENGKAP BUTANG KELUAR SISTEM)
========================================================================
"""

import streamlit as st
import pandas as pd
from crypto_vault import encrypt_payload

def render_navigation_bar(current_step: int, total_steps: int = 3):
    """
    Menampilkan Bar Navigasi Berpandu (Sebelum / Lanjut) 
    serta Butang Keluar Sistem (Simpan Vault & Padam Sesi Pelayan).
    """
    st.markdown("<hr style='margin: 25px 0 15px 0;'>", unsafe_allow_html=True)
    col_back, col_exit, col_next = st.columns([2, 3, 2])

    # 1. BUTANG SEBELUM
    with col_back:
        if current_step > 1:
            if st.button("⬅️ Langkah Sebelumnya", use_container_width=True):
                st.session_state.current_step = current_step - 1
                st.rerun()

    # 2. BUTANG KELUAR SISTEM (EXIT)
    with col_exit:
        with st.popover("🚪 Keluar Sistem / Reset Sesi", use_container_width=True):
            st.markdown("#### 🔒 Keluar Dari Sistem")
            st.caption("Keluar akan membersihkan memori sementara di pelayan demi keselamatan data (PDPA).")
            
            pilihan_keluar = st.radio(
                "Pilihan Keluar:",
                ["💾 Simpan Vault (.mysg) & Keluar", "🧹 Keluar Tanpa Menyimpan"],
                key=f"opt_exit_{current_step}"
            )

            if pilihan_keluar == "💾 Simpan Vault (.mysg) & Keluar":
                passphrase = st.text_input("Tetapkan Kata Laluan Vault:", type="password", key=f"exit_pass_{current_step}")
                
                try:
                    school_info = st.session_state.get('school_info', {})
                    kod_sek = school_info.get('kod_sekolah', 'MYSG')
                    df_staff = st.session_state.get('staff_df', None)
                    staff_dict = df_staff.to_dict(orient='records') if (df_staff is not None and not df_staff.empty) else []

                    full_payload = {
                        'school_info': school_info,
                        'staff_df_dict': staff_dict
                    }

                    if passphrase and len(passphrase) >= 4:
                        encrypted_bytes = encrypt_payload(full_payload, passphrase)

                        if st.download_button(
                            label="📥 Simpan Vault & Keluar Sekarang",
                            data=encrypted_bytes,
                            file_name=f"Vault_MySG_{kod_sek}_Backup.mysg",
                            mime="application/octet-stream",
                            type="primary",
                            use_container_width=True
                        ):
                            st.session_state.clear()
                            st.success("✅ Fail vault disimpan & memori pelayan telah dibersihkan sepenuhnya!")
                            st.rerun()
                    else:
                        st.caption("⚠️ Masukkan kata laluan (sekurang-kurangnya 4 aksara) untuk mengaktifkan muat turun.")
                except Exception as e:
                    st.error(f"❌ Ralat: {str(e)}")

            else:
                if st.button("🔴 Sahkan Keluar Tanpa Menyimpan", type="primary", use_container_width=True):
                    st.session_state.clear()
                    st.success("✅ Memori sesi dibersihkan.")
                    st.rerun()

    # 3. BUTANG LANJUT
    with col_next:
        if current_step < total_steps:
            if st.button("Langkah Seterusnya ➡️", type="primary", use_container_width=True):
                st.session_state.current_step = current_step + 1
                st.rerun()