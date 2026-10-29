# SPDX-License-Identifier: AGPL-3.0-only
"""防止仓库首页退化为仅列出部分知识点的链接清单。

本测试检查首页能覆盖每个已有算法及 Python 笔记的真实入口。
讲解质量、推导与示例仍须由维护者在 PR 审查中检查。
"""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")


def knowledge_sources() -> list[Path]:
    sources = [
        p for p in (ROOT / "algorithms").rglob("*.py")
        if p.name != "__init__.py"
    ]
    sources.extend((ROOT / "algorithms").rglob("README.md"))
    sources.extend((ROOT / "python" / "idioms").glob("*.md"))
    sources.extend(
        p for p in (ROOT / "benchmarks").glob("*.py")
        if p.name != "__init__.py"
    )
    return sorted(sources)


@pytest.mark.parametrize(
    "source",
    knowledge_sources(),
    ids=lambda p: str(p.relative_to(ROOT)),
)
def test_each_knowledge_topic_is_referenced_from_root_readme(source: Path) -> None:
    relative = source.relative_to(ROOT).as_posix()
    assert relative in README, f"Missing homepage explanation/link for {relative}"


def test_homepage_contains_substantive_algorithm_explanations() -> None:
    # Minimum safeguards, not a substitute for reviewing the real explanations.
    assert "## 算法（Algorithms）" in README
    assert "### 冒泡排序（Bubble Sort）" in README
    assert "### 卡拉楚巴算法（Karatsuba Multiplication）" in README
    assert "### 堆排序（Heap Sort）" in README
    assert "### 二分搜索（Binary Search）" in README
    assert "### Trie 前缀树（Prefix Tree）" in README
    assert "### 动态规划（DP）与 0/1 背包" in README
    assert "### Dijkstra 最短路径算法" in README
    assert "T(n)=3T(n/2)" in README
    assert "最好时间复杂度" in README
    assert "## Python 惯用写法与语言特性" in README
    assert README.count("```python") >= 8
