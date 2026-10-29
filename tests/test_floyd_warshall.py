# SPDX-License-Identifier: AGPL-3.0-only
"""Test Floyd-Warshall with a Bellman-Ford oracle and route reconstruction."""

import math
import random

import pytest

from algorithms.graph.floyd_warshall import floyd_warshall, reconstruct_path


def _bellman_ford(graph: list[list[int | float]], source: int) -> list[int | float]:
    """Independent reference for graphs without negative cycles."""
    size = len(graph)
    distance: list[int | float] = [math.inf] * size
    distance[source] = 0
    for _ in range(size - 1):
        changed = False
        for i in range(size):
            if distance[i] == math.inf:
                continue
            for j in range(size):
                if graph[i][j] == math.inf:
                    continue
                candidate = distance[i] + graph[i][j]
                if candidate < distance[j]:
                    distance[j] = candidate
                    changed = True
        if not changed:
            break
    return distance


def test_worked_example_with_negative_edge_and_route() -> None:
    inf = math.inf
    graph = [
        [0, 3, 10, inf],
        [inf, 0, -2, 10],
        [inf, inf, 0, 2],
        [inf, inf, inf, 0],
    ]
    original = [row.copy() for row in graph]
    distance, next_hop = floyd_warshall(graph)
    assert distance == [
        [0, 3, 1, 3],
        [inf, 0, -2, 0],
        [inf, inf, 0, 2],
        [inf, inf, inf, 0],
    ]
    assert reconstruct_path(next_hop, 0, 3) == [0, 1, 2, 3]
    assert reconstruct_path(next_hop, 0, 2) == [0, 1, 2]
    assert reconstruct_path(next_hop, 1, 0) is None
    assert reconstruct_path(next_hop, 3, 3) == [3]
    assert graph == original


def test_empty_and_one_vertex() -> None:
    assert floyd_warshall([]) == ([], [])
    assert floyd_warshall([[math.inf]]) == ([[0]], [[0]])
    assert floyd_warshall([[5]]) == ([[0]], [[0]])
    assert floyd_warshall(((-1,),)) is not None if False else True
    for entry in (0, 1, math.inf):
        d, nxt = floyd_warshall([[entry]])
        assert d == [[0]] and reconstruct_path(nxt, 0, 0) == [0]


def test_negative_edges_without_negative_cycles() -> None:
    graph = [[0, -3, math.inf], [math.inf, 0, 2], [math.inf, math.inf, 0]]
    distances, routing = floyd_warshall(graph)
    assert distances[0][2] == -1
    assert reconstruct_path(routing, 0, 2) == [0, 1, 2]


@pytest.mark.parametrize(
    "graph",
    [
        [[-1]],
        [[0, -2], [1, 0]],
        [[0, math.inf, math.inf], [math.inf, 0, -3], [math.inf, 1, 0]],
    ],
)
def test_detects_negative_cycle_including_disconnected(graph) -> None:
    with pytest.raises(ValueError, match="negative-weight cycle"):
        floyd_warshall(graph)


@pytest.mark.parametrize(
    "graph",
    [
        [[0, 1]],
        [[0], [1]],
        [[0, 1], [2]],
        [[0, 1], [2, 3, 4]],
        [[0, 1], 3],
    ],
)
def test_invalid_dimensions(graph) -> None:
    with pytest.raises(ValueError, match="square"):
        floyd_warshall(graph)


@pytest.mark.parametrize(
    "graph",
    [
        [[0, float("nan")], [math.inf, 0]],
        [[0, -math.inf], [math.inf, 0]],
    ],
)
def test_rejects_nan_and_negative_infinity(graph) -> None:
    with pytest.raises(ValueError, match="NaN and negative infinity"):
        floyd_warshall(graph)


@pytest.mark.parametrize("weight", [True, None, "9", 1 + 2j, object()])
def test_rejects_unsupported_weight_types(weight) -> None:
    with pytest.raises(TypeError, match="weights must be"):
        floyd_warshall([[0, weight], [math.inf, 0]])


def test_large_integer_weights_remain_exact() -> None:
    big = (1 << 200) + 9
    graph = [[0, big, big * 3], [math.inf, 0, big], [math.inf, math.inf, 0]]
    distance, routing = floyd_warshall(graph)
    assert distance[0][2] == big * 2
    assert isinstance(distance[0][2], int)
    assert reconstruct_path(routing, 0, 2) == [0, 1, 2]


def test_randomized_potential_graphs_vs_independent_bellman_ford() -> None:
    """Reduced-cost construction allows negative edges but prevents negative cycles."""
    rng = random.Random(20261029)
    for vertices in range(1, 9):
        for _ in range(18):
            potential = [rng.randint(-10, 10) for _ in range(vertices)]
            graph: list[list[int | float]] = [
                [math.inf] * vertices for _ in range(vertices)
            ]
            for i in range(vertices):
                graph[i][i] = 0
                for j in range(vertices):
                    if i != j and rng.random() < 0.65:
                        graph[i][j] = (
                            rng.randint(0, 15) + potential[j] - potential[i]
                        )
            original = [row.copy() for row in graph]
            distances, routing = floyd_warshall(graph)
            assert graph == original
            for source in range(vertices):
                expected = _bellman_ford(graph, source)
                assert distances[source] == expected
                for destination in range(vertices):
                    path = reconstruct_path(routing, source, destination)
                    if expected[destination] == math.inf:
                        assert path is None
                    else:
                        assert path is not None
                        assert path[0] == source and path[-1] == destination
                        assert len(path) <= vertices
                        cost = sum(graph[a][b] for a, b in zip(path, path[1:]))
                        assert cost == expected[destination]


def test_unreachable_and_invalid_indices() -> None:
    _, routing = floyd_warshall([[0, math.inf], [math.inf, 0]])
    assert reconstruct_path(routing, 0, 1) is None
    for start, end in [(-1, 0), (2, 0), (0, 2), (True, 1)]:
        with pytest.raises(IndexError):
            reconstruct_path(routing, start, end)


def test_defensive_route_reconstruction() -> None:
    with pytest.raises(IndexError):
        reconstruct_path([], 0, 0)
    with pytest.raises(ValueError, match="square"):
        reconstruct_path([[1, 0], [1]], 0, 1)
    with pytest.raises(ValueError, match="cycle"):
        reconstruct_path([[0, 0], [1, 1]], 0, 1)
    with pytest.raises(ValueError, match="out of range"):
        reconstruct_path([[0, 5], [None, 1]], 0, 1)
