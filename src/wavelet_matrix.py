# name: Wavelet Matrix
# prefix: wavelet matrix
# ---
class WaveletMatrix:
    _log: int
    _n: int
    _dat: list[list[int]]
    _cum: list[list[int]]
    def __init__(self, _v: list[int], _log: int = 30):
        v = _v[:]
        self._log = _log

        self._n = len(v)
        self._dat = [[] for _ in range(self._log)]
        self._cum = [[] for _ in range(self._log)]
        for k in reversed(range(self._log)):
            dir = [0]*self._n
            left = []
            right = []
            for i in range(self._n):
                dir[i] = v[i]>>k&1
                if dir[i] == 0:
                    left.append(v[i])
                else:
                    right.append(v[i])
            v = left + right
            self._dat[k] = [0]*(self._n+1)
            self._cum[k] = [0]*(self._n+1)
            for i in range(self._n):
                self._dat[k][i+1] = self._dat[k][i] + dir[i]
                self._cum[k][i+1] = self._cum[k][i] + v[i]
    
    def _subtree_range(self, h: int, l: int, r: int):
        a0 = l - self._dat[h][l]
        a1 = self._dat[h][l]
        b0 = r - self._dat[h][r]
        b1 = self._dat[h][r]
        c0 = self._n - self._dat[h][self._n]
        return a0, b0, c0+a1, c0+b1
    
    def _kth_smallest_nrec(self, h: int, l: int, r: int, k: int, xor: int = 0):
        res = 0
        while h > 0:
            l0, r0, l1, r1 = self._subtree_range(h-1, l, r)
            if xor>>(h-1)&1:
                l0, r0, l1, r1 = l1, r1, l0, r0
            left_size = r0 - l0
            if k < left_size:
                l, r = l0, r0
            else:
                res += 1<<(h-1)
                l, r = l1, r1
                k -= left_size
            h -= 1
        return res

    def _count_lt_nrec(self, h: int, l: int, r: int, x: int):
        res = 0
        while h > 0:
            l0, r0, l1, r1 = self._subtree_range(h-1, l, r)
            if x>>(h-1)&1:
                res += r0-l0
                l, r = l1, r1
            else:
                l, r = l0, r0
            h -= 1
        return res
        
    def _sum_lt_nrec(self, h: int, l: int, r: int, x: int):
        res = 0
        while h > 0:
            l0, r0, l1, r1 = self._subtree_range(h-1, l, r)
            if x>>(h-1)&1:
                res += self._cum[h-1][r0]-self._cum[h-1][l0]
                l, r = l1, r1
            else:
                l, r = l0, r0
            h -= 1
        return res

    def kth_smallest(self, l: int, r: int, k: int, xor: int = 0):
        assert 0 <= l < r <= self._n and 1 <= k <= r-l
        return self._kth_smallest_nrec(self._log, l, r, k-1, xor)
    
    def kth_biggest(self, l: int, r: int, k: int, xor: int = 0):
        assert 0 <= l < r <= self._n and 1 <= k <= r-l
        return self._kth_smallest_nrec(self._log, l, r, r-l-k, xor)

    def count_lt(self, l: int, r: int, x: int): # [l, r), [0, x)
        assert 0 <= l < r <= self._n and 0 <= x <= (1<<self._log)
        return self._count_lt_nrec(self._log, l, r, x)
    
    def count_range(self, l: int, r: int, a: int, b: int): # [l, r), [a, b)
        assert 0 <= l < r <= self._n and 0 <= a < b <= (1<<self._log)
        return self._count_lt_nrec(self._log, l, r, b) - self._count_lt_nrec(self._log, l, r, a)
    
    def sum_lt(self, l: int, r: int, x: int): # [l, r), [0, x)
        assert 0 <= l < r <= self._n and 0 <= x <= (1<<self._log)
        return self._sum_lt_nrec(self._log, l, r, x)
    
    def sum_range(self, l: int, r: int, a: int, b: int): # [l, r), [a, b)
        assert 0 <= l < r <= self._n and 0 <= a < b <= (1<<self._log)
        return self._sum_lt_nrec(self._log, l, r, b) - self._sum_lt_nrec(self._log, l, r, a)
"""
種類数
* 直前の同じ数字のindexを1_indexedで求める。初登場なら0。
* [l, r)の範囲内の、直前のindexが[0, l+1)の要素は範囲内に初登場。
P = [0]*N
prev = {}
for i in range(N):
    P[i] = prev.get(A[i], 0)
    prev[A[i]] = i+1
W = WaveletMatrix(P)
print(W.count_lt(l, r, l+1))
"""