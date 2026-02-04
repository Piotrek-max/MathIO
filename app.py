import streamlit as st
from pathlib import Path
from utils.settings import load_settings
import importlib


st.set_page_config(
    page_title="MathIO",
    page_icon="assets/favico.ico",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'settings_loaded' not in st.session_state:
    settings = load_settings()
    st.session_state.update(settings)
    st.session_state['settings_loaded'] = True

theme = st.session_state.get('theme', 'dark')


st.title("MathIO - Mathematical Operations & ML")
st.markdown("---")

with st.sidebar:
    logo = str(Path("assets/logo_color.png"))
    if logo:
        st.image(logo, width=180)
    else:
        st.warning("Logo not found")

    st.markdown("---")

    st.header("📋 Menu")

    functionalities = st.session_state.get('functionalities')

    menu_tabs = {k: v for k, v in functionalities.items() if k != 'Settings'}

    tab_items = list(menu_tabs.items())
    first_five = tab_items[:5]
    remaining = tab_items[5:]

    if 'selected_tab' not in st.session_state:
        st.session_state['selected_tab'] = tab_items[0][0] if tab_items else None

    for tab_name, tab_file in first_five:
        if st.button(tab_name, key=f"btn_{tab_name}", use_container_width=True):
            st.session_state['selected_tab'] = tab_name
            st.session_state['show_settings'] = False
            st.rerun()

    if remaining:
        st.markdown("**More:**")
        more_tabs = dict(remaining)
        selected_more = st.selectbox(
            "More tabs:",
            options=[""] + list(more_tabs.keys()),
            label_visibility="collapsed",
            key="more_tabs_select"
        )
        if selected_more:
            st.session_state['selected_tab'] = selected_more
            st.session_state['show_settings'] = False
            st.rerun()

    st.markdown("---")

    # Settings button in sidebar
    if st.button("⚙️ Settings", use_container_width=True):
        st.session_state['show_settings'] = True
        st.rerun()

# Show Settings page or selected tab
if st.session_state.get('show_settings', False):
    from tabs import settings_tab
    st.header("⚙️ Settings")
    settings_tab.show()
else:
    selected_tab = st.session_state.get('selected_tab')
    module_file = menu_tabs.get(selected_tab)
    if module_file:
        try:
            module_name = module_file.replace('.py', '')
            module = importlib.import_module(f'tabs.{module_name}')
            module.show()
        except Exception as e:
            st.error(f"Error loading tab '{selected_tab}': {e}")
    else:
        st.error(f"Tab '{selected_tab}' not found in settings!")

