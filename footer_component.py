"""
========================================================================
MYSG KPM: SISTEM PENGURUSAN & ANALISIS BEBAN KERJA
MODULE: FOOTER COMPONENT (KAD FOOTER RASMI BERSIH UNTUK SEMUA HALAMAN)
========================================================================
"""

import streamlit as st
import os
import base64

try:
    from mysg_core import SYSTEM_NAME, SYSTEM_VERSION, SYSTEM_RELEASE_DATE
except ImportError:
    SYSTEM_NAME = "MySG KPM: Sistem Pengurusan & Analisis Beban Kerja"
    SYSTEM_VERSION = "1.0.0"
    SYSTEM_RELEASE_DATE = "18 Oktober 2026"

def get_logo_s_base64():
    """Mengambil logo S dalam format Base64 untuk dipaparkan dalam HTML."""
    possible_paths = [
        "logo.png",
        os.path.join(os.getcwd(), "logo.png"),
        os.path.join(os.path.dirname(__file__), "logo.png")
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    return f"data:image/png;base64,{encoded_string}"
            except Exception:
                pass
                
    return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOxAAADsQBlSsOGwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBo="

def render_footer():
    """Menjana kad footer rasmi seragam untuk semua halaman sistem (1, 2, dan 3)."""
    logo_s_b64 = get_logo_s_base64()
    
    st.markdown("<br><hr style='border:none; border-top:1px solid #e2e8f0; margin-top:30px; margin-bottom:20px;'>", unsafe_allow_html=True)
    
    footer_html = f"""<div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-left: 5px solid #2563eb; border-radius: 12px; padding: 16px 24px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02); display: flex; align-items: center; justify-content: space-between; gap: 16px; font-family: Arial, sans-serif;">
<div style="flex: 0 0 75px; display: flex; align-items: center; justify-content: center;">
<img src="{logo_s_b64}" style="height: 48px; width: auto; max-width: 60px; object-fit: contain;" alt="Logo S">
</div>
<div style="flex: 1; text-align: center; padding: 0 10px;">
<h4 style="margin: 0 0 5px 0; font-size: 14px; color: #0f172a; font-weight: 800; letter-spacing: -0.2px; line-height: 1.3;">{SYSTEM_NAME}</h4>
<div style="display: flex; justify-content: center; align-items: center; gap: 8px; margin-bottom: 5px; flex-wrap: wrap;">
<span style="background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%); color: #ffffff; font-size: 10px; font-weight: 700; padding: 2px 10px; border-radius: 12px; letter-spacing: 0.5px; display: inline-block; box-shadow: 0 1px 3px rgba(37, 99, 235, 0.2);">VERSI RASMI v{SYSTEM_VERSION}</span>
<span style="background-color: #d97706; color: #ffffff; font-size: 10px; font-weight: 700; padding: 2px 10px; border-radius: 12px;">📅 DIJANA: {SYSTEM_RELEASE_DATE}</span>
<span style="background-color: #059669; color: #ffffff; font-size: 10px; font-weight: 700; padding: 2px 10px; border-radius: 12px;">🔒 ZERO-CLOUD STORAGE (PDPA COMPLIANT)</span>
</div>
<p style="margin: 0; font-size: 11px; color: #64748b; line-height: 1.4;">Hak Cipta Terpelihara &copy; 2026 &bull; Rekaan &amp; Seni Bina Perisian Oleh <b style="color: #1e3a8a;">Sazahlie S.</b></p>
<p style="margin: 2px 0 0 0; font-size: 10px; color: #94a3b8; font-style: italic;">Inisiatif Bebas: Alat Bantu Pentadbiran Sekolah. Tidak mewakili secara rasmi mana-mana agensi kerajaan.</p>
</div>
<div style="flex: 0 0 auto; display: flex; align-items: center; justify-content: center;">
<a href="mailto:sazahlie.sapar@moe.edu.my" style="background-color: #0066ff; border: none; color: #ffffff; padding: 7px 18px; border-radius: 20px; font-size: 12px; font-weight: 700; text-decoration: none; display: inline-flex; align-items: center; gap: 6px; box-shadow: 0 2px 6px rgba(0, 102, 255, 0.25); white-space: nowrap;">📩 sazahlie.sapar@moe.edu.my</a>
</div>
</div>"""
    
    if hasattr(st, "html"):
        st.html(footer_html)
    else:
        st.markdown(footer_html, unsafe_allow_html=True)
