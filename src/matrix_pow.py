# name: Matrix Pow
# prefix: matrixpow
# ---
class MatrixPow:
    def __init__(self, add, zero, mul, one, mat):
        h = len(mat)
        w = len(mat[0])
        assert h == w
        self.n = h
        self.add = add
        self.zero = zero
        self.mul = mul
        self.one = one
        self.mat = self._zeros()
        for i in range(self.n):
            for j in range(self.n):
                self.mat[i][j] = mat[i][j]
    
    def pow(self, k: int):
        mat = self._mat()
        res = self._identity()
        while k != 0:
            z = (k&-k).bit_length()-1
            for _ in range(z): mat = self._mul_mat(mat, mat)
            k >>= z
            k -= 1
            res = self._mul_mat(res, mat)
        return res
    
    def _mat(self):
        res = self._zeros()
        for i in range(self.n):
            for j in range(self.n):
                res[i][j] = self.mat[i][j]
        return res
    
    def _zeros(self):
        return [[self.zero]*self.n for _ in range(self.n)]
    
    def _identity(self):
        ret = self._zeros()
        for i in range(self.n): ret[i][i] = self.one
        return ret
    
    def _mul_mat(self, a, b):
        res = self._zeros()
        for i in range(self.n):
            for j in range(self.n):
                s = self.zero
                for k in range(self.n): s = self.add(s, self.mul(a[i][k], b[k][j]))
                res[i][j] = s
        return res
    
    @staticmethod
    def mul_mat_vec(mat, vec, add, zero, mul):
        n = len(mat)
        res = [zero]*n
        for i in range(n):
            for j in range(n):
                res[i] = add(res[i], mul(mat[i][j], vec[j]))
        return res
# |a, b| |x|   |(a⊗x)⊕(b⊗y)|
# |c, d| |y| = |(c⊗x)⊕(d⊗y)|