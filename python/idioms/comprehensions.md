# 推导式（Comprehensions）

## 1. 列表推导式

传统写法：

```python
squares = []
for i in range(10):
    if i % 2 == 0:
        squares.append(i ** 2)
```

等价的推导式：

```python
squares = [i ** 2 for i in range(10) if i % 2 == 0]
assert squares == [0, 4, 16, 36, 64]
```

这里 `if` 放在 `for` **后面**，表示过滤：只有满足条件的元素才被保留。

## 2. 过滤与条件映射不是一回事

```python
data = [-5, 3, -1, 10, 0]

filtered = [x for x in data if x > 0]
mapped = [x if x > 0 else 0 for x in data]

assert filtered == [3, 10]
assert mapped == [0, 3, 0, 10, 0]
assert data == [-5, 3, -1, 10, 0]  # 原列表没有被修改
```

- `for` 后的 `if` 是**过滤条件**，可缩短结果列表。
- `for` 前的 `if ... else ...` 是**条件表达式**，为每个输入生成一个输出；这不是“原地修正”。

## 3. 复杂逻辑应退回普通函数

不推荐将多层条件嵌套到单行推导式。下面的写法更容易验证：

```python
def classify(number: int) -> str:
    if number % 2 == 0:
        return "even"
    if number > 5:
        return "large odd"
    return "small odd"

labels = [classify(x) for x in range(10)]
```

## 4. 字典、集合与生成器

```python
squares_by_number = {x: x * x for x in range(5)}
unique_squares = {x * x for x in [1, 1, 2, 3]}
lazy_squares = (x * x for x in range(1_000_000))

assert squares_by_number[3] == 9
assert unique_squares == {1, 4, 9}
assert next(lazy_squares) == 0
```

生成器表达式按需产生值，不会像列表推导式一样立即建立完整结果列表。Python 没有直接对应的“元组推导式”；需要元组时可使用 `tuple(generator)`。

## 5. 性能与作用域

- 推导式经常比手写 `append` 循环精简，但**不保证一定更快**；应依据具体 Python 版本和负载测量。
- Python 3 中，推导式的迭代变量不会泄漏到外围作用域；普通 `for` 循环变量在相同作用域中仍然可见。
- CPython 3.12 开始采用 [PEP 709](https://peps.python.org/pep-0709/) 的内联优化，不能将所有版本的字节码、函数调用或临时对象行为一概而论。
- 包含难以理解的多重循环或副作用时，普通循环往往更适合。笛卡尔积可考虑 `itertools.product`。

## 来源

- [Python 教程：列表推导式](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)
- [Python 语言参考：Displays for lists, sets and dictionaries](https://docs.python.org/3/reference/expressions.html#displays-for-lists-sets-and-dictionaries)
- [PEP 709：Inlined Comprehensions](https://peps.python.org/pep-0709/)
