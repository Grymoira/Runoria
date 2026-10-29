# SPDX-License-Identifier: AGPL-3.0-only
"""Binary search and the leftmost insertion position in sorted sequences."""

from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


def lower_bound(values: Sequence[T], target: T) -> int:
    """Return the first index i with values[i] >= target (or len(values)).

    The caller MUST supply an ascending-sorted sequence of comparable values.
    This precondition is not checked, keeping O(log n) search complexity.
    """
    left, right = 0, len(values)  # half-open interval [left, right)
    while left < right:
        middle = left + (right - left) // 2
        if values[middle] < target:
            left = middle + 1
        else:
            right = middle
    return left


def binary_search(values: Sequence[T], target: T) -> int:
    """Return the first occurrence of target, or -1 if absent.

    Unlike a typical exact-match implementation, this is deterministic for
    duplicates. Inputs must be sorted ascending; ordering is not validated.
    """
    index = lower_bound(values, target)
    if index < len(values) and values[index] == target:
        return index
    return -1


if __name__ == "__main__":
    sample = [1, 2, 2, 4, 8]
    assert binary_search(sample, 2) == 1
    assert binary_search(sample, 3) == -1
    assert lower_bound(sample, 3) == 3
    print("First 2:", binary_search(sample, 2))
