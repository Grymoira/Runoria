"""可选 Numba 基准测试；基础 CI 未安装 Numba 时自动跳过。"""

import pytest

np = pytest.importorskip("numpy")
pytest.importorskip("numba")

from benchmarks.bubble_sort_numba import benchmark, bubble_sort_numba


@pytest.mark.parametrize("values", [[], [1], [2, 1], [3, 3, 2, -1], [5, 4, 3, 2, 1]])
def test_numba_sort_matches_builtin(values: list[int]) -> None:
    original = np.asarray(values, dtype=np.int64)
    actual = original.copy()
    bubble_sort_numba(actual)
    assert actual.tolist() == sorted(values)


@pytest.mark.parametrize("size", [0, 1, 20])
def test_benchmark_return_values(size: int) -> None:
    plain, jit = benchmark(size=size, repeat=2)
    assert plain >= 0 and jit >= 0


@pytest.mark.parametrize(("size", "repeat"), [(-1, 1), (1, 0)])
def test_invalid_arguments(size: int, repeat: int) -> None:
    with pytest.raises(ValueError):
        benchmark(size=size, repeat=repeat)
