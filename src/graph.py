# name: Graph
# prefix: graph
# ---
# https://github.com/manuo-git/python-lib/blob/main/src/graph.py
import heapq
MEMORY_CAP: int = 130000
class Graph:
    shift: int
    mask: int
    _n: int
    _E: list[list[int]]
    _max_cost: int
    _dist: list[int]
    _vis: list[int]
    _bf: list[int]
    _last_start: int
    def __init__(self, n: int):
        self.shift = (n-1).bit_length()
        self.mask = (1<<self.shift)-1
        self._n = n
        self._E = [[] for _ in range(self._n)]
        self._max_cost = 0
    
    def _init_data(self) -> None:
        self._dist = [INF]*self._n
        self._vis = [0]*self._n
        self._bf = [-1]*self._n
    
    def add_edge(self, u: int, v: int, c: int = 1) -> None:
        assert 0 <= u < self._n
        assert 0 <= v < self._n
        assert 0 <= c
        if self._max_cost < c: self._max_cost = c
        self._E[u].append(c<<self.shift | v)

    def calc_dist(self, start: int) -> None:
        border = MEMORY_CAP//self._n
        if self._max_cost <= 1:
            self.bfs01(start)
        elif self._max_cost <= border:
            self.dials_algorithm(start)
        else:
            self.dijkstra(start)

    def dijkstra(self, start: int) -> None:
        assert 0 <= start < self._n
        self._init_data()
        self._dist[start] = 0
        self._last_start = start
        q = [start]
        while q:
            ni = heapq.heappop(q)
            cost, i = ni >> self.shift, ni & self.mask
            if self._vis[i]: continue
            self._vis[i] = 1
            for nj in self._E[i]:
                c, j = nj >> self.shift, nj & self.mask
                tc = cost+c
                if self._vis[j]: continue
                if self._dist[j] <= tc: continue
                self._dist[j] = tc
                self._bf[j] = i
                heapq.heappush(q, tc<<self.shift | j)
    
    def dials_algorithm(self, start: int, next_func) -> None:
        n = self._n
        S = self._max_cost+1
        self._init_data()
        dist = self._dist
        vis = self._vis
        bf = self._bf
        B = [-1] * S
        prv = [-1] * n
        nxt = [-1] * n
        slot = [0] * n
        dist[start] = 0
        B[0] = start
        self._last_start = start
        pending = 1
        w = 0
        b = 0
        while pending:
            i = B[b]
            if i == -1:
                w += 1
                b += 1
                if b == S: b = 0
                continue
            ni = nxt[i]
            B[b] = ni
            if ni != -1: prv[ni] = -1
            prv[i] = -1
            nxt[i] = -1
            pending -= 1
            vis[i] = 1
            for nj in self._E[i]:
                c, j = nj >> self.shift, nj & self.mask
                nd = w + c
                d = dist[j]
                if nd >= d: continue
                if d != INF:
                    ob = slot[j]
                    p = prv[j]
                    q = nxt[j]
                    if p != -1: nxt[p] = q
                    else: B[ob] = q
                    if q != -1: prv[q] = p
                else:
                    pending += 1
                dist[j] = nd
                bf[j] = i
                nb = b + c
                if nb >= S: nb -= S
                slot[j] = nb
                h = B[nb]
                prv[j] = -1
                nxt[j] = h
                if h != -1: prv[h] = j
                B[nb] = j
    
    def bfs01(self, start: int) -> None:
        assert 0 <= start < self._n
        self._init_data()
        dist = self._dist
        vis = self._vis
        E = self._E
        bf = self._bf
        shift = self.shift
        mask = self.mask

        dist[start] = 0
        self._last_start = start
        cur = [start]
        nxt = []
        d = 0
        while cur:
            while cur:
                i = cur.pop()
                if vis[i] or dist[i] != d: continue
                vis[i] = 1
                for nj in E[i]:
                    c, j = nj >> shift, nj & mask
                    if vis[j]: continue
                    if d+c >= dist[j]: continue
                    dist[j] = d+c
                    bf[j] = i
                    if c == 0: cur.append(j)
                    else: nxt.append(j)
            cur, nxt = nxt, cur
            d += 1

    def dist(self, goal: int) -> int:
        return self._dist[goal]

    def vis(self, goal: int) -> int:
        return self._vis[goal]
    
    def path_to(self, goal: int) -> list[int]:
        assert 0 <= goal < self._n
        if self._vis[goal] == 0: return []
        cur = goal
        ret = [cur]
        while cur != self._last_start:
            cur = self._bf[cur]
            ret.append(cur)
        ret.reverse()
        return ret