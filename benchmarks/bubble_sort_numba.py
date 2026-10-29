"""比较纯 Python 冒泡排序与 Numba JIT 版本的演示性基准。

运行前安装：python -m pip install numpy numba
示例：python benchmarks/bubble_sort_numba.py --size 1000 --repeat 5

两者使用相同的原始数值，但 Python 使用 list，Numba 使用 ndarray；
因此测量的差异同时受运行时与数据容器影响，不能只归因于 JIT。
"""

import argparse
import statistics
import time

import numpy as np
from numba import njit


@njit(cache=True)
def bubble_sort_numba(values: np.ndarray) -> np.ndarray:
    """原地排序 ndarray；在计时前应预热 JIT。"""
    for end in range(len(values) - 1, 0, -1):
        swapped = False
        for index in range(end):
            if values[index] > values[index + 1]:
                values[index], values[index + 1] = (
                    values[index + 1],
                    values[index],
                )
                swapped = True
        if not swapped:
            break
    return values


def bubble_sort_python(values: list[int]) -> list[int]:
    """与 Numba 版一致的纯 Python 算法，便于单文件运行此实验。"""
    for end in range(len(values) - 1, 0, -1):
        swapped = False
        for index in range(end):
            if values[index] > values[index + 1]:
                values[index], values[index + 1] = (
                    values[index + 1],
                    values[index],
                )
                swapped = True
        if not swapped:
            break
    return values


def benchmark(size: int = 1000, repeat: int = 5) -> tuple[float, float]:
    if size < 0 or repeat < 1:
        raise ValueError("size must be nonnegative; repeat must be positive")

    rng = np.random.default_rng(seed=42)
    original = rng.integers(0, 10_001, size=size, dtype=np.int64)
    expected = sorted(original.tolist())

    # 单独预热：触发一次编译，不把编译时间计入稳态运行时间。
    bubble_sort_numba(original.copy())

    python_times: list[float] = []
    numba_times: list[float] = []

    for _ in range(repeat):
        plain = original.tolist()
        start = time.perf_counter()
        bubble_sort_python(plain)
        python_times.append(time.perf_counter() - start)
        assert plain == expected

        accelerated = original.copy()
        start = time.perf_counter()
        bubble_sort_numba(accelerated)
        numba_times.append(time.perf_counter() - start)
        assert accelerated.tolist() == expected

    return statistics.median(python_times), statistics.median(numba_times)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--size", type=int, default=1000, help="Number of integers")
    parser.add_argument("--repeat", type=int, default=5, help="Measured runs")
    args = parser.parse_args()
    pure, jit = benchmark(args.size, args.repeat)
    print(f"Input elements: {args.size}; measured runs: {args.repeat}")
    print(f"Pure Python median: {pure:.6f}s")
    print(f"Numba median (JIT warmed): {jit:.6f}s")
    print("Note: Python list and NumPy ndarray have different runtime costs.")
