"""逐个执行 python/idioms 中独立的 Python 示例。

只验证仓库维护者编写的本地 Markdown，不运行来自网络的任意内容。
凡是不能独立执行的占位语法，应使用 text 代码围栏。
"""

from pathlib import Path
import re

import pytest

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "python" / "idioms"
PYTHON_BLOCK = re.compile(r"^```python[ \t]*\n(.*?)^```[ \t]*$", re.MULTILINE | re.DOTALL)


def examples() -> list:
    cases = []
    for document in sorted(DOCS.glob("*.md")):
        blocks = PYTHON_BLOCK.findall(document.read_text(encoding="utf-8"))
        if not blocks:
            raise AssertionError(f"No runnable Python examples in {document}")
        for index, code in enumerate(blocks, 1):
            cases.append(pytest.param(document.name, index, code, id=f"{document.stem}:{index}"))
    return cases


@pytest.mark.parametrize("filename,index,code", examples())
def test_python_example_runs_alone(filename: str, index: int, code: str) -> None:
    namespace = {"__name__": "__runoria_example__"}
    exec(compile(code, f"{filename}:example:{index}", "exec"), namespace)
