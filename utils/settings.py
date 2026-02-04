from pathlib import Path
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
        'export_formats': ['CSV', 'JSON', 'TXT'],
        'functionalities': {
            'Matrix Operations': 'matrix_tab.py',
            'ML Prediction': 'ml_tab.py',
            'Settings': 'settings_tab.py'
        }
    }
