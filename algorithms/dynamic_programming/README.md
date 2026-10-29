# 动态规划（Dynamic Programming）与 0/1 背包

> 归类：动态规划 / 最优化 / 组合选择  
> 源码：[knapsack_01.py](knapsack_01.py) · 测试：[test_knapsack_01.py](../../tests/test_knapsack_01.py)

## 动态规划不是单个算法

动态规划（DP）是一种解决**最优子结构**与**重叠子问题**的方法。它的关键不是套公式，而是选择有意义的**状态**、规定**状态转移**、设置**边界条件**，然后决定采用记忆化递归（自顶向下）还是表格递推（自底向上）。

这里选择 **0/1 背包（0/1 Knapsack）** 示范全过程：每个物品只有“选/不选”两种情况，**最多选择一次**；有重量与价值，要求不超过容量时最大化总价值。

## 状态定义与转移

令 `dp[i][c]` 表示：**只考虑前 i 件物品、容量不超过 c** 时能得到的最大总价值。物品 i 的重量和价值分别为 `w_i` 与 `v_i`。

初始化：`dp[0][c] = 0`，没有物品时只能选择空集合。

转移（如果第 i 件物品放不下，只能跳过）：

$$
dp[i][c]=
\begin{cases}
dp[i-1][c], & w_i>c,\\
\max(dp[i-1][c],\;dp[i-1][c-w_i]+v_i),& w_i\le c.
\end{cases}
$$

其中左侧 `i` 从 1 开始，物品在 Python 列表中的索引是 `i-1`。**一定要看上一行 `i−1`**，才能保证每个物品最多使用一次；如果错误地在当前行重复取，问题就变成了“完全背包”。

### 示例：三件物品

- 重量 `[2,3,4]`
- 价值 `[3,4,5]`
- 背包容量 `5`

选择第 0 和第 1 件，合计重量 `2+3=5`，价值 `3+4=7`，优于只选第 2 件（价值 5）。

```python
from algorithms.dynamic_programming.knapsack_01 import knapsack_01

value, chosen = knapsack_01([2, 3, 4], [3, 4, 5], 5)
assert value == 7
assert chosen == [0, 1]  # 原始数组的零基索引
```

## 如何重建选中的物品？

DP 表格计算完后，从 `dp[n][capacity]` 逆向检查：若 `dp[i][c] > dp[i-1][c]`，说明第 `i` 件物品必须被选中以取得这一更高价值，此时记录其索引并将容量减去对应重量；否则直接转到上一行。

对于相等价值的多种最优解，本实现优先**不取当前物品**，因此返回一组确定性的物品编号。负价值物品可被跳过；零重量但价值为正的物品仍然最多被选一次。

## 复杂度与重要限制

- 时间 `O(nC)`、额外空间 `O(nC)`，`n` 是物品数，`C` 是**整数容量值**。
- **伪多项式（pseudo-polynomial）**：当容量很大（如 `10^9`），即使物品数量不多，DP 表格也可能不可行。
- 输入重量与容量必须是非负整数；价值是整数，可以为负。
- 可返回空选择，最大价值至少为 0；列表不会被修改。
- 本实现为了恢复具体选中物品保留二维表格；只计算最优值时可以压缩成一维 `O(C)`，但逆向遍历容量的顺序必须正确。

单元测试同时以小规模穷举的独立结果核对价值与所选索引。

参考：[cp-algorithms knapsack](https://cp-algorithms.com/dynamic_programming/knapsack.html)；[MIT OCW Dynamic Programming](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/pages/lecture-videos/lecture-19-dynamic-programming-i-fibonacci-shortest-paths/)。
