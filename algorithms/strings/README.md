# Trie 前缀树（Prefix Tree）

> 归类：字符串 / 树形数据结构  
> 源码：[trie.py](trie.py) · 测试：[test_trie.py](../../tests/test_trie.py)

## 目的与结构

Trie 将多个单词按**字符前缀**合并存储。例如 `cat`、`car` 共用前两个节点 `c→a`，之后才分成 `t` 和 `r`。

```text
(root)
  └── c
      └── a
          ├── t *  (cat)
          └── r *  (car)
```

星号表示 `terminal=True`：即便某节点存在，也只有 `terminal` 为真才代表存入了完整单词。否则，`"ca"` 是前缀，却不是已存在的完整单词。

本仓库的 Trie 是纯 Python 教学实现，内部 `_Node` 保存 `children: dict[str,_Node]` 和 `terminal` 标志，并记录不同单词的数量。

## 使用 API

```python
from algorithms.strings.trie import Trie

trie = Trie()
assert trie.insert("cat")  # 新增成功
assert trie.insert("car")
assert not trie.insert("cat")  # 重复插入
assert trie.contains("cat")
assert trie.starts_with("ca")
assert not trie.contains("ca")
assert trie.delete("cat")
assert not trie.contains("cat") and trie.contains("car")
assert len(trie) == 1
```

删除单词时只去掉它的 `terminal` 标记，并从底部清理不再需要的孤立节点；**共享前缀与其他单词不会被错误删除**。

## 边界与限制

- 支持空字符串：`insert("")` 会把根标为单词结束；`starts_with("")` 始终返回真。
- 支持 Unicode 字符串（中文、emoji 等），**区分大小写**；不会自动做 Unicode 规范化或大小写折叠。
- 只接受 `str`，其他对象抛出 `TypeError`。
- `insert/contains/starts_with/delete` 对长度为 L 的单词，在通常的哈希字典平均成本假设下为 `O(L)`。
- 额外存储与所有不同单词的字符节点总数成正比，字典节点对象有实际 Python 内存开销。
- 适合前缀查询、自动补全结构的基础学习；若要处理极大规模词典，可考虑压缩 Trie、DAWG 或其他专门结构。

测试覆盖了共享前缀、删除、重复添加、空字符串、Unicode、类型错误和随机操作与 Python `set` 的交叉比较。

参考：[Wikipedia — Trie](https://en.wikipedia.org/wiki/Trie)；[Python dataclasses](https://docs.python.org/3/library/dataclasses.html)。