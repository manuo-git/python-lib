# name: LCS
# prefix: lcs
# ---
def LCS(s, t): # O(|s|*|t|)
    N = len(s)
    M = len(t)
    dp = [[0]*(M+1) for _ in range(N+1)]
    for i in range(N+1):
        for j in range(M+1):
            if j < M: dp[i][j+1] = max(dp[i][j+1], dp[i][j])
            if i < N: dp[i+1][j] = max(dp[i+1][j], dp[i][j])
            if i < N and j < M and s[i] == t[j]:
                dp[i+1][j+1] = max(dp[i+1][j+1], dp[i][j]+1)
    return dp[N][M]