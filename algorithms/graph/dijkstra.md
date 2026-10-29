# Dijkstra 最短路径算法

> 归类：图论 / 单源最短路径 / 优先队列  
> 源码：[dijkstra.py](dijkstra.py) · 测试：[test_dijkstra.py](../../tests/test_dijkstra.py)  
> 同目录的 [Floyd–Warshall](README.md) 负责全源最短路，本算法专注从**一个**指定起点到其他顶点。

## 问题与限制

给出带权有向图，从起点 `source` 计算到所有节点的最短距离，并恢复路径。

**Dijkstra 要求所有边权非负**。不能仅仅因为算法给出了一个结果就忽视负权边：对负权图应改用 Bellman–Ford（单源）或 Floyd–Warshall（全源；但不能有负权环）。

## 贪心不变量与最小堆

算法从起点开始，记录到各个节点的**暂定最短距离**。每一步从优先队列取出当前最短的候选节点，并尝试沿它的出边**松弛（relax）**：

$$
\text{if }d[u]+w(u,v)<d[v],
\quad d[v]\leftarrow d[u]+w(u,v).
$$

之所以成立：当所有边权非负时，任何未来绕远路到达已经取出的最短候选节点，不可能通过加入非负边而使该距离变小。

本实现以 `heapq` 作为**最小堆**，每次弹出当前距离最小的候选；如果条目已经过时（比最新的 `dist[u]` 更大），就跳过它。每次严格变短才更新前驱节点 `predecessor[v]=u`。

### 邻接表输入

```python
from algorithms.graph.dijkstra import dijkstra, reconstruct_dijkstra_path

graph = [
    [(1, 4), (2, 1)],  # 0 -> 1 (4), 0 -> 2 (1)
    [(3, 1)],          # 1 -> 3 (1)
    [(1, 2), (3, 5)],  # 2 -> 1 (2), 2 -> 3 (5)
    [],                 # 3 无出边
]

dist, previous = dijkstra(graph, 0)
assert dist == [0, 3, 1, 4]
assert reconstruct_dijkstra_path(previous, 0, 3) == [0, 2, 1, 3]
```

从 0 到 3 如果直接取 0→2→3，费用为 1+5=6；走 0→2→1→3 则为 1+2+1=4。算法得到正确的 4。

## 复杂度与边界

设顶点数 `V`、边数 `E`，邻接表配合二叉最小堆是典型的 `O((V+E)\log(V+E))` 上界；简单图常写作 `O((V+E)\log V)`。程序还对邻接表做一次输入验证和复制：`O(V+E)` 的额外存储；堆中可能有多个指向同一节点的过期候选。

- 允许 **0 权边**，但禁止任何负数权重。
- 不可达返回 `math.inf`，恢复路径时返回 `None`。
- 起点到自身距离 `0`，路径为 `[source]`。
- 仅支持整数/有限浮点数边权；拒绝 `NaN`、无穷大、非数字。
- 大整数权重不强制转换成浮点数，保持精确计算。
- 若有限浮点路径求和溢出为无穷大，会主动抛出 `OverflowError`。
- 严格改善才更新路径，避免零权边导致相同距离时不断替换前驱。

## 与 Floyd–Warshall 比较

| 维度 | Dijkstra | Floyd–Warshall |
| --- | --- | --- |
| 路径查询 | 单源到所有节点 | 所有顶点对 |
| 数据结构 | 邻接表 + 小根堆 | 邻接矩阵 |
| 负权边 | 不支持 | 支持（不能存在负权环） |
| 时间复杂度 | 典型 `O((V+E)\log(V+E))` | `O(V^3)` |
| 路径重建 | 前驱数组 | 下一跳矩阵 |

随机测试将 Dijkstra 的每个源点距离和路线成本，与同一图上的 Floyd–Warshall 结果逐一对比。

参考：[cp-algorithms Dijkstra](https://cp-algorithms.com/graph/dijkstra_sparse.html)；[Python heapq](https://docs.python.org/3/library/heapq.html)。