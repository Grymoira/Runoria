# SPDX-License-Identifier: AGPL-3.0-only
"""Repeatable educational timing: Strassen vs conventional Python matrix multiply.

Run from the repository root:
    python -m benchmarks.strassen_vs_naive --size 32 --cutoff 8 --number 3 --repeat 3

These implementations are pure Python. No speedup is asserted.
"""

import argparse
import random
import statistics
import timeit

from algorithms.matrix.strassen import naive_multiply, strassen_multiply


def benchmark(
    size: int = 32, cutoff: int = 8, number: int = 3, repeat: int = 3
) -> tuple[float, float]:
    """Return median seconds per call: naive multiplication, Strassen."""
    if any(isinstance(x, bool) or not isinstance(x, int) or x < 1
           for x in (size, cutoff, number, repeat)):
        raise ValueError("size, cutoff, number and repeat must be positive integers")

    rng = random.Random(20261029)
    a = [[rng.randint(-9, 9) for _ in range(size)] for _ in range(size)]
    b = [[rng.randint(-9, 9) for _ in range(size)] for _ in range(size)]

    expected = naive_multiply(a, b)
    if strassen_multiply(a, b, cutoff=cutoff) != expected:
        raise RuntimeError("Strassen did not match the reference product")

    naive_times = timeit.repeat(
        lambda: naive_multiply(a, b), number=number, repeat=repeat
    )
    strassen_times = timeit.repeat(
        lambda: strassen_multiply(a, b, cutoff=cutoff),
        number=number,
        repeat=repeat,
    )
    return (
        statistics.median(naive_times) / number,
        statistics.median(strassen_times) / number,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--size", type=int, default=32, help="Square matrix side length")
    parser.add_argument("--cutoff", type=int, default=8, help="Naive base-case threshold")
    parser.add_argument("--number", type=int, default=3, help="Calls per run")
    parser.add_argument("--repeat", type=int, default=3, help="Measured repetitions")
    args = parser.parse_args()

    naive_seconds, strassen_seconds = benchmark(
        size=args.size, cutoff=args.cutoff, number=args.number, repeat=args.repeat
    )
    print(f"Matrix size: {args.size}x{args.size}; cutoff: {args.cutoff}")
    print(f"Naive:    {naive_seconds:.7f} s/call (median)")
    print(f"Strassen: {strassen_seconds:.7f} s/call (median)")
    print("The goal is reproducible comparison, not a guaranteed speedup.")


if __name__ == "__main__":
    main()
