# name: Arg Sort
# prefix: argsort
# ---
from typing import *
def sort(data: List[Any], cmp):
    if len(data) == 1: return
    res = _sort(data, cmp)
    data.clear()
    data.extend(res)

def _sort(data: List[Any], cmp):
    if len(data) <= 1:
        return data
    m = len(data)//2
    ret = merge(_sort(data[:m], cmp), _sort(data[m:], cmp), cmp)
    return ret

def merge(l, r, cmp):
    res = []
    i, j = 0, 0
    while i < len(l) and j < len(r):
        if cmp(l[i], r[j]):
            res.append(l[i])
            i += 1
        else:
            res.append(r[j])
            j += 1
    if i < len(l): res.extend(l[i:])
    if j < len(r): res.extend(r[j:])
    return res

# t: 0 -> 時計回り
# t: 1 -> 反時計回り
def argsort(XY: list[tuple[int, int]], t = 0) -> list[tuple[int, int, int]]:
    def argcmp(p1, p2):
        # p1が左ならTrue
        x1, y1, _ = p1
        x2, y2, _ = p2
        if x1 == x2 == 0:
            res = y1 > y2
        else:
            res = y1*x2 > y2*x1
        return res^t
    n = len(XY)
    R = []
    L = []
    for i in range(n):
        x, y = XY[i]
        if x >= 0:
            R.append((x, y, i))
        else:
            L.append((x, y, i))
    sort(R, argcmp)
    sort(L, argcmp)
    if t == 0:
        return R+L
    else:
        return L+R

def samearg(p1, p2):
    x1, y1, _ = p1
    x2, y2, _ = p2
    cross = y2*x1 - y1*x2
    dot = x1*x2 + y1*y2
    if cross == 0:
        return dot > 0
    else:
        return y1*x2 == y2*x1