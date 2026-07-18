# name: Re Rooting DP
# prefix: rerooting
# ---
class ReRooting[T, F, G]:
    _n: int
    _E: list[list[int]]
    _op: F # op(T, T) -> T
    _e: T  # op(_e, *) = *
    _up: G # op(T, i) -> T
    _dp: list[list[T]]
    def __init__(self, n: int, op: F, e: T, up: G):
        self._n = n
        self._E = [[] for _ in range(self._n)]
        self._op = op
        self._e = e
        self._up = up
        self._dp = [[] for _ in range(self._n)]
    
    def add_edge(self, u: int, v:int):
        self._E[u].append(v)
        self._E[v].append(u)

    def _dfs(self, i: int, p: int) -> T:
        assert 0 <= i < self._n
        res = self._e
        self._dp[i] = [self._e]*len(self._E[i])
        for e, j in enumerate(self._E[i]):
            if j == p: continue
            assert 0 <= e < len(self._dp[i])
            self._dp[i][e] = self._dfs(j, i)
            res = self._op(res, self._dp[i][e])
        return self._up(res, i)
    
    def _dfsdp(self, i: int, p: int, pval: T) -> None:
        for e, j in enumerate(self._E[i]):
            if j == p: self._dp[i][e] = pval

        size = len(self._E[i])
        left: list[T] = [self._e]*(size+1)
        right: list[T] = [self._e]*(size+1)
        for e in range(size):
            left[e+1] = self._op(left[e], self._dp[i][e])
            right[e+1] = self._op(right[e], self._dp[i][size-e-1])
        for e, j in enumerate(self._E[i]):
            if j == p: continue
            ival = self._up(self._op(left[e], right[size-e-1]), i)
            self._dfsdp(j, i, ival)

    def calc(self):
        self._dfs(0, -1)
        self._dfsdp(0, -1, self._e)

    def __getitem__(self, i: int):
        assert 0 <= i < self._n
        res = self._e
        for j in range(len(self._E[i])):
            res = self._op(res, self._dp[i][j])
        return self._up(res, i)
    
# def dfs(p, i):
#     res = e
#     for j in E[i]:
#         if j == p: continue
#         res = op(res, dfs(i, j))
#     return up(res, i)