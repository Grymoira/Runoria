# any() 与 all()：短路布尔归约

- `any(iterable)`：只要存在一个真值就返回 `True`；没有真值返回 `False`。
- `all(iterable)`：只有全部为真才返回 `True`；遇到假值就返回 `False`。

相比维护额外的布尔状态和 `break`，生成器表达式更容易表达检查目的。

```python
numbers = [1, -3, 5]
has_negative = any(x < 0 for x in numbers)
all_positive = all(x > 0 for x in numbers)
assert has_negative is True
assert all_positive is False
```

## 短路与惰性计算

`any()` 遇到第一个真值就停止；`all()` 遇到第一个假值就停止。因此优先使用生成器表达式：

```python
any(x < 0 for x in numbers)
```

而不是提前计算全部比较结果的列表：

```python
any([x < 0 for x in numbers])
```

## 非常重要：空输入

```python
assert any([]) is False
assert all([]) is True
```

后者称为 **空真（vacuous truth）**：没有元素违反要求，但**不代表**确实存在满足要求的元素。

在验证权限时，还要根据业务规则确认输入不能为空。对于列表等容器：

```python
permissions = []
allowed = bool(permissions) and all(p.is_active for p in permissions)
assert allowed is False
```

注意：上面的非空检查只适用于这里的容器类型。对一个迭代器调用 `bool(iterator)` 通常不能检测它是否还有元素；需要根据实际数据来源设计验证逻辑。

## 来源

- [Python 内置函数：any](https://docs.python.org/3/library/functions.html#any)
- [Python 内置函数：all](https://docs.python.org/3/library/functions.html#all)
