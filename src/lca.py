# name: LCA
# prefix: lca
# ---
from typing import List, Tuple
class LCA:
    """ダブリングを用いた最小共通祖先 (LCA) 計算ライブラリ。

    2頂点のLCA、距離、パス上の頂点、パス内の最大・最小エッジ重みを O(log N) で計算します。

    Attributes:
        N (int): 頂点数。
        E (List[List[Tuple[int, int]]]): 隣接リスト。各要素は (隣接頂点, 重み)。
        root (int): 木の根。
        log_size (int): ダブリングテーブルの高さ (bit_length)。
        depth (List[int]): 根からの深さ（エッジ数）。
        dist_from_root (List[int]): 根からの累積重み。
        parent (List[List[int]]): ダブリングテーブル (2^k 個上の親)。
        min_edge (List[List[int]]): パス上の最小エッジ重みのダブリングテーブル。
        max_edge (List[List[int]]): パス上の最大エッジ重みのダブリングテーブル。
    """

    INF = 1<<60

    def __init__(self, N: int, E: List[List], root=0) -> None:
        """LCAクラスの初期化。入力形式の判定と前処理の実行。

        Args:
            N (int): 頂点数。
            E (List[List]): 隣接リスト。重みなし(int)または重み付き(tuple)に対応。
            root (int, optional): 木の根。 Defaults to 0.
        """
        self.N = N
        t = 0
        self.E = [[] for _ in range(self.N)]
        for i in range(self.N):
            for e in E[i]:
                if t == 0:
                    t = 1 if isinstance(e, int) else 2
                if t == 1:
                    self.E[i].append((e, 1))
                else:
                    self.E[i].append(e)

        self.root = root
        self.log_size = N.bit_length()
        self.depth = [-1] * N
        self.dist_from_root = [-1] * N
        self.parent = [-1] * (self.log_size * N)
        self.min_edge = [LCA.INF] * (self.log_size * N)
        self.max_edge = [-LCA.INF] * (self.log_size * N)
        self._build()

    def _build(self) -> None:
        """DFSによる初期値の設定とダブリングテーブルの構築を行う内部メソッド。

        このメソッドは、クラスの初期化時に一度だけ呼び出されます。
        以下の2つのステップで構成されます:
        1. 非再帰DFSを用いて各頂点の親、根からの深さ(エッジ数)、および累積距離（コスト和）を
           計算し、ダブリングの基底状態(2^0 = 1つ上の親)を埋めます。
        2. 動的計画法(DP)の要領で、parent[k][i] = parent[k-1][parent[k-1][i]] の関係を利用し、
           2^k 先の親およびそのパス上の最大・最小エッジ重みを前計算します。

        Complexity:
            時間計算量: O(N log N)
            空間計算量: O(N log N)
        """
        N = self.N
        log_size = self.log_size
        parent = self.parent
        min_edge = self.min_edge
        max_edge = self.max_edge
        depth = self.depth
        dist_from_root = self.dist_from_root
        E = self.E
        root = self.root

        depth[root] = 0
        dist_from_root[root] = 0
        q = [root]
        while q:
            i = q.pop()
            for j, cost in E[i]:
                if depth[j] != -1:
                    continue
                parent[j] = i
                max_edge[j] = cost
                min_edge[j] = cost
                depth[j] = depth[i] + 1
                dist_from_root[j] = dist_from_root[i] + cost
                q.append(j)

        for k in range(1, log_size):
            prev_offset = (k - 1) * N
            curr_offset = k * N
            for i in range(N):
                j = parent[prev_offset + i]
                if j == -1: continue

                parent[curr_offset + i] = parent[prev_offset + j]

                m1, m2 = min_edge[prev_offset + i], min_edge[prev_offset + j]
                min_edge[curr_offset + i] = m1 if m1 < m2 else m2
                
                m1, m2 = max_edge[prev_offset + i], max_edge[prev_offset + j]
                max_edge[curr_offset + i] = m1 if m1 > m2 else m2

    def get_lca(self, u: int, v: int) -> int:
        """2頂点 u, v の最小共通祖先を返す。

        Args:
            u (int): 頂点1。
            v (int): 頂点2。

        Returns:
            int: LCAとなる頂点番号。
        """
        N = self.N
        log_size = self.log_size
        parent = self.parent
        depth = self.depth
        if depth[u] > depth[v]:
            u, v = v, u
        
        diff = depth[v] - depth[u]
        while diff:
            k = (diff & -diff).bit_length() - 1
            v = parent[k * N + v]
            diff &= diff - 1

        if u == v:
            return u

        for k in reversed(range(log_size)):
            idx_u = k * N + u
            idx_v = k * N + v
            if parent[idx_u] != parent[idx_v]:
                u = parent[idx_u]
                v = parent[idx_v]

        return self.parent[u]

    def get_dist(self, u: int, v: int) -> int:
        """2頂点 u, v 間の最短距離（重みの総和）を返す。

        Args:
            u (int): 頂点1。
            v (int): 頂点2。

        Returns:
            int: u-v 間の累積重み。
        """
        lca = self.get_lca(u, v)
        return self.dist_from_root[u] + self.dist_from_root[v] - 2 * self.dist_from_root[lca]

    def kth_ancestor(self, u: int, k: int) -> int:
        """頂点 u の k 個上の祖先を返す。

        Args:
            u (int): 開始頂点。
            k (int): 遡る個数。

        Returns:
            int: 祖先の頂点番号。存在しない場合は -1。
        """
        N = self.N
        parent = self.parent
        curr = u
        for ki in range(k.bit_length()):
            if k>>ki&1:
                curr = parent[ki * N + curr]
                if curr == -1: break
        return curr

    def jump(self, u: int, v: int, k: int) -> int:
        """u から v へのパス上で u から k 進んだ頂点を返す。

        Args:
            u (int): 起点。
            v (int): 終点。
            k (int): 進むエッジ数。

        Returns:
            int: 到達頂点番号。k がパスの長さを超える場合は -1。
        """
        d = self._get_edge_dist(u, v)
        if k > d: return -1
        lca = self.get_lca(u, v)
        d_u = self.depth[u] - self.depth[lca]
        if d_u >= k:
            return self.kth_ancestor(u, k)
        else:
            return self.kth_ancestor(v, d - k)

    def is_on_path(self, u: int, v: int, x: int) -> bool:
        """頂点 x がパス u-v 上に存在するか判定する。

        Args:
            u (int): パス端点1。
            v (int): パス端点2。
            x (int): 判定対象の頂点。

        Returns:
            bool: x がパス上に存在すれば True。
        """
        return self._get_edge_dist(u, x) + self._get_edge_dist(x, v) == self._get_edge_dist(u, v)

    def get_path_min_max(self, u: int, v: int) -> Tuple[int, int]:
        """パス u-v 上に含まれるエッジ重みの最小値と最大値を返す。

        Args:
            u (int): 頂点1。
            v (int): 頂点2。

        Returns:
            Tuple[int, int]: (最小重み, 最大重み)。
        """
        N = self.N
        log_size = self.log_size
        parent = self.parent
        min_edge = self.min_edge
        max_edge = self.max_edge
        depth = self.depth
        res_min, res_max = LCA.INF, -LCA.INF
        
        if self.depth[u] > self.depth[v]:
            u, v = v, u
        
        diff = depth[v] - depth[u]
        while diff:
            k = (diff & -diff).bit_length() - 1
            idx = k * N + v
            if res_min > min_edge[idx]: res_min = min_edge[idx]
            if res_max < max_edge[idx]: res_max = max_edge[idx]
            v = parent[idx]
            diff &= diff - 1
        
        if u == v:
            return res_min, res_max
        
        for k in reversed(range(log_size)):
            idx_u = k * N + u
            idx_v = k * N + v
            if parent[idx_u] != parent[idx_v]:
                if res_min > min_edge[idx_u]: res_min = min_edge[idx_u]
                if res_max < max_edge[idx_u]: res_max = max_edge[idx_u]
                if res_min > min_edge[idx_v]: res_min = min_edge[idx_v]
                if res_max < max_edge[idx_v]: res_max = max_edge[idx_v]
                u = parent[idx_u]
                v = parent[idx_v]
        
        idx_u, idx_v = u, v
        if res_min > min_edge[idx_u]: res_min = min_edge[idx_u]
        if res_min > min_edge[idx_v]: res_min = min_edge[idx_v]
        if res_max < max_edge[idx_u]: res_max = max_edge[idx_u]
        if res_max < max_edge[idx_v]: res_max = max_edge[idx_v]
        
        return res_min, res_max

    def _get_edge_dist(self, u: int, v: int) -> int:
        """2頂点間のエッジ数(重みによらない距離)を計算する内部関数。

        Args:
            u (int): 頂点1。
            v (int): 頂点2。

        Returns:
            int: u-v パスを構成するエッジの個数。
        """
        lca = self.get_lca(u, v)
        return self.depth[u] + self.depth[v] - 2 * self.depth[lca]