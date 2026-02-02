import numpy as np


def multiply(a: np.ndarray, b: np.ndarray) -> np.ndarray | str:
    try:
        if a.shape[1] != b.shape[0]:
            return 'Matrix dimensions incompatible for multiplication'
        return np.matmul(a, b)
    except Exception as e:
        return f'Multiplication error: {str(e)}'


def inverse(a: np.ndarray) -> np.ndarray | str:
    try:
        if a.shape[0] != a.shape[1]:
            return 'Matrix must be square'
        det = np.linalg.det(a)
        if abs(det) < 1e-10:
            return 'Matrix is singular (determinant = 0)'
        return np.linalg.inv(a)
    except Exception as e:
        return f'Inverse error: {str(e)}'


def determinant(a: np.ndarray) -> float | str:
    try:
        if a.shape[0] != a.shape[1]:
            return 'Matrix must be square'
        return np.linalg.det(a)
    except Exception as e:
        return f'Determinant error: {str(e)}'


def transpose(a: np.ndarray) -> np.ndarray:
    return np.transpose(a)


def add(a: np.ndarray, b: np.ndarray) -> np.ndarray | str:
    try:
        if a.shape != b.shape:
            return 'Matrices must have the same dimensions'
        return a + b
    except Exception as e:
        return f'Addition error: {str(e)}'


def subtract(a: np.ndarray, b: np.ndarray) -> np.ndarray | str:
    try:
        if a.shape != b.shape:
            return 'Matrices must have the same dimensions'
        return a - b
    except Exception as e:
        return f'Subtraction error: {str(e)}'


def eigenvalues(a: np.ndarray) -> np.ndarray | str:
    try:
        if a.shape[0] != a.shape[1]:
            return 'Matrix must be square'
        return np.linalg.eigvals(a)
    except Exception as e:
        return f'Eigenvalues error: {str(e)}'


def rank(a: np.ndarray) -> int:
    return np.linalg.matrix_rank(a)

