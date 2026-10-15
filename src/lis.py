# name: LIS
# prefix: lis
# ---
# https://github.com/manuo-git/python-lib/blob/main/src/lis.py
from bisect import bisect_left, bisect_right
def lis(A, t = True): # t==Trueの時狭義単調増加
    if len(A) == 0: return 0
    res = []
    for a in A:
        if t:
            if len(res) == 0 or res[-1] < a:
                res.append(a)
            else:
                res[bisect_left(res, a)] = a
        else:
            if len(res) == 0 or res[-1] <= a:
                res.append(a)
            else:
                res[bisect_right(res, a)] = a
    return len(res)