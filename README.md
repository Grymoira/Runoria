# Runoria

**Understand → Implement → Verify → Document**  
**理解原理、动手实现、验证正确性、记录知识。**

Runoria 是一个以 Python 为起点的计算机科学个人知识库，记录算法、Pythonic 写法、标准库知识与可复现的性能实验。仓库以**学习正确性、阅读体验和可验证性**为优先目标，而不是提供生产环境的通用算法库。

> **阅读原则：打开根目录 README 就能理解已有知识点。** 对每个算法，本页直接解释问题背景、核心思想、关键公式、算例、复杂度、使用方法和局限性；相应源码、测试与子目录专题文档用于进一步研究，而不是阅读的前提。

## 目录与快速索引

| 内容 | 本页讲解 | 源码 / 详细笔记 |
| --- | --- | --- |
| 冒泡排序（Bubble Sort） | [原理、过程、稳定性及复杂度](#冒泡排序bubble-sort) | [算法实现](algorithms/sorting/bubble_sort.py) · [深入笔记](algorithms/sorting/README.md) |
| 卡拉楚巴算法（Karatsuba） | [三次乘法、分治推导与大整数](#卡拉楚巴算法karatsuba-multiplication) | [算法实现](algorithms/arithmetic/karatsuba.py) · [深入笔记](algorithms/arithmetic/README.md) |
| 斯特拉森算法（Strassen） | [七次矩阵乘法与分治推导](#斯特拉森算法strassen-matrix-multiplication) | [算法实现](algorithms/matrix/strassen.py) · [深入笔记](algorithms/matrix/README.md) |
| 弗洛伊德–沃舍尔（Floyd–Warshall） | [动态规划、全源最短路、负权环和路径恢复](#弗洛伊德沃舍尔算法floydwarshall-algorithm) | [算法实现](algorithms/graph/floyd_warshall.py) · [深入笔记](algorithms/graph/README.md) |
| Python 惯用写法 | [推导式、解包、比较、条件、any/all、enumerate/zip](#python-惯用写法与语言特性) | [笔记目录](python/idioms/) |
| 性能实验 | [测量方法与误区](#性能实验) | [冒泡排序 / Numba](benchmarks/bubble_sort_numba.py) · [Karatsuba / 内置乘法](benchmarks/karatsuba_vs_builtin.py) |
| 正确性与维护 | [测试、贡献与学习模板](#测试与知识维护) | [测试目录](tests/) · [贡献规范](CONTRIBUTING.md) |

## 算法（Algorithms）

### 冒泡排序（Bubble Sort）

**解决什么问题？** 将一组可比较的元素按升序排列。冒泡排序适合学习相邻交换、循环不变量和算法复杂度，而不是处理大规模数据的首选方案。

#### 工作原理

从序列左侧开始，逐对比较相邻元素。如果左侧元素更大，就交换这两个元素。一次完整扫描会把**当前未排序部分的最大元素移到末尾**。因此，每完成一轮，右侧就多出一个已经排好序的元素，下一轮的比较范围可以缩短。

以 `[5, 1, 4, 2, 8, 2]` 为例：

| 步骤 | 序列状态 | 说明 |
| --- | --- | --- |
| 初始 | `[5, 1, 4, 2, 8, 2]` | 尚未排序 |
| 第一轮结束 | `[1, 4, 2, 5, 2, 8]` | 最大值 `8` 已到末尾 |
| 第二轮结束 | `[1, 2, 4, 2, 5, 8]` | 末尾的 `5, 8` 已就位 |
| 最终 | `[1, 2, 2, 4, 5, 8]` | 全部升序 |

**提前终止优化**：如果某一轮没有发生交换，说明当前序列已经有序，可以直接结束。这也是仓库实现中 `swapped` 变量的用途。仅在 `left > right` 时交换（而不交换相等元素），还保留了**排序稳定性**：相同排序键的元素仍保持原来的相对顺序。

#### Python 使用示例

```python
from algorithms.sorting.bubble_sort import bubble_sort

values = [5, 1, 4, 2, 8, 2]
result = bubble_sort(values)

assert result is values  # 原地排序并返回同一对象
assert values == [1, 2, 2, 4, 5, 8]
```

#### 复杂度与边界

| 性质 | 结论 | 原因 |
| --- | --- | --- |
| 最好时间复杂度 | `O(n)` | 已排序时扫描一轮后直接退出 |
| 平均、最坏时间复杂度 | `O(n²)` | 通常需要多轮相邻比较 |
| 额外空间复杂度 | `O(1)` | 只用少量局部变量，直接修改输入 |
| 稳定性 | **稳定** | 不交换比较结果相等的相邻元素 |
| 输入要求 | 可变、元素可比较的序列 | 不支持不可比较对象的正常排序 |

空序列、单元素、重复元素、负数及已经排好序的数据都属于已测试的情况。注意：该函数会修改传入列表；如果需要保留原数据，请先复制。

**何时不使用？** 一般 Python 项目应优先选择 `sorted(values)`（返回新列表）或 `values.sort()`（原地排序），它们使用高度优化的排序实现。冒泡排序主要用于学习和小规模实验。

相关文件：[完整实现](algorithms/sorting/bubble_sort.py) · [复杂度与性质说明](algorithms/sorting/README.md) · [单元测试](tests/test_bubble_sort.py)。

---

### 卡拉楚巴算法（Karatsuba Multiplication）

**解决什么问题？** 更高效地计算大整数乘法。传统的逐位竖式乘法，通常需要约 `n²` 次数位运算，其中 `n` 表示输入整数的位数。

**关键思想：分治（Divide and Conquer）。** 把两个大整数拆成高位和低位，直接展开原本需要 **4 次**较小规模的乘法；Karatsuba 利用代数恒等式，把它减少为 **3 次**，用加减法算出交叉项。

#### 核心数学原理：为什么只要三次乘法？

令 `B = 2^m`，把整数写成：

$$
x = x_1B + x_0,\qquad y = y_1B + y_0
$$

直接展开：

$$
xy = x_1y_1B^2 + (x_1y_0 + x_0y_1)B + x_0y_0
$$

如果直接递归计算 `x₁y₁`、`x₁y₀`、`x₀y₁`、`x₀y₀`，需要四次子乘法。Karatsuba 改为只计算：

$$
\begin{aligned}
z_2 &= x_1y_1,\\
z_0 &= x_0y_0,\\
p &= (x_1+x_0)(y_1+y_0).
\end{aligned}
$$

由于 `p` 已包含四个交叉乘积，中间项可以直接用减法得到：

$$
z_1 = p-z_2-z_0 = x_1y_0+x_0y_1
$$

最后将高位、中间项和低位拼回去：

$$
\boxed{xy = z_2B^2 + z_1B + z_0}
$$

这就是卡拉楚巴算法的核心：**多做几次加减法，减少一整次递归乘法**。注意“三次”说的是**每层递归**，不是整个算法只执行三次乘法。

#### 手算：1234 × 5678

为了便于理解，先用十进制 `B=100` 拆分（代码实际采用二进制）：

$$
1234 = 12\times100 + 34,\qquad
5678 = 56\times100 + 78
$$

接着计算：

| 中间值 | 计算过程 | 结果 |
| --- | --- | --- |
| `z₂` | `12 × 56` | `672` |
| `z₀` | `34 × 78` | `2652` |
| `p` | `(12 + 34) × (56 + 78)` | `6164` |
| `z₁` | `6164 − 672 − 2652` | `2840` |

所以：

$$
1234\times5678
=672\times10000+2840\times100+2652
=\boxed{7006652}
$$

#### Python 如何实现拆分？

仓库实现基于**二进制移位与掩码**，避免将大整数反复转成十进制字符串：

- `x.bit_length()`：读取整数的位数。
- `x >> m`：取出高位。
- `x & ((1 << m) - 1)`：取出低位。
- `high << m`：将高位移回原来的数值位置。

```python
from algorithms.arithmetic.karatsuba import karatsuba

assert karatsuba(1234, 5678) == 7_006_652
assert karatsuba(-1234, 5678) == -7_006_652
assert karatsuba(0, 10**100) == 0
assert karatsuba((1 << 512) + 1, (1 << 256) - 1) == (
    ((1 << 512) + 1) * ((1 << 256) - 1)
)
```

递归主体先求出 `z₂`、`z₀` 和 `p`，再计算 `z₁ = p - z₂ - z₀`。当输入不超过 **64 位**时，改用内置乘法作为递归的终止条件；这是本教学实现选取的阈值，不代表所有机器都应如此优化。

#### 为什么理论复杂度更好？

朴素分治中的四次子乘法对应：

$$
T(n)=4T(n/2)+O(n)=O(n^2)
$$

而 Karatsuba 减少为三个子问题：

$$
T(n)=3T(n/2)+O(n)
$$

根据主定理：

$$
\boxed{T(n)=\Theta(n^{\log_2 3})\approx\Theta(n^{1.585})}
$$

这里的分析使用经典位运算成本模型；**这不意味着本仓库的纯 Python 递归代码在实测时一定比内置 `*` 快**。Python 大整数乘法是在底层实现的，函数调用和中间整数分配都可能带来明显额外开销。递归调用深度约为 `O(\log n)`，不属于 `O(1)` 额外空间的原地算法。

#### 使用范围与限制

- 支持零、负数、不等位长的整数及大整数。
- 对浮点数、字符串、复数等非整数参数抛出 `TypeError`。
- Python 中的 `bool` 是 `int` 的子类，因此 `True`、`False` 分别按 `1`、`0` 处理。
- 适合学习大整数运算、分治与复杂度分析；日常业务优先使用内置 `x * y`。

相关文件：[完整实现](algorithms/arithmetic/karatsuba.py) · [深入推导与边界说明](algorithms/arithmetic/README.md) · [正确性测试](tests/test_karatsuba.py) · [基准实验](benchmarks/karatsuba_vs_builtin.py)。

### 斯特拉森算法（Strassen Matrix Multiplication）

**解决什么问题？** 给定两个矩阵 $A$ 和 $B$，求它们的乘积 $C=AB$。对于普通的 $n\times n$ 方阵，三层循环计算每个元素的乘加组合，总时间通常是 $O(n^3)$。Strassen 算法采用**分治 + 代数重组**，把每一层原本需要的 8 次子矩阵乘法缩减到 **7 次**，以更多加减法换取更低的理论复杂度。

#### 1. 核心推导：8 次乘法为什么能变为 7 次？

把方阵分割成四块：

$
A=\begin{bmatrix}A_{11}&A_{12}\\A_{21}&A_{22}\end{bmatrix},
\qquad
B=\begin{bmatrix}B_{11}&B_{12}\\B_{21}&B_{22}\end{bmatrix}.
$

普通块乘法分别计算：

$
\begin{aligned}
C_{11}&=A_{11}B_{11}+A_{12}B_{21},\\
C_{12}&=A_{11}B_{12}+A_{12}B_{22},\\
C_{21}&=A_{21}B_{11}+A_{22}B_{21},\\
C_{22}&=A_{21}B_{12}+A_{22}B_{22}.
\end{aligned}
$

共需 8 个子矩阵乘积。Strassen 构造 7 个新的乘积：

$
\begin{aligned}
M_1&=(A_{11}+A_{22})(B_{11}+B_{22}),\\
M_2&=(A_{21}+A_{22})B_{11},\\
M_3&=A_{11}(B_{12}-B_{22}),\\
M_4&=A_{22}(B_{21}-B_{11}),\\
M_5&=(A_{11}+A_{12})B_{22},\\
M_6&=(A_{21}-A_{11})(B_{11}+B_{12}),\\
M_7&=(A_{12}-A_{22})(B_{21}+B_{22}).
\end{aligned}
$

然后通过加减法组合四块结果：

$
\begin{aligned}
C_{11}&=M_1+M_4-M_5+M_7,\\
C_{12}&=M_3+M_5,\\
C_{21}&=M_2+M_4,\\
C_{22}&=M_1-M_2+M_3+M_6.
\end{aligned}
$

这七个 $M_i$ 本身又可以继续使用同样的分治乘法。注意是**每层递归 7 次**，不是整个计算只乘 7 次。

#### 2. 手算示例：两个 2×2 矩阵

设

$
A=\begin{bmatrix}1&2\\3&4\end{bmatrix},
\qquad B=\begin{bmatrix}5&6\\7&8\end{bmatrix}.
$

根据上面的公式，$M_1,\ldots,M_7$ 依次为：

| 中间结果 | 计算 | 数值 |
| --- | --- | --- |
| $M_1$ | $(1+4)(5+8)$ | 65 |
| $M_2$ | $(3+4)\times5$ | 35 |
| $M_3$ | $1\times(6-8)$ | -2 |
| $M_4$ | $4\times(7-5)$ | 8 |
| $M_5$ | $(1+2)\times8$ | 24 |
| $M_6$ | $(3-1)(5+6)$ | 22 |
| $M_7$ | $(2-4)(7+8)$ | -30 |

组合得：

$
C=\begin{bmatrix}
65+8-24-30 & -2+24\\
35+8 & 65-35-2+22
\end{bmatrix}
=\boxed{\begin{bmatrix}19&22\\43&50\end{bmatrix}}.
$

仓库中的代码可以直接复现；这里设置 `cutoff=1`，确保小矩阵也走七乘法的分治分支：

```python
from algorithms.matrix.strassen import strassen_multiply, naive_multiply

a = [[1, 2], [3, 4]]
b = [[5, 6], [7, 8]]
result = strassen_multiply(a, b, cutoff=1)
assert result == [[19, 22], [43, 50]]
assert result == naive_multiply(a, b)
```

#### 3. 不是方阵或尺寸不是 2 的幂怎么办？

本仓库支持 **$m\times k$ 乘以 $k\times n$ 的矩形矩阵**。实现会将两个矩阵补零到共同的、边长为 2 的幂的方阵，计算后裁剪到 $m\times n$；原始输入不会被修改。

```python
from algorithms.matrix.strassen import strassen_multiply

left = [[1, 2, 3], [4, 5, 6]]      # 2 × 3
right = [[7, 8], [9, 10], [11, 12]] # 3 × 2

assert strassen_multiply(left, right, cutoff=1) == [
    [58, 64],
    [139, 154],
]
```

这类填充能保证正确性，但对非常瘦长的矩阵可能导致大量无用运算和额外内存占用。空矩阵、参差不齐的行或无法相乘的维度会抛出 `ValueError`；非整数/浮点数元素会抛出 `TypeError`。

#### 4. 复杂度、阈值与实际局限

普通分治依靠 8 次子乘法，$T(n)=8T(n/2)+O(n^2)=O(n^3)$。Strassen 改为：

$
\boxed{T(n)=7T(n/2)+O(n^2)=\Theta(n^{\log_2 7})\approx\Theta(n^{2.807})}.
$

对于本实现，若补零后的方阵边长为 $p$，应以 $p$ 分析时间与额外空间。切分和中间矩阵会增加内存开销，辅助空间在常规递归分析下为 $O(p^2)$ 量级，递归深度约为 $O(\log p)$。

- `strassen_multiply(left, right, cutoff=32)`：默认在边长不超过 32 时使用普通乘法结束递归，降低 Python 的函数调用开销。
- `naive_multiply(left, right)`：普通三层循环，作为正确性与基准测试参照。
- 对整数可精确比较结果；对浮点数，Strassen 的加减顺序不同，可能产生额外的数值舍入误差，应该用容差比较。
- **理论更优不代表纯 Python 实际运行一定更快**。日常大规模数值计算优先考虑 NumPy/BLAS 等优化实现。

相关阅读：[专题推导](algorithms/matrix/README.md) · [完整源码](algorithms/matrix/strassen.py) · [单元测试](tests/test_strassen.py) · [基准测试](benchmarks/strassen_vs_naive.py)。

### 弗洛伊德–沃舍尔算法（Floyd–Warshall Algorithm）

**解决什么问题？** 给定带权图，求出**任意两个顶点之间的最短距离**，而非仅从某一个起点出发的最短路。该问题称为 *All-Pairs Shortest Paths（APSP，全源最短路径）*。

Floyd–Warshall 适合学习图论中的**动态规划**：它允许出现**负权边**，但如果图中存在负权环，就无法对受该环影响的路径定义有限最短值，本仓库会明确报错。

#### 1. 邻接矩阵与状态

设图有 `V` 个顶点，用 `dist[i][j]` 表示 `i` 到 `j` 的当前最短距离。初始为邻接矩阵：

- `dist[i][i] = 0`：顶点到自身的空路径长度为 0。
- 有直接边 `i→j`：填入边权（**边权 0 也是合法的边**）。
- 没有直接边：填入 `math.inf`，代表目前不可达。

核心思路是：**依次允许每一个顶点 `k` 充当路径中转点**。对于 `i→j`，更短的路线只有两种可能：不经过 `k`，或者先从 `i` 到 `k` 再从 `k` 到 `j`。

#### 2. 动态规划公式

最重要的状态转移是：

$
\boxed{dist[i][j] = \min\left(dist[i][j],\;dist[i][k]+dist[k][j]\right)}
$

其中 `k` 是当前允许使用的中间顶点，必须作为**最外层循环**；`i` 和 `j` 分别表示起点、终点。

```text
for k in vertices:
    for i in vertices:
        for j in vertices:
            if i -> k and k -> j are reachable:
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
```

这个过程逐步扩大“允许经过的中转顶点集合”，最终覆盖所有可能的中转顶点。实现会在计算前检查不可达的 `math.inf`，避免把它当作真实边参与加法。

#### 3. 逐步算例：负权边也可以使用

有向图包含以下边：

| 边 | 权重 |
| --- | --- |
| `0→1` | `3` |
| `0→2` | `10` |
| `1→2` | `-2` |
| `1→3` | `10` |
| `2→3` | `2` |

最初，`0→2` 的直接距离是 `10`。若允许顶点 `1` 作为中转，就有：

$
dist[0][2] = \min(10,\;3+(-2)) = 1
$

接着允许顶点 `2` 作为中转，从 `0` 到 `3` 的最短路变为：

$
dist[0][3] = 1 + 2 = 3.
$

最终矩阵（`∞` 表示不可达）：

$
\begin{bmatrix}
0 & 3 & 1 & 3\\
\infty & 0 & -2 & 0\\
\infty & \infty & 0 & 2\\
\infty & \infty & \infty & 0
\end{bmatrix}
$

实际最短路线为 **0 → 1 → 2 → 3**，总权重为 `3 + (-2) + 2 = 3`。

#### 4. Python 示例：同时还原最短路径

本仓库不仅计算最短距离，还维护下一跳矩阵 `next_hop`。当经过 `k` 找到更短路线时，会更新“从 `i` 出发应该先走向哪个节点”；之后使用 `reconstruct_path()` 恢复实际经过的顶点。

```python
from math import inf
from algorithms.graph.floyd_warshall import floyd_warshall, reconstruct_path

graph = [
    [0, 3, 10, inf],
    [inf, 0, -2, 10],
    [inf, inf, 0, 2],
    [inf, inf, inf, 0],
]

distances, routes = floyd_warshall(graph)
assert distances[0][3] == 3
assert reconstruct_path(routes, 0, 3) == [0, 1, 2, 3]
assert distances[3][0] == inf
assert reconstruct_path(routes, 3, 0) is None
```

两个返回值都是新矩阵，不会修改原始输入。不可达路线返回 `None`，起点等于终点返回 `[start]`。

#### 与早期 Floyd–Warshall 笔记的区别

最初的手写版本已经包含**正确的三层动态规划与下一跳更新**；但有几个问题需要在实际使用前修正：

| 讨论点 | 早期写法 | 仓库当前实现 |
| --- | --- | --- |
| 最短距离更新 | `dist[i][k] + dist[k][j]` 与原距离比较 | 核心数学公式相同；先跳过不可达的 `inf` |
| 自身到自身 | 没有初始化 `next_node[i][i]`，通常误返回 `[]` | 返回 `[i]`，表示零长度路径 |
| 不可达 | 使用 `[]` | 使用 `None`，与有效路径列表区分 |
| 负权环 | 没有检查，可能得到无效距离与循环的下一跳 | 检测任意负对角线并拒绝结果 |
| 路线恢复 | 没有循环上限 | 限制跳转次数，拒绝损坏的下一跳表 |
| 非法输入 | 无矩阵形状及数值检查 | 显式验证矩阵、边权与索引 |

**旧版的 `reconstruct_path_floyd()` 和当前 `reconstruct_path()` 返回值不同。** 迁移旧代码时请注意：`start == end` 应返回 `[start]`，不可达返回 `None`。这既使语义更清楚，也避免把“最短路径没有中间节点”误认为无法到达。



#### 5. 负权环检测与重要限制

**负权边不等于负权环**：上面的 `1→2` 权重为 `-2` 是安全的，因为不存在能反复降低总成本的负权闭环。

若出现 `0→1→2→0`，权重分别为 `1、-3、1`，循环总权重为 `-1`；无限重复就可以把相关路径成本无限降低，因此不存在有限的最短距离。

当某顶点的 `dist[v][v] < 0` 时，说明图中有负权环。本仓库会在检测到**任何一个连通分量中的负权环**时抛出 `ValueError`，而不是返回可能误导人的完整最短路矩阵。

```python
from math import inf
from algorithms.graph.floyd_warshall import floyd_warshall

try:
    floyd_warshall([
        [0, 1, inf],
        [inf, 0, -3],
        [1, inf, 0],
    ])
except ValueError as exc:
    assert "negative-weight cycle" in str(exc)
else:
    raise AssertionError("A negative cycle must be rejected")
```

函数要求方形邻接矩阵、整数或浮点数边权；`NaN` 和 `-inf` 会被拒绝。对于大整数，使用 Python 原生整数，避免不必要的浮点精度损失。对于浮点数，累积误差可能影响严格的距离比较；**即使每条浮点边权都有限，多条边相加仍可能溢出为 `+inf` 或 `-inf`**，此时本实现会抛出 `OverflowError`，而不是错误地把可达路径当成不可达。

#### 6. 复杂度、适用场景与实验

| 性质 | 结论 | 理由 |
| --- | --- | --- |
| 时间复杂度 | **`O(V³)`** | 三层顶点循环 |
| 额外空间复杂度 | **`O(V²)`** | 保存距离矩阵与下一跳矩阵 |
| 能否处理负权边 | **可以** | 不依赖 Dijkstra 的非负权假设 |
| 能否处理负权环 | **拒绝** | 环上路径可被无限次降低 |
| 是否修改输入 | **不会** | 输入矩阵先复制 |
| 路径重建 | **支持** | `next_hop` 记录第一跳 |

适合规模中等、需要**所有顶点对**路径的图。对于单源最短路或非常稀疏的大图，应根据图的性质考虑 Dijkstra、Bellman–Ford 或 Johnson 算法等替代方案。

**不要把 `V ≤ 500` 当成普适门槛。** 这不是 Floyd–Warshall 的数学限制。纯 Python 三层循环、图的稠密程度、硬件性能以及可接受的计算时间都会影响实际规模；需要基准测试，而不是照搬某些竞赛题的经验值。

相关链接：[详细动态规划笔记](algorithms/graph/README.md) · [完整源码](algorithms/graph/floyd_warshall.py) · [正确性测试](tests/test_floyd_warshall.py) · [与 Bellman–Ford 的基准实验](benchmarks/floyd_warshall_vs_bellman_ford.py)。

## Python 惯用写法与语言特性

除了算法，Runoria 还整理了六组经常出现、值得深入理解的 Python 写法。下面直接给出含义、可运行示例与常见误区；每篇的详细笔记可通过标题链接打开。

### 1. [列表、字典与集合推导式](python/idioms/comprehensions.md)

推导式把“遍历、过滤、映射”组织为紧凑表达式。要注意 **`for` 后面的 `if` 用来过滤，`for` 前面的 `if ... else` 用来映射**，二者不等价。

```python
numbers = [-2, 0, 3, 5]

positive = [x for x in numbers if x > 0]        # 过滤
clamped = [x if x > 0 else 0 for x in numbers]   # 条件映射

assert positive == [3, 5]
assert clamped == [0, 0, 3, 5]
assert numbers == [-2, 0, 3, 5]  # 没有原地修改输入
```

字典推导式 `{k: f(k) for k in items}`、集合推导式 `{f(x) for x in items}` 和生成器表达式 `(f(x) for x in items)` 在结果类型和惰性计算方面也不同。不要为追求单行代码而过度嵌套。

### 2. [序列解包与变量交换](python/idioms/unpacking.md)

Python 可以把多个值一次分配给多个变量。星号解包会把中间的剩余元素收集为列表：

```python
a, b = 1, 2
a, b = b, a
assert (a, b) == (2, 1)

first, *middle, last = [10, 20, 30, 40]
assert (first, middle, last) == (10, [20, 30], 40)
```

右侧先求值，再将结果分配给左侧目标；具体解释器是否创建某种临时元组属于实现细节。元素不足时会发生 `ValueError`。

### 3. [链式比较](python/idioms/chained_comparisons.md)

`lower < value < upper` 既接近数学表达，也让**中间表达式只求值一次**；它具有短路行为：

```python
x = 7
assert 0 < x < 10
assert not (10 < x < 20)
```

`0 < x < 10` 是开区间；需要包含边界时应使用 `<=`。对有副作用的表达式，中间项只求值一次这一点尤其重要。

### 4. [条件表达式](python/idioms/conditional_expression.md)

`value_if_true if condition else value_if_false` 是一个表达式，适合简单的二选一赋值；只有**被选中的分支**会被求值。

```python
score = 78
status = "Pass" if score >= 60 else "Fail"
assert status == "Pass"
```

嵌套多层条件时，清晰的 `if/elif/else` 往往更容易维护。

### 5. [any() 与 all()](python/idioms/any_and_all.md)

`any()` 在遇到第一个真值时停止；`all()` 在遇到第一个假值时停止。使用生成器表达式可以避免提前构造整份布尔列表：

```python
numbers = [1, -3, 5]
assert any(x < 0 for x in numbers)
assert not all(x > 0 for x in numbers)

assert any([]) is False
assert all([]) is True
```

**空集合上的 `all()` 为真（空真）**。如果业务规则要求至少存在一个元素，应额外检查输入非空；对迭代器不能仅靠 `bool(iterator)` 检测是否耗尽。

### 6. [enumerate() 与 zip()](python/idioms/enumerate_and_zip.md)

`enumerate()` 在迭代时提供索引；`zip()` 把多个可迭代对象并行组合。默认 `zip()` 在最短输入耗尽时停止，可能悄悄丢弃多出来的数据。

```python
names = ["Alice", "Bob"]
ages = [20, 21]

assert list(enumerate(names, start=1)) == [(1, "Alice"), (2, "Bob")]
assert list(zip(names, ages, strict=True)) == [
    ("Alice", 20),
    ("Bob", 21),
]
```

Python 3.10+ 可使用 `zip(..., strict=True)` 检查长度不一致；确实需要补齐缺失值时，再使用 `itertools.zip_longest`。

## 性能实验

学习算法不能只比较程序运行一次所消耗的时间，还要验证输入、测量方法与结果正确性。Runoria 已包含两类实验：

| 实验 | 实验内容 | 需要的依赖 | 注意事项 |
| --- | --- | --- | --- |
| [冒泡排序与 Numba](benchmarks/bubble_sort_numba.py) | 对比普通 Python 与 JIT 编译版本 | NumPy、Numba | 两边的容器类型不同：`list` vs `ndarray`；JIT 预热后再计时 |
| [Karatsuba 与内置乘法](benchmarks/karatsuba_vs_builtin.py) | 对比纯 Python 分治乘法和内置 `*` | 仅标准库 | 固定随机输入、多轮计时、报告每次乘法时间中位数 |
| [Strassen 与普通矩阵乘法](benchmarks/strassen_vs_naive.py) | 比较两种纯 Python 矩阵乘法 | 仅标准库 | 大量子矩阵的拆分与补零有额外成本，不保证加速 |
| [Floyd–Warshall 与重复 Bellman–Ford](benchmarks/floyd_warshall_vs_bellman_ford.py) | 对比两种纯 Python 全源最短路 | 仅标准库 | 随机图可含负权边，但构造时保证无负权环 |

关键原则：**正确性优先于性能**；多轮重复测量；避免把数据生成、JIT 编译、复制输入或结果验证的时间混进算法本身的耗时（除非实验明确要测端到端时间）；绝不预先承诺某种实现一定更快。

## 运行、测试与知识维护

本项目的基本算法需要 **Python 3.10+**。请在仓库根目录执行：

```bash
# 运行三个算法示例
python algorithms/sorting/bubble_sort.py
python -m algorithms.arithmetic.karatsuba
python -m algorithms.matrix.strassen
python -m algorithms.graph.floyd_warshall

# 安装测试依赖，并执行所有基础测试
python -m pip install -r requirements-dev.txt
python -m pytest -q

# Karatsuba 性能实验（标准库）
python -m benchmarks.karatsuba_vs_builtin --bits 1024 --number 20 --repeat 5

# Strassen 性能实验（标准库）
python -m benchmarks.strassen_vs_naive --size 32 --cutoff 8 --number 3 --repeat 3

# Floyd–Warshall 基准实验（标准库）
python -m benchmarks.floyd_warshall_vs_bellman_ford --vertices 16 --density 0.6 --number 2 --repeat 3

# 可选 Numba 实验
python -m pip install numpy numba
python -m benchmarks.bubble_sort_numba --size 1000 --repeat 5
```

**自动化测试包括：** [冒泡排序](tests/test_bubble_sort.py)、[Karatsuba 乘法](tests/test_karatsuba.py)、[Karatsuba 基准接口](tests/test_karatsuba_benchmark.py)、[Strassen 矩阵乘法](tests/test_strassen.py)、[Strassen 基准接口](tests/test_strassen_benchmark.py)、[Floyd–Warshall 最短路与路径重建](tests/test_floyd_warshall.py)、[Floyd–Warshall 基准接口](tests/test_floyd_warshall_benchmark.py)、[Markdown Python 示例](tests/test_documentation_examples.py)、[首页知识覆盖检查](tests/test_readme_coverage.py) 和 [内部链接](tests/test_markdown_links.py)，以及可选的 [Numba 实验测试](tests/test_numba_benchmark.py)。GitHub Actions 在 Python 3.10 / 3.12 / 3.13 下检查基础实现。

### 后续新增算法必须怎样记录？

**根目录 README 是知识正文的第一入口，不是链接集合。** 新增算法时，必须同步在本页新增独立小节，至少说明：问题与应用、核心思路、必要数学推导、逐步算例、可运行示例、复杂度、边界和限制，并提供源码、单元测试与深入笔记链接。

子目录 `README.md` 可提供更完整的推导、示意、扩展实验，但不得把最关键的解释全部藏在子目录内。Python 语言特性和其他知识同样应在本页有可阅读的说明和实际示例。

详细约定见 [CONTRIBUTING.md](CONTRIBUTING.md)，学习笔记结构见 [docs/learning_template.md](docs/learning_template.md)。

## 目录结构

```text
Runoria/
├── algorithms/
│   ├── arithmetic/         # Karatsuba 等整数算法与原理
│   ├── matrix/             # Strassen 等矩阵运算
│   ├── graph/              # Floyd–Warshall 等图论算法
│   └── sorting/            # 冒泡排序等排序算法
├── python/
│   └── idioms/             # Python 惯用写法与语言细节
├── benchmarks/             # 独立性能实验
├── tests/                  # 算法、文档示例与链接验证
├── docs/                   # 学习笔记模板
├── .github/workflows/      # Python 跨版本自动测试
└── CONTRIBUTING.md         # 长期维护约定
```

尚无实际学习内容的类别不预先创建空目录；有真实条目时再自然扩展。

## 许可证

当前 Runoria 使用 **[GNU Affero General Public License v3.0 only（AGPL-3.0-only）](LICENSE)**。使用、修改、分发或作为网络服务提供时，应根据具体行为履行相应条款。

历史版本的 MIT 授权不会因当前版本更换许可证而被追溯撤销；原版权与许可声明见 [NOTICE.md](NOTICE.md) 与 [LICENSES/MIT-legacy.txt](LICENSES/MIT-legacy.txt)。引用第三方内容时必须遵守相应的版权及许可要求。
