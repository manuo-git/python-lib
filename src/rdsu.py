# name: Rollback DSU
# prefix: rdsu
# ---
from atcoder.dsu import DSU
class RollbackDSU(DSU):
    def __init__(self, n: int = 0) -> None:
        super().__init__(n)
        self._history: list[tuple[int, int]] = []
        self._snapshots: list[int] = [0]

    def leader(self, a: int) -> int:
        assert 0 <= a < self._n
        while self.parent_or_size[a] >= 0:
            a = self.parent_or_size[a]
        return a

    def merge(self, a: int, b: int) -> int:
        assert 0 <= a < self._n
        assert 0 <= b < self._n

        x = self.leader(a)
        y = self.leader(b)

        if x == y: return x

        if -self.parent_or_size[x] < -self.parent_or_size[y]:
            x, y = y, x

        self._history.append((x, self.parent_or_size[x]))
        self._history.append((y, self.parent_or_size[y]))

        self.parent_or_size[x] += self.parent_or_size[y]
        self.parent_or_size[y] = x

        return x

    def snapshot(self) -> None:
        self._snapshots.append(len(self._history))

    def rollback(self) -> bool:
        if len(self._snapshots) <= 1: 
            target_len = self._snapshots[0]
        else:
            target_len = self._snapshots.pop()
        while len(self._history) > target_len:
            idx, val = self._history.pop()
            self.parent_or_size[idx] = val
        return True