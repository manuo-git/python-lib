# name: Factor Big
# prefix: factor big
# ---
# [(x1, c1), (x2, c2) ... (xk, ck)]
# X = x1^c1 * x2^c2 * ... * xk^ck
def factor(X):
    M = X
    ret = []
    if X == 1: return []
    if X%2 == 0:
        cnt = 0
        while X%2 == 0:
            X //= 2
            cnt += 1
        ret.append((2, cnt))
    for x in range(3, math.isqrt(M)+1, 2):
        if X%x == 0:
            cnt = 0
            while X%x == 0:
                X //= x
                cnt += 1
            ret.append((x, cnt))
    if X != 1: ret.append((X, 1))
    return ret