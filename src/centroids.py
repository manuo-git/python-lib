# name: Centroids
# prefix: centroids
# ---
def get_centroids(N: int, edge: list[list[int]]) -> list[int]:
    """木の重心を求める (O(N))
    
    Args:
        N: 頂点数
        edge: 隣接リスト
        
    Returns:
        重心(1個または2個)のリスト
    """
    parent = [-1] * N
    order = []
    stack = [0]    
    while stack:
        u = stack.pop()
        order.append(u)
        for v in edge[u]:
            if v == parent[u]:
                continue
            parent[v] = u
            stack.append(v)
    size = [1] * N
    centroids = []
    half_N = N / 2    
    for u in reversed(order):
        is_centroid = True
        for v in edge[u]:
            if v == parent[u]: continue
            if size[v] > half_N: is_centroid = False
            size[u] += size[v]        
        if N-size[u] > half_N: is_centroid = False
        if is_centroid: centroids.append(u)
    return centroids