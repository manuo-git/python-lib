# name: Codon Macro
# prefix: macro_codon
# ---
from collections import deque, defaultdict, Counter
from bisect import bisect_left, bisect_right
from itertools import permutations, combinations, groupby
from heapq import heappop, heappush
import math, sys
def printl(li, sep=" "): print(sep.join(map(str, li)))
def yn(flag): print(Yes if flag else No)
_int = lambda x: int(x)-1
INF = 1<<60
Yes, No = "Yes", "No"

#mapの返り値をlist(map)で固定
import internal.static as _internal_static
def map(f, *args) -> list:
    if _internal_static.len(args) == 0:
        compile_error("map() expects at least one iterator")
    elif _internal_static.len(args) == 1:
        return [f(a) for a in args[0]]
    else:
        return [f(*a) for a in zip(*args)]

#int同士の除算結果をPythonの負の無限大丸めに合わせる
@extend
class int:
    @pure
    @llvm
    def _floordiv_int_int(self: int, other: int) -> int:
        %0 = sdiv i64 %self, %other
        ret i64 %0
    @overload
    def __floordiv__(self, other: int):
        d = self._floordiv_int_int(other)
        m = self - d * other
        if m and ((other ^ m) < 0):
            d -= 1
        return d
    @pure
    @llvm
    def _mod_int_int(self: int, other: int) -> int:
        %0 = srem i64 %self, %other
        ret i64 %0
    @overload
    def __mod__(self, other: int) -> int:
        m = self._mod_int_int(other)
        if m and ((other ^ m) < 0):
            m += other
        return m

#Int[N](N <= 128)同士の除算結果をPythonの負の無限大丸めに合わせる
@extend
class Int:
    def __floordiv__(self, other: Int[N]) -> Int[N]:
        if N > 128:
            compile_error("division is not supported on Int[N] when N > 128")
        d = self._floordiv(other)
        m = self - d * other
        if m and ((other ^ m) < Int[N](0)):
            d -= Int[N](1)
        return d
    def __mod__(self, other: Int[N]) -> Int[N]:
        if N > 128:
            compile_error("modulus is not supported on Int[N] when N > 128")
        m = self._mod(other)
        if m and ((other ^ m) < Int[N](0)):
            m += other
        return m

#int.bit_length, int.bit_countに対応
@extend
class int:
    def bit_length(self): 
        return 64 - abs(self).__ctlz__()
    def bit_count(self):
        return abs(self).__ctpop__()

#floatの出力桁数を15桁に増やす
@extend
class float:
    def __str__(self): return f'{self:.15f}'

#巨大mod時のオーバーフローを回避  pow(base, -1, mod)に対応
def _extended_pow():
    _builtin_pow = pow
    def _codon_pow(base, exp):
        return _builtin_pow(base, exp)
    @overload
    def _codon_pow(base: int, exp: int, mod: int) -> int:
        '''
        codon用に pow(base, exp, mod) を拡張した関数です。
        1. (abs(mod) - 1) ** 2 >= 1 << 63 の場合に発生していたオーバーフローを回避しました。
        2. pow(base: int, exp: 負整数, mod: int) による逆元計算に対応しました。

        返り値の符号は mod の符号に一致します。
        いずれかの引数に INF_MIN := -1 << 63 を渡した場合の動作は未定義です。
        '''
        if mod == 0:
            raise ValueError('pow() 3rd argument cannot be 0')
        if mod == 1 or mod == -1:
            return 0
        if exp < 0:  #拡張ユークリッドの互除法
            a, b, x, y = base, mod, 1, 0
            while b:
                q = a // b
                a, b, x, y = b, a - q * b, y, x - q * y
            if a != 1 and a != -1:
                raise ValueError('base is not invertible for the given modulus')
            b128, m128 = Int[128](x), Int[128](mod)
            if a == -1:
                b128 = - b128
            exp = - exp
        else:
            b128, m128 = Int[128](base), Int[128](mod)
        v128 = Int[128](1)
        while exp:
            if exp & 1 == 1:
                v128 = v128 * b128 % m128
            b128 = b128 * b128 % m128
            exp >>= 1
        v = int(v128)
        return v + mod if v != 0 and (0 < v) != (0 < mod) else v
    return _codon_pow

def isqrt(n: int) -> int:
    if n <= 0: return 0
    x = int(math.sqrt(n))
    while (x+1)*(x+1) <= n: x += 1
    while x*x > n: x -= 1
    return x

pow = _extended_pow()
MOD = 998244353 #10**9+7
def exit(): sys.exit()