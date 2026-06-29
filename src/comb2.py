# name: Combination2
# prefix: comb2
# ---
# O(NMAX^2)
NMAX = $1
MOD = $2
F = [[0]*(NMAX+1) for _ in range(NMAX+1)]
F[0][0] = 1
for n in range(1, NMAX+1):
    F[n][0] = 1
    for k in range(1, n+1):
        F[n][k] = (F[n-1][k-1] + F[n-1][k])%MOD
def comb(n, k): return F[n][k]
def homb(n, r): return comb(n+r-1, r) # 重複組み合わせ