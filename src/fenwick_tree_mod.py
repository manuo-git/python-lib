# name: Fenwick Tree MOD
# prefix: fenwicktreemod
# ---
class FenwickTreeMOD(FenwickTree):
    mod: int
    def __init__(self, n: int = 0, mod: int = 0) -> None:
        super().__init__(n)
        self.mod = mod

    def add(self, p: int, x: int) -> None:
        assert 0 <= p < self._n

        p += 1
        while p <= self._n:
            self.data[p - 1] += x
            if self.mod > 0:
                self.data[p - 1] %= self.mod
            p += p & -p

    def _sum(self, r: int) -> int:
        s = 0
        while r > 0:
            s += self.data[r - 1]
            if self.mod > 0:
                s %= self.mod
            r -= r & -r

        return s