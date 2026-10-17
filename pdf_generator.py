"""
========================================================================
SISTEM PENGURUSAN & PENGIRAAN BEBAN KERJA KAKITANGAN SEKOLAH (MYSG KPM)
MODULE: PDF GENERATOR (STABIL, HIGH-RES JATA & MYSG KPM COMPLIANT)
========================================================================
"""

import io
import datetime
import base64
import os
from PIL import Image as PILImage, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

def get_local_image_base64(file_path):
    """Membaca fail imej tempatan dan mengembalikannya sebagai string Base64."""
    if os.path.exists(file_path):
        try:
            with open(file_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception:
            pass
    return ""

def get_reportlab_image_from_b64(b64_str, width=65, height=65):
    """Menukar rentetan Base64 kepada objek Image ReportLab."""
    if not b64_str or len(b64_str) < 30:
        return None
    try:
        data_str = b64_str.split(',')[1] if ',' in b64_str else b64_str
        img_bytes = base64.b64decode(data_str)
        pil_img = PILImage.open(io.BytesIO(img_bytes))
        
        if pil_img.mode != 'RGBA' and pil_img.mode != 'RGB':
            pil_img = pil_img.convert('RGBA')
            
        buf = io.BytesIO()
        pil_img.save(buf, format='PNG')
        buf.seek(0)
        return Image(buf, width=width, height=height)
    except Exception:
        return None

def format_tarikh_melayu(d):
    bulan = [
        "", "Januari", "Februari", "Mac", "April", "Mei", "Jun",
        "Julai", "Ogos", "September", "Oktober", "November", "Disember"
    ]
    return f"{d.day} {bulan[d.month]} {d.year}"

def mask_ic_number(ic_str):
    """Fungsi Data Masking (PDPA) untuk menyembunyikan 4 digit terakhir No. KP."""
    if not ic_str or ic_str in ["nan", "None", "-"]:
        return "-"
    ic_str = ic_str.replace("-", "").strip()
    if len(ic_str) == 12:
        return f"{ic_str[:6]}-{ic_str[6:8]}-XXXX"
    return "XXXXXX-XX-XXXX"

def generate_appointment_letter_pdf(staf_row, school_info, no_rujukan=""):
    from mysg_core import MYSG_PORTFOLIO_P, MYSG_JAWATANKUASA_J

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=25,
        bottomMargin=25
    )

    story = []
    styles = getSampleStyleSheet()

    body_style = ParagraphStyle('BodyDark', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=12, alignment=TA_JUSTIFY)
    bold_body = ParagraphStyle('BoldBody', parent=body_style, fontName='Helvetica-Bold')

    # -------------------------------------------------------------
    # 1. OBJEK IMEJ JATA NEGARA & LENCANA (SAIZ DIKEMAS KINI)
    # -------------------------------------------------------------
    jata_b64 = ""
    for fname in ["jata_negara.png", "jata.png", "jata_negara.jpg", "jata.jpg", "JATA_NEGARA.png", "JATA NEGARA.png"]:
        path = os.path.join(os.getcwd(), fname)
        if os.path.exists(path):
            jata_b64 = get_local_image_base64(path)
            break
            
    # Jata Negara dibesarkan (75x75)
    jata_img = get_reportlab_image_from_b64(jata_b64, width=75, height=75) 
    col_jata = jata_img if jata_img else Paragraph("<b>MALAYSIA</b>", body_style)

    logo_b64 = school_info.get('logo_base64', '')
    
    # Lencana Sekolah dikecilkan (55x55) agar Jata lebih menonjol
    logo_sek_img = get_reportlab_image_from_b64(logo_b64, width=55, height=55) 
    col_logo = logo_sek_img if logo_sek_img else Paragraph("", body_style)

    # -------------------------------------------------------------
    # 2. MAKLUMAT SEKOLAH & ALAMAT (JARAK RAPAT)
    # -------------------------------------------------------------
    nama_sekolah = str(school_info.get('nama_sekolah', 'SEKOLAH KEBANGSAAN BANDAR')).upper()
    
    b1 = str(school_info.get('alamat_1', '')).strip().upper()
    b2 = str(school_info.get('alamat_2', '')).strip().upper()
    b3 = str(school_info.get('negeri_negara', '')).strip().upper()

    if not b1.replace(',', '').strip(): b1 = ''
    if not b2.replace(',', '').strip(): b2 = ''
    if not b3.replace(',', '').strip(): b3 = ''

    alamat_lines = []
    if b1: alamat_lines.append(b1)
    if b2: alamat_lines.append(b2)
    if b3: alamat_lines.append(b3)
    
    alamat_str = "<br/>".join(alamat_lines) if alamat_lines else "KM 4, JALAN LEILA,<br/>90000 SANDAKAN,<br/>SABAH, MALAYSIA"

    # GABUNGAN: KPM, Sekolah & Alamat disatukan dalam satu perenggan untuk jarak (spacing) yang rapat
    header_text = (
        f"<b><font size='11.5'>KEMENTERIAN PENDIDIKAN MALAYSIA</font></b><br/>"
        f"<b><font size='10.5'>{nama_sekolah}</font></b><br/>"
        f"<font size='8.5'>{alamat_str}</font>"
    )
    header_p = Paragraph(header_text, ParagraphStyle('HeaderCenterText', parent=styles['Normal'], fontName='Helvetica', leading=12.5, alignment=TA_LEFT))

    # -------------------------------------------------------------
    # 3. MAKLUMAT HUBUNGI & PEMBOLEH UBAH PENTING LAIN
    # -------------------------------------------------------------
    no_tel = str(school_info.get('no_telefon', '089-612673'))
    no_fax = str(school_info.get('no_faks', '089-612673'))
    emel_rasmi = str(school_info.get('emel_rasmi', 'xba2004@moe.edu.my'))
    
    # VARIABEL YANG HILANG SEBELUMNYA TELAH DIKEMBALIKAN DI SINI
    tahun_sesi = str(school_info.get('tahun_sesi', '2027'))
    nama_gb = str(school_info.get('nama_gb', 'AHMAD BIN MOHD')).upper()

    contact_style = ParagraphStyle('ContactP', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=11, alignment=TA_LEFT)
    contact_p = Paragraph(
        f"Tel&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: {no_tel}<br/>"
        f"Faks&nbsp;&nbsp;&nbsp;&nbsp;: {no_fax}<br/>"
        f"Emel&nbsp;&nbsp;&nbsp;: {emel_rasmi}", 
        contact_style
    )

    # -------------------------------------------------------------
    # 4. JADUAL HEADER (KEDUDUKAN & PENJAJARAN DIKEMAS KINI)
    # -------------------------------------------------------------
    header_table_data = [
        [col_jata, header_p, contact_p, col_logo]
    ]

    header_table = Table(header_table_data, colWidths=[80, 240, 140, 60])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (0,0), 'MIDDLE'), # Jata di tengah
        ('VALIGN', (1,0), (1,0), 'MIDDLE'), # Teks Alamat di tengah
        ('VALIGN', (2,0), (2,0), 'BOTTOM'), # Maklumat Hubungi dijajarkan ke Bawah (Bottom)
        ('VALIGN', (3,0), (3,0), 'MIDDLE'), # Lencana di tengah
        ('ALIGN', (0,0), (0,0), 'LEFT'),
        ('ALIGN', (1,0), (1,0), 'LEFT'),
        ('ALIGN', (2,0), (2,0), 'LEFT'),
        ('ALIGN', (3,0), (3,0), 'RIGHT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    
    story.append(header_table)
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.black, spaceBefore=2, spaceAfter=8))

    # -------------------------------------------------------------
    # 5. RUJUKAN & TARIKH
    # -------------------------------------------------------------
    if not no_rujukan:
        kod_sek = str(school_info.get('kod_sekolah', 'SEK'))
        no_rujukan = f"KP/{kod_sek}/MYSG/{tahun_sesi.split('/')[0]}/01"

    tarikh_hari_ini = format_tarikh_melayu(datetime.date.today())

    rujukan_table_data = [
        ['', Paragraph(f"<b>Ruj. Kami:</b> {no_rujukan}", body_style)],
        ['', Paragraph(f"<b>Tarikh:</b> {tarikh_hari_ini}", body_style)]
    ]
    rujukan_table = Table(rujukan_table_data, colWidths=[300, 220])
    rujukan_table.setStyle(TableStyle([('ALIGN', (1,0), (1,-1), 'RIGHT')]))
    story.append(rujukan_table)
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # 6. PENERIMA SURAT
    # -------------------------------------------------------------
    nama_staf = str(staf_row.get('Nama', '')).upper()
    raw_kp = str(staf_row.get('No_KP', '')).strip()
    no_kp = mask_ic_number(raw_kp)

    story.append(Paragraph(f"<b>{nama_staf}</b>", bold_body))
    story.append(Paragraph(f"No. KP: {no_kp}", body_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Tuan / Puan,", body_style))
    story.append(Spacer(1, 6))

    # -------------------------------------------------------------
    # 7. TAJUK SURAT
    # -------------------------------------------------------------
    tajuk_surat = f"<b>LANTIKAN DAN AGIHAN TUGAS BAGI SESI PERSEKOLAHAN TAHUN {tahun_sesi}</b>"
    story.append(Paragraph(tajuk_surat, ParagraphStyle('TajukP', parent=bold_body, fontSize=9.5, leading=12)))
    story.append(Spacer(1, 6))

    # -------------------------------------------------------------
    # 8. KANDUNGAN SURAT
    # -------------------------------------------------------------
    p1 = "Dengan segala hormatnya perkara di atas adalah dirujuk bersama perkara-perkara berkaitan di bawah Akta Pendidikan 1996, Surat-surat Pekeliling Ikhtisas (SPI), serta arahan dan garis panduan MySG KPM yang berkuat kuasa."
    p2 = "2. Sukacita dimaklumkan bahawa pihak sekolah melantik tuan/puan untuk memegang jawatan dan melaksanakan amanah seperti berikut berkuat kuasa mulai tarikh surat ini dikeluarkan sehingga ke suatu tarikh yang dimaklumkan kemudian:"
    story.append(Paragraph(p1, body_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph(p2, body_style))
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # 9. KOTAK AGIHAN TUGAS
    # -------------------------------------------------------------
    jawatan_val = str(staf_row.get('Jawatan', '')).strip()
    dtl_h = str(staf_row.get('Detail_H_1', '')).strip()
    kod_h = str(staf_row.get('Kod_H_1', '')).strip()
    
    if jawatan_val in ["nan", "None", ""]:
        jawatan_val = dtl_h if dtl_h not in ["nan", "None", ""] else "Guru Akademik Biasa"

    if kod_h and kod_h not in jawatan_val:
        jawatan_full = f"{kod_h} | {jawatan_val}"
    else:
        jawatan_full = jawatan_val

    task_box_data = []
    task_box_data.append([Paragraph(f"<b>2.1. JAWATAN BERPORTFOLIO:</b> {jawatan_full}", bold_body)])

    pdp_cols = [c for c in staf_row.index if c.startswith('Subjek_')]
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
            task_box_data.append([Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;2.1.{sub_count}. Mengajar <b>{sub_val}</b>{cls_str} ({wkt_num} Waktu)", body_style)])
            sub_count += 1

    task_box_data.append([Paragraph("<b>2.2. PORTFOLIO TANPA JAWATAN:</b>", bold_body)])
    p_cols = [c for c in staf_row.index if c.startswith('Kod_P_')]
    p_count = 1
    for col in p_cols:
        idx_num = col.split('_')[2]
        p_kod = str(staf_row.get(f"Kod_P_{idx_num}", '')).strip()
        p_dtl = str(staf_row.get(f"Detail_P_{idx_num}", '')).strip()

        if p_kod not in ["nan", "None", ""]:
            from mysg_core import MYSG_PORTFOLIO_P
            label_p = f"{p_kod} | {MYSG_PORTFOLIO_P[p_kod][0]}" if p_kod in MYSG_PORTFOLIO_P else p_kod
            dtl_str = f": {p_dtl}" if p_dtl and p_dtl not in ["nan", "None", label_p] else ""
            task_box_data.append([Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;2.2.{p_count}. <b>{label_p}</b>{dtl_str}", body_style)])
            p_count += 1

    if p_count == 1:
        task_box_data.append([Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;<i>Tiada Jawatan Tanpa Portfolio Ditetapkan</i>", body_style)])

    task_box_data.append([Paragraph("<b>2.3. JAWATANKUASA:</b>", bold_body)])
    j_cols = [c for c in staf_row.index if c.startswith('Kod_J_')]
    j_count = 1
    for col in j_cols:
        idx_num = col.split('_')[2]
        j_kod = str(staf_row.get(f"Kod_J_{idx_num}", '')).strip()
        j_dtl = str(staf_row.get(f"Detail_J_{idx_num}", '')).strip()

        if j_kod not in ["nan", "None", ""]:
            from mysg_core import MYSG_JAWATANKUASA_J
            label_j = f"{j_kod} | {MYSG_JAWATANKUASA_J[j_kod][0]}" if j_kod in MYSG_JAWATANKUASA_J else j_kod
            dtl_str = f": {j_dtl}" if j_dtl and j_dtl not in ["nan", "None", label_j] else ""
            task_box_data.append([Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;2.3.{j_count}. <b>{label_j}</b>{dtl_str}", body_style)])
            j_count += 1

    if j_count == 1:
        task_box_data.append([Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;<i>Tiada Jawatankuasa Ditetapkan</i>", body_style)])

    task_table = Table(task_box_data, colWidths=[520])
    task_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(task_table)
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # 10. PENUTUP & TANDATANGAN
    # -------------------------------------------------------------
    p3 = "3. Sehubungan dengan itu, tuan/puan adalah dinasihatkan untuk merujuk dan memahami tugas serta tanggungjawab yang ditetapkan selaras dengan Garis Panduan Tadbir Urus Sekolah (MySG KPM)."
    story.append(Paragraph(p3, body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>\"MALAYSIA MADANI\"</b>", bold_body))
    story.append(Paragraph("<b>\"BERKHIDMAT UNTUK NEGARA\"</b>", bold_body))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Saya yang menjalankan amanah,", body_style))
    story.append(Spacer(1, 28))
    story.append(Paragraph(f"<b>({nama_gb})</b>", bold_body))
    story.append(Paragraph("Pengetua / Guru Besar", body_style))
    story.append(Paragraph(f"{nama_sekolah}", body_style))

    # JANA PDF
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
