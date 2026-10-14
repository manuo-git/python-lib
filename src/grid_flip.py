# name: Grid Flip
# prefix: flip
# ---
# https://github.com/manuo-git/python-lib/blob/main/src/grid_flip.py
def flip(G):
    h, w = len(G), len(G[0])
    nG = [[0]*w for _ in range(h)]
    for i in range(h):
        for j in range(w):
            nG[i][j] = G[i][w-j-1]
    return nG