# name: Sum of a Floor Sequence
# prefix: sum_floor
# ---
# sum(N//b for b in range(1, N+1))
def sum_floor(N, MOD): # O(√N)
    res = 0
    prevk = -1
    idx = 1
    while True:
        l = N//(idx+1)+1
        r = N//idx
        if l <= r:
            res += (r-l+1)*idx
            res %= MOD
        prevk = l
        if prevk <= N//prevk: break
        idx += 1
    while True:
        prevk -= 1
        if prevk < 1: break
        res += N//prevk
        res %= MOD
    return res