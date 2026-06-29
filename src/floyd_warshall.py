# name: Floyd-Warshall
# prefix: floydwarshall
# ---
class FloydWarshall:
    INF = 1<<60
    _n: int
    _dp: list[int]
    _pathcnt: list[int]
    _is_init_calc: bool
    
    def __init__(self, n: int):
        self._n = n
        self._dp = [FloydWarshall.INF] * (n*n)
        self._pathcnt = [0] * (n*n)
        self._is_init_calc = False

        for i in range(self._n): self._dp[i*self._n + i] = 0

    def add_edge(self, u: int, v: int, c: int, update: bool = False):
        assert 0 <= u < self._n
        assert 0 <= v < self._n
        assert 0 <= c

        self._add_edge(u, v, c, update)
        
    def _add_edge(self, u: int, v: int, c: int, update: bool = False):
        if update:
            assert self._is_init_calc

            for i in range(self._n):
                for j in range(self._n):
                    nc = self._dp[i*self._n + u] + c + self._dp[v*self._n + j]
                    if self._dp[i*self._n + j] > nc:
                        self._dp[i*self._n + j] = nc
                        self._pathcnt[i*self._n + j] = 1
                    elif self._dp[i*self._n + j] == nc and nc != 0:
                        self._pathcnt[i*self._n + j] += 1
        else:
            if self._dp[u*self._n + v] > c:
                self._dp[u*self._n + v] = c
                self._pathcnt[u*self._n + v] = 1
            elif self._dp[u*self._n + v] == c and c != 0:
                self._pathcnt[u*self._n + v] += 1

    def init_calc(self): # O(N^3)
        self._is_init_calc = True

        for k in range(self._n):
            for i in range(self._n):
                for j in range(self._n):
                    if k == i or k == j: continue
                    nc = self._dp[i*self._n + k] + self._dp[k*self._n + j]
                    if self._dp[i*self._n + j] > nc:
                        self._dp[i*self._n + j] = nc
                        self._pathcnt[i*self._n + j] = 1
                    elif self._dp[i*self._n + j] == nc and nc != 0:
                        self._pathcnt[i*self._n + j] += 1
    
    def cost(self, i: int, j: int, default: int = None) -> int:
        assert 0 <= i < self._n
        assert 0 <= j < self._n
        assert self._is_init_calc

        if self._dp[i*self._n + j] == FloydWarshall.INF and default != None:
            return default
        else:
            return self._dp[i*self._n + j]
    def pathcnt(self, i: int, j: int) -> int:
        assert 0 <= i < self._n
        assert 0 <= j < self._n
        assert self._is_init_calc

        return self._pathcnt[i*self._n + j]