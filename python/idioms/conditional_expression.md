# 条件表达式（Conditional Expression）

Python 的条件表达式语法：

```text
value_if_true if condition else value_if_false
```

与其他语言的 `condition ? a : b` 风格不同，这一写法更接近自然语言。

传统写法：

```python
score = 60
if score >= 60:
    status = "Pass"
else:
    status = "Fail"
```

等价的简洁写法：

```python
score = 60
status = "Pass" if score >= 60 else "Fail"
assert status == "Pass"
```

## 什么时候适合？

- 简单的二选一赋值，阅读成本低。
- 结合列表推导式，对每个元素做条件映射。

```python
raw_data = [-3, 0, 5]
processed = [x if x > 0 else 0 for x in raw_data]
assert processed == [0, 0, 5]
```

不建议堆叠多层 `... if ... else ... if ... else ...`：条件复杂时请使用普通 `if/elif/else` 或拆分成清晰的函数。

注意：条件表达式会根据条件只求值被选中的那个分支，不能简单理解为先计算两个候选值再选择。

## 求值顺序

条件表达式只求值被选中的分支，未选中的分支不会被计算。

```python
calls = []

def selected():
    calls.append("yes")
    return 1

def skipped():
    calls.append("no")
    return 0

result = selected() if True else skipped()
assert result == 1 and calls == ["yes"]
```

## 来源

[Python 语言参考：Conditional Expressions](https://docs.python.org/3/reference/expressions.html#conditional-expressions)
