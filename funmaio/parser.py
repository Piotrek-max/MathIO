import numpy as np


def text_to_numpy(text: str) -> np.ndarray | str:
    try:
        text = text.strip().replace(',', ' ')
        matrix = []
        for line in text.split('\n'):
            row = list(map(float, line.split()))
            matrix.append(row)
        return np.array(matrix)
    except:
        return 'Invalid matrix format'


def numpy_to_text(matrix: np.ndarray, decimals: int = 4) -> str:
    result = []
    for row in matrix:
        formatted_row = ' '.join([f"{num:10.{decimals}f}" for num in row])
        result.append(formatted_row)
    return '\n'.join(result)


