# SPDX-License-Identifier: AGPL-3.0-only
"""0/1 knapsack validation with brute-force subset enumeration."""

import random
from itertools import combinations

import pytest

from algorithms.dynamic_programming.knapsack_01 import knapsack_01


def _brute_best(weights: list[int], values: list[int], capacity: int) -> int:
    best = 0
    for length in range(len(weights) + 1):
        for choice in combinations(range(len(weights)), length):
            if sum(weights[i] for i in choice) <= capacity:
                best = max(best, sum(values[i] for i in choice))
    return best


@pytest.mark.parametrize(("weights", "values", "capacity", "best"), [
    ([], [], 0, 0),
    ([], [], 10, 0),
    ([2, 3, 4], [3, 4, 5], 5, 7),
    ([2, 3, 4], [3, 4, 5], 0, 0),
    ([0, 2], [5, 3], 0, 5),
    ([0, 0, 3], [3, 2, 9], 0, 5),
    ([3, 4], [-8, -1], 10, 0),
    ([1, 1], [4, 4], 1, 4),
])
def test_examples_and_reconstruction(weights, values, capacity, best) -> None:
    value, selected = knapsack_01(weights, values, capacity)
    assert value == best
    assert selected == sorted(set(selected))
    assert all(0 <= i < len(weights) for i in selected)
    assert sum(weights[i] for i in selected) <= capacity
    assert sum(values[i] for i in selected) == best


def test_deterministic_ties_prefer_existing_solution() -> None:
    assert knapsack_01([1, 1], [4, 4], 1) == (4, [0])


def test_random_small_cases_vs_brute_force() -> None:
    rng = random.Random(20261029)
    for n in range(9):
        for _ in range(35):
            weights = [rng.randint(0, 9) for _ in range(n)]
            values = [rng.randint(-5, 15) for _ in range(n)]
            cap = rng.randint(0, 20)
            best, chosen = knapsack_01(weights, values, cap)
            assert best == _brute_best(weights, values, cap)
            assert len(chosen) == len(set(chosen))
            assert sum(weights[i] for i in chosen) <= cap
            assert sum(values[i] for i in chosen) == best


@pytest.mark.parametrize(("w", "v", "cap", "error"), [
    ([1], [1, 2], 3, ValueError),
    ([-1], [1], 3, ValueError),
    ([1.5], [1], 3, ValueError),
    ([True], [1], 3, ValueError),
    ([1], [1.5], 3, TypeError),
    ([1], [True], 3, TypeError),
    ([1], [1], -1, ValueError),
    ([1], [1], True, ValueError),
])
def test_invalid_inputs(w, v, cap, error) -> None:
    with pytest.raises(error):
        knapsack_01(w, v, cap)
