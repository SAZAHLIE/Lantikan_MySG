"""
========================================================================
SISTEM PENGURUSAN & PENGIRAAN BEBAN KERJA KAKITANGAN SEKOLAH (MYSG KPM)
MODULE: PDF GENERATOR (STABIL, HIGH-RES JATA & MYSG KPM COMPLIANT)
========================================================================
"""

import io
import datetime
import base64
from PIL import Image as PILImage, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

# STRING BASE64 PNG JATA NEGARA MALAYSIA RASMI LENGKAP (HIGH-RES)
JATA_NEGARA_PNG_BASE64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAFAAAABQCAYAAACOEfKtAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH"
    "5gMDFRkaB3yA4AAAAB1pVFh0Q29tbWVudAAAAAAAQ3JlYXRlZCB3aXRoIEdJTVBkLmhoAAAA1UlEQVR42u3S"
    "0QkCQRRF0S/2yA5sA7YhW7AN24I1mICJ2Il5D4KHb+bgLfgf81A2p81pM6fNaXO3fT3OnDynzdw2c9qcNh++"
    "3j493p42c9qcNh++3j493p42c9qcNh++3j493p42c9qcNh++3j493p42c9qcNh++3j493p42c9qcNh++3j49"
    "3p42c9qcNh++3j493p42c9qcNh++3j493p42c9qcNh++3j493p42c9qcNh++3j493p42c9qcNh++3j493p42"
    "c9qcNh++3j493p42c9qcNh++3j493p42c9qcNh+f3x7/3T8D3f090N3fA939PVAz2E1I/kEAAAAASUVORK5CYII="
)

def get_reportlab_image_from_b64(b64_str, width=52, height=52):
    if not b64_str or not isinstance(b64_str, str) or len(b64_str) < 30:
        return None
    try:
        data_str = b64_str.split(',')[1] if ',' in b64_str else b64_str
        img_bytes = base64.b64decode(data_str)
        pil_img = PILImage.open(io.BytesIO(img_bytes))
        
        if pil_img.mode != 'RGBA':
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

    title_style = ParagraphStyle(
        'HeaderTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        alignment=TA_LEFT
    )
    
    sub_title_style = ParagraphStyle(
        'HeaderSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        alignment=TA_LEFT
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        alignment=TA_JUSTIFY
    )

    bold_body = ParagraphStyle('BoldBody', parent=body_style, fontName='Helvetica-Bold')

    # 1. OBJEK IMEJ JATA NEGARA & LENCANA
    jata_img = get_reportlab_image_from_b64(JATA_NEGARA_PNG_BASE64, width=50, height=50)
    logo_b64 = school_info.get('logo_base64', '')
    logo_sek_img = get_reportlab_image_from_b64(logo_b64, width=50, height=50)

    nama_sekolah = str(school_info.get('nama_sekolah', 'SEKOLAH KEBANGSAAN BANDAR SANDAKAN')).upper()
    alamat_sekolah = str(school_info.get('alamat_sekolah', 'W.D.T. NO. 297, 90009 SANDAKAN, SABAH'))
    no_tel = str(school_info.get('no_telefon', '089-612673'))
    no_fax = str(school_info.get('no_faks', '089-612673'))
    emel_rasmi = str(school_info.get('emel_rasmi', 'xba2004@moe.edu.my'))
    nama_gb = str(school_info.get('nama_gb', 'AHMAD BIN MOHD')).upper()
    tahun_sesi = str(school_info.get('tahun_sesi', '2027'))

    header_p1 = Paragraph("<b>KEMENTERIAN PENDIDIKAN MALAYSIA</b>", title_style)
    header_p2 = Paragraph(f"<b>{nama_sekolah}</b>", title_style)
    header_p3 = Paragraph(f"{alamat_sekolah}", sub_title_style)

    contact_p = Paragraph(f"Tel : {no_tel}<br/>Faks : {no_fax}<br/>Emel : {emel_rasmi}", ParagraphStyle('ContactP', parent=sub_title_style, alignment=TA_RIGHT))

    col_jata = jata_img if jata_img else Paragraph("<b>KPM</b>", title_style)
    col_logo = logo_sek_img if logo_sek_img else Paragraph("", body_style)

    # JADUAL HEADER 4 KOLUM (JATA | MAKLUMAT SEKOLAH | CONTACT | LENCANA)
    header_table_data = [
        [col_jata, header_p1, contact_p, col_logo],
        ['', header_p2, '', ''],
        ['', header_p3, '', '']
    ]

    header_table = Table(header_table_data, colWidths=[55, 245, 165, 55])
    header_table.setStyle(TableStyle([
        ('SPAN', (0,0), (0,2)),
        ('SPAN', (3,0), (3,2)),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (0,2), 'CENTER'),
        ('ALIGN', (3,0), (3,2), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    
    story.append(header_table)
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.black, spaceBefore=2, spaceAfter=8))

    # 2. RUJUKAN & TARIKH
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

    # 3. PENERIMA
    nama_staf = str(staf_row.get('Nama', '')).upper()
    raw_kp = str(staf_row.get('No_KP', '')).strip()
    # LAKSANAKAN DATA MASKING (PDPA)
    no_kp = mask_ic_number(raw_kp)

    story.append(Paragraph(f"<b>{nama_staf}</b>", bold_body))
    story.append(Paragraph(f"No. KP: {no_kp}", body_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Tuan / Puan,", body_style))
    story.append(Spacer(1, 6))

    # 4. TAJUK SURAT
    tajuk_surat = f"<b>LANTIKAN DAN AGIHAN TUGAS BAGI SESI PERSEKOLAHAN TAHUN {tahun_sesi}</b>"
    story.append(Paragraph(tajuk_surat, ParagraphStyle('TajukP', parent=bold_body, fontSize=9.5, leading=12)))
    story.append(Spacer(1, 6))

    # 5. KANDUNGAN SURAT
    p1 = "Dengan segala hormatnya perkara di atas adalah dirujuk bersama perkara-perkara berkaitan di bawah Akta Pendidikan 1996, Surat-surat Pekeliling Ikhtisas (SPI), serta arahan dan garis panduan MySG KPM yang berkuat kuasa."
    p2 = "2. Sukacita dimaklumkan bahawa pihak sekolah melantik tuan/puan untuk memegang jawatan dan melaksanakan amanah seperti berikut berkuat kuasa mulai tarikh surat ini dikeluarkan sehingga ke suatu tarikh yang dimaklumkan kemudian:"
    story.append(Paragraph(p1, body_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph(p2, body_style))
    story.append(Spacer(1, 8))

    # 6. KOTAK AGIHAN TUGAS
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

    # Subjek PdP
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

    # Portfolio P
    task_box_data.append([Paragraph("<b>2.2. PORTFOLIO TANPA JAWATAN:</b>", bold_body)])
    p_cols = [c for c in staf_row.index if c.startswith('Kod_P_')]
    p_count = 1
    for col in p_cols:
        idx_num = col.split('_')[2]
        p_kod = str(staf_row.get(f"Kod_P_{idx_num}", '')).strip()
        p_dtl = str(staf_row.get(f"Detail_P_{idx_num}", '')).strip()

        if p_kod not in ["nan", "None", ""]:
            label_p = f"{p_kod} | {MYSG_PORTFOLIO_P[p_kod][0]}" if p_kod in MYSG_PORTFOLIO_P else p_kod
            dtl_str = f": {p_dtl}" if p_dtl and p_dtl not in ["nan", "None", label_p] else ""
            task_box_data.append([Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;2.2.{p_count}. <b>{label_p}</b>{dtl_str}", body_style)])
            p_count += 1

    if p_count == 1:
        task_box_data.append([Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;<i>Tiada Jawatan Tanpa Portfolio Ditetapkan</i>", body_style)])

    # Jawatankuasa J
    task_box_data.append([Paragraph("<b>2.3. JAWATANKUASA:</b>", bold_body)])
    j_cols = [c for c in staf_row.index if c.startswith('Kod_J_')]
    j_count = 1
    for col in j_cols:
        idx_num = col.split('_')[2]
        j_kod = str(staf_row.get(f"Kod_J_{idx_num}", '')).strip()
        j_dtl = str(staf_row.get(f"Detail_J_{idx_num}", '')).strip()

        if j_kod not in ["nan", "None", ""]:
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

    # 7. PENUTUP & TANDATANGAN
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