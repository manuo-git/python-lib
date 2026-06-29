# name: Aho-Corasick
# prefix: aho corasick
# ---
# https://atcoder.jp/contests/abc419/editorial/13623
class AhoCorasick:
    def __init__(self, sigma=26):
        self.node = [[-1] * sigma]
        self.last = [0]
        self.sigma = sigma
    def add(self, arr, ID):
        v = 0
        for c in arr:
            if self.node[v][c] == -1:
                self.node[v][c] = len(self.node)
                self.node.append([-1] * self.sigma)
                self.last.append(0)
            v = self.node[v][c]
        self.last[v] |= 1 << ID
    def build(self):
        link = [0] * len(self.node)
        que = deque()
        for i in range(self.sigma):
            if self.node[0][i] == -1:
                self.node[0][i] = 0
            else:
                link[self.node[0][i]] = 0
                que.append(self.node[0][i])
        while que:
            v = que.popleft()
            self.last[v] |= self.last[link[v]]
            for i in range(self.sigma):
                u = self.node[v][i]
                if u == -1:
                    self.node[v][i] = self.node[link[v]][i]
                else:
                    link[u] = self.node[link[v]][i]
                    que.append(u)
    def __len__(self) -> int: return len(self.node)
    def to(self, fr: int, i: int) -> int:
        assert 0 <= fr < len(self.node)
        assert 0 <= i < self.sigma
        return self.node[fr][i]
    def state(self, i: int) -> int:
        assert 0 <= i < len(self.last)
        return self.last[i]