# SPDX-License-Identifier: AGPL-3.0-only
"""Dijkstra versus Floyd-Warshall plus route reconstruction tests."""

import math
import random

import pytest

from algorithms.graph.dijkstra import dijkstra, reconstruct_dijkstra_path
from algorithms.graph.floyd_warshall import floyd_warshall


def test_example_and_unreachable_route() -> None:
    graph = [[(1, 4), (2, 1)], [(3, 1)], [(1, 2), (3, 5)], []]
    before = [row[:] for row in graph]
    distances, predecessors = dijkstra(graph, 0)
    assert distances == [0, 3, 1, 4]
    assert reconstruct_dijkstra_path(predecessors, 0, 3) == [0, 2, 1, 3]
    assert reconstruct_dijkstra_path(predecessors, 0, 0) == [0]
    assert graph == before


def test_zero_weights_and_equal_costs() -> None:
    graph = [[(1, 0), (2, 1)], [(2, 0)], []]
    distances, predecessors = dijkstra(graph, 0)
    assert distances == [0, 0, 0]
    assert reconstruct_dijkstra_path(predecessors, 0, 2) == [0, 1, 2]


def test_single_vertex_and_disconnected() -> None:
    assert dijkstra([[]], 0) == ([0], [None])
    dist, parent = dijkstra([[(1, 7)], [], []], 0)
    assert dist == [0, 7, math.inf]
    assert reconstruct_dijkstra_path(parent, 0, 2) is None


def test_randomized_graph_vs_floyd_warshall() -> None:
    rng = random.Random(20261029)
    for n in range(1, 13):
        for _ in range(20):
            graph: list[list[tuple[int, int]]] = [[] for _ in range(n)]
            matrix: list[list[int | float]] = [
                [math.inf] * n for _ in range(n)
            ]
            for i in range(n):
                matrix[i][i] = 0
                for j in range(n):
                    if i != j and rng.random() < 0.32:
                        cost = rng.randint(0, 30)
                        graph[i].append((j, cost))
                        matrix[i][j] = cost
            floyd_distances, _ = floyd_warshall(matrix)
            for source in range(n):
                distances, predecessors = dijkstra(graph, source)
                assert distances == floyd_distances[source]
                for target in range(n):
                    path = reconstruct_dijkstra_path(predecessors, source, target)
                    if distances[target] == math.inf:
                        assert path is None
                    else:
                        assert path is not None and path[0] == source and path[-1] == target
                        assert len(path) <= n
                        assert sum(matrix[a][b] for a, b in zip(path, path[1:])) == distances[target]


@pytest.mark.parametrize("graph,source,error", [
    ([], 0, IndexError),
    ([[]], -1, IndexError),
    ([[]], 1, IndexError),
    ([[]], True, IndexError),
    ([[(1, 2)]], 0, IndexError),
    ([[(0, -1)]], 0, ValueError),
    ([[(0, math.inf)]], 0, ValueError),
    ([[(0, math.nan)]], 0, ValueError),
    ([[(0, "x")]], 0, TypeError),
    ([[(0, True)]], 0, TypeError),
    ([[("0", 1)]], 0, IndexError),
    ([[1]], 0, ValueError),
    ([None], 0, TypeError),
])
def test_invalid_graphs(graph, source, error) -> None:
    with pytest.raises(error):
        dijkstra(graph, source)


def test_large_exact_ints_and_float_overflow() -> None:
    huge = 1 << 300
    assert dijkstra([[(1, huge)], []], 0)[0][1] == huge
    with pytest.raises(OverflowError):
        dijkstra([[(1, 1e308)], [(2, 1e308)], []], 0)


def test_defensive_path_reconstruction() -> None:
    with pytest.raises(IndexError):
        reconstruct_dijkstra_path([None], 0, 1)
    with pytest.raises(ValueError, match="cycle"):
        reconstruct_dijkstra_path([None, 2, 1], 0, 1)
    with pytest.raises(ValueError, match="invalid vertex"):
        reconstruct_dijkstra_path([None, 5], 0, 1)
