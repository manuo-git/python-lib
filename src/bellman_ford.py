# name: Bellman-Ford
# prefix: bellmanford
# ---
class BellmanFord:
    INF = 1 << 60

    def __init__(self, n: int):
        self._n = n
        self._edges = []
    
    def _init_data(self) -> None:
        self._dist = [BellmanFord.INF] * self._n
        self._bf = [-1] * self._n
        self._has_negative_cycle = False
    
    def add_edge(self, u: int, v: int, c: int, directed: bool = False) -> None:
        assert 0 <= u < self._n
        assert 0 <= v < self._n
        self._edges.append((u, v, c))
        if not directed:
            self._edges.append((v, u, c))
    
    def calc(self, start: int):
        assert 0 <= start < self._n
        self._init_data()
        self._dist[start] = 0
        self._last_start = start

        # V-1 回の緩和処理
        for i in range(self._n):
            updated = False
            for u, v, cost in self._edges:
                if self._dist[u] != BellmanFord.INF and self._dist[v] > self._dist[u] + cost:
                    self._dist[v] = self._dist[u] + cost
                    self._bf[v] = u
                    updated = True
                    
                    # n回目のループで更新があれば負の閉路が存在する
                    if i == self._n - 1:
                        self._has_negative_cycle = True
                        return None # 負の閉路がある場合はNoneを返す（運用に合わせて調整可）
            
            # 更新が一度も行われなければ、その時点で最短距離は確定
            if not updated:
                break
                
        return self._dist

    def has_negative_cycle(self) -> bool:
        """負の閉路が存在するかどうかを返す"""
        return self._has_negative_cycle

    def dist(self) -> list[int]:
        return self._dist
    
    def path_to(self, goal: int):
        assert 0 <= goal < self._n
        if self._dist[goal] == BellmanFord.INF:
            return None
        
        cur = goal
        path = [cur]
        # 負の閉路がある場合、無限ループになる可能性があるため一応チェック
        visited_in_path = {cur}
        
        while cur != self._last_start:
            cur = self._bf[cur]
            if cur == -1 or cur in visited_in_path:
                return None # 到達不能または閉路検出
            path.append(cur)
            visited_in_path.add(cur)
            
        path.reverse()
        return path