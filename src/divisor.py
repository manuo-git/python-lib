# name: Divisor
# prefix: divisor
# ---
# https://github.com/manuo-git/python-lib/blob/main/src/divisor.py
def div(num):
    left = []
    right = []
    i = 1
    while i*i <= num:
        if num%i == 0:
            left.append(i)
            if i*i < num: right.append(num//i)
        i += 1
    ret = left + right[::-1]
    return ret