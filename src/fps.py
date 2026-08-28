# name: FPS
# prefix: fps
# ---
from dataclasses import dataclass
from typing import Iterable, Union

# O(NMAX)。MODが素数じゃないときは二次元配列を作ってO(NMAX^2)で求める。
# comb2を参照
NMAX = 1000000
COMB_F = [1]*(NMAX+1)
for i in range(2, NMAX+1):
    COMB_F[i] = COMB_F[i-1]*i%MOD
COMB_RF = [1]*NMAX + [pow(COMB_F[NMAX], -1, MOD)]
for i in reversed(range(2, NMAX+1)):
    COMB_RF[i-1] = COMB_RF[i]*i%MOD
def fac(n): return COMB_F[n]
def invfac(n): return COMB_RF[n]
def comb(n, r):
    if r < 0: return 0
    if n < 0: return comb(r-n-1, r)*(-1 if r&1 else 1)%MOD
    if n < r: return 0
    return COMB_F[n]*COMB_RF[r]*COMB_RF[n-r]%MOD
def homb(n, r): return comb(n+r-1, r) # 重複組み合わせ

Number = int

# https://judge.yosupo.jp/submission/55648
# AtCoder Libary v1.4 を python に移植したもの
# https://github.com/atcoder/ac-library/blob/master/atcoder/convolution.hpp

MOD = 998244353
IMAG = 911660635
IIMAG = 86583718
rate2 = (0, 911660635, 509520358, 369330050, 332049552, 983190778, 123842337, 238493703, 975955924, 603855026, 856644456, 131300601, 842657263, 730768835, 942482514, 806263778, 151565301, 510815449, 503497456, 743006876, 741047443, 56250497, 867605899, 0)
irate2 = (0, 86583718, 372528824, 373294451, 645684063, 112220581, 692852209, 155456985, 797128860, 90816748, 860285882, 927414960, 354738543, 109331171, 293255632, 535113200, 308540755, 121186627, 608385704, 438932459, 359477183, 824071951, 103369235, 0)
rate3 = (0, 372528824, 337190230, 454590761, 816400692, 578227951, 180142363, 83780245, 6597683, 70046822, 623238099, 183021267, 402682409, 631680428, 344509872, 689220186, 365017329, 774342554, 729444058, 102986190, 128751033, 395565204, 0)
irate3 = (0, 509520358, 929031873, 170256584, 839780419, 282974284, 395914482, 444904435, 72135471, 638914820, 66769500, 771127074, 985925487, 262319669, 262341272, 625870173, 768022760, 859816005, 914661783, 430819711, 272774365, 530924681, 0)

def butterfly(a):
    n = len(a)
    h = (n - 1).bit_length()
    le = 0
    while le < h:
        if h - le == 1:
            p = 1 << (h - le - 1)
            rot = 1
            for s in range(1 << le):
                offset = s << (h - le)
                for i in range(p):
                    l = a[i + offset]
                    r = a[i + offset + p] * rot
                    a[i + offset] = (l + r) % MOD
                    a[i + offset + p] = (l - r) % MOD
                rot *= rate2[(~s & -~s).bit_length()]
                rot %= MOD
            le += 1
        else:
            p = 1 << (h - le - 2)
            rot = 1
            for s in range(1 << le):
                rot2 = rot * rot % MOD
                rot3 = rot2 * rot % MOD
                offset = s << (h - le)
                for i in range(p):
                    a0 = a[i + offset]
                    a1 = a[i + offset + p] * rot
                    a2 = a[i + offset + p * 2] * rot2
                    a3 = a[i + offset + p * 3] * rot3
                    a1na3imag = (a1 - a3) % MOD * IMAG
                    a[i + offset] = (a0 + a2 + a1 + a3) % MOD
                    a[i + offset + p] = (a0 + a2 - a1 - a3) % MOD
                    a[i + offset + p * 2] = (a0 - a2 + a1na3imag) % MOD
                    a[i + offset + p * 3] = (a0 - a2 - a1na3imag) % MOD
                rot *= rate3[(~s & -~s).bit_length()]
                rot %= MOD
            le += 2

def butterfly_inv(a):
    n = len(a)
    h = (n - 1).bit_length()
    le = h
    while le:
        if le == 1:
            p = 1 << (h - le)
            irot = 1
            for s in range(1 << (le - 1)):
                offset = s << (h - le + 1)
                for i in range(p):
                    l = a[i + offset]
                    r = a[i + offset + p]
                    a[i + offset] = (l + r) % MOD
                    a[i + offset + p] = (l - r) * irot % MOD
                irot *= irate2[(~s & -~s).bit_length()]
                irot %= MOD
            le -= 1
        else:
            p = 1 << (h - le)
            irot = 1
            for s in range(1 << (le - 2)):
                irot2 = irot * irot % MOD
                irot3 = irot2 * irot % MOD
                offset = s << (h - le + 2)
                for i in range(p):
                    a0 = a[i + offset]
                    a1 = a[i + offset + p]
                    a2 = a[i + offset + p * 2]
                    a3 = a[i + offset + p * 3]
                    a2na3iimag = (a2 - a3) * IIMAG % MOD
                    a[i + offset] = (a0 + a1 + a2 + a3) % MOD
                    a[i + offset + p] = (a0 - a1 + a2na3iimag) * irot % MOD
                    a[i + offset + p * 2] = (a0 + a1 - a2 - a3) * irot2 % MOD
                    a[i + offset + p * 3] = (a0 - a1 - a2na3iimag) * irot3 % MOD
                irot *= irate3[(~s & -~s).bit_length()]
                irot %= MOD
            le -= 2

def convolution(s, t, limit: int | None = None):
    n = len(s)
    m = len(t)
    if min(n, m) <= 60:
        a = [0] * (n + m - 1)
        for i in range(n):
            if i % 8 == 0:        
                for j in range(m):
                    a[i + j] += s[i] * t[j]
                    a[i + j] %= MOD
            else:
                for j in range(m):
                    a[i + j] += s[i] * t[j]
        return [x % MOD for x in a]
    full_len = n + m - 1
    if limit is not None:
        if limit <= 0:
            return []
        target_len = min(full_len, limit)
    else:
        target_len = full_len
    a = s[::]
    b = t[::]
    z = 1 << (n + m - 2).bit_length()
    a += [0] * (z - n)
    b += [0] * (z - m)
    butterfly(a)
    butterfly(b)
    for i in range(z):
        a[i] *= b[i]
        a[i] %= MOD
    butterfly_inv(a)
    a = a[:target_len]
    iz = pow(z, MOD - 2, MOD)

    return [v * iz % MOD for v in a]


@dataclass(frozen=True)
class FPSContext:
    """A calculation environment for formal power series.

    n means that all FPS are kept modulo x^n.
    """
    n: int
    mod: int = MOD

    def __post_init__(self) -> None:
        if self.n < 0:
            raise ValueError("n must be non-negative")
        if self.mod != MOD:
            raise NotImplementedError(
                "This first version uses NTT modulo 998244353 only."
            )

    def __call__(self, coeffs: Iterable[int] | int) -> "FPS":
        if isinstance(coeffs, int):
            coeffs = [coeffs]
        return FPS(self, list(coeffs))

    def zero(self) -> "FPS":
        return FPS(self, [])

    def one(self) -> "FPS":
        return FPS(self, [1])

    def x(self) -> "FPS":
        return FPS(self, [], special=("monomial", 1))

    def monomial(self, degree: int, coefficient: int = 1) -> "FPS":
        if degree < 0:
            raise ValueError("degree must be non-negative")
        coefficient %= self.mod

        if degree >= self.n or coefficient == 0:
            return self.zero()

        if coefficient == 1:
            return FPS(self, [], special=("monomial", degree))

        a = [0] * (degree + 1)
        a[degree] = coefficient
        return FPS(self, a)

    def factorials(self) -> tuple[list[int], list[int]]:
        """Return (fact, ifact), both of length n+1."""
        fact = [1] * (self.n + 1)
        for i in range(1, self.n + 1):
            fact[i] = fact[i - 1] * i % self.mod
        ifact = [1] * (self.n + 1)
        ifact[self.n] = pow(fact[self.n], self.mod - 2, self.mod)
        for i in range(self.n, 0, -1):
            ifact[i - 1] = ifact[i] * i % self.mod
        return fact, ifact


class FPS:
    """Formal power series modulo x^ctx.n over F_998244353.

    The public API intentionally resembles ordinary algebra:
        x = ctx.x()
        f = (1 + x + x**2) ** 10
        g = 1 / (1 - x)
        h = f * g
        ans = h[N]

    Coefficients are stored in ascending order:
        [a0, a1, a2, ...] == a0 + a1*x + a2*x^2 + ...
    """

    __slots__ = ("ctx", "a", "_special")

    def __init__(
        self,
        ctx: FPSContext,
        coeffs: Iterable[int],
        special: tuple[str, int] | None = None,
    ):
        self.ctx = ctx
        self._special = special

        n = ctx.n
        a = [c % ctx.mod for c in coeffs]

        if n == 0:
            a = []

        elif len(a) > n:
            a = a[:n]

        while a and a[-1] == 0:
            a.pop()

        # x^k
        if special is not None and special[0] == "monomial":
            degree = special[1]
            if degree < 0 or degree >= n:
                self._special = None
                a = []
        
        # 1 - x^k
        elif special is not None and special[0] == "one_minus_xk":
            degree = special[1]
            if degree <= 0 or degree >= n:
                # k >= n なら x^k == 0 なので 1-x^k == 1
                if degree >= n:
                    self._special = None
                    a = [1]
                else:
                    raise ValueError("degree must be positive")

        self.a = a

    def copy(self) -> "FPS":
        return FPS(self.ctx, self.a, self._special)

    def __repr__(self) -> str:
        return f"FPS({self.a!r}, n={self.ctx.n}, special={self._special})"

    def __len__(self) -> int:
        return len(self.a)

    def __iter__(self):
        return iter(self.a)

    def __getitem__(self, key):
        if isinstance(key, slice):
            if self._special is not None:
                return self._materialize()[key]
            return FPS(self.ctx, self.a[key])

        if key < 0:
            key += self.ctx.n

        if key < 0 or key >= self.ctx.n:
            raise IndexError("FPS coefficient index out of range")

        return self._coeff(key)

    def __setitem__(self, i: int, value: int) -> None:
        if i < 0:
            i += self.ctx.n
        if not (0 <= i < self.ctx.n):
            raise IndexError("FPS coefficient index out of range")
        if i >= len(self.a):
            self.a.extend([0] * (i + 1 - len(self.a)))
        self.a[i] = value % self.ctx.mod
        while self.a and self.a[-1] == 0:
            self.a.pop()

    def truncate(self, n: int) -> "FPS":
        n = max(0, min(n, self.ctx.n))

        if self._special is not None:
            _, degree = self._special

            if degree >= n: return FPS(self.ctx, [])

            return FPS(self.ctx, [], special=self._special)

        return FPS(self.ctx, self.a[:n])
    
    def __add__(self, other) -> "FPS":
        if isinstance(other, int):
            other = self.ctx(other)
        self._check_ctx(other)
        n = max(len(self), len(other))
        out = [0] * n
        for i in range(n):
            out[i] = ((self.a[i] if i < len(self) else 0)
                      + (other.a[i] if i < len(other) else 0)) % self.ctx.mod
        return FPS(self.ctx, out)

    __radd__ = __add__

    def __sub__(self, other) -> "FPS":
        if isinstance(other, int):
            other = self.ctx(other)

        self._check_ctx(other)

        # 1 - x^k
        if (
            self._is_constant_one()
            and other._special is not None
            and other._special[0] == "monomial"
        ):
            k = other._special[1]
            return FPS(self.ctx, [], special=("one_minus_xk", k))

        n = max(len(self), len(other))
        out = [0] * n

        for i in range(n):
            out[i] = (
                (self.a[i] if i < len(self.a) else 0)
                - (other.a[i] if i < len(other.a) else 0)
            ) % self.ctx.mod

        return FPS(self.ctx, out)

    def __rsub__(self, other) -> "FPS":
        if isinstance(other, int):
            return self.ctx(other) - self
        return NotImplemented

    def __neg__(self) -> "FPS":
        return FPS(self.ctx, [-x for x in self.a])

    def __mul__(self, other) -> "FPS":
        if isinstance(other, int):
            return FPS(self.ctx, [x * other for x in self.a])

        self._check_ctx(other)

        # f * (1 - x^k)
        if (
            other._special is not None
            and other._special[0] == "one_minus_xk"
        ):
            return self.mul_1_xk(other._special[1])

        # (1 - x^k) * f
        if (
            self._special is not None
            and self._special[0] == "one_minus_xk"
        ):
            return other.mul_1_xk(self._special[1])

        return FPS(
            self.ctx,
            convolution(self.a, other.a, self.ctx.n),
        )
    
    __rmul__ = __mul__

    def __truediv__(self, other) -> "FPS":
        if isinstance(other, int):
            if other % self.ctx.mod == 0:
                raise ZeroDivisionError

            inv = pow(other % self.ctx.mod, self.ctx.mod - 2, self.ctx.mod)
            return self * inv

        self._check_ctx(other)

        # f / (1 - x^k)
        if (
            other._special is not None
            and other._special[0] == "one_minus_xk"
        ):
            return self.div_1_xk(other._special[1])

        return self * other.inv()

    def __rtruediv__(self, other) -> "FPS":
        if isinstance(other, int):
            # other / (1 - x^k)
            if (
                self._special is not None
                and self._special[0] == "one_minus_xk"
            ):
                return self.ctx(other).div_1_xk(self._special[1])

            return self.ctx(other) / self

        return NotImplemented

    def __pow__(self, exponent: int) -> "FPS":
        # print("POW", len(self), exponent, self._special)
        if exponent < 0:
            # (1 - x^k)^(-1)
            if (
                self._special is not None
                and self._special[0] == "one_minus_xk"
            ):
                return self.ctx.one().div_1_xk(
                    self._special[1]
                )

            return self.inv() ** (-exponent)

        if exponent == 0:
            return self.ctx.one()

        # x^k
        if (
            self._special is not None
            and self._special[0] == "monomial"
        ):
            k = self._special[1] * exponent

            if k >= self.ctx.n:
                return self.ctx.zero()

            return FPS(
                self.ctx,
                [],
                special=("monomial", k),
            )

        # 1 - x^k
        if (
            self._special is not None
            and self._special[0] == "one_minus_xk"
        ):
            # 現時点では一般のFPSとして計算
            # （必要になればここも二項展開で高速化可能）
            return self._pow_one_minus_xk(exponent)


        if self.ctx.n == 0:
            return self.ctx.zero()

        v = self.valuation()

        if v == self.ctx.n: return self.ctx.zero()

        shift = v * exponent

        if shift >= self.ctx.n: return self.ctx.zero()

        if v > 0:
            target_n = self.ctx.n - shift

            reduced_ctx = FPSContext(target_n, self.ctx.mod)
            base = reduced_ctx(self.a[v:])

            result = base._pow_nonnegative(exponent)

            return FPS(self.ctx, [0] * shift + result.a)

        return self._pow_nonnegative(exponent)


    def _pow_nonnegative(self, exponent: int) -> "FPS":
        if exponent == 0:
            return self.ctx.one()

        if exponent == 1:
            return self.copy()

        result = self.ctx.one()
        base = self

        while exponent:
            if exponent & 1:
                result = result * base

            exponent >>= 1

            if exponent:
                base = base * base

        return result

    def _pow_one_minus_xk(self, exponent: int) -> "FPS":
        if exponent == 0:
            return self.ctx.one()

        k = self._special[1]
        n = self.ctx.n

        if k >= n:
            return self.ctx.one()

        out = [0] * n

        # (1-x^k)^m
        # = sum_j (-1)^j C(m,j) x^(kj)
        comb = 1
        degree = 0

        j = 0
        while degree < n and j <= exponent:
            out[degree] = comb

            j += 1
            degree += k

            if j <= exponent and degree < n:
                comb = (
                    comb
                    * (exponent - j + 1)
                    % self.ctx.mod
                    * pow(j, self.ctx.mod - 2, self.ctx.mod)
                    % self.ctx.mod
                )

        return FPS(self.ctx, out)

    def _materialize(self) -> "FPS":
        if self._special is None:
            return self

        kind, degree = self._special

        if kind == "monomial":
            return FPS(self.ctx, [0] * degree + [1])

        if kind == "one_minus_xk":
            out = [0] * (degree + 1)
            out[0] = 1
            out[degree] = -1
            return FPS(self.ctx, out)

        raise ValueError(f"unknown special FPS: {kind}")

    def __lshift__(self, k: int) -> "FPS":
        if k < 0:
            return self >> (-k)
        if k >= self.ctx.n or not self.a:
            return self.ctx.zero()
        return FPS(self.ctx, [0] * k + self.a)

    def __rshift__(self, k: int) -> "FPS":
        if k < 0:
            return self << (-k)
        if k >= len(self.a):
            return self.ctx.zero()
        return FPS(self.ctx, self.a[k:])

    def valuation(self) -> int:
        if self._special is not None:
            if self._special[0] == "monomial":
                return self._special[1]

        if not self.a:
            return self.ctx.n

        return next(
            (i for i, x in enumerate(self.a) if x),
            self.ctx.n,
        )
    
    def constant(self) -> int:
        return self[0]

    def derivative(self) -> "FPS":
        if len(self.a) <= 1:
            return self.ctx.zero()
        return FPS(self.ctx, [i * self.a[i] for i in range(1, len(self.a))])

    def integral(self) -> "FPS":
        if self.ctx.n <= 1:
            return self.ctx.zero()
        out = [0] * min(self.ctx.n, len(self.a) + 1)
        for i, x in enumerate(self.a):
            if i + 1 >= self.ctx.n:
                break
            out[i + 1] = x * pow(i + 1, self.ctx.mod - 2, self.ctx.mod) % self.ctx.mod
        return FPS(self.ctx, out)

    def inv(self) -> "FPS":
        """Multiplicative inverse, assuming a[0] != 0.

        This first version uses O(n^2) formal division.  It is deliberately
        simple; NTT/Newton acceleration can be added later without changing
        the public API.
        """
        if self.constant() == 0:
            raise ZeroDivisionError("FPS with constant term 0 is not invertible")

        n = self.ctx.n
        out = [0] * n
        out[0] = pow(self.a[0], self.ctx.mod - 2, self.ctx.mod)

        for i in range(1, n):
            s = 0
            upper = min(i, len(self.a) - 1)
            for j in range(1, upper + 1):
                s += self.a[j] * out[i - j]
            out[i] = (-s * out[0]) % self.ctx.mod
        return FPS(self.ctx, out)

    def log(self) -> "FPS":
        if self.constant() != 1:
            raise ValueError("log(f) requires f[0] == 1")
        return (self.derivative() / self).integral()

    def exp(self) -> "FPS":
        if self.constant() != 0:
            raise ValueError("exp(f) requires f[0] == 0")

        # Solve g' = f' g coefficient-by-coefficient.
        n = self.ctx.n
        if n == 0:
            return self.ctx.zero()

        g = [0] * n
        g[0] = 1
        f = self.a

        # For k >= 1:
        # k*g[k] = sum_{i=1..k} i*f[i]*g[k-i]
        for k in range(1, n):
            s = 0
            upper = min(k, len(f) - 1)
            for i in range(1, upper + 1):
                s += i * f[i] * g[k - i]
            g[k] = s * pow(k, self.ctx.mod - 2, self.ctx.mod) % self.ctx.mod
        return FPS(self.ctx, g)

    def pow_small(self, exponent: int) -> "FPS":
        """Alias for **, kept as a readable name for beginners."""
        return self ** exponent

    def mul_1_xk(self, k: int) -> "FPS":
        if k <= 0:
            raise ValueError("k must be positive")

        n = self.ctx.n
        mod = self.ctx.mod

        a = [0] * n

        for i in range(n):
            a[i] = self._coeff(i)

            if i >= k:
                a[i] = (a[i] - self._coeff(i - k)) % mod

        return FPS(self.ctx, a)

    def div_1_xk(self, k: int) -> "FPS":
        if k <= 0:
            raise ValueError("k must be positive")

        n = self.ctx.n
        mod = self.ctx.mod

        a = [0] * n

        for i in range(n):
            a[i] = self._coeff(i)

            if i >= k:
                a[i] = (a[i] + a[i - k]) % mod

        return FPS(self.ctx, a)

    def _coeff(self, i: int) -> int:
        if i < 0 or i >= self.ctx.n:
            return 0

        if self._special is None:
            return self.a[i] if i < len(self.a) else 0

        kind, degree = self._special

        if kind == "monomial":
            return 1 if i == degree else 0

        if kind == "one_minus_xk":
            if i == 0:
                return 1
            if i == degree:
                return -1 % self.ctx.mod
            return 0

        raise ValueError(f"unknown special FPS: {kind}")

    def _is_constant_one(self) -> bool:
        return (
            self._special is None
            and len(self.a) == 1
            and self.a[0] == 1
        )

    def __repr_polynomial__(self) -> str:
        if not self.a:
            return "0"
        terms = []
        for i, c in enumerate(self.a):
            if c == 0:
                continue
            if i == 0:
                terms.append(str(c))
            elif i == 1:
                terms.append(f"{c}*x")
            else:
                terms.append(f"{c}*x^{i}")
        return " + ".join(terms) if terms else "0"

    def _check_ctx(self, other: "FPS") -> None:
        if self.ctx != other.ctx:
            raise ValueError("FPS objects must belong to the same FPSContext")


# A convenient top-level constructor for contest code.
def fps(coeffs: Iterable[int], n: int = 1_000_000, mod: int = 998244353) -> "FPS":
    return FPSContext(n+1, mod)(coeffs)

def getx(n: int = 1_000_000, mod: int = 998244353) -> "FPS":
    return FPSContext(n+1, mod).x()

def get1(n: int = 1_000_000, mod: int = 998244353) -> "FPS":
    return FPSContext(n+1, mod).one()