from drills import solution as s


def ll(values: list[int]) -> s.ListNode | None:
    dummy = s.ListNode()
    cur = dummy
    for v in values:
        cur.next = s.ListNode(v)
        cur = cur.next
    return dummy.next


def to_list(head: s.ListNode | None) -> list[int]:
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


class TestReverseList:
    def test_basic(self):
        result = to_list(s.reverse_list(ll([1, 2, 3, 4])))
        assert result == [4, 3, 2, 1], \
            f"reverse_list([1,2,3,4]): got {result}, want [4,3,2,1]"

    def test_empty(self):
        result = to_list(s.reverse_list(None))
        assert result == [], f"reverse_list(None): got {result}, want []"

    def test_single(self):
        result = to_list(s.reverse_list(ll([1])))
        assert result == [1], f"reverse_list([1]): got {result}, want [1]"

    def test_two(self):
        result = to_list(s.reverse_list(ll([1, 2])))
        assert result == [2, 1], f"reverse_list([1,2]): got {result}, want [2,1]"

    def test_large(self):
        vals = list(range(1000))
        result = to_list(s.reverse_list(ll(vals)))
        expected = list(reversed(vals))
        assert result == expected, \
            f"reverse_list(range(1000)): first 5 got {result[:5]}, want {expected[:5]}"

    def test_very_large(self):
        vals = list(range(5000))
        result = to_list(s.reverse_list(ll(vals)))
        assert result == list(reversed(vals)), \
            f"reverse_list(range(5000)): first 5 got {result[:5]}"

    def test_does_not_modify_length(self):
        vals = list(range(100))
        length = len(to_list(s.reverse_list(ll(vals))))
        assert length == 100, f"reverse should preserve length, got {length}, want 100"

    def test_reverse_twice_is_identity(self):
        orig = list(range(500))
        result = to_list(s.reverse_list(s.reverse_list(ll(orig))))
        assert result == orig, \
            f"reversing twice should give original, first mismatch at {next((i for i,(a,b) in enumerate(zip(result,orig)) if a!=b), 'none')}"

    def test_all_same_values(self):
        vals = [7] * 100
        result = to_list(s.reverse_list(ll(vals)))
        assert result == vals, f"all same values: reverse of [7]*100 should still be [7]*100"

    def test_negatives(self):
        vals = [-3, -2, -1, 0, 1, 2, 3]
        result = to_list(s.reverse_list(ll(vals)))
        assert result == list(reversed(vals)), \
            f"reverse_list({vals}): got {result}, want {list(reversed(vals))}"

    def test_new_head_is_old_tail(self):
        vals = list(range(10))
        new_head = s.reverse_list(ll(vals))
        assert new_head.val == 9, \
            f"new head should be old tail (9), got {new_head.val}"

    def test_new_tail_is_old_head(self):
        vals = list(range(10))
        head = s.reverse_list(ll(vals))
        tail = head
        while tail.next:
            tail = tail.next
        assert tail.val == 0, \
            f"new tail should be old head (0), got {tail.val}"

    def test_no_cycle_after_reverse(self):
        vals = list(range(50))
        head = s.reverse_list(ll(vals))
        seen = set()
        cur = head
        while cur:
            assert id(cur) not in seen, "reverse_list created a cycle"
            seen.add(id(cur))
            cur = cur.next


class TestHasCycle:
    def test_no_cycle(self):
        assert not s.has_cycle(ll([1, 2, 3, 4])), \
            "has_cycle([1,2,3,4]): linear list has no cycle, should be False"

    def test_empty(self):
        assert not s.has_cycle(None), "has_cycle(None): empty list has no cycle"

    def test_single_no_cycle(self):
        assert not s.has_cycle(ll([1])), "has_cycle([1]): single node, no cycle"

    def test_tail_to_head(self):
        head = ll([1, 2, 3, 4])
        tail = head
        while tail.next:
            tail = tail.next
        tail.next = head
        assert s.has_cycle(head), \
            "has_cycle: tail points back to head, should detect cycle"

    def test_tail_to_middle(self):
        head = ll([1, 2, 3, 4])
        second = head.next
        tail = head
        while tail.next:
            tail = tail.next
        tail.next = second
        assert s.has_cycle(head), \
            "has_cycle: tail points to middle node, should detect cycle"

    def test_self_loop(self):
        node = s.ListNode(1)
        node.next = node
        assert s.has_cycle(node), "has_cycle: single node pointing to itself, should be True"

    def test_two_nodes_no_cycle(self):
        assert not s.has_cycle(ll([1, 2])), "has_cycle([1,2]): no cycle, should be False"

    def test_two_nodes_cycle(self):
        a = s.ListNode(1)
        b = s.ListNode(2)
        a.next = b
        b.next = a
        assert s.has_cycle(a), "has_cycle: 2-node cycle, should be True"

    def test_large_no_cycle(self):
        assert not s.has_cycle(ll(list(range(5000)))), \
            "has_cycle: 5000-node linear list has no cycle"

    def test_large_cycle_at_end(self):
        head = ll(list(range(1000)))
        # find node at index 500 and connect tail to it
        mid = head
        for _ in range(500):
            mid = mid.next
        tail = mid
        while tail.next:
            tail = tail.next
        tail.next = mid
        assert s.has_cycle(head), \
            "has_cycle: 1000-node list with cycle at index 500, should be True"

    def test_large_cycle_at_start(self):
        head = ll(list(range(2000)))
        tail = head
        while tail.next:
            tail = tail.next
        tail.next = head
        assert s.has_cycle(head), \
            "has_cycle: 2000-node list cycling back to head, should be True"

    def test_long_tail_short_cycle(self):
        # 900 linear nodes then a cycle of 100
        linear = ll(list(range(900)))
        cycle_start = s.ListNode(999)
        cur = linear
        while cur.next:
            cur = cur.next
        # attach cycle of 100 nodes
        cycle_head = cycle_start
        prev = cycle_start
        for i in range(99):
            node = s.ListNode(1000 + i)
            prev.next = node
            prev = node
        prev.next = cycle_head  # close the cycle
        cur.next = cycle_head
        assert s.has_cycle(linear), \
            "has_cycle: long tail with short cycle at end, should be True"


class TestMiddleNode:
    def test_odd_length(self):
        result = s.middle_node(ll([1, 2, 3])).val
        assert result == 2, f"middle_node([1,2,3]): got {result}, want 2"

    def test_even_length(self):
        result = s.middle_node(ll([1, 2, 3, 4])).val
        assert result == 3, \
            f"middle_node([1,2,3,4]): even length returns second middle, got {result}, want 3"

    def test_single(self):
        result = s.middle_node(ll([1])).val
        assert result == 1, f"middle_node([1]): got {result}, want 1"

    def test_two(self):
        result = s.middle_node(ll([1, 2])).val
        assert result == 2, \
            f"middle_node([1,2]): second middle of even-length list, got {result}, want 2"

    def test_five(self):
        result = s.middle_node(ll([1, 2, 3, 4, 5])).val
        assert result == 3, f"middle_node([1,2,3,4,5]): got {result}, want 3"

    def test_six(self):
        result = s.middle_node(ll([1, 2, 3, 4, 5, 6])).val
        assert result == 4, \
            f"middle_node([1,2,3,4,5,6]): second middle, got {result}, want 4"

    def test_large_odd(self):
        # 999 nodes: middle is index 499 (0-indexed), value 499
        vals = list(range(999))
        result = s.middle_node(ll(vals)).val
        assert result == 499, \
            f"middle_node(range(999)): middle of 999 nodes is index 499, got {result}"

    def test_large_even(self):
        # 1000 nodes: second middle is index 500, value 500
        vals = list(range(1000))
        result = s.middle_node(ll(vals)).val
        assert result == 500, \
            f"middle_node(range(1000)): second middle of 1000 nodes is index 500, got {result}"

    def test_middle_is_truly_middle(self):
        # verify the returned node has roughly equal tails on each side
        for n in [3, 5, 7, 11, 99, 101, 999]:
            vals = list(range(n))
            mid_node = s.middle_node(ll(vals))
            remaining = len(to_list(mid_node))
            expected_remaining = (n + 1) // 2  # ceil(n/2)
            assert remaining == expected_remaining, \
                f"middle_node(range({n})): remaining length should be {expected_remaining}, got {remaining}"

    def test_result_is_actual_node_not_copy(self):
        head = ll([1, 2, 3, 4, 5])
        mid = s.middle_node(head)
        assert mid.val == 3, f"middle_node: got {mid.val}, want 3"
        assert mid.next is not None, "middle_node: returned node should still have next pointer"
        assert mid.next.val == 4, \
            f"middle_node: next after middle should be 4, got {mid.next.val}"


class TestMergeTwoLists:
    def test_interleaved(self):
        result = to_list(s.merge_two_lists(ll([1, 3, 5]), ll([2, 4, 6])))
        assert result == [1, 2, 3, 4, 5, 6], \
            f"merge_two_lists([1,3,5], [2,4,6]): got {result}, want [1,2,3,4,5,6]"

    def test_left_empty(self):
        result = to_list(s.merge_two_lists(None, ll([1, 2])))
        assert result == [1, 2], f"merge_two_lists(None, [1,2]): got {result}, want [1,2]"

    def test_right_empty(self):
        result = to_list(s.merge_two_lists(ll([1, 2]), None))
        assert result == [1, 2], f"merge_two_lists([1,2], None): got {result}, want [1,2]"

    def test_both_empty(self):
        result = to_list(s.merge_two_lists(None, None))
        assert result == [], f"merge_two_lists(None, None): got {result}, want []"

    def test_all_left_smaller(self):
        result = to_list(s.merge_two_lists(ll([1, 2]), ll([3, 4])))
        assert result == [1, 2, 3, 4], \
            f"merge_two_lists([1,2], [3,4]): got {result}, want [1,2,3,4]"

    def test_all_right_smaller(self):
        result = to_list(s.merge_two_lists(ll([3, 4]), ll([1, 2])))
        assert result == [1, 2, 3, 4], \
            f"merge_two_lists([3,4], [1,2]): got {result}, want [1,2,3,4]"

    def test_duplicates(self):
        result = to_list(s.merge_two_lists(ll([1, 1, 3]), ll([1, 2])))
        assert result == [1, 1, 1, 2, 3], \
            f"merge_two_lists([1,1,3], [1,2]): got {result}, want [1,1,1,2,3]"

    def test_unequal_lengths(self):
        result = to_list(s.merge_two_lists(ll([1, 2]), ll([2, 3, 4, 5])))
        assert result == [1, 2, 2, 3, 4, 5], \
            f"merge_two_lists([1,2], [2,3,4,5]): got {result}"

    def test_single_each(self):
        result = to_list(s.merge_two_lists(ll([2]), ll([1])))
        assert result == [1, 2], f"merge_two_lists([2],[1]): got {result}, want [1,2]"

    def test_single_vs_many(self):
        result = to_list(s.merge_two_lists(ll([3]), ll([1, 2, 4, 5])))
        assert result == [1, 2, 3, 4, 5], \
            f"merge_two_lists([3], [1,2,4,5]): got {result}, want [1,2,3,4,5]"

    def test_result_is_sorted(self):
        import random
        rng = random.Random(42)
        a = sorted(rng.randint(0, 100) for _ in range(50))
        b = sorted(rng.randint(0, 100) for _ in range(50))
        result = to_list(s.merge_two_lists(ll(a), ll(b)))
        assert result == sorted(a + b), \
            f"merge result should be sorted, got unsorted result"

    def test_large(self):
        a = list(range(0, 2000, 2))
        b = list(range(1, 2000, 2))
        result = to_list(s.merge_two_lists(ll(a), ll(b)))
        expected = list(range(2000))
        assert result == expected, \
            f"merge even/odd lists: first mismatch at index {next((i for i,(x,y) in enumerate(zip(result,expected)) if x!=y), 'none')}"

    def test_large_all_same(self):
        a = [5] * 500
        b = [5] * 500
        result = to_list(s.merge_two_lists(ll(a), ll(b)))
        assert result == [5] * 1000, \
            f"merge [5]*500 and [5]*500: should be [5]*1000, got length {len(result)}"

    def test_no_cycle_after_merge(self):
        a = list(range(0, 100, 2))
        b = list(range(1, 100, 2))
        head = s.merge_two_lists(ll(a), ll(b))
        seen = set()
        cur = head
        while cur:
            assert id(cur) not in seen, "merge_two_lists created a cycle"
            seen.add(id(cur))
            cur = cur.next

    def test_original_nodes_used(self):
        # result should reuse original nodes, not create copies
        node_a = s.ListNode(1)
        node_b = s.ListNode(2)
        head = s.merge_two_lists(node_a, node_b)
        assert head is node_a or head is node_b, \
            "merge_two_lists should reuse original nodes, not create new ones"


class TestTreeTraversals:
    def root(self):
        #        1
        #       / \
        #      2   3
        #     / \
        #    4   5
        return s.TreeNode(1,
                          s.TreeNode(2, s.TreeNode(4), s.TreeNode(5)),
                          s.TreeNode(3))

    def test_inorder(self):
        result = s.inorder(self.root())
        assert result == [4, 2, 5, 1, 3], \
            f"inorder: got {result}, want [4,2,5,1,3] (left, node, right)"

    def test_preorder(self):
        result = s.preorder(self.root())
        assert result == [1, 2, 4, 5, 3], \
            f"preorder: got {result}, want [1,2,4,5,3] (node, left, right)"

    def test_postorder(self):
        result = s.postorder(self.root())
        assert result == [4, 5, 2, 3, 1], \
            f"postorder: got {result}, want [4,5,2,3,1] (left, right, node)"

    def test_empty(self):
        assert s.inorder(None) == [], "inorder(None): should return []"
        assert s.preorder(None) == [], "preorder(None): should return []"
        assert s.postorder(None) == [], "postorder(None): should return []"

    def test_single_node(self):
        node = s.TreeNode(7)
        assert s.inorder(node) == [7], f"inorder(7): got {s.inorder(node)}, want [7]"
        assert s.preorder(node) == [7], f"preorder(7): got {s.preorder(node)}, want [7]"
        assert s.postorder(node) == [7], f"postorder(7): got {s.postorder(node)}, want [7]"

    def test_inorder_bst_is_sorted(self):
        bst = s.TreeNode(4,
                         s.TreeNode(2, s.TreeNode(1), s.TreeNode(3)),
                         s.TreeNode(6, s.TreeNode(5), s.TreeNode(7)))
        result = s.inorder(bst)
        assert result == sorted(result), \
            f"inorder of BST should be sorted, got {result}"

    def test_right_skewed(self):
        root = s.TreeNode(1, None, s.TreeNode(2, None, s.TreeNode(3)))
        assert s.inorder(root) == [1, 2, 3], \
            f"right-skewed inorder: got {s.inorder(root)}, want [1,2,3]"
        assert s.preorder(root) == [1, 2, 3], \
            f"right-skewed preorder: got {s.preorder(root)}, want [1,2,3]"
        assert s.postorder(root) == [3, 2, 1], \
            f"right-skewed postorder: got {s.postorder(root)}, want [3,2,1]"

    def test_left_skewed(self):
        root = s.TreeNode(3, s.TreeNode(2, s.TreeNode(1), None), None)
        assert s.inorder(root) == [1, 2, 3], \
            f"left-skewed inorder: got {s.inorder(root)}, want [1,2,3]"
        assert s.preorder(root) == [3, 2, 1], \
            f"left-skewed preorder: got {s.preorder(root)}, want [3,2,1]"
        assert s.postorder(root) == [1, 2, 3], \
            f"left-skewed postorder: got {s.postorder(root)}, want [1,2,3]"

    def test_large_complete_tree(self):
        # build a complete binary tree of depth 10 (~1023 nodes)
        def build(depth):
            if depth == 0:
                return None
            return s.TreeNode(depth, build(depth - 1), build(depth - 1))
        root = build(10)
        inorder_result = s.inorder(root)
        preorder_result = s.preorder(root)
        postorder_result = s.postorder(root)
        n = len(inorder_result)
        assert n == len(preorder_result) == len(postorder_result), \
            "all traversals should visit the same number of nodes"
        # inorder and preorder should be permutations of each other
        assert sorted(inorder_result) == sorted(preorder_result), \
            "inorder and preorder should contain the same values"

    def test_large_bst_inorder_sorted(self):
        # BST: insert 1..100 in a balanced way
        def build_bst(lo, hi):
            if lo > hi:
                return None
            mid = (lo + hi) // 2
            return s.TreeNode(mid, build_bst(lo, mid - 1), build_bst(mid + 1, hi))
        root = build_bst(1, 127)
        result = s.inorder(root)
        assert result == sorted(result), "inorder of BST must be sorted"
        assert len(result) == 127, f"BST(1..127): inorder should have 127 nodes, got {len(result)}"

    def test_traversal_count_equals_nodes(self):
        # every traversal should visit every node exactly once
        def build(val, depth):
            if depth == 0:
                return s.TreeNode(val)
            return s.TreeNode(val, build(val * 2, depth - 1), build(val * 2 + 1, depth - 1))
        root = build(1, 7)  # 255 nodes
        for name, fn in [("inorder", s.inorder), ("preorder", s.preorder), ("postorder", s.postorder)]:
            result = fn(root)
            assert len(result) == 255, \
                f"{name} on 255-node tree: got {len(result)} nodes, want 255"
            assert len(set(result)) == 255, \
                f"{name}: should visit each node exactly once, found duplicates"


class TestLevelOrder:
    def test_basic(self):
        root = s.TreeNode(1, s.TreeNode(2, s.TreeNode(4), s.TreeNode(5)), s.TreeNode(3))
        result = s.level_order(root)
        assert result == [[1], [2, 3], [4, 5]], \
            f"level_order: got {result}, want [[1],[2,3],[4,5]]"

    def test_empty(self):
        assert s.level_order(None) == [], "level_order(None): should return []"

    def test_single(self):
        result = s.level_order(s.TreeNode(1))
        assert result == [[1]], f"level_order(single): got {result}, want [[1]]"

    def test_right_skewed(self):
        root = s.TreeNode(1, None, s.TreeNode(2, None, s.TreeNode(3)))
        result = s.level_order(root)
        assert result == [[1], [2], [3]], \
            f"right-skewed level_order: got {result}, want [[1],[2],[3]]"

    def test_complete_tree(self):
        root = s.TreeNode(1,
                          s.TreeNode(2, s.TreeNode(4), s.TreeNode(5)),
                          s.TreeNode(3, s.TreeNode(6), s.TreeNode(7)))
        result = s.level_order(root)
        assert result == [[1], [2, 3], [4, 5, 6, 7]], \
            f"complete tree level_order: got {result}, want [[1],[2,3],[4,5,6,7]]"

    def test_level_sizes(self):
        root = s.TreeNode(1, s.TreeNode(2, s.TreeNode(4), s.TreeNode(5)), s.TreeNode(3))
        sizes = [len(l) for l in s.level_order(root)]
        assert sizes == [1, 2, 2], \
            f"level sizes should be [1,2,2], got {sizes}"

    def test_left_skewed(self):
        root = s.TreeNode(1, s.TreeNode(2, s.TreeNode(3, s.TreeNode(4), None), None), None)
        result = s.level_order(root)
        assert result == [[1], [2], [3], [4]], \
            f"left-skewed level_order: got {result}, want [[1],[2],[3],[4]]"

    def test_unbalanced(self):
        root = s.TreeNode(1,
                          s.TreeNode(2, s.TreeNode(4, s.TreeNode(8), None), s.TreeNode(5)),
                          s.TreeNode(3, None, s.TreeNode(7)))
        result = s.level_order(root)
        assert result[0] == [1], f"level 0: got {result[0]}, want [1]"
        assert set(result[1]) == {2, 3}, f"level 1: got {result[1]}, want [2,3]"
        assert set(result[2]) == {4, 5, 7}, f"level 2: got {result[2]}, want {{4,5,7}}"
        assert result[3] == [8], f"level 3: got {result[3]}, want [8]"

    def test_large_complete_tree_level_sizes(self):
        # depth-7 complete tree: levels have 1,2,4,8,...,64 nodes
        def build(depth):
            if depth < 0:
                return None
            return s.TreeNode(depth, build(depth - 1), build(depth - 1))
        root = build(6)
        levels = s.level_order(root)
        assert len(levels) == 7, f"depth-7 tree should have 7 levels, got {len(levels)}"
        for i, level in enumerate(levels):
            expected = 2 ** i
            assert len(level) == expected, \
                f"level {i}: expected {expected} nodes, got {len(level)}"

    def test_large_total_nodes(self):
        def build(depth):
            if depth < 0:
                return None
            return s.TreeNode(depth, build(depth - 1), build(depth - 1))
        root = build(9)  # 1023 nodes
        levels = s.level_order(root)
        total = sum(len(l) for l in levels)
        assert total == 1023, f"depth-10 complete tree: expected 1023 nodes total, got {total}"

    def test_each_level_is_left_to_right(self):
        # verify BFS visits left child before right child within each level
        root = s.TreeNode(0,
                          s.TreeNode(1, s.TreeNode(3), s.TreeNode(4)),
                          s.TreeNode(2, s.TreeNode(5), s.TreeNode(6)))
        levels = s.level_order(root)
        assert levels[1] == [1, 2], f"level 1 must be left-to-right: got {levels[1]}, want [1,2]"
        assert levels[2] == [3, 4, 5, 6], \
            f"level 2 must be left-to-right: got {levels[2]}, want [3,4,5,6]"


class TestMaxDepth:
    def test_basic(self):
        root = s.TreeNode(1, s.TreeNode(2, s.TreeNode(4), s.TreeNode(5)), s.TreeNode(3))
        result = s.max_depth(root)
        assert result == 3, f"max_depth of 3-level tree: got {result}, want 3"

    def test_empty(self):
        result = s.max_depth(None)
        assert result == 0, f"max_depth(None): got {result}, want 0"

    def test_single(self):
        result = s.max_depth(s.TreeNode(1))
        assert result == 1, f"max_depth(single node): got {result}, want 1"

    def test_left_skewed(self):
        root = s.TreeNode(1, s.TreeNode(2, s.TreeNode(3, s.TreeNode(4), None), None), None)
        result = s.max_depth(root)
        assert result == 4, f"left-skewed 4-level tree: got {result}, want 4"

    def test_right_skewed(self):
        root = s.TreeNode(1, None, s.TreeNode(2, None, s.TreeNode(3)))
        result = s.max_depth(root)
        assert result == 3, f"right-skewed 3-level tree: got {result}, want 3"

    def test_unbalanced(self):
        root = s.TreeNode(1,
                          s.TreeNode(2, s.TreeNode(3, s.TreeNode(4), None), None),
                          s.TreeNode(5))
        result = s.max_depth(root)
        assert result == 4, \
            f"unbalanced (left depth 4, right depth 2): got {result}, want 4"

    def test_depth_is_max_not_min(self):
        # one branch depth 10, other depth 1 — must return 10 not 1
        deep = s.TreeNode(0)
        cur = deep
        for i in range(1, 10):
            cur.left = s.TreeNode(i)
            cur = cur.left
        root = s.TreeNode(99, deep, s.TreeNode(100))
        result = s.max_depth(root)
        assert result == 11, \
            f"max_depth should return deepest branch (11), got {result}"

    def test_large_balanced(self):
        def build(depth):
            if depth == 0:
                return None
            return s.TreeNode(depth, build(depth - 1), build(depth - 1))
        root = build(12)
        result = s.max_depth(root)
        assert result == 12, f"balanced tree of depth 12: got {result}, want 12"

    def test_large_right_skewed(self):
        # chain of 500 nodes going right
        root = s.TreeNode(0)
        cur = root
        for i in range(1, 500):
            cur.right = s.TreeNode(i)
            cur = cur.right
        result = s.max_depth(root)
        assert result == 500, f"right-skewed chain of 500: got {result}, want 500"

    def test_depth_one_more_than_children(self):
        # max_depth(root) == 1 + max(max_depth(left), max_depth(right))
        for depth in [1, 2, 3, 5, 8, 10]:
            def build(d):
                if d == 0:
                    return None
                return s.TreeNode(d, build(d - 1), build(d - 1))
            root = build(depth)
            result = s.max_depth(root)
            assert result == depth, \
                f"balanced tree of depth {depth}: got {result}, want {depth}"
