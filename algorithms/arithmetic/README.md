# 卡拉楚巴算法（Karatsuba Multiplication）

> 分类：分治（Divide and Conquer）/ 整数算术  
> 适用版本：Python 3.10+；无需第三方依赖  
> 实现：[karatsuba.py](karatsuba.py) · [单元测试](../../tests/test_karatsuba.py)

## 1. 算法目的

小学竖式乘法的朴素实现通常需要对两个长度为 `n` 的整数执行约 `n²` 次数位乘法。**卡拉楚巴算法的关键洞见，是将四次规模减半的乘法减少为三次**，以额外的加法与移位换取更低的渐近时间复杂度。

在经典的位运算成本模型下，它的运行时间为 **$\Theta(n^{\log_2 3}) \approx \Theta(n^{1.585})$**，这里 `n` 是输入的位数而非整数的数值大小。

本仓库的版本是**教学实现**。Python 自带的整数乘法已经在底层进行了优化，普通项目应该优先使用 `x * y`，而不是假设纯 Python 的递归一定更快。

## 2. 从四次乘法到三次乘法

令 `B = 2^m`，将两个非负整数按高、低位拆分：

$$
x = x_1 B + x_0,\qquad y = y_1 B + y_0
$$

直接展开：

$$
xy = x_1y_1 B^2 + (x_1y_0 + x_0y_1)B + x_0y_0
$$

原式涉及四次规模较小的乘法。但只需要先求：

$$
\begin{aligned}
z_2 &= x_1y_1,\\
z_0 &= x_0y_0,\\
p &= (x_1+x_0)(y_1+y_0).
\end{aligned}
$$

因为

$$
p = x_1y_1 + x_1y_0 + x_0y_1 + x_0y_0,
$$

可以**通过加减法**得到中间交叉项：

$$
z_1 = x_1y_0 + x_0y_1 = p - z_2 - z_0.
$$

最终组合：

$$
\boxed{xy = z_2B^2 + z_1B + z_0}
$$

每层只有 `z₂`、`z₀` 和 `p` 这**三次递归乘法**，这是算法相较普通分治乘法的关键改进。

## 3. 手工推导：1234 × 5678

为了便于心算，本节选择十进制基数 `B=100`；实际 Python 实现使用二进制。

- `1234 = 12 × 100 + 34`，因此 `x₁=12`，`x₀=34`。
- `5678 = 56 × 100 + 78`，因此 `y₁=56`，`y₀=78`。
- `z₂ = 12 × 56 = 672`。
- `z₀ = 34 × 78 = 2652`。
- `p = (12+34) × (56+78) = 46 × 134 = 6164`。
- `z₁ = 6164 − 672 − 2652 = 2840`。

于是：

$$
1234 \times 5678
= 672 \times 10000 + 2840 \times 100 + 2652
= 7006652.
$$

对照可执行的 Python 实现：

```python
from algorithms.arithmetic.karatsuba import karatsuba

assert karatsuba(1234, 5678) == 7_006_652
assert karatsuba(-1234, 5678) == -7_006_652
```

## 4. 本仓库的二进制实现

阅读源码：[karatsuba.py](karatsuba.py)。

首先使用 `int.bit_length()` 找到较大的输入位数，再以 `m = n // 2` 分割。`x >> m` 取得高位；`x & ((1 << m) - 1)` 取得低位。

```python
x = 13          # 二进制 1101
m = 2
high = x >> m
low = x & ((1 << m) - 1)

assert (high, low) == (3, 1)
assert x == (high << m) + low
```

每层执行的主要步骤为：

```text
high_product = K(x_high, y_high)
low_product  = K(x_low, y_low)
sum_product  = K(x_high + x_low, y_high + y_low)

middle_product = sum_product - high_product - low_product
result = (high_product << (2*m)) + (middle_product << m) + low_product
```

示例代码的 `K` 表示递归 Karatsuba 计算，而不是一个额外的 Python 内置函数。

### 为什么需要递归终止条件？

位数不超过 **64 位**时，使用 Python 内置 `x * y` 结束递归。这样既保证递归终止，也避免对小整数反复拆分的额外开销。阈值是教学上的工程选择，不是数学定理或通用的最佳性能参数。

## 5. 复杂度与内存

朴素分治会有四个规模约为 `n/2` 的乘法子问题：

$$
T(n) = 4T(n/2) + O(n) = O(n^2)
$$

Karatsuba 的递推式改为：

$$
T(n) = 3T(n/2) + O(n)
$$

用主定理可得：

$$
T(n) = \Theta(n^{\log_2 3}) \approx \Theta(n^{1.585}).
$$

这属于**经典整数运算模型下的理论分析**，并非对 CPython 实测时间的保证。实现会创建中间大整数，递归深度约为 `O(log n)`；它**不是**仅需 `O(1)` 额外空间的原地算法。

## 6. 输入边界及常见误区

| 场景 | 行为 |
| --- | --- |
| 零、负数 | 支持；先处理零和符号，再对绝对值执行递归 |
| 位数不等、奇数位 | 支持；按最大位数分割，不要求输入长度为 2 的幂 |
| 非整数（浮点数、字符串、复数等） | 明确抛出 `TypeError`，不偷偷转换 |
| `True` / `False` | `bool` 是 Python 中 `int` 的子类，分别作为 1 / 0 |
| 很大的整数 | 用位运算拆分，不使用十进制字符串 |
| 小整数 | 直接使用 `x * y` 作为递归基准情形 |

**不要把“三次乘法”误读成“整个算法只乘三次”**：每次递归又产生三个子问题，直到到达基准情形。

## 7. 运行和测试

请在**仓库根目录**执行：

```bash
python -m algorithms.arithmetic.karatsuba
python -m pytest -q tests/test_karatsuba.py
```

性能对比（仅用于观察，不要求 Karatsuba 更快）：

```bash
python -m benchmarks.karatsuba_vs_builtin --bits 1024 --number 20 --repeat 5
```

详见 [基准测试源码](../../benchmarks/karatsuba_vs_builtin.py)。它固定随机种子，对相同输入分别测量纯 Python Karatsuba 与 Python 内置乘法。

## 8. 参考资料

- [Wolfram MathWorld — Karatsuba Multiplication](https://mathworld.wolfram.com/KaratsubaMultiplication.html)：经典恒等式与渐近复杂度。
- [University of Illinois — Karatsuba Recursion Tree](https://courses.grainger.illinois.edu/cs173/sp2026/AB/lecture-notes/karatsuba-recursion-tree.html)：以递归树说明为什么指数是 $\log_2 3$。
- [Archive of Formal Proofs — Karatsuba Multiplication on Integers](https://isa-afp.org/entries/Karatsuba.html)：包含形式化验证的整数乘法实现与运行时间界。

以上资料用于核对数学结论。Runoria 的 Python 代码与中文解释均为独立编写。
