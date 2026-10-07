from drills import solution as s


class TestTwoSum:
    def test_basic(self):
        nums, target = [2, 7, 11, 15], 9
        result = s.two_sum(nums, target)
        assert result == [0, 1], f"two_sum({nums}, {target}): got {result}, want [0,1]"

    def test_not_first_pair(self):
        nums, target = [3, 2, 4], 6
        result = s.two_sum(nums, target)
        assert result == [1, 2], f"two_sum({nums}, {target}): got {result}, want [1,2]"

    def test_same_element_twice(self):
        nums, target = [3, 3], 6
        result = s.two_sum(nums, target)
        assert result == [0, 1], f"two_sum({nums}, {target}): got {result}, want [0,1]"

    def test_negatives(self):
        nums, target = [-3, 4, 3, 90], 0
        result = s.two_sum(nums, target)
        assert result is not None, f"two_sum({nums}, {target}): should find a solution, got None"
        assert set(result) == {0, 2}, \
            f"two_sum({nums}, {target}): indices should be {{0,2}}, got {result}"

    def test_not_found(self):
        result = s.two_sum([1, 2, 3], 10)
        assert result is None, f"two_sum([1,2,3], 10): no solution exists, got {result}"

    def test_large(self):
        nums = list(range(1000))
        target = 999 + 998
        result = s.two_sum(nums, target)
        assert result is not None, f"two_sum(range(1000), {target}): should find solution"
        assert sum(nums[i] for i in result) == target, \
            f"two_sum: indices {result} don't sum to {target}"


class TestIsPalindrome:
    def test_odd_palindrome(self):
        assert s.is_palindrome("racecar"), "is_palindrome('racecar'): should be True"

    def test_even_palindrome(self):
        assert s.is_palindrome("abba"), "is_palindrome('abba'): should be True"

    def test_not_palindrome(self):
        assert not s.is_palindrome("hello"), "is_palindrome('hello'): should be False"

    def test_empty(self):
        assert s.is_palindrome(""), "is_palindrome(''): empty string is a palindrome"

    def test_single(self):
        assert s.is_palindrome("a"), "is_palindrome('a'): single char is a palindrome"

    def test_two_same(self):
        assert s.is_palindrome("aa"), "is_palindrome('aa'): should be True"

    def test_two_different(self):
        assert not s.is_palindrome("ab"), "is_palindrome('ab'): should be False"

    def test_numbers(self):
        assert s.is_palindrome("12321"), "is_palindrome('12321'): should be True"
        assert not s.is_palindrome("12345"), "is_palindrome('12345'): should be False"


class TestMaxSubarraySumFixed:
    def test_basic(self):
        nums, k = [1, 2, 3, 4, 5], 2
        result = s.max_subarray_sum_fixed(nums, k)
        assert result == 9, f"max_subarray_sum_fixed({nums}, k={k}): got {result}, want 9 (4+5)"

    def test_window_size_one(self):
        nums, k = [3, 1, 4, 1, 5], 1
        result = s.max_subarray_sum_fixed(nums, k)
        assert result == 5, f"max_subarray_sum_fixed({nums}, k=1): got {result}, want 5 (max element)"

    def test_window_full_array(self):
        nums, k = [1, 2, 3], 3
        result = s.max_subarray_sum_fixed(nums, k)
        assert result == 6, f"max_subarray_sum_fixed({nums}, k=3): got {result}, want 6 (sum of all)"

    def test_window_larger_than_array(self):
        result = s.max_subarray_sum_fixed([1, 2], 5)
        assert result is None, \
            f"max_subarray_sum_fixed([1,2], k=5): k>len, got {result}, want None"

    def test_negatives(self):
        nums, k = [-1, -2, -3, -4], 2
        result = s.max_subarray_sum_fixed(nums, k)
        assert result == -3, \
            f"max_subarray_sum_fixed({nums}, k={k}): all negative, got {result}, want -3 (-1+-2)"

    def test_mixed(self):
        nums, k = [2, 1, 5, 1, 3, 2], 3
        result = s.max_subarray_sum_fixed(nums, k)
        assert result == 9, \
            f"max_subarray_sum_fixed({nums}, k={k}): got {result}, want 9 (5+1+3)"

    def test_best_at_start(self):
        nums, k = [5, 4, 1, 1, 1], 2
        result = s.max_subarray_sum_fixed(nums, k)
        assert result == 9, \
            f"max_subarray_sum_fixed({nums}, k={k}): best window is at start [5,4], got {result}, want 9"

    def test_best_at_end(self):
        nums, k = [1, 1, 1, 4, 5], 2
        result = s.max_subarray_sum_fixed(nums, k)
        assert result == 9, \
            f"max_subarray_sum_fixed({nums}, k={k}): best window is at end [4,5], got {result}, want 9"


class TestLongestUniqueSubstring:
    def test_basic(self):
        result = s.longest_unique_substring("abcabcbb")
        assert result == 3, \
            f"longest_unique_substring('abcabcbb'): got {result}, want 3 ('abc')"

    def test_all_same(self):
        result = s.longest_unique_substring("bbbbb")
        assert result == 1, \
            f"longest_unique_substring('bbbbb'): got {result}, want 1 (any single 'b')"

    def test_empty(self):
        result = s.longest_unique_substring("")
        assert result == 0, f"longest_unique_substring(''): got {result}, want 0"

    def test_all_unique(self):
        result = s.longest_unique_substring("abcdef")
        assert result == 6, \
            f"longest_unique_substring('abcdef'): all unique, got {result}, want 6"

    def test_single(self):
        result = s.longest_unique_substring("a")
        assert result == 1, f"longest_unique_substring('a'): got {result}, want 1"

    def test_pwwkew(self):
        result = s.longest_unique_substring("pwwkew")
        assert result == 3, \
            f"longest_unique_substring('pwwkew'): got {result}, want 3 ('wke')"

    def test_answer_at_end(self):
        result = s.longest_unique_substring("aabcd")
        assert result == 4, \
            f"longest_unique_substring('aabcd'): got {result}, want 4 ('abcd')"

    def test_answer_at_start(self):
        result = s.longest_unique_substring("abcdaa")
        assert result == 4, \
            f"longest_unique_substring('abcdaa'): got {result}, want 4 ('abcd')"


class TestSubsets:
    def test_count(self):
        result = s.subsets([1, 2, 3])
        assert len(result) == 8, \
            f"subsets([1,2,3]): should have 2^3=8 subsets, got {len(result)}"

    def test_contains_empty(self):
        result = s.subsets([1, 2, 3])
        assert [] in result, f"subsets([1,2,3]): should contain empty set [], got {result}"

    def test_contains_full(self):
        result = s.subsets([1, 2, 3])
        assert [1, 2, 3] in result, \
            f"subsets([1,2,3]): should contain full set [1,2,3], got {result}"

    def test_all_unique(self):
        result = s.subsets([1, 2, 3])
        as_tuples = [tuple(sorted(x)) for x in result]
        dupes = [x for x in as_tuples if as_tuples.count(x) > 1]
        assert len(dupes) == 0, f"subsets should all be unique, duplicates found: {dupes}"

    def test_empty_input(self):
        result = s.subsets([])
        assert result == [[]], f"subsets([]): only subset is [], got {result}"

    def test_single_element(self):
        result = sorted(s.subsets([1]))
        assert result == [[], [1]], f"subsets([1]): got {result}, want [[], [1]]"

    def test_four_elements(self):
        result = s.subsets([1, 2, 3, 4])
        assert len(result) == 16, \
            f"subsets([1,2,3,4]): should have 2^4=16 subsets, got {len(result)}"


class TestPermutations:
    def test_count_three(self):
        result = s.permutations([1, 2, 3])
        assert len(result) == 6, \
            f"permutations([1,2,3]): should have 3!=6, got {len(result)}"

    def test_all_present(self):
        result = s.permutations([1, 2, 3])
        expected = [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
        assert sorted(result) == sorted(expected), \
            f"permutations([1,2,3]): got {sorted(result)}, want {sorted(expected)}"

    def test_no_duplicates(self):
        result = s.permutations([1, 2, 3])
        as_tuples = [tuple(x) for x in result]
        dupes = [x for x in as_tuples if as_tuples.count(x) > 1]
        assert len(dupes) == 0, f"no duplicate permutations, found: {dupes}"

    def test_single_element(self):
        result = s.permutations([1])
        assert result == [[1]], f"permutations([1]): got {result}, want [[1]]"

    def test_two_elements(self):
        result = s.permutations([1, 2])
        assert sorted(result) == [[1, 2], [2, 1]], \
            f"permutations([1,2]): got {sorted(result)}, want [[1,2],[2,1]]"

    def test_each_permutation_is_full_length(self):
        nums = [1, 2, 3, 4]
        for p in s.permutations(nums):
            assert sorted(p) == nums, \
                f"each permutation should contain all elements {nums}, got {p}"


class TestClimbStairs:
    def test_one(self):
        assert s.climb_stairs(1) == 1, f"climb_stairs(1): got {s.climb_stairs(1)}, want 1"

    def test_two(self):
        assert s.climb_stairs(2) == 2, f"climb_stairs(2): got {s.climb_stairs(2)}, want 2"

    def test_three(self):
        assert s.climb_stairs(3) == 3, \
            f"climb_stairs(3): 3 ways (1+1+1, 1+2, 2+1), got {s.climb_stairs(3)}, want 3"

    def test_five(self):
        assert s.climb_stairs(5) == 8, f"climb_stairs(5): got {s.climb_stairs(5)}, want 8"

    def test_ten(self):
        assert s.climb_stairs(10) == 89, f"climb_stairs(10): got {s.climb_stairs(10)}, want 89"


class TestCoinChange:
    def test_basic(self):
        coins, amount = [1, 2, 5], 11
        result = s.coin_change(coins, amount)
        assert result == 3, \
            f"coin_change({coins}, {amount}): got {result}, want 3 (5+5+1)"

    def test_impossible(self):
        coins, amount = [2], 3
        result = s.coin_change(coins, amount)
        assert result == -1, \
            f"coin_change({coins}, {amount}): impossible, got {result}, want -1"

    def test_zero_amount(self):
        result = s.coin_change([1], 0)
        assert result == 0, f"coin_change([1], 0): 0 coins needed for amount 0, got {result}"

    def test_exact_coin(self):
        result = s.coin_change([5], 5)
        assert result == 1, f"coin_change([5], 5): 1 coin needed, got {result}"

    def test_single_coin_exact(self):
        result = s.coin_change([3], 9)
        assert result == 3, f"coin_change([3], 9): 3 coins of 3, got {result}"

    def test_greedy_fails(self):
        coins, amount = [1, 3, 4, 6], 9
        result = s.coin_change(coins, amount)
        assert result == 2, \
            f"coin_change({coins}, {amount}): greedy would pick 6+1+1+1=4, optimal is 6+3=2, got {result}"

    def test_large_amount(self):
        result = s.coin_change([1, 2, 5], 100)
        assert result == 20, \
            f"coin_change([1,2,5], 100): got {result}, want 20 (20 fives)"


class TestLongestCommonSubsequence:
    def test_basic(self):
        result = s.longest_common_subsequence("abcde", "ace")
        assert result == 3, \
            f"lcs('abcde','ace'): got {result}, want 3 ('ace')"

    def test_identical(self):
        result = s.longest_common_subsequence("abc", "abc")
        assert result == 3, \
            f"lcs('abc','abc'): identical strings, got {result}, want 3"

    def test_no_common(self):
        result = s.longest_common_subsequence("abc", "def")
        assert result == 0, f"lcs('abc','def'): no common chars, got {result}, want 0"

    def test_empty_first(self):
        result = s.longest_common_subsequence("", "abc")
        assert result == 0, f"lcs('','abc'): empty string, got {result}, want 0"

    def test_empty_second(self):
        result = s.longest_common_subsequence("abc", "")
        assert result == 0, f"lcs('abc',''): empty string, got {result}, want 0"

    def test_subsequence_not_substring(self):
        result = s.longest_common_subsequence("axbycz", "abc")
        assert result == 3, \
            f"lcs('axbycz','abc'): 'abc' is a subsequence (not substring), got {result}, want 3"

    def test_longer(self):
        result = s.longest_common_subsequence("AGGTAB", "GXTXAYB")
        assert result == 4, \
            f"lcs('AGGTAB','GXTXAYB'): got {result}, want 4 ('GTAB')"


class TestKnapsack01:
    def test_basic(self):
        w, v, cap = [2, 3, 4, 5], [3, 4, 5, 6], 5
        result = s.knapsack_01(w, v, cap)
        assert result == 7, \
            f"knapsack_01(weights={w}, values={v}, cap={cap}): got {result}, want 7"

    def test_exact_fit(self):
        w, v, cap = [1, 2, 3], [10, 15, 40], 6
        result = s.knapsack_01(w, v, cap)
        assert result == 65, \
            f"knapsack_01(weights={w}, values={v}, cap={cap}): got {result}, want 65 (all items)"

    def test_zero_capacity(self):
        result = s.knapsack_01([1, 2], [10, 20], 0)
        assert result == 0, f"knapsack_01 with capacity=0: got {result}, want 0"

    def test_single_item_fits(self):
        result = s.knapsack_01([3], [10], 5)
        assert result == 10, f"knapsack_01([3],[10],cap=5): item fits, got {result}, want 10"

    def test_single_item_too_heavy(self):
        result = s.knapsack_01([10], [100], 5)
        assert result == 0, \
            f"knapsack_01([10],[100],cap=5): item too heavy, got {result}, want 0"

    def test_all_items_fit(self):
        result = s.knapsack_01([1, 1, 1], [5, 5, 5], 10)
        assert result == 15, \
            f"knapsack_01: all items fit within capacity, got {result}, want 15"

    def test_greedy_fails(self):
        w, v, cap = [5, 4, 3], [10, 6, 6], 7
        result = s.knapsack_01(w, v, cap)
        assert result == 12, \
            f"knapsack_01: greedy (highest value first) picks item 0 (v=10) but optimal is items 1+2 (v=12), got {result}"
