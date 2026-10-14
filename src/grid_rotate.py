# name: Grid Rotate
# prefix: rotate
# ---
# https://github.com/manuo-git/python-lib/blob/main/src/grid_rotate.py
def rotate(G, left = True):
    # 反時計周り
    if left:
        h, w = len(G), len(G[0])
        nG = [[0]*h for _ in range(w)]
        for i in range(w):
            for j in range(h):
                nG[i][j] = G[j][w-i-1]
        return nG
    else:
        h, w = len(G), len(G[0])
        nG = [[0]*h for _ in range(w)]
        for i in range(w):
            for j in range(h):
                nG[i][j] = G[h-j-1][i]
        return nG