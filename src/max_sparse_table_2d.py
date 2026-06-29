# name: Max Sparse Table 2D
# prefix: sparsetable2dmax
# ---
class MaxDisjointSparseTable2D:
    def __init__(self, A: list[list[int]]):
        self.N = len(A)
        self.M = len(A[0])
        self.log_n = (self.N - 1).bit_length() if self.N > 1 else 1
        self.log_m = (self.M - 1).bit_length() if self.M > 1 else 1
        
        self.stride_dy = self.N * self.M
        self.stride_dx = self.log_m * self.stride_dy
        
        MIN_VAL = -(1<<60)
        
        size = self.log_n * self.log_m * self.N * self.M
        self.st = [MIN_VAL] * size
        
        tmp_x = [MIN_VAL] * (self.log_n * self.N * self.M)
        stride_tmp_x = self.N * self.M
        
        for dx in range(self.log_n):
            offset_x = dx * stride_tmp_x
            shift = 1 << dx
            
            for i in range(self.N):
                row_offset = offset_x + i * self.M
                for j in range(self.M):
                    tmp_x[row_offset + j] = A[i][j]
            
            for mid in range(shift, self.N, 2 * shift):
                for j in range(self.M):
                    curr = A[mid-1][j]
                    tmp_x[offset_x + (mid-1) * self.M + j] = curr
                    for i in range(mid-2, mid-shift-1, -1):
                        if i < 0: break
                        if A[i][j] > curr: curr = A[i][j]
                        tmp_x[offset_x + i * self.M + j] = curr
                    if mid < self.N:
                        curr = A[mid][j]
                        tmp_x[offset_x + mid * self.M + j] = curr
                        for i in range(mid+1, mid+shift):
                            if i >= self.N: break
                            if A[i][j] > curr: curr = A[i][j]
                            tmp_x[offset_x + i * self.M + j] = curr

        for dx in range(self.log_n):
            offset_dx = dx * self.stride_dx
            offset_tmp_x = dx * stride_tmp_x
            
            for i in range(self.N):
                base_tmp_idx = offset_tmp_x + i * self.M
                
                for dy in range(self.log_m):
                    offset_dy = offset_dx + dy * self.stride_dy + i * self.M
                    shift_y = 1 << dy
                    
                    for j in range(self.M):
                        self.st[offset_dy + j] = tmp_x[base_tmp_idx + j]
                    
                    for mid_y in range(shift_y, self.M, 2 * shift_y):
                        curr_y = tmp_x[base_tmp_idx + mid_y - 1]
                        self.st[offset_dy + mid_y - 1] = curr_y
                        for j in range(mid_y-2, mid_y-shift_y-1, -1):
                            if j < 0: break
                            val = tmp_x[base_tmp_idx + j]
                            if val > curr_y: curr_y = val
                            self.st[offset_dy + j] = curr_y
                        if mid_y < self.M:
                            curr_y = tmp_x[base_tmp_idx + mid_y]
                            self.st[offset_dy + mid_y] = curr_y
                            for j in range(mid_y+1, mid_y+shift_y):
                                if j >= self.M: break
                                val = tmp_x[base_tmp_idx + j]
                                if val > curr_y: curr_y = val
                                self.st[offset_dy + j] = curr_y

    def query(self, x1: int, x2: int, y1: int, y2: int) -> int:
        if x1 >= x2 or y1 >= y2: return -(1 << 62)
        _x1, _x2 = x1, x2 - 1
        _y1, _y2 = y1, y2 - 1
        
        dx = (_x1 ^ _x2).bit_length() - 1 if _x1 != _x2 else 0
        dy = (_y1 ^ _y2).bit_length() - 1 if _y1 != _y2 else 0
        
        if dx >= self.log_n: dx = self.log_n - 1
        if dy >= self.log_m: dy = self.log_m - 1
        
        base_offset = dx * self.stride_dx + dy * self.stride_dy
        
        v1 = self.st[base_offset + _x1 * self.M + _y1]
        v2 = self.st[base_offset + _x1 * self.M + _y2]
        v3 = self.st[base_offset + _x2 * self.M + _y1]
        v4 = self.st[base_offset + _x2 * self.M + _y2]
        
        res = v1
        if v2 > res: res = v2
        if v3 > res: res = v3
        if v4 > res: res = v4
        return res