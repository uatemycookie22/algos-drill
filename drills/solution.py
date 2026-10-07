"""YOUR BLANK EDITOR. Rewrite each function from memory — no peeking.

Run `pytest` to check yourself. Everything starts red (NotImplementedError).
Peek at reference/ ONLY after you've struggled. Struggle first, then confirm.
"""
from __future__ import annotations
from collections import deque, defaultdict
from collections.abc import Callable
import heapq

_TODO = NotImplementedError("drill me: rewrite from memory")

type Graph = dict[int, list[int]]
type WeightedGraph = dict[int, list[tuple[int, int]]]


# ============================ searching.py ============================

def binary_search(nums: list[int], target: int) -> int:
    """Return the index of target in sorted nums, or -1 if not found.

    Input:  nums=[1,3,5,7,9], target=5  →  2
    Input:  nums=[1,3,5,7,9], target=4  →  -1
    Input:  nums=[],           target=1  →  -1

    Constraints: nums is sorted ascending.
    Edge cases:  empty list, target below min, target above max, single element.
    """

    raise _TODO


def bisect_left(nums: list[int], target: int) -> int:
    """Return the leftmost index where target can be inserted to keep nums sorted.

    Input:  nums=[1,2,2,2,3], target=2  →  1
    Input:  nums=[1,2,3],     target=0  →  0
    Input:  nums=[1,2,3],     target=4  →  3
    Input:  nums=[],          target=5  →  0

    Edge cases: empty list, target smaller than all, target larger than all, all duplicates.
    """
    # [L, R)
    raise _TODO

        
        


def bisect_right(nums: list[int], target: int) -> int:
    """Return the rightmost insertion point: first index where nums[i] > target.

    Input:  nums=[1,2,2,2,3], target=2  →  4
                  L   M     R
    Input:  nums=[1,2,3],     target=3  →  3
                           
    Input:  nums=[3,3,3,3],   target=3  →  4
    """
    raise _TODO


def binary_search_on_answer(lo: int, hi: int, feasible: Callable[[int], bool]) -> int:
    """Return the smallest integer x in [lo, hi] where feasible(x) is True.

    Requires: feasible is monotonic — False for small x, True once a threshold is crossed.

    Input:  lo=0, hi=100, feasible=lambda x: x*x>=81  →  9
    Input:  lo=0, hi=10,  feasible=lambda x: x>=0     →  0

    Common uses: minimum capacity to ship packages, minimum eating speed, smallest divisor.

    arr = [F,F,F,T,T,T,T,T,T,T]
    Goal: Find leftmost index i where arr[i] is True

    """
    raise _TODO
            



def merge(a: list[int], b: list[int]) -> list[int]:
    """Merge two sorted lists into one sorted list.

    Input:  a=[1,3,5], b=[2,4,6]  →  [1,2,3,4,5,6]
    Input:  a=[],      b=[1,2]    →  [1,2]
    Input:  a=[1,1,3], b=[1,2]    →  [1,1,1,2,3]

    Edge cases: either list empty.
    """
    raise _TODO
    





def quickselect(nums: list[int], k: int) -> int | None:
    """Return the k-th smallest element (1-indexed) in O(n) average time.

    Input:  nums=[3,1,2,5,4], k=1  →  1
    Input:  nums=[3,1,2,5,4], k=3  →  3
    Input:  nums=[3,1,2,5,4], k=5  →  5

    Constraints: 1 <= k <= len(nums).
    """
    raise _TODO


# ============================ graphs.py ============================

def build_adjacency_list(n: int, edges: list[tuple[int, int]], directed: bool = False) -> Graph:
    """Build an adjacency list from an edge list. Nodes are labeled 0..n-1.

    Input:  n=3, edges=[(0,1),(1,2)], directed=False  →  {0:[1], 1:[0,2], 2:[1]}
    Input:  n=3, edges=[(0,1),(1,2)], directed=True   →  {0:[1], 1:[2]}
    """
    raise _TODO


def bfs(adj: Graph, start: int) -> list[int]:
    """Breadth-first traversal. Return nodes in visit order.

    Input:  adj={0:[1,2], 1:[3], 2:[3], 3:[]}, start=0  →  [0,1,2,3]

    Edge cases: single node with no edges, disconnected graph (only reachable nodes returned).
    """
    
    raise _TODO




def bfs_shortest_dist(adj: Graph, start: int) -> dict[int, int]:
    """Return the shortest distance (number of edges) from start to every reachable node.

    Input:  adj={0:[1,2], 1:[3], 2:[3], 3:[]}, start=0  →  {0:0, 1:1, 2:1, 3:2}

    Edge cases: unreachable nodes are absent from the returned dict.
    """
    raise _TODO

    
    


def dfs_recursive(adj: Graph, start: int, visited: set[int] | None = None, order: list[int] | None = None) -> list[int]:
    """Depth-first traversal, recursive. Return nodes in visit order.

    Input:  adj={0:[1,2], 1:[3], 2:[], 3:[]}, start=0  →  [0,1,3,2]

    Edge cases: single node, disconnected graph.
    """
    raise _TODO



def dfs_iterative(adj: Graph, start: int) -> list[int]:
    """Depth-first traversal, explicit stack. Return nodes in visit order.

    Same result as dfs_recursive.
    """
    raise _TODO
    



def num_islands(grid: list[list[str]]) -> int:
    """Count connected regions of '1's in a grid (4-directional connectivity).

    Input:  [["1","1","0"],
             ["0","0","1"]]  →  2

    Constraints: grid[r][c] is '0' or '1'.
    Edge cases:  empty grid → 0, all water → 0, all land → 1.
    """
    raise _TODO



def topo_sort_kahn(n: int, edges: list[tuple[int, int]]) -> list[int] | None:
    """Topological sort. Return a valid ordering, or None if a cycle exists.

    Edge (u, v) means u must come before v.

    Input:  n=4, edges=[(0,1),(0,2),(1,3),(2,3)]  →  [0,1,2,3] or [0,2,1,3]
    Input:  n=2, edges=[(0,1),(1,0)]              →  None
    """
    # Build adj
    raise _TODO

import math
def dijkstra(adj: WeightedGraph, start: int, n: int) -> list[float]:
    """Shortest paths from start to all nodes. adj[u] = [(v, weight), ...].

    Input:  adj={0:[(1,1),(2,4)], 1:[(2,2)], 2:[]}, start=0, n=3
    Output: [0, 1, 3]

    Constraints: all weights are non-negative.
    Edge cases:  unreachable nodes have distance inf.
    """
    raise _TODO


    


# ============================ structures.py ============================

class UnionFind:
    """Disjoint Set Union. Tracks connected components.

    Example:
        uf = UnionFind(5)
        uf.union(0,1); uf.union(1,2)
        uf.connected(0,2)  →  True
        uf.connected(0,3)  →  False
        uf.count           →  3
    """

    def __init__(self, n: int) -> None:
        raise _TODO

    def find(self, x: int) -> int:
        # Path compression
        raise _TODO

    def union(self, a: int, b: int) -> bool:
        """Connect a and b. Returns True if they were previously disconnected."""
        raise _TODO
        

    def connected(self, a: int, b: int) -> bool:
        raise _TODO


class MinHeap:
    """Binary min-heap. push and pop are O(log n).

    Example:
        h = MinHeap()
        h.push(3); h.push(1); h.push(2)
        h.pop()  →  1
        h.pop()  →  2
    """

    def __init__(self) -> None:
        raise _TODO


    def push(self, val: int) -> None:
        raise _TODO

        

    def pop(self) -> int:
        """Remove and return the minimum. Raises IndexError if empty."""
        raise _TODO

    def peek(self) -> int:
        raise _TODO

    def __len__(self) -> int:
        raise _TODO


class TrieNode:
    """One node in a Trie: a children dict and an is_word flag."""

    def __init__(self) -> None:
        raise _TODO



class Trie:
    """Prefix tree. Insert and search in O(len(word)) time.

    Example:
        t = Trie()
        t.insert("apple")
        t.search("apple")     →  True
        t.search("app")       →  False
        t.starts_with("app")  →  True

    Edge cases: inserting then searching the empty string.
    """

    def __init__(self) -> None:
        raise _TODO

    def insert(self, word: str) -> None:
        raise _TODO

            

    def search(self, word: str) -> bool:
        raise _TODO

    def starts_with(self, prefix: str) -> bool:
        raise _TODO


# ======================= linkedlist_trees.py =======================

class ListNode:
    def __init__(self, val: int = 0, next: ListNode | None = None) -> None:
        raise _TODO


class TreeNode:
    def __init__(self, val: int = 0, left: TreeNode | None = None, right: TreeNode | None = None) -> None:
        raise _TODO


def reverse_list(head: ListNode | None) -> ListNode | None:
    """Reverse a singly linked list in-place. Return the new head.

    Input:  1->2->3->4->None  →  4->3->2->1->None
    Input:  None              →  None
    Input:  1->None           →  1->None
    """
    # 0->1->2->3->4
    # 0<-1->2->3->4
    # 0<-1<-2->3->4
    # 0<-1<-2<-3->4
    # 0<-1<-2<-3<-4

    raise _TODO
        



def has_cycle(head: ListNode | None) -> bool:
    """Return True if the linked list contains a cycle.

    Input:  1->2->3->2 (cycle)  →  True
    Input:  1->2->3->None       →  False
    Input:  None                →  False
    """
    raise _TODO


def middle_node(head: ListNode) -> ListNode:
    """Return the middle node. For even length, return the second middle.

    Input:  1->2->3        →  node(2)
    Input:  1->2->3->4     →  node(3)
    Input:  1->2->3->4->5->6->7  →  node(3)
    """
    
    raise _TODO


def merge_two_lists(a: ListNode | None, b: ListNode | None) -> ListNode | None:
    """Merge two sorted linked lists into one sorted list.

    Input:  1->3->5,  2->4->6   →  1->2->3->4->5->6
    Input:  None,     1->2->3   →  1->2->3

    Edge cases: either list is None.
    """

    raise _TODO


def inorder(root: TreeNode | None) -> list[int]:
    """In-order traversal: left, node, right.

    Input:      1              →  [4, 2, 5, 1, 3]
               / \\
              2   3
             / \\
            4   5

    Edge cases: empty tree → [].
    """
    raise _TODO


def preorder(root: TreeNode | None) -> list[int]:
    """Pre-order traversal: node, left, right.

    Input:      1              →  [1, 2, 4, 5, 3]
               / \\
              2   3
             / \\
            4   5

    Input: same tree  →  [1, 2, 4, 5, 3]
    Edge cases: empty tree → [].
    """
    raise _TODO


def postorder(root: TreeNode | None) -> list[int]:
    """Post-order traversal: left, right, node.

    Input: same tree  →  [4, 5, 2, 3, 1]
    Edge cases: empty tree → [].
    """
    raise _TODO


def level_order(root: TreeNode | None) -> list[list[int]]:
    """Level-order BFS. Return a list of levels.

    Input:      1              →  [[1], [2,3], [4,5]]
               / \\
              2   3
             / \\
            4   5

    Edge cases: empty tree → [].
    """
    raise _TODO



def max_depth(root: TreeNode | None) -> int:
    """Return the number of nodes along the longest root-to-leaf path.

    Input:  1->2->4 (left spine)  →  3
    Input:  None                  →  0
    Input:  single node           →  1
    """
    raise _TODO


# ============================ patterns.py ============================

def two_sum(nums: list[int], target: int) -> list[int] | None:
    """Return [i, j] where nums[i] + nums[j] == target, or None.

    Input:  nums=[2,7,11,15], target=9   →  [0,1]
    Input:  nums=[3,2,4],     target=6   →  [1,2]
    Input:  nums=[1,2,3],     target=10  →  None

    Constraints: each input has at most one solution, cannot use same index twice.
    """
    raise _TODO


def is_palindrome(s: str) -> bool:
    """Return True if s reads the same forwards and backwards.

    Input:  "racecar"  →  True
    Input:  "hello"    →  False
    Input:  ""         →  True
    """
    raise _TODO


def max_subarray_sum_fixed(nums: list[int], k: int) -> int | None:
    """Return the maximum sum of any contiguous subarray of length k.

    Input:  nums=[2,1,5,1,3,2], k=3  →  9
    Input:  nums=[1,2,3,4,5],   k=2  →  9
    Input:  nums=[1,2],         k=5  →  None

    Edge cases: k > len(nums) → None.
    """
    raise _TODO


def longest_unique_substring(s: str) -> int:
    """Return the length of the longest substring with no repeated characters.

    Input:  "abcabcbb"  →  3
    Input:  "bbbbb"     →  1
    Input:  ""          →  0
    Input:  "pwwkew"    →  3
    """
    raise _TODO


def subsets(nums: list[int]) -> list[list[int]]:
    """Return all subsets of nums (the power set).

    Input:  [1,2,3]  →  [[], [1], [2], [3], [1,2], [1,3], [2,3], [1,2,3]]

    Constraints: all elements are unique. Result has 2^n subsets.
    """
    raise _TODO


def permutations(nums: list[int]) -> list[list[int]]:
    """Return all permutations of nums.

    Input:  [1,2,3]  →  [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

    Constraints: all elements are unique. Result has n! permutations.
    """
    raise _TODO


def climb_stairs(n: int) -> int:
    """Return the number of ways to climb n stairs, taking 1 or 2 steps at a time.

    Input:  1  →  1
    Input:  2  →  2
    Input:  3  →  3
    Input:  5  →  8
    """
    raise _TODO


def coin_change(coins: list[int], amount: int) -> int:
    """Return the fewest coins needed to make amount, or -1 if impossible.

    Input:  coins=[1,2,5], amount=11  →  3
    Input:  coins=[2],     amount=3   →  -1
    Input:  coins=[1],     amount=0   →  0

    Constraints: coins can be reused any number of times.
    """
    raise _TODO


def longest_common_subsequence(a: str, b: str) -> int:
    """Return the length of the longest common subsequence of a and b.

    Input:  a="abcde",  b="ace"    →  3
    Input:  a="abc",    b="abc"    →  3
    Input:  a="abc",    b="def"    →  0
    Input:  a="AGGTAB", b="GXTXAYB" →  4

    Edge cases: either string empty → 0.
    """
    raise _TODO


def knapsack_01(weights: list[int], values: list[int], capacity: int) -> int:
    """Return the maximum value achievable without exceeding capacity. Each item used at most once.

    Input:  weights=[1,2,3], values=[10,15,40], capacity=6  →  65
    Input:  weights=[5],     values=[10],       capacity=3  →  0

    Edge cases: capacity=0 → 0, no item fits → 0.
    """
    raise _TODO
