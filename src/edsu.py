# name: Edge DSU
# prefix: edsu
# ---
from atcoder.dsu import DSU
class EDSU(DSU):
    _edge_sum: list[int]

    def __init__(self, n: int = 0):
        super().__init__(n)
        self._edge_sum = [0]*n
    
    def merge(self, a: int, b: int) -> int:
        _edge_sum = -1
        if not self.same(a, b):
            _edge_sum = self._edge_sum[self.leader(a)] + self._edge_sum[self.leader(b)]
        else:
            _edge_sum = self._edge_sum[self.leader(a)]
        x = super().merge(a, b)
        if _edge_sum >= 0:
            self._edge_sum[self.leader(a)] = _edge_sum + 1
        return x

    def edge_sum(self, a: int) -> int:
        p = self.leader(a)
        return self._edge_sum[p]