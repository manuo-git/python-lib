# name: Bit Subset
# prefix: subsetbit
# ---
class subset:
    def __init__(self, bi):
        self.bi = bi
        self.si = bi
    def __iter__(self): return self
    def __next__(self):
        if self.si < 0: raise StopIteration
        self.si &= self.bi
        res = self.si
        self.si -= 1
        return res