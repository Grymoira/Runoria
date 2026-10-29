# SPDX-License-Identifier: AGPL-3.0-only
"""Dijkstra's single-source shortest paths using a binary min-heap.

The graph is an adjacency list indexed by vertices 0..n-1:
    graph[u] = [(neighbor, nonnegative_weight), ...]
Negative, NaN, infinite and non-numeric edge weights are rejected.
"""

import heapq
import math
from collections.abc import Sequence

Weight = int | float
AdjacencyList = Sequence[Sequence[tuple[int, Weight]]]


def dijkstra(
    graph: AdjacencyList, source: int
) -> tuple[list[Weight], list[int | None]]:
    """Return (shortest distances, predecessors) without modifying graph.

    Unreachable vertices have distance math.inf and predecessor None.
    The source has distance 0 and predecessor None. Floating-point overflow
    is rejected to avoid mistaking a representable edge for no route.

    Complexity with adjacency lists and heapq: O((V+E) log V) time,
    O(V+E) for the copied validated graph plus O(E) for heap entries worst-case.
    """
    if not isinstance(graph, (list, tuple)):
        raise TypeError("graph must be an adjacency list (list or tuple)")
    n = len(graph)
    if isinstance(source, bool) or not isinstance(source, int) or not 0 <= source < n:
        raise IndexError("source must be a vertex index within the graph")

    adjacency: list[list[tuple[int, Weight]]] = []
    for row in graph:
        if not isinstance(row, (list, tuple)):
            raise TypeError("each adjacency row must be a list or tuple")
        checked: list[tuple[int, Weight]] = []
        for edge in row:
            if not isinstance(edge, (list, tuple)) or len(edge) != 2:
                raise ValueError("edges must be (neighbor, weight) pairs")
            neighbor, weight = edge
            if (
                isinstance(neighbor, bool)
                or not isinstance(neighbor, int)
                or not 0 <= neighbor < n
            ):
                raise IndexError("neighbor must be a valid vertex index")
            if (
                isinstance(weight, bool)
                or not isinstance(weight, (int, float))
            ):
                raise TypeError("edge weights must be int or float")
            if (isinstance(weight, float) and not math.isfinite(weight)) or weight < 0:
                raise ValueError("Dijkstra requires finite nonnegative edge weights")
            checked.append((neighbor, weight))
        adjacency.append(checked)

    distances: list[Weight] = [math.inf] * n
    predecessors: list[int | None] = [None] * n
    distances[source] = 0
    heap: list[tuple[Weight, int]] = [(0, source)]

    while heap:
        current_distance, u = heapq.heappop(heap)
        if current_distance > distances[u]:
            continue
        for v, weight in adjacency[u]:
            candidate = current_distance + weight
            if isinstance(candidate, float) and not math.isfinite(candidate):
                raise OverflowError("floating-point path weight overflow")
            if candidate < distances[v]:
                distances[v] = candidate
                predecessors[v] = u
                heapq.heappush(heap, (candidate, v))
    return distances, predecessors


def reconstruct_dijkstra_path(
    predecessors: Sequence[int | None],
    source: int,
    target: int,
) -> list[int] | None:
    """Return source-to-target inclusive route, or None when unreachable.

    Valid predecessor tables from dijkstra never contain a cycle.
    A malformed table raises ValueError rather than looping forever.
    """
    n = len(predecessors)
    if (
        isinstance(source, bool)
        or isinstance(target, bool)
        or not isinstance(source, int)
        or not isinstance(target, int)
        or not 0 <= source < n
        or not 0 <= target < n
    ):
        raise IndexError("source and target must be valid vertex indices")
    if source == target:
        return [source]

    path: list[int] = []
    current = target
    seen: set[int] = set()
    while current != source:
        if current in seen:
            raise ValueError("predecessor table contains a cycle")
        seen.add(current)
        path.append(current)
        next_vertex = predecessors[current]
        if next_vertex is None:
            return None
        if (
            isinstance(next_vertex, bool)
            or not isinstance(next_vertex, int)
            or not 0 <= next_vertex < n
        ):
            raise ValueError("predecessor table contains an invalid vertex")
        current = next_vertex
    path.append(source)
    path.reverse()
    return path


if __name__ == "__main__":
    graph = [[(1, 4), (2, 1)], [(3, 1)], [(1, 2), (3, 5)], []]
    distances, predecessors = dijkstra(graph, 0)
    assert distances[3] == 4
    assert reconstruct_dijkstra_path(predecessors, 0, 3) == [0, 2, 1, 3]
    print("Shortest 0 -> 3:", distances[3])
