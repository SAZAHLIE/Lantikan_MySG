"""
========================================================================
SISTEM PENGURUSAN & PENGIRAAN BEBAN KERJA KAKITANGAN SEKOLAH (MYSG KPM)
PAGE 1 - PROFIL SEKOLAH & INTEGRASI VAULT TERENKRIPSI (AES-256)
========================================================================
"""

import streamlit as st
import json
import base64
import os
import pandas as pd
from crypto_vault import encrypt_payload, decrypt_payload
from mysg_core import calculate_workload_df
from header_component import render_school_header
from footer_component import render_footer

def render_page_1():
    render_school_header()

    st.subheader("🔑 Modul Storan Selamat (Zero-Server-Storage)")
    st.info(
        "Sistem ini mematuhi Akta Perlindungan Data Peribadi (PDPA). "
        "Tiada data disimpan pada pelayan. Anda boleh menyimpan atau membuka vault terenkripsi (.mysg) secara terus pada komputer anda."
    )

    # PILIHAN MOD
    mode = st.radio(
        "Pilih Mod Akses:",
        ["📂 Pengguna Ulangan (Buka Vault Terenkripsi .mysg)", "🆕 Pengguna Baru / Kemaskini Profil Manual"],
        horizontal=True
    )

    st.markdown("---")

    # -------------------------------------------------------------------
    # MOD 1: PENGGUNA ULANGAN (DECRYPT VAULT)
    # -------------------------------------------------------------------
    if mode == "📂 Pengguna Ulangan (Buka Vault Terenkripsi .mysg)":
        st.markdown("### 🔓 Buka Fail Vault Terenkripsi")
        uploaded_vault = st.file_uploader("Muat naik fail Vault Sekolah (.mysg / .json):", type=["mysg", "json", "vault"])
        passphrase = st.text_input("Masukkan Kata Laluan / Kunci Rahsia Vault:", type="password")

        if st.button("🔓 Dekrip & Buka Data Sekolah", type="primary", use_container_width=True):
            if not uploaded_vault:
                st.error("⚠️ Sila muat naik fail vault terlebih dahulu.")
            elif not passphrase:
                st.error("⚠️ Sila masukkan kata laluan kunci rahsia vault.")
            else:
                try:
                    encrypted_bytes = uploaded_vault.read()
                    payload = decrypt_payload(encrypted_bytes, passphrase)

                    # 1. Simpan semula Maklumat Sekolah
                    if 'school_info' in payload:
                        st.session_state.school_info = payload['school_info']
                    
                    # 2. Simpan & Hitung Semula Data Staf
                    if 'staff_df_dict' in payload and payload['staff_df_dict']:
                        df_raw = pd.DataFrame.from_dict(payload['staff_df_dict'])
                        
                        # Dapatkan jenis sekolah dari profil
                        jenis_sekolah = st.session_state.school_info.get('jenis_sekolah', 'Sekolah Rendah')
                        
                        # Hitung semula beban kerja menggunakan engine mysg_core
                        df_processed = calculate_workload_df(df_raw, jenis_sekolah)
                        st.session_state.staff_df = df_processed
                        
                        st.success(f"✅ Vault berjaya didekrip! {len(df_processed)} rekod staf dan profil sekolah telah dimuatkan.")
                    else:
                        st.warning("⚠️ Vault didekrip tetapi tiada rekod data staf ditemui di dalamnya.")

                    # Lompati ke Langkah 3 secara automatik
                    st.session_state.current_step = 3
                    st.rerun()

                except Exception as e:
                    st.error(f"❌ Kata laluan salah atau fail vault telah rosak / diubah suai! (Detail: {str(e)})")

    # -------------------------------------------------------------------
    # MOD 2: PENGGUNA BARU / INPUT PROFIL MANUAL
    # -------------------------------------------------------------------
    else:
        st.markdown("### 🏫 Maklumat Profil Sekolah")
        
        info = st.session_state.get('school_info', {})

        col1, col2 = st.columns(2)
        with col1:
            kod_sekolah = st.text_input("Kod Sekolah:", value=info.get('kod_sekolah', 'XBA2004'))
            nama_sekolah = st.text_input("Nama Sekolah:", value=info.get('nama_sekolah', 'SEKOLAH KEBANGSAAN BANDAR SANDAKAN'))
            jenis_sekolah = st.selectbox("Jenis Sekolah:", ["Sekolah Rendah", "Sekolah Menengah"], index=0 if info.get('jenis_sekolah') == "Sekolah Rendah" else 1)
            nama_gb = st.text_input("Nama Pengetua / Guru Besar:", value=info.get('nama_gb', 'SAZAHLIE BIN SAPAR'))

        with col2:
            alamat_sekolah = st.text_area("Alamat Sekolah:", value=info.get('alamat_sekolah', 'W.D.T. No. 297, 90009, Sandakan, SABAH, MALAYSIA'), height=100)
            no_tel = st.text_input("No. Telefon:", value=info.get('no_telefon', '089-612673'))
            no_fax = str(info.get('no_faks', '089-612673'))
            emel_rasmi = st.text_input("Emel Rasmi Sekolah:", value=info.get('emel_rasmi', 'xba2004@moe.edu.my'))
            tahun_sesi = st.text_input("Tahun Sesi Persekolahan:", value=info.get('tahun_sesi', '2026/2027'))

        st.markdown("#### 🖼️ Lencana Sekolah (Opsional)")
        logo_file = st.file_uploader("Muat Naik Lencana Sekolah (PNG/JPG):", type=["png", "jpg", "jpeg"])
        
        logo_b64 = info.get('logo_base64', '')
        if logo_file is not None:
            bytes_data = logo_file.read()
            ext = logo_file.name.split('.')[-1].lower()
            logo_b64 = f"data:image/{ext};base64,{base64.b64encode(bytes_data).decode('utf-8')}"
            st.success("✅ Lencana sekolah berjaya dimuat naik!")

        # BUTANG SIMPAN SESSION
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("💾 Simpan Profil & Teruskan", type="primary", use_container_width=True):
                st.session_state.school_info = {
                    'kod_sekolah': kod_sekolah,
                    'nama_sekolah': nama_sekolah,
                    'jenis_sekolah': jenis_sekolah,
                    'nama_gb': nama_gb,
                    'alamat_sekolah': alamat_sekolah,
                    'no_telefon': no_tel,
                    'no_faks': no_fax,
                    'emel_rasmi': emel_rasmi,
                    'tahun_sesi': tahun_sesi,
                    'logo_base64': logo_b64
                }
                st.success("✅ Maklumat profil disimpan dalam ingatan sementara.")
                st.session_state.current_step = 3
                st.rerun()

        # SECTION CIPTA / EKSPOR VAULT
        st.markdown("---")
        st.markdown("### 🔐 Ekspor / Cipta Fail Vault Terenkripsi (.mysg)")
        st.caption("Ekspor keseluruhan Profil Sekolah & Data Staf (jika ada) ke dalam fail terenkripsi AES-256 untuk kegunaan akan datang.")

        save_passphrase = st.text_input("Tetapkan Kata Laluan Untuk Enkripsi Vault:", type="password", key="new_vault_pass")

        if st.button("🔒 Cipta & Muat Turun Fail Vault Terenkripsi", use_container_width=True):
            if not save_passphrase or len(save_passphrase) < 4:
                st.warning("⚠️ Sila tetapkan kata laluan sekurang-kurangnya 4 aksara.")
            else:
                try:
                    school_info_payload = {
                        'kod_sekolah': kod_sekolah,
                        'nama_sekolah': nama_sekolah,
                        'jenis_sekolah': jenis_sekolah,
                        'nama_gb': nama_gb,
                        'alamat_sekolah': alamat_sekolah,
                        'no_telefon': no_tel,
                        'no_faks': no_fax,
                        'emel_rasmi': emel_rasmi,
                        'tahun_sesi': tahun_sesi,
                        'logo_base64': logo_b64
                    }
                    
                    df_staff = st.session_state.get('staff_df', None)
                    staff_dict = df_staff.to_dict(orient='records') if (df_staff is not None and not df_staff.empty) else []

                    full_payload = {
                        'school_info': school_info_payload,
                        'staff_df_dict': staff_dict
                    }

                    encrypted_vault_bytes = encrypt_payload(full_payload, save_passphrase)

                    st.download_button(
                        label="📥 Muat Turun Fail Vault (.mysg)",
                        data=encrypted_vault_bytes,
                        file_name=f"Vault_MySG_{kod_sekolah}.mysg",
                        mime="application/octet-stream",
                        type="primary",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"❌ Ralat semasa mencipta vault: {str(e)}")

    render_footer()