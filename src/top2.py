# name: Top2
# prefix: top2
# ---
from typing import ClassVar
class Top2:
    NEG_INF: ClassVar[int] = -(1<<60)
    mx1: int
    mx2: int
    def __init__(self):
        self.mx1 = Top2.NEG_INF
        self.mx2 = Top2.NEG_INF
    
    def insert(self, x: int):
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
        if self.mx1 != Top2.NEG_INF: yield self.mx1
        if self.mx2 != Top2.NEG_INF: yield self.mx2
    
    def __len__(self):
        if self.mx1 == Top2.NEG_INF: return 0
        if self.mx2 == Top2.NEG_INF: return 1
        return 2
    
    def __repr__(self):
        vals = [str(x) if x != Top2.NEG_INF else "-INF" for x in [self.mx1, self.mx2]]
        return f"Top2({', '.join(vals)})"
    
    def update(self, other):
        if other.mx1 > self.mx2: self.insert(other.mx1)
        if other.mx2 > self.mx2: self.insert(other.mx2)
    
    def __add__(self, other):
        res = Top2()
        res.mx1 = self.mx1
        res.mx2 = self.mx2
        res.update(other)
        return res