# name: SegTree Beats
# prefix: segtreebeats
# ---
import sys
sys.setrecursionlimit(10**6)

class SegTreeBeats:
    """Segment Tree Beatsの実装。

    区間chmin, 区間chmax, 区間加算, 区間更新, 区間和, 区間最大・最小クエリを
    すべてO(log N)またはO(log^2 N)で処理するデータ構造です。

    Attributes:
        n (int): 元の配列の要素数。
        size (int): セグメント木の葉の数(n以上の最小の2の累乗)。
        max1 (list[int]): 各ノードの範囲内における最大値。
        max2 (list[int]): 各ノードの範囲内における厳密に2番目に大きい値(存在しない場合は-INF)。
        max_c (list[int]): 最大値(max1)の出現回数。
        min1 (list[int]): 各ノードの範囲内における最小値。
        min2 (list[int]): 各ノードの範囲内における厳密に2番目に小さい値(存在しない場合はINF)。
        min_c (list[int]): 最小値(min1)の出現回数。
        sum (list[int]): 各ノードの範囲内の合計値。
        lazy_add (list[int]): 加算クエリ用の遅延評価フラグ。
        INF (int): 無限大を表す定数。
    """
    INF: int
    n: int
    size: int
    max1: list[int]
    max2: list[int]
    max_c: list[int]
    min1: list[int]
    min2: list[int]
    min_c: list[int]
    sum: list[int]
    lazy_add: list[int]

    def __init__(self, n: int, arr = None):
        """SegmentTreeBeatsを初期化する。

        Args:
            n (int): 配列のサイズ。
            arr (Optional[Iterable[int]], optional): 初期データ。
                map(int, input().split()) などのイテラブルも受け付けます。
        """
        self.INF = 1 << 60
        self.n = n
        self.size = 1
        while self.size < n: 
            self.size *= 2
        
        self.max1 = [-self.INF] * (2 * self.size)
        self.max2 = [-self.INF] * (2 * self.size)
        self.max_c = [0] * (2 * self.size)
        
        self.min1 = [self.INF] * (2 * self.size)
        self.min2 = [self.INF] * (2 * self.size)
        self.min_c = [0] * (2 * self.size)
        
        self.sum = [0] * (2 * self.size)
        self.lazy_add = [0] * (2 * self.size)
        
        if arr is not None:
            data = list(arr)
            for i, x in enumerate(data):
                idx = i + self.size
                self.max1[idx] = self.min1[idx] = self.sum[idx] = x
                self.max_c[idx] = self.min_c[idx] = 1
            for i in range(self.size - 1, 0, -1):
                self._update(i)

    def _update(self, k: int):
        left, right = 2 * k, 2 * k + 1
        self.sum[k] = self.sum[left] + self.sum[right]
        
        if self.max1[left] > self.max1[right]:
            self.max1[k] = self.max1[left]
            self.max_c[k] = self.max_c[left]
            m2l, m1r = self.max2[left], self.max1[right]
            self.max2[k] = m2l if m2l > m1r else m1r
        elif self.max1[left] < self.max1[right]:
            self.max1[k] = self.max1[right]
            self.max_c[k] = self.max_c[right]
            m1l, m2r = self.max1[left], self.max2[right]
            self.max2[k] = m1l if m1l > m2r else m2r
        else:
            self.max1[k] = self.max1[left]
            self.max_c[k] = self.max_c[left] + self.max_c[right]
            m2l, m2r = self.max2[left], self.max2[right]
            self.max2[k] = m2l if m2l > m2r else m2r

        if self.min1[left] < self.min1[right]:
            self.min1[k] = self.min1[left]
            self.min_c[k] = self.min_c[left]
            m2l, m1r = self.min2[left], self.min1[right]
            self.min2[k] = m2l if m2l < m1r else m1r
        elif self.min1[left] > self.min1[right]:
            self.min1[k] = self.min1[right]
            self.min_c[k] = self.min_c[right]
            m1l, m2r = self.min1[left], self.min2[right]
            self.min2[k] = m1l if m1l < m2r else m2r
        else:
            self.min1[k] = self.min1[left]
            self.min_c[k] = self.min_c[left] + self.min_c[right]
            m2l, m2r = self.min2[left], self.min2[right]
            self.min2[k] = m2l if m2l < m2r else m2r

    def _apply_add(self, k: int, x: int, il: int, ir: int):
        self.max1[k] += x
        if self.max2[k] != -self.INF: self.max2[k] += x
        self.min1[k] += x
        if self.min2[k] != self.INF: self.min2[k] += x
        self.sum[k] += x * (ir - il)
        self.lazy_add[k] += x

    def _push_chmin(self, k: int, x: int):
        if self.max1[k] <= x: return
        self.sum[k] -= (self.max1[k] - x) * self.max_c[k]
        if self.min1[k] == self.max1[k]: self.min1[k] = x
        elif self.min2[k] == self.max1[k]: self.min2[k] = x
        self.max1[k] = x

    def _push_chmax(self, k: int, x: int):
        if self.min1[k] >= x: return
        self.sum[k] += (x - self.min1[k]) * self.min_c[k]
        if self.max1[k] == self.min1[k]: self.max1[k] = x
        elif self.max2[k] == self.min1[k]: self.max2[k] = x
        self.min1[k] = x

    def _push(self, k: int, il: int, ir: int):
        mid = (il + ir) // 2
        if self.lazy_add[k] != 0:
            self._apply_add(2 * k, self.lazy_add[k], il, mid)
            self._apply_add(2 * k + 1, self.lazy_add[k], mid, ir)
            self.lazy_add[k] = 0
        self._push_chmin(2 * k, self.max1[k])
        self._push_chmin(2 * k + 1, self.max1[k])
        self._push_chmax(2 * k, self.min1[k])
        self._push_chmax(2 * k + 1, self.min1[k])

    def range_add(self, l: int, r: int, x: int):
        """区間 [l, r) の各要素に x を加算する。

        Args:
            l (int): 開始インデックス(0-indexed)。
            r (int): 終了インデックス(開区間)。
            x (int): 加算する値(負数も可)。
        """
        self._range_add(l, r, x, 1, 0, self.size)

    def _range_add(self, l: int, r: int, x: int, k: int, il: int, ir: int):
        if ir <= l or r <= il: return
        if l <= il and ir <= r:
            self._apply_add(k, x, il, ir)
            return
        self._push(k, il, ir)
        mid = (il + ir) // 2
        self._range_add(l, r, x, 2 * k, il, mid)
        self._range_add(l, r, x, 2 * k + 1, mid, ir)
        self._update(k)

    def range_chmin(self, l: int, r: int, x: int):
        """区間 [l, r) の各要素 a_i を min(a_i, x) に更新する。

        Args:
            l (int): 開始インデックス(0-indexed)。
            r (int): 終了インデックス(開区間)。
            x (int): 比較する値。
        """
        self._range_chmin(l, r, x, 1, 0, self.size)

    def _range_chmin(self, l: int, r: int, x: int, k: int, il: int, ir: int):
        if ir <= l or r <= il or self.max1[k] <= x: return
        if l <= il and ir <= r and self.max2[k] < x:
            self._push_chmin(k, x)
            return
        self._push(k, il, ir)
        mid = (il + ir) // 2
        self._range_chmin(l, r, x, 2 * k, il, mid)
        self._range_chmin(l, r, x, 2 * k + 1, mid, ir)
        self._update(k)

    def range_chmax(self, l: int, r: int, x: int):
        """区間 [l, r) の各要素 a_i を max(a_i, x) に更新する。

        Args:
            l (int): 開始インデックス(0-indexed)。
            r (int): 終了インデックス(開区間)。
            x (int): 比較する値。
        """
        self._range_chmax(l, r, x, 1, 0, self.size)

    def _range_chmax(self, l: int, r: int, x: int, k: int, il: int, ir: int):
        if ir <= l or r <= il or self.min1[k] >= x: return
        if l <= il and ir <= r and self.min2[k] > x:
            self._push_chmax(k, x)
            return
        self._push(k, il, ir)
        mid = (il + ir) // 2
        self._range_chmax(l, r, x, 2 * k, il, mid)
        self._range_chmax(l, r, x, 2 * k + 1, mid, ir)
        self._update(k)

    def range_update(self, l: int, r: int, x: int):
        """区間 [l, r) の各要素を x に更新(代入)する。

        内部的には range_chmax と range_chmin を組み合わせて実現。

        Args:
            l (int): 開始インデックス(0-indexed)。
            r (int): 終了インデックス(開区間)。
            x (int): 代入する値。
        """
        self.range_chmax(l, r, x)
        self.range_chmin(l, r, x)

    def range_sum(self, l: int, r: int) -> int:
        """区間 [l, r) の合計値を計算する。

        Args:
            l (int): 開始インデックス(0-indexed)。
            r (int): 終了インデックス(開区間)。

        Returns:
            int: 区間和。
        """
        return self._range_sum(l, r, 1, 0, self.size)

    def _range_sum(self, l: int, r: int, k: int, il: int, ir: int) -> int:
        if ir <= l or r <= il: return 0
        if l <= il and ir <= r: return self.sum[k]
        self._push(k, il, ir)
        mid = (il + ir) // 2
        return self._range_sum(l, r, 2 * k, il, mid) + self._range_sum(l, r, 2 * k + 1, mid, ir)
    
    def range_max(self, l: int, r: int) -> int:
        """区間 [l, r) の最大値を取得する。

        Args:
            l (int): 開始インデックス(0-indexed)。
            r (int): 終了インデックス(開区間)。

        Returns:
            int: 区間内の最大値。
        """
        return self._range_max(l, r, 1, 0, self.size)
    
    def _range_max(self, l: int, r: int, k: int, il: int, ir: int) -> int:
        if ir <= l or r <= il: return -self.INF
        if l <= il and ir <= r: return self.max1[k]
        self._push(k, il, ir)
        mid = (il + ir) // 2
        left = self._range_max(l, r, 2 * k, il, mid)
        right = self._range_max(l, r, 2 * k + 1, mid, ir)
        return left if left >= right else right

    def range_min(self, l: int, r: int) -> int:
        """区間 [l, r) の最小値を取得する。

        Args:
            l (int): 開始インデックス(0-indexed)。
            r (int): 終了インデックス(開区間)。

        Returns:
            int: 区間内の最小値。
        """
        return self._range_min(l, r, 1, 0, self.size)
    
    def _range_min(self, l: int, r: int, k: int, il: int, ir: int) -> int:
        if ir <= l or r <= il: return self.INF
        if l <= il and ir <= r: return self.min1[k]
        self._push(k, il, ir)
        mid = (il + ir) // 2
        left = self._range_min(l, r, 2 * k, il, mid)
        right = self._range_min(l, r, 2 * k + 1, mid, ir)
        return left if left <= right else right
    
    def get(self, i: int) -> int:
        """インデックス i の要素の値を取得する。

        内部的には区間和クエリ range_sum(i, i+1) を利用して一点の値を取得します。
        この際、対象要素までのパス上にある遅延フラグがすべて解消(push)されます。

        Args:
            i (int): 取得したい要素のインデックス(0-indexed)。

        Returns:
            int: インデックス i の要素の現在の値。
        """
        return self._range_sum(i, i+1, 1, 0, self.size)
    
    def set(self, i: int, x: int) -> None:
        """インデックス i の要素の値を x に更新(代入)する。

        内部的には区間代入クエリ range_update(i, i+1, x) を利用します。
        chmin と chmax を組み合わせることで、Beatsの不変条件を維持しながら
        安全に一点更新を行います。

        Args:
            i (int): 更新したい要素のインデックス(0-indexed)。
            x (int): 代入する新しい値。
        """
        self.range_update(i, i+1, x)