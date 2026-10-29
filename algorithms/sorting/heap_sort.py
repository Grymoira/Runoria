# SPDX-License-Identifier: AGPL-3.0-only
"""In-place ascending heap sort using a binary max heap.

The implementation intentionally avoids heapq so that heap construction,
sift-down, and repeated extraction can be inspected independently.
"""

from typing import MutableSequence, TypeVar

T = TypeVar("T")


def heap_sort(values: MutableSequence[T]) -> MutableSequence[T]:
    """Sort a mutable sequence in place and return the same object.

    O(n log n) worst-case time, O(1) auxiliary space, NOT stable.
    Elements must support ordering with >.
    """
    n = len(values)

    def sift_down(root: int, end: int) -> None:
        """Restore the max-heap property within [0, end)."""
        while 2 * root + 1 < end:
            left = 2 * root + 1
            largest = root
            if values[left] > values[largest]:
                largest = left
            right = left + 1
            if right < end and values[right] > values[largest]:
                largest = right
            if largest == root:
                return
            values[root], values[largest] = values[largest], values[root]
            root = largest

    # Floyd's bottom-up heap construction takes O(n) time.
    for root in range(n // 2 - 1, -1, -1):
        sift_down(root, n)

    # Move the largest remaining item to the sorted right-hand suffix.
    for end in range(n - 1, 0, -1):
        values[0], values[end] = values[end], values[0]
        sift_down(0, end)
    return values


if __name__ == "__main__":
    sample = [5, 1, 4, 2, 8, 2]
    assert heap_sort(sample) == [1, 2, 2, 4, 5, 8]
    print("Heap sort:", sample)
