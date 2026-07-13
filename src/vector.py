# name: Vector
# prefix: vector
# ---
import math
def cross(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return y2*x1 - y1*x2
def dot(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return x1*x2 + y1*y2
def slope(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    # b/a
    b = y2-y1
    a = x2-x1
    if a == 0:
        return (1, 0)
    elif b == 0:
        return (0, 1)
    g = math.gcd(a, b)
    b //= g
    a //= g
    if a < 0:
        a = -a
        b = -b
    return (b, a)
def vec(p1, p2):
    # p2-p1
    x1, y1 = p1
    x2, y2 = p2
    return x2-x1, y2-y1