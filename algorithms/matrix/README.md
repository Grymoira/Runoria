# 斯特拉森算法（Strassen Matrix Multiplication）

> 分类：矩阵运算 / 分治（Divide and Conquer）  
> 环境：Python 3.10+，仅依赖标准库  
> 源码：[strassen.py](strassen.py) · 测试：[test_strassen.py](../../tests/test_strassen.py)  
> **本专题的核心解释也已直接写进仓库根目录 [README](../../README.md#斯特拉森算法strassen-matrix-multiplication)。**

## 1. 算法为什么重要？

矩阵乘法用于线性代数、计算机图形学、科学计算和机器学习。对于两个 $n \times n$ 方阵，最直接的三层循环做法需要 $O(n^3)$ 次标量运算。

分治可以将矩阵分成四个 $n/2 \times n/2$ 子块。普通的块矩阵乘法仍需要 **8 次**规模减半的子矩阵乘法；1969 年，Volker Strassen 发现通过代数重组，可以将其减少到 **7 次**。

因此经典复杂度从 $O(n^3)$ 下降到：

$$
T(n) = 7T(n/2) + O(n^2)
      = \Theta\left(n^{\log_2 7}\right)
      \approx \Theta(n^{2.807}).
$$

这是一项理论上的改进，但在 Python 中常数开销很大，不保证比普通乘法更快。

## 2. 7 次子乘法的推导

对 $2\times2$ 块矩阵：

$$
A=\begin{bmatrix}A_{11}&A_{12}\\A_{21}&A_{22}\end{bmatrix},
\qquad
B=\begin{bmatrix}B_{11}&B_{12}\\B_{21}&B_{22}\end{bmatrix}.
$$

普通块乘法：

$$
\begin{aligned}
C_{11} &= A_{11}B_{11}+A_{12}B_{21},\\
C_{12} &= A_{11}B_{12}+A_{12}B_{22},\\
C_{21} &= A_{21}B_{11}+A_{22}B_{21},\\
C_{22} &= A_{21}B_{12}+A_{22}B_{22}.
\end{aligned}
$$

共有 8 个子矩阵乘积。Strassen 取以下 7 个新乘积：

$$
\begin{aligned}
M_1 &= (A_{11}+A_{22})(B_{11}+B_{22}),\\
M_2 &= (A_{21}+A_{22})B_{11},\\
M_3 &= A_{11}(B_{12}-B_{22}),\\
M_4 &= A_{22}(B_{21}-B_{11}),\\
M_5 &= (A_{11}+A_{12})B_{22},\\
M_6 &= (A_{21}-A_{11})(B_{11}+B_{12}),\\
M_7 &= (A_{12}-A_{22})(B_{21}+B_{22}).
\end{aligned}
$$

通过加减便可得到结果的四个子块：

$$
\begin{aligned}
C_{11} &= M_1+M_4-M_5+M_7,\\
C_{12} &= M_3+M_5,\\
C_{21} &= M_2+M_4,\\
C_{22} &= M_1-M_2+M_3+M_6.
\end{aligned}
$$

注意：此处的 $A_{ij}$ 与 $B_{ij}$ 是**子矩阵**，不仅仅是某一个数字。每个 $M_i$ 都可以继续递归执行同样的算法。

## 3. 真实手算：两个 2×2 矩阵

取

$$
A=\begin{bmatrix}1&2\\3&4\end{bmatrix},
\qquad
B=\begin{bmatrix}5&6\\7&8\end{bmatrix}.
$$

算出七个乘积：

| 变量 | 计算 | 结果 |
| --- | --- | --- |
| $M_1$ | $(1+4)(5+8)$ | 65 |
| $M_2$ | $(3+4)5$ | 35 |
| $M_3$ | $1(6-8)$ | -2 |
| $M_4$ | $4(7-5)$ | 8 |
| $M_5$ | $(1+2)8$ | 24 |
| $M_6$ | $(3-1)(5+6)$ | 22 |
| $M_7$ | $(2-4)(7+8)$ | -30 |

然后：

$$
\begin{aligned}
C_{11} &= 65+8-24-30=19,\\
C_{12} &= -2+24=22,\\
C_{21} &= 35+8=43,\\
C_{22} &= 65-35-2+22=50.
\end{aligned}
$$

得到

$$
AB=\begin{bmatrix}19&22\\43&50\end{bmatrix}.
$$

可执行验证（设置 `cutoff=1` 确实经过七次乘法的 Strassen 分治路径）：

```python
from algorithms.matrix.strassen import strassen_multiply

a = [[1, 2], [3, 4]]
b = [[5, 6], [7, 8]]
assert strassen_multiply(a, b, cutoff=1) == [[19, 22], [43, 50]]
```

## 4. 不是 2 的幂、不是方阵怎么办？

经典推导假定输入为边长 $2^k$ 的方阵。现实中的矩阵可能是 $3\times3$、$3\times5$，甚至 $2\times3$ 与 $3\times4$ 的相乘。

本仓库通过**零填充（zero padding）**解决：

1. 验证 $A$ 为 $m\times k$，$B$ 为 $k\times n$，内层维度必须一致。
2. 取 $p$ 为不小于 $\max(m,k,n)$ 的最小的 $2$ 的幂。
3. 把两个矩阵放到 $p\times p$ 零矩阵左上角。
4. 对补零方阵执行 Strassen。
5. 将输出裁剪成 $m\times n$。

```python
from algorithms.matrix.strassen import strassen_multiply

a = [[1, 2, 3], [4, 5, 6]]             # 2 × 3
b = [[7, 8], [9, 10], [11, 12]]       # 3 × 2

assert strassen_multiply(a, b, cutoff=1) == [
    [58, 64],
    [139, 154],
]
```

补零保持乘积正确，但**很瘦长的矩阵**可能需要大量额外填充空间，性能甚至明显劣于三层循环。

## 5. Python API、递归阈值与约束

完整实现：[strassen.py](strassen.py)。核心函数：

- `strassen_multiply(a, b, *, cutoff=32)`：通过递归和补零计算，可返回新矩阵；不修改输入。
- `naive_multiply(a, b)`：三层循环的参考实现，便于交叉验证。

默认阈值 `cutoff=32` 的含义是：当递归中的方阵边长小于或等于 32 时，直接采用朴素乘法终止递归。它是教学中为了降低 Python 函数调用开销的经验选择，**不是理论上的最优阈值**。如需测试 2×2 的七乘积公式，请使用 `cutoff=1`。

| 情形 | 处理方式 |
| --- | --- |
| 正方形、矩形、非 2 的幂 | 全部支持，必要时补零 |
| 输入包含整数、浮点数、负数、零 | 支持；返回新列表矩阵 |
| 空矩阵、空行、参差不齐的行 | 抛出 `ValueError` |
| 两矩阵内层维度不同 | 抛出 `ValueError` |
| 字符串、复数、其他非 int / float 元素 | 抛出 `TypeError` |
| 小于 1 或不是整数的 `cutoff` | 抛出 `ValueError` |
| 是否修改输入 | **不会**修改 |
| 浮点数 | 可能与三层循环有细微舍入差异 |

Python 的 `bool` 是 `int` 的子类，故按 Python 数字语义作为 0 或 1 参与运算。这里没有加入 NumPy、GPU 或并行化依赖。

## 6. 时间、空间复杂度和数值问题

如果输入为 $n\times n$ 的二次幂方阵，经典递归模型给出：

$$
T(n)=7T(n/2)+O(n^2)
=\Theta(n^{\log_2 7})
\approx\Theta(n^{2.807}).
$$

朴素乘法为 $\Theta(n^3)$。对于任意形状的输入，本仓库先补成 $p\times p$，因此成本需按**补零之后的边长 $p$** 判断，而不是只按结果矩阵大小判断。

朴素实现会存储 $m\times n$ 输出；Strassen 实现还会分配多个加减结果、子块和中间矩阵。对于本实现，峰值辅助存储在一般递归模型下为 $O(p^2)$ 的量级，且常数较大；递归深度是 $O(\log p)$。当底层是 Python 列表与浮点对象时，实际内存管理的开销不可忽略。

**重要数值限制**：Strassen 改变了浮点运算的加减顺序，浮点数相乘的结果可能出现更大的误差放大或舍入差异。整数可以精确比较；浮点矩阵应使用容差进行验证。

## 7. 可复现的运行与测试

在仓库根目录执行：

```bash
python -m algorithms.matrix.strassen
python -m pytest -q tests/test_strassen.py tests/test_strassen_benchmark.py
python -m benchmarks.strassen_vs_naive --size 32 --cutoff 8 --number 3 --repeat 3
```

基准脚本使用固定随机种子、多次测量并报告每次调用中位数；不要求 Strassen 一定更快。对于通常的实用数值计算，请优先使用 NumPy 或其他经过优化的线性代数库。

## 8. 参考资料

- [Cornell University — Introduction to Algorithms, matrix multiplication notes](https://www.cs.cornell.edu/courses/cs4820/2026sp/notes/matrix%20notes.pdf)：七乘积恒等式、递归分析。
- [Virginia Tech OpenDSA — Matrix Multiplication](https://opendsa-server.cs.vt.edu/ODSA/Books/vt/cs4104-80dcbe0b-7910-4c9a-883019/spring-2025/S25/html/Matrix.html)：复杂度和常数开销。
- [CLRS-Lean — Strassen Algorithm](https://tanktechnology.github.io/CLRS-Lean/CLRSLean/FourthEdition/Chapter_04/Section_04_2_Strassen_Algorithm/)：正式化的补零/正确性思路。

所有中文说明与 Python 代码独立撰写，不直接复制上述教程的版权正文。
