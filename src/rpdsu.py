# name: Rollback Potential DSU
# prefix: rpdsu, prdsu
# ---
from atcoder.dsu import DSU
class RollbackPDSU(DSU):
    def __init__(self, n: int = 0, 
                 op = lambda a, b: a+b,
                 rev = lambda a: -a,
                 e = 0
                 ) -> None:
        super().__init__(n)
        self.op = op
        self.rev = rev
        self.e = e
        self._diff_weight = [e] * n
        self._history: list[tuple[int, int]] = []
        self._snapshots: list[int] = [0]

    def _leader_weight(self, a: int) -> tuple[int, int]:
        assert 0 <= a < self._n
        weight = self.e
        while self.parent_or_size[a] >= 0:
            weight = self.op(weight, self._diff_weight[a])
            a = self.parent_or_size[a]
        return a, weight

    def leader(self, a: int) -> int:
        return self._leader_weight(a)[0]
    
    def weight(self, a: int):
        return self._leader_weight(a)[1]

    def merge(self, a: int, b: int, w) -> int:
        assert 0 <= a < self._n
        assert 0 <= b < self._n

        w = self.op(self.op(w, self.weight(a)), self.rev(self.weight(b)))

        x = self.leader(a)
        y = self.leader(b)

        if x == y: return x

        if -self.parent_or_size[x] < -self.parent_or_size[y]:
            x, y = y, x
            w = self.rev(w)

        self._history.append((x, 0, self.parent_or_size[x]))
        self._history.append((y, 0, self.parent_or_size[y]))
        self._history.append((y, 1, self._diff_weight[y]))

        self.parent_or_size[x] += self.parent_or_size[y]
        self.parent_or_size[y] = x
        self._diff_weight[y] = w

        return x
    
    def diff(self, a: int, b: int):
        return self.op(self.weight(b), self.rev(self.weight(a)))

    def snapshot(self) -> None:
        self._snapshots.append(len(self._history))

    def rollback(self) -> bool:
        if len(self._snapshots) <= 1: 
            target_len = self._snapshots[0]
        else:
            target_len = self._snapshots.pop()
        while len(self._history) > target_len:
            idx, t, val = self._history.pop()
            if t == 0:
                self.parent_or_size[idx] = val
            else:
                self._diff_weight[idx] = val
        return True