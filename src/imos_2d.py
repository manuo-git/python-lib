# name: Imos 2D
# prefix: imos2d
# ---
class imos2D:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.grid = [[0]*(m+1) for _ in range(n+1)]
        self.calced = False
    
    def add(self, r1, c1, r2, c2, num = 1): # [r1, r2), [c1, c2)
        assert r1 < r2 and c1 < c2
        assert not self.calced
        self.grid[r1][c1] += num
        self.grid[r1][c2] -= num
        self.grid[r2][c1] -= num
        self.grid[r2][c2] += num
    
    def calc(self):
        assert not self.calced
        self.calced = True
        for i in range(self.n+1):
            for j in range(self.m):
                self.grid[i][j+1] += self.grid[i][j]
        for j in range(self.m+1):
            for i in range(self.n):
                self.grid[i+1][j] += self.grid[i][j]
    
    def __getitem__(self, index):
        assert self.calced
        return self.grid[index]