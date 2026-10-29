# SPDX-License-Identifier: AGPL-3.0-only
"""Karatsuba multiplication: a divide-and-conquer algorithm for integers.

This educational implementation uses binary splitting, not decimal-string
conversion. Python's built-in multiplication handles small base cases.
"""

_BASE_CASE_BITS = 64


def karatsuba(x: int, y: int) -> int:
    """Multiply two integers using the Karatsuba algorithm.

    Supports zero, negatives, unequal bit lengths, and arbitrarily large Python
    integers. For normal Python code prefer built-in multiplication.

    Args:
        x: First integer.
        y: Second integer.

    Returns:
        The exact product, equal to x * y.

    Raises:
        TypeError: If either operand is not an integer.

    Note:
        bool counts as an int, consistent with Python arithmetic.
    """
    if not isinstance(x, int) or not isinstance(y, int):
        raise TypeError("karatsuba() expects two integers")

    if x == 0 or y == 0:
        return 0

    result = _multiply_nonnegative(abs(x), abs(y))
    return -result if (x < 0) != (y < 0) else result


def _multiply_nonnegative(x: int, y: int) -> int:
    """Multiply nonnegative integers; all recursive calls meet this contract."""
    if x == 0 or y == 0:
        return 0

    bits = max(x.bit_length(), y.bit_length())
    if bits <= _BASE_CASE_BITS:
        return x * y

    half = bits // 2
    mask = (1 << half) - 1
    x_high, x_low = x >> half, x & mask
    y_high, y_low = y >> half, y & mask

    # Three recursive products instead of the usual four.
    high_product = _multiply_nonnegative(x_high, y_high)
    low_product = _multiply_nonnegative(x_low, y_low)
    sum_product = _multiply_nonnegative(
        x_high + x_low, y_high + y_low
    )

    middle_product = sum_product - high_product - low_product
    return (
        (high_product << (2 * half))
        + (middle_product << half)
        + low_product
    )


if __name__ == "__main__":
    for left, right in [(13, 11), (1234, 5678), (-1234, 5678), (0, 2**128)]:
        product = karatsuba(left, right)
        assert product == left * right
        print(f"{left} * {right} = {product}")
