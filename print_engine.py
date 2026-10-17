"""
========================================================================
MYSG KPM: ENJIN PENCETAKAN & PENJANAAN DOKUMEN RASMI A4 (GATEWAY)
========================================================================
"""

import pandas as pd
from print_individual import generate_appointment_letter_html, generate_individual_detailed_report_html
from print_comparison import generate_detailed_comparison_html

def generate_printable_html(arg1, arg2=None, arg3=None, arg4=None, *args, **kwargs):
    """Fungsi penyesuai fleksibel bagi mengekalkan keserasian modul lama seperti tab_2_staff_management.py."""
    if isinstance(arg1, pd.DataFrame):
        return generate_detailed_comparison_html(arg1, title=arg2, school_info=arg3, session_state=arg4, *args, **kwargs)
    else:
        return generate_individual_detailed_report_html(arg1, school_info=arg2, *args, **kwargs)