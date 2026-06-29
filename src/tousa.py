# name: Sum of a Geometric Sequence
# prefix: tousa
# ---
# t: 0 -> tousa_wa(初項, 末項, 項数)
# t: 1 -> tousa_wa(初項, 末項, 公差, 1)
# t: 2 -> tousa_wa(初項, 公差, 項数, 2)
def tousa_wa(fi, lst, cnt, t = 0):
    if t == 0:
        return (fi+lst)*cnt//2
    if t == 1:
        d = cnt
        _cnt = (lst-fi)//d + 1
        return tousa_wa(fi, lst, _cnt)
    if t == 2:
        d = lst
        return (2*fi+(cnt-1)*d)*cnt//2