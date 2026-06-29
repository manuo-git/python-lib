# name: Combination
# prefix: comb
# ---
# O(NMAX)。MODが素数じゃないときは二次元配列を作ってO(NMAX^2)で求める。
# comb2を参照
NMAX = 1000000
COMB_F = [1]*(NMAX+1)
for i in range(2, NMAX+1):
    COMB_F[i] = COMB_F[i-1]*i%MOD
COMB_RF = [1]*NMAX + [pow(COMB_F[NMAX], -1, MOD)]
for i in reversed(range(2, NMAX+1)):
    COMB_RF[i-1] = COMB_RF[i]*i%MOD
def fac(n): return COMB_F[n]
def invfac(n): return COMB_RF[n]
def comb(n, r):
    if r < 0: return 0
    if n < 0: return comb(r-n-1, r)*(-1 if r&1 else 1)%MOD
    if n < r: return 0
    return COMB_F[n]*COMB_RF[r]*COMB_RF[n-r]%MOD
def homb(n, r): return comb(n+r-1, r) # 重複組み合わせ