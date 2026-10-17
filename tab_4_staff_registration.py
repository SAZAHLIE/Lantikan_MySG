"""
========================================================================
MYSG KPM: SISTEM PENGURUSAN & ANALISIS BEBAN KERJA
MODULE: TAB 4 - PENDAFTARAN KAKITANGAN MASUK / KELUAR / PERTUKARAN
========================================================================
"""

import streamlit as st
import pandas as pd
import time
import datetime
from mysg_core import (
    calculate_workload_df, 
    MYSG_PORTFOLIO_H_SR, 
    MYSG_PORTFOLIO_H_SM,
    MYSG_PORTFOLIO_P,
    MYSG_JAWATANKUASA_J
)

# SENARAI SUBJEK RASMI KPM MENGIKUT PERINGKAT
SUBJEK_KPM_SR = [
    "", "Bahasa Melayu", "Bahasa Inggeris", "Matematik", "Sains",
    "Pendidikan Islam", "Pend. Agama Islam", "Pendidikan Moral", 
    "Bahasa Arab", "Bahasa Cina", "Bahasa Tamil",
    "Pend. Jasmani Pend. Kesihatan", "Pendidikan Jasmani", "Pendidikan Kesihatan",
    "Pend. Seni Visual", "Pendidikan Seni Visual", "Pend. Muzik", "Pendidikan Muzik",
    "Sejarah", "Reka Bentuk Teknologi", "Reka Bentuk & Teknologi (RBT)",
    "TASMIK", "Al-Quran", "PRA Sekolah", "Lain-Lain Subjek"
]

SUBJEK_KPM_SM = [
    "", "Bahasa Melayu", "Bahasa Inggeris", "Matematik", "Matematik Tambahan",
    "Sains", "Fizik", "Kimia", "Biologi",
    "Pendidikan Islam", "Pendidikan Moral", "Sejarah", "Geografi",
    "Reka Bentuk & Teknologi (RBT)", "Asas Sains Komputer (ASK)", "Sains Komputer",
    "Prinsip Perakaunan", "Ekonomi", "Perniagaan",
    "Pend. Jasmani Pend. Kesihatan", "Pendidikan Seni Visual", "Pendidikan Muzik",
    "Bahasa Arab", "Bahasa Cina", "Bahasa Tamil",
    "Tasawwur Islam", "Pend. Al-Quran & Al-Sunnah", "Pend. Syariah Islamiah",
    "Lain-Lain Subjek"
]

def render_tab_4(school_info):
    """Menjana kandungan Tab 4: Pendaftaran Kakitangan Masuk / Keluar mengikut Dropdown Subjek KPM & Notifikasi Serta-Merta."""
    st.subheader("🔄 Pendaftaran Kakitangan Masuk / Keluar / Pertukaran")
    st.caption("Urus pergerakan kakitangan sekolah secara langsung mengikut format skema dataset terlaras. PIN Pengesahan diperlukan.")

    df_staff = st.session_state.get('staff_df', pd.DataFrame())
    jenis_sek = school_info.get('jenis_sekolah', 'Sekolah Rendah')
    is_sm = "Menengah" in str(jenis_sek)

    # Tetapan pilihan subjek mengikut peringkat sekolah
    list_subjek_kpm = SUBJEK_KPM_SM if is_sm else SUBJEK_KPM_SR

    if 'pdp_batch_count' not in st.session_state:
        st.session_state['pdp_batch_count'] = 5
    if 'p_batch_count' not in st.session_state:
        st.session_state['p_batch_count'] = 5
    if 'j_batch_count' not in st.session_state:
        st.session_state['j_batch_count'] = 5

    sub1, sub2 = st.tabs([
        "➕ Pendaftaran Kakitangan Baharu / Bertukar Masuk", 
        "➖ Pendaftaran Kakitangan Keluar / Bersara"
    ])

    # -------------------------------------------------------------------
    # SUB-TAB 1: DAFTAR KAKITANGAN BAHARU
    # -------------------------------------------------------------------
    with sub1:
        st.markdown("##### 📝 Borang Pendaftaran Kakitangan Baharu")
        st.info("Sila isi maklumat kakitangan baharu di bawah. Anda boleh menambah Subjek PdP, Portfolio (P), dan Jawatankuasa (J).")

        with st.form(key="form_add_staff_dynamic", clear_on_submit=False):
            
            # SEKSYEN 1: PROFIL PEGAWAI & JAWATAN HAKIKI
            st.markdown("#### 1. Maklumat Peribadi & Portfolio Hakiki (Kod H)")
            col_p1, col_p2, col_p3 = st.columns(3)
            with col_p1:
                nama_baharu = st.text_input("Nama Penuh Kakitangan:", placeholder="e.g. AHMAD BIN ABDULLAH")
                no_kp_baharu = st.text_input("No. Kad Pengenalan (Pilihan):", placeholder="e.g. 850101125555")
            with col_p2:
                kumpulan_baharu = st.selectbox("Kumpulan Perkhidmatan:", options=["Guru", "Anggota Kumpulan Pelaksana"])
                gred_baharu = st.text_input("Gred Perkhidmatan:", value="DG41" if kumpulan_baharu == "Guru" else "N19")
            with col_p3:
                if kumpulan_baharu == "Guru":
                    mapping_h = MYSG_PORTFOLIO_H_SM if is_sm else MYSG_PORTFOLIO_H_SR
                    options_jawatan = [f"{k} | {v[0]}" for k, v in mapping_h.items()]
                    jawatan_selected = st.selectbox("Jawatan Hakiki (Kod H):", options=options_jawatan)
                else:
                    options_akp = [
                        "HR24 | Pembantu Tadbir (P/O)",
                        "HR25 | Pembantu Tadbir (Kewangan)",
                        "HR27 | Pembantu Pengurusan Murid",
                        "HR30 | Pembantu Operasi",
                        "HR31 | Pemandu Kenderaan",
                        "HR32 | Pembantu Awam"
                    ]
                    jawatan_selected = st.selectbox("Jawatan Hakiki AKP:", options=options_akp)

            st.markdown("---")

            # SEKSYEN 2: JADUAL PDP (WAKTU DALAM NOMBOR BULAT)
            pdp_inputs = {}
            if kumpulan_baharu == "Guru":
                max_pdp = st.session_state['pdp_batch_count']
                with st.expander(f"📖 2. Perincian Jadual Pengajaran & Pembelajaran (PdP) — (Paparan 1 hingga {max_pdp})", expanded=False):
                    st.caption(f"Pilih Subjek rasmi KPM ({'Sekolah Menengah' if is_sm else 'Sekolah Rendah'}), Kelas, dan Bilangan Waktu (Nombor Bulat sahaja; 1 Waktu = 0.5 Jam).")
                    for i in range(1, max_pdp + 1):
                        c1, c2, c3 = st.columns([2, 1.5, 1])
                        with c1:
                            pdp_inputs[f'Subjek_{i}'] = st.selectbox(f"Subjek {i}:", options=list_subjek_kpm, key=f"dyn_subj_{i}")
                        with c2:
                            pdp_inputs[f'Kelas_{i}'] = st.text_input(f"Kelas {i}:", key=f"dyn_kelas_{i}")
                        with c3:
                            pdp_inputs[f'Waktu_{i}'] = st.number_input(f"Waktu {i}:", min_value=0, step=1, value=0, key=f"dyn_waktu_{i}")

            # SEKSYEN 3: PORTFOLIO TANPA JAWATAN
            p_inputs = {}
            max_p = st.session_state['p_batch_count']
            opts_p = [""] + [f"{k} | {v[0]}" for k, v in MYSG_PORTFOLIO_P.items()]
            with st.expander(f"💼 3. Perincian Portfolio Tanpa Jawatan (Kod P) — (Paparan 1 hingga {max_p})", expanded=False):
                st.caption("Pilih Kod P dan masukkan butiran terperinci (Detail P) sekiranya ada.")
                for i in range(1, max_p + 1):
                    cp1, cp2 = st.columns([2, 2])
                    with cp1:
                        p_inputs[f'Kod_P_{i}'] = st.selectbox(f"Kod P_{i}:", options=opts_p, key=f"dyn_kod_p_{i}")
                    with cp2:
                        p_inputs[f'Detail_P_{i}'] = st.text_input(f"Butiran Detail P_{i}:", key=f"dyn_det_p_{i}")

            # SEKSYEN 4: JAWATANKUASA SEKOLAH
            j_inputs = {}
            max_j = st.session_state['j_batch_count']
            opts_j = [""] + [f"{k} | {v[0]}" for k, v in MYSG_JAWATANKUASA_J.items()]
            with st.expander(f"🏛️ 4. Perincian Jawatankuasa Sekolah (Kod J) — (Paparan 1 hingga {max_j})", expanded=False):
                st.caption("Pilih Kod J dan masukkan butiran terperinci (Detail J) sekiranya ada.")
                for i in range(1, max_j + 1):
                    cj1, cj2 = st.columns([2, 2])
                    with cj1:
                        j_inputs[f'Kod_J_{i}'] = st.selectbox(f"Kod J_{i}:", options=opts_j, key=f"dyn_kod_j_{i}")
                    with cj2:
                        j_inputs[f'Detail_J_{i}'] = st.text_input(f"Butiran Detail J_{i}:", key=f"dyn_det_j_{i}")

            st.markdown("<br>", unsafe_allow_html=True)
            
            # KAWALAN AKSES (RBAC) - PIN PENGESAHAN
            pin_pengesahan_1 = st.text_input("🔑 Masukkan PIN Pengesahan Pentadbir untuk menyimpan:", type="password", key="pin_tambah_staf")
            btn_add = st.form_submit_button("➕ Simpan & Daftarkan Kakitangan Baharu", type="primary", use_container_width=True)

            if btn_add:
                if pin_pengesahan_1 != school_info.get('admin_pin', '1234'):
                    st.error("🔒 PIN Pengesahan salah! Akses ditolak. Hanya pentadbir yang sah dibenarkan mengubah data.")
                elif not nama_baharu.strip():
                    st.toast("⚠️ Sila masukkan Nama Penuh Kakitangan!", icon="⚠️")
                    st.error("⚠️ Sila masukkan Nama Penuh Kakitangan.")
                else:
                    kod_h = jawatan_selected.split(" | ")[0].strip()
                    label_jawatan = jawatan_selected.split(" | ")[1].strip() if " | " in jawatan_selected else jawatan_selected

                    # BINA ENTRI DIKTIONARI BAHARU
                    new_row = {
                        'Nama': nama_baharu.upper().strip(),
                        'No_KP': no_kp_baharu.strip() if no_kp_baharu.strip() else None,
                        'Kumpulan': kumpulan_baharu,
                        'Gred': gred_baharu.upper().strip(),
                        'Jawatan': jawatan_selected if " | " in jawatan_selected else f"{kod_h} | {label_jawatan}",
                        'Kod_H_1': kod_h
                    }

                    # Isi Subjek PdP
                    total_waktu_calc = 0
                    if kumpulan_baharu == "Guru":
                        for i in range(1, 16):
                            s_val = pdp_inputs.get(f'Subjek_{i}', '').strip() if i <= max_pdp else ''
                            k_val = pdp_inputs.get(f'Kelas_{i}', '').strip() if i <= max_pdp else ''
                            w_val = int(pdp_inputs.get(f'Waktu_{i}', 0)) if i <= max_pdp else 0

                            new_row[f'Subjek_{i}'] = s_val if s_val else None
                            new_row[f'Kelas_{i}'] = k_val if k_val else None
                            new_row[f'Waktu_{i}'] = float(w_val) if w_val > 0 else None
                            if s_val and w_val > 0:
                                total_waktu_calc += w_val

                    new_row['JUMLAH_WAKTU_PDP'] = float(total_waktu_calc)

                    # Isi Kod P & Detail P
                    for i in range(1, 16):
                        kp_val = p_inputs.get(f'Kod_P_{i}', '').strip() if i <= max_p else ''
                        dp_val = p_inputs.get(f'Detail_P_{i}', '').strip() if i <= max_p else ''
                        new_row[f'Kod_P_{i}'] = kp_val if kp_val else None
                        new_row[f'Detail_P_{i}'] = dp_val if dp_val else None

                    # Isi Kod J & Detail J
                    for i in range(1, 16):
                        kj_val = j_inputs.get(f'Kod_J_{i}', '').strip() if i <= max_j else ''
                        dj_val = j_inputs.get(f'Detail_J_{i}', '').strip() if i <= max_j else ''
                        new_row[f'Kod_J_{i}'] = kj_val if kj_val else None
                        new_row[f'Detail_J_{i}'] = dj_val if dj_val else None

                    # GABUNGKAN DATA KAKITANGAN INDUK
                    df_new_entry = pd.DataFrame([new_row])
                    if df_staff is not None and not df_staff.empty:
                        df_combined_raw = pd.concat([df_staff, df_new_entry], ignore_index=True)
                    else:
                        df_combined_raw = df_new_entry

                    try:
                        df_recalculated = calculate_workload_df(df_combined_raw, jenis_sek)
                        st.session_state['staff_df'] = df_recalculated
                        st.session_state['data_version'] = int(time.time())
                        
                        # REKOD LOG AKTIVITI
                        if 'audit_log' not in st.session_state:
                            st.session_state['audit_log'] = []
                        st.session_state['audit_log'].append({
                            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "action": "PENDAFTARAN BAHARU",
                            "staff_name": nama_baharu.upper()
                        })
                        
                        # NOTIFIKASI KEPADA PENGGUNA
                        st.toast(f"🎉 Kakitangan {nama_baharu.upper()} berjaya didaftarkan!", icon="✅")
                        st.success(f"✅ Kakitangan **{nama_baharu.upper()}** berjaya didaftarkan ke dalam sistem!")
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.toast("❌ Ralat semasa menyimpan data!", icon="🚨")
                        st.error(f"❌ Ralat memproses data kakitangan: {str(e)}")

        # BUTANG KAWALAN TAMBAH RUANG (DILUAR FORM)
        st.markdown("##### ➕ Tambah Ruang Input Tambahan (Jika Perlu)")
        col_b1, col_b2, col_b3 = st.columns(3)

        with col_b1:
            if st.session_state['pdp_batch_count'] < 15:
                next_pdp = st.session_state['pdp_batch_count'] + 5
                if st.button(f"➕ Buka Ruang PdP ({next_pdp-4} - {next_pdp})", use_container_width=True, key="btn_add_pdp"):
                    st.session_state['pdp_batch_count'] = next_pdp
                    st.toast(f"📖 Ruang PdP ({next_pdp-4} - {next_pdp}) dibuka!", icon="🔓")
                    st.rerun()

        with col_b2:
            if st.session_state['p_batch_count'] < 15:
                next_p = st.session_state['p_batch_count'] + 5
                if st.button(f"➕ Buka Ruang Kod P ({next_p-4} - {next_p})", use_container_width=True, key="btn_add_p"):
                    st.session_state['p_batch_count'] = next_p
                    st.toast(f"💼 Ruang Kod P ({next_p-4} - {next_p}) dibuka!", icon="🔓")
                    st.rerun()

        with col_b3:
            if st.session_state['j_batch_count'] < 15:
                next_j = st.session_state['j_batch_count'] + 5
                if st.button(f"➕ Buka Ruang Kod J ({next_j-4} - {next_j})", use_container_width=True, key="btn_add_j"):
                    st.session_state['j_batch_count'] = next_j
                    st.toast(f"🏛️ Ruang Kod J ({next_j-4} - {next_j}) dibuka!", icon="🔓")
                    st.rerun()

    # -------------------------------------------------------------------
    # SUB-TAB 2: DAFTAR KAKITANGAN KELUAR / BERSARA
    # -------------------------------------------------------------------
    with sub2:
        st.markdown("##### 🗑️ Pengeluaran Rekod Kakitangan (Bertukar / Bersara)")

        if df_staff is not None and not df_staff.empty and 'Nama' in df_staff.columns:
            st.warning("⚠️ **Peringatan:** Tindakan ini akan mengeluarkan rekod kakitangan daripada jadual beban kerja sekolah terkini.")

            col_del_sel, col_del_btn = st.columns([2.5, 1.5])

            with col_del_sel:
                staf_to_remove = st.selectbox(
                    "Pilih Kakitangan untuk Dikeluarkan:", 
                    options=df_staff['Nama'].tolist(), 
                    key="select_staf_remove"
                )

            row_to_remove = df_staff[df_staff['Nama'] == staf_to_remove].iloc[0]
            st.caption(f"📌 **Profil Dipilih:** {row_to_remove.get('Nama')} | {row_to_remove.get('Jawatan')} ({row_to_remove.get('Kumpulan')})")

            with col_del_btn:
                st.markdown("<br>", unsafe_allow_html=True)
                
                # KAWALAN AKSES (RBAC) - PIN PENGESAHAN
                pin_pengesahan_2 = st.text_input("🔑 PIN Pentadbir:", type="password", key="pin_buang_staf")
                
                if st.button("🔴 Pengesahan Keluarkan Kakitangan", type="primary", use_container_width=True, key="btn_confirm_remove_staf"):
                    if pin_pengesahan_2 != school_info.get('admin_pin', '1234'):
                        st.error("🔒 PIN Pengesahan salah! Akses ditolak.")
                    else:
                        df_filtered_raw = df_staff[df_staff['Nama'] != staf_to_remove].reset_index(drop=True)

                        if not df_filtered_raw.empty:
                            df_recalculated = calculate_workload_df(df_filtered_raw, jenis_sek)
                            st.session_state['staff_df'] = df_recalculated
                        else:
                            st.session_state['staff_df'] = pd.DataFrame()

                        st.session_state['data_version'] = int(time.time())
                        
                        # REKOD LOG AKTIVITI
                        if 'audit_log' not in st.session_state:
                            st.session_state['audit_log'] = []
                        st.session_state['audit_log'].append({
                            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "action": "PENGELUARAN REKOD",
                            "staff_name": staf_to_remove
                        })
                        
                        st.toast(f"🗑️ Rekod {staf_to_remove} berjaya dikeluarkan!", icon="🗑️")
                        st.success(f"✅ Rekod kakitangan **{staf_to_remove}** telah berjaya dikeluarkan.")
                        time.sleep(1)
                        st.rerun()
        else:
            st.info("ℹ️ Tiada rekod kakitangan ditemui untuk dikeluarkan.")
