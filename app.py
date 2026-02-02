import streamlit as st
from pathlib import Path
from tabs import matrix_tab, ml_tab, settings_tab
import json


def load_settings():
    settings_file = Path("settings.json")
    if settings_file.exists():
        with open(settings_file, 'r') as f:
            return json.load(f)
    return {
        'decimal_places': 2,
        'theme': 'dark',
        'timeout': 30,
        'export_formats': ['CSV', 'JSON', 'TXT']
    }


st.set_page_config(
    page_title="MathIO",
    page_icon="static/favico.ico",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'settings_loaded' not in st.session_state:
    settings = load_settings()
    st.session_state.update(settings)
    st.session_state['settings_loaded'] = True

theme = st.session_state.get('theme', 'dark')

def load_logo():
    logo_path = Path("static/logo_color.png")
    if logo_path.exists():
        return str(logo_path)
    return None


st.title("MathIO - Mathematical Operations & ML")
st.markdown("---")

with st.sidebar:
    logo = load_logo()
    if logo:
        st.image(logo, width=180)
    else:
        st.warning("Logo not found")

    st.markdown("---")

    st.header("📋 Menu")
    st.write("Select tab:")

    option = st.selectbox(
        "Options",
        ["Matrix Operations", "ML Predictions", "Settings"],
        label_visibility="collapsed"
    )

if option == "Matrix Operations":
    matrix_tab.show()
elif option == "ML Predictions":
    ml_tab.show()
elif option == "Settings":
    settings_tab.show()



