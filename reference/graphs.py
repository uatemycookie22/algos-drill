"""Canonical graph algorithms — Tier 1 & Tier 3."""
from collections import deque, defaultdict
import heapq

type Graph = dict[int, list[int]]
type WeightedGraph = dict[int, list[tuple[int, int]]]


def build_adjacency_list(n: int, edges: list[tuple[int, int]], directed: bool = False) -> Graph:
    """Edge list -> adjacency list. `n` nodes labeled 0..n-1."""
    adj: Graph = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        if not directed:
            adj[v].append(u)
    return adj


def bfs(adj: Graph, start: int) -> list[int]:
    """Breadth-first traversal. Returns visit order."""
    visited: set[int] = {start}
    queue: deque[int] = deque([start])
    order: list[int] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nb in adj[node]:
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
    return order


def bfs_shortest_dist(adj: Graph, start: int) -> dict[int, int]:
    """BFS that tracks distance (# edges) from start to every reachable node."""
    dist: dict[int, int] = {start: 0}
    queue: deque[int] = deque([start])
    while queue:
        node = queue.popleft()
        for nb in adj[node]:
            if nb not in dist:
                dist[nb] = dist[node] + 1
                queue.append(nb)
    return dist


def dfs_recursive(adj: Graph, start: int, visited: set[int] | None = None, order: list[int] | None = None) -> list[int]:
    """Depth-first traversal, recursive form."""
    if visited is None:
        visited, order = set(), []
    assert order is not None
    visited.add(start)
    order.append(start)
    for nb in adj[start]:
        if nb not in visited:
            dfs_recursive(adj, nb, visited, order)
    return order


def dfs_iterative(adj: Graph, start: int) -> list[int]:
    """Depth-first traversal, explicit-stack form."""
    visited: set[int] = set()
    stack: list[int] = [start]
    order: list[int] = []
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        for nb in reversed(adj[node]):
            if nb not in visited:
                stack.append(nb)
    return order


def num_islands(grid: list[list[str]]) -> int:
    """Count connected regions of '1's in a grid."""
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    seen: set[tuple[int, int]] = set()
    count = 0

    def sink(r: int, c: int) -> None:
        stack: list[tuple[int, int]] = [(r, c)]
        while stack:
            cr, cc = stack.pop()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = cr + dr, cc + dc
                if (0 <= nr < rows and 0 <= nc < cols
                        and grid[nr][nc] == "1" and (nr, nc) not in seen):
                    seen.add((nr, nc))
                    stack.append((nr, nc))

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and (r, c) not in seen:
                seen.add((r, c))
                sink(r, c)
                count += 1
    return count


def topo_sort_kahn(n: int, edges: list[tuple[int, int]]) -> list[int] | None:
    """Topological order via Kahn's algorithm. Returns None if cycle exists."""
    adj: Graph = defaultdict(list)
    indeg: list[int] = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1

    queue: deque[int] = deque(i for i in range(n) if indeg[i] == 0)
    order: list[int] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nb in adj[node]:
            indeg[nb] -= 1
            if indeg[nb] == 0:
                queue.append(nb)
    return order if len(order) == n else None


def dijkstra(adj: WeightedGraph, start: int, n: int) -> list[float]:
    """Shortest paths with non-negative weights. adj[u] = [(v, weight), ...]."""
    dist: list[float] = [float("inf")] * n
    dist[start] = 0
    heap: list[tuple[float, int]] = [(0, start)]
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue
        for nb, w in adj[node]:
            nd = d + w
            if nd < dist[nb]:
                dist[nb] = nd
                heapq.heappush(heap, (nd, nb))
    return dist
