# name: Trie
# prefix: trie
# ---
nxt = [{}]
node = [0]

def new_node():
    node.append(0)

def middle(cur):
    node[cur] += 1

def last(cur):
    node[cur] += 1

def next_cur(cur, c):
    if c not in nxt[cur]:
        nxt[cur][c] = len(nxt)
        nxt.append({})
        new_node()
    return nxt[cur][c]

def insert(st):
    n = len(st)
    cur = 0
    for i in range(n):
        c = st[i]
        middle(cur)
        cur = next_cur(cur, c)
    last(cur)