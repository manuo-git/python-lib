# name: Trie
# prefix: trie
# ---
nxt = [{}]
node = [0]

def insert(st):
    n = len(st)
    cur = 0
    for i in range(n):
        c = st[i]
        if c not in nxt[cur]:
            nxt[cur][c] = len(nxt)
            nxt.append({})
            node.append(0)
        cur = nxt[cur][c]