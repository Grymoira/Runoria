# SPDX-License-Identifier: AGPL-3.0-only
"""教学基准：比较纯 Python Karatsuba 与内置整数乘法。

在仓库根目录执行：
    python -m benchmarks.karatsuba_vs_builtin --bits 1024 --number 20 --repeat 5

两种方法使用相同输入；测量不包含生成随机数与结果验证。
均以 lambda 调用，使计时调用方式一致，但短耗时结果会有噪声。
"""

import argparse
import random
import statistics
import timeit

from algorithms.arithmetic.karatsuba import karatsuba


def benchmark(bits: int = 1024, number: int = 20, repeat: int = 5) -> tuple[float, float]:
    """返回内置乘法、Karatsuba 每次乘法的中位数耗时（秒）。"""
    if bits < 1 or number < 1 or repeat < 1:
        raise ValueError("bits, number, and repeat must all be positive")

    rng = random.Random(20261029)
    left = rng.getrandbits(bits) | (1 << (bits - 1))
    right = rng.getrandbits(bits) | (1 << (bits - 1))

    expected = left * right
    if karatsuba(left, right) != expected:
        raise RuntimeError("Karatsuba differs from native multiplication")

    native_timings = timeit.repeat(
        lambda: left * right, number=number, repeat=repeat
    )
    karatsuba_timings = timeit.repeat(
        lambda: karatsuba(left, right), number=number, repeat=repeat
    )
    return (
        statistics.median(native_timings) / number,
        statistics.median(karatsuba_timings) / number,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bits", type=int, default=1024, help="Bits per operand")
    parser.add_argument("--number", type=int, default=20, help="Calls per round")
    parser.add_argument("--repeat", type=int, default=5, help="Timed rounds")
    args = parser.parse_args()

    builtin, custom = benchmark(args.bits, args.number, args.repeat)
    print(f"Operand bits: {args.bits}; rounds: {args.repeat}; calls per round: {args.number}")
    print(f"Built-in: {builtin:.8f}s per call (median)")
    print(f"Karatsuba: {custom:.8f}s per call (median)")
    print("No speedup is assumed; this is an educational Python benchmark.")


if __name__ == "__main__":
    main()
