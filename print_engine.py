"""
========================================================================
MYSG KPM: ENJIN PENCETAKAN & PENJANAAN DOKUMEN RASMI A4 (GATEWAY)
========================================================================
"""

import pandas as pd
from print_individual import generate_appointment_letter_html, generate_individual_detailed_report_html
from print_comparison import generate_detailed_comparison_html
from print_workload import generate_simple_workload_report_html

def generate_printable_html(arg1, arg2=None, arg3=None, arg4=None, *args, **kwargs):
    """Fungsi penyesuai fleksibel bagi mengalirkan laporan terus vs laporan bandingan."""
    if isinstance(arg1, pd.DataFrame):
        # Menerima pemanggilan Laporan Beban Kerja Terus
        return generate_simple_workload_report_html(arg1, title=arg2, school_info=arg3, *args, **kwargs)
    else:
        return generate_individual_detailed_report_html(arg1, school_info=arg2, *args, **kwargs)
