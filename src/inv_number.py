# name: Inversion Number
# prefix: invnumber
# ---
def invnumber(A):
    X = sorted(list(set(A)))
    pos = {x: e for e, x in enumerate(X)}
    M = len(X)
    from atcoder.fenwicktree import FenwickTree
    F = FenwickTree(M)
    res = 0
    for a in A:
        i = pos[a]
        res += F.sum(i, M)
        F.add(i, 1)
    return res