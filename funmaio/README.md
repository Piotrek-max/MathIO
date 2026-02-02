# FunMaIO - Matrix Operations Library

A simple and efficient library for matrix operations using NumPy.

## Modules

### parser.py
Handles conversion between text and NumPy arrays.

**Functions:**
- `text_to_numpy(text: str) -> np.ndarray | str`
  - Converts text input to NumPy array
  - Accepts space or comma-separated values
  - Returns error message string if parsing fails

- `numpy_to_text(matrix: np.ndarray, decimals: int = 4) -> str`
  - Converts NumPy array to formatted text
  - Customizable decimal precision
  - Returns nicely formatted string representation

### operations.py
Matrix mathematical operations.

**Functions:**

- `multiply(a: np.ndarray, b: np.ndarray) -> np.ndarray | str`
  - Matrix multiplication A × B
  - Validates dimensions compatibility
  
- `inverse(a: np.ndarray) -> np.ndarray | str`
  - Calculates inverse matrix A⁻¹
  - Checks for square matrix and non-zero determinant
  
- `determinant(a: np.ndarray) -> float | str`
  - Calculates matrix determinant
  - Only for square matrices
  
- `transpose(a: np.ndarray) -> np.ndarray`
  - Matrix transpose Aᵀ
  
- `add(a: np.ndarray, b: np.ndarray) -> np.ndarray | str`
  - Matrix addition A + B
  - Requires same dimensions
  
- `subtract(a: np.ndarray, b: np.ndarray) -> np.ndarray | str`
  - Matrix subtraction A - B
  - Requires same dimensions
  
- `eigenvalues(a: np.ndarray) -> np.ndarray | str`
  - Calculates eigenvalues
  - Only for square matrices
  
- `rank(a: np.ndarray) -> int`
  - Matrix rank calculation

## Usage Example

```python
from funmaio.parser import text_to_numpy, numpy_to_text
from funmaio.operations import multiply, inverse

text_a = "1 2 3\n4 5 6\n7 8 9"
text_b = "9 8 7\n6 5 4\n3 2 1"

a = text_to_numpy(text_a)
b = text_to_numpy(text_b)

result = multiply(a, b)
print(numpy_to_text(result, decimals=2))
```


