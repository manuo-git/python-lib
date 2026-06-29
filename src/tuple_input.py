# name: Tuple Input
# prefix: tinput
# ---
def ctypes(li, types):
    assert len(li) == len(types)
    return [t(a) for a, t in zip(li, types)]
def tinput(*types):
    li = input().split()
    return ctypes(li, types)