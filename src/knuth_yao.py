# name: Knuth-Yao
# prefix: knuth_yao
# ---
def Knuth_Yao(N, op):
    opt = [[0]*(2*N+1) for _ in range(2*N+1)]
    for i in range(1, 2*N+1):
        opt[i][i] = i

    dp = [[0]*(2*N+1) for _ in range(2*N+1)]
    for w in range(2, N+1):
        for l in range(1, N+1):
            r = l+w-1
            val = INF
            for k in range(opt[l][r-1], min(r-1, opt[l+1][r])+1):
                if val >= dp[l][k]+dp[k+1][r]:
                    val = dp[l][k]+dp[k+1][r]
                    opt[l][r] = k
            val += op(l-1, r)
            dp[l][r] = val
            if N+r <= 2*N:
                dp[N+l][N+r] = val
                opt[N+l][N+r] = opt[l][r]+N
    return dp