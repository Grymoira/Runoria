# Bubble Sort
# Time complexity - O(n^2)

import time
import random

def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 -i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if not swapped:
            break
    return arr

if __name__ == "__main__":
    big_list = [random.randint(0, 10000) for _ in range(10000)]
    start_time = time.time()
    bubble_sort(big_list)
    end_time = time.time()
    print(f"Sort time consuming: {end_time - start_time: .4f}s")
