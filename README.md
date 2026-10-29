# Runoria

**从理解到验证：可检索、可运行的计算机科学学习笔记。**

Runoria 是一个以 Python 为起点的个人学习知识库，用于记录算法、语言特性、Pythonic 写法及性能实验。它不是通用算法库，也不宣称每份学习实现都适合直接投入生产环境。

> Understand → Implement → Verify → Document（理解 → 实现 → 验证 → 记录）

## 知识索引

| 分类 | 内容 | 入口 |
| --- | --- | --- |
| Algorithms · 算法 | 冒泡排序、复杂度、边界情况 | [Bubble sort](algorithms/sorting/README.md) |
| Algorithms · 整数算术 | 卡拉楚巴算法（Karatsuba）、分治乘法、渐近复杂度 | [Karatsuba multiplication](algorithms/arithmetic/README.md) |
| Python idioms · 惯用写法 | [推导式](python/idioms/comprehensions.md)、[序列解包](python/idioms/unpacking.md)、[链式比较](python/idioms/chained_comparisons.md) | [python/idioms](python/idioms/) |
| Python idioms · 惯用写法 | [enumerate / zip](python/idioms/enumerate_and_zip.md)、[any / all](python/idioms/any_and_all.md)、[条件表达式](python/idioms/conditional_expression.md) | [python/idioms](python/idioms/) |
| Benchmarks · 性能实验 | [普通 Python 与 Numba 的冒泡排序对比](benchmarks/bubble_sort_numba.py) | [benchmarks](benchmarks/) |
| Tests · 正确性验证 | [冒泡排序](tests/test_bubble_sort.py)、[笔记代码示例](tests/test_documentation_examples.py)、[内部链接](tests/test_markdown_links.py) | [tests](tests/) |

## 目录结构

```text
Runoria/
├── algorithms/
│   ├── sorting/            # 排序算法及原理说明
│   └── arithmetic/         # 整数算术与分治算法
├── python/
│   └── idioms/             # 语言特性与惯用写法笔记
├── benchmarks/             # 独立的性能实验（可选依赖）
├── tests/                  # 可自动运行的正确性测试
├── docs/                   # 笔记模板
├── .github/workflows/      # Python 自动测试
└── CONTRIBUTING.md         # 记录和贡献约定
```

尚未学习到的分类不创建空目录；有真实内容时再扩展，例如图论、动态规划、标准库或数据结构。

## 运行与验证

使用 **Python 3.10+**。主算法仅使用 Python 标准库；运行普通算法无需安装第三方依赖。

```bash
# 在仓库根目录执行
python algorithms/sorting/bubble_sort.py
python -m algorithms.arithmetic.karatsuba

# 安装开发测试依赖并运行测试
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Numba 性能实验依赖 NumPy 和 Numba，单独安装（不作为学习笔记的必需依赖）：

```bash
python -m pip install numpy numba
python -m benchmarks.bubble_sort_numba --size 1000 --repeat 5
```

性能结果依赖 Python、NumPy、Numba 版本与运行环境；示例仅用于学习测量方法，不代表普遍性能结论。

Karatsuba 的可选性能对比（仅依赖标准库）：

```bash
python -m benchmarks.karatsuba_vs_builtin --bits 1024 --number 20 --repeat 5
```

这项实验不假定纯 Python 的 Karatsuba 一定快于原生大整数乘法。

## 阅读约定

- 每个知识点尽量包含：**是什么 → 传统写法 → 推荐写法 → 为什么 → 版本/边界条件 → 来源**。
- 算法应明确：输入输出、是否原地修改、时间与空间复杂度，以及可复现的测试。
- 语言规范、CPython 实现细节和实际测量结果应分开表述。
- `python/idioms/` 内的 `python` 代码块必须是可独立运行示例，CI 会验证；只表示语法形式的占位符使用 `text` 代码块。
- 可独立运行的算法程序放在 `.py` 文件中，性能实验复用标准算法实现。
- 详见 [CONTRIBUTING.md](CONTRIBUTING.md) 和 [笔记模板](docs/learning_template.md)。

## 许可

本仓库当前版本采用 **[GNU Affero General Public License v3.0 only (AGPL-3.0-only)](LICENSE)** 发布；修改、分发及网络服务场景应遵守许可证条款。历史版本的 MIT 授权不会因新版本换证而失效，原有版权及许可声明记录在 [NOTICE.md](NOTICE.md) 与 [LICENSES/MIT-legacy.txt](LICENSES/MIT-legacy.txt)。引用第三方内容时必须遵守其实际授权条件。
