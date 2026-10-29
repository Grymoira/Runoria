"""冒泡排序的正确性、边界行为和稳定性测试。"""

from dataclasses import dataclass

import pytest

from algorithms.sorting.bubble_sort import bubble_sort


@pytest.mark.parametrize(
    "values",
    [
        [],
        [1],
        [1, 2, 3, 4],
        [4, 3, 2, 1],
        [3, -1, 3, 0, -7, 2],
        [2, 2, 2, 2],
        [10, 1, 10, 1, 0],
    ],
)
def test_matches_builtin_sorted(values: list[int]) -> None:
    original = values.copy()
    result = bubble_sort(values)
    assert result is values
    assert result == sorted(original)


@dataclass(frozen=True)
class Item:
    key: int
    name: str

    def __gt__(self, other: "Item") -> bool:
        return self.key > other.key


def test_stable_for_equal_keys() -> None:
    items = [
        Item(2, "first"),
        Item(1, "other"),
        Item(2, "second"),
    ]
    bubble_sort(items)
    assert [item.name for item in items] == ["other", "first", "second"]


def test_non_numeric_orderable_values() -> None:
    words = ["pear", "apple", "banana"]
    assert bubble_sort(words) == ["apple", "banana", "pear"]
