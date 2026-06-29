# name: Query Input
# prefix: qinput
# ---
def ctypes(li, types):
    assert len(li) == len(types)
    return [t(a) for a, t in zip(li, types)]
def qinput(*types, indexed = 1):
    li = input().split()
    t = int(li[0])
    if len(li) == 1: return t, None
    elif len(li) == 2: return t, types[t-indexed][0](li[1])
    else: return t, ctypes(li[1:], types[t-indexed])