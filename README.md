# algos-drill

Cold-recall practice for core algorithms & data structures. The goal isn't to
*solve problems* — it's to be able to write each fundamental **from a blank
editor, correct on the first try, in a few minutes**, the way you can multiply
in your head.

## Quick start

```bash
git clone https://github.com/uatemycookie22/algos-drill.git
cd algos-drill

python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
python -m pip install -r requirements-dev.txt
python -m pytest
```

The repository intentionally starts with a blank `drills/solution.py`. The
`reference/` directory contains the answer key, and the tests are designed to
tell you exactly what is missing after each cold-recall attempt.

## The loop

1. Open `drills/solution.py` — your blank editor. Every function starts as
   `raise _TODO`.
2. Pick an item. Rewrite it **from memory**. No peeking.
3. Run the tests:
   ```
   cd algos-drill && python3 -m pytest
   ```
   Green = it's correct. Red = the traceback tells you exactly what's off.
4. Struggled? *Now* open `reference/` and compare. Understand the gap, then
   blank your function back to `raise _TODO` and do it again.
5. Log it in `TRACKER.md` and schedule the next re-solve (+1d → +1wk → +2wk).

## Run a subset

```
python3 -m pytest drills/test_graphs.py              # one topic
python3 -m pytest drills/test_graphs.py::test_bfs_visits_all   # one item
python3 -m pytest -k "binary_search or dijkstra"     # by name
```

## Layout

```
reference/   canonical, commented implementations — the "answer key"
  searching.py          binary search (+ variants), merge, quickselect
  graphs.py             adj list, BFS, DFS, num_islands, topo sort, dijkstra
  structures.py         UnionFind, MinHeap, Trie, heapq idioms
  linkedlist_trees.py   list ops, tree traversals, level-order
  patterns.py           two pointers, sliding window, backtracking, DP
drills/
  solution.py           YOUR blank editor — rewrite here
  test_*.py             pytest checks (same tests pass against reference/)
TRACKER.md              spaced-repetition schedule, seeded by tier
```

## Weekly cold check

Once a week, blank all of **Tier 1 + Tier 2** in `TRACKER.md` and re-solve from
scratch. Anything slow or shaky is your signal for what to drill that week —
those are the foundations everything else is built on (Dijkstra = BFS + heap,
backtracking = DFS + undo), so they must never decay.

## Note on signatures

The tests import from `drills.solution` and expect the reference signatures
exactly. Keep the names/parameters as given; rewrite only the *bodies*.

## Resetting a drill

To archive the current local attempt, blank implemented functions, and clear
local progress:

```bash
python3 reset.py
```

Personal archives and progress are ignored by Git and are not published.

## Interactive lessons

The browser-based learning lab currently includes an interactive Quickselect
lesson and is structured to grow with the rest of the curriculum.

```bash
open learning/index.html
```

Or run `python3 -m http.server 8000 --directory learning` and open
`http://localhost:8000`. The site has no frontend dependencies or build step.
