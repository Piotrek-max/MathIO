from pathlib import Path
import json


def load_settings():
    settings_file = Path("settings.json")
    if settings_file.exists():
        with open(settings_file, 'r') as f:
            return json.load(f)
    return {
        'decimal_places': 2,
        'timeout': 30,
        'export_formats': ['CSV', 'JSON', 'TXT'],
        'functionalities': {
            'Matrix Operations': 'matrix_tab.py',
            'ML Prediction': 'ml_tab.py',
            'Settings': 'settings_tab.py'
        }
    }


def save_settings(settings):
    with open("settings.json", 'w') as f:
        json.dump(settings, f, indent=2)


DEFAULT_SETTINGS = {
    'decimal_places': 2,
    'timeout': 30,
    'export_formats': ['CSV', 'JSON', 'TXT'],
    'functionalities': {
        'Matrix Operations': 'matrix_tab.py',
        'Statistical ML': 'ml_tab.py',
        'Settings': 'settings_tab.py',
        'Models Management': 'mm_tab.py'
        # TODO Features
        # 'File dataset preparation': 'ml_tab.py',
        # 'Data view': 'dv_tab.py',

    }
}
