"""
========================================================================
SISTEM PENGURUSAN & PENGIRAAN BEBAN KERJA KAKITANGAN SEKOLAH (MYSG KPM)
PAGE 2 - PENDAFTARAN PROFIL SEKOLAH (PURE ZERO-STORAGE & CLEAN FORM)
========================================================================
"""

import streamlit as st
import base64
from footer_component import render_footer

def render_page_2():
    st.title("🏫 Pendaftaran & Tetapan Profil Sekolah")
    st.caption("Lengkapkan maklumat rasmi sekolah untuk dipaparkan pada Kepala Surat Lantikan (Header KPM), Laporan, dan Penyata Beban Kerja.")
    st.markdown("<br>", unsafe_allow_html=True)

    # Ambil maklumat dari Session State sahaja (tiada lagi pembacaan fail .json tempatan)
    info_sec = st.session_state.get('school_info', {})

    with st.form("form_profil_sekolah"):
        st.markdown("### 🏛️ **Maklumat Sekolah**")
        col_s1, col_s2 = st.columns(2)
        
        # SUSUNAN SEBELAH KIRI (MEDAN KOSONG)
        with col_s1:
            nama_sek = st.text_input(
                "Nama Penuh Sekolah *", 
                value=info_sec.get('nama_sekolah', ''),
                placeholder="Contoh: SEKOLAH KEBANGSAAN BANDAR SANDAKAN"
            )
            kod_sek = st.text_input(
                "Kod Sekolah *", 
                value=info_sec.get('kod_sekolah', ''),
                placeholder="Contoh: XBA2004"
            )
            alamat_1 = st.text_input(
                "Alamat Baris 1 (Peti Surat / Jalan) *", 
                value=info_sec.get('alamat_1', ''),
                placeholder="Contoh: W.D.T. No. 297"
            )
            alamat_2 = st.text_input(
                "Alamat Baris 2 (Poskod & Daerah) *", 
                value=info_sec.get('alamat_2', ''),
                placeholder="Contoh: 90009, Sandakan"
            )
            negeri_negara = st.text_input(
                "Negeri & Negara *", 
                value=info_sec.get('negeri_negara', ''),
                placeholder="Contoh: SABAH, MALAYSIA"
            )
            no_tel = st.text_input(
                "No. Telefon *", 
                value=info_sec.get('no_telefon', ''),
                placeholder="Contoh: 089-612673"
            )
            no_fax = st.text_input(
                "No. Faks", 
                value=info_sec.get('no_faks', ''),
                placeholder="Contoh: 089-612673"
            )
            emel_rasmi = st.text_input(
                "Emel *", 
                value=info_sec.get('emel_rasmi', ''),
                placeholder="Contoh: xba2004@moe.edu.my"
            )

        # SUSUNAN SEBELAH KANAN
        with col_s2:
            jenis_sek = st.selectbox(
                "Peringkat Institusi *", 
                options=["Sekolah Rendah", "Sekolah Menengah"],
                index=1 if "Menengah" in str(info_sec.get('jenis_sekolah', '')) else 0
            )
            
            sesi_opts = ["2027", "2028", "2029", "2030"]
            curr_sesi = str(info_sec.get('tahun_sesi', '2027'))
            sesi_index = sesi_opts.index(curr_sesi) if curr_sesi in sesi_opts else 0

            tahun_sesi = st.selectbox(
                "Sesi Persekolahan *", 
                options=sesi_opts,
                index=sesi_index
            )
            nama_gb = st.text_input(
                "Nama Pengetua / Guru Besar *", 
                value=info_sec.get('nama_gb', ''),
                placeholder="Contoh: SAZAHLIE BIN SAPAR"
            )
            admin_pin = st.text_input(
                "Tetapan PIN Keselamatan Pentadbir *", 
                value=info_sec.get('admin_pin', '1234'),
                type="password",
                help="PIN ini diperlukan untuk mendaftar, membuang, atau merombak tugas kakitangan."
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("🖼️ **Muat Naik Lencana Sekolah (Optional)**")
            uploaded_logo = st.file_uploader(
                "Pilih fail imej Lencana Sekolah (PNG / JPG / JPEG)", 
                type=['png', 'jpg', 'jpeg'],
                help="Imej ini akan dipaparkan di sebelah kanan Header Surat Lantikan KPM."
            )

            # PRATONTON LENCANA
            existing_logo_b64 = info_sec.get('logo_base64', '')
            if uploaded_logo is not None:
                st.caption("🔍 **Pratonton Lencana Baharu Dimuat Naik:**")
                st.image(uploaded_logo.getvalue(), width=120)
            elif existing_logo_b64:
                st.caption("🔍 **Pratonton Lencana Sekolah Sedia Ada:**")
                st.markdown(f'<img src="{existing_logo_b64}" style="max-height:100px; max-width:120px; object-fit:contain; border:1px solid #cbd5e1; border-radius:6px; padding:4px; background-color:#ffffff;">', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        btn_submit_profile = st.form_submit_button("💾 Sahkan & Simpan Profil Sekolah", type="primary", use_container_width=True)

        if btn_submit_profile:
            if not nama_sek.strip() or not kod_sek.strip() or not nama_gb.strip():
                st.error("❌ Sila lengkapkan maklumat bertanda (*) iaitu Nama Sekolah, Kod Sekolah, dan Nama Pengetua/Guru Besar.")
            else:
                logo_b64 = existing_logo_b64
                if uploaded_logo is not None:
                    try:
                        bytes_data = uploaded_logo.read()
                        encoded = base64.b64encode(bytes_data).decode('utf-8')
                        mime = "png" if uploaded_logo.name.lower().endswith('.png') else "jpeg"
                        logo_b64 = f"data:image/{mime};base64,{encoded}"
                    except Exception:
                        pass

                alamat_penuh = f"{alamat_1}, {alamat_2}, {negeri_negara}"

                updated_info = {
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

                st.session_state['school_info'] = updated_info
                st.success("✅ Profil sekolah berjaya disimpan!")
                st.session_state.current_step = 3
                st.rerun()
