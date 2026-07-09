# name: Cum KD
# prefix: cumkd
# ---
class cumKD:
    def __init__(self, k: int, *lim):
        self.k = k
        self.m = 1
        self.lim = lim
        for a in self.lim: self.m *= a
        self.dig = [1]*self.k
        for i in range(1, self.k): self.dig[i] = self.dig[i-1]*self.lim[i-1]
        self.dat = [0]*self.m
        self.is_build = False

        self.gray_k = []
        self.gray_is_plus = []
        self.gray_g = []
        self.gray_is_odd = []

        prev_g = 0        
        for i in range(1, 1 << self.k):
            curr_g = i ^ (i >> 1)
            
            change = prev_g ^ curr_g
            k_bit = change.bit_length() - 1
            
            self.gray_k.append(k_bit)
            self.gray_is_plus.append(bool(curr_g & change))
            self.gray_g.append(curr_g)
            self.gray_is_odd.append(i & 1)
            prev_g = curr_g
    
    def ind(self, *idxs):
        x = 0
        c = 1
        for i in range(self.k):
            x += idxs[i]*c
            c *= self.lim[i]
        return x
    
    def digit(self, x, k):
        return x//self.dig[k]%self.lim[k]

    def add_value(self, x, v):
        assert not self.is_build
        self.dat[x] += v

    def build(self):
        assert not self.is_build
        self.is_build = True
        dat = self.dat
        for k in range(self.k):
            step = self.dig[k]
            lim_k = self.lim[k]
            period = step * lim_k
            for base in range(0, self.m, period):
                for x in range(base + step, base + period):
                    dat[x] += dat[x - step]
    
    def rec(self, x, y): # [x, y)
        xd = [self.digit(x, k) for k in range(self.k)]
        yd = [self.digit(y, k) for k in range(self.k)]
        return self.rec_coords(xd, yd)

    def rec_coords(self, xd, yd):
        assert self.is_build
        for k in range(self.k):
            if xd[k] > yd[k]: return 0
        
        z = 0
        diff = [0] * self.k
        ng = 0
        
        for k in range(self.k):
            t0 = yd[k] * self.dig[k]
            z += t0
            if xd[k] == 0:
                ng |= (1 << k)
            else:
                t1 = (xd[k] - 1) * self.dig[k]
                diff[k] = t1 - t0
        
        dat = self.dat
        
        res = dat[z]
        
        gray_k = self.gray_k
        gray_is_plus = self.gray_is_plus
        gray_g = self.gray_g
        gray_is_odd = self.gray_is_odd
        
        for i in range(len(gray_k)):
            if gray_is_plus[i]:
                z += diff[gray_k[i]]
            else:
                z -= diff[gray_k[i]]
                
            if gray_g[i] & ng: continue
                
            if gray_is_odd[i]:
                res -= dat[z]
            else:
                res += dat[z]
        return res

# --cum[a][b][c][d][e][f]--
# cum = cumKD(6, a, b, c, d, e, f)