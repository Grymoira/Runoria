# 弗洛伊德–沃舍尔算法（Floyd–Warshall Algorithm）

> 分类：图论（Graph Theory）/ 动态规划（Dynamic Programming）/ 全源最短路径（All-Pairs Shortest Paths）  
> Python：3.10+，无第三方依赖  
> 源码：[floyd_warshall.py](floyd_warshall.py) · 测试：[test_floyd_warshall.py](../../tests/test_floyd_warshall.py)

**仓库根目录 [README.md](../../README.md#弗洛伊德沃舍尔算法floydwarshall-algorithm) 也直接包含这一算法的完整核心讲解。** 本专题进一步解释路径重建、负权环与交叉验证。

## 1. 为什么需要它？

对于带权图，如果只需要一个起点到其他节点的最短路径，可以选择 Dijkstra 或 Bellman–Ford；如果想知道**任意两个节点**之间的最短距离，Floyd–Warshall 是一种简洁的动态规划方法。

- 输入：一个有 `V` 个顶点的带权图，用 `V × V` 的邻接矩阵记录边权。
- 输出：`V × V` 的最短距离矩阵，以及用于实际路线重建的下一跳矩阵。
- 支持有向图、**负权边**，但要求没有**负权环**。
- 不可达记为 `math.inf`，没有边不等于边权为 `0`。
- 时间复杂度：`O(V³)`；额外空间：`O(V²)`（不计输入）。

## 2. 动态规划状态与正确性直觉

设 `D⁽ᵏ⁾[i][j]` 表示**只允许编号小于 k 的顶点作为中间节点**时，`i` 到 `j` 的最短距离。

起点 `D⁽⁰⁾` 是原始邻接矩阵（自环的空路径长度设为 0）。

当允许顶点 `k` 参与路径时，最短路线分为两类：

1. **不经过 k**：维持已知距离 `D[i][j]`。
2. **经过 k**：先从 `i` 到 `k`，再从 `k` 到 `j`，距离 `D[i][k]+D[k][j]`。

因此核心状态转移为：

$$
\boxed{D[i][j] \leftarrow \min\left(D[i][j], D[i][k]+D[k][j]\right)}
$$

对应三层循环必须让 `k` 位于最外层：

```text
for k in vertices:
    for i in vertices:
        for j in vertices:
            if D[i][k] and D[k][j] are reachable:
                D[i][j] = min(D[i][j], D[i][k] + D[k][j])
```

这里的 `and` 表示可达条件而不是直接把距离当作 Python 布尔值；**0 权边是合法边**，不能用 `if distance` 判断是否有路。

## 3. 具体示例：最短路径可以包含负权边

设四个节点 `0、1、2、3`，边如下：

- `0→1` 权重为 `3`，`0→2` 为 `10`。
- `1→2` 权重为 `-2`，`1→3` 为 `10`。
- `2→3` 权重为 `2`。
- 其他不同顶点间没有直接边。

最初的矩阵（`∞` 代表不可达）：

$$
D^{(0)}=
\begin{bmatrix}
0&3&10&\infty\\
\infty&0&-2&10\\
\infty&\infty&0&2\\
\infty&\infty&\infty&0
\end{bmatrix}
$$

把顶点 `1` 作为允许经过的中间节点，原来的 `0→2` 直接路径长 `10`，改走 `0→1→2` 就变成：

$$
D[0][2]=\min(10,3+(-2))=1.
$$

再允许顶点 `2`，从 `0` 到 `3` 的最短路线可以是 `0→1→2→3`：

$$
D[0][3]=\min(\infty,1+2)=3.
$$

最终最短距离矩阵为：

$$
D=
\begin{bmatrix}
0&3&1&3\\
\infty&0&-2&0\\
\infty&\infty&0&2\\
\infty&\infty&\infty&0
\end{bmatrix}.
$$

可运行代码（从仓库根目录执行）：

```python
from math import inf
from algorithms.graph.floyd_warshall import floyd_warshall, reconstruct_path

graph = [
    [0,   3,   10,  inf],
    [inf, 0,   -2,  10],
    [inf, inf, 0,   2],
    [inf, inf, inf, 0],
]
distances, routes = floyd_warshall(graph)
assert distances[0][2] == 1
assert distances[0][3] == 3
assert reconstruct_path(routes, 0, 3) == [0, 1, 2, 3]
assert reconstruct_path(routes, 3, 0) is None  # 无法到达
```

## 4. 如何重建真实路径？

单有 `D[i][j]` 只能知道最短距离，不能知道“经过了哪些节点”。

本实现额外维护 `next_hop[i][j]`：

- 如果 `i→j` 有直接边，初始值为 `j`。
- 如果 `i` 无法到达 `j`，初始值为 `None`。
- 当经过 `k` 得到严格更短路径时，令 `next_hop[i][j] = next_hop[i][k]`，即从 `i` 出发该走的**第一跳**。

对 `reconstruct_path(routes, start, end)` 来说，从起点开始不断查看“去往终点应该先走到哪里”，直到终点。

- `start == end` 返回 `[start]`，对应长度为零的空路径。
- 不可达返回 `None`。
- 越界节点编号抛出 `IndexError`。
- 对不合法的下一跳表，函数限制行走步数，避免无限循环。

## 5. 为什么负权边可以，而负权环不行？

负权边本身不会破坏动态规划：上例中 `1→2` 权重为 `-2`，仍然得到正确最短路。

但存在**总权重为负的有向环**时，可以反复绕环，让某些路径成本不断减小，因此受影响节点对不再有有限的最短距离。

例如：

```python
from algorithms.graph.floyd_warshall import floyd_warshall

negative_cycle = [
    [0, 1, float("inf")],
    [float("inf"), 0, -3],
    [1, float("inf"), 0],
]
try:
    floyd_warshall(negative_cycle)
except ValueError as error:
    assert "negative-weight cycle" in str(error)
else:
    raise AssertionError("Expected negative-cycle detection")
```

Floyd–Warshall 的典型检测方法是检查对角线：存在 `D[v][v] < 0` 就说明有负权环。本仓库选择**一旦图中任何地方存在负权环，就整体抛出 `ValueError`**，不会返回可能误导人的“完整最短路径表”。

对于无向图，一条负权边往返走两次就形成负权闭合游走，所以这里尤其需要注意“无向负权边”的含义。

## 6. 边界条件与输入约定

| 场景 | 结果 |
| --- | --- |
| 空图 `[]` | 返回 `([], [])` |
| 独立节点 | 对角线为 `0`，其他距离为 `inf` |
| `0` 权重边 | 完全合法，不当作“没有边” |
| 正数对角线、`inf` 对角线 | 归一化成 `0`（空路径） |
| 负数对角线 | 构成负权自环，拒绝 |
| 负权边但无负权环 | 正确求最短路 |
| 负权环（包括不连通分量中的环） | 抛出 `ValueError` |
| 非方阵、参差行 | 抛出 `ValueError` |
| 非 `int` / `float` 权重 | 抛出 `TypeError`；`bool` 也明确拒绝 |
| `NaN`、`-inf` | 抛出 `ValueError` |
| Python 超大整数边权 | 保留整数运算，不强制转换成浮点数 |
| 浮点数边权 | 允许，但数值误差可能影响严格比较和负权环检测 |

算法不会修改传入的邻接矩阵。这里的距离矩阵和下一跳矩阵都是**新分配的数据结构**。

## 7. 复杂度与什么时候使用

- 初始化与路线记录：`O(V²)`。
- 三层循环每个允许的中间点都要考虑所有 `(i,j)`：`O(V³)`。
- 最短距离矩阵和下一跳矩阵各为 `V×V`：额外空间 `O(V²)`。
- 一次路线查询会沿着路径逐步跳转：最坏约为 `O(V)`；函数还会验证下一跳矩阵形状，实际调用包含 `O(V²)` 的输入检查。

适合顶点数中等、图较稠密、需要任意两点最短路的教学或实际场景。仅需单源路径时优先根据负权情况考虑 Dijkstra 或 Bellman–Ford；大规模稀疏图通常需要不同方案。

## 8. 运行、测试和基准实验

```bash
python -m algorithms.graph.floyd_warshall
python -m pytest -q tests/test_floyd_warshall.py tests/test_floyd_warshall_benchmark.py
python -m benchmarks.floyd_warshall_vs_bellman_ford --vertices 16 --density 0.6 --number 2 --repeat 3
```

基准实验生成**允许负权边但不包含负权环**的随机图，用重复运行的耗时中位数比较 Floyd–Warshall 与“每个起点各跑一次 Bellman–Ford”。两者都使用纯 Python 实现，不预设性能胜负。

测试还通过固定随机种子生成没有负权环、却可能有负权边的图，并与独立 Bellman–Ford 结果交叉比较，同时验证重建路径的每一步确实对应原图边权。

## 9. 参考资料

- [cp-algorithms — Floyd–Warshall](https://cp-algorithms.com/graph/all-pair-shortest-path-floyd-warshall.html)：动态规划、路径恢复与负权环。
- [Formal Proof Archive — Floyd–Warshall Algorithm](https://www.isa-afp.org/entries/Floyd_Warshall.html)：形式化验证的正确性说明。
- [CLRS Floyd–Warshall 练习讨论](https://walkccc.me/CLRS/Chap25/25.2/)：递推关系与空间优化思路。

文档与实现独立编写，参考链接用于术语、数学性质和边界条件的核查。
