# name: Mo's Algorithm on Tree
# prefix: mo_tree
# ---
class MinSparseTable: # 中身はDisjointSparseTable。セグ木に乗るものなら何でも乗る。
    n: int
    log: int
    data: list[int]
    e: int

    def __init__(self, e: int, v: list[int]):
        self.n = len(v)
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
                        res = min(v[i], res)
                        self.data[offset+i] = res
                
                if mid < self.n:
                    res = v[mid]
                    self.data[offset+mid] = res
                    for i in range(mid+1, min(self.n, mid+mid_step)):
                        res = min(res, v[i])
                        self.data[offset+i] = res

    def prod(self, l: int, r: int):
        if l == r: return self.e
        r -= 1
        if l == r: return self.data[l]
        k = (l ^ r).bit_length() - 1
        offset = k * self.n
        return min(self.data[offset+l], self.data[offset+r])

class MoTreeSolver:
    n: int
    log: int
    mask: int
    q: int
    is_build: bool
    qs: list[tuple[int, int, int, int]]
    E: list[list[int]]
    IN: list[int]
    V: list[int]

    table: MinSparseTable

    def __init__(self, n: int):
        self.n = n
        self.log = (n-1).bit_length()
        self.mask = (1<<self.log)-1
        self.q = 0
        self.qs = []
        self.is_build = False
        self.E = [[] for _ in range(self.n)]
        self.IN = [-1]*n
        self.V = [0]*2*n

    def add_edge(self, u: int, v: int):
        assert 0 <= u < self.n
        assert 0 <= v < self.n
        self.E[u].append(v)
        self.E[v].append(u)

    def _code(self, x, i): return x<<self.log | i
    def _decode(self, e): return e>>self.log, e&self.mask

    def build(self, root: int = 0):
        self.is_build = True
        q = [(1, root, -1), (0, root, -1)]
        dat = [0]*(2*self.n)
        d = -1
        cur = 0
        while q:
            t, i, p = q.pop()
            self.V[cur] = i
            if t == 0:
                d += 1
                self.IN[i] = cur
                for j in self.E[i]:
                    if j == p: continue
                    q.append((1, j, i))
                    q.append((0, j, i))
                dat[cur] = self._code(d, i)
            else:
                d -= 1
                dat[cur] = self._code(d, p)
            cur += 1
        self.table = MinSparseTable(self._code(1<<self.log+1, 0), dat)

    def _prod(self, u, v):
        l, r = self.IN[u], self.IN[v]
        if l > r: l, r = r, l
        return self.table.prod(l, r+1)

    def lca(self, u, v):
        return self._decode(self._prod(u, v))[1]

    def add_path_query(self, u: int, v: int):
        assert 0 <= u < self.n
        assert 0 <= v < self.n
        assert self.is_build
        a = self.IN[u]
        b = self.IN[v]
        if a <= b:
            l, r = a+1, b+1
        else:
            l, r = b+1, a+1
        self.qs.append((l, r, self.q, self.lca(u, v)))
        self.q += 1

    def solve(self, add, erase, answer):
        b = int((self.n+self.n) / (self.q**0.5)) + 1
        self.qs.sort(key=lambda x: (x[0] // b, x[1] if (x[0] // b) % 2 == 0 else -x[1]))
        parity = [0]*self.n

        ans = [0]*self.q
        cur_l, cur_r = 0, 0
        for l, r, idx, lca in self.qs:
            while cur_l > l: # [l, r) -> [l-1, r)
                cur_l -= 1
                i = self.V[cur_l]
                parity[i] ^= 1
                if parity[i]:
                    add(i)
                else:
                    erase(i)
            while cur_r < r: # [l, r) -> [l, r+1)
                i = self.V[cur_r]
                parity[i] ^= 1
                if parity[i]:
                    add(i)
                else:
                    erase(i)
                cur_r += 1
            while cur_l < l: # [l, r) -> [l+1, r)
                i = self.V[cur_l]
                parity[i] ^= 1
                if parity[i]:
                    add(i)
                else:
                    erase(i)
                cur_l += 1
            while cur_r > r: # [l, r) -> [l, r-1)
                cur_r -= 1
                i = self.V[cur_r]
                parity[i] ^= 1
                if parity[i]:
                    add(i)
                else:
                    erase(i)
            add(lca)
            ans[idx] = answer(idx)
            erase(lca)
        return ans
"""
1. 宣言
Mo = MoTreeSolver(N)

2. 木の辺追加
Mo.add_edge(u, v)

3. 木をビルドする
Mo.build

4. パスクエリを登録する
Mo.add_path_query(u, v)

5. add(i)
頂点iを追加する時の操作

6. erase(i)
頂点iを削除する時の操作

7. answer(qi)
クエリqiの答えを返す

8. solveを呼ぶ
ans = Mo.solve(add, erase, answer)
"""

# def add(i):
# def erase(i):
# def answer(qi):