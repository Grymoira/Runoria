# 链式比较（Chained Comparisons）

Python 可以按照数学表达式的习惯连续比较，而不必重复写逻辑运算符。

```python
x = 7
print(0 < x < 10)  # True
```

普通写法：

```python
x > 0 and x < 10
```

## 为什么有用？

链式比较具备**短路求值**特性：每个比较必须成功，才会继续后面的比较。中间的操作数表达式只计算一次。这与简单地将中间操作数复制两遍并不完全相同。

```python
def measure() -> int:
    print("called")
    return 5

print(0 < measure() < 10)  # called 仅打印一次
```

虽然 `a < b > c` 合法，其含义是 `a < b and b > c`，不是把整个式子按算术运算逐步计算；应优先使用容易阅读的比较区间。

## 常见误区

- `0 < x < 10` 是开区间，不包含 0 和 10。
- `min < value < max` 只是占位写法；实际代码可使用 `lower < value < upper`，避免遮蔽内置函数 `min` 和 `max`。
- 不是所有比较符号组合都适合写成一条长链；可读性优先。

## 来源

[Python 表达式参考：Comparisons](https://docs.python.org/3/reference/expressions.html#comparisons)
