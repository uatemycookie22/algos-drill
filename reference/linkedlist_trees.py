"""Linked lists & binary trees — Tier 2."""
from collections import deque


class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None) -> None:
        self.val = val
        self.next = next


def to_linked(values: list[int]) -> ListNode | None:
    dummy = ListNode()
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def to_list(head: ListNode | None) -> list[int]:
    out: list[int] = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def reverse_list(head: ListNode | None) -> ListNode | None:
    prev: ListNode | None = None
    cur = head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev


def has_cycle(head: ListNode | None) -> bool:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next  # type: ignore[assignment]
        fast = fast.next.next
        if slow is fast:
            return True
    return False


def middle_node(head: ListNode) -> ListNode:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next  # type: ignore[assignment]
        fast = fast.next.next
    return slow


def merge_two_lists(a: ListNode | None, b: ListNode | None) -> ListNode | None:
    dummy = ListNode()
    tail = dummy
    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next


class TreeNode:
    def __init__(self, val: int = 0, left: "TreeNode | None" = None, right: "TreeNode | None" = None) -> None:
        self.val = val
        self.left = left
        self.right = right


def inorder(root: TreeNode | None) -> list[int]:
    out: list[int] = []

    def walk(node: TreeNode | None) -> None:
        if not node:
            return
        walk(node.left)
        out.append(node.val)
        walk(node.right)

    walk(root)
    return out


def preorder(root: TreeNode | None) -> list[int]:
    out: list[int] = []

    def walk(node: TreeNode | None) -> None:
        if not node:
            return
        out.append(node.val)
        walk(node.left)
        walk(node.right)

    walk(root)
    return out


def postorder(root: TreeNode | None) -> list[int]:
    out: list[int] = []

    def walk(node: TreeNode | None) -> None:
        if not node:
            return
        walk(node.left)
        walk(node.right)
        out.append(node.val)

    walk(root)
    return out


def level_order(root: TreeNode | None) -> list[list[int]]:
    if not root:
        return []
    out: list[list[int]] = []
    queue: deque[TreeNode] = deque([root])
    while queue:
        level: list[int] = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        out.append(level)
    return out


def max_depth(root: TreeNode | None) -> int:
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
