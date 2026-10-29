# 如何维护 Runoria

Runoria 优先保证**知识正确、代码可验证、目录易于查找**，而不是尽可能收集更多示例。

## 新增知识条目

1. 根据内容归类：算法放在 `algorithms/`，Python 的语言特性与惯用法放在 `python/idioms/`，性能测量放在 `benchmarks/`。
2. 参考 [docs/learning_template.md](docs/learning_template.md) 写 Markdown，说明用途、完整或局部示例、边界条件、最低 Python 版本和可靠来源。
3. 把真正需要复用或测试的实现放在 `.py` 文件中；示例代码应避免不必要的网络、写盘等副作用。
4. 算法至少覆盖空输入、单元素、正常输入、重复元素和特殊边界；明确是否修改原输入。
5. 如涉及性能，必须说明数据规模、输入类型、测量工具、重复次数及预热方法，不应将 JIT 编译耗时与运行耗时混为一谈。
6. 更新根目录 README 的索引，避免只有文件名却无法从首页找到。

## 本地验证

```bash
python -m pip install -r requirements-dev.txt
python -m compileall -q algorithms benchmarks tests
python -m pytest -q
```

CI 包含 Python 3.10 / 3.12 / 3.13 的标准库算法测试，以及 Python 3.12 的可选 Numba 实验冒烟测试。后者只验证实验能够运行且排序结果正确，不以性能数值作为 CI 通过标准；实验所需的 NumPy 和 Numba 不作为普通学习的必需依赖。

## 命名和提交约定

- 文件、目录统一采用小写 `snake_case`，无需在文件名中使用括号或空格。
- 一个知识点尽量对应一篇主文档；避免重复或相互矛盾的解释。
- 提交信息建议使用 `docs:`、`feat:`、`fix:`、`test:`、`refactor:` 等前缀，说明具体更改。
- 保留个人化的写作风格，但技术事实、版本边界和可运行代码必须准确。
- 引用教程或开源项目时提供链接及必要的许可信息，不直接复制整篇第三方资料。
