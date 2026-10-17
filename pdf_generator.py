"""
========================================================================
SISTEM PENGURUSAN & PENGIRAAN BEBAN KERJA KAKITANGAN SEKOLAH (MYSG KPM)
MODULE: PDF GENERATOR (SPA COMPLIANT, PAGE TEMPLATES & CLEAN TEXT)
========================================================================
"""

import io
import datetime
import base64
import os
import urllib.request
from PIL import Image as PILImage, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, NextPageTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas

# KELAS KANVAS KHAS UNTUK FOOTER, NOMBOR MUKA SURAT & HEADER PAGE 2+
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            
            # --- 1. KAKI SURAT (FOOTER SPA) UNTUK SEMUA MUKA SURAT ---
            # Garisan Pemisah Bawah (30mm / 85pt dari bawah, 20mm / 56.7pt dari kiri)
            self.setLineWidth(1.0)
            self.line(56.7, 85.0, A4[0] - 56.7, 85.0)

            # Cogan Kata Sekolah (Di bawah garisan hitam)
            cogan_kata = getattr(self, 'cogan_kata', 'BERBUDAYA BERILMU BERWAWASAN')
            self.setFont("Helvetica-Bold", 8)
            self.drawCentredString(A4[0] / 2.0, 72.0, cogan_kata.upper())

            # Nota Janaan Sistem (Kiri Bawah)
            self.setFont("Helvetica", 6)
            kod = getattr(self, 'kod_sekolah', '')
            self.drawString(56.7, 20, f"Janaan MySG KPM: Sistem Pengurusan & Analisis Beban Kerja ({kod})")

            # Nombor Muka Surat (Tepat di ATAS garisan pemisah 85pt, TIDAK BOLD)
            if self._pageNumber < num_pages:
                self.setFont("Helvetica", 10)
                self.drawRightString(A4[0] - 56.7, 95.0, f"...{self._pageNumber + 1}/")
            
            # --- 2. HEADER KHUSUS UNTUK MUKA SURAT 2 DAN SETERUSNYA ---
            if self._pageNumber > 1:
                ruj = getattr(self, 'no_ruj_format_str', '')
                tajuk = getattr(self, 'tajuk_surat_str', '')
                
                # Koordinat bermula dari Margin Atas
                self.setFont("Helvetica-Bold", 10)
                self.drawString(56.7, 803, tajuk)
                
                self.setFont("Helvetica", 10)
                self.drawString(56.7, 788, f"Ruj. Kami: {ruj}")
                
                # Garis Pemisah Atas Muka Surat Sambungan
                self.setLineWidth(1.0)
                self.line(56.7, 780, A4[0] - 56.7, 780)
            
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

def get_local_image_base64(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception:
            pass
    return ""

def fetch_jata_negara_online():
    url = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Coat_of_arms_of_Malaysia.svg/200px-Coat_of_arms_of_Malaysia.svg.png"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            return base64.b64encode(response.read()).decode('utf-8')
    except:
        return ""

def get_reportlab_image_from_b64(b64_str, max_width=73.7, max_height=56.7):
    if not b64_str or len(b64_str) < 30:
        return None
    try:
        data_str = b64_str.split(',')[1] if ',' in b64_str else b64_str
        img_bytes = base64.b64decode(data_str)
        pil_img = PILImage.open(io.BytesIO(img_bytes))
        
        if pil_img.mode != 'RGBA' and pil_img.mode != 'RGB':
            pil_img = pil_img.convert('RGBA')
            
        orig_w, orig_h = pil_img.size
        aspect = orig_h / float(orig_w)
        
        if aspect > 1:
            new_h = max_height
            new_w = new_h / aspect
        else:
            new_w = max_width
            new_h = new_w * aspect
            if new_h > max_height:
                new_h = max_height
                new_w = new_h / aspect
                
        buf = io.BytesIO()
        pil_img.save(buf, format='PNG')
        buf.seek(0)
        return Image(buf, width=new_w, height=new_h)
    except Exception:
        return None

def format_tarikh_melayu(d):
    bulan = ["", "JANUARI", "FEBRUARI", "MAC", "APRIL", "MEI", "JUN", "JULAI", "OGOS", "SEPTEMBER", "OKTOBER", "NOVEMBER", "DISEMBER"]
    return f"{d.day} {bulan[d.month]} {d.year}"

def mask_ic_number(ic_str):
    if not ic_str or ic_str in ["nan", "None", "-"]: return "-"
    ic_str = ic_str.replace("-", "").strip()
    if len(ic_str) == 12: return f"{ic_str[:6]}-{ic_str[6:8]}-XXXX"
    return "XXXXXX-XX-XXXX"

def generate_appointment_letter_pdf(staf_row, school_info, no_rujukan=""):
    from mysg_core import MYSG_PORTFOLIO_P, MYSG_JAWATANKUASA_J

    kod_sek = str(school_info.get('kod_sekolah', 'SEK'))
    jenis_sek = str(school_info.get('jenis_sekolah', 'Sekolah Rendah'))
    gelaran_gb = "Pengetua" if "Menengah" in jenis_sek else "Guru Besar"
    cogan_kata = str(school_info.get('cogan_kata', 'BERBUDAYA BERILMU BERWAWASAN')).strip()
    tahun_sesi = str(school_info.get('tahun_sesi', '2027'))

    if not no_rujukan:
        no_rujukan = str(school_info.get('no_rujukan', '')).strip()
        if not no_rujukan:
            no_rujukan = f"KP/{kod_sek}/MYSG/{tahun_sesi.split('/')[0]}/01"
            
    # Parameter Rujukan Bersih (Tanpa tag HTML) untuk dicetak pada Kanvas Muka Surat 2
    no_ruj_format_clean = f"{no_rujukan} (          )"
    tajuk_surat_str = f"LANTIKAN DAN AGIHAN TUGAS BAGI SESI PERSEKOLAHAN TAHUN {tahun_sesi}"

    def make_canvas(*args, **kwargs):
        canvas_obj = NumberedCanvas(*args, **kwargs)
        canvas_obj.kod_sekolah = kod_sek
        canvas_obj.cogan_kata = cogan_kata
        canvas_obj.no_ruj_format_str = no_ruj_format_clean
        canvas_obj.tajuk_surat_str = tajuk_surat_str
        return canvas_obj

    buffer = io.BytesIO()
    
    # TETAPAN ASAS BASE DOC TEMPLATE
    # bottomMargin dinaikkan kepada 120.0pt supaya ada 1 baris kosong sebelum nombor muka surat (Y: 95.0)
    doc = BaseDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=56.7, 
        rightMargin=56.7,
        topMargin=28.3,
        bottomMargin=120.0
    )

    # Frame Muka Surat 1 (Ruang penuh)
    frame_first = Frame(
        doc.leftMargin, 
        doc.bottomMargin, 
        doc.width, 
        doc.height, 
        id='first',
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0
    )

    # Frame Muka Surat 2+ (Margin atas diturunkan 45pt untuk beri ruang kepada Header Rujukan)
    frame_later = Frame(
        doc.leftMargin, 
        doc.bottomMargin, 
        doc.width, 
        doc.height, 
        id='later',
        leftPadding=0, rightPadding=0, topPadding=45, bottomPadding=0
    )

    template_first = PageTemplate(id='First', frames=frame_first)
    template_later = PageTemplate(id='Later', frames=frame_later)
    doc.addPageTemplates([template_first, template_later])

    story = []
    
    # Arahan agar Muka Surat Seterusnya (Page 2+) menggunakan templat 'Later'
    story.append(NextPageTemplate('Later'))
    
    styles = getSampleStyleSheet()
    body_style = ParagraphStyle('BodyDark', parent=styles['Normal'], fontName='Helvetica', fontSize=11, leading=14, alignment=TA_JUSTIFY)
    bold_body = ParagraphStyle('BoldBody', parent=body_style, fontName='Helvetica-Bold')
    
    # -------------------------------------------------------------
    # 1. KEPALA SURAT (MUKA SURAT 1 SAHAJA)
    # -------------------------------------------------------------
    jata_b64 = ""
    for fname in ["JATA.png", "jata_negara.png", "jata.png", "jata_negara.jpg", "jata.jpg"]:
        path = os.path.join(os.getcwd(), fname)
        if os.path.exists(path):
            jata_b64 = get_local_image_base64(path)
            break
            
    if not jata_b64:
        jata_b64 = fetch_jata_negara_online()
            
    jata_img = get_reportlab_image_from_b64(jata_b64, max_width=73.7, max_height=56.7) 
    col_jata = jata_img if jata_img else Paragraph("<b>MALAYSIA</b>", body_style)

    logo_b64 = school_info.get('logo_base64', '')
    logo_sek_img = get_reportlab_image_from_b64(logo_b64, max_width=50, max_height=50) 
    col_logo = logo_sek_img if logo_sek_img else Paragraph("", body_style)

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

    header_text = (
        f"<b><font size='11'>KEMENTERIAN PENDIDIKAN MALAYSIA</font></b><br/>"
        f"<b><font size='11'>{nama_sekolah}</font></b><br/>"
        f"<font size='10'>{alamat_str}</font>"
    )
    header_p = Paragraph(header_text, ParagraphStyle('HeaderCenterText', parent=styles['Normal'], fontName='Helvetica', leading=12.5, alignment=TA_LEFT))

    no_tel = str(school_info.get('no_telefon', '089-612673'))
    no_fax = str(school_info.get('no_faks', '089-612673'))
    emel_rasmi = str(school_info.get('emel_rasmi', 'xba2004@moe.edu.my'))
    nama_gb = str(school_info.get('nama_gb', 'AHMAD BIN MOHD')).upper()

    contact_p = Paragraph(
        f"Tel: {no_tel}<br/>"
        f"Faks: {no_fax}<br/>"
        f"Emel: {emel_rasmi}", 
        ParagraphStyle('ContactP', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=10.5, alignment=TA_LEFT)
    )

    header_table = Table([[col_jata, header_p, contact_p, col_logo]], colWidths=[78, 220, 128, 55])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (0,0), 'TOP'),
        ('VALIGN', (1,0), (-1,-1), 'BOTTOM'),
        ('ALIGN', (0,0), (2,0), 'LEFT'),
        ('ALIGN', (3,0), (3,0), 'RIGHT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    
    story.append(header_table)
    story.append(HRFlowable(width="100%", thickness=1.0, color=colors.black, spaceBefore=0, spaceAfter=8))

    no_ruj_format = f"{no_rujukan} (&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;)"
    tarikh_hari_ini = format_tarikh_melayu(datetime.date.today())

    ruj_style = ParagraphStyle('Ruj', parent=styles['Normal'], fontName='Helvetica', fontSize=11, leading=14, alignment=TA_LEFT)
    
    rujukan_table_data = [
        ['', Paragraph(f"Ruj. Kami: {no_ruj_format}", ruj_style)],
        ['', Paragraph(f"Tarikh: {tarikh_hari_ini}", ruj_style)]
    ]
    
    rujukan_table = Table(rujukan_table_data, colWidths=[298, 183])
    rujukan_table.setStyle(TableStyle([
        ('ALIGN', (1,0), (1,-1), 'LEFT'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    
    story.append(rujukan_table)
    story.append(Spacer(1, 16))

    # -------------------------------------------------------------
    # 2. PENERIMA & TAJUK SURAT
    # -------------------------------------------------------------
    nama_staf = str(staf_row.get('Nama', '')).upper()
    no_kp = mask_ic_number(str(staf_row.get('No_KP', '')).strip())

    story.append(Paragraph(f"<b>{nama_staf}</b>", bold_body))
    story.append(Paragraph(f"No. KP: {no_kp}", body_style))
    story.append(Spacer(1, 14))
    
    story.append(Paragraph("Tuan / Puan,", body_style))
    story.append(Spacer(1, 14))

    story.append(Paragraph(f"<b>{tajuk_surat_str}</b>", ParagraphStyle('TajukP', parent=bold_body, fontSize=11, leading=14)))
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # 3. KANDUNGAN BADAN SURAT
    # -------------------------------------------------------------
    p1 = "Dengan segala hormatnya perkara di atas adalah dirujuk bersama perkara-perkara berkaitan di bawah Akta Pendidikan 1996, Surat-surat Pekeliling Ikhtisas (SPI), serta arahan-arahan dan garis panduan yang berkuat kuasa."
    p2 = "2. Sukacita dimaklumkan bahawa pihak sekolah melantik tuan/puan untuk memegang jawatan dan melaksanakan amanah seperti butiran di bawah berkuat kuasa dari tarikh surat ini dikeluarkan sehingga ke suatu tarikh yang dimaklumkan kemudian."
    
    story.append(Paragraph(p1, body_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph(p2, body_style))
    
    # -------------------------------------------------------------
    # 4. KOTAK AGIHAN TUGAS (DIJAJARKAN KIRI PENUH & BERLANGKAU)
    # -------------------------------------------------------------
    
    # Pembersihan teks 'nan' dari Pandas DataFrame
    jawatan_val = str(staf_row.get('Jawatan', '')).replace('nan | ', '').replace('nan', '').strip()
    dtl_h = str(staf_row.get('Detail_H_1', '')).replace('nan', '').strip()
    kod_h = str(staf_row.get('Kod_H_1', '')).replace('nan', '').strip()
    
    if jawatan_val.startswith('| '):
        jawatan_val = jawatan_val[2:]
        
    jawatan_val = jawatan_val if jawatan_val else (dtl_h if dtl_h else "Guru Akademik Biasa")
    jawatan_full = f"{kod_h} | {jawatan_val}" if kod_h and kod_h not in jawatan_val else jawatan_val
    jawatan_full = jawatan_full.lstrip('| ').strip()

    # 2.1 JAWATAN BERPORTFOLIO 
    story.append(Spacer(1, 14))
    story.append(Paragraph(f"2.1. JAWATAN BERPORTFOLIO: {jawatan_full}", body_style))

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
            story.append(Paragraph(f"2.1.{sub_count}. Mengajar {sub_val}{cls_str} ({wkt_num} Waktu)", body_style))
            sub_count += 1

    # 2.2 PORTFOLIO TANPA JAWATAN 
    story.append(Spacer(1, 14))
    story.append(Paragraph("2.2. PORTFOLIO TANPA JAWATAN:", body_style))
    
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
            story.append(Paragraph(f"2.2.{p_count}. {label_p}{dtl_str}", body_style))
            p_count += 1
            
    if p_count == 1: 
        story.append(Paragraph("<i>Tiada Jawatan Tanpa Portfolio Ditetapkan</i>", body_style))

    # 2.3 JAWATANKUASA 
    story.append(Spacer(1, 14))
    story.append(Paragraph("2.3. JAWATANKUASA:", body_style))
    
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
            story.append(Paragraph(f"2.3.{j_count}. {label_j}{dtl_str}", body_style))
            j_count += 1
            
    if j_count == 1: 
        story.append(Paragraph("<i>Tiada Jawatankuasa Ditetapkan</i>", body_style))

    story.append(Spacer(1, 14))

    # -------------------------------------------------------------
    # 5. PENUTUP & TANDATANGAN
    # -------------------------------------------------------------
    p3 = "3. Sehubungan dengan itu, tuan/puan adalah dinasihatkan untuk merujuk dan memahami tugas serta tanggungjawab yang ditetapkan seperti yang dinyatakan dalam MySG KPM, Pekeliling dan SPI serta dokumen yang berkaitan."
    p4 = "4. Sebarang kecuaian dan ketidakakuran tuan/puan dalam menjalankan tugas-tugas tersebut, tuan/puan boleh dikenakan Tindakan di bawah Peraturan-peraturan Pegawai Awam (Kelakuan dan Tatatertib) 1993."
    p5 = "5. Semoga tuan/puan dapat menjalankan tugas yang diamanahkan dengan komitmen dan akauntabiliti yang tinggi."
    
    story.append(Paragraph(p3, body_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph(p4, body_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph(p5, body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Sekian, terima kasih.", body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>\"MALAYSIA MADANI\"</b>", bold_body))
    story.append(Paragraph("<b>\"BERKHIDMAT UNTUK NEGARA\"</b>", bold_body))
    story.append(Spacer(1, 14))

    story.append(Paragraph("Saya yang menjalankan amanah,", body_style))
    story.append(Spacer(1, 35))
    
    story.append(Paragraph(f"<b>{nama_gb}</b>", bold_body))
    story.append(Paragraph(f"{gelaran_gb}", body_style))
    story.append(Paragraph(f"{nama_sekolah.title()}", body_style))

    doc.build(story, canvasmaker=make_canvas)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
