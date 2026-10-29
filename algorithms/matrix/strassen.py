# SPDX-License-Identifier: AGPL-3.0-only
"""Strassen's matrix multiplication in pure Python (no external dependencies).

Accepts nonempty, rectangular matrices of int/float values. The inputs remain
unchanged. Zero-padding lets the recursive core multiply arbitrary dimensions.

This implementation emphasizes correctness and readability over speed; for
real numerical work prefer optimized numerical computing libraries.
"""

from collections.abc import Sequence

Scalar = int | float
Matrix = list[list[Scalar]]


def _validate_matrix(
    values: Sequence[Sequence[Scalar]], name: str
) -> tuple[Matrix, int, int]:
    if not isinstance(values, (list, tuple)) or not values:
        raise ValueError(f"{name} must be a nonempty rectangular matrix")

    if not isinstance(values[0], (list, tuple)) or not values[0]:
        raise ValueError(f"{name} must have at least one column")

    cols = len(values[0])
    result: Matrix = []
    for row in values:
        if not isinstance(row, (list, tuple)) or len(row) != cols:
            raise ValueError(f"{name} has ragged rows or an invalid row")
        if not all(isinstance(element, (int, float)) for element in row):
            raise TypeError(f"{name} entries must be int or float")
        result.append(list(row))

    return result, len(result), cols


def _prepare(
    left: Sequence[Sequence[Scalar]],
    right: Sequence[Sequence[Scalar]],
) -> tuple[Matrix, Matrix, int, int, int]:
    a, rows, inner = _validate_matrix(left, "left")
    b, right_rows, cols = _validate_matrix(right, "right")
    if inner != right_rows:
        raise ValueError(
            f"incompatible matrix shapes: {rows}x{inner} and {right_rows}x{cols}"
        )
    return a, b, rows, inner, cols


def _naive_square(a: Matrix, b: Matrix) -> Matrix:
    """Multiply two equally sized square matrices without shape checks."""
    n = len(a)
    result: Matrix = [[0] * n for _ in range(n)]
    for row in range(n):
        for inner in range(n):
            for col in range(n):
                result[row][col] += a[row][inner] * b[inner][col]
    return result


def naive_multiply(
    left: Sequence[Sequence[Scalar]],
    right: Sequence[Sequence[Scalar]],
) -> Matrix:
    """Conventional O(mkn) matrix multiplication; used as a reference."""
    a, b, rows, inner, cols = _prepare(left, right)
    result: Matrix = [[0] * cols for _ in range(rows)]
    for row in range(rows):
        for k in range(inner):
            for col in range(cols):
                result[row][col] += a[row][k] * b[k][col]
    return result


def _add(a: Matrix, b: Matrix) -> Matrix:
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def _subtract(a: Matrix, b: Matrix) -> Matrix:
    return [[x - y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def _quadrants(a: Matrix) -> tuple[Matrix, Matrix, Matrix, Matrix]:
    half = len(a) // 2
    return (
        [row[:half] for row in a[:half]],
        [row[half:] for row in a[:half]],
        [row[:half] for row in a[half:]],
        [row[half:] for row in a[half:]],
    )


def _combine(c11: Matrix, c12: Matrix, c21: Matrix, c22: Matrix) -> Matrix:
    top = [left + right for left, right in zip(c11, c12)]
    bottom = [left + right for left, right in zip(c21, c22)]
    return top + bottom


def _strassen_square(a: Matrix, b: Matrix, cutoff: int) -> Matrix:
    n = len(a)
    if n <= cutoff:
        return _naive_square(a, b)

    a11, a12, a21, a22 = _quadrants(a)
    b11, b12, b21, b22 = _quadrants(b)

    # Seven recursive products instead of eight in ordinary block splitting.
    m1 = _strassen_square(_add(a11, a22), _add(b11, b22), cutoff)
    m2 = _strassen_square(_add(a21, a22), b11, cutoff)
    m3 = _strassen_square(a11, _subtract(b12, b22), cutoff)
    m4 = _strassen_square(a22, _subtract(b21, b11), cutoff)
    m5 = _strassen_square(_add(a11, a12), b22, cutoff)
    m6 = _strassen_square(_subtract(a21, a11), _add(b11, b12), cutoff)
    m7 = _strassen_square(_subtract(a12, a22), _add(b21, b22), cutoff)

    c11 = _add(_subtract(_add(m1, m4), m5), m7)
    c12 = _add(m3, m5)
    c21 = _add(m2, m4)
    c22 = _add(_add(_subtract(m1, m2), m3), m6)
    return _combine(c11, c12, c21, c22)


def strassen_multiply(
    left: Sequence[Sequence[Scalar]],
    right: Sequence[Sequence[Scalar]],
    *,
    cutoff: int = 32,
) -> Matrix:
    """Return matrix multiplication of left (m x k) and right (k x n).

    For square power-of-two matrices above cutoff, the recursive core has
    O(n**log2(7)) scalar arithmetic complexity under the standard model.
    All other shapes are zero-padded to a square with power-of-two side length,
    then cropped back to m x n. Padding can be expensive for skinny inputs.

    Does not modify either input. Only int/float elements are supported.
    Floating-point results may have different rounding than naive_multiply.
    Empty, ragged, or incompatible matrices raise ValueError.
    """
    if isinstance(cutoff, bool) or not isinstance(cutoff, int) or cutoff < 1:
        raise ValueError("cutoff must be a positive integer")

    a, b, rows, inner, cols = _prepare(left, right)
    maximum = max(rows, inner, cols)
    size = 1 << (maximum - 1).bit_length()

    padded_a: Matrix = [[0] * size for _ in range(size)]
    padded_b: Matrix = [[0] * size for _ in range(size)]

    for row in range(rows):
        padded_a[row][:inner] = a[row]
    for row in range(inner):
        padded_b[row][:cols] = b[row]

    product = _strassen_square(padded_a, padded_b, cutoff)
    return [row[:cols] for row in product[:rows]]


if __name__ == "__main__":
    a = [[1, 2], [3, 4]]
    b = [[5, 6], [7, 8]]
    print("A × B =", strassen_multiply(a, b, cutoff=1))
