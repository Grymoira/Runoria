# SPDX-License-Identifier: AGPL-3.0-only
"""Heap sort against Python sorted, including instability and edge cases."""

import random
from dataclasses import dataclass

import pytest

from algorithms.sorting.heap_sort import heap_sort


@pytest.mark.parametrize("values", [
    [], [1], [4, 3, 2, 1], [1, 2, 3, 4],
    [3, -1, 0, 3, -8, 3], [7, 7, 7, 7],
])
def test_heap_sort_matches_sorted(values: list[int]) -> None:
    before = values.copy()
    assert heap_sort(values) is values
    assert values == sorted(before)


def test_randomized_heap_sort() -> None:
    rng = random.Random(20261029)
    for size in range(60):
        for _ in range(4):
            original = [rng.randint(-30, 30) for _ in range(size)]
            data = original.copy()
            heap_sort(data)
            assert data == sorted(original)


@dataclass(frozen=True)
class Entry:
    key: int
    label: str

    def __gt__(self, other: "Entry") -> bool:
        return self.key > other.key


def test_orderable_objects_preserve_membership_but_not_stability() -> None:
    items = [Entry(2, "a"), Entry(1, "b"), Entry(2, "c")]
    before = items.copy()
    heap_sort(items)
    assert [x.key for x in items] == [1, 2, 2]
    assert sorted(x.label for x in items) == sorted(x.label for x in before)
    # Heap sort does not promise original relative order for equal keys.


def test_strings_and_unorderable_objects() -> None:
    values = ["pear", "apple", "banana"]
    assert heap_sort(values) == ["apple", "banana", "pear"]
    with pytest.raises(TypeError):
        heap_sort([object(), object()])
