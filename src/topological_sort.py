# name: Topological Sort
# prefix: topologicalsort
# ---
def tplgsort(N, E):
    incnt = [0]*N
    for i in range(N):
        for j in E[i]:
            incnt[j] += 1
    q = deque()
    for i in range(N):
        if incnt[i] == 0: q.append(i)
    
    ret = []
    while q:
        i = q.popleft()
        ret.append(i)
        for j in E[i]:
            incnt[j] -= 1
            if incnt[j] > 0: continue
            q.append(j)
    return ret