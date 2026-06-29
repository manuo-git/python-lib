# name: Doubling List
# prefix: doubling list
# ---
# B_i <- A_x_i
def f(x, p): # O(NlogP) 使いまわすなら真面目に
    if p == 0:
        return [i for i in range(N)]
    elif p%2:
        y = f(x, p-1)
        return [y[v] for v in x]
    else:
        y = f(x, p//2)
        return [y[v] for v in y]