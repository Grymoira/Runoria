# SPDX-License-Identifier: AGPL-3.0-only
"""Karatsuba 与内置乘法的演示性基准测试检查。"""

import pytest

from benchmarks.karatsuba_vs_builtin import benchmark


@pytest.mark.parametrize(
    ("bits", "number", "repeat"),
    [(1, 1, 1), (64, 2, 2), (65, 2, 2), (257, 3, 2)],
)
def test_benchmark_returns_nonnegative_times(
    bits: int, number: int, repeat: int
) -> None:
    builtin, karatsuba_time = benchmark(bits=bits, number=number, repeat=repeat)
    assert builtin >= 0
    assert karatsuba_time >= 0


@pytest.mark.parametrize(
    ("bits", "number", "repeat"),
    [(0, 1, 1), (-1, 1, 1), (1, 0, 1), (1, 1, 0)],
)
def test_invalid_benchmark_arguments(
    bits: int, number: int, repeat: int
) -> None:
    with pytest.raises(ValueError, match="must all be positive"):
        benchmark(bits=bits, number=number, repeat=repeat)
