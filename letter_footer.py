"""
========================================================================
MYSG KPM: MODUL KHAS FOOTER SURAT LANTIKAN (A4 PORTRAIT)
========================================================================
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