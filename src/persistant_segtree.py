# name: Persistant SegTree
# prefix: persistant segtree
# ---
class Node[T]:
    l: Node[T]
    r: Node[T]
    x: T
    def __init__(self, x: T):
        self.x = x
        self.l = self
        self.r = self

# https://nyaannyaan.github.io/library/segment-tree/persistent-segment-tree.hpp
class PersistantSegTree[T, F]:
    _op: F
    _e: T
    _nil: Node[T]
    _roots: list[Node[T]]
    _nodes: list[Node[T]]
    _n: int

    def __init__(self, op: F, e: T, v) -> None:
        self._op = op
        self._e = e
        self._roots = []

        self._nil = Node[T](e)
        self._nodes = []

        if isinstance(v, int):
            self._n = v
            self._roots.append(self._nil)
        else:
            self._n = len(v)
            self._roots.append(self._build(v))

    def latest_root(self) -> Node[T]:
        return self._roots[-1]
    
    def latest_root_id(self) -> int:
        return len(self._roots)-1

    def _new(self, x: T) -> Node[T]:
        node = Node[T](x)
        node.l = node.r = self._nil
        self._nodes.append(node)
        return node
    
    def _merge(self, left: Node[T], right: Node[T]) -> Node[T]:
        node = self._new(self._op(left.x, right.x))
        node.l = left
        node.r = right
        return node

    def _build(self, v: list[T]) -> Node[T]:
        return self._build_lr(0, self._n, v)
    
    def _build_lr(self, l: int, r: int, v: list[T]) -> Node[T]:
        if l+1 == r: return self._new(v[l])
        m = (l+r)>>1
        return self._merge(self._build_lr(l, m, v), self._build_lr(m, r, v))

    def _set(self, p: int, x: T, n: Node[T], l: int, r: int) -> Node[T]:
        if l+1 == r: return self._new(x)
        m = (l+r)>>1
        if p < m:
            return self._merge(self._set(p, x, n.l, l, m), n.r)
        else:
            return self._merge(n.l, self._set(p, x, n.r, m, r))
    
    def _get(self, p: int, n: Node[T], l: int, r: int) -> T:
        if l+1 == r: return n.x
        m = (l+r)>>1
        if p < m:
            return self._get(p, n.l, l, m)
        else:
            return self._get(p, n.r, m, r)

    def _add(self, p: int, x: T, n: Node[T], l, r) -> Node[T]:
        if l+1 == r: return self._new(self._op(n.x, x))
        m = (l+r)>>1
        if p < m:
            return self._merge(self._add(p, x, n.l, l, m), n.r)
        else:
            return self._merge(n.l, self._add(p, x, n.r, m, r))
    
    def _prod(self, a: int, b: int, n: Node[T], l: int, r: int) -> T:
        if n is self._nil: return self._e
        if r <= a or b <= l: return self._e
        if a <= l and r <= b: return n.x
        m = (l+r)>>1
        return self._op(self._prod(a, b, n.l, l, m), self._prod(a, b, n.r, m, r))
    
    def _copy(self, a: int, b: int, fr: Node[T], to: Node[T], l: int, r: int):
        if r <= a or b <= l: return to
        if a <= l and r <= b: return fr
        m = (l+r)>>1
        return self._merge(self._copy(a, b, fr.l, to.l, l, m), self._copy(a, b, fr.r, to.r, m, r))
    
    # get
    def get(self, n: Node[T], p: int) -> T:
        assert 0 <= p < self._n
        return self._get(p, n, 0, self._n)
    
    def get(self, t: int, p: int) -> T:
        assert 0 <= t < len(self._roots)
        assert 0 <= p < self._n
        return self._get(p, self._roots[t], 0, self._n)
    
    def get(self, p: int) -> T:
        assert 0 <= p < self._n
        return self._get(p, self._roots[-1], 0, self._n)

    # set
    def set(self, n: Node[T], p: int, x: T) -> int:
        assert 0 <= p < self._n
        root = self._set(p, x, n, 0, self._n)
        pid = len(self._roots)
        self._roots.append(root)
        return pid
    
    def set(self, t: int, p: int, x: T) -> int:
        assert 0 <= t < len(self._roots)
        assert 0 <= p < self._n
        root = self._set(p, x, self._roots[t], 0, self._n)
        pid = len(self._roots)
        self._roots.append(root)
        return pid

    def set(self, p: int, x: T) -> int:
        assert 0 <= p < self._n
        root = self._set(p, x, self._roots[-1], 0, self._n)
        pid = len(self._roots)
        self._roots.append(root)
        return pid
    
    # add
    def add(self, n: Node[T], p: int, x: T) -> int:
        assert 0 <= p < self._n
        root = self._add(p, x, n, 0, self._n)
        pid = len(self._roots)
        self._roots.append(root)
        return pid
    
    def add(self, t: int, p: int, x: T) -> int:
        assert 0 <= t < len(self._roots)
        assert 0 <= p < self._n
        root = self._add(p, x, self._roots[t], 0, self._n)
        pid = len(self._roots)
        self._roots.append(root)
        return pid

    def add(self, p: int, x: T) -> int:
        assert 0 <= p < self._n
        root = self._add(p, x, self._roots[-1], 0, self._n)
        pid = len(self._roots)
        self._roots.append(root)
        return pid

    # prod
    def prod(self, n: Node[T], l: int, r: int) -> T:
        assert 0 <= l < r <= self._n
        return self._prod(l, r, n, 0, self._n)
    
    def prod(self, t: int, l: int, r: int) -> T:
        assert 0 <= t < len(self._roots)
        assert 0 <= l < r <= self._n
        return self._prod(l, r, self._roots[t], 0, self._n)
    
    def prod(self, l: int, r: int) -> T:
        assert 0 <= l < r <= self._n
        return self._prod(l, r, self._roots[-1], 0, self._n)
    
    # copy
    def copy(self, fr: Node[T], to: Node[T], l: int, r: int) -> int:
        assert 0 <= l < r <= self._n
        root = self._copy(l, r, fr, to, 0, self._n)
        pid = len(self._roots)
        self._roots.append(root)
        return pid
    
    def copy(self, fr: int, to: int, l: int, r: int) -> int:
        assert 0 <= fr < len(self._roots)
        assert 0 <= to < len(self._roots)
        assert 0 <= l < r <= self._n
        root = self._copy(l, r, self._roots[fr], self._roots[to], 0, self._n)
        pid = len(self._roots)
        self._roots.append(root)
        return pid