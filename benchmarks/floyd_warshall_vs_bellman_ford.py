# SPDX-License-Identifier: AGPL-3.0-only
"""Educational timing: Floyd-Warshall vs repeated Bellman-Ford.

Run from the repository root:
    python -m benchmarks.floyd_warshall_vs_bellman_ford --vertices 16 --density 0.6 --number 2 --repeat 3

The graph generator uses reduced nonnegative edge costs plus vertex potentials.
This allows negative edge weights while ensuring no negative-weight cycles.
The benchmark compares two pure Python algorithms, not production graph tools.
"""

import argparse
import math
import random
import statistics
import timeit

from algorithms.graph.floyd_warshall import floyd_warshall


def all_pairs_bellman_ford(
    graph: list[list[int | float]],
) -> list[list[int | float]]:
    """Independent O(V^2 E) worst-case baseline for all sources."""
    n = len(graph)
    output: list[list[int | float]] = []
    for source in range(n):
        distances: list[int | float] = [math.inf] * n
        distances[source] = 0
        for _ in range(n - 1):
            changed = False
            for u in range(n):
                if distances[u] == math.inf:
                    continue
                for v in range(n):
                    w = graph[u][v]
                    if w == math.inf:
                        continue
                    candidate = distances[u] + w
                    if candidate < distances[v]:
                        distances[v] = candidate
                        changed = True
            if not changed:
                break
        output.append(distances)
    return output


def benchmark(
    vertices: int = 16,
    density: float = 0.6,
    number: int = 2,
    repeat: int = 3,
) -> tuple[float, float]:
    """Return median seconds/call for Floyd-Warshall and Bellman-Ford."""
    if any(
        isinstance(value, bool) or not isinstance(value, int) or value < 1
        for value in (vertices, number, repeat)
    ):
        raise ValueError("vertices, number and repeat must be positive integers")
    if (
        isinstance(density, bool)
        or not isinstance(density, (int, float))
        or not math.isfinite(density)
        or not 0 <= density <= 1
    ):
        raise ValueError("density must be a finite number between 0 and 1")

    rng = random.Random(20261029)
    potential = [rng.randint(-20, 20) for _ in range(vertices)]
    graph: list[list[int | float]] = [
        [math.inf] * vertices for _ in range(vertices)
    ]
    for u in range(vertices):
        graph[u][u] = 0
        for v in range(vertices):
            if u != v and rng.random() < density:
                graph[u][v] = rng.randint(0, 20) + potential[v] - potential[u]

    expected = all_pairs_bellman_ford(graph)
    actual, _ = floyd_warshall(graph)
    if actual != expected:
        raise RuntimeError("Floyd-Warshall and Bellman-Ford disagree")

    fw_times = timeit.repeat(
        lambda: floyd_warshall(graph), number=number, repeat=repeat
    )
    bf_times = timeit.repeat(
        lambda: all_pairs_bellman_ford(graph), number=number, repeat=repeat
    )
    return (
        statistics.median(fw_times) / number,
        statistics.median(bf_times) / number,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vertices", type=int, default=16, help="Number of vertices")
    parser.add_argument("--density", type=float, default=0.6, help="Directed edge probability")
    parser.add_argument("--number", type=int, default=2, help="Calls per round")
    parser.add_argument("--repeat", type=int, default=3, help="Timed rounds")
    args = parser.parse_args()

    fw_seconds, bf_seconds = benchmark(
        args.vertices, args.density, args.number, args.repeat
    )
    print(f"Vertices: {args.vertices}; edge density: {args.density}")
    print(f"Floyd-Warshall:        {fw_seconds:.7f}s per call (median)")
    print(f"Repeated Bellman-Ford: {bf_seconds:.7f}s per call (median)")
    print("No speedup is assumed; input generation and validation are excluded.")


if __name__ == "__main__":
    main()
