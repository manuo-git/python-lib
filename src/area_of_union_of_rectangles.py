# name: Area of Union of Rectangles
# prefix: area of union of rectangles
# ---
# https://atcoder.jp/contests/abc449/submissions/74125516
class UnionOfLines:
    def __init__(self,n, width=None):
        self._n = n
        self.data = [0]*(2*n)
        self.lazy = [0]*(2*n)
        if width is None:
            width = [1]*n
        self.total = sum(width)
        assert n == len(width)
        self.data[self._n:2*self._n] = width
        for k in range(self._n-1,0,-1):
            self.data[k] = self.data[2*k] + self.data[2*k+1]

    def _update_above(self,k):
        while k >= 2:
            k >>= 1
            self.data[k] = (0 if self.lazy[2*k] else self.data[2*k]) + (0 if self.lazy[2*k+1] else self.data[2*k+1])
    
    def _visualize_binarytree(self,lst):
        def str_modify(x):
            return "INF" if type(x)==int and x >= 10**18+1 else str(x)
        
        A = list(map(str_modify,lst))+["*"]*(2**((len(lst)-1).bit_length()) - len(lst))
        N = len(A)
        spacestring = [" "*len(A[N//(i&-i)//2 + i//(i&-i)//2]) for i in range(1,N)]
    
        res = []
        for base in (2**i for i in range(N.bit_length()-1)):
            r = spacestring[:]
            for j,v in enumerate(A[base:2*base]):
                r[N//base//2-1+j*N//base] = v
            res.append("".join(r))
        return "\n".join(res)

    def __str__(self):
        res = []
        s = self._visualize_binarytree(self.lazy).split("\n")
        t = self._visualize_binarytree(self.data).split("\n")
        for i,j in zip(s,t):
            res.append(i + " | " + j)
        return "\n".join(res)
 
    def all_prod(self):
        return self.total - (0 if self.lazy[1] else self.data[1])
 
    def apply(self, l, r, f):
        if l == r: return
        l += self._n
        r += self._n
        L,R = l//(l&-l), r//(r&-r)
        while l < r:
            if l & 1: 
                self.lazy[l] += f
                l += 1
            if r & 1:
                r -= 1
                self.lazy[r] += f
            l >>= 1
            r >>= 1
        self._update_above(L)
        self._update_above(R-1)

class AreaUnionRect:
    shift = 31
    mask = (1<<31)-1
    def __init__(self, H, W):
        assert 0 <= H <= AreaUnionRect.mask
        assert 0 <= W <= AreaUnionRect.mask
        self.size = H*W
        self.X = [0, W]
        self.Y = [0, H]
        self.ABCD = []
    
    def add_rect(self, r1, c1, r2, c2): # [r1, r2), [c1, c2)
        self.X.append(c1)
        self.X.append(c2)
        self.Y.append(r1)
        self.Y.append(r2)
        self.ABCD.append((r1, c1, r2, c2))

    @staticmethod
    def _code(x, cnt): return x<<AreaUnionRect.shift | cnt
    @staticmethod
    def _decode(e): return e>>AreaUnionRect.shift, e&AreaUnionRect.mask

    def calc(self, white: bool = False):
        X = sorted(list(set(self.X)))
        Y = sorted(list(set(self.Y)))
        posx = {x: e for e, x in enumerate(X)}
        posy = {x: e for e, x in enumerate(Y)}
        M = len(X)
        K = len(Y)

        query = [[] for _ in range(M)]
        for a, b, c, d in self.ABCD:
            e = AreaUnionRect._code(posy[a], posy[c])
            query[posx[b]].append(e<<1|1)
            query[posx[d]].append(e<<1|0)
        S = UnionOfLines(K-1, [Y[i+1]-Y[i] for i in range(K-1)])
        ans = 0
        for i in range(M-1):
            for e in query[i]:
                t = 1 if e&1 else -1
                a, b = AreaUnionRect._decode(e>>1)
                S.apply(a, b, t)
            ans += (X[i+1]-X[i])*S.all_prod()
        
        return self.size - ans if white else ans