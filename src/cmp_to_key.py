# name: Cmp to Key
# prefix: cmp to key
# ---
from typing import *
def sort(data: list[Any], cmp):
    if len(data) == 1: return
    res = _sort(data, cmp)
    data.clear()
    data.extend(res)

def _sort(data: list[Any], cmp):
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

def cmp(p1, p2):
    # p1が左ならTrue