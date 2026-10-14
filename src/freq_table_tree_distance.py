# name: Freq Table Tree Distance
# prefix: freq_table_tree_distance
# ---
def convolution_int(a: list[int], b: list[int]) -> list[int]:
    """非負整数配列の正確な整数畳み込み。"""
    if not a or not b:
        return []

    na, nb = len(a), len(b)
    need = na + nb - 1
    self_conv = a is b

    # 小さい畳み込みは愚直に計算
    if self_conv and (min(na, nb) <= 32 or na * nb <= 4096):
        c = [0] * need
        for i, x in enumerate(a):
            c[2 * i] += x * x
            for j in range(i + 1, na):
                c[i + j] += 2 * x * a[j]
        return c

    p1 = 998244353
    p2 = 1004535809
    root = 3

    size = 1 << (need - 1).bit_length()
    if size > (1 << 21):
        raise ValueError("NTT length exceeds supported size")


    def ntt(f, invert, mod):
        n = len(f)

        j = 0
        for i in range(1, n):
            bit = n >> 1
            while j & bit:
                j ^= bit
                bit >>= 1
            j ^= bit
            if i < j:
                f[i], f[j] = f[j], f[i]

        length = 2
        while length <= n:
            wlen = pow(root, (mod - 1) // length, mod)
            if invert:
                wlen = pow(wlen, mod - 2, mod)

            half = length >> 1
            for start in range(0, n, length):
                w = 1
                end = start + half
                for i in range(start, end):
                    u = f[i]
                    v = f[i + half] * w % mod

                    x = u + v
                    if x >= mod:
                        x -= mod
                    y = u - v
                    if y < 0:
                        y += mod

                    f[i] = x
                    f[i + half] = y
                    w = w * wlen % mod

            length <<= 1

        if invert:
            inv_n = pow(n, mod - 2, mod)
            for i in range(n):
                f[i] = f[i] * inv_n % mod

    def conv_mod(mod):
        fa = [x % mod for x in a]
        fa.extend([0] * (size - na))

        if self_conv:
            ntt(fa, False, mod)
            for i in range(size):
                fa[i] = fa[i] * fa[i] % mod
        else:
            fb = [x % mod for x in b]
            fb.extend([0] * (size - nb))

            ntt(fa, False, mod)
            ntt(fb, False, mod)

            for i in range(size):
                fa[i] = fa[i] * fb[i] % mod

        ntt(fa, True, mod)
        return fa[:need]

    c1 = conv_mod(p1)
    c2 = conv_mod(p2)

    # 2法による CRT
    inv_p1 = pow(p1, -1, p2)
    for i in range(need):
        c2[i] = c1[i] + p1 * ((c2[i] - c1[i]) * inv_p1 % p2)
    return c2

def FreqTableTreeDistance(N: int, E: list[list[int]]):
    res = [0]*N
    allq = [0]
    ng = [0]*N
    parent = [-1]*N
    size = [1] * N
    while allq:
        si = allq.pop()
        order = []
        parent[si] = -1
        stack = [(-1, si)]
        n = 0
        while stack:
            p, u = stack.pop()
            n += 1
            size[u] = 1
            order.append(u)
            for v in E[u]:
                if v == p or ng[v]:
                    continue
                parent[v] = u
                stack.append((u, v))
        if n == 1: continue
        ci = -1
        half_n = n // 2    
        for u in reversed(order):
            is_centroid = True
            for v in E[u]:
                if v == parent[u] or ng[v]:
                    continue
                if size[v] > half_n: is_centroid = False
                size[u] += size[v]        
            if n-size[u] > half_n: is_centroid = False
            if is_centroid:
                ci = u
                break
        ng[ci] = 1
        K = 0
        for si in E[ci]:
            if ng[si] == 0: K += 1
        if K <= 2: # 部分木間
            A = []
            first = True
            for si in E[ci]:
                if ng[si]: continue
                D = []
                q = [(-1, si, 1)]
                while q:
                    p, i, d = q.pop()
                    if len(D) < d+1: D.extend([0]*(d+1-len(D)))
                    D[d] += 1
                    res[d] += 2
                    for j in E[i]:
                        if j == p or ng[j]: continue
                        q.append((i, j, d+1))
                if not first:
                    C = convolution_int(A, D)
                    for i in range(1, min(len(C), N)):
                        res[i] += 2*C[i]
                first = False
                if len(A) < len(D): A.extend([0]*(len(D)-len(A)))
                for i in range(1, len(D)):
                    A[i] += D[i]            
                allq.append(si)
        else: # 自己畳み込み
            A = [1]
            for si in E[ci]:
                if ng[si]: continue
                D = []
                q = [(-1, si, 1)]
                while q:
                    p, i, d = q.pop()
                    if len(D) < d+1: D.extend([0]*(d+1-len(D)))
                    if len(A) < d+1: A.extend([0]*(d+1-len(A)))
                    A[d] += 1
                    D[d] += 1
                    for j in E[i]:
                        if j == p or ng[j]: continue
                        q.append((i, j, d+1))
                DD = convolution_int(D, D)
                for i in range(1, min(len(DD), N)):
                    res[i] -= DD[i]
                allq.append(si)
            AA = convolution_int(A, A)
            for i in range(1, min(len(AA), N)):
                res[i] += AA[i]
    for i in range(N): res[i] //= 2
    return res
