# name: LCA O(1)
# prefix: lca_fast
# ---
class SparseTable: # 中身はDisjointSparseTable。セグ木に乗るものなら何でも乗る。
    def __init__(self, op, e, v):
        self.n = len(v)
        self.op = op
        self.e = e
        self.log = 1 if self.n <= 1 else (self.n - 1).bit_length()
        
        self.data = [e] * (self.log * self.n)
        for k in range(self.log):
            offset = k * self.n
            mid_step = 1 << k
            for mid in range(mid_step, self.n + mid_step, mid_step*2):
                if mid <= self.n:
                    res = v[mid-1]
                    self.data[offset+mid-1] = res
                    for i in range(mid-2, max(-1, mid-mid_step-1), -1):
                        res = self.op(v[i], res)
                        self.data[offset+i] = res
                
                if mid < self.n:
                    res = v[mid]
                    self.data[offset+mid] = res
                    for i in range(mid+1, min(self.n, mid+mid_step)):
                        res = self.op(res, v[i])
                        self.data[offset+i] = res

    def prod(self, l: int, r: int):
        if l == r: return self.e
        r -= 1
        if l == r: return self.data[l]
        k = (l ^ r).bit_length() - 1
        offset = k * self.n
        return self.op(self.data[offset+l], self.data[offset+r])
    
    def max_right(self, left: int, f):
        l, r = left, self.n+1
        while r-l>1:
            m = (l+r)//2
            if f(self.prod(left, m)): l = m
            else: r = m
        return l
    
    def min_left(self, right: int, f):
        l, r = -1, right
        while r-l>1:
            m = (l+r)//2
            if f(self.prod(m, right)): r = m
            else: l = m
        return r

class LCA:
    def __init__(self, n: int):
        self.n = n
        self.log = (n-1).bit_length()
        self.edges = [[] for _ in range(self.n)]
    
    def add_edge(self, u: int, v: int, w: int = 1):
        assert 0 <= u < self.n
        assert 0 <= v < self.n
        self.edges[u].append((v, w))
        self.edges[v].append((u, w))

    def build(self, root: int = 0):
        self.mask = (1<<self.log)-1
        self.depth = [0]*self.n
        self.depth_dist = [0]*self.n
        li = []
        self.first = [-1]*self.n
        self.m = 2*self.n-1
        dat = [0]*self.m
        q = [(-1, root, 0, 0)]
        d = -1
        dist = 0
        idx = 0
        while q:
            p, i, t, w = q.pop()
            li.append(i)
            if t == 0:
                d += 1
                dist += w
                self.depth[i] = d
                self.depth_dist[i] = dist
                self.first[i] = idx
                for j, w in self.edges[i]:
                    if j == p: continue
                    q.append((-1, i, 1, w))
                    q.append((i, j, 0, w))
            else:
                d -= 1
                dist -= w
            dat[idx] = self._code(d, i)
            idx += 1
        self.table = SparseTable(lambda a,b: min(a,b), self._code(1<<self.log+1, 0), dat)
    
    def _code(self, x, i): return x<<self.log | i
    def _decode(self, e): return e>>self.log, e&self.mask

    def _prod(self, u, v):
        l, r = self.first[u], self.first[v]
        if l > r: l, r = r, l
        return self.table.prod(l, r+1)

    def _lca_depth(self, u, v):
        return self._decode(self._prod(u, v))[0]
    
    def _lca_depth_dist(self, u, v):
        lca = self._decode(self._prod(u, v))[1]
        return self.depth_dist[lca]
    
    def lca(self, u, v):
        return self._decode(self._prod(u, v))[1]
    
    def edge_count(self, u, v):
        return self.depth[u]+self.depth[v] - 2*self._lca_depth(u, v)
    
    def dist(self, u, v):
        return self.depth_dist[u]+self.depth_dist[v] - 2*self._lca_depth_dist(u, v)