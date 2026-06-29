# name: Persistant LazySegTree
# prefix: persistant lazysegtree
# ---
class Node[T, F]:
    l: Node[T, F]
    r: Node[T, F]
    x: T
    lazy: F
    def __init__(self, x: T, _id: F):
        self.x = x
        self.lazy = _id
        self.l = self
        self.r = self
    
    def __repr__(self) -> str:
        return f"({self.x}, {self.lazy})"

# https://nyaannyaan.github.io/library/segment-tree/persistent-segment-tree.hpp
class PersistantSegTree[T, OP, F, MP, CP]:
    _op: OP
    _e: T
    _mapp: MP
    _comp: CP
    _id: F
    _nil: Node[T, F]
    _roots: list[Node[T, F]]
    _nodes: list[Node[T, F]]
    _n: int

    def __init__(self, op: OP, e: T, mapp: MP, comp: CP, _id: F, v) -> None:
        self._op = op
        self._e = e
        self._mapp = mapp
        self._comp = comp
        self._id = _id
        self._roots = []

        self._nil = Node[T, F](e, _id)
        self._nodes = []

        if isinstance(v, int):
            self._n = v
            self._roots.append(self._nil)
        else:
            self._n = len(v)
            self._roots.append(self._build(v))

    def latest_root(self) -> Node[T, F]:
        return self._roots[-1]
    
    def latest_root_id(self) -> int:
        return len(self._roots)-1
    
    def _clone(self, n: Node[T, F]) -> Node[T, F]:
        node = Node[T, F](n.x, n.lazy)
        node.l = n.l
        node.r = n.r
        self._nodes.append(node)
        return node

    def _new(self, x: T) -> Node[T, F]:
        node = Node[T, F](x, self._id)
        node.l = node.r = self._nil
        self._nodes.append(node)
        return node
    
    def _new(self, x: T, lazy: F) -> Node[T, F]:
        node = Node[T, F](x, lazy)
        node.l = node.r = self._nil
        self._nodes.append(node)
        return node
    
    def _merge(self, left: Node[T, F], right: Node[T, F]) -> Node[T, F]:
        node = self._new(self._op(left.x, right.x))
        node.l = left
        node.r = right
        self._eval(node)
        return node

    def _build(self, v: list[T]) -> Node[T, F]:
        return self._build_lr(0, self._n, v)
    
    def _build_lr(self, l: int, r: int, v: list[T]) -> Node[T, F]:
        if l+1 == r: return self._new(v[l])
        m = (l+r)>>1
        return self._merge(self._build_lr(l, m, v), self._build_lr(m, r, v))

    # private
    def _eval(self, n: Node[T, F]) -> None:
        if n.lazy == self._id: return
        left = self._clone(n.l)
        right = self._clone(n.r)
        left.lazy = self._comp(n.lazy, left.lazy)
        right.lazy = self._comp(n.lazy, right.lazy)
        n.x = self._mapp(n.lazy, n.x)
        n.lazy = self._id
        n.l = left
        n.r = right

    def _set(self, p: int, x: T, n: Node[T, F], l: int, r: int) -> Node[T, F]:
        self._eval(n)
        if l+1 == r: return self._new(x)
        m = (l+r)>>1
        if p < m:
            return self._merge(self._set(p, x, n.l, l, m), n.r)
        else:
            return self._merge(n.l, self._set(p, x, n.r, m, r))
    
    def _get(self, p: int, n: Node[T, F], l: int, r: int) -> T:
        self._eval(n)
        if l+1 == r: return n.x
        m = (l+r)>>1
        if p < m:
            return self._get(p, n.l, l, m)
        else:
            return self._get(p, n.r, m, r)

    def _add(self, p: int, x: T, n: Node[T, F], l, r) -> Node[T, F]:
        self._eval(n)
        if l+1 == r: return self._new(self._op(n.x, x))
        m = (l+r)>>1
        if p < m:
            return self._merge(self._add(p, x, n.l, l, m), n.r)
        else:
            return self._merge(n.l, self._add(p, x, n.r, m, r))
    
    def _prod(self, a: int, b: int, n: Node[T, F], l: int, r: int) -> T:
        if n is self._nil: return self._e
        self._eval(n)
        if r <= a or b <= l: return self._e
        if a <= l and r <= b: return n.x
        m = (l+r)>>1
        return self._op(self._prod(a, b, n.l, l, m), self._prod(a, b, n.r, m, r))
    
    def _apply(self, a: int, b: int, n: Node[T, F], f: F, l: int, r: int) -> Node[T, F]:
        self._eval(n)
        if r <= a or b <= l: return n
        if a <= l and r <= b:
            node = self._clone(n)
            node.lazy = f
            self._eval(node)
            return node
        m = (l+r)>>1
        return self._merge(self._apply(a, b, n.l, f, l, m), self._apply(a, b, n.r, f, m, r))

    def _copy(self, a: int, b: int, fr: Node[T, F], to: Node[T, F], l: int, r: int):
        if r <= a or b <= l: return to
        if a <= l and r <= b: return fr
        m = (l+r)>>1
        return self._merge(self._copy(a, b, fr.l, to.l, l, m), self._copy(a, b, fr.r, to.r, m, r))
    
    # get
    def get(self, n: Node[T, F], p: int) -> T:
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
    def set(self, n: Node[T, F], p: int, x: T) -> int:
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
    def add(self, n: Node[T, F], p: int, x: T) -> int:
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
    def prod(self, n: Node[T, F], l: int, r: int) -> T:
        assert 0 <= l < r <= self._n
        return self._prod(l, r, n, 0, self._n)
    
    def prod(self, t: int, l: int, r: int) -> T:
        assert 0 <= t < len(self._roots)
        assert 0 <= l < r <= self._n
        return self._prod(l, r, self._roots[t], 0, self._n)
    
    def prod(self, l: int, r: int) -> T:
        assert 0 <= l < r <= self._n
        return self._prod(l, r, self._roots[-1], 0, self._n)
    
    # apply
    def apply(self, n: Node[T, F], l: int, r: int, f: F) -> int:
        assert 0 <= l < r <= self._n
        root = self._apply(l, r, n, f, 0, self._n)
        pid = len(self._roots)
        self._roots.append(root)
        return pid
    
    def apply(self, t: int, l: int, r: int, f: F) -> int:
        assert 0 <= t < len(self._roots)
        assert 0 <= l < r <= self._n
        root = self._apply(l, r, self._roots[t], f, 0, self._n)
        pid = len(self._roots)
        self._roots.append(root)
        return pid
    
    def apply(self, l: int, r: int, f: F) -> int:
        assert 0 <= l < r <= self._n
        root = self._apply(l, r, self._roots[-1], f, 0, self._n)
        pid = len(self._roots)
        self._roots.append(root)
        return pid
    
    # copy
    def copy(self, fr: Node[T, F], to: Node[T, F], l: int, r: int) -> int:
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