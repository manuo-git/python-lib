# name: Prime
# prefix: prime
# ---
def prime(num):
    num = int(num)
    p = []
    if num < 2: return p
    p.append(2)
    memo = [i%2 for i in range(num+1)]
    for i in range(3, num+1, 2):
        if memo[i] == 0: continue
        p.append(i)
        for j in range(i, num+1, i):
            memo[j] = 0
    return p