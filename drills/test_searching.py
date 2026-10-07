import pytest
from drills import solution as s


class TestBinarySearch:
    def test_found_first(self):
        nums = [1, 3, 5, 7, 9]
        assert s.binary_search(nums, 1) == 0, \
            f"binary_search({nums}, 1): got {s.binary_search(nums, 1)}, want 0"

    def test_found_last(self):
        nums = [1, 3, 5, 7, 9]
        assert s.binary_search(nums, 9) == 4, \
            f"binary_search({nums}, 9): got {s.binary_search(nums, 9)}, want 4"

    def test_found_middle(self):
        nums = [1, 3, 5, 7, 9]
        assert s.binary_search(nums, 5) == 2, \
            f"binary_search({nums}, 5): got {s.binary_search(nums, 5)}, want 2"

    def test_not_found_between(self):
        nums = [1, 3, 5, 7, 9]
        assert s.binary_search(nums, 4) == -1, \
            f"binary_search({nums}, 4): 4 not in list, got {s.binary_search(nums, 4)}, want -1"

    def test_not_found_below(self):
        nums = [1, 3, 5, 7, 9]
        assert s.binary_search(nums, 0) == -1, \
            f"binary_search({nums}, 0): 0 below min, got {s.binary_search(nums, 0)}, want -1"

    def test_not_found_above(self):
        nums = [1, 3, 5, 7, 9]
        assert s.binary_search(nums, 10) == -1, \
            f"binary_search({nums}, 10): 10 above max, got {s.binary_search(nums, 10)}, want -1"

    def test_single_element_found(self):
        assert s.binary_search([42], 42) == 0, \
            f"binary_search([42], 42): got {s.binary_search([42], 42)}, want 0"

    def test_single_element_not_found(self):
        assert s.binary_search([42], 1) == -1, \
            f"binary_search([42], 1): got {s.binary_search([42], 1)}, want -1"

    def test_empty(self):
        assert s.binary_search([], 1) == -1, \
            f"binary_search([], 1): empty list should return -1, got {s.binary_search([], 1)}"

    def test_two_elements_first(self):
        assert s.binary_search([1, 2], 1) == 0, \
            f"binary_search([1,2], 1): got {s.binary_search([1,2], 1)}, want 0"

    def test_two_elements_second(self):
        assert s.binary_search([1, 2], 2) == 1, \
            f"binary_search([1,2], 2): got {s.binary_search([1,2], 2)}, want 1"

    def test_negatives(self):
        nums = [-10, -5, 0, 5, 10]
        assert s.binary_search(nums, -5) == 1, \
            f"binary_search({nums}, -5): got {s.binary_search(nums, -5)}, want 1"
        assert s.binary_search(nums, 0) == 2, \
            f"binary_search({nums}, 0): got {s.binary_search(nums, 0)}, want 2"

    def test_large(self):
        nums = list(range(0, 10000, 2))
        result = s.binary_search(nums, 9998)
        assert result == 4999, f"binary_search(range(0,10000,2), 9998): got {result}, want 4999"
        result = s.binary_search(nums, 9999)
        assert result == -1, f"binary_search(range(0,10000,2), 9999): 9999 not in list, got {result}, want -1"

    def test_all_same_value(self):
        nums = [5, 5, 5, 5]
        idx = s.binary_search(nums, 5)
        assert 0 <= idx <= 3, f"binary_search([5,5,5,5], 5): any valid index acceptable, got {idx}"

    def test_all_items_individually(self):
        nums = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
        for i, v in enumerate(nums):
            result = s.binary_search(nums, v)
            assert result == i, f"binary_search({nums}, {v}): got {result}, want {i}"


class TestBisectLeft:
    def test_insert_before_duplicates(self):
        nums = [1, 2, 2, 2, 3]
        assert s.bisect_left(nums, 2) == 1, \
            f"bisect_left({nums}, 2): got {s.bisect_left(nums, 2)}, want 1 (first occurrence)"

    def test_insert_at_start(self):
        nums = [1, 2, 3]
        assert s.bisect_left(nums, 0) == 0, \
            f"bisect_left({nums}, 0): 0 smaller than all, got {s.bisect_left(nums, 0)}, want 0"

    def test_insert_at_end(self):
        nums = [1, 2, 3]
        assert s.bisect_left(nums, 4) == 3, \
            f"bisect_left({nums}, 4): 4 larger than all, got {s.bisect_left(nums, 4)}, want 3"

    def test_exact_match_no_duplicates(self):
        nums = [1, 2, 3]
        assert s.bisect_left(nums, 2) == 1, \
            f"bisect_left({nums}, 2): got {s.bisect_left(nums, 2)}, want 1"

    def test_empty(self):
        assert s.bisect_left([], 5) == 0, \
            f"bisect_left([], 5): empty list, got {s.bisect_left([], 5)}, want 0"

    def test_single_less(self):
        assert s.bisect_left([5], 3) == 0, \
            f"bisect_left([5], 3): 3 < 5, insert at 0, got {s.bisect_left([5], 3)}"

    def test_single_equal(self):
        assert s.bisect_left([5], 5) == 0, \
            f"bisect_left([5], 5): equal, leftmost so insert at 0, got {s.bisect_left([5], 5)}"

    def test_single_greater(self):
        assert s.bisect_left([5], 7) == 1, \
            f"bisect_left([5], 7): 7 > 5, insert after, got {s.bisect_left([5], 7)}, want 1"

    def test_all_same(self):
        nums = [3, 3, 3, 3]
        assert s.bisect_left(nums, 3) == 0, \
            f"bisect_left({nums}, 3): leftmost position is 0, got {s.bisect_left(nums, 3)}"

    def test_large(self):
        nums = list(range(1000))
        assert s.bisect_left(nums, 500) == 500, \
            f"bisect_left(range(1000), 500): got {s.bisect_left(nums, 500)}, want 500"


class TestBisectRight:
    def test_insert_after_duplicates(self):
        nums = [1, 2, 2, 2, 3]
        assert s.bisect_right(nums, 2) == 4, \
            f"bisect_right({nums}, 2): got {s.bisect_right(nums, 2)}, want 4 (after last occurrence)"

    def test_insert_at_start(self):
        nums = [1, 2, 3]
        assert s.bisect_right(nums, 0) == 0, \
            f"bisect_right({nums}, 0): 0 smaller than all, got {s.bisect_right(nums, 0)}, want 0"

    def test_insert_at_end(self):
        nums = [1, 2, 3]
        assert s.bisect_right(nums, 3) == 3, \
            f"bisect_right({nums}, 3): insert after last element, got {s.bisect_right(nums, 3)}, want 3"

    def test_insert_beyond_end(self):
        nums = [1, 2, 3]
        assert s.bisect_right(nums, 4) == 3, \
            f"bisect_right({nums}, 4): larger than all, got {s.bisect_right(nums, 4)}, want 3"

    def test_empty(self):
        assert s.bisect_right([], 5) == 0, \
            f"bisect_right([], 5): empty list, got {s.bisect_right([], 5)}, want 0"

    def test_all_same(self):
        nums = [3, 3, 3, 3]
        assert s.bisect_right(nums, 3) == 4, \
            f"bisect_right({nums}, 3): insert after all 4 elements, got {s.bisect_right(nums, 3)}, want 4"

    def test_single_less(self):
        assert s.bisect_right([5], 3) == 0, \
            f"bisect_right([5], 3): 3 < 5, got {s.bisect_right([5], 3)}, want 0"

    def test_single_equal(self):
        assert s.bisect_right([5], 5) == 1, \
            f"bisect_right([5], 5): insert after the element, got {s.bisect_right([5], 5)}, want 1"

    def test_large(self):
        nums = list(range(1000))
        assert s.bisect_right(nums, 500) == 501, \
            f"bisect_right(range(1000), 500): got {s.bisect_right(nums, 500)}, want 501"


class TestBinarySearchOnAnswer:
    def test_square_root(self):
        result = s.binary_search_on_answer(0, 100, lambda x: x * x >= 81)
        assert result == 9, f"smallest x where x²≥81: got {result}, want 9"

    def test_always_feasible(self):
        result = s.binary_search_on_answer(0, 10, lambda x: True)
        assert result == 0, f"always feasible: smallest x is lo=0, got {result}"

    def test_only_last_feasible(self):
        result = s.binary_search_on_answer(0, 10, lambda x: x >= 10)
        assert result == 10, f"only x=10 feasible: got {result}, want 10"

    def test_mid_feasible(self):
        result = s.binary_search_on_answer(1, 100, lambda x: x >= 50)
        assert result == 50, f"feasible from 50 onward: got {result}, want 50"

    def test_single_range(self):
        result = s.binary_search_on_answer(5, 5, lambda x: True)
        assert result == 5, f"lo==hi==5: got {result}, want 5"

    def test_large_range(self):
        result = s.binary_search_on_answer(0, 10**6, lambda x: x >= 999999)
        assert result == 999999, f"large range, feasible from 999999: got {result}, want 999999"


class TestMerge:
    def test_interleaved(self):
        a, b = [1, 3, 5], [2, 4, 6]
        result = s.merge(a, b)
        assert result == [1, 2, 3, 4, 5, 6], \
            f"merge({a}, {b}): got {result}, want [1,2,3,4,5,6]"

    def test_left_empty(self):
        result = s.merge([], [1, 2, 3])
        assert result == [1, 2, 3], f"merge([], [1,2,3]): got {result}, want [1,2,3]"

    def test_right_empty(self):
        result = s.merge([1, 2, 3], [])
        assert result == [1, 2, 3], f"merge([1,2,3], []): got {result}, want [1,2,3]"

    def test_both_empty(self):
        assert s.merge([], []) == [], f"merge([], []): got {s.merge([], [])}, want []"

    def test_all_left_smaller(self):
        a, b = [1, 2, 3], [4, 5, 6]
        result = s.merge(a, b)
        assert result == [1, 2, 3, 4, 5, 6], \
            f"merge({a}, {b}): got {result}, want [1,2,3,4,5,6]"

    def test_all_right_smaller(self):
        a, b = [4, 5, 6], [1, 2, 3]
        result = s.merge(a, b)
        assert result == [1, 2, 3, 4, 5, 6], \
            f"merge({a}, {b}): got {result}, want [1,2,3,4,5,6]"

    def test_duplicates(self):
        a, b = [1, 1, 3], [1, 2]
        result = s.merge(a, b)
        assert result == [1, 1, 1, 2, 3], \
            f"merge({a}, {b}): got {result}, want [1,1,1,2,3]"

    def test_single_each(self):
        result = s.merge([2], [1])
        assert result == [1, 2], f"merge([2], [1]): got {result}, want [1,2]"

    def test_negatives(self):
        a, b = [-5, -1, 3], [-4, 0, 4]
        result = s.merge(a, b)
        assert result == [-5, -4, -1, 0, 3, 4], \
            f"merge({a}, {b}): got {result}, want [-5,-4,-1,0,3,4]"

    def test_large(self):
        a = list(range(0, 1000, 2))
        b = list(range(1, 1000, 2))
        result = s.merge(a, b)
        assert result == list(range(1000)), \
            f"merge(evens, odds): result is not sorted range(1000), first mismatch at index {next((i for i,(x,y) in enumerate(zip(result, range(1000))) if x!=y), 'none')}"


class TestQuickselect:
    def test_min(self):
        nums = [3, 1, 2, 5, 4]
        assert s.quickselect(nums, 1) == 1, \
            f"quickselect({nums}, k=1): 1st smallest is 1, got {s.quickselect(nums, 1)}"

    def test_max(self):
        nums = [3, 1, 2, 5, 4]
        assert s.quickselect(nums, 5) == 5, \
            f"quickselect({nums}, k=5): 5th smallest is 5, got {s.quickselect(nums, 5)}"

    def test_median(self):
        nums = [3, 1, 2, 5, 4]
        assert s.quickselect(nums, 3) == 3, \
            f"quickselect({nums}, k=3): median is 3, got {s.quickselect(nums, 3)}"

    def test_single(self):
        assert s.quickselect([7], 1) == 7, \
            f"quickselect([7], k=1): only element is 7, got {s.quickselect([7], 1)}"

    def test_duplicates(self):
        nums = [2, 2, 2, 2]
        assert s.quickselect(nums, 2) == 2, \
            f"quickselect({nums}, k=2): all same value, got {s.quickselect(nums, 2)}, want 2"

    def test_already_sorted(self):
        nums = [1, 2, 3, 4, 5]
        assert s.quickselect(nums, 2) == 2, \
            f"quickselect({nums}, k=2): got {s.quickselect(nums, 2)}, want 2"

    def test_reverse_sorted(self):
        nums = [5, 4, 3, 2, 1]
        assert s.quickselect(nums, 4) == 4, \
            f"quickselect({nums}, k=4): 4th smallest is 4, got {s.quickselect(nums, 4)}"

    def test_negatives(self):
        nums = [-3, -1, -2, 0]
        assert s.quickselect(nums, 1) == -3, \
            f"quickselect({nums}, k=1): smallest is -3, got {s.quickselect(nums, 1)}"

    def test_large(self):
        import random
        nums = list(range(1000))
        random.shuffle(nums)
        result = s.quickselect(nums, 500)
        assert result == 499, \
            f"quickselect(shuffled range(1000), k=500): 500th smallest is 499, got {result}"
