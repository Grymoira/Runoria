# 堆排序（Heap Sort）

> 归类：比较排序 / 完全二叉树 / 堆（Heap）  
> 代码：[heap_sort.py](heap_sort.py) · 测试：[test_heap_sort.py](../../tests/test_heap_sort.py)  
> 首页 [README.md](../../README.md) 也包含本算法的完整原理讲解。

## 核心问题和思想

堆排序把普通数组视为一棵完全二叉树。**最大堆（max heap）**要求父节点的值不小于两个子节点的值。最大元素恒位于数组索引 `0`。

假设根索引为 `i`，对应的零基索引为：

- 左子节点 `2i+1`
- 右子节点 `2i+2`
- 父节点 `(i-1)//2`

不需要实际创建树节点，完全可以在原数组上完成。

### 两个阶段

1. **建堆**：从最后一个非叶子节点 `n//2 - 1` 开始向前执行 `sift_down`，让全数组符合最大堆规则；从下向上建堆的总成本为 **O(n)**，不是 O(n log n)。
2. **重复取最大元素**：交换根和未排序区末尾，将未排序区缩短一个位置，对新根执行 `sift_down`。每次为 **O(log n)**，最多执行 n−1 次。

举例 `[4, 10, 3, 5, 1]`：先整理最大堆得到 `[10, 5, 3, 4, 1]`；根 `10` 与末尾 `1` 交换，再恢复前 4 个节点的堆，得到 `[5, 4, 3, 1, 10]`；继续重复直至 `[1, 3, 4, 5, 10]`。

```python
from algorithms.sorting.heap_sort import heap_sort

nums = [4, 10, 3, 5, 1]
result = heap_sort(nums)
assert result is nums                 # 原地排序
assert nums == [1, 3, 4, 5, 10]
```

## 时间、空间与稳定性

| 性质 | 结论 |
| --- | --- |
| 建堆成本 | `O(n)` |
| 总时间复杂度：最好 / 平均 / 最坏 | 全部 `O(n log n)` |
| 辅助空间 | `O(1)`，本实现用迭代 `sift_down` |
| 稳定排序 | **否**；相等元素的相对顺序可能变化 |
| 修改输入 | 是，原地更新 |
| 对比冒泡排序 | 堆排序保证更好的最坏渐近时间；冒泡排序稳定，且已经有序时可提前终止 |

排序通常应优先使用 Python `sorted()` 或 `list.sort()`；它们对真实数据通常更合适，且保持稳定性。本算法主要用于学习堆和复杂度保证。

## 边界与测试

空列表、单元素、负数、重复值、已经排序/逆序数据，以及自定义可比较对象都加入了测试；对无法比较大小的元素，Python 会自然抛出 `TypeError`。

参考：[Python sorting HOWTO](https://docs.python.org/3/howto/sorting.html)；[OpenDSA heap sort](https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/Heapsort.html)。