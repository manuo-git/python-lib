# name: SegTree 2D
# prefix: segtree2d
# ---
import math, sys
def gcd(x: int, y: int) -> int:
    return gcd(y, x % y) if y else abs(x)

# --- モードをIDで定義 ---
# 0: min, 1: max, 2: sum, 3: prd, 4: gcd, 5: lmc, 6: ^, 7: &, 8: |
MODE_MIN = 0
MODE_MAX = 1
MODE_SUM = 2
MODE_PRD = 3
MODE_GCD = 4
MODE_LMC = 5
MODE_XOR = 6
MODE_AND = 7
MODE_OR  = 8

class SegTree2D:
    N: int
    M: int
    KN: int
    KM: int
    N2: int
    M2: int
    default: int
    mode_id: int  # 関数の代わりにIDを保存
    dat: list[list[int]]

    def __init__(self, ls2D: list[list[int]], mode: str = 'min'):
        # 1. mode文字列をIDに変換し、デフォルト値を決定
        self.mode_id = MODE_MIN
        d = 1 << 60
        
        if mode == 'min':
            self.mode_id = MODE_MIN
            d = 1 << 60
        elif mode == 'max':
            self.mode_id = MODE_MAX
            d = -(1 << 60)
        elif mode == 'sum':
            self.mode_id = MODE_SUM
            d = 0
        elif mode == 'prd':
            self.mode_id = MODE_PRD
            d = 1
        elif mode == 'gcd':
            self.mode_id = MODE_GCD
            d = 0
        elif mode == 'lmc':
            self.mode_id = MODE_LMC
            d = 1
        elif mode == '^':
            self.mode_id = MODE_XOR
            d = 0
        elif mode == '&':
            self.mode_id = MODE_AND
            d = (1 << 60) - 1
        elif mode == '|':
            self.mode_id = MODE_OR
            d = 0
        
        self.default = d
        self.N = len(ls2D)
        self.M = len(ls2D[0])
        self.KN = (self.N - 1).bit_length() if self.N > 1 else 0
        self.KM = (self.M - 1).bit_length() if self.M > 1 else 0
        self.N2 = 1 << self.KN
        self.M2 = 1 << self.KM
        
        self.dat = [[self.default] * (self.M2 * 2) for _ in range(self.N2 * 2)]
        for i in range(self.N):
            row = ls2D[i]
            for j in range(self.M):
                self.dat[self.N2 + i][self.M2 + j] = row[j]
        self.build()

    # --- 関数の代わりにこのメソッドを呼ぶ ---
    def _op(self, a: int, b: int) -> int:
        mid = self.mode_id
        if mid == MODE_MIN: return min(a, b)
        if mid == MODE_MAX: return max(a, b)
        if mid == MODE_SUM: return a + b
        if mid == MODE_PRD: return a * b
        if mid == MODE_GCD: return gcd(a, b)
        if mid == MODE_LMC:
            g = gcd(a, b)
            return (a * b) // g if g != 0 else 0
        if mid == MODE_XOR: return a ^ b
        if mid == MODE_AND: return a & b
        if mid == MODE_OR:  return a | b
        return a

    def build(self):
        for i in range(self.N2 * 2):
            for j in range(self.M2 - 1, 0, -1):
                self.dat[i][j] = self._op(self.dat[i][j << 1], self.dat[i][j << 1 | 1])
        for i in range(self.N2 - 1, 0, -1):
            for j in range(self.M2 * 2):
                self.dat[i][j] = self._op(self.dat[i << 1][j], self.dat[i << 1 | 1][j])

    def update(self, x: int, y: int, value: int):
        i = x + self.N2
        j_orig = y + self.M2
        self.dat[i][j_orig] = value
        
        curr_j = j_orig
        while curr_j > 1:
            curr_j >>= 1
            self.dat[i][curr_j] = self._op(self.dat[i][curr_j << 1], self.dat[i][curr_j << 1 | 1])
        
        curr_i = i
        while curr_i > 1:
            curr_i >>= 1
            curr_j = j_orig
            self.dat[curr_i][curr_j] = self._op(self.dat[curr_i << 1][curr_j], self.dat[curr_i << 1 | 1][curr_j])
            while curr_j > 1:
                curr_j >>= 1
                self.dat[curr_i][curr_j] = self._op(self.dat[curr_i][curr_j << 1], self.dat[curr_i][curr_j << 1 | 1])

    def query(self, Lx: int, Rx: int, Ly: int, Ry: int) -> int:
        res = self.default
        Lx += self.N2
        Rx += self.N2
        while Lx < Rx:
            if Lx & 1:
                res = self._op(res, self._query_y(Lx, Ly, Ry))
                Lx += 1
            if Rx & 1:
                Rx -= 1
                res = self._op(res, self._query_y(Rx, Ly, Ry))
            Lx >>= 1
            Rx >>= 1
        return res

    def _query_y(self, idx_x: int, Ly: int, Ry: int) -> int:
        res_y = self.default
        Ly += self.M2
        Ry += self.M2
        while Ly < Ry:
            if Ly & 1:
                res_y = self._op(res_y, self.dat[idx_x][Ly])
                Ly += 1
            if Ry & 1:
                Ry -= 1
                res_y = self._op(self.dat[idx_x][Ry], res_y)
            Ly >>= 1
            Ry >>= 1
        return res_y