# SPDX-License-Identifier: AGPL-3.0-only
"""A character Trie (prefix tree) supporting insert, lookup and deletion.

Supports Unicode Python strings, including the empty string. It is
case-sensitive; it performs no Unicode normalization or case folding.
"""

from dataclasses import dataclass, field


@dataclass
class _Node:
    children: dict[str, "_Node"] = field(default_factory=dict)
    terminal: bool = False


class Trie:
    """A mutable prefix tree with O(L) operations for word length L.

    Auxiliary storage is O(total number of stored character nodes).
    """

    def __init__(self) -> None:
        self._root = _Node()
        self._size = 0

    def __len__(self) -> int:
        return self._size

    @staticmethod
    def _validate(word: str) -> None:
        if not isinstance(word, str):
            raise TypeError("Trie words and prefixes must be strings")

    def _walk(self, prefix: str) -> _Node | None:
        current = self._root
        for character in prefix:
            following = current.children.get(character)
            if following is None:
                return None
            current = following
        return current

    def insert(self, word: str) -> bool:
        """Insert a word. Return True if newly inserted, False if already stored."""
        self._validate(word)
        node = self._root
        for character in word:
            node = node.children.setdefault(character, _Node())
        if node.terminal:
            return False
        node.terminal = True
        self._size += 1
        return True

    def contains(self, word: str) -> bool:
        """Check whether word is stored as a COMPLETE word."""
        self._validate(word)
        node = self._walk(word)
        return node is not None and node.terminal

    def starts_with(self, prefix: str) -> bool:
        """Check for a matching prefix; the empty prefix always matches."""
        self._validate(prefix)
        return self._walk(prefix) is not None

    def delete(self, word: str) -> bool:
        """Delete a stored word and prune orphaned nodes, keeping shared prefixes."""
        self._validate(word)
        node = self._root
        chain: list[tuple[_Node, str]] = []
        for character in word:
            following = node.children.get(character)
            if following is None:
                return False
            chain.append((node, character))
            node = following
        if not node.terminal:
            return False
        node.terminal = False
        self._size -= 1
        for parent, character in reversed(chain):
            child = parent.children[character]
            if child.terminal or child.children:
                break
            del parent.children[character]
        return True


if __name__ == "__main__":
    trie = Trie()
    trie.insert("cat")
    trie.insert("car")
    assert trie.contains("cat") and trie.starts_with("ca")
    assert not trie.contains("ca")
    assert trie.delete("cat") and trie.contains("car")
    print("Trie words:", len(trie))
