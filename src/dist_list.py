# name: Dist List
# prefix: distlist
# ---
def distlist(st, n, edge):
    q = deque([st])
    dist = [-1]*n
    bf = [-1]*n
    dist[st] = 0
    while q:
        i = q.popleft()
        for j in edge[i]:
            if dist[j] >= 0: continue
            bf[j] = i
            dist[j] = dist[i]+1
            q.append(j)
    # return dist, bf
    return dist