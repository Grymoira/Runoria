# SPDX-License-Identifier: AGPL-3.0-only
"""Binary search first occurrence and insertion index vs Python bisect."""

from bisect import bisect_left
import random

import pytest

from algorithms.search.binary_search import binary_search, lower_bound


@pytest.mark.parametrize(
    ("values", "target", "position", "found"),
    [
        ([], 4, 0, -1),
        ([4], 4, 0, 0),
        ([4], 3, 0, -1),
        ([4], 5, 1, -1),
        ([1, 2, 2, 2, 5], 2, 1, 1),
        ([1, 2, 2, 2, 5], 3, 4, -1),
        ([-4, -1, 0, 2], -3, 1, -1),
        ([-4, -1, 0, 2], 0, 2, 2),
        ([9] * 20, 9, 0, 0),
        ([1, 2, 3], 99, 3, -1),
    ],
)
def test_known_search_cases(values, target, position, found) -> None:
    original = values.copy()
    assert lower_bound(values, target) == position
    assert binary_search(values, target) == found
    assert values == original


def test_randomized_comparison_to_bisect_left() -> None:
    rng = random.Random(20261029)
    for length in range(120):
        values = sorted(rng.randint(-15, 15) for _ in range(length))
        for target in range(-18, 19):
            expected = bisect_left(values, target)
            assert lower_bound(values, target) == expected
            found = expected if expected < length and values[expected] == target else -1
            assert binary_search(values, target) == found


def test_strings_and_immutable_sequences() -> None:
    assert binary_search(("a", "b", "b", "z"), "b") == 1
    assert lower_bound("acfg", "d") == 2


def test_unorderable_elements_raise() -> None:
    with pytest.raises(TypeError):
        binary_search([object(), object()], object())
