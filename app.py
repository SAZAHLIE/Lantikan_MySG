"""
========================================================================
SISTEM PENGURUSAN & PENGIRAAN BEBAN KERJA KAKITANGAN SEKOLAH (MYSG KPM)
APP UTAMA - STREAMLIT ENTRY POINT (ZERO-SERVER-STORAGE COMPLIANT)
========================================================================
"""

import streamlit as st
from mysg_core import SYSTEM_NAME, SYSTEM_VERSION

st.set_page_config(
    page_title=SYSTEM_NAME,
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------------------------
# [BARU] SUNTIKAN CSS UNTUK NAIK TARAF UI (MESRA PENGGUNA)
# -------------------------------------------------------------------
st.markdown("""
<style>
    /* 1. SKALA FONT ASAS: Besarkan teks biasa untuk mudah dibaca */
    html, body, [class*="css"]  {
        font-size: 16px !important; 
    }

    /* 2. TAJUK (HEADERS): Lebih jelas dan berhierarki */
    h1 { font-size: 2.2rem !important; font-weight: 700 !important; }
    h2 { font-size: 1.8rem !important; font-weight: 600 !important; }
    h3 { font-size: 1.5rem !important; }

    /* 3. BUTANG TINDAKAN (CTA): Lebih besar, tebal, dan mudah diklik */
    .stButton > button {
        min-height: 50px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
    }
    
    /* Efek hover pada butang supaya lebih interaktif */
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-color: #ff4b4b !important;
        color: #ff4b4b !important;
    }

    /* 4. RUANG INPUT (Borang/Fail): Ketinggian ditambah untuk keselesaan */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stFileUploader {
        font-size: 15px !important;
        padding: 10px !important;
    }

    /* 5. RUANG BERNAFAS (Padding): Jarakkan elemen supaya tidak padat */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1200px !important; /* Hadkan lebar maksimum supaya kemas di skrin besar */
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# SEKATAN KLIK KANAN & PINTASAN PEMBANGUN (PENYUNTIKAN PARENT WINDOW)
# -------------------------------------------------------------------
st.components.v1.html("""
    <script>
    (function() {
        // Dapatkan rujukan kepada tetingkap utama pelayar (Parent Document)
        var targetDoc = window.parent ? window.parent.document : document;
        var targetWin = window.parent ? window.parent : window;

        // 1. Mematikan Menu Klik Kanan secara menyeluruh pada Parent Window
        function disableRightClick(e) {
            if (e.stopPropagation) e.stopPropagation();
            if (e.preventDefault) e.preventDefault();
            e.returnValue = false;
            return false;
        }

        targetDoc.addEventListener('contextmenu', disableRightClick, true);
        targetWin.addEventListener('contextmenu', disableRightClick, true);

        // 2. Mematikan Selection Teks & Dragging pada Pelayar
        targetDoc.addEventListener('selectstart', function(e) { e.preventDefault(); }, false);
        targetDoc.addEventListener('dragstart', function(e) { e.preventDefault(); }, false);

        // 3. Mematikan Pintasan Kekunci DevTools & View Source (F12, Ctrl+U, Ctrl+Shift+I, Ctrl+S)
        function disableShortcuts(e) {
            var evt = e || targetWin.event;
            var keyCode = evt.keyCode || evt.which;
            var ctrlOrCmd = evt.ctrlKey || evt.metaKey;

            // F12 Key
            if (keyCode === 123) {
                evt.preventDefault();
                return false;
            }

            if (ctrlOrCmd) {
                // Ctrl+U / Cmd+U (View Source)
                if (keyCode === 85) {
                    evt.preventDefault();
                    return false;
                }
                // Ctrl+S / Cmd+S (Save Page)
                if (keyCode === 83) {
                    evt.preventDefault();
                    return false;
                }
                // Ctrl+P / Cmd+P (Print Default Browser)
                if (keyCode === 80) {
                    evt.preventDefault();
                    return false;
                }
                // Ctrl+Shift+I / Ctrl+Shift+J / Ctrl+Shift+C (Inspect Elements)
                if (evt.shiftKey && (keyCode === 73 || keyCode === 74 || keyCode === 67)) {
                    evt.preventDefault();
                    return false;
                }
                // Cmd+Option+I (Safari / Mac DevTools)
                if (evt.altKey && (keyCode === 73 || keyCode === 74)) {
                    evt.preventDefault();
                    return false;
                }
            }
        }

        targetDoc.addEventListener('keydown', disableShortcuts, true);
        targetWin.addEventListener('keydown', disableShortcuts, true);
    })();
    </script>
""", height=0)

from page_1_requirements import render_page_1
from page_2_school_profile import render_page_2
from page_3_main_system import render_page_3
from navigation_component import render_navigation_bar
from footer_component import render_footer

def main():
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1

    current = st.session_state.current_step

    # 1. PAPARKAN KANDUNGAN HALAMAN
    if current == 1:
        render_page_1()
    elif current == 2:
        render_page_2()
    elif current == 3:
        render_page_3()

    # 2. PAPARKAN BAR NAVIGASI (DI ATAS FOOTER)
    render_navigation_bar(current_step=current, total_steps=3)

    # 3. PAPARKAN FOOTER RASMI
    render_footer()

if __name__ == "__main__":
    main()
