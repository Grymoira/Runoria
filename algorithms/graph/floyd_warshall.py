# SPDX-License-Identifier: AGPL-3.0-only
"""Floyd-Warshall all-pairs shortest paths with route reconstruction.

Use a square adjacency matrix: edge weights are integers or finite floats;
math.inf indicates the absence of an edge. Negative edges are allowed, but a
negative cycle raises ValueError, since finite shortest distances then do not
exist for all reachable vertex pairs.
"""

import math
from collections.abc import Sequence

Weight = int | float
AdjacencyMatrix = Sequence[Sequence[Weight]]
DistanceMatrix = list[list[Weight]]
NextHopMatrix = list[list[int | None]]


def floyd_warshall(
    graph: AdjacencyMatrix,
) -> tuple[DistanceMatrix, NextHopMatrix]:
    """Compute every shortest distance and the next-hop routing table.

    Input must be a square list/tuple of rows of int/float values, with
    math.inf marking missing edges. NaN and negative infinity are rejected.
    An empty graph produces two empty matrices. Missing/positive diagonal
    entries are normalized to 0, representing the empty path to oneself.

    Returns:
        (distances, next_hop) as independent new matrices. A missing route
        has distance math.inf and next_hop[i][j] is None.

    Raises:
        ValueError: For invalid dimensions, weights, or a negative cycle.
        TypeError: For unsupported edge-weight types.
    """
    if not isinstance(graph, (list, tuple)):
        raise TypeError("graph must be a square list or tuple of rows")

    size = len(graph)
    if size == 0:
        return [], []

    distances: DistanceMatrix = []
    for row in graph:
        if not isinstance(row, (list, tuple)) or len(row) != size:
            raise ValueError("graph must be a square adjacency matrix")
        copied_row: list[Weight] = []
        for weight in row:
            if isinstance(weight, bool) or not isinstance(weight, (int, float)):
                raise TypeError("edge weights must be int or float (or math.inf)")
            if isinstance(weight, float) and (
                math.isnan(weight) or weight == -math.inf
            ):
                raise ValueError("NaN and negative infinity are not valid weights")
            copied_row.append(weight)
        distances.append(copied_row)

    next_hop: NextHopMatrix = [[None] * size for _ in range(size)]
    for i in range(size):
        distances[i][i] = min(distances[i][i], 0)
        next_hop[i][i] = i
        for j in range(size):
            if i != j and distances[i][j] != math.inf:
                next_hop[i][j] = j

    # Invariant: after processing k, paths may use vertices 0..k as
    # intermediate vertices; previously processed vertices remain allowed.
    for k in range(size):
        for i in range(size):
            left = distances[i][k]
            if left == math.inf:
                continue
            for j in range(size):
                right = distances[k][j]
                if right == math.inf:
                    continue
                through_k = left + right
                if through_k < distances[i][j]:
                    distances[i][j] = through_k
                    next_hop[i][j] = next_hop[i][k]

    # Every negative cycle is reflected by a negative diagonal entry.
    if any(distances[v][v] < 0 for v in range(size)):
        raise ValueError("graph contains a negative-weight cycle")

    return distances, next_hop


def reconstruct_path(
    next_hop: NextHopMatrix, start: int, end: int
) -> list[int] | None:
    """Rebuild a shortest path (inclusive) from a Floyd-Warshall next-hop table.

    Returns None when no route exists; start==end returns [start]. A malformed
    routing table or a routing cycle raises ValueError instead of looping.
    Vertex indices outside the table raise IndexError.
    """
    size = len(next_hop)
    if (
        isinstance(start, bool)
        or isinstance(end, bool)
        or not isinstance(start, int)
        or not isinstance(end, int)
        or not (0 <= start < size and 0 <= end < size)
    ):
        raise IndexError("start and end must be valid vertex indices")
    if any(not isinstance(row, (list, tuple)) or len(row) != size for row in next_hop):
        raise ValueError("next_hop must be a square matrix")

    if next_hop[start][end] is None:
        return None

    path = [start]
    current = start
    # With no negative cycle, a shortest route can be chosen to be simple.
    # At most size-1 edges are needed.
    for _ in range(size):
        if current == end:
            return path
        successor = next_hop[current][end]
        if isinstance(successor, bool) or not isinstance(successor, int):
            raise ValueError("malformed next-hop route")
        if not 0 <= successor < size:
            raise ValueError("next-hop vertex is out of range")
        path.append(successor)
        current = successor
    raise ValueError("next-hop routing table contains a cycle")


if __name__ == "__main__":
    inf = math.inf
    graph = [
        [0, 3, 10, inf],
        [inf, 0, -2, 10],
        [inf, inf, 0, 2],
        [inf, inf, inf, 0],
    ]
    distances, routes = floyd_warshall(graph)
    assert distances[0][3] == 3
    assert reconstruct_path(routes, 0, 3) == [0, 1, 2, 3]
    print("Distances:", distances)
    print("Shortest 0 -> 3:", reconstruct_path(routes, 0, 3))
