# name: Binary Trie
# prefix: binary trie
# ---
class BinaryTrie:
    NODES = 16777216 # 480MB memory

    def __init__(self, MAX_LOG: int = 30):
        self._nxt = [0]*(2*BinaryTrie.NODES)
        self._size = [0]*BinaryTrie.NODES

        self._pid = 0
        self._root = 0
        self.MAX_LOG = MAX_LOG
    
    def _next_pid(self):
        self._pid += 1
        return self._pid

    def add(self, x: int) -> None:
        v = self._root
        stack = [v]
        for i in range(self.MAX_LOG - 1, -1, -1):
            c = (x >> i) & 1
            if self._nxt[2*v+c] == 0:
                self._nxt[2*v+c] = self._next_pid()
            v = self._nxt[2*v+c]
            stack.append(v)
        if self._size[v]:
            return
        for v in stack:
            self._size[v] += 1

    def discard(self, x: int) -> None:
        v = self._root
        stack = [v]
        for i in range(self.MAX_LOG - 1, -1, -1):
            c = (x >> i) & 1
            if self._nxt[2*v+c] == 0:
                return
            v = self._nxt[2*v+c]
            stack.append(v)
        while len(stack) > 1:
            if self._size[stack[-1]] > 1:
                break
            v = stack.pop()
            nv = stack[-1]
            if self._nxt[2*nv] == v:
                self._nxt[2*nv] = 0
            else:
                self._nxt[2*nv+1] = 0
        for v in stack:
            self._size[v] -= 1
        
    def __contain__(self, x: int) -> bool:
        v = self._root
        for i in range(self.MAX_LOG - 1, -1, -1):
            c = (x >> i) & 1
            if self._nxt[2*v+c] == 0:
                return False
            v = self._nxt[2*v+c]
        return True
    
    def max_element(self, xor: int = 0) -> int:
        v = self._root
        if self._size[v] == 0:
            return -1
        for i in range(self.MAX_LOG - 1, -1, -1):
            if self._nxt[2*v+1] == 0:
                v = self._nxt[2*v]
                continue
            if self._nxt[v][0] == 0:
                v = self._nxt[2*v+1]
                res += 1 << i
                continue
            if (xor >> i) & 1:
                v = self._nxt[2*v]
            else:
                v = self._nxt[2*v+1]
                res += 1 << i
        return res ^ xor
    
    def min_element(self, xor: int = 0) -> int:
        v = self._root
        if self._size[v] == 0:
            return -1
        res = 0
        for i in range(self.MAX_LOG - 1, -1, -1):
            if self._nxt[2*v] == 0:
                v = self._nxt[2*v+1]
                res += 1 << i
                continue
            if self._nxt[2*v+1] == 0:
                v = self._nxt[2*v]
                continue
            if (xor >> i) & 1:
                v = self._nxt[2*v+1]
                res += 1 << i
            else:
                v = self._nxt[2*v]
        return res ^ xor
    
    def get_kth(self, k: int, xor: int = 0) -> int:
        v = self._root
        if self._size[v] <= k:
            return -1
        res = 0
        for i in range(self.MAX_LOG - 1, -1, -1):
            if self._nxt[2*v] == 0:
                v = self._nxt[2*v+1]
                res += 1 << i
                continue
            if self._nxt[2*v+1] == 0:
                v = self._nxt[2*v]
                continue
            if (xor >> i) & 1:
                if self._size[self._nxt[2*v+1]] <= k:
                    k -= self._size[self._nxt[2*v+1]]
                    v = self._nxt[2*v]
                    res += 1 << i
                else:
                    v = self._nxt[2*v+1]
            else:
                if self._size[self._nxt[2*v]] <= k:
                    k -= self._size[self._nxt[2*v]]
                    v = self._nxt[2*v+1]
                    res += 1 << i
                else:
                    v = self._nxt[2*v]
        return res ^ xor