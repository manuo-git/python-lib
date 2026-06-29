# name: Lucy DP
# prefix: lucydp
# ---
# https://qiita.com/masa0599/items/2704047579eaafb2a322
# N以下の素数の数を数える
def lucydp(num): # O(√N)
    r = math.isqrt(num)
    V = [num//i for i in range(1,r+1)]
    V.extend(list(range(V[-1]-1,0,-1)))
    S = {i:i-1 for i in V}
    for p in range(2,r+1):
        if S[p] == S[p-1]: continue # p is not prime
        sp = S[p-1]  # num. of primes smaller than p
        for v in V:
            if v < p**2: break  
            S[v] -= (S[v//p] - sp)  
    return S[num]