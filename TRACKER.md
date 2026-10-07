# Spaced-Repetition Tracker

The drill loop: rewrite the item from a blank editor, run `pytest`, confirm green.
When solid, blank the function back to `raise _TODO` and schedule the next re-solve.

**Re-solve schedule:** first pass → +1 day → +1 week → +2 weeks. If you can produce
it cold at +2 weeks, it's yours. If you stumble at any checkpoint, reset to +1 day.

**Status key:** ⬜ not started · 🟡 learned, decaying · ✅ cold-recall solid

## Tier 1 — must never decay (weekly cold check)

| Item | File | Status | Last solved | Next due |
|---|---|---|---|---|
| binary_search | searching | ⬜ | | |
| bisect_left / bisect_right | searching | ⬜ | | |
| binary_search_on_answer | searching | ⬜ | | |
| merge (two sorted) | searching | ⬜ | | |
| quickselect | searching | ⬜ | | |
| bfs / bfs_shortest_dist | graphs | ⬜ | | |
| dfs_recursive / dfs_iterative | graphs | ⬜ | | |
| num_islands (grid traversal) | graphs | ⬜ | | |
| max_subarray_sum_fixed | patterns | ⬜ | | |
| longest_unique_substring | patterns | ⬜ | | |

## Tier 2 — build the structure from scratch

| Item | File | Status | Last solved | Next due |
|---|---|---|---|---|
| UnionFind | structures | ⬜ | | |
| MinHeap (sift up/down) | structures | ⬜ | | |
| Trie | structures | ⬜ | | |
| reverse_list | linkedlist_trees | ⬜ | | |
| has_cycle / middle_node | linkedlist_trees | ⬜ | | |
| merge_two_lists | linkedlist_trees | ⬜ | | |
| tree traversals (in/pre/post) | linkedlist_trees | ⬜ | | |
| level_order (tree BFS) | linkedlist_trees | ⬜ | | |
| max_depth | linkedlist_trees | ⬜ | | |

## Tier 3 — know the template, apply with a little thought

| Item | File | Status | Last solved | Next due |
|---|---|---|---|---|
| build_adjacency_list | graphs | ⬜ | | |
| topo_sort_kahn | graphs | ⬜ | | |
| dijkstra | graphs | ⬜ | | |
| subsets (backtracking skeleton) | patterns | ⬜ | | |
| permutations | patterns | ⬜ | | |
| climb_stairs (DP: Fibonacci shape) | patterns | ⬜ | | |
| coin_change (DP: unbounded) | patterns | ⬜ | | |
| longest_common_subsequence (2D DP) | patterns | ⬜ | | |
| knapsack_01 | patterns | ⬜ | | |
