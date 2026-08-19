# name: Doubling O(N)
# prefix: doubling_o(n)
# ---
def f(x, p, si):
    i = si
    size = len(x)
    vis = [-1]*size
    vis[i] = 0
    n = 0
    while n < p:
        ni = x[i]
        i = ni
        n += 1
        if vis[i] >= 0:
            d = n-vis[i]
            n += (p-n)//d*d
            break
        vis[i] = n
    while n < p:
        i = x[i]
        n += 1
    return i