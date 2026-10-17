"""
========================================================================
MYSG KPM: SISTEM PENGURUSAN & ANALISIS BEBAN KERJA
PAGE 1 - LANDING PAGE ELEGAN & INTEGRASI PENGGUNA BARU (PROFIL + CSV)
========================================================================
"""

import streamlit as st
import json
import base64
import os
import re
import pandas as pd
from crypto_vault import encrypt_payload, decrypt_payload
from mysg_core import calculate_workload_df

def sanitize_dataframe_text(df):
    """Fungsi keselamatan ICT: Membersihkan sebarang tag HTML / skrip berbahaya pada data."""
    if df is not None and not df.empty:
        # Bersihkan lajur 'Nama'
        if 'Nama' in df.columns:
            df['Nama'] = df['Nama'].apply(lambda x: re.sub(r'<[^>]*>', '', str(x)) if pd.notna(x) else x)
        
        # Bersihkan lajur-lajur teks penting yang lain
        for col in df.columns:
            if col.startswith(('Subjek_', 'Kelas_', 'Detail_')):
                df[col] = df[col].apply(lambda x: re.sub(r'<[^>]*>', '', str(x)) if pd.notna(x) else x)
    return df

def generate_106_col_template_df():
    """
    Menjana DataFrame templat standard 106 lajur mengikut ketetapan Dataset_KPM_Terlaras_butir_15.
    """
    cols = ['Nama', 'No_KP', 'Kumpulan', 'Gred', 'Jawatan']

    for i in range(1, 12):
        cols.extend([f'Subjek_{i}', f'Kelas_{i}', f'Waktu_{i}'])
    for i in range(12, 16):
        cols.extend([f'Subjek_{i}', f'Waktu_{i}'])

    for i in range(1, 16):
        cols.extend([f'Kod_P_{i}', f'Detail_P_{i}'])

    for i in range(1, 16):
        cols.extend([f'Kod_J_{i}', f'Detail_J_{i}'])

    row1 = {c: '' for c in cols}
    row1.update({
        'Nama': 'AHMAD BIN MOHAMED',
        'No_KP': '850101125543',
        'Kumpulan': 'GURU',
        'Gred': 'DG44',
        'Jawatan': 'GURU AKADEMIK BIASA',
        'Subjek_1': 'BAHASA MELAYU', 'Kelas_1': '6 BESTARI', 'Waktu_1': 10,
        'Subjek_2': 'SEJARAH', 'Kelas_2': '5 CEKAL', 'Waktu_2': 6,
        'Kod_P_1': 'P01', 'Detail_P_1': 'GURU KELAS / GURU TINGKATAN',
        'Kod_J_1': 'J01', 'Detail_J_1': 'AJK PENGURUSAN MAKLUMAT SEKOLAH (JPMS)'
    })

    row2 = {c: '' for c in cols}
    row2.update({
        'Nama': 'SITI AMINAH BINTI HASSAN',
        'No_KP': '900215125224',
        'Kumpulan': 'GURU',
        'Gred': 'DG41',
        'Jawatan': 'GURU PENOLONG',
        'Subjek_1': 'MATEMATIK', 'Kelas_1': '4 USHAWAN', 'Waktu_1': 12,
        'Subjek_2': 'SAINS', 'Kelas_2': '4 USHAWAN', 'Waktu_2': 8,
        'Kod_P_1': 'P03', 'Detail_P_1': 'GURU SPBT',
        'Kod_J_1': 'J02', 'Detail_J_1': 'AJK HAL EHWAL MURID (HEM)'
    })

    return pd.DataFrame([row1, row2], columns=cols)


def render_page_1():
    # -------------------------------------------------------------------
    # STYLESHEET KHAS DENGAN HIERARKI TIPOGRAFI SERAGAM
    # -------------------------------------------------------------------
    st.markdown(
        """
        <style>
            .main-title {
                font-size: 24px !important;
                font-weight: 800 !important;
                color: #ffffff !important;
                margin: 0 !important;
                line-height: 1.3 !important;
                letter-spacing: -0.3px !important;
            }
            .section-header {
                font-size: 20px !important;
                font-weight: 700 !important;
                color: #0f172a !important;
                margin-bottom: 12px !important;
                letter-spacing: -0.2px !important;
            }
            .card-title {
                font-size: 16px !important;
                font-weight: 700 !important;
                color: #1e293b !important;
                margin: 0 0 6px 0 !important;
            }
            .body-text {
                font-size: 13.5px !important;
                font-weight: 400 !important;
                color: #475569 !important;
                line-height: 1.6 !important;
            }
            .body-text-light {
                font-size: 13.5px !important;
                font-weight: 400 !important;
                color: #dbeafe !important;
                line-height: 1.6 !important;
            }
            .caption-text {
                font-size: 12px !important;
                font-weight: 400 !important;
                color: #64748b !important;
            }
            .badge-tag {
                background-color: rgba(255, 255, 255, 0.2);
                color: #ffffff;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 0.5px;
                text-transform: uppercase;
                display: inline-block;
                margin-bottom: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # -------------------------------------------------------------------
    # 1. BANNER HERO ELEGAN
    # -------------------------------------------------------------------
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 50%, #1d4ed8 100%);
            padding: 30px 36px;
            border-radius: 16px;
            color: #ffffff;
            margin-bottom: 24px;
            box-shadow: 0 10px 25px -5px rgba(30, 58, 138, 0.25);
            border: 1px solid rgba(255, 255, 255, 0.1);
        ">
            <div class="badge-tag">
                🚀 PEMACU TRANSFORMASI PENTADBIRAN SEKOLAH
            </div>
            <h1 class="main-title">
                Memudah Cara Perancangan, Memperkasa Kepimpinan Berasaskan Data
            </h1>
            <p class="body-text-light" style="margin-top: 10px; max-width: 1000px;">
                Selamat datang ke <b>MySG KPM: Sistem Pengurusan & Analisis Beban Kerja</b>. Solusi pintar yang direka khas untuk membantu Pengetua, Guru Besar, dan Barisan Pentadbir merancang agihan tugas yang seimbang, telus, dan saksama demi kesejahteraan wawasan sekolah.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # -------------------------------------------------------------------
    # 2. KAD MATLAMAT TERAS
    # -------------------------------------------------------------------
    col_k1, col_k2, col_k3 = st.columns(3)

    with col_k1:
        st.markdown(
            """
            <div style="background: #ffffff; border: 1px solid #e2e8f0; border-top: 4px solid #2563eb; border-radius: 12px; padding: 20px; height: 100%; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);">
                <div style="font-size: 24px; margin-bottom: 8px;">🎯</div>
                <h3 class="card-title">Keseimbangan Saksama</h3>
                <p class="body-text">
                    Memastikan agihan Jawatan Berportfolio Hakiki (HR/HM), Jadual PdP, Jawatan Tanpa Portfolio (P01–P15), dan Jawatankuasa (J01–J15) dihitung secara telus.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_k2:
        st.markdown(
            """
            <div style="background: #ffffff; border: 1px solid #e2e8f0; border-top: 4px solid #0284c7; border-radius: 12px; padding: 20px; height: 100%; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);">
                <div style="font-size: 24px; margin-bottom: 8px;">📊</div>
                <h3 class="card-title">Keputusan Berfakta</h3>
                <p class="body-text">
                    Menjana analisis graf, laporan ringkasan berkategori, serta penyata individu dan surat lantikan secara automatik bagi sokongan Dialog Prestasi dan PBPPP.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_k3:
        st.markdown(
            """
            <div style="background: #ffffff; border: 1px solid #e2e8f0; border-top: 4px solid #059669; border-radius: 12px; padding: 20px; height: 100%; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);">
                <div style="font-size: 24px; margin-bottom: 8px;">⚡</div>
                <h3 class="card-title">Kecepatan Operasi</h3>
                <p class="body-text">
                    Mengurangkan masa perancangan pentadbiran daripada beberapa minggu kepada beberapa klik sahaja, memberi anda ruang fokus kepada visi sekolah.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------------------------
    # 3. EXPANDER RUJUKAN & TEMPLAT
    # -------------------------------------------------------------------
    with st.expander("📌 **Lihat Peraturan Ketetapan Masa & Templat Dataset MySG KPM (106 Lajur)**", expanded=False):
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.markdown("""
            **⏰ Kadar Masa PdP Standard:**
            * **Sekolah Rendah:** 1 Waktu = 30 Minit (0.5000 Jam)
            * **Sekolah Menengah:** 1 Waktu = 40 Minit (0.6667 Jam)
            
            **💼 Jawatan Berportfolio Hakiki (HR / HM):**
            * Setiap staf memegang **1 Jawatan Hakiki** sahaja (Sekolah Rendah = HR / Sekolah Menengah = HM).
            
            **📂 Jawatan Tanpa Portfolio (P01–P15):**
            * Menyokong 15 butir portfolio (`Kod_P_1`, `Detail_P_1` hingga `Kod_P_15`, `Detail_P_15`).
            """)
        with col_r2:
            st.markdown("""
            **🏛️ Jawatankuasa Rasmi (J01–J15):**
            * Menyokong 15 butir keahlian jawatankuasa (`Kod_J_1`, `Detail_J_1` hingga `Kod_J_15`, `Detail_J_15`).
            
            **📝 Penyelarasan Istilah & Standard:**
            * Format dataset terlaras merangkumi 106 lajur lengkap untuk PdP, Portfolio, dan Jawatankuasa.
            """)

        st.markdown("<hr style='margin: 15px 0 10px 0;'>", unsafe_allow_html=True)
        st.markdown("<h4 class='card-title'>📥 Muat Turun Templat CSV Dataset MySG KPM Terlaras (106 Lajur)</h4>", unsafe_allow_html=True)
        st.markdown("<p class='caption-text'>Templat ini disediakan mengikut ketetapan format <code>Dataset_KPM_Terlaras_butir_15</code> untuk persediaan data staf sekolah anda.</p>", unsafe_allow_html=True)

        df_template_106 = generate_106_col_template_df()
        csv_bytes_106 = df_template_106.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="📄 Muat Turun Templat CSV Rasmi MySG (Dataset Terlaras 106 Lajur)",
            data=csv_bytes_106,
            file_name="Dataset_KPM_Terlaras_butir_15_Templat.csv",
            mime="text/csv",
            type="primary",
            use_container_width=True
        )

    # -------------------------------------------------------------------
    # 4. NOTA KESELAMATAN DATA (PDPA) & PENAFIAN LIABILITI
    # -------------------------------------------------------------------
    with st.expander("🛡️ **Nota Keselamatan Data Peribadi (PDPA) & Penafian Liabiliti**", expanded=False):
        col_sec1, col_sec2 = st.columns(2)
        with col_sec1:
            st.markdown("""
            🔒 **Perlindungan Data Peribadi (PDPA & Zero-Server-Storage):**
            * **Tiada Pangkalan Data Pelayan:** Data sekolah dan maklumat peribadi staf (Nama, No. KP, Gred) **TIDAK DISIMPAN** pada pelayan awam cloud.
            * **Enkripsi AES-256:** Fail *Vault* (`.mysg`) dilindungi sepenuhnya dengan teknologi enkripsi gred tentera AES-256.
            * **Pembersihan Memori:** Memori sementara (*session state*) dipadamkan secara automatik apabila anda menekan butang **Keluar Sistem**.
            """)
        with col_sec2:
            st.markdown("""
            ⚖️ **Penafian Liabiliti & Inisiatif Bebas:**
            * **Alat Bantu Pengurusan:** Perisian ini dibangunkan secara peribadi sebagai alat pemudah cara pentadbiran sekolah untuk pengiraan beban kerja dan penjanaan surat lantikan internal.
            * **Bukan Aplikasi Rasmi KPM:** Perisian ini **TIDAK TERLIBAT ATAU DIWAKILI SECARA RASMI** oleh Kementerian Pendidikan Malaysia (KPM).
            * **Autonomi Sekolah:** Pihak pengurusan sekolah bertanggungjawab sepenuhnya ke atas ketepatan data yang dimasukkan.
            """)

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------------------------
    # 5. MODUL STORAN VAULT TERENKRIPSI & PEMILIHAN MOD
    # -------------------------------------------------------------------
    st.markdown("<h2 class='section-header'>🔑 Modul Storan Selamat (Zero-Server-Storage)</h2>", unsafe_allow_html=True)
    st.info(
        "Sistem ini mematuhi Akta Perlindungan Data Peribadi (PDPA). "
        "Tiada data disimpan pada pelayan. Anda boleh menyimpan atau membuka vault terenkripsi (.mysg) secara terus pada komputer anda."
    )

    mode = st.radio(
        "Pilih Mod Akses:",
        ["📂 Pengguna Ulangan (Buka Vault Terenkripsi .mysg)", "🆕 Pengguna Baru / Kemaskini Profil Manual"],
        horizontal=True,
        key="p1_mode_select"
    )

    st.markdown("---")

    # -------------------------------------------------------------------
    # MOD 1: PENGGUNA ULANGAN
    # -------------------------------------------------------------------
    if mode == "📂 Pengguna Ulangan (Buka Vault Terenkripsi .mysg)":
        st.markdown("<h3 class='card-title' style='font-size: 18px !important;'>🔓 Buka Fail Vault Terenkripsi</h3>", unsafe_allow_html=True)
        uploaded_vault = st.file_uploader("Muat naik fail Vault Sekolah (.mysg / .json):", type=["mysg", "json", "vault"], key="p1_upload_vault")
        passphrase = st.text_input("Masukkan Kata Laluan / Kunci Rahsia Vault:", type="password", key="p1_passphrase")

        if st.button("🔓 Dekrip & Buka Data Sekolah", type="primary", use_container_width=True, key="p1_btn_decrypt"):
            if not uploaded_vault:
                st.error("⚠️ Sila muat naik fail vault terlebih dahulu.")
            elif not passphrase:
                st.error("⚠️ Sila masukkan kata laluan kunci rahsia vault.")
            else:
                try:
                    encrypted_bytes = uploaded_vault.read()
                    payload = decrypt_payload(encrypted_bytes, passphrase)

                    if 'school_info' in payload:
                        st.session_state.school_info = payload['school_info']
                    
                    if 'audit_log' in payload:
                        st.session_state.audit_log = payload['audit_log']
                    else:
                        st.session_state.audit_log = []
                    
                    if 'staff_df_dict' in payload and payload['staff_df_dict']:
                        df_raw = pd.DataFrame.from_dict(payload['staff_df_dict'])
                        # Laksanakan proses Sanitasi
                        df_raw = sanitize_dataframe_text(df_raw)
                        
                        jenis_sekolah = st.session_state.get('school_info', {}).get('jenis_sekolah', 'Sekolah Rendah')
                        df_processed = calculate_workload_df(df_raw, jenis_sekolah)
                        st.session_state.staff_df = df_processed
                        st.success(f"✅ Vault berjaya didekrip! {len(df_processed)} rekod staf dan profil sekolah telah dimuatkan.")
                    else:
                        st.warning("⚠️ Vault didekrip tetapi tiada rekod data staf ditemui.")

                    st.session_state.current_step = 3
                    st.rerun()

                except Exception as e:
                    st.error(f"❌ Kata laluan salah atau fail vault telah rosak / diubah suai! ({str(e)})")

    # -------------------------------------------------------------------
    # MOD 2: PENGGUNA BARU (PROFIL SEKOLAH + PRATONTON LENCANA AUTOMATIK + CSV)
    # -------------------------------------------------------------------
    else:
        st.markdown("<h3 class='card-title' style='font-size: 18px !important;'>🏛️ Pendaftaran Profil Sekolah & Muat Naik CSV Staf</h3>", unsafe_allow_html=True)
        st.caption("Lengkapkan maklumat profil sekolah dan muat naik fail CSV staf secara berpusat di bawah.")
        
        info_sec = st.session_state.get('school_info', {})

        col_s1, col_s2 = st.columns(2)
        
        with col_s1:
            nama_sek = st.text_input("Nama Penuh Sekolah *", value=info_sec.get('nama_sekolah', ''), placeholder="Contoh: SEKOLAH KEBANGSAAN BANDAR SANDAKAN", key="input_nama_sek")
            kod_sek = st.text_input("Kod Sekolah *", value=info_sec.get('kod_sekolah', ''), placeholder="Contoh: XBA2004", key="input_kod_sek")
            alamat_1 = st.text_input("Alamat Baris 1 (Peti Surat / Jalan) *", value=info_sec.get('alamat_1', ''), placeholder="Contoh: W.D.T. No. 297", key="input_alamat_1")
            alamat_2 = st.text_input("Alamat Baris 2 (Poskod & Daerah) *", value=info_sec.get('alamat_2', ''), placeholder="Contoh: 90009, Sandakan", key="input_alamat_2")
            negeri_negara = st.text_input("Negeri & Negara *", value=info_sec.get('negeri_negara', ''), placeholder="Contoh: SABAH, MALAYSIA", key="input_negeri")
            no_tel = st.text_input("No. Telefon *", value=info_sec.get('no_telefon', ''), placeholder="Contoh: 089-612673", key="input_no_tel")
            no_fax = st.text_input("No. Faks", value=info_sec.get('no_faks', ''), placeholder="Contoh: 089-612673", key="input_no_fax")
            emel_rasmi = st.text_input("Emel *", value=info_sec.get('emel_rasmi', ''), placeholder="Contoh: xba2004@moe.edu.my", key="input_emel")

        with col_s2:
            jenis_sek = st.selectbox(
                "Peringkat Institusi *", 
                options=["Sekolah Rendah", "Sekolah Menengah"],
                index=1 if "Menengah" in str(info_sec.get('jenis_sekolah', '')) else 0,
                key="select_jenis_sek"
            )
            
            sesi_opts = ["2027", "2028", "2029", "2030"]
            curr_sesi = str(info_sec.get('tahun_sesi', '2027'))
            sesi_index = sesi_opts.index(curr_sesi) if curr_sesi in sesi_opts else 0

            tahun_sesi = st.selectbox("Sesi Persekolahan *", options=sesi_opts, index=sesi_index, key="select_tahun_sesi")
            nama_gb = st.text_input("Nama Pengetua / Guru Besar *", value=info_sec.get('nama_gb', ''), placeholder="Contoh: SAZAHLIE BIN SAPAR", key="input_nama_gb")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("🖼️ **Muat Naik Lencana Sekolah (Optional)**")
            uploaded_logo = st.file_uploader("Pilih imej Lencana Sekolah (PNG / JPG)", type=['png', 'jpg', 'jpeg'], key="p1_upload_logo_btn")

            # ---------------------------------------------------------------
            # PRATONTON LENCANA AUTOMATIK (REAL-TIME LIVE PREVIEW)
            # ---------------------------------------------------------------
            if uploaded_logo is not None:
                st.caption("🔍 **Pratonton Lencana Sekolah Terpilih:**")
                st.image(uploaded_logo, width=120)
            elif info_sec.get('logo_base64', ''):
                st.caption("🔍 **Pratonton Lencana Sekolah Sedia Ada:**")
                st.image(info_sec.get('logo_base64'), width=120)

        st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
        st.markdown("<h4 class='card-title'>📊 Muat Naik Fail CSV Staf Sekolah (Standard MySG 106 Lajur)</h4>", unsafe_allow_html=True)
        uploaded_csv = st.file_uploader("Pilih fail CSV Staf yang telah diisi mengikut templat:", type=['csv'], key="p1_upload_csv_btn")

        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("💾 Sahkan Profil & Proses Data Staf", type="primary", use_container_width=True, key="btn_confirm_process_new"):
            if not nama_sek.strip() or not kod_sek.strip() or not nama_gb.strip():
                st.error("❌ Sila lengkapkan maklumat bertanda (*) iaitu Nama Sekolah, Kod Sekolah, dan Nama Pengetua/Guru Besar.")
            elif uploaded_csv is None:
                st.error("⚠️ Sila muat naik fail CSV Staf untuk meneruskan pengiraan beban kerja.")
            else:
                try:
                    # 1. Simpan Maklumat Profil Sekolah ke Session
                    existing_logo_b64 = info_sec.get('logo_base64', '')
                    logo_b64 = existing_logo_b64
                    if uploaded_logo is not None:
                        bytes_data = uploaded_logo.read()
                        encoded = base64.b64encode(bytes_data).decode('utf-8')
                        mime = "png" if uploaded_logo.name.lower().endswith('.png') else "jpeg"
                        logo_b64 = f"data:image/{mime};base64,{encoded}"

                    alamat_penuh = f"{alamat_1}, {alamat_2}, {negeri_negara}"

                    st.session_state['school_info'] = {
                        'nama_sekolah': nama_sek.upper().strip(),
                        'kod_sekolah': kod_sek.upper().strip(),
                        'jenis_sekolah': jenis_sek,
                        'alamat_1': alamat_1.strip(),
                        'alamat_2': alamat_2.strip(),
                        'negeri_negara': negeri_negara.upper().strip(),
                        'alamat_sekolah': alamat_penuh,
                        'no_telefon': no_tel.strip(),
                        'no_faks': no_fax.strip(),
                        'emel_rasmi': emel_rasmi.strip(),
                        'nama_gb': nama_gb.upper().strip(),
                        'tahun_sesi': tahun_sesi,
                        'logo_base64': logo_b64
                    }

                    # 2. Baca dan Hitung Beban Kerja CSV Staf
                    df_raw = pd.read_csv(uploaded_csv)
                    
                    # Laksanakan proses Sanitasi
                    df_raw = sanitize_dataframe_text(df_raw)
                    
                    df_processed = calculate_workload_df(df_raw, jenis_sek)
                    st.session_state.staff_df = df_processed

                    st.success(f"✅ Profil sekolah disahkan & {len(df_processed)} rekod staf berjaya diproses! Beralih ke Dashboard Utama...")
                    st.session_state.current_step = 3
                    st.rerun()

                except Exception as e:
                    st.error(f"❌ Ralat memproses fail CSV: {str(e)}")