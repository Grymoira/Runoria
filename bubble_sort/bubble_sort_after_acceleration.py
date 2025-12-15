# Bubble Sort accelerated by Numba
import time
from numba import jit
import random

@jit(nopython = True)
def bubble_sort_fast(arr):
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
    bubble_sort_fast(big_list)
    end_time = time.time()
    print(f"Time taken after Numba acceleration: {end_time - start_time: .4f}s")