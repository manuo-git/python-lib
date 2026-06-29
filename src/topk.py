# name: TopK
# prefix: topk
# ---
class TopK:
    mx: list[int]
    k: int
    def __init__(self, k):
        self.mx = []
        self.k = k
    
    def insert(self, x: int):
        if len(self.mx) == self.k and x <= self.mx[-1]: return
        
        l, r = 0, len(self.mx)
        while l < r:
            mid = (l+r)//2
            if x > self.mx[mid]: r = mid
            else: l = mid + 1
        
        self.mx.insert(l, x)
        if len(self.mx) > self.k: self.mx.pop()
        
    def __getitem__(self, i: int):
        assert -len(self.mx) <= i < len(self.mx)
        return self.mx[i]
    
    def __iter__(self):
        return iter(self.mx)
    
    def __len__(self):
        return len(self.mx)
    
    def __repr__(self):
        vals = list(map(str, self.mx))+["-INF"]*(self.k-len(self.mx))
        return f"Top{self.k}({', '.join(vals)})"
    
    def update(self, other):
        for x in other.mx: self.insert(x)
    
    def __add__(self, other):
        res = TopK(k=self.k)
        res.mx = self.mx[:]
        res.update(other)
        return res