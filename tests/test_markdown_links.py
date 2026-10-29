"""保证目录迁移不会破坏已有 Markdown 相对链接。"""

from pathlib import Path
import re

import pytest

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def markdown_files() -> list[Path]:
    sources = [ROOT / "README.md", ROOT / "CONTRIBUTING.md"]
    for folder in ("algorithms", "docs", "python"):
        sources.extend((ROOT / folder).rglob("*.md"))
    return sorted(sources)


@pytest.mark.parametrize(
    "document", markdown_files(), ids=lambda p: str(p.relative_to(ROOT))
)
def test_markdown_local_links_exist(document: Path) -> None:
    content = document.read_text(encoding="utf-8")
    for dest in MARKDOWN_LINK.findall(content):
        target = dest.strip().split("#", 1)[0]
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        assert (document.parent / target).exists(), f"Invalid link in {document}: {dest}"
