# SPDX-License-Identifier: AGPL-3.0-only
"""Karatsuba 的确定性、随机性、边界与类型测试。"""

import random

import pytest

from algorithms.arithmetic.karatsuba import karatsuba


@pytest.mark.parametrize(
    ("x", "y"),
    [
        (0, 0),
        (0, 123456789),
        (-123456789, 0),
        (1, 1),
        (-1, 1),
        (-1, -1),
        (13, 11),
        (1234, 5678),
        (-1234, 5678),
        (1234, -5678),
        (-1234, -5678),
        ((1 << 63) - 1, (1 << 63) + 1),
        ((1 << 64) - 1, (1 << 64) - 1),
        ((1 << 64) + 1, (1 << 64) - 1),
        ((1 << 65) + 1, (1 << 65) - 1),
        ((1 << 127) + 1, (1 << 65) - 3),
        ((1 << 257) - 1, (1 << 130) + 19),
        (1 << 4096, 3),
        (-((1 << 4096) + 7), (1 << 64) + 3),
        (True, 12345),
        (False, -9),
    ],
)
def test_known_products_match_python(x: int, y: int) -> None:
    assert karatsuba(x, y) == x * y


@pytest.mark.parametrize(
    ("x", "y"),
    [
        (3.14, 2),
        (2, 3.14),
        ("100", 2),
        (2, None),
        (complex(1, 2), 3),
    ],
)
def test_rejects_non_integer_operands(x: object, y: object) -> None:
    with pytest.raises(TypeError, match="two integers"):
        karatsuba(x, y)  # type: ignore[arg-type]


def test_random_integers_with_unequal_bit_lengths() -> None:
    rng = random.Random(20261029)
    widths = (0, 1, 2, 31, 63, 64, 65, 127, 128, 129, 255, 256, 512, 1024, 2048)
    for left_bits in widths:
        for right_bits in (0, 1, 17, 64, 65, 128, 512):
            left = rng.getrandbits(left_bits)
            right = rng.getrandbits(right_bits)
            for x, y in ((left, right), (-left, right), (left, -right), (-left, -right)):
                assert karatsuba(x, y) == x * y


def test_large_inputs_do_not_require_decimal_string_conversion() -> None:
    """避免用 str(int) 拆分引发十进制转换的位数限制。"""
    x = (1 << 15000) + 123
    y = (1 << 100) + 456
    assert karatsuba(x, y) == x * y


def test_equal_large_operands() -> None:
    value = (1 << 2048) - 33
    assert karatsuba(value, value) == value * value
