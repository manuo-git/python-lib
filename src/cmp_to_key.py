# name: Cmp to Key
# prefix: cmp to key
# ---
# https://github.com/manuo-git/python-lib/blob/main/src/cmp_to_key.py
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

def cmp(p1, p2):
    # p1が左ならTrue