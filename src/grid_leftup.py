# name: Grid Left Up
# prefix: leftup
# ---
def leftup(G, white = "."):
    h, w = len(G), len(G[0])
    si, sj = h, w
    for i in range(h):
        for j in range(w):
            if G[i][j] != white:
                si = min(si, i)
                sj = min(sj, j)
    res = [[white]*w for _ in range(h)]
    for i in range(si, h):
        for j in range(sj, w):
            res[i-si][j-sj] = G[i][j]
    return res