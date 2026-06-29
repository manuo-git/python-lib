# name: Sparse Table
# prefix: sparsetable
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