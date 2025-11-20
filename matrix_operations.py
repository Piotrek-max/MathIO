def transfrom_text_to_matrix(text: str) -> list | str:
    matrix = []
    text.strip()
    text = text.replace(',', ' ')
    for line in text.split('\n'):
        try:
            matrix.append(list(map(float, line.split())))
        except:
            return 'Matrix is not correct'
    return matrix

def check_if_matrix_multiplication_is_correct(matrix_1: list,matrix_2) -> bool:
    rows = len(matrix_1[0])
    columns = len(matrix_2)
    print(rows, columns)
    if rows==columns:
        for i in range(len(matrix_2[0])):
            if len(matrix_1[i]) != rows:
                return False
    else:
        return False
    return True

def multiply_matrix(matrix1: list, matrix2: list) -> list | str:
    result = []
    if check_if_matrix_multiplication_is_correct(matrix1, matrix2):
        for i in range(len(matrix1)):
            result.append([])
            for j in range(len(matrix2[0])):
                result[i].append(0)
                for k in range(len(matrix2)):
                    result[i][j] += matrix1[i][k] * matrix2[k][j]

    else:
        return 'Matrix multiplication is not possible'
    return result



def multiply_matrix_end(text1, text2):
    matrix1 = transfrom_text_to_matrix(text1)
    matrix2 = transfrom_text_to_matrix(text2)
    if matrix1 == 'Matrix is not correct' or matrix2 == 'Matrix is not correct':
        return 'Matrix is not correct'
    result = multiply_matrix(matrix1, matrix2)
    return result

def determinant(matrix: list) -> float:
    """Rekurencyjne liczenie wyznacznika macierzy."""
    n = len(matrix)

    # 1×1
    if n == 1:
        return matrix[0][0]

    # 2×2
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    # większe macierze — rozwinięcie Laplace’a
    det = 0
    for c in range(n):
        # minor
        sub = [row[:c] + row[c+1:] for row in matrix[1:]]
        det += ((-1) ** c) * matrix[0][c] * determinant(sub)
    return det


def matrix_of_minors(matrix: list) -> list:
    """Macierz minorów."""
    n = len(matrix)
    minors = []

    for i in range(n):
        minors.append([])
        for j in range(n):
            # macierz bez wiersza i i kolumny j
            sub = [row[:j] + row[j+1:] for k, row in enumerate(matrix) if k != i]
            minors[i].append(determinant(sub))
    return minors


def cofactor_matrix(matrix: list) -> list:
    """Macierz kofaktorów."""
    n = len(matrix)
    minors = matrix_of_minors(matrix)

    for i in range(n):
        for j in range(n):
            minors[i][j] *= (-1) ** (i + j)

    return minors


def transpose(matrix: list) -> list:
    """Transpozycja macierzy."""
    return [list(row) for row in zip(*matrix)]


def inverse_matrix(matrix: list) -> list | str:
    """Macierz odwrotna A⁻¹ = 1/det(A) * adj(A)."""
    # sprawdzenie kwadratowej
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        return "Matrix is not square"

    det = determinant(matrix)
    if det == 0:
        return "Matrix is singular (det = 0)"

    cof = cofactor_matrix(matrix)
    adj = transpose(cof)

    inv = []
    for row in adj:
        inv.append([x / det for x in row])

    return inv


def inverse_matrix_end(text):
    matrix = transfrom_text_to_matrix(text)
    if matrix == 'Matrix is not correct':
        return 'Matrix is not correct'

    result = inverse_matrix(matrix)
    return result
