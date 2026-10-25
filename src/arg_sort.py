# name: Arg Sort
# prefix: argsort
# ---
# https://github.com/manuo-git/python-lib/blob/main/src/arg_sort.py
from typing import *
from random import randint
from collections import deque
def sort(data: list[Any], cmp):
    q = deque([(0, len(data))])
    while q:
        l, r = q.popleft()
        m = _quick_sort(data, l, r, cmp)
        if m == -1: continue
        q.append((l, m))
        q.append((m+1, r))

def _quick_sort(data, l, r, cmp):
    n = r-l
    if n <= 1: return -1
    if n == 2:
        if cmp(data[l+1], data[l]):
            data[l], data[l+1] = data[l+1], data[l]
        return -1
    pi = randint(l, r-1)
    pivot = data[pi]
    data[pi], data[r-1] = data[r-1], data[pi]
    i = l
    j = r-2
    while i < j:
        while i < j and cmp(data[i], pivot):
            i += 1
        while i < j and cmp(pivot, data[j]):
            j -= 1
        if i == j: break
        data[i], data[j] = data[j], data[i]
        if i+1 == j: break
        i += 1
        j -= 1
    m = i
    if cmp(data[i], pivot): m = i+1
    data[m], data[r-1] = data[r-1], data[m]
    return m

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