import streamlit as st
import json
from pathlib import Path


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


def save_settings(settings):
    with open("settings.json", 'w') as f:
        json.dump(settings, f, indent=2)


def show():
    st.header("Settings")
    st.write("Configure the application according to your needs.")

    if 'settings_loaded' not in st.session_state:
        settings = load_settings()
        st.session_state.update(settings)
        st.session_state['settings_loaded'] = True

    st.markdown("---")

    st.subheader("🎨 Display")

    theme = st.selectbox(
        "Display theme:",
        ["Light", "Dark", "Auto"],
        index=["Light", "Dark", "Auto"].index(st.session_state.get('theme', 'Dark').title())
    )
    st.session_state['theme'] = theme.lower()

    st.markdown("---")

    st.subheader("⚙️ Calculations")

    col1, col2 = st.columns(2)

    with col1:
        decimal_places = st.slider(
            "Decimal places in results:",
            min_value=0,
            max_value=10,
            value=st.session_state.get('decimal_places', 2)
        )
        st.session_state['decimal_places'] = decimal_places

    with col2:
        timeout = st.number_input(
            "Calculation timeout (seconds):",
            min_value=1,
            max_value=300,
            value=st.session_state.get('timeout', 30)
        )
        st.session_state['timeout'] = timeout

    st.markdown("---")

    st.subheader("💾 Data Export")

    export_format = st.multiselect(
        "Available export formats:",
        ["CSV", "JSON", "TXT"],
        default=st.session_state.get('export_formats', ["CSV", "JSON", "TXT"])
    )
    st.session_state['export_formats'] = export_format

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("💾 Save Settings", type="primary"):
            settings = {
                'decimal_places': st.session_state.get('decimal_places', 2),
                'theme': st.session_state.get('theme', 'dark'),
                'timeout': st.session_state.get('timeout', 30),
                'export_formats': st.session_state.get('export_formats', ['CSV', 'JSON', 'TXT'])
            }
            save_settings(settings)
            st.success("Settings saved successfully!")

    with col2:
        if st.button("🔄 Restore Defaults"):
            defaults = {
                'decimal_places': 2,
                'theme': 'dark',
                'timeout': 30,
                'export_formats': ['CSV', 'JSON', 'TXT']
            }
            st.session_state.update(defaults)
            save_settings(defaults)
            st.rerun()

    with col3:
        if st.button("📤 Export Configuration"):
            settings = {
                'decimal_places': st.session_state.get('decimal_places', 2),
                'theme': st.session_state.get('theme', 'dark'),
                'timeout': st.session_state.get('timeout', 30),
                'export_formats': st.session_state.get('export_formats', ['CSV', 'JSON', 'TXT'])
            }
            config_json = json.dumps(settings, indent=2)
            st.download_button(
                label="Download Config",
                data=config_json,
                file_name="mathio_config.json",
                mime="application/json"
            )

    st.markdown("---")

    with st.expander("ℹ️ About"):
        st.write("""
        **MathIO v0.2**
        
        Application for matrix operations and ML predictions.
        
        - 🔢 Matrix operations
        - 🤖 Machine Learning
        - 📊 Visualizations
        - 💾 Data export
        
        Built with Streamlit and Python.
        """)

