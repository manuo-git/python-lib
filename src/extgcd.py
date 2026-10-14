# name: Extended GCD
# prefix: extgcd
# ---
# https://github.com/manuo-git/python-lib/blob/main/src/extgcd.py
def extgcd(a, b) -> tuple[int, int]:
    if b == 0: return 1, 0
    y, x = extgcd(b, a%b)
    y -= (a//b)*x
    return x, y