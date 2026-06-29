# name: Prev Permutations
# prefix: prevpermutations
# ---
def prev_permutations(li):
    n = len(li)
    for i in reversed(range(1, n)):
        if li[i-1] > li[i]:
            ch = i-1
            break
    else:
        return False
    for i in reversed(range(ch+1, n)):
        if li[i] < li[ch]:
            li[i], li[ch] = li[ch], li[i]
            break
    for i in range(ch+1, n):
        j = n-(i-ch-1)-1
        if i >= j: break
        li[i], li[j] = li[j], li[i]
    return True