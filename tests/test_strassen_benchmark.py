# SPDX-License-Identifier: AGPL-3.0-only
"""Validate the Strassen benchmarking harness without timing thresholds."""

import pytest

from benchmarks.strassen_vs_naive import benchmark


@pytest.mark.parametrize("size", [1, 2, 3, 8])
def test_benchmark_returns_nonnegative_times(size: int) -> None:
    naive_time, strassen_time = benchmark(
        size=size, cutoff=2, number=1, repeat=2
    )
    assert naive_time >= 0
    assert strassen_time >= 0


@pytest.mark.parametrize(
    ("size", "cutoff", "number", "repeat"),
    [
        (0, 1, 1, 1), (2, 0, 1, 1), (2, 2, 0, 1),
        (2, 2, 1, 0), (2, True, 1, 1), (2, 1, 1.5, 1),
    ],
)
def test_benchmark_rejects_invalid_inputs(size, cutoff, number, repeat) -> None:
    with pytest.raises(ValueError, match="positive integers"):
        benchmark(size=size, cutoff=cutoff, number=number, repeat=repeat)
