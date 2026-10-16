
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
