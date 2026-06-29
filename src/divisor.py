# name: Divisor
# prefix: divisor
# ---
def div(num):
    ret = []
    i = 1
    while i*i <= num:
        if num%i == 0:
            ret.append(i)
            if i*i < num: ret.append(num//i)
        i += 1
    ret.sort()
    return ret