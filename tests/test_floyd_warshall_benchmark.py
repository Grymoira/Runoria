# SPDX-License-Identifier: AGPL-3.0-only
"""Benchmark interface checks, independent of timing thresholds."""

import pytest

from benchmarks.floyd_warshall_vs_bellman_ford import benchmark


@pytest.mark.parametrize(("vertices", "density"), [(1, 0), (2, 1), (5, 0.5), (8, 0.8)])
def test_benchmark_executes_and_returns_nonnegative_timings(
    vertices: int, density: float
) -> None:
    fw, bf = benchmark(vertices=vertices, density=density, number=1, repeat=2)
    assert fw >= 0 and bf >= 0


@pytest.mark.parametrize(
    ("vertices", "density", "number", "repeat"),
    [
        (0, 0.5, 1, 1),
        (3, 0.5, 0, 1),
        (3, 0.5, 1, 0),
        (True, 0.5, 1, 1),
        (3, -0.1, 1, 1),
        (3, 1.1, 1, 1),
        (3, float("nan"), 1, 1),
        (3, float("inf"), 1, 1),
    ],
)
def test_invalid_benchmark_arguments(vertices, density, number, repeat) -> None:
    with pytest.raises(ValueError):
        benchmark(vertices, density, number, repeat)
