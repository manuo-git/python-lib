# name: Factor
# prefix: factor
# ---
FACMAX = $1
FAC = [0]*(FACMAX+1)
PRIME = []
FAC[1] = 1
for d in range(2, FACMAX+1):
    if FAC[d] == 0:
        FAC[d] = d
        PRIME.append(d)
    for p in PRIME:
        if p*d > FACMAX or p > FAC[d]: break
        FAC[p*d] = p

def factor(num):
    num = int(num)
    ret = []
    while num != 1:
        f = FAC[num]
        cnt = 0
        while num%f == 0:
            cnt += 1
            num //= f
        ret.append((f, cnt))
    return ret

def div(num):
    f = factor(num)
    ret = [1]
    for x, c in f:
        size = len(ret)
        for i in range(size):
            mul = x
            for _ in range(c):
                ret.append(ret[i]*mul)
                mul *= x
    return ret