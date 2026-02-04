import streamlit as st
import json
from utils.settings import load_settings


def save_settings(settings):
    with open("settings.json", 'w') as f:
        json.dump(settings, f, indent=2)


def show():
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

    st.subheader("📑 Tabs Management")

    functionalities = st.session_state.get('functionalities', {
        'Matrix Operations': 'matrix_tab.py',
        'ML Prediction': 'ml_tab.py',
        'Settings': 'settings_tab.py'
    })

    st.write("**Current tabs:**")

    # Display current tabs with delete option
    tabs_to_delete = []
    for tab_name, tab_file in list(functionalities.items()):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.text(f"• {tab_name} → {tab_file}")
        with col2:
            if st.button("🗑️", key=f"delete_tab_{tab_name}"):
                tabs_to_delete.append(tab_name)

    # Delete selected tabs
    for tab_name in tabs_to_delete:
        del functionalities[tab_name]
        st.session_state['functionalities'] = functionalities
        st.rerun()

    st.write("**Add new tab:**")

    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        new_tab_name = st.text_input(
            "Tab name:",
            placeholder="e.g., Data Analysis",
            key="new_tab_name"
        )

    with col2:
        new_tab_file = st.text_input(
            "Module file:",
            placeholder="e.g., data_analysis_tab.py",
            key="new_tab_file"
        )

    with col3:
        st.write("")  # Spacer
        st.write("")  # Spacer
        if st.button("➕ Add", type="secondary"):
            if new_tab_name and new_tab_file:
                if not new_tab_file.endswith('.py'):
                    st.error("File must end with .py")
                elif new_tab_name in functionalities:
                    st.error(f"Tab '{new_tab_name}' already exists!")
                else:
                    functionalities[new_tab_name] = new_tab_file
                    st.session_state['functionalities'] = functionalities
                    st.success(f"✅ Added '{new_tab_name}'!")
                    st.rerun()
            else:
                st.error("Both fields are required!")

    st.info("💡 Tip: Create the module file in `tabs/` folder before adding it here.")

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("💾 Save Settings to file", type="primary"):
            settings = {
                'decimal_places': st.session_state.get('decimal_places', 2),
                'theme': st.session_state.get('theme', 'dark'),
                'timeout': st.session_state.get('timeout', 30),
                'export_formats': st.session_state.get('export_formats', ['CSV', 'JSON', 'TXT']),
                'functionalities': st.session_state.get('functionalities', {
                    'Matrix Operations': 'matrix_tab.py',
                    'ML Prediction': 'ml_tab.py',
                    'Settings': 'settings_tab.py'
                })
            }
            save_settings(settings)
            st.success("Settings saved successfully!")

    with col2:
        if st.button("🔄 Restore Defaults"):
            defaults = {
                'decimal_places': 2,
                'theme': 'dark',
                'timeout': 30,
                'export_formats': ['CSV', 'JSON', 'TXT'],
                'functionalities': {
                    'Matrix Operations': 'matrix_tab.py',
                    'ML Prediction': 'ml_tab.py',
                    'Settings': 'settings_tab.py'
                }
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
                'export_formats': st.session_state.get('export_formats', ['CSV', 'JSON', 'TXT']),
                'functionalities': st.session_state.get('functionalities', {
                    'Matrix Operations': 'matrix_tab.py',
                    'ML Prediction': 'ml_tab.py',
                    'Settings': 'settings_tab.py'
                })
            }
            config_json = json.dumps(settings, indent=2)
            st.download_button(
                label="Download Config",
                data=config_json,
                file_name="mathio_config.json",
                mime="application/json"
            )

    st.markdown("---")
