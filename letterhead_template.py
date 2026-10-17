"""
========================================================================
MYSG KPM: TEMPLAT KEPALA SURAT, COGAN KATA & FOOTER RASMI (A4)
========================================================================
"""

import os
import base64

def get_image_base64(file_path):
    """Membaca fail imej tempatan dan menukarkannya kepada Base64."""
    if os.path.exists(file_path):
        try:
            with open(file_path, "rb") as img_file:
                encoded = base64.b64encode(img_file.read()).decode('utf-8')
                ext = file_path.split('.')[-1].lower()
                mime_type = "image/png" if ext == "png" else "image/jpeg"
                return f"data:{mime_type};base64,{encoded}"
        except Exception:
            pass
    return ""

def get_official_letterhead(school_info):
    """Menjana HTML Kepala Surat Rasmi KPM (Tanpa Cogan Kata di Bawah Garisan)."""
    if not isinstance(school_info, dict):
        school_info = {}

    # 1. PANGGILAN DATA TEPAT DARI BORANG PROFIL SEKOLAH
    nama_sekolah = str(school_info.get('nama_sekolah', 'SEKOLAH KEBANGSAAN BANDAR')).upper()
    
    b1 = str(school_info.get('alamat_1', '')).strip().upper()
    b2 = str(school_info.get('alamat_2', '')).strip().upper()
    b3 = str(school_info.get('negeri_negara', '')).strip().upper()

    # PEMBERSIHAN: Buang sisa koma bertindih jika data dari Vault lama rosak
    if not b1.replace(',', '').strip(): b1 = ''
    if not b2.replace(',', '').strip(): b2 = ''
    if not b3.replace(',', '').strip(): b3 = ''

    if not b1 and school_info.get('alamat_sekolah'):
        parts = [p.strip() for p in str(school_info.get('alamat_sekolah')).split(',') if p.strip()]
        if len(parts) >= 3:
            b1 = parts[0].upper()
            b2 = ", ".join(parts[1:-1]).upper()
            b3 = parts[-1].upper()
        else:
            b1 = str(school_info.get('alamat_sekolah')).upper()

    # Nilai lalai mutlak jika tiada data langsung
    if not b1: b1 = "KM 4, JALAN LEILA,"
    if not b2: b2 = "90000 SANDAKAN,"
    if not b3: b3 = "SABAH, MALAYSIA"
    
    no_tel = str(school_info.get('no_telefon', '089-612673'))
    no_fax = str(school_info.get('no_faks', '089-612673'))
    email_sekolah = str(school_info.get('emel_rasmi', 'xba2004@moe.edu.my'))

    # 2. LOGIK JATA NEGARA
    jata_b64 = (get_image_base64("jata_negara.png") or 
                get_image_base64("jata.png") or 
                get_image_base64("jata_negara.jpg"))
    
    if not jata_b64:
        jata_html = '<img src="https://upload.wikimedia.org/wikipedia/commons/2/26/Coat_of_arms_of_Malaysia.svg" style="height: 75px; width: auto; object-fit: contain;" alt="Jata Negara">'
    else:
        jata_html = f'<img src="{jata_b64}" style="height: 75px; width: auto; object-fit: contain;" alt="Jata Negara">'

    # 3. LOGIK LENCANA SEKOLAH
    logo_b64 = school_info.get('logo_base64', '')
    
    if not logo_b64:
        logo_b64 = (get_image_base64("logo.png") or 
                    get_image_base64("logo.jpg") or 
                    get_image_base64("logo_sekolah.png") or 
                    get_image_base64("logo_sekolah.jpg") or 
                    get_image_base64("lencana.png"))
    
    if not logo_b64:
        logo_html = '<div style="height: 75px; width: 65px; border: 1px dashed #ccc; display: flex; align-items: center; justify-content: center; font-size: 8px; color: #888;">[Logo Sekolah]</div>'
    else:
        logo_html = f'<img src="{logo_b64}" style="height: 75px; width: auto; max-width: 90px; object-fit: contain;" alt="Logo Sekolah">'

    # 4. PENJANAAN HTML KEPALA SURAT
    return f"""
    <div style="font-family: Arial, Helvetica, sans-serif; color: #000000; width: 100%; margin-bottom: 6px;">
        <table style="width: 100%; border-collapse: collapse; border: none; margin: 0; padding: 0;">
            <tr style="vertical-align: top;">
                <td style="width: 12%; text-align: left; padding: 0;">
                    {jata_html}
                </td>
                <td style="width: 53%; text-align: left; padding-left: 8px; white-space: nowrap;">
                    <div style="font-size: 13pt; font-weight: bold; font-family: 'Arial Black', Arial, sans-serif; letter-spacing: 0.5px; line-height: 1.15; text-transform: uppercase;">
                        KEMENTERIAN PENDIDIKAN MALAYSIA
                    </div>
                    <div style="font-size: 12pt; font-weight: bold; line-height: 1.2; margin-top: 2px;">
                        {nama_sekolah}
                    </div>
                    <div style="font-size: 11pt; font-weight: normal; line-height: 1.2; margin-top: 2px;">
                        {b1}
                    </div>
                    <div style="font-size: 11pt; font-weight: normal; line-height: 1.2;">
                        {b2}
                    </div>
                    <div style="font-size: 11pt; font-weight: normal; line-height: 1.2; text-transform: uppercase;">
                        {b3}
                    </div>
                </td>
                <td style="width: 25%; text-align: left; vertical-align: bottom; font-size: 9.5pt; padding-right: 5px; padding-bottom: 2px;">
                    <table style="border-collapse: collapse; border: none; font-size: 9.5pt; font-family: Arial, sans-serif; text-align: left; width: 100%;">
                        <tr>
                            <td style="text-align: left; padding-right: 4px; width: 25%;">Tel</td>
                            <td style="text-align: center; padding-right: 4px; width: 5%;">:</td>
                            <td style="text-align: left; white-space: nowrap; width: 70%;">{no_tel}</td>
                        </tr>
                        <tr>
                            <td style="text-align: left; padding-right: 4px;">Faks</td>
                            <td style="text-align: center; padding-right: 4px;">:</td>
                            <td style="text-align: left; white-space: nowrap;">{no_fax}</td>
                        </tr>
                        <tr>
                            <td style="text-align: left; padding-right: 4px;">Emel</td>
                            <td style="text-align: center; padding-right: 4px;">:</td>
                            <td style="text-align: left; white-space: nowrap;">{email_sekolah}</td>
                        </tr>
                    </table>
                </td>
                <td style="width: 10%; text-align: right; padding: 0; vertical-align: middle;">
                    {logo_html}
                </td>
            </tr>
        </table>
        <hr style="border: none; border-top: 2.5px solid #000000; margin-top: 8px; margin-bottom: 10px; opacity: 1;">
    </div>
    """

def get_appointment_letter_footer_html(school_info=None):
    """Menjana HTML Kaki Surat Lantikan: Garisan di atas, Cogan Kata di bawah."""
    if not isinstance(school_info, dict):
        school_info = {}

    cogan_kata = str(school_info.get('cogan_kata', 'BERBUDAYA, BERILMU, BERWAWASAN')).upper().strip()

    cogan_kata_html = ""
    if cogan_kata:
        cogan_kata_html = f"""
        <div style="text-align: center; font-weight: bold; font-size: 8.5pt; letter-spacing: 1px; text-transform: uppercase; margin-top: 4px; color: #000000; font-family: Arial, sans-serif;">
            "{cogan_kata}"
        </div>
        """

    return f"""
    <div style="width: 100%; margin-top: 15pt; page-break-inside: avoid;">
        <hr style="border: none; border-top: 1.5px solid #000000; margin: 0; padding: 0; opacity: 1;">
        {cogan_kata_html}
    </div>
    """

def get_official_letter_footer(school_info, show_akuan_terima=False):
    """Menjana HTML Footer Standard Laporan Individu."""
    if not isinstance(school_info, dict):
        school_info = {}

    kod_sekolah = school_info.get('kod_sekolah', 'XBA2004')

    return f"""
    <div style="margin-top: 10px; border-top: 1px solid #ccc; padding-top: 3px; font-size: 7pt; color: #555; display: flex; justify-content: space-between; font-family: Arial, sans-serif;">
        <div><i>Dokumen Rasmi Dijana Menerusi MySG KPM: Sistem Pengurusan & Analisis Beban Kerja ({kod_sekolah})</i></div>
    </div>
    """

def get_a4_print_css(orientation='portrait'):
    """Gaya CSS Tema Standard Cetakan A4."""
    margin_setting = "1.8cm 2.2cm 1.8cm 2.2cm" if orientation == 'portrait' else "1.2cm 1.5cm 1.2cm 1.5cm"
    
    return f"""
    @page {{
        size: A4 {orientation};
        margin: {margin_setting};
    }}
    body {{
        font-family: Arial, Helvetica, sans-serif;
        font-size: 10.5pt;
        color: #000000;
        line-height: 1.35;
        background-color: #ffffff;
        margin: 0;
        padding: 0;
    }}
    .print-table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 8px;
        margin-bottom: 12px;
    }}
    .print-table th, .print-table td {{
        border: 1px solid #000;
        padding: 5px 7px;
        font-size: 10pt;
    }}
    .print-table th {{
        background-color: #f2f2f2;
        font-weight: bold;
    }}
    @media print {{
        body {{ margin: 0; }}
    }}
    """
