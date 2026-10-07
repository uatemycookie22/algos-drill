"""Canonical searching & array algorithms — Tier 1."""
from collections.abc import Callable


def binary_search(nums: list[int], target: int) -> int:
    """Classic binary search on a sorted array. Returns index or -1."""
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def bisect_left(nums: list[int], target: int) -> int:
    """Leftmost insertion point: first index i where nums[i] >= target."""
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def bisect_right(nums: list[int], target: int) -> int:
    """Rightmost insertion point: first index i where nums[i] > target."""
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def binary_search_on_answer(lo: int, hi: int, feasible: Callable[[int], bool]) -> int:
    """Find the smallest x in [lo, hi] where feasible(x) is True."""
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def merge(a: list[int], b: list[int]) -> list[int]:
    """Merge two sorted lists into one sorted list."""
    i = j = 0
    out: list[int] = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return out


def quickselect(nums: list[int], k: int) -> int | None:
    """Return the k-th smallest element (1-indexed). O(n) average."""
    nums = list(nums)

    def partition(lo: int, hi: int) -> int:
        pivot = nums[hi]
        i = lo
        for j in range(lo, hi):
            if nums[j] < pivot:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
        nums[i], nums[hi] = nums[hi], nums[i]
        return i

    lo, hi = 0, len(nums) - 1
    target = k - 1
    while lo <= hi:
        p = partition(lo, hi)
        if p == target:
            return nums[p]
        elif p < target:
            lo = p + 1
        else:
            hi = p - 1
    return None
