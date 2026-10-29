# SPDX-License-Identifier: AGPL-3.0-only
"""Strassen 乘法：递归、补零、矩形尺寸、数值与错误输入的回归验证。"""

import math
import random

import pytest

from algorithms.matrix.strassen import naive_multiply, strassen_multiply


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        ([[2]], [[3]], [[6]]),
        ([[1, 2], [3, 4]], [[5, 6], [7, 8]], [[19, 22], [43, 50]]),
        ([[0, 0], [0, 0]], [[3, 4], [5, 6]], [[0, 0], [0, 0]]),
        ([[1, 2, 3]], [[4], [5], [6]], [[32]]),
        ([[1], [2], [3]], [[4, 5]], [[4, 5], [8, 10], [12, 15]]),
        ([[-1, 2], [3, -4]], [[5, -6], [-7, 8]], [[-19, 22], [43, -50]]),
        ([[1, 2, 3], [4, 5, 6]], [[7, 8], [9, 10], [11, 12]], [[58, 64], [139, 154]]),
    ],
)
@pytest.mark.parametrize("cutoff", [1, 2, 8, 32])
def test_example_products(left, right, expected, cutoff) -> None:
    original_a, original_b = [row[:] for row in left], [row[:] for row in right]
    assert strassen_multiply(left, right, cutoff=cutoff) == expected
    assert naive_multiply(left, right) == expected
    assert left == original_a and right == original_b


def test_randomized_rectangular_and_square_matrices() -> None:
    rng = random.Random(20261029)
    for rows, inner, cols in [
        (1, 1, 1), (1, 9, 1), (3, 5, 2),
        (5, 3, 7), (6, 6, 6), (7, 8, 5),
        (8, 8, 8), (9, 7, 11), (16, 16, 16),
        (33, 33, 33),
    ]:
        left = [[rng.randint(-10, 10) for _ in range(inner)] for _ in range(rows)]
        right = [[rng.randint(-10, 10) for _ in range(cols)] for _ in range(inner)]
        expected = naive_multiply(left, right)
        for cutoff in (1, 8, 32):
            assert strassen_multiply(left, right, cutoff=cutoff) == expected


@pytest.mark.parametrize(
    ("left", "right"),
    [
        ([[0.5, -1.25], [2.0, 3.5]], [[3.0, 2.5], [1.5, 4.0]]),
        ([[1.3, -4.1, 9.7]], [[0.25], [-2.0], [3.0]]),
    ],
)
def test_floating_point_with_tolerance(left, right) -> None:
    expected = naive_multiply(left, right)
    actual = strassen_multiply(left, right, cutoff=1)
    for actual_row, expected_row in zip(actual, expected):
        for x, y in zip(actual_row, expected_row):
            assert math.isclose(x, y, rel_tol=1e-12, abs_tol=1e-12)


@pytest.mark.parametrize(
    ("left", "right"),
    [
        ([], [[1]]),
        ([[1]], []),
        ([[]], [[1]]),
        ([[1]], [[]]),
        ([[1], [2, 3]], [[4], [5]]),
        ([[1, 2]], [[3, 4]]),
        ([[1], [2]], [[1], [2], [3]]),
    ],
)
def test_invalid_shapes(left, right) -> None:
    with pytest.raises(ValueError):
        strassen_multiply(left, right)
    with pytest.raises(ValueError):
        naive_multiply(left, right)


@pytest.mark.parametrize("bad", [0, -1, 1.5, "2", None, True])
def test_invalid_cutoff(bad) -> None:
    with pytest.raises(ValueError, match="cutoff"):
        strassen_multiply([[1]], [[2]], cutoff=bad)


@pytest.mark.parametrize("bad", ["text", None, 2 + 3j, object()])
def test_rejects_non_numeric_entries(bad) -> None:
    with pytest.raises(TypeError, match="int or float"):
        strassen_multiply([[bad]], [[1]])
    with pytest.raises(TypeError, match="int or float"):
        naive_multiply([[1]], [[bad]])


def test_tuple_rows_are_accepted_and_unmodified() -> None:
    a = ((1, 2), (3, 4))
    b = ((5, 6), (7, 8))
    assert strassen_multiply(a, b, cutoff=1) == [[19, 22], [43, 50]]
    assert a == ((1, 2), (3, 4))


def test_large_rectangular_padding() -> None:
    a = [[1, 0, -1] for _ in range(17)]
    b = [[2, 3], [4, 5], [6, 7]]
    assert strassen_multiply(a, b, cutoff=8) == [[-4, -4] for _ in range(17)]
