# name: Potential DSU
# prefix: pdsu
# ---
from typing import *
from atcoder.dsu import DSU
class PDSU(DSU):
    _diff_weight: list[Any]

    def __init__(self,
                 n: int,
                 op = lambda a, b: a+b,
                 rev = lambda a: -a,
                 e = 0
                 ) -> None:
        super().__init__(n)
        self.op = op
        self.rev = rev
        self.e = e
        self._diff_weight = [e] * n

    # weight(b) - weight(a) = w
    def merge(self, a: int, b: int, w) -> int:
        assert 0 <= a < self._n
        assert 0 <= b < self._n

        w = self.op(self.op(w, self.weight(a)), self.rev(self.weight(b)))

        x = self.leader(a)
        y = self.leader(b)

        if x == y:
            return x

        if -self.parent_or_size[x] < -self.parent_or_size[y]:
            x, y = y, x
            w = self.rev(w)

        self.parent_or_size[x] += self.parent_or_size[y]
        self.parent_or_size[y] = x
        self._diff_weight[y] = w

        return x

    def _leader_weight(self, a: int) -> int:
        assert 0 <= a < self._n

        parent = self.parent_or_size[a]
        weight = self.e
        while parent >= 0:
            if self.parent_or_size[parent] < 0:
                weight = self.op(weight, self._diff_weight[a])
                a = parent
                break
            new_weight = self.op(self._diff_weight[a], self._diff_weight[parent])
            before_a = a
            self.parent_or_size[a], a, parent = (
                self.parent_or_size[parent],
                self.parent_or_size[parent],
                self.parent_or_size[self.parent_or_size[parent]]
            )
            self._diff_weight[before_a] = new_weight
            weight = self.op(weight, new_weight)

        return a, weight

    def leader(self, a: int) -> int:
        p, _ = self._leader_weight(a)
        return p
    
    def weight(self, a: int):
        _, w = self._leader_weight(a)
        return w
    
    def diff(self, a: int, b: int):
        return self.op(self.weight(b), self.rev(self.weight(a)))