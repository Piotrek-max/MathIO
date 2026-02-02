# MathIO - Project Structure

## 📁 Folder Structure

```
MathIO/
├── app.py                          # Main Streamlit application
├── funmaio/                        # Matrix operations library
│   ├── __init__.py                # Module initialization
│   ├── parser.py                  # Text ↔ NumPy conversion
│   └── operations.py              # Matrix calculations
├── tabs/                           # Application tabs
│   ├── __init__.py                # Module initialization
│   ├── matrix_tab.py              # Matrix operations tab
│   ├── ml_tab.py                  # ML predictions tab
│   └── settings_tab.py            # Settings tab
├── static/                         # Static assets
│   ├── favico.ico
│   ├── logo_color.png
│   └── styles.css
└── models/                         # ML models
```

## 🚀 How to Run

```bash
streamlit run app.py
```

## 📝 How to Add New Tab

1. Create new file in `tabs/` folder, e.g. `new_tab.py`
2. Implement `show()` function:

```python
import streamlit as st

def show():
    st.header("New Tab")
    st.write("Tab content...")
```

3. Import tab in `app.py`:

```python
from tabs import matrix_tab, ml_tab, settings_tab, new_tab
```

4. Add option in selectbox and routing:

```python
option = st.selectbox(
    "Options",
    ["Matrix Operations", "ML Predictions", "Settings", "New Tab"]
)

elif option == "New Tab":
    new_tab.show()
```

## 🔧 Available Functions

### funmaio/parser.py

- `text_to_numpy(text: str)` - converts text to NumPy array
- `numpy_to_text(matrix: np.ndarray, decimals: int)` - converts NumPy array to formatted text

### funmaio/operations.py

- `multiply(a, b)` - matrix multiplication
- `inverse(a)` - inverse matrix
- `determinant(a)` - determinant
- `transpose(a)` - transpose
- `add(a, b)` - matrix addition
- `subtract(a, b)` - matrix subtraction
- `eigenvalues(a)` - eigenvalues
- `rank(a)` - matrix rank

## 📋 Tabs

### 1. Matrix Operations (`matrix_tab.py`)
- Matrix multiplication
- Inverse matrix

### 2. ML Predictions (`ml_tab.py`)
- Linear regression
- Classification
- Clustering

### 3. Settings (`settings_tab.py`)
- Display configuration
- Calculation settings
- Data export


