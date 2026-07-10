# name: HLD
# prefix: hld
# ---
class HLD:
    n: int
    edges: list[list[tuple[int, int]]]
    root: int
    parent: list[int]
    depth: list[int]
    size: list[int]
    heavy: list[int]
    head: list[int]
    vid: list[int]
    inv_vid: list[int]
    dist_from_root: list[int]
    edge_to_child: list[int]

    def __init__(self, n: int, root: int = 0) -> None:
        """HLD (Heavy-Light Decomposition) クラスを初期化し、内部構造を構築する。

        Args:
            n (int): 木の頂点数。
            root (int): 木の根とする頂点番号。デフォルトは 0。

        """
        self.n = n
        self.root = root
        self.edges = [[] for _ in range(n)]
        self.uv = []

    def add_edge(self, u: int, v: int, w: int = 1):
        self.edges[u].append((v, w))
        self.edges[v].append((u, w))
        self.uv.append((u, v))

    def build(self) -> None:
        """木の情報を走査し、部分木サイズ、重い辺、各頂点のHLD上のIDを計算する。

        このメソッドは内部的に2回の走査を行う:
        1. BFS/スタックによる走査で親子関係、深さ、根からの距離を計算。
        2. 逆順走査で部分木サイズと重い子 (heavy child) を決定。
        その後、重い辺を優先的に走査してパスを分解 (Heavy-Light Decomposition) し、
        各頂点にセグメント木等で利用可能な連続した ID (vid) を割り当てる。
        """
        n = self.n
        self.parent = [0] * n
        self.depth = [-1] * n
        self.size = [0] * n
        self.heavy = [-1] * n
        self.head = [0] * n
        self.vid = [0] * n
        self.inv_vid = []
        self.dist_from_root = [0] * n
        self.edge_to_child = []
        edges = self.edges
        parent = self.parent
        depth = self.depth
        size = self.size
        dist_from_root = self.dist_from_root
        heavy = self.heavy
        q = [(-1, self.root)]
        depth[self.root] = 0
        order = []
        while q:
            p, i = q.pop()
            order.append(i)
            parent[i] = p
            size[i] = 1
            for j, w in edges[i]:
                if p == j: continue
                assert depth[j] == -1, "this input is not tree."
                depth[j] = depth[i]+1
                dist_from_root[j] = dist_from_root[i]+w
                q.append((i, j))
        
        for i in reversed(order):
            p = parent[i]
            if p == -1: continue
            size[p] += size[i]
            if heavy[p] == -1 or size[heavy[p]] < size[i]:
                heavy[p] = i        
        
        head = self.head
        vid = self.vid
        inv_vid = self.inv_vid
        q = [(self.root, self.root)]
        while q:
            i, hi = q.pop()
            inv_vid.append(i)
            head[i] = hi
            for j, _ in edges[i]:
                if j == parent[i]: continue
                if j == heavy[i]: continue
                q.append((j, j))
            if heavy[i] >= 0:
                q.append((heavy[i], hi))
        for i in range(n):
            vid[inv_vid[i]] = i

        assert len(self.uv) == self.n-1
        self.edge_to_child = [0] * (self.n-1)
        for i, (u, v) in enumerate(self.uv):
            self.edge_to_child[i] = v if self.depth[v] > self.depth[u] else u

    def get_lca(self, u: int, v: int):
        """2頂点 u, v の最近共通祖先 (LCA) を返す。

        Args:
            u (int): 頂点番号。
            v (int): 頂点番号。

        Returns:
            int: LCA となる頂点番号。
        """
        head = self.head
        depth = self.depth
        parent = self.parent
        while True:
            hu = head[u]
            hv = head[v]
            if hu == hv: break
            if depth[hu] < depth[hv]:
                v = parent[hv]
            else:
                u = parent[hu]
        lca = u if depth[u] < depth[v] else v
        return lca

    def kth_ancestor(self, u: int, k: int) -> int:
        """頂点 u から k 個上の祖先を返す。

        Args:
            u (int): 頂点番号。
            k (int): 遡る数。

        Returns:
            int: 祖先の頂点番号。存在しない場合は -1。
        """
        head = self.head
        depth = self.depth
        parent = self.parent
        target = depth[u] - k
        if target < 0: return -1
        while True:
            hu = head[u]
            if depth[hu] <= target: break
            u = parent[head[u]]
        vid = self.vid
        uid = vid[u]
        targetid = uid - (depth[u]-target)
        v = self.inv_vid[targetid]
        return v

    def jump(self, u: int, v: int, k: int) -> int:
        """u-v パス上で u から数えて k 個目の頂点を返す。

        Args:
            u (int): 始点。
            v (int): 終点。
            k (int): 移動ステップ数。

        Returns:
            int: 到達した頂点番号。パスの長さを超える場合は -1。
        """
        d = self.get_edge_dist(u, v)
        if k > d: return -1
        lca = self.get_lca(u, v)
        d_u = self.depth[u] - self.depth[lca]
        if d_u >= k:
            return self.kth_ancestor(u, k)
        else:
            return self.kth_ancestor(v, d - k)

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

    def is_on_path(self, u: int, v: int, x: int) -> bool:
        """頂点 x がパス u-v 上に存在するか判定する。

        Args:
            u (int): パス端点1。
            v (int): パス端点2。
            x (int): 判定対象の頂点。

        Returns:
            bool: x がパス上に存在すれば True。
        """
        return self.get_edge_dist(u, x) + self.get_edge_dist(x, v) == self.get_edge_dist(u, v)


    def get_edge_dist(self, u: int, v: int) -> int:
        """2頂点間のエッジ数(重みによらない距離)を計算する。

        Args:
            u (int): 頂点1。
            v (int): 頂点2。

        Returns:
            int: u-v パスを構成するエッジの個数。
        """
        lca = self.get_lca(u, v)
        return self.depth[u] + self.depth[v] - 2 * self.depth[lca]
    
    def path_sections(self, u: int, v: int, edge: bool = False):
        """
        u-v パスをセグメント木上の連続区間 [l, r) に分解して yield する。
        戻り値: (l, r, is_reverse)
        
        Args:
            u, v: 端点となる頂点
            edge: True の場合、辺クエリ(LCAを含まない)として処理する
        """
        head = self.head
        depth = self.depth
        parent = self.parent
        vid = self.vid
        # u側（登り）とv側（最終的に降りになる）の区間を溜めるリスト
        # 各要素は (l, r, is_reverse)
        l_parts: list[tuple[int, int, bool]] = []
        r_parts: list[tuple[int, int, bool]] = []
        
        while head[u] != head[v]:
            if depth[head[u]] > depth[head[v]]:
                # u側を登る: IDが減る方向なので is_reverse=True
                l_parts.append((vid[head[u]], vid[u] + 1, True))
                u = parent[head[u]]
            else:
                # v側を登る: 後で逆順(降り)にするため、ここでは反転させない(False)
                r_parts.append((vid[head[v]], vid[v] + 1, False))
                v = parent[head[v]]
        
        # 同じ Chain に到達した後の、LCA付近の処理
        if depth[u] > depth[v]:
            # u側が深い場合
            l_offset = 1 if edge else 0
            # 頂点クエリなら [vid[v], vid[u]+1], 辺クエリなら [vid[v]+1, vid[u]+1]
            if vid[v] + l_offset < vid[u] + 1:
                l_parts.append((vid[v] + l_offset, vid[u] + 1, True))
        else:
            # v側が深い(または同じ)場合
            r_offset = 1 if edge else 0
            # 頂点クエリなら [vid[u], vid[v]+1], 辺クエリなら [vid[u]+1, vid[v]+1]
            if vid[u] + r_offset < vid[v] + 1:
                r_parts.append((vid[u] + r_offset, vid[v] + 1, False))
        
        # 1. u から LCA への昇順区間を順番に出す
        for section in l_parts:
            yield section
            
        # 2. v 側のリストを逆順にして、LCA から v へ降りる順序で出す
        # reversed() を使うことで、LCAに近い方の区間から順に出現する
        for section in reversed(r_parts):
            yield section
    
    def prod_path(self, u: int, v: int, e, prod_func, op, edge: bool = False):
        """u-v パス上の値を集約して返す。

        Args:
            u (int): 始点。
            v (int): 終点。
            e (T): 単位元。
            prod_func (Callable[[int, int], tuple[T, T]]): セグメント木の範囲取得関数。 (forward, backward) のペアを返す必要があります。
            op (Callable[[T, T], T]): 二項演算。
            edge (bool): True の場合、辺クエリ (LCA を含まない) として処理する。

        Returns:
            T: パス上の要素を op で集約した結果。
        """
        res = e
        for l, r, is_rev in self.path_sections(u, v, edge):
            fwd, bwd = prod_func(l, r)
            # 登りなら backward、降りなら forward を使う
            chunk = bwd if is_rev else fwd
            res = op(res, chunk)
        return res
            
    def prod_subtree(self, u: int, e, prod_func, op, edge: bool = False):
        """頂点 u の部分木を集約して返す。

        Args:
            u (int): 部分木の根となる頂点。
            e (T): 単位元。
            prod_func (Callable[[int, int], tuple[T, T]]): セグメント木の範囲取得関数。
            op (Callable[[T, T], T]): 二項演算。
            edge (bool): True の場合、辺クエリ (u 直上の辺を含まない) として処理する。

        Returns:
            T: 部分木内の要素を集約した結果。
        """
        l = self.vid[u]
        r = self.vid[u] + self.size[u]
        if edge:
            l += 1
        if l < r:
            fwd, _ = prod_func(l, r)
            return fwd
        return e
    
    def apply_path(self, u: int, v: int, x, apply_func, edge: bool = False) -> None:
        """u-v パス上の要素に一括操作 (範囲更新) を適用する。

        Args:
            u (int): 始点。
            v (int): 終点。
            x (F): 作用させる値 (作用素)。
            apply_func (Callable[[int, int, F], None]): セグメント木の範囲更新関数 (apply(l, r, x))。
            edge (bool): True の場合、辺クエリ (LCA を含まない) として処理する。
        """
        for l, r, _ in self.path_sections(u, v, edge):
            apply_func(l, r, x)
            
    def apply_subtree(self, u: int, x, apply_func, edge: bool = False) -> None:
        """頂点 u の部分木に一括操作 (範囲更新) を適用する。

        Args:
            u (int): 部分木の根となる頂点。
            x (F): 作用させる値 (作用素)。
            apply_func (Callable[[int, int, F], None]): セグメント木の範囲更新関数 (apply(l, r, x))。
            edge (bool): True の場合、辺クエリ (u 直上の辺を含まない) として処理する。
        """
        l = self.vid[u]
        r = self.vid[u] + self.size[u]
        if edge:
            l += 1
        if l < r:
            apply_func(l, r, x)
    
    def set(self, u: int, set_func, x, edge: bool = False) -> None:
        """頂点 u の値、もしくは辺番号 u の値を更新する。

        Args:
            u (int): 頂点クエリの場合は更新対象の頂点番号。辺番号を指定する場合は辺番号。
            set_func (Callable[[int, tuple[T, T]], None]): セグメント木の一点更新関数。
            x (T): 更新後の値。
            edge (bool): 辺番号を指定する場合は True。
        """
        if not edge:
            set_func(self.vid[u], (x, x))
        else:
            child = self.edge_to_child[u]
            set_func(self.vid[child], (x, x))

    def get(self, u: int, get_func, edge: bool = False):
        """頂点 u、もしくは辺番号 u の現在の値を取得する。

        Args:
            u (int): 取得対象の頂点。
            get_func (Callable[[int], tuple[T, T]]): セグメント木の一点取得関数。
            edge (bool): 辺番号を指定する場合は True。
        Returns:
            T: 頂点 u、もしくは辺番号 u の現在の値。
        """
        if not edge:
            val_pair = get_func(self.vid[u])
            return val_pair[0]
        else:
            child = self.edge_to_child[u]
            val_pair = get_func(self.vid[child])
            return val_pair[0]
    
    def make_v(self, original_values: list, e, edge: bool = False):
        """元の順序の値を、HLD順に並べ替えた (forward, backward) のペアリストに変換する。

        セグメント木の初期化用データを作成する際に使用します。

        Args:
            original_values (list): 元の順序の値リスト。
                頂点クエリの場合は頂点 0, 1, ..., N-1 の値 (長さ N)。
                辺クエリの場合は入力された辺 0, 1, ..., M-1 の値 (長さ N-1)。
            e (T): 単位元。辺クエリで根に対応する位置を埋めるために使用。
            edge (bool): 辺重みのリストを作成する場合は True。

        Returns:
            list[tuple[T, T]]: セグ木構築用の (val, val) のリスト。
        """
        if not edge:
            # 頂点クエリの場合、頂点数とリストの長さが一致することを確認
            assert len(original_values) == self.n, f"Expected length {self.n}, but got {len(original_values)}"
            hld_ordered: list = [original_values[0]] * self.n # 型推論のための仮初期化
            for i, val in enumerate(original_values):
                hld_ordered[self.vid[i]] = val
        else:
            # 辺クエリの場合、根の補完用 e が必須であり、リストの長さは N-1 であることを確認
            if e is None: # assertの代わりに明示的なif
                raise ValueError("Edge queries require identity element e")
            assert len(original_values) == self.n - 1, f"Expected length {self.n-1}, but got {len(original_values)}"
            hld_ordered = [e] * self.n
            for i, val in enumerate(original_values):
                child = self.edge_to_child[i]
                hld_ordered[self.vid[child]] = val
                
        return [(x, x) for x in hld_ordered]
    
    @staticmethod
    def make_op(op):
        """非可換演算を (forward, backward) のペアで扱えるようにラップする。

        セグメント木の初期化時に渡す演算関数を作成します。
        forward は左から右 (a -> b)、backward は右から左 (b -> a) の順で演算を適用します。

        Args:
            op (Callable[[T, T], T]): 元の二項演算 (例: 行列の積、文字列の結合など)。

        Returns:
            Callable[[tuple[T, T], tuple[T, T]], tuple[T, T]]: 
                ペアを受け取りペアを返す、セグメント木用の二項演算関数。
        """
        return lambda a, b: (op(a[0], b[0]), op(b[1], a[1]))
    
    @staticmethod
    def make_e(e):
        """単位元を (forward, backward) のペアにする。

        セグメント木の初期化時に渡す単位元を作成します。

        Args:
            e (T): 元の演算における単位元。

        Returns:
            tuple[T, T]: (e, e) のペア。
        """
        return (e, e)
    
    @staticmethod
    def make_mapp(mapp):
        """作用関数を (forward, backward) ペア用にラップします。

        HLDで非可換なパスを扱う際、セグメント木のデータ S が (fwd, bwd) のペアになるため、
        単一の作用素 f を両方の要素に適用するように変換します。

        Args:
            mapp (Callable[[F, T], T]): 元の作用関数。
                第1引数に作用素 (F)、第2引数にデータ (T) を受け取り、新しいデータを返すもの。

        Returns:
            Callable[[F, Tuple[T, T]], Tuple[T, T]]: ラップされた作用関数。
        """
        return lambda f, x: (mapp(f, x[0]), mapp(f, x[1]))
    
    @staticmethod
    def make_comp(comp):
        """作用素の合成関数を、インターフェースの対称性のためにラップします。

        作用素 F は HLD によるペア化の影響を受けないため、基本的には引数をそのまま返します。

        Args:
            comp (Callable[[F, F], F]): 元の合成関数。
                第1引数に新しい作用素、第2引数に古い作用素を受け取り、合成された作用素を返すもの。

        Returns:
            Callable[[F, F], F]: 入力された合成関数をそのまま返します。
        """
        return comp
    
    @staticmethod
    def make_id(id):
        """作用素の単位元を、インターフェースの対称性のためにラップします。

        データ S と異なり、作用素 F はペア化されないため、値は変更されません。

        Args:
            f (F): 元の作用素の単位元 (identity element)。

        Returns:
            F: 入力された単位元をそのまま返します。
        """
        return id
    
# -----------------------------------------------------------------
# HLD 使用例 (Usage Examples)
# -----------------------------------------------------------------

"""
0. 初期化
"""
# hld = HLD(N, root)

# (u, v)に重みwの辺を追加
# hld.add_edge(u, v, w)

"""
1. 準備: セグメント木 (一点更新・パス集約・部分木集約)
   例: パス上の行列積や最大値など (非可換対応)
"""
# atcoder libのものを使う想定

# def op(a, b): return a+b
# e = 0
# S = SegTree(
#     hld.make_op(op),
#     hld.make_e(e),
#     hld.make_v(v, e)
# )


"""
2. 準備: 遅延セグメント木 (部分木更新・パス更新・部分木集約・パス集約)
   例: パス一括加算、パス一括塗りつぶし
"""
# atcoder libのものを使う想定

# def op(a, b): return a+b
# e = 0
# def mapp(f, x): return f+x
# def comp(f, g): return f+g
# id = 0
# S = LazySegTree(
#     hld.make_op(op),
#     hld.make_e(e),
#     hld.make_mapp(mapp),
#     hld.make_comp(comp),
#     hld.make_id(id),
#     hld.make_v(v, e)
# )


"""
3. 頂点クエリ
"""
# --- 値の更新 (一点) ---
# hld.set(u, S.set, x)

# --- パス集約 (u から v への順序を考慮) ---
# res = hld.prod_path(u, v, e, S.prod, op)

# --- 部分木集約 ---
# res = hld.prod_subtree(u, e, S.prod, op)

# --- パス一括更新 (遅延セグ木使用) ---
# hld.apply_path(u, v, x, S.apply)

# --- 部分木一括更新 (遅延セグ木使用) ---
# hld.apply_subtree(u, x, S.apply)


"""
4. 辺クエリ
   辺の値を「根から遠い方の頂点」に持たせて管理します。
   edge=True を指定することで LCA (頂点) を自動的に除外します。
"""

# --- 準備 (辺の初期値リストから HLD 順のペアリストを作成) ---
# S = SegTree(
#     hld.make_op(op),
#     hld.make_e(e),
#     hld.make_v(edge_weights, e, edge=True)
# )

# --- 辺の値の更新 (入力時の i 番目の辺を指定) ---
# hld.set_edge_by_id(i, S.set, new_w)

# --- パス上の辺の集約 ---
# res = hld.prod_path(u, v, e, S.prod, op, edge=True)

# --- 頂点 u の直下にある部分木内の辺をすべて更新 ---
# hld.apply_subtree(u, x, S.apply, edge=True)


"""
5. その他便利機能
"""
# --- LCA (最近共通祖先) ---
# lca = hld.get_lca(u, v)

# --- 距離 (重みなしエッジ数 / 重みあり距離) ---
# 辺に重みがない場合は同じ結果になる。
# dist_steps = hld.get_edge_dist(u, v)
# dist_weighted = hld.get_dist(u, v)

# --- K個上の祖先 (存在しなければ -1) ---
# anc = hld.kth_ancestor(u, k)

# --- パス上のジャンプ (u から v 方向へ k ステップ移動) ---
# target = hld.jump(u, v, k)