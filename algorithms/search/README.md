# 二分搜索（Binary Search）

> 归类：有序序列搜索 / 分治  
> 源码：[binary_search.py](binary_search.py) · 测试：[test_binary_search.py](../../tests/test_binary_search.py)  
> 根目录 [README.md](../../README.md) 提供可直接阅读的算法讲解。

## 为什么必须有序？

二分搜索在一次比较之后淘汰一半候选范围，必须依赖数组**已按升序排序**。如果数组未排序，它没有足够信息判定哪一半不可能存在目标。

这里采用**左闭右开区间** `[left, right)`：

1. 初始化 `left=0`、`right=len(values)`；
2. 取中点 `mid = left + (right-left)//2`；
3. 若 `values[mid] < target`，排除 `mid` 及之前的所有位置，令 `left=mid+1`；
4. 否则保留 `mid`，令 `right=mid`；
5. 当 `left==right`，得到第一个 **不小于** target 的位置（也叫 `lower_bound`、`bisect_left`）。

要精确匹配，需额外判断该位置确实小于 `len(values)` 且与目标相等，否则返回 `-1`。

### 为什么不直接找到就返回？

数组可能有重复值，例如 `[1, 2, 2, 2, 7]`。随便找到一个 `2` 就返回，可能是索引 `1/2/3` 中任意一个；本实现保证返回**第一个匹配位置**，即索引 1。

```python
from algorithms.search.binary_search import binary_search, lower_bound

nums = [1, 2, 2, 2, 7]
assert binary_search(nums, 2) == 1
assert binary_search(nums, 5) == -1
assert lower_bound(nums, 5) == 4
assert lower_bound(nums, 9) == len(nums)
```

## 核心复杂度与常见误区

每次 `right-left` 至少大致减半：

- 时间复杂度：`O(log n)`。
- 额外空间：`O(1)`，迭代实现。
- 空列表时 `lower_bound` 返回 0、`binary_search` 返回 −1。
- 该函数**不会验证输入有序**，因为检查排序会需要额外 `O(n)` 时间，破坏本函数的复杂度。
- 这是按索引检索的序列，适合列表、元组和其他索引访问快速的容器；链表的中点访问未必是 `O(1)`。
- Python 标准库提供 `bisect.bisect_left`，通常优先采用标准库。

测试与 `bisect_left` 在随机有序数组、重复元素、空输入和边界值上交叉验证。

参考：[Python bisect documentation](https://docs.python.org/3/library/bisect.html)；[cp-algorithms binary search](https://cp-algorithms.com/num_methods/binary_search.html)。