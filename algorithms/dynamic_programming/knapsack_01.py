# SPDX-License-Identifier: AGPL-3.0-only
"""0/1 knapsack solved by bottom-up dynamic programming and reconstruction."""

from collections.abc import Sequence


def knapsack_01(
    weights: Sequence[int],
    values: Sequence[int],
    capacity: int,
) -> tuple[int, list[int]]:
    """Return (maximum value, selected original zero-based indices).

    Each item is selected at most once; ties prefer *not* to take the current
    item. Supports zero-weight items and negative values (which can be skipped).
    The empty selection has value 0. Integer capacity/weights are required.

    Time and auxiliary space: O(items * capacity), hence pseudo-polynomial.
    """
    if isinstance(capacity, bool) or not isinstance(capacity, int) or capacity < 0:
        raise ValueError("capacity must be a nonnegative integer")
    if len(weights) != len(values):
        raise ValueError("weights and values must have the same length")
    if any(isinstance(w, bool) or not isinstance(w, int) or w < 0 for w in weights):
        raise ValueError("all weights must be nonnegative integers")
    if any(isinstance(v, bool) or not isinstance(v, int) for v in values):
        raise TypeError("all values must be integers")

    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        weight, value = weights[i - 1], values[i - 1]
        previous, current = dp[i - 1], dp[i]
        for c in range(capacity + 1):
            best = previous[c]
            if weight <= c:
                candidate = previous[c - weight] + value
                if candidate > best:
                    best = candidate
            current[c] = best

    selected: list[int] = []
    remaining = capacity
    for i in range(n, 0, -1):
        if dp[i][remaining] > dp[i - 1][remaining]:
            selected.append(i - 1)
            remaining -= weights[i - 1]
    selected.reverse()
    return dp[n][capacity], selected


if __name__ == "__main__":
    value, indices = knapsack_01([2, 3, 4], [3, 4, 5], 5)
    assert (value, indices) == (7, [0, 1])
    print("Knapsack best:", value, "items:", indices)
