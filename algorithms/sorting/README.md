# 冒泡排序（Bubble Sort）

## 核心思路

重复比较相邻元素；如果顺序错误，就交换它们。一次完整的遍历会将尚未排序部分的最大元素“冒泡”到末尾。因此下一轮可以少比较一个位置。

本仓库实现 [bubble_sort.py](bubble_sort.py) 使用 `swapped` 记录是否发生交换：如果某轮没有交换，说明序列已经有序，可以提前结束。

## 复杂度与性质

| 性质 | 结论 | 理由 |
| --- | --- | --- |
| 最佳时间 | O(n) | 已有序时，一轮扫描后提前退出 |
| 平均时间 | O(n²) | 一般需要多轮相邻比较 |
| 最坏时间 | O(n²) | 例如逆序输入 |
| 额外空间 | O(1) | 只使用少量局部变量 |
| 稳定性 | 稳定 | 仅在左侧元素严格大于右侧时交换 |
| 修改输入 | 是 | 对传入的可变序列原地排序并返回同一对象 |

该算法要求元素支持 `>` 比较。它用于理解交换排序、循环不变量和复杂度分析；日常项目中需要排序时通常优先使用 Python 的 `sorted()` 或 `list.sort()`。

## 执行

```bash
python algorithms/sorting/bubble_sort.py
python -m pytest -q tests/test_bubble_sort.py
```

相关实验：[Numba 与普通 Python 冒泡排序性能对比](../../benchmarks/bubble_sort_numba.py)。注意 JIT 性能不能代表所有输入规模或 Python 对象类型的情况。
