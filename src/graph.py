# name: Graph
# prefix: graph
# ---
from heapq import heappop, heappush
from collections import deque
from typing import *
class Graph:
    INF = 1<<60
    shift = 20
    mask = (1<<20)-1
    memory_cap = 130000
    _n: int
    _E: list[list[int]]
    _max_cost: int
    _dist: list[int]
    _vis: list[int]
    _bf: list[int]

    def __init__(self, n: int):
        assert n <= 1<<Graph.shift, "Please consider increasing the Graph.shift value."
        self._n = n
        self._E = [[] for _ in range(self._n)]
        self._max_cost = 0
    
    def _init_data(self) -> None:
        self._dist = [Graph.INF]*self._n
        self._vis = [0]*self._n
        self._bf = [-1]*self._n
    
    def add_edge(self, u: int, v: int, c: int = 1) -> None:
        assert 0 <= u < self._n
        assert 0 <= v < self._n
        assert 0 <= c
        if self._max_cost < c: self._max_cost = c
        self._E[u].append(c<<Graph.shift | v)
    
    def calc_dist(self, start: int) -> None:
        border = Graph.memory_cap//self._n
        if self._max_cost <= 1:
            self.bfs01(start)
        elif self._max_cost <= border:
            self.dials_algorithm(start)
        else:
            self.dijkstra(start)
        return self._dist[:]
    
    def dijkstra(self, start: int) -> List[int]:
        assert 0 <= start < self._n
        self._init_data()
        self._dist[start] = 0
        self._last_start = start
        q = [start]
        while q:
            ni = heappop(q)
            cost, i = ni >> Graph.shift, ni & Graph.mask
            if self._vis[i]: continue
            self._vis[i] = 1
            for nj in self._E[i]:
                c, j = nj >> Graph.shift, nj & Graph.mask
                tc = cost+c
                if self._vis[j]: continue
                if self._dist[j] <= tc: continue
                self._dist[j] = tc
                self._bf[j] = i
                heappush(q, tc<<Graph.shift | j)
        return self._dist
    
    # https://tjkendev.github.io/procon-library/python/graph/dial.html
    def dials_algorithm(self, start: int) -> List[int]:
        assert 0 <= start < self._n
        self._init_data()
        _m = self._n*self._max_cost
        B = [-1]*(_m + 1) # first
        L = [-1]*(_m + 1) # last

        *prv, = range(-1, self._n-1)
        *nxt, = range(1, self._n+1)

        nxt[-1] = -1
        if start < self._n-1: prv[start+1] = (start-1 if start > 0 else -1)
        if start > 0: nxt[start-1] = (start+1 if start < self._n-1 else -1)
        prv[start] = nxt[start] = -1
        B[0] = L[0] = start
        B[_m] = +(start == 0)
        L[_m] = (self._n-1 if start < self._n-1 else self._n-2)
        
        self._dist[start] = 0
        self._last_start = start
        for w in range(_m):
            i = B[w]
            while i != -1:
                self._vis[i] = 1
                for nj in self._E[i]:
                    c, j = nj >> Graph.shift, nj & Graph.mask
                    tc = w + c
                    if tc >= self._dist[j]: continue
                    d = self._dist[j]
                    if d > _m: d = _m
                    self._dist[j] = tc
                    p = prv[j]
                    n = nxt[j]
                    if p != -1: nxt[p] = n
                    else: B[d] = n
                    if n != -1: prv[n] = p
                    else: L[d] = p
                    l = L[tc]
                    if l != -1: nxt[l] = j
                    else: B[tc] = j
                    prv[j] = l
                    nxt[j] = -1
                    self._bf[j] = i
                    L[tc] = j
                i = nxt[i]
    
    def bfs01(self, start: int) -> None:
        assert 0 <= start < self._n
        self._init_data()
        self._dist[start] = 0
        self._last_start = start
        q = deque([start])
        while q:
            i = q.popleft()
            if self._vis[i]: continue
            self._vis[i] = 1
            for nj in self._E[i]:
                c, j = nj >> Graph.shift, nj & Graph.mask
                assert 0 <= c <= 1
                tc = self._dist[i]+c
                if self._vis[j]: continue
                if self._dist[j] <= tc: continue
                self._dist[j] = tc
                self._bf[j] = i
                if c == 0: q.appendleft(j)
                else: q.append(j)

    def bfs(self, start: int) -> None:
        assert 0 <= start < self._n
        self._init_data()
        self._dist[start] = 0
        self._last_start = start
        q = deque([start])
        while q:
            i = q.popleft()
            if self._vis[i]: continue
            self._vis[i] = 1
            for nj in self._E[i]:
                c, j = nj >> Graph.shift, nj & Graph.mask
                assert c == 1
                tc = self._dist[i]+c
                if self._vis[j]: continue
                if self._dist[j] <= tc: continue
                self._dist[j] = tc
                self._bf[j] = i
                q.append(j)

    def dist(self, goal: int) -> int:
        return self._dist[goal]

    def vis(self, goal: int) -> int:
        return self._vis[goal]
    
    def path_to(self, goal: int) -> Union[List[int], None]:
        assert 0 <= goal < self._n
        if self._vis[goal] == 0: return None
        cur = goal
        ret = [cur]
        while cur != self._last_start:
            cur = self._bf[cur]
            ret.append(cur)
        ret.reverse()
        return ret