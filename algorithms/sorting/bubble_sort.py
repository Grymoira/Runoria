"""冒泡排序：原地、稳定、无第三方依赖的教学实现。"""

from typing import MutableSequence, TypeVar

T = TypeVar("T")


def bubble_sort(values: MutableSequence[T]) -> MutableSequence[T]:
    """将可变序列原地升序排列，并返回同一个序列。

    比较时使用 >；元素需要支持相互比较。
    最佳时间复杂度 O(n)，平均与最坏 O(n²)，额外空间 O(1)。
    """
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


if __name__ == "__main__":
    sample = [5, 1, 4, 2, 8, 2]
    print("Before:", sample)
    bubble_sort(sample)
    print("After: ", sample)
