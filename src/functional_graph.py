# name: Functional Graph
# prefix: functionalgraph
# ---
class FunctionalGraph:
    _n: int
    loop_id: int
    nxt: list[int]
    vis: list[int]
    loop: list[list[int]]
    _is_init_calc: bool
    def __init__(self, n):
        self._n = n
        self.loop_id = 1
        self.nxt = [0]*n
        self.vis = [0]*n
        self.loop = []
        self._is_init_calc = False
    
    def add_edge(self, u: int, v: int):
        assert 0 <= u < self._n
        assert 0 <= v < self._n
        self.nxt[u] = v
        if u == self.nxt[u]:
            self.vis[u] = self.loop_id
            self.loop.append([u])
            self.loop_id += 1
    
    def init_calc(self):
        for i in range(self._n):
            if self.vis[i] == 0:
                loop_memo = []
                self._dfs(i, loop_memo)
                if len(loop_memo) > 0: self.loop.append(loop_memo)
        self._is_init_calc = True
        
    def _dfs(self, u, loop_memo):
        self.vis[u] = -self.loop_id
        v = self.nxt[u]
        if self.vis[v] == -self.loop_id:
            loop_memo.append(u)
            loop_memo.append(v)
            self.vis[u] = self.loop_id
            self.vis[v] = self.loop_id
            self._make_loop(u, v, loop_memo)
            self.loop_id += 1
            return 0
        elif self.vis[v] == 0:
            res = self._dfs(v, loop_memo)
            if res == 0: return 0
            self.vis[u] = res
            return res
        ret = -self.vis[v] if self.vis[v] > 0 else self.vis[v]
        self.vis[u] = ret
        return ret

    def _make_loop(self, si, now, loop_memo):
        while self.nxt[now] != si:
            now = self.nxt[now]
            loop_memo.append(now)
            self.vis[now] = self.loop_id
    
    def make_inverse_graph(self):
        assert self._is_init_calc
        res = [[] for _ in range(self._n)]
        for i in range(self._n):
            if self.vis[i] < 0: res[self.nxt[i]].append(i)
        return res

    def make_loop_rooted_graph(self):
        assert self._is_init_calc
        res = [[] for _ in range(self._n)]
        for i in range(self._n):
            if self.vis[i] > 0: continue
            v = self.nxt[i]
            if self.vis[v] > 0:
                v = self.loop[self.vis[v]-1][0]
            res[v].append(i)
        return res
    
    def roots(self):
        assert self._is_init_calc
        return [self.loop[i][0] for i in range(self.loop_id-1)]
    
    def connected_loop_count(self, i: int):
        assert self._is_init_calc
        assert 0 <= i < self._n
        return len(self.loop[abs(self.vis[i])-1])
    def loops(self):
        return self.loop