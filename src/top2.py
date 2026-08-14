# name: Top2
# prefix: top2
# ---
NEG_INF = -(1<<60)
class Top2:
    mx1: int
    mx2: int
    multi: bool
    def __init__(self, multi: bool = True):
        self.mx1 = NEG_INF
        self.mx2 = NEG_INF
        self.multi = multi
    
    def insert(self, x: int):
        if not self.multi and (self.mx1 == x or self.mx2 == x): return
        if self.mx1 < x:
            self.mx2 = self.mx1
            self.mx1 = x
        elif self.mx2 < x:
            self.mx2 = x
    
    def __getitem__(self, i: int):
        assert 0 <= i <= 1
        if i == 0: return self.mx1
        if i == 1: return self.mx2

    def __iter__(self):
        if self.mx1 != NEG_INF: yield self.mx1
        if self.mx2 != NEG_INF: yield self.mx2
    
    def __len__(self):
        if self.mx1 == NEG_INF: return 0
        if self.mx2 == NEG_INF: return 1
        return 2
    
    def __repr__(self):
        vals = [str(x) if x != NEG_INF else "-INF" for x in [self.mx1, self.mx2]]
        return f"Top2({', '.join(vals)})"
    
    def _update(self, other):
        if other.mx1 > self.mx2: self.insert(other.mx1)
        if other.mx2 > self.mx2: self.insert(other.mx2)
    
    def __add__(self, other):
        res = Top2(self.multi)
        res.mx1 = self.mx1
        res.mx2 = self.mx2
        res._update(other)
        return res
"""
# 重複を許す場合
a = Top2()
a.insert(5) # 5, -INF
a.insert(3) # 5, 3
a.insert(2) # 5, 3
a.insert(4) # 5, 4
a.insert(5) # 5, 5
a.insert(6) # 6, 5
# 重複を許さない場合
b = Top2(False)
a.insert(5) # 5, -INF
a.insert(3) # 5, 3
a.insert(2) # 5, 3
a.insert(4) # 5, 4
a.insert(5) # 5, 4 <-
a.insert(6) # 6, 5
"""