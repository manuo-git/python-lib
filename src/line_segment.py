# name: Line Segments
# prefix: linesegment
# ---
def calcline(x1, y1, x2, y2):
    p = x1-x2
    q = y1-y2
    r = -q*x1+p*y1
    d = p**2 + q**2
    g = math.gcd(p, q, r)
    p //= g
    q //= g
    r //= g
    if p < 0:
        return -p, -q, -r, d
    elif p == 0:
        return p, abs(q), abs(r), d
    else:
        return p, q, r, d