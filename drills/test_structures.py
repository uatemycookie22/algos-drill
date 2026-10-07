import random
from drills import solution as s


class TestUnionFind:
    def test_initially_disconnected(self):
        uf = s.UnionFind(5)
        for i in range(5):
            for j in range(5):
                if i != j:
                    assert not uf.connected(i, j), \
                        f"UnionFind(5): nodes {i} and {j} should start disconnected"

    def test_union_connects(self):
        uf = s.UnionFind(5)
        uf.union(0, 1)
        assert uf.connected(0, 1), "after union(0,1): nodes 0 and 1 should be connected"

    def test_transitivity(self):
        uf = s.UnionFind(5)
        uf.union(0, 1)
        uf.union(1, 2)
        assert uf.connected(0, 2), \
            "after union(0,1) and union(1,2): 0 and 2 should be connected transitively"

    def test_count_decrements(self):
        uf = s.UnionFind(5)
        assert uf.count == 5, f"initial count should be 5, got {uf.count}"
        uf.union(0, 1)
        assert uf.count == 4, f"after union(0,1): count should be 4, got {uf.count}"
        uf.union(2, 3)
        assert uf.count == 3, f"after union(2,3): count should be 3, got {uf.count}"
        uf.union(0, 2)
        assert uf.count == 2, f"after union(0,2): count should be 2, got {uf.count}"

    def test_already_connected_no_decrement(self):
        uf = s.UnionFind(3)
        uf.union(0, 1)
        uf.union(1, 2)
        assert uf.count == 1, f"after connecting all 3: count should be 1, got {uf.count}"
        result = uf.union(0, 2)
        assert result is False, \
            f"union(0,2) when already connected: should return False, got {result}"
        assert uf.count == 1, \
            f"count should stay 1 after redundant union, got {uf.count}"

    def test_union_returns_true_when_new(self):
        uf = s.UnionFind(3)
        result = uf.union(0, 1)
        assert result is True, f"union(0,1) first time: should return True, got {result}"

    def test_reflexive(self):
        uf = s.UnionFind(3)
        assert uf.connected(0, 0), "a node should always be connected to itself"

    def test_two_separate_components(self):
        uf = s.UnionFind(6)
        uf.union(0, 1); uf.union(1, 2)
        uf.union(3, 4); uf.union(4, 5)
        assert uf.connected(0, 2), "component {0,1,2}: 0 and 2 should be connected"
        assert uf.connected(3, 5), "component {3,4,5}: 3 and 5 should be connected"
        assert not uf.connected(0, 3), \
            "components {0,1,2} and {3,4,5} are separate: 0 and 3 should not be connected"
        assert uf.count == 2, f"two components: count should be 2, got {uf.count}"

    def test_path_compression_correctness(self):
        uf = s.UnionFind(5)
        uf.union(0, 1); uf.union(1, 2); uf.union(2, 3); uf.union(3, 4)
        r = uf.find(0)
        for i in range(5):
            assert uf.find(i) == r, \
                f"after chaining 0-4: find({i}) should return root {r}, got {uf.find(i)}"

    def test_large_chain(self):
        n = 10000
        uf = s.UnionFind(n)
        for i in range(n - 1):
            uf.union(i, i + 1)
        assert uf.count == 1, \
            f"after chaining {n} nodes: count should be 1, got {uf.count}"
        assert uf.connected(0, n - 1), \
            f"after chaining: node 0 and node {n-1} should be connected"

    def test_large_many_components(self):
        n = 10000
        uf = s.UnionFind(n)
        # union even pairs: (0,1), (2,3), (4,5), ...
        for i in range(0, n, 2):
            uf.union(i, i + 1)
        assert uf.count == n // 2, \
            f"n/2 pairs: count should be {n//2}, got {uf.count}"
        for i in range(0, n, 2):
            assert uf.connected(i, i + 1), \
                f"pair ({i},{i+1}) should be connected"
            if i + 2 < n:
                assert not uf.connected(i, i + 2), \
                    f"different pairs ({i},{i+2}) should not be connected"

    def test_large_merge_components(self):
        n = 1000
        uf = s.UnionFind(n)
        # first connect pairs
        for i in range(0, n, 2):
            uf.union(i, i + 1)
        assert uf.count == n // 2
        # now merge all pairs into one component
        for i in range(0, n - 2, 2):
            uf.union(i, i + 2)
        assert uf.count == 1, \
            f"after merging all pairs into one: count should be 1, got {uf.count}"
        assert uf.connected(0, n - 1), \
            f"after full merge: node 0 and {n-1} should be connected"

    def test_large_star(self):
        # all nodes connect to node 0 — worst case for naive union without size tracking
        n = 5000
        uf = s.UnionFind(n)
        for i in range(1, n):
            uf.union(0, i)
        assert uf.count == 1, \
            f"star graph: all {n} nodes connected to 0, count should be 1, got {uf.count}"
        for i in range(1, n):
            assert uf.connected(0, i), \
                f"star: node 0 and node {i} should be connected"
        for i in range(1, min(n, 20)):
            for j in range(i + 1, min(n, 20)):
                assert uf.connected(i, j), \
                    f"star: all nodes should be transitively connected, {i} and {j} are not"

    def test_large_redundant_unions(self):
        n = 1000
        uf = s.UnionFind(n)
        for i in range(n - 1):
            uf.union(i, i + 1)
        assert uf.count == 1
        # now do 1000 redundant unions — count must stay 1
        for i in range(n - 1):
            result = uf.union(i, i + 1)
            assert result is False, \
                f"redundant union({i},{i+1}): should return False, got {result}"
        assert uf.count == 1, \
            f"after redundant unions: count should still be 1, got {uf.count}"

    def test_large_find_consistency(self):
        n = 5000
        uf = s.UnionFind(n)
        for i in range(n - 1):
            uf.union(i, i + 1)
        root = uf.find(0)
        for i in range(n):
            assert uf.find(i) == root, \
                f"all nodes in one component: find({i}) should return root {root}, got {uf.find(i)}"

    def test_deep_chain_no_recursion_error(self):
        # Without iterative path compression, find(0) on a manually constructed
        # chain of 2000 nodes recurses 2000 levels deep — past Python's default
        # limit of 1000 → RecursionError.
        # With an iterative find loop, this completes instantly.
        n = 2000
        uf = s.UnionFind(n)
        # bypass union() to force a true worst-case chain: 0→1→2→...→n-1
        # union() with rank would balance the tree and hide the problem
        for i in range(n - 1):
            uf.parent[i] = i + 1
        uf.count = 1
        try:
            root = uf.find(0)
            assert root == n - 1, \
                f"chain root should be {n-1}, got {root}"
        except RecursionError:
            raise AssertionError(
                f"find() hit Python's recursion limit on a chain of {n} nodes — "
                f"implement path compression with an iterative find loop, not recursion"
            )

    def test_large_random_unions(self):
        n = 1000
        uf = s.UnionFind(n)
        rng = random.Random(42)
        pairs = [(rng.randint(0, n-1), rng.randint(0, n-1)) for _ in range(2000)]
        for a, b in pairs:
            uf.union(a, b)
        # verify find consistency: all nodes in same component share same root
        components: dict[int, set] = {}
        for i in range(n):
            r = uf.find(i)
            components.setdefault(r, set()).add(i)
        assert uf.count == len(components), \
            f"count {uf.count} should equal number of distinct roots {len(components)}"
        for root, members in components.items():
            for m in members:
                assert uf.connected(m, root), \
                    f"node {m} should be connected to its root {root}"


class TestMinHeap:
    def test_pop_returns_min(self):
        h = s.MinHeap()
        for v in [5, 3, 8, 1, 9, 2]:
            h.push(v)
        result = h.pop()
        assert result == 1, f"pop() should return minimum (1), got {result}"

    def test_sorted_order(self):
        h = s.MinHeap()
        for v in [5, 3, 8, 1, 9, 2]:
            h.push(v)
        out = [h.pop() for _ in range(6)]
        assert out == [1, 2, 3, 5, 8, 9], \
            f"repeated pop() should yield sorted order, got {out}, want [1,2,3,5,8,9]"

    def test_peek_does_not_remove(self):
        h = s.MinHeap()
        h.push(3); h.push(1)
        peeked = h.peek()
        assert peeked == 1, f"peek() should return 1 (min), got {peeked}"
        assert len(h) == 2, f"peek() should not remove element, len should be 2, got {len(h)}"

    def test_len(self):
        h = s.MinHeap()
        assert len(h) == 0, f"empty heap: len should be 0, got {len(h)}"
        h.push(1); h.push(2)
        assert len(h) == 2, f"after 2 pushes: len should be 2, got {len(h)}"
        h.pop()
        assert len(h) == 1, f"after 1 pop: len should be 1, got {len(h)}"

    def test_single_element(self):
        h = s.MinHeap()
        h.push(42)
        assert h.peek() == 42, f"single element peek: got {h.peek()}, want 42"
        assert h.pop() == 42, f"single element pop: got 42"
        assert len(h) == 0, f"after popping last element: len should be 0, got {len(h)}"

    def test_duplicates(self):
        h = s.MinHeap()
        for v in [3, 3, 1, 1, 2, 2]:
            h.push(v)
        out = [h.pop() for _ in range(6)]
        assert out == [1, 1, 2, 2, 3, 3], \
            f"duplicates: got {out}, want [1,1,2,2,3,3]"

    def test_negatives(self):
        h = s.MinHeap()
        for v in [-5, 3, -1, 0]:
            h.push(v)
        result = h.pop()
        assert result == -5, f"min of [-5,3,-1,0] is -5, got {result}"

    def test_pop_empty_raises(self):
        h = s.MinHeap()
        raised = False
        try:
            h.pop()
        except (IndexError, Exception):
            raised = True
        assert raised, "pop() on empty heap should raise an exception"

    def test_large_sorted_input(self):
        h = s.MinHeap()
        for v in range(1000):
            h.push(v)
        out = [h.pop() for _ in range(1000)]
        assert out == list(range(1000)), \
            f"already sorted input: pop order should still be sorted"

    def test_large_reverse_sorted_input(self):
        h = s.MinHeap()
        for v in range(999, -1, -1):
            h.push(v)
        out = [h.pop() for _ in range(1000)]
        assert out == list(range(1000)), \
            f"reverse sorted input: pop order should be sorted, first mismatch at index {next((i for i,(x,y) in enumerate(zip(out,range(1000))) if x!=y), 'none')}"

    def test_large_random(self):
        vals = list(range(5000))
        random.Random(42).shuffle(vals)
        h = s.MinHeap()
        for v in vals:
            h.push(v)
        out = [h.pop() for _ in range(5000)]
        assert out == list(range(5000)), \
            f"5000 shuffled elements: pop order should be sorted, first mismatch at index {next((i for i,(x,y) in enumerate(zip(out,range(5000))) if x!=y), 'none')}"

    def test_large_all_same(self):
        h = s.MinHeap()
        for _ in range(1000):
            h.push(7)
        out = [h.pop() for _ in range(1000)]
        assert out == [7] * 1000, f"1000 identical values: all pops should return 7"

    def test_large_interleaved_push_pop(self):
        # push and pop alternately — tests heap integrity under mixed operations
        h = s.MinHeap()
        rng = random.Random(42)
        reference = []
        import heapq
        for _ in range(2000):
            v = rng.randint(0, 10000)
            h.push(v)
            heapq.heappush(reference, v)
        for _ in range(2000):
            got = h.pop()
            expected = heapq.heappop(reference)
            assert got == expected, \
                f"interleaved push/pop: got {got}, expected {expected}"

    def test_large_peek_consistent(self):
        h = s.MinHeap()
        for v in range(500, 0, -1):
            h.push(v)
        for expected_min in range(1, 501):
            assert h.peek() == expected_min, \
                f"peek() before pop: expected {expected_min}, got {h.peek()}"
            assert h.pop() == expected_min, \
                f"pop(): expected {expected_min}"

    def test_large_negative_values(self):
        vals = list(range(-2500, 2500))
        random.Random(99).shuffle(vals)
        h = s.MinHeap()
        for v in vals:
            h.push(v)
        out = [h.pop() for _ in range(5000)]
        assert out == list(range(-2500, 2500)), \
            f"mixed negative/positive values: pop order should be sorted"


class TestTrie:
    def test_search_inserted_word(self):
        t = s.Trie()
        t.insert("hello")
        assert t.search("hello"), "search('hello') after insert('hello'): should be True"

    def test_search_missing_word(self):
        t = s.Trie()
        t.insert("hello")
        assert not t.search("hell"), \
            "search('hell'): 'hell' is a prefix of 'hello' but not inserted, should be False"
        assert not t.search("helloo"), \
            "search('helloo'): longer than inserted word, should be False"
        assert not t.search("world"), \
            "search('world'): completely different word, should be False"

    def test_prefix_not_word(self):
        t = s.Trie()
        t.insert("card")
        assert not t.search("car"), \
            "search('car'): 'car' is a prefix of 'card' but not a word, should be False"
        assert t.starts_with("car"), \
            "starts_with('car'): 'car' is a prefix of 'card', should be True"

    def test_word_is_also_prefix(self):
        t = s.Trie()
        t.insert("car"); t.insert("card")
        assert t.search("car"), "search('car') after insert('car'): should be True"
        assert t.search("card"), "search('card') after insert('card'): should be True"

    def test_starts_with_true(self):
        t = s.Trie()
        t.insert("apple")
        for prefix in ["a", "ap", "app", "appl", "apple"]:
            assert t.starts_with(prefix), \
                f"starts_with('{prefix}'): all prefixes of 'apple' should return True"

    def test_starts_with_empty(self):
        t = s.Trie()
        t.insert("apple")
        assert t.starts_with(""), "starts_with(''): empty string is prefix of everything"

    def test_starts_with_false(self):
        t = s.Trie()
        t.insert("apple")
        assert not t.starts_with("apl"), \
            "starts_with('apl'): 'apl' is not a prefix of 'apple', should be False"
        assert not t.starts_with("b"), \
            "starts_with('b'): no words starting with 'b', should be False"

    def test_multiple_words(self):
        t = s.Trie()
        for w in ["cat", "car", "card", "dog", "do"]:
            t.insert(w)
        assert t.search("cat"), "search('cat'): should be True"
        assert t.search("do"), "search('do'): should be True"
        assert not t.search("ca"), "search('ca'): prefix only, should be False"
        assert not t.search("d"), "search('d'): prefix only, should be False"

    def test_empty_string(self):
        t = s.Trie()
        t.insert("")
        assert t.search(""), "search('') after insert(''): should be True"

    def test_large_word_list(self):
        t = s.Trie()
        words = [f"word{i}" for i in range(2000)]
        for w in words:
            t.insert(w)
        for w in words:
            assert t.search(w), f"search('{w}'): inserted word should be found"
        assert not t.search("word"), \
            "search('word'): prefix only, not inserted"
        assert t.starts_with("word"), \
            "starts_with('word'): all words share this prefix"

    def test_large_shared_prefixes(self):
        # all words share long common prefix — stresses deep trie paths
        t = s.Trie()
        prefix = "abcdefghij"
        words = [prefix + str(i) for i in range(1000)]
        for w in words:
            t.insert(w)
        for w in words:
            assert t.search(w), f"search('{w}'): should be True"
        assert not t.search(prefix), \
            f"search('{prefix}'): prefix itself not inserted, should be False"
        assert t.starts_with(prefix), \
            f"starts_with('{prefix}'): all words share this prefix, should be True"
        for i in range(1, len(prefix) + 1):
            assert t.starts_with(prefix[:i]), \
                f"starts_with('{prefix[:i]}'): should be True"

    def test_large_distinct_prefixes(self):
        # words with no shared prefixes — stresses root branching
        t = s.Trie()
        import string
        words = [c * 10 for c in string.ascii_lowercase]  # "aaaaaaaaaa", "bbbbbbbbbb", ...
        for w in words:
            t.insert(w)
        for w in words:
            assert t.search(w), f"search('{w}'): should be True"
        for c in string.ascii_lowercase:
            assert t.starts_with(c), \
                f"starts_with('{c}'): single char prefix should exist"
        assert not t.starts_with("A"), \
            "starts_with('A'): uppercase not inserted, should be False"

    def test_large_search_nonexistent(self):
        t = s.Trie()
        for i in range(1000):
            t.insert(f"word{i}")
        # search for words that were never inserted
        for i in range(1000, 2000):
            assert not t.search(f"word{i}"), \
                f"search('word{i}'): not inserted, should be False"
        assert not t.search("completely_different"), \
            "search('completely_different'): not inserted, should be False"

    def test_large_interleaved_insert_search(self):
        # insert and search alternately — each search only sees words inserted so far
        t = s.Trie()
        inserted = set()
        for i in range(500):
            word = f"item{i}"
            t.insert(word)
            inserted.add(word)
            # verify all inserted words are found
            assert t.search(word), f"search('{word}') immediately after insert: should be True"
            # verify a not-yet-inserted word is not found
            future = f"item{i + 500}"
            assert not t.search(future), \
                f"search('{future}'): not yet inserted, should be False"

    def test_large_overwrite_same_word(self):
        # inserting the same word many times should not break anything
        t = s.Trie()
        for _ in range(1000):
            t.insert("duplicate")
        assert t.search("duplicate"), \
            "search('duplicate'): should be True after 1000 inserts"
        assert not t.search("duplicat"), \
            "search('duplicat'): prefix only, should be False"
        assert t.starts_with("dup"), \
            "starts_with('dup'): should be True"
