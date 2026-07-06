# name: Convex Hull
# prefix: convexhull
# ---
# https://atcoder.jp/contests/awc0103/editorial/22410
def sub(p1, p2):
    return (p1[0]-p2[0], p1[1]-p2[1])

# 符号付き面積の2倍
def signed_area_vector(v1, v2):
    area = v1[0]*v2[1] - v2[0]*v1[1]
    return area

# x座標最小の点から反時計回り
def convex_hull_list(p_list):
    assert len(p_list) >= 3
    p_list.sort()
    res = []
    k = 0
    for p in p_list:
        while k >= 2 and signed_area_vector(sub(res[k-1], res[k-2]), sub(p, res[k-1])) <= 0:
            res.pop()
            k -= 1
        res.append(p)
        k += 1
    t = k+1
    for p in p_list[:-1][::-1]:
        while k >= t and signed_area_vector(sub(res[k-1], res[k-2]), sub(p, res[k-1])) <= 0:
            res.pop()
            k -= 1
        res.append(p)
        k += 1
    res.pop()
    return res

# 2倍の面積。座標が整数の場合整数になる。
def area_convex_hull(p_list):
    res = convex_hull_list(p_list)
    ans = sum(signed_area_vector(res[i], res[(i+1)%len(res)]) for i in range(len(res)))
    return abs(ans)