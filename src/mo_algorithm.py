# name: Mo's Algorithm
# prefix: mo
# ---
class MoSolver:
    n: int
    q: int
    qs: list[tuple[int, int, int]]
    
    def __init__(self, n: int):
        self.n = n
        self.q = 0
        self.qs = []

    def add_query(self, l: int, r: int): # [l, r)
        self.qs.append((l, r, self.q))
        self.q += 1

    def solve(self, add_left, add_right, erase_left, erase_right, answer) -> list[int]:
        b = int(self.n / (self.q**0.5)) + 1
        self.qs.sort(key=lambda x: (x[0] // b, x[1] if (x[0] // b) % 2 == 0 else -x[1]))

        ans = [0]*self.q
        cur_l, cur_r = 0, 0
        for l, r, idx in self.qs:
            while cur_l > l: # [l, r) -> [l-1, r)
                cur_l -= 1
                add_left(cur_l, cur_l, cur_r)
            while cur_r < r: # [l, r) -> [l, r+1)
                add_right(cur_r, cur_l, cur_r+1)
                cur_r += 1
            while cur_l < l: # [l, r) -> [l+1, r)
                erase_left(cur_l, cur_l, cur_r)
                cur_l += 1
            while cur_r > r: # [l, r) -> [l, r-1)
                cur_r -= 1
                erase_right(cur_r, cur_l, cur_r+1)
            ans[idx] = answer(idx, cur_l, cur_r)
        return ans
    
# def add_left(i, cur_l, cur_r):
# def add_right(i, cur_l, cur_r):
# def erase_left(i, cur_l, cur_r):
# def erase_right(i, cur_l, cur_r):
# def answer(i, cur_l, cur_r):