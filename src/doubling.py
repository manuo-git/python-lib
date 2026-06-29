# name: Doubling
# prefix: doubling
# ---
class Doubling:
    def __init__(self, op, e, p, v, log = 60):
        assert len(p) == len(v)
        self.n = len(p)
        self.op = op
        self.e = e
        self.log = log
        self.dp = [[0]*self.n for _ in range(self.log)]
        self.ep = [[e]*self.n for _ in range(self.log)]
        for i in range(self.n):
            self.dp[0][i] = p[i]
            self.ep[0][i] = v[i]
        
        for k in range(self.log-1):
            for i in range(self.n):
                self.dp[k+1][i] = self.dp[k][self.dp[k][i]]
                self.ep[k+1][i] = self.op(self.ep[k][i], self.ep[k][self.dp[k][i]], k)

    def pow(self, k, si = 0):
        res = self.e
        bi = k
        cur = si
        for k in range(self.log):
            if bi>>k&1 == 0: continue
            res = self.op(res, self.ep[k][cur], k)
            cur = self.dp[k][cur]
        return res
    
    def pow_cur(self, k, si = 0):
        bi = k
        cur = si
        for k in range(self.log):
            if bi>>k&1 == 0: continue
            cur = self.dp[k][cur]
        return cur
    
    def pow_list(self, k):
        bi = k
        cur = [i for i in range(N)]
        for k in range(self.log):
            if bi>>k&1 == 0: continue
            cur = [self.dp[k][cur[i]] for i in range(N)]
        return cur