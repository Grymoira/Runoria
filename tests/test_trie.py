# SPDX-License-Identifier: AGPL-3.0-only
"""Trie insertion, deletion and Unicode prefix semantics."""

import random

import pytest

from algorithms.strings.trie import Trie


def test_shared_prefixes_and_deletion() -> None:
    tree = Trie()
    assert tree.insert("app")
    assert tree.insert("apple")
    assert tree.insert("application")
    assert tree.insert("apt")
    assert len(tree) == 4
    assert not tree.insert("app")
    assert tree.contains("app")
    assert tree.starts_with("ap")
    assert not tree.contains("ap")
    assert tree.delete("apple")
    assert not tree.contains("apple")
    assert tree.contains("app") and tree.contains("application")
    assert tree.delete("app")
    assert not tree.contains("app")
    assert tree.starts_with("app")
    assert not tree.delete("app")
    assert len(tree) == 2


def test_empty_string_and_unicode_are_explicitly_supported() -> None:
    tree = Trie()
    assert tree.starts_with("")
    assert not tree.contains("")
    assert tree.insert("")
    assert tree.contains("")
    assert tree.insert("中文")
    assert tree.insert("中午")
    assert tree.insert("🍎apple")
    assert tree.starts_with("中") and tree.starts_with("🍎")
    assert tree.contains("中文") and not tree.contains("中")
    assert tree.delete("") and not tree.contains("")
    assert tree.contains("中文")


def test_case_and_normalization_not_implicit() -> None:
    tree = Trie()
    tree.insert("Cat")
    tree.insert("café")
    assert not tree.contains("cat")
    assert not tree.contains("cafe\u0301")
    assert tree.contains("café")


@pytest.mark.parametrize("invalid", [None, 123, True, [], object()])
def test_invalid_strings_rejected(invalid) -> None:
    tree = Trie()
    with pytest.raises(TypeError):
        tree.insert(invalid)
    with pytest.raises(TypeError):
        tree.contains(invalid)
    with pytest.raises(TypeError):
        tree.starts_with(invalid)
    with pytest.raises(TypeError):
        tree.delete(invalid)


def test_random_operations_against_python_set() -> None:
    rng = random.Random(20261029)
    tree = Trie()
    reference: set[str] = set()
    words = ["".join(rng.choice("abc") for _ in range(rng.randrange(0, 9)))
             for _ in range(250)]
    for _ in range(500):
        word = rng.choice(words)
        if rng.random() < 0.5:
            expected = word not in reference
            assert tree.insert(word) == expected
            reference.add(word)
        else:
            expected = word in reference
            assert tree.delete(word) == expected
            reference.discard(word)
        assert len(tree) == len(reference)
        for probe in rng.sample(words, 5):
            assert tree.contains(probe) == (probe in reference)
            prefix = probe[:rng.randrange(len(probe) + 1)]
            assert tree.starts_with(prefix) == (
                prefix == "" or any(w.startswith(prefix) for w in reference)
            )
