# name: Cum 2D
# prefix: cum2d
# ---
class cum2D:
    def __init__(self, grid):
        self.n = len(grid)
        self.m = len(grid[0])
        self.grid = [[0]*(self.m+1) for _ in range(self.n+1)]
        for i in range(self.n):
            for j in range(self.m):
                self.grid[i+1][j+1] = self.grid[i][j+1]+self.grid[i+1][j]-self.grid[i][j]+grid[i][j]
    
    def rec(self, r1, c1, r2, c2): # [r1, r2), [c1, c2)
        assert r1 < r2 and c1 < c2
        return self.grid[r2][c2]-self.grid[r1][c2]-self.grid[r2][c1]+self.grid[r1][c1]