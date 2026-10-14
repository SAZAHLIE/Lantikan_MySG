"""
========================================================================
SISTEM PENGURUSAN & PENGIRAAN BEBAN KERJA KAKITANGAN SEKOLAH (MYSG KPM)
MODULE: PENJANA SURAT LANTIKAN TUGAS RASMI (BEBAS DOUBLE JATA)
========================================================================
"""

import datetime
import os
import base64

def format_tarikh_melayu(d):
    bulan = [
        "", "Januari", "Februari", "Mac", "April", "Mei", "Jun",
        "Julai", "Ogos", "September", "Oktober", "November", "Disember"
    ]
    return f"{d.day} {bulan[d.month]} {d.year}"

def get_local_image_base64(file_path):
    """Membaca fail imej tempatan dan mengembalikannya sebagai string Base64"""
    if os.path.exists(file_path):
        try:
            ext = os.path.splitext(file_path)[1].lower().replace('.', '')
            if ext == 'jpg': ext = 'jpeg'
            with open(file_path, "rb") as image_file:
                encoded = base64.b64encode(image_file.read()).decode('utf-8')
                return f"data:image/{ext};base64,{encoded}"
        except Exception:
            return ""
    return ""

def generate_appointment_letter_html(staf_row, school_info, no_rujukan=""):
    from mysg_core import MYSG_PORTFOLIO_P, MYSG_JAWATANKUASA_J

    # 1. MAKLUMAT SEKOLAH & HEADER
    nama_sekolah = str(school_info.get('nama_sekolah', 'SEKOLAH KEBANGSAAN BANDAR SANDAKAN')).upper()
    alamat_sekolah = str(school_info.get('alamat_sekolah', 'W.D.T. NO. 297, 90009 SANDAKAN, SABAH, MALAYSIA'))
    no_tel = str(school_info.get('no_telefon', '089-612673'))
    no_fax = str(school_info.get('no_faks', '089-612673'))
    emel_rasmi = str(school_info.get('emel_rasmi', 'xba2004@moe.edu.my'))
    nama_gb = str(school_info.get('nama_gb', 'AHMAD BIN MOHD')).upper()
    tahun_sesi = str(school_info.get('tahun_sesi', '2027'))
    logo_base64 = school_info.get('logo_base64', '')

    # 2. BACA JATA NEGARA DARI FOLDER TEMPATAN (KIRI SAHAJA)
    jata_b64 = ""
    possible_files = ["jata.png", "jata.jpg", "JATA_NEGARA.png", "JATA_NEGARA.jpg", "JATA NEGARA.png", "JATA NEGARA.jpg"]
    for fname in possible_files:
        path = os.path.join(os.getcwd(), fname)
        if os.path.exists(path):
            jata_b64 = get_local_image_base64(path)
            break
            
    if not jata_b64:
        # Fallback SVG/Text jika fail jata.png tiada di folder projek
        jata_img_html = '<div style="font-size: 13px; font-weight: bold; color: #1e3a8a;">MALAYSIA</div>'
    else:
        jata_img_html = f'<img src="{jata_b64}" style="height: 68px; width: auto;" alt="Jata Negara">'

    # 3. LENCANA SEKOLAH (KANAN SAHAJA - TANPA FALLBACK JATA NEGARA)
    logo_sek_html = ''
    if logo_base64 and len(logo_base64) > 100:
        logo_sek_html = f'<img src="{logo_base64}" style="max-height: 75px; max-width: 90px; object-fit: contain;" alt="Lencana Sekolah">'

    # 4. MAKLUMAT STAF
    nama_staf = str(staf_row.get('Nama', '')).upper()
    raw_kp = str(staf_row.get('No_KP', '')).strip()
    no_kp = "-" if raw_kp in ["nan", "None", ""] else raw_kp

    tarikh_hari_ini = format_tarikh_melayu(datetime.date.today())

    if not no_rujukan:
        kod_sek = str(school_info.get('kod_sekolah', 'SEK'))
        no_rujukan = f"KP/{kod_sek}/MYSG/{tahun_sesi.split('/')[0]}/01"

    # 5. JAWATAN HAKIKI
    jawatan_val = str(staf_row.get('Jawatan', '')).strip()
    dtl_h = str(staf_row.get('Detail_H_1', '')).strip()
    kod_h = str(staf_row.get('Kod_H_1', '')).strip()
    
    if jawatan_val in ["nan", "None", ""]:
        jawatan_val = dtl_h if dtl_h not in ["nan", "None", ""] else "Guru Akademik Biasa"

    if kod_h and kod_h not in jawatan_val:
        jawatan_full = f"{kod_h} | {jawatan_val}"
    else:
        jawatan_full = jawatan_val

    # 6. SUBJEK PDP
    pdp_cols = [c for c in staf_row.index if c.startswith('Subjek_')]
    pdp_items_html = ""
    sub_count = 1
    for col in pdp_cols:
        idx_num = col.split('_')[1]
        sub_val = str(staf_row.get(f"Subjek_{idx_num}", '')).strip()
        cls_val = str(staf_row.get(f"Kelas_{idx_num}", '')).strip()
        wkt_val = staf_row.get(f"Waktu_{idx_num}", 0)

        if sub_val not in ["nan", "None", ""]:
            try: wkt_num = int(wkt_val)
            except: wkt_num = 0
            cls_str = f", {cls_val}" if cls_val not in ["nan", "None", ""] else ""
            pdp_items_html += f"""
            <div style="margin-left: 20px; margin-top: 2px; font-size: 13px; color: #1e293b;">
                <b>2.1.{sub_count}.</b> Mengajar <b>{sub_val}</b>{cls_str}, ({wkt_num} Waktu)
            </div>
            """
            sub_count += 1

    # 7. PORTFOLIO P
    p_cols = [c for c in staf_row.index if c.startswith('Kod_P_')]
    p_items_html = ""
    p_count = 1
    for col in p_cols:
        idx_num = col.split('_')[2]
        p_kod = str(staf_row.get(f"Kod_P_{idx_num}", '')).strip()
        p_dtl = str(staf_row.get(f"Detail_P_{idx_num}", '')).strip()

        if p_kod not in ["nan", "None", ""]:
            label_p = f"{p_kod} | {MYSG_PORTFOLIO_P[p_kod][0]}" if p_kod in MYSG_PORTFOLIO_P else p_kod
            dtl_str = f": {p_dtl}" if p_dtl and p_dtl not in ["nan", "None", label_p] else ""
            p_items_html += f"""
            <div style="margin-left: 20px; margin-top: 2px; font-size: 13px; color: #1e293b;">
                <b>2.2.{p_count}.</b> <b>{label_p}</b>{dtl_str}
            </div>
            """
            p_count += 1

    if not p_items_html:
        p_items_html = '<div style="margin-left: 20px; font-style: italic; color: #64748b; font-size: 12.5px;">Tiada Jawatan Tanpa Portfolio Ditetapkan</div>'

    # 8. JAWATANKUASA J
    j_cols = [c for c in staf_row.index if c.startswith('Kod_J_')]
    j_items_html = ""
    j_count = 1
    for col in j_cols:
        idx_num = col.split('_')[2]
        j_kod = str(staf_row.get(f"Kod_J_{idx_num}", '')).strip()
        j_dtl = str(staf_row.get(f"Detail_J_{idx_num}", '')).strip()

        if j_kod not in ["nan", "None", ""]:
            label_j = f"{j_kod} | {MYSG_JAWATANKUASA_J[j_kod][0]}" if j_kod in MYSG_JAWATANKUASA_J else j_kod
            dtl_str = f": {j_dtl}" if j_dtl and j_dtl not in ["nan", "None", label_j] else ""
            j_items_html += f"""
            <div style="margin-left: 20px; margin-top: 2px; font-size: 13px; color: #1e293b;">
                <b>2.3.{j_count}.</b> <b>{label_j}</b>{dtl_str}
            </div>
            """
            j_count += 1

    if not j_items_html:
        j_items_html = '<div style="margin-left: 20px; font-style: italic; color: #64748b; font-size: 12.5px;">Tiada Jawatankuasa Ditetapkan</div>'

    # 9. HTML SURAT CANTIK LENGKAP
    html_content = f"""
    <div id="mysgLetterContent" style="
        background-color: #ffffff;
        font-family: Arial, Helvetica, sans-serif;
        color: #0f172a;
        padding: 25px 35px;
        max-width: 800px;
        margin: 0 auto;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        line-height: 1.45;
    ">
        <!-- HEADER KEPALA SURAT RASMI KPM -->
        <table style="width: 100%; border-collapse: collapse; margin-bottom: 12px; border-bottom: 2px solid #000; padding-bottom: 8px;">
            <tr>
                <!-- JATA NEGARA (KIRI SAHAJA) -->
                <td style="width: 12%; text-align: left; vertical-align: middle;">
                    {jata_img_html}
                </td>
                
                <!-- NAMA KPM & SEKOLAH (TENGAH) -->
                <td style="width: 55%; text-align: left; vertical-align: middle; padding-left: 8px;">
                    <div style="font-size: 13.5px; font-weight: 800; color: #000; font-family: Arial, sans-serif; text-transform: uppercase;">KEMENTERIAN PENDIDIKAN MALAYSIA</div>
                    <div style="font-size: 13.5px; font-weight: 800; color: #000; font-family: Arial, sans-serif; text-transform: uppercase; margin: 2px 0;">{nama_sekolah}</div>
                    <div style="font-size: 10.5px; color: #333; font-family: Arial, sans-serif;">{alamat_sekolah}</div>
                </td>
                
                <!-- TEL/FAKS/EMEL & LENCANA SEKOLAH (KANAN SAHAJA) -->
                <td style="width: 33%; text-align: right; vertical-align: middle;">
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="text-align: right; vertical-align: middle; padding-right: 8px; font-size: 9.5px; color: #333; line-height: 1.3; font-family: Arial, sans-serif;">
                                Tel : {no_tel}<br>
                                Faks : {no_fax}<br>
                                Emel : {emel_rasmi}
                            </td>
                            <td style="width: 80px; text-align: right; vertical-align: middle;">
                                {logo_sek_html}
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>

        <!-- RUJUKAN & TARIKH -->
        <table style="width: 100%; border-collapse: collapse; margin-bottom: 15px; font-size: 12.5px;">
            <tr>
                <td style="width: 58%;"></td>
                <td style="width: 14%; font-weight: bold; text-align: right;">Ruj. Kami</td>
                <td style="width: 28%;">: {no_rujukan}</td>
            </tr>
            <tr>
                <td></td>
                <td style="font-weight: bold; text-align: right;">Tarikh</td>
                <td>: {tarikh_hari_ini}</td>
            </tr>
        </table>

        <!-- MAKLUMAT PENERIMA -->
        <div style="margin-bottom: 12px; font-size: 13.5px;">
            <div style="font-weight: 800; color: #000; font-size: 14.5px;">{nama_staf}</div>
            <div style="color: #475569; font-size: 12.5px;">No. KP: {no_kp}</div>
        </div>

        <div style="font-size: 13px; margin-bottom: 12px;">Tuan / Puan,</div>

        <!-- TAJUK SURAT -->
        <div style="font-size: 13.5px; font-weight: 800; color: #000; text-transform: uppercase; margin-bottom: 10px; line-height: 1.35;">
            LANTIKAN DAN AGIHAN TUGAS BAGI SESI PERSEKOLAHAN TAHUN {tahun_sesi}
        </div>

        <p style="font-size: 13px; text-align: justify; margin-bottom: 10px; color: #1e293b;">
            Dengan segala hormatnya perkara di atas adalah dirujuk bersama perkara-perkara berkaitan di bawah Akta Pendidikan 1996, Surat-surat Pekeliling Ikhtisas (SPI), serta arahan-arahan dan garis panduan MySG KPM yang berkuat kuasa.
        </p>

        <p style="font-size: 13px; text-align: justify; margin-bottom: 12px; color: #1e293b;">
            2. Sukacita dimaklumkan bahawa pihak sekolah melantik tuan/puan untuk memegang jawatan dan melaksanakan amanah seperti butiran di bawah berkuat kuasa mulai tarikh surat ini dikeluarkan sehingga ke suatu tarikh yang dimaklumkan kemudian:
        </p>

        <!-- KOTAK SENARAI TUGAS -->
        <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; margin-bottom: 15px;">
            <div style="font-size: 13px; font-weight: bold; color: #0f172a; margin-bottom: 4px;">
                2.1. JAWATAN BERPORTFOLIO: <span style="font-weight: bold; color: #0f172a;">{jawatan_full}</span>
            </div>
            {pdp_items_html}

            <br>

            <div style="font-size: 13px; font-weight: bold; color: #0f172a; margin-bottom: 4px;">
                2.2. JAWATAN TANPA PORTFOLIO:
            </div>
            {p_items_html}

            <br>

            <div style="font-size: 13px; font-weight: bold; color: #0f172a; margin-bottom: 4px;">
                2.3. JAWATANKUASA:
            </div>
            {j_items_html}
        </div>

        <p style="font-size: 13px; text-align: justify; margin-bottom: 10px; color: #1e293b;">
            3. Sehubungan dengan itu, tuan/puan adalah dinasihatkan untuk merujuk dan memahami tugas serta tanggungjawab yang ditetapkan seperti dalam MySG KPM dan pekeliling yang berkuat kuasa.
        </p>

        <div style="font-size: 13px; font-weight: bold; margin-bottom: 12px; color: #000;">
            "MALAYSIA MADANI"<br>
            "BERKHIDMAT UNTUK NEGARA"
        </div>

        <div style="font-size: 13px; margin-bottom: 30px; color: #1e293b;">
            Saya yang menjalankan amanah,<br><br><br>
            <b>({nama_gb})</b><br>
            Pengetua / Guru Besar<br>
            {nama_sekolah}
        </div>
    </div>
    """
    return html_content