# name: Merge Sort Tree
# prefix: mergesorttree
# ---
from bisect import bisect_right, bisect_left
from itertools import accumulate

class MergeSortTree:
    def __init__(self, v: list[int]):
        self._n = len(v)
        self._log = (self._n - 1).bit_length()
        self._size = 1 << self._log
        self._d = [[] for _ in range(2 * self._size)]
        self._cum = [[] for _ in range(2 * self._size)]

        for i, x in enumerate(v):
            self._d[self._size + i] = [x]
        
        for i in range(self._size - 1, 0, -1):
            self._d[i] = sorted(self._d[2 * i] + self._d[2 * i + 1])
        
        for i in range(1, 2 * self._size):
            if self._d[i]:
                self._cum[i] = list(accumulate(self._d[i], initial=0))

    def _query_le(self, left: int, right: int, x: int, mode="count"):
        """
        内部共通処理
        mode: "count" (x以下の個数), "sum" (x以下の総和)
        """
        res = 0
        left += self._size
        right += self._size
        while left < right:
            if left & 1:
                idx = bisect_right(self._d[left], x)
                res += idx if mode == "count" else self._cum[left][idx]
                left += 1
            if right & 1:
                right -= 1
                idx = bisect_right(self._d[right], x)
                res += idx if mode == "count" else self._cum[right][idx]
            left >>= 1
            right >>= 1
        return res

    def count_le(self, l, r, x): return self._query_le(l, r, x, "count")
    def sum_le(self, l, r, x):   return self._query_le(l, r, x, "sum")
    def count_lt(self, l, r, x): return self._query_le(l, r, x-1, "count")
    def sum_lt(self, l, r, x):   return self._query_le(l, r, x-1, "sum")

    def _query_ge(self, left: int, right: int, x: int, mode="count"):
        """
        内部共通処理
        mode: "count" (x以下の個数), "sum" (x以下の総和)
        """
        res = 0
        left += self._size
        right += self._size
        while left < right:
            if left & 1:
                idx = bisect_left(self._d[left], x)
                cum_size = len(self._cum[left])-1
                res += cum_size - idx if mode == "count" else self._cum[left][cum_size] - self._cum[left][idx]
                left += 1
            if right & 1:
                right -= 1
                idx = bisect_left(self._d[right], x)
                cum_size = len(self._cum[right])-1
                res += cum_size - idx if mode == "count" else self._cum[right][cum_size] - self._cum[right][idx]
            left >>= 1
            right >>= 1
        return res
    
    def count_ge(self, l, r, x): return self._query_ge(l, r, x, "count")
    def sum_ge(self, l, r, x):   return self._query_ge(l, r, x, "sum")
    def count_gt(self, l, r, x): return self._query_ge(l, r, x+1, "count")
    def sum_gt(self, l, r, x):   return self._query_ge(l, r, x+1, "sum")

    def count_range(self, l, r, low, high):
        return self.count_le(l, r, high) - self.count_le(l, r, low - 1)
    def sum_range(self, l, r, low, high):
        return self.sum_le(l, r, high) - self.sum_le(l, r, low - 1)

    def kth_smallest(self, l: int, r: int, k: int) -> int:
        """
        [l, r) の中で k 番目 (1-indexed) に小さい値を返す
        """
        assert 0 < k <= (r - l)
        
        low = self._d[1][0]
        high = self._d[1][-1]
        
        ans = high
        while low <= high:
            mid = (low + high) // 2
            if self.count_le(l, r, mid) >= k:
                ans = mid
                high = mid - 1
            else:
                low = mid + 1
        return ans