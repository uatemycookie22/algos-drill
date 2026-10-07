from collections import defaultdict
from drills import solution as s


def make_graph(n: int, edges: list[tuple[int, int]], directed: bool = False) -> s.Graph:
    return s.build_adjacency_list(n, edges, directed)


def make_chain(n: int) -> s.Graph:
    """0→1→2→...→n-1 undirected chain."""
    return make_graph(n, [(i, i + 1) for i in range(n - 1)])


def make_complete(n: int) -> s.Graph:
    """Every node connected to every other node."""
    edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    return make_graph(n, edges)


def make_grid_graph(rows: int, cols: int) -> s.Graph:
    """Grid graph where each cell connects to its 4 neighbors."""
    def idx(r, c): return r * cols + c
    edges = []
    for r in range(rows):
        for c in range(cols):
            if c + 1 < cols: edges.append((idx(r, c), idx(r, c + 1)))
            if r + 1 < rows: edges.append((idx(r, c), idx(r + 1, c)))
    return make_graph(rows * cols, edges)


class TestBuildAdjacencyList:
    def test_undirected_bidirectional(self):
        adj = s.build_adjacency_list(3, [(0, 1), (1, 2)])
        assert set(adj[0]) == {1},     f"node 0 neighbors: got {set(adj[0])}, want {{1}}"
        assert set(adj[1]) == {0, 2},  f"node 1 neighbors: got {set(adj[1])}, want {{0,2}}"
        assert set(adj[2]) == {1},     f"node 2 neighbors: got {set(adj[2])}, want {{1}}"

    def test_directed_one_way(self):
        adj = s.build_adjacency_list(3, [(0, 1), (1, 2)], directed=True)
        assert list(adj[0]) == [1],  f"directed node 0: got {list(adj[0])}, want [1]"
        assert list(adj[1]) == [2],  f"directed node 1: got {list(adj[1])}, want [2]"
        assert 0 not in adj[2],      f"directed node 2 should have no back-edge to 0, got {adj[2]}"

    def test_no_edges(self):
        adj = s.build_adjacency_list(3, [])
        assert adj[0] == [], f"no edges: node 0 should be [], got {adj[0]}"
        assert adj[1] == [], f"no edges: node 1 should be [], got {adj[1]}"

    def test_self_loop(self):
        adj = s.build_adjacency_list(1, [(0, 0)])
        assert 0 in adj[0], f"self-loop: node 0 should appear in its own neighbors, got {adj[0]}"

    def test_multiple_edges_same_node(self):
        adj = s.build_adjacency_list(4, [(0, 1), (0, 2), (0, 3)])
        assert set(adj[0]) == {1, 2, 3}, f"node 0 with 3 edges: got {set(adj[0])}, want {{1,2,3}}"

    def test_large_undirected(self):
        n = 1000
        edges = [(i, i + 1) for i in range(n - 1)]
        adj = s.build_adjacency_list(n, edges)
        assert set(adj[0]) == {1}, f"large chain: node 0 should only connect to 1"
        assert set(adj[500]) == {499, 501}, f"large chain: node 500 should connect to 499 and 501"
        assert set(adj[n - 1]) == {n - 2}, f"large chain: last node should only connect to {n-2}"

    def test_large_directed(self):
        n = 500
        edges = [(i, (i + 1) % n) for i in range(n)]
        adj = s.build_adjacency_list(n, edges, directed=True)
        for i in range(n):
            assert list(adj[i]) == [(i + 1) % n], \
                f"directed cycle: node {i} should point to {(i+1)%n}, got {adj[i]}"

    def test_star_graph(self):
        n = 100
        edges = [(0, i) for i in range(1, n)]
        adj = s.build_adjacency_list(n, edges)
        assert set(adj[0]) == set(range(1, n)), \
            f"star center should connect to all {n-1} leaves"
        for i in range(1, n):
            assert set(adj[i]) == {0}, f"leaf {i} should only connect to center 0"


class TestBFS:
    def test_visits_all_connected(self):
        edges = [(0, 1), (0, 2), (1, 3), (2, 4)]
        adj = make_graph(5, edges)
        result = set(s.bfs(adj, 0))
        assert result == {0, 1, 2, 3, 4}, \
            f"bfs({edges}, start=0): got {result}, want {{0,1,2,3,4}}"

    def test_starts_at_start(self):
        adj = make_graph(3, [(0, 1), (1, 2)])
        result = s.bfs(adj, 0)
        assert result[0] == 0, f"first visited node should be start=0, got {result[0]}"

    def test_single_node(self):
        adj = make_graph(1, [])
        result = s.bfs(adj, 0)
        assert result == [0], f"single node graph: got {result}, want [0]"

    def test_disconnected_only_visits_reachable(self):
        adj = make_graph(4, [(0, 1)])
        result = s.bfs(adj, 0)
        assert set(result) == {0, 1}, \
            f"disconnected graph starting at 0: got {set(result)}, want {{0,1}} (nodes 2,3 unreachable)"

    def test_no_duplicate_visits(self):
        edges = [(0, 1), (0, 2), (1, 2), (2, 3)]
        adj = make_graph(4, edges)
        result = s.bfs(adj, 0)
        dupes = [x for x in result if result.count(x) > 1]
        assert len(result) == len(set(result)), \
            f"bfs({edges}): node(s) visited more than once: {dupes}"

    def test_breadth_order(self):
        edges = [(0, 1), (0, 2), (1, 3), (1, 4)]
        adj = make_graph(5, edges)
        result = s.bfs(adj, 0)
        assert result.index(0) < result.index(1), \
            f"node 0 (d=0) must come before node 1 (d=1), got order {result}"
        assert result.index(0) < result.index(2), \
            f"node 0 (d=0) must come before node 2 (d=1), got order {result}"
        assert result.index(1) < result.index(3), \
            f"node 1 (d=1) must come before node 3 (d=2), got order {result}"
        assert result.index(1) < result.index(4), \
            f"node 1 (d=1) must come before node 4 (d=2), got order {result}"

    def test_linear_chain(self):
        adj = make_graph(5, [(0, 1), (1, 2), (2, 3), (3, 4)])
        result = s.bfs(adj, 0)
        assert result == [0, 1, 2, 3, 4], \
            f"linear chain 0→1→2→3→4: got {result}, want [0,1,2,3,4]"

    def test_large_chain_visits_all(self):
        n = 500
        adj = make_chain(n)
        result = s.bfs(adj, 0)
        assert set(result) == set(range(n)), \
            f"large chain bfs: visited {len(result)} nodes, expected {n}"
        assert len(result) == n, \
            f"large chain bfs: {n - len(result)} nodes missed"

    def test_large_chain_order(self):
        n = 500
        adj = make_chain(n)
        result = s.bfs(adj, 0)
        assert result == list(range(n)), \
            f"large chain bfs from 0: should visit in order 0,1,2,...,{n-1}, got {result[:5]}..."

    def test_large_complete_graph(self):
        n = 50
        adj = make_complete(n)
        result = s.bfs(adj, 0)
        assert set(result) == set(range(n)), \
            f"complete graph K{n}: all {n} nodes should be reachable"
        assert len(result) == n, f"complete graph: no duplicates, got {len(result)} visits"
        assert result[0] == 0, f"complete graph: first visited should be start=0"

    def test_large_grid_graph(self):
        rows, cols = 20, 20
        adj = make_grid_graph(rows, cols)
        result = s.bfs(adj, 0)
        assert set(result) == set(range(rows * cols)), \
            f"20x20 grid bfs: should visit all {rows*cols} nodes"

    def test_multiple_start_nodes(self):
        adj = make_chain(10)
        for start in [0, 3, 7, 9]:
            result = s.bfs(adj, start)
            assert result[0] == start, \
                f"bfs from {start}: first node should be {start}, got {result[0]}"
            assert set(result) == set(range(10)), \
                f"bfs from {start}: should visit all 10 nodes in connected chain"


class TestBFSShortestDist:
    def test_direct_neighbors(self):
        edges = [(0, 1), (0, 2), (1, 3)]
        adj = make_graph(4, edges)
        dist = s.bfs_shortest_dist(adj, 0)
        assert dist[0] == 0, f"dist[0] should be 0 (start node), got {dist[0]}"
        assert dist[1] == 1, f"dist[1] should be 1 (direct neighbor), got {dist[1]}"
        assert dist[2] == 1, f"dist[2] should be 1 (direct neighbor), got {dist[2]}"
        assert dist[3] == 2, f"dist[3] should be 2 (neighbor's neighbor), got {dist[3]}"

    def test_shortest_path_used(self):
        adj = make_graph(3, [(0, 1), (1, 2), (0, 2)])
        dist = s.bfs_shortest_dist(adj, 0)
        assert dist[2] == 1, \
            f"dist[2]: direct edge 0→2 gives distance 1, but got {dist[2]} (did you use the longer path 0→1→2?)"

    def test_unreachable_not_in_dict(self):
        adj = make_graph(3, [(0, 1)])
        dist = s.bfs_shortest_dist(adj, 0)
        assert 2 not in dist, \
            f"node 2 is unreachable from 0, should be absent from dist, but got dist[2]={dist.get(2)}"

    def test_long_chain(self):
        edges = [(i, i + 1) for i in range(9)]
        adj = make_graph(10, edges)
        dist = s.bfs_shortest_dist(adj, 0)
        for i in range(10):
            assert dist[i] == i, \
                f"linear chain: dist[{i}] should be {i}, got {dist.get(i)}"

    def test_large_chain_distances(self):
        n = 500
        adj = make_chain(n)
        dist = s.bfs_shortest_dist(adj, 0)
        assert len(dist) == n, f"chain of {n}: dist should have {n} entries, got {len(dist)}"
        for i in range(n):
            assert dist[i] == i, \
                f"large chain: dist[{i}] should be {i}, got {dist.get(i)}"

    def test_large_chain_from_middle(self):
        n = 500
        mid = n // 2
        adj = make_chain(n)
        dist = s.bfs_shortest_dist(adj, mid)
        for i in range(n):
            assert dist[i] == abs(i - mid), \
                f"chain from middle ({mid}): dist[{i}] should be {abs(i-mid)}, got {dist.get(i)}"

    def test_large_complete_graph_all_distance_one(self):
        n = 100
        adj = make_complete(n)
        dist = s.bfs_shortest_dist(adj, 0)
        assert dist[0] == 0, f"start node distance should be 0"
        for i in range(1, n):
            assert dist[i] == 1, \
                f"complete graph: every non-start node should be distance 1, dist[{i}]={dist.get(i)}"

    def test_large_grid_distances(self):
        rows, cols = 10, 10
        adj = make_grid_graph(rows, cols)
        dist = s.bfs_shortest_dist(adj, 0)
        # node at (r,c) = index r*cols+c, manhattan distance from (0,0) = r+c
        for r in range(rows):
            for c in range(cols):
                node = r * cols + c
                expected = r + c
                assert dist[node] == expected, \
                    f"grid dist from (0,0) to ({r},{c}): expected {expected}, got {dist.get(node)}"


class TestDFS:
    def test_recursive_visits_all(self):
        edges = [(0, 1), (0, 2), (1, 3), (2, 4)]
        adj = make_graph(5, edges)
        result = set(s.dfs_recursive(adj, 0))
        assert result == {0, 1, 2, 3, 4}, \
            f"dfs_recursive({edges}): got {result}, want {{0,1,2,3,4}}"

    def test_iterative_visits_all(self):
        edges = [(0, 1), (0, 2), (1, 3), (2, 4)]
        adj = make_graph(5, edges)
        result = set(s.dfs_iterative(adj, 0))
        assert result == {0, 1, 2, 3, 4}, \
            f"dfs_iterative({edges}): got {result}, want {{0,1,2,3,4}}"

    def test_recursive_no_duplicates(self):
        edges = [(0, 1), (0, 2), (1, 2), (2, 3)]
        adj = make_graph(4, edges)
        result = s.dfs_recursive(adj, 0)
        dupes = [x for x in result if result.count(x) > 1]
        assert len(result) == len(set(result)), \
            f"dfs_recursive({edges}): node(s) visited more than once: {dupes}"

    def test_iterative_no_duplicates(self):
        edges = [(0, 1), (0, 2), (1, 2), (2, 3)]
        adj = make_graph(4, edges)
        result = s.dfs_iterative(adj, 0)
        dupes = [x for x in result if result.count(x) > 1]
        assert len(result) == len(set(result)), \
            f"dfs_iterative({edges}): node(s) visited more than once: {dupes}"

    def test_both_start_at_start(self):
        adj = make_graph(3, [(0, 1), (1, 2)])
        r = s.dfs_recursive(adj, 0)
        i = s.dfs_iterative(adj, 0)
        assert r[0] == 0, f"dfs_recursive: first node should be start=0, got {r[0]}"
        assert i[0] == 0, f"dfs_iterative: first node should be start=0, got {i[0]}"

    def test_single_node(self):
        adj = make_graph(1, [])
        assert s.dfs_recursive(adj, 0) == [0], \
            f"single node: dfs_recursive got {s.dfs_recursive(adj, 0)}, want [0]"
        assert s.dfs_iterative(adj, 0) == [0], \
            f"single node: dfs_iterative got {s.dfs_iterative(adj, 0)}, want [0]"

    def test_disconnected_only_reachable(self):
        adj = make_graph(4, [(0, 1)])
        r = set(s.dfs_recursive(adj, 0))
        i = set(s.dfs_iterative(adj, 0))
        assert r == {0, 1}, f"dfs_recursive disconnected: got {r}, want {{0,1}}"
        assert i == {0, 1}, f"dfs_iterative disconnected: got {i}, want {{0,1}}"

    def test_large_chain_visits_all(self):
        n = 200  # modest size to avoid recursion limit for recursive variant
        adj = make_chain(n)
        r = set(s.dfs_recursive(adj, 0))
        i = set(s.dfs_iterative(adj, 0))
        assert r == set(range(n)), \
            f"dfs_recursive large chain: visited {len(r)}/{n} nodes"
        assert i == set(range(n)), \
            f"dfs_iterative large chain: visited {len(i)}/{n} nodes"

    def test_large_complete_graph(self):
        n = 50
        adj = make_complete(n)
        r = set(s.dfs_recursive(adj, 0))
        i = set(s.dfs_iterative(adj, 0))
        assert r == set(range(n)), f"dfs_recursive complete K{n}: missed {set(range(n)) - r}"
        assert i == set(range(n)), f"dfs_iterative complete K{n}: missed {set(range(n)) - i}"

    def test_large_no_duplicates(self):
        n = 50
        adj = make_complete(n)
        r = s.dfs_recursive(adj, 0)
        i = s.dfs_iterative(adj, 0)
        assert len(r) == n, f"dfs_recursive: {n - len(r)} duplicate visits"
        assert len(i) == n, f"dfs_iterative: {n - len(i)} duplicate visits"

    def test_large_grid(self):
        rows, cols = 10, 10
        n = rows * cols
        adj = make_grid_graph(rows, cols)
        i = set(s.dfs_iterative(adj, 0))
        assert i == set(range(n)), \
            f"dfs_iterative 10x10 grid: visited {len(i)}/{n} nodes"


class TestNumIslands:
    def test_three_islands(self):
        grid = [list("11000"), list("11000"), list("00100"), list("00011")]
        result = s.num_islands(grid)
        assert result == 3, f"3-island grid: got {result}, want 3"

    def test_no_islands(self):
        grid = [list("000"), list("000")]
        result = s.num_islands(grid)
        assert result == 0, f"all water: got {result}, want 0"

    def test_all_land(self):
        grid = [list("111"), list("111")]
        result = s.num_islands(grid)
        assert result == 1, f"all land (one island): got {result}, want 1"

    def test_empty_grid(self):
        result = s.num_islands([])
        assert result == 0, f"empty grid: got {result}, want 0"

    def test_single_cell_land(self):
        result = s.num_islands([["1"]])
        assert result == 1, f"single land cell: got {result}, want 1"

    def test_single_cell_water(self):
        result = s.num_islands([["0"]])
        assert result == 0, f"single water cell: got {result}, want 0"

    def test_checkerboard(self):
        grid = [list("10101"), list("01010"), list("10101")]
        result = s.num_islands(grid)
        assert result == 8, \
            f"checkerboard (diagonal cells not connected, 4-directional only): got {result}, want 8"

    def test_single_row(self):
        grid = [list("10011")]
        result = s.num_islands(grid)
        assert result == 2, f"single row '10011': got {result}, want 2"

    def test_single_column(self):
        grid = [["1"], ["0"], ["1"], ["1"], ["0"]]
        result = s.num_islands(grid)
        assert result == 2, f"single column [1,0,1,1,0]: got {result}, want 2"

    def test_large_single_island(self):
        grid = [list("1" * 50) for _ in range(50)]
        result = s.num_islands(grid)
        assert result == 1, f"50x50 all-land grid: got {result}, want 1 (one giant island)"

    def test_large_all_water(self):
        grid = [list("0" * 50) for _ in range(50)]
        result = s.num_islands(grid)
        assert result == 0, f"50x50 all-water grid: got {result}, want 0"

    def test_large_checkerboard(self):
        n = 20
        grid = [[("1" if (r + c) % 2 == 0 else "0") for c in range(n)] for r in range(n)]
        result = s.num_islands(grid)
        expected = sum(1 for r in range(n) for c in range(n) if (r + c) % 2 == 0)
        assert result == expected, \
            f"20x20 checkerboard: got {result}, want {expected} isolated cells"

    def test_large_striped_rows(self):
        # alternating full rows of land and water — each land row is one island
        grid = []
        for r in range(20):
            grid.append(list("1" * 20 if r % 2 == 0 else "0" * 20))
        result = s.num_islands(grid)
        expected = 10  # rows 0,2,4,...,18
        assert result == expected, \
            f"20x20 striped rows: got {result}, want {expected} horizontal islands"

    def test_large_striped_columns(self):
        # alternating full columns of land and water
        grid = [[("1" if c % 2 == 0 else "0") for c in range(20)] for _ in range(20)]
        result = s.num_islands(grid)
        expected = 10  # columns 0,2,4,...,18
        assert result == expected, \
            f"20x20 striped columns: got {result}, want {expected} vertical islands"

    def test_large_spiral_is_one_island(self):
        # a large solid block with a hole — still one island
        n = 30
        grid = [list("1" * n) for _ in range(n)]
        # carve out interior
        for r in range(2, n - 2):
            for c in range(2, n - 2):
                grid[r][c] = "0"
        result = s.num_islands(grid)
        assert result == 1, \
            f"hollow square border ({n}x{n}): outer ring is one connected island, got {result}"


class TestTopoSort:
    def test_linear_chain(self):
        edges = [(0, 1), (1, 2)]
        order = s.topo_sort_kahn(3, edges)
        assert order is not None, f"linear chain {edges}: expected valid order, got None (cycle detected?)"
        assert order.index(0) < order.index(1) < order.index(2), \
            f"linear chain {edges}: got order {order}, need 0 before 1 before 2"

    def test_diamond(self):
        edges = [(0, 1), (0, 2), (1, 3), (2, 3)]
        order = s.topo_sort_kahn(4, edges)
        assert order is not None, f"diamond {edges}: expected valid order, got None"
        for u, v in edges:
            assert order.index(u) < order.index(v), \
                f"constraint {u}→{v} violated: {u} at pos {order.index(u)}, {v} at pos {order.index(v)} in {order}"

    def test_cycle_returns_none(self):
        edges = [(0, 1), (1, 0)]
        result = s.topo_sort_kahn(2, edges)
        assert result is None, f"cycle {edges}: expected None, got {result}"

    def test_self_loop_returns_none(self):
        result = s.topo_sort_kahn(1, [(0, 0)])
        assert result is None, f"self-loop: expected None, got {result}"

    def test_no_edges(self):
        order = s.topo_sort_kahn(3, [])
        assert order is not None, "no edges, 3 nodes: expected a valid order, got None"
        assert set(order) == {0, 1, 2}, f"no edges: got {order}, want all 3 nodes present"

    def test_single_node(self):
        result = s.topo_sort_kahn(1, [])
        assert result == [0], f"single node: got {result}, want [0]"

    def test_all_constraints_satisfied(self):
        edges = [(0, 2), (1, 2), (2, 3), (2, 4)]
        order = s.topo_sort_kahn(5, edges)
        assert order is not None, f"{edges}: expected valid order, got None"
        for u, v in edges:
            assert order.index(u) < order.index(v), \
                f"constraint {u}→{v} violated in order {order}"

    def test_larger_cycle(self):
        edges = [(0, 1), (1, 2), (2, 3), (3, 1)]
        result = s.topo_sort_kahn(4, edges)
        assert result is None, f"cycle 1→2→3→1: expected None, got {result}"

    def test_large_linear_chain(self):
        n = 500
        edges = [(i, i + 1) for i in range(n - 1)]
        order = s.topo_sort_kahn(n, edges)
        assert order is not None, f"large chain of {n}: expected valid order, got None"
        assert order == list(range(n)), \
            f"large linear chain: only valid order is [0,1,...,{n-1}], got {order[:5]}..."

    def test_large_all_constraints_satisfied(self):
        n = 200
        edges = [(i, i + 1) for i in range(n - 1)]
        # add some long-range edges
        edges += [(0, 50), (0, 100), (50, 150), (100, 199)]
        order = s.topo_sort_kahn(n, edges)
        assert order is not None, f"large DAG: expected valid order, got None"
        assert len(order) == n, f"large DAG: order should have {n} nodes, got {len(order)}"
        for u, v in edges:
            assert order.index(u) < order.index(v), \
                f"constraint {u}→{v} violated in order"

    def test_large_wide_dag(self):
        # one source (0), one sink (n-1), all others in between with no ordering between them
        n = 100
        edges = [(0, i) for i in range(1, n - 1)] + [(i, n - 1) for i in range(1, n - 1)]
        order = s.topo_sort_kahn(n, edges)
        assert order is not None, f"wide DAG: expected valid order, got None"
        assert order[0] == 0, f"wide DAG: source (0) must be first, got {order[0]}"
        assert order[-1] == n - 1, f"wide DAG: sink ({n-1}) must be last, got {order[-1]}"

    def test_large_cycle_detection(self):
        n = 500
        edges = [(i, i + 1) for i in range(n - 1)]
        edges.append((n - 1, 0))  # cycle back to start
        result = s.topo_sort_kahn(n, edges)
        assert result is None, \
            f"large cycle of {n} nodes: expected None, got order of length {len(result) if result else 0}"

    def test_large_partial_cycle(self):
        # 500 nodes, only nodes 400-499 form a cycle
        n = 500
        edges = [(i, i + 1) for i in range(399)]  # 0..399 chain, no cycle
        edges += [(i, i + 1) for i in range(400, 499)]
        edges.append((499, 400))  # cycle in 400..499
        result = s.topo_sort_kahn(n, edges)
        assert result is None, \
            f"partial cycle in large graph: expected None, got order of length {len(result) if result else 0}"


class TestDijkstra:
    def test_basic(self):
        adj = {0: [(1, 1), (2, 4)], 1: [(2, 2)], 2: []}
        dist = s.dijkstra(adj, 0, 3)
        assert dist[0] == 0, f"dist[0] should be 0 (start), got {dist[0]}"
        assert dist[1] == 1, f"dist[1]: direct edge weight=1, got {dist[1]}"
        assert dist[2] == 3, \
            f"dist[2]: 0→1→2 (cost 3) beats 0→2 (cost 4), got {dist[2]}"

    def test_direct_is_cheaper(self):
        adj = {0: [(1, 10), (2, 1)], 1: [(2, 1)], 2: []}
        dist = s.dijkstra(adj, 0, 3)
        assert dist[2] == 1, \
            f"dist[2]: direct edge 0→2 (cost 1) beats 0→1→2 (cost 11), got {dist[2]}"

    def test_unreachable_is_inf(self):
        adj = {0: [(1, 1)], 1: [], 2: []}
        dist = s.dijkstra(adj, 0, 3)
        assert dist[2] == float("inf"), \
            f"node 2 unreachable: expected inf, got {dist[2]}"

    def test_single_node(self):
        dist = s.dijkstra({0: []}, 0, 1)
        assert dist[0] == 0, f"single node: dist[0] should be 0, got {dist[0]}"

    def test_start_is_zero(self):
        adj = {0: [(1, 5)], 1: [(2, 3)], 2: []}
        dist = s.dijkstra(adj, 0, 3)
        assert dist[0] == 0, f"start node always has distance 0, got {dist[0]}"

    def test_chain(self):
        adj = {0: [(1, 1)], 1: [(2, 2)], 2: [(3, 3)], 3: []}
        dist = s.dijkstra(adj, 0, 4)
        assert dist[3] == 6, f"chain 0→1→2→3 (costs 1+2+3=6): got {dist[3]}"

    def test_all_weights_equal(self):
        adj = {0: [(1, 1), (2, 1)], 1: [(3, 1)], 2: [(3, 1)], 3: []}
        dist = s.dijkstra(adj, 0, 4)
        assert dist[3] == 2, \
            f"two equal-length paths to node 3 (each cost 2): got {dist[3]}"

    def test_large_chain(self):
        n = 500
        adj = {i: [(i + 1, 1)] for i in range(n - 1)}
        adj[n - 1] = []
        dist = s.dijkstra(adj, 0, n)
        for i in range(n):
            assert dist[i] == i, \
                f"large chain: dist[{i}] should be {i}, got {dist[i]}"

    def test_large_chain_weighted(self):
        n = 200
        adj = {i: [(i + 1, i + 1)] for i in range(n - 1)}
        adj[n - 1] = []
        dist = s.dijkstra(adj, 0, n)
        expected = 0
        for i in range(n):
            assert dist[i] == expected, \
                f"weighted chain: dist[{i}] should be {expected}, got {dist[i]}"
            expected += i + 1

    def test_large_shortcut(self):
        # long path 0→1→2→...→99 each weight 10, plus direct 0→99 weight 50
        n = 100
        adj = defaultdict(list)
        for i in range(n - 1):
            adj[i].append((i + 1, 10))
        adj[0].append((n - 1, 50))  # shortcut
        dist = s.dijkstra(adj, 0, n)
        assert dist[n - 1] == 50, \
            f"shortcut 0→{n-1} (cost 50) beats chain (cost {10*(n-1)}): got {dist[n-1]}"

    def test_large_all_unreachable_except_chain(self):
        # nodes 0..49 form a chain; nodes 50..99 are isolated
        n = 100
        adj = {i: [(i + 1, 1)] for i in range(49)}
        adj[49] = []
        for i in range(50, n):
            adj[i] = []
        dist = s.dijkstra(adj, 0, n)
        for i in range(50):
            assert dist[i] == i, f"reachable node {i}: expected {i}, got {dist[i]}"
        for i in range(50, n):
            assert dist[i] == float("inf"), \
                f"isolated node {i}: expected inf, got {dist[i]}"

    def test_must_process_min_cost_node_first(self):
        # exposes the idx=0 bug: after processing node 0, queue=[1(cost2), 2(cost1)]
        # correct: process node 2 first (cheaper), then relax 2→1 to get dist[1]=1.5
        # wrong (idx=0): process node 1 first, mark it visited at cost 2,
        #   then when node 2 is processed it can't update node 1 (already visited) → dist[1]=2
        adj = {0: [(1, 2), (2, 1)], 2: [(1, 0.5)], 1: []}
        dist = s.dijkstra(adj, 0, 3)
        assert dist[1] == 1.5, \
            f"dist[1]: 0→2→1 (cost 1.5) beats 0→1 (cost 2), got {dist[1]} — did you always process the minimum-cost node from the queue?"

    def test_large_dense_graph(self):
        # complete directed graph with weight = abs(u-v)
        n = 30
        adj = defaultdict(list)
        for u in range(n):
            for v in range(n):
                if u != v:
                    adj[u].append((v, abs(u - v)))
        dist = s.dijkstra(adj, 0, n)
        for i in range(n):
            assert dist[i] == i, \
                f"dense graph: shortest path 0→{i} should be {i} (direct edge), got {dist[i]}"
