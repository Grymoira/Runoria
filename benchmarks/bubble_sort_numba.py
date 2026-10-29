"""普通 Python 冒泡排序与 Numba 加速版的教学性性能比较。

在仓库根目录运行：
    python -m benchmarks.bubble_sort_numba --size 1000 --repeat 5

输入数值相同，但容器分别为 Python list 和 NumPy ndarray，速度差异不能
全部归功于 JIT。计时前预热 JIT，输入复制与结果校验均不纳入测量。
"""

import argparse
import statistics
import time

import numpy as np
from numba import njit

from algorithms.sorting.bubble_sort import bubble_sort


@njit(cache=True)
def bubble_sort_numba(values: np.ndarray) -> np.ndarray:
    """在输入数组上执行冒泡排序。元素需要相互可比较。"""
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
    """返回纯 Python 与预热后 Numba 的运行耗时中位数（秒）。"""
    if size < 0 or repeat < 1:
        raise ValueError("size must be nonnegative; repeat must be positive")

    rng = np.random.default_rng(seed=42)
    original = rng.integers(0, 10_001, size=size, dtype=np.int64)
    expected = sorted(original.tolist())
    expected_numpy = np.asarray(expected, dtype=np.int64)

    # 此调用负责触发第一次 JIT 编译，不包含在稳态测量中。
    bubble_sort_numba(original.copy())

    plain_times: list[float] = []
    jit_times: list[float] = []
    for _ in range(repeat):
        plain = original.tolist()
        start = time.perf_counter()
        bubble_sort(plain)
        plain_times.append(time.perf_counter() - start)
        if plain != expected:
            raise RuntimeError("Pure Python sort returned incorrect values")

        accelerated = original.copy()
        start = time.perf_counter()
        bubble_sort_numba(accelerated)
        jit_times.append(time.perf_counter() - start)
        if not np.array_equal(accelerated, expected_numpy):
            raise RuntimeError("Numba sort returned incorrect values")

    return statistics.median(plain_times), statistics.median(jit_times)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--size", type=int, default=1000, help="Number of integers")
    parser.add_argument("--repeat", type=int, default=5, help="Measured runs")
    args = parser.parse_args()

    plain, jit = benchmark(args.size, args.repeat)
    print(f"Input elements: {args.size}; measured runs: {args.repeat}")
    print(f"Pure Python median: {plain:.6f}s")
    print(f"Numba median (JIT warmed): {jit:.6f}s")
    print("Note: Python list and NumPy ndarray have different runtime costs.")


if __name__ == "__main__":
    main()
