# name: LIS
# prefix: lis
# ---
from bisect import bisect_left
def lis(A):
    if len(A) == 0: return 0
    res = []
    for a in A:
        if len(res) == 0 or res[-1] < a:
            res.append(a)
        else:
            res[bisect_left(res, a)] = a
    return len(res)