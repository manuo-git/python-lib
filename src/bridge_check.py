# name: Bridge Check
# prefix: bridge check
# ---
def find_bridges(n, edges):
    """
    n: 頂点数
    edges: (u, v) のリスト
    return: 各辺が橋なら1, そうでなければ0のリスト
    """
    E = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        E[u].append((v, i))
        E[v].append((u, i))

    ord = [-1] * n
    low = [-1] * n
    is_bridge = [0] * len(edges)
    timer = 0

    def dfs(u, parent_edge_id=-1):
        nonlocal timer
        ord[u] = low[u] = timer
        timer += 1
        
        for v, edge_id in E[u]:
            if edge_id == parent_edge_id:
                continue
            if ord[v] != -1:
                low[u] = min(low[u], ord[v])
            else:
                dfs(v, edge_id)
                low[u] = min(low[u], low[v])
                if ord[u] < low[v]:
                    is_bridge[edge_id] = 1

    for i in range(n):
        if ord[i] == -1:
            dfs(i)
    return is_bridge