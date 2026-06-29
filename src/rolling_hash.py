# name: Rolling Hash
# prefix: rollinghash
# ---
class FenwickTreeMOD():
    mod: int
    def __init__(self, n: int, mod: int) -> None:
        self._n = n
        self.data = [0] * n
        self.mod = mod

    def add(self, p: int, x: int) -> None:
        assert 0 <= p < self._n
        x %= self.mod
        p += 1
        while p <= self._n:
            self.data[p-1] += x
            if self.data[p-1] >= self.mod: self.data[p-1] -= self.mod
            p += p & -p

    def sum(self, left: int, right: int) -> int:
        assert 0 <= left <= right <= self._n
        return self._sum(right) - self._sum(left)
    
    def get(self, p: int) -> int:
        return self.sum(p, p+1)
    
    def set(self, p: int, x: int) -> None:
        self.add(p, x-self.get(p))

    def _sum(self, r: int) -> int:
        s = 0
        while r > 0:
            s += self.data[r-1]
            if s >= self.mod: s -= self.mod
            r -= r & -r
        return s

MOD = (1<<61)-1
import random
rand_seed = random.randint(2, MOD-2)
class RollingHash:
    _MASK30 = (1<<30)-1
    _MASK31 = (1<<31)-1
    _MASK61 = MOD

    def __init__(self, st: str, reverse: bool = False):
        if reverse: st = st[::-1]
        self._rev = reverse
        self._st = [self._to_num(c) for c in st]
        self._n = len(st)
        self._li = []
        self._cum = [0]
        self._powr = [1]
        self._rpow = [1]
        self._change = False
        invr = pow(rand_seed, -1, MOD)
        for c in self._st:
            value = self._mul(c, self._powr[-1])
            self._li.append(value)
            self._cum.append(self._add(self._cum[-1], value))
            self._powr.append(self._mul(self._powr[-1],rand_seed))
            self._rpow.append(self._mul(self._rpow[-1],invr))

    @staticmethod
    def _to_num(element):
        return ord(element)-96

    @staticmethod
    def _op(a, b): 
        if a+b >= MOD: return a+b-MOD
        else: return a+b

    # https://qiita.com/keymoon/items/11fac5627672a6d6a9f6
    @staticmethod
    def _mul(a, b):
        au = a >> 31
        ad = a & RollingHash._MASK31
        bu = b >> 31
        bd = b & RollingHash._MASK31
        mid = ad * bu + au * bd
        midu = mid >> 30
        midd = mid & RollingHash._MASK30
        return RollingHash._calc_mod(au * bu * 2 + midu + (midd << 31) + ad * bd)
    
    @staticmethod
    def _calc_mod(x):
        xu = x >> 61
        xd = x & RollingHash._MASK61
        return RollingHash._add(xu, xd)
    
    @staticmethod
    def _sub(a, b):
        if a >= b: return a-b
        return MOD+a-b
    
    @staticmethod
    def _add(a, b):
        ret = a+b
        if ret >= MOD: return ret-MOD
        return ret

    def set(self, p: int, c: str):
        assert 0 <= p < self._n
        if self._rev: p = self._n-p-1
        if self._change == False:
            self._S = FenwickTreeMOD(self._n, MOD)
            for i in range(self._n): self._S.add(i, self._li[i])
            self._change = True
        self._S.add(p, self._mul(self._sub(self._to_num(c), self._st[p]),self._powr[p]))
        self._st[p] = self._to_num(c)
    
    # [l, r)
    def value(self, l: int, r: int):
        if self._rev: l, r = self._n-r, self._n-l
        if l == r == self._n: return 0
        assert 0 <= l <= r <= self._n
        if self._change:
            ret = self._mul(self._S.sum(l, r), self._rpow[l])
        else:
            ret = self._mul(self._sub(self._cum[r], self._cum[l]), self._rpow[l])
        return ret