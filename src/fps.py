# name: FPS
# prefix: fps
# ---
from dataclasses import dataclass, field
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

def convolution(s, t):
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
    iz = pow(z, MOD - 2, MOD)

    return [v * iz % MOD for v in a]

def _mod_sqrt(a: int, mod: int) -> int:
    """Solve x^2 = a (mod mod).

    Returns one square root if it exists.
    Returns None if no square root exists.

    Tonelli-Shanks.
    """
    a %= mod

    if a == 0:
        return 0

    if mod == 2:
        return a

    # Euler's criterion.
    if pow(a, (mod - 1) // 2, mod) != 1:
        return -1

    # mod - 1 = q * 2^s, q is odd.
    q = mod - 1
    s = 0

    while q % 2 == 0:
        q //= 2
        s += 1

    # Find a quadratic non-residue z.
    z = 2

    while pow(z, (mod - 1) // 2, mod) != mod - 1:
        z += 1

    c = pow(z, q, mod)
    x = pow(a, (q + 1) // 2, mod)
    t = pow(a, q, mod)
    m = s

    while t != 1:
        # Find the smallest i such that
        # t^(2^i) = 1.
        i = 1
        t2 = t * t % mod

        while t2 != 1:
            t2 = t2 * t2 % mod
            i += 1

        b = pow(c, 1 << (m - i - 1), mod)

        x = x * b % mod
        c = b * b % mod
        t = t * c % mod
        m = i

    return x

@dataclass(frozen=True)
class FPSContext:
    """A calculation environment for formal power series.

    n means that all FPS are kept modulo x^n.
    """
    n: int
    mod: int = MOD
    inv_int: list[int] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if self.n < 0:
            raise ValueError("n must be non-negative")

        if self.mod != MOD:
            raise NotImplementedError(
                "This first version uses NTT modulo 998244353 only."
            )

                # Largest power of two >= n.
        limit = 1
        while limit < self.n:
            limit <<= 1

        # We need inverse integers up to the largest
        # NTT length and also for ordinary integration.
        inv = [0] * (limit + 1)

        if limit >= 1:
            inv[1] = 1

        for i in range(2, limit + 1):
            inv[i] = (
                self.mod
                - (self.mod // i)
                * inv[self.mod % i]
                % self.mod
            ) % self.mod

        object.__setattr__(self, "inv_int", inv)

    def __call__(self, coeffs) -> "FPS":
        if isinstance(coeffs, int):
            coeffs = [coeffs]
        return FPS(self, list(coeffs))

    def zero(self) -> "FPS":
        return FPS(self, [])

    def one(self) -> "FPS":
        return FPS(self, [1])

    def x(self) -> "FPS":
        if self.n <= 1:
            return self.zero()

        return FPS(self, [], special=("monomial", 1, 1))

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

    Special representations:
        ("monomial", degree, coefficient)
            coefficient * x^degree

        ("one_minus_xk", degree)
            1 - x^degree
    """

    __slots__ = ("ctx", "a", "_special")

    def __init__(
        self,
        ctx: FPSContext,
        coeffs: Iterable[int],
        special = None,
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

        # coefficient * x^degree
        if special is not None and special[0] == "monomial":
            if len(special) != 3:
                raise ValueError(
                    "monomial special must be "
                    "(kind, degree, coefficient)"
                )

            degree = special[1]
            coefficient = special[2] % ctx.mod

            if (
                degree < 0
                or degree >= n
                or coefficient == 0
            ):
                self._special = None
                a = []

        # 1 - x^degree
        elif special is not None and special[0] == "one_minus_xk":
            if len(special) != 2:
                raise ValueError(
                    "one_minus_xk special must be "
                    "(kind, degree)"
                )

            degree = special[1]

            if degree <= 0:
                raise ValueError("degree must be positive")

            if degree >= n:
                # x^degree == 0 modulo x^n
                self._special = None
                a = [1]

        self.a = a

    # ------------------------------------------------------------
    # Basic utilities
    # ------------------------------------------------------------

    def copy(self) -> "FPS":
        return FPS(self.ctx, self.a, self._special)

    def __repr__(self) -> str:
        return (
            f"FPS({self.a!r}, "
            f"n={self.ctx.n}, "
            f"special={self._special})"
        )

    def __len__(self) -> int:
        if self._special is not None:
            degree = self._special_degree()
            return min(self.ctx.n, degree + 1)

        return len(self.a)

    def __iter__(self):
        if self._special is not None:
            return iter(self._materialize().a)

        return iter(self.a)

    def __getitem__(self, key):
        if isinstance(key, slice):
            if self._special is not None:
                return self._materialize()[key]

            return FPS(self.ctx, self.a[key])

        if key < 0:
            key += self.ctx.n

        if key < 0 or key >= self.ctx.n:
            raise IndexError(
                "FPS coefficient index out of range"
            )

        return self._coeff(key)

    def __setitem__(self, i: int, value: int) -> None:
        if i < 0:
            i += self.ctx.n

        if not (0 <= i < self.ctx.n):
            raise IndexError(
                "FPS coefficient index out of range"
            )

        # Special representation cannot be modified directly.
        if self._special is not None:
            normal = self._materialize()
            self.a = normal.a
            self._special = None

        if i >= len(self.a):
            self.a.extend([0] * (i + 1 - len(self.a)))

        self.a[i] = value % self.ctx.mod

        while self.a and self.a[-1] == 0:
            self.a.pop()

    def truncate(self, n: int) -> "FPS":
        n = max(0, min(n, self.ctx.n))

        if self._special is None:
            return FPS(self.ctx, self.a[:n])

        if self._is_monomial():
            degree = self._special_degree()

            if degree >= n:
                return FPS(self.ctx, [])

            return FPS(
                self.ctx,
                [],
                special=self._special,
            )

        if self._is_one_minus_xk():
            degree = self._special_degree()

            if degree >= n:
                # 1 - x^k == 1 mod x^n
                return FPS(self.ctx, [1])

            return FPS(
                self.ctx,
                [],
                special=self._special,
            )

        raise ValueError(
            f"unknown special FPS: {self._special}"
        )

    # ------------------------------------------------------------
    # Special representation helpers
    # ------------------------------------------------------------

    def _is_monomial(self) -> bool:
        return (
            self._special is not None
            and self._special[0] == "monomial"
        )

    def _is_one_minus_xk(self) -> bool:
        return (
            self._special is not None
            and self._special[0] == "one_minus_xk"
        )

    def _special_degree(self) -> int:
        if self._special is None:
            raise ValueError("FPS is not special")

        return self._special[1]

    def _special_coefficient(self) -> int:
        if not self._is_monomial():
            raise ValueError("FPS is not a monomial")

        return self._special[2] % self.ctx.mod

    def _normal(self) -> "FPS":
        """Return an ordinary FPS representation."""
        if self._special is None:
            return self

        return self._materialize()

    def _coeff(self, i: int) -> int:
        if i < 0 or i >= self.ctx.n:
            return 0

        if self._special is None:
            return self.a[i] if i < len(self.a) else 0

        if self._is_monomial():
            return (
                self._special_coefficient()
                if i == self._special_degree()
                else 0
            )

        if self._is_one_minus_xk():
            if i == 0:
                return 1

            if i == self._special_degree():
                return -1 % self.ctx.mod

            return 0

        raise ValueError(
            f"unknown special FPS: {self._special}"
        )

    def _materialize(self) -> "FPS":
        if self._special is None:
            return self

        if self._is_monomial():
            degree = self._special_degree()
            coefficient = self._special_coefficient()

            return FPS(
                self.ctx,
                [0] * degree + [coefficient],
            )

        if self._is_one_minus_xk():
            degree = self._special_degree()

            out = [0] * (degree + 1)
            out[0] = 1
            out[degree] = -1

            return FPS(self.ctx, out)

        raise ValueError(
            f"unknown special FPS: {self._special}"
        )

    def _is_constant_one(self) -> bool:
        return (
            self._special is None
            and len(self.a) == 1
            and self.a[0] == 1
        )

    # ------------------------------------------------------------
    # Addition / subtraction
    # ------------------------------------------------------------

    def __add__(self, other) -> "FPS":
        if isinstance(other, int):
            other = self.ctx(other)

        self._check_ctx(other)

        self = self._normal()
        other = other._normal()

        n = max(len(self), len(other))
        out = [0] * n

        for i in range(n):
            out[i] = (
                (self.a[i] if i < len(self.a) else 0)
                + (other.a[i] if i < len(other.a) else 0)
            ) % self.ctx.mod

        return FPS(self.ctx, out)

    __radd__ = __add__

    def __sub__(self, other) -> "FPS":
        if isinstance(other, int):
            other = self.ctx(other)

        self._check_ctx(other)

        # 1 - x^k
        if (
            self._is_constant_one()
            and other._is_monomial()
            and other._special_coefficient() == 1
        ):
            return FPS(
                self.ctx,
                [],
                special=(
                    "one_minus_xk",
                    other._special_degree(),
                ),
            )

        self = self._normal()
        other = other._normal()

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
        if self._is_monomial():
            return FPS(
                self.ctx,
                [],
                special=(
                    "monomial",
                    self._special_degree(),
                    -self._special_coefficient()
                    % self.ctx.mod,
                ),
            )

        self = self._normal()

        return FPS(
            self.ctx,
            [-x for x in self.a],
        )

    # ------------------------------------------------------------
    # Multiplication / division
    # ------------------------------------------------------------

    def __mul__(self, other) -> "FPS":
        if isinstance(other, int):
            c = other % self.ctx.mod

            if c == 0:
                return self.ctx.zero()

            if self._is_monomial():
                degree = self._special_degree()
                coefficient = self._special_coefficient()

                coefficient = (
                    coefficient * c
                ) % self.ctx.mod

                if coefficient == 0:
                    return self.ctx.zero()

                return FPS(
                    self.ctx,
                    [],
                    special=(
                        "monomial",
                        degree,
                        coefficient,
                    ),
                )

            if self._is_one_minus_xk():
                k = self._special_degree()

                if k >= self.ctx.n:
                    return self.ctx(c)

                a = [0] * (k + 1)
                a[0] = c
                a[k] = -c % self.ctx.mod

                return FPS(self.ctx, a)

            return FPS(
                self.ctx,
                [
                    (x * c) % self.ctx.mod
                    for x in self.a
                ],
            )

        self._check_ctx(other)

        # f * (1 - x^k)
        if other._is_one_minus_xk():
            return self.mul_1_xk(
                other._special_degree()
            )

        # (1 - x^k) * f
        if self._is_one_minus_xk():
            return other.mul_1_xk(
                self._special_degree()
            )

        # monomial * monomial
        if self._is_monomial() and other._is_monomial():
            degree = (
                self._special_degree()
                + other._special_degree()
            )

            if degree >= self.ctx.n:
                return self.ctx.zero()

            coefficient = (
                self._special_coefficient()
                * other._special_coefficient()
                % self.ctx.mod
            )

            if coefficient == 0:
                return self.ctx.zero()

            return FPS(
                self.ctx,
                [],
                special=(
                    "monomial",
                    degree,
                    coefficient,
                ),
            )

        # monomial * ordinary FPS
        if self._is_monomial():
            degree = self._special_degree()
            coefficient = self._special_coefficient()

            if degree >= self.ctx.n:
                return self.ctx.zero()

            other = other._normal()

            out = [0] * min(
                self.ctx.n,
                len(other.a) + degree,
            )

            for i, x in enumerate(other.a):
                j = i + degree

                if j >= self.ctx.n:
                    break

                out[j] = x * coefficient % self.ctx.mod

            return FPS(self.ctx, out)

        # ordinary FPS * monomial
        if other._is_monomial():
            return other * self

        self = self._normal()
        other = other._normal()

        return FPS(
            self.ctx,
            convolution(
                self.a,
                other.a,
            ),
        )

    __rmul__ = __mul__

    def __truediv__(self, other) -> "FPS":
        if isinstance(other, int):
            if other % self.ctx.mod == 0:
                raise ZeroDivisionError

            inv = pow(
                other % self.ctx.mod,
                self.ctx.mod - 2,
                self.ctx.mod,
            )

            return self * inv

        self._check_ctx(other)

        # f / (1 - x^k)
        if other._is_one_minus_xk():
            return self.div_1_xk(
                other._special_degree()
            )

        return self * other.inv()

    def __rtruediv__(self, other) -> "FPS":
        if isinstance(other, int):
            if self._is_one_minus_xk():
                return self.ctx(other).div_1_xk(
                    self._special_degree()
                )

            return self.ctx(other) / self

        return NotImplemented

    # ------------------------------------------------------------
    # Power
    # ------------------------------------------------------------

    def __pow__(self, exponent: int) -> "FPS":
        if exponent < 0:
            if self._is_one_minus_xk():
                return self.ctx.one().div_1_xk(
                    self._special_degree()
                )

            return self.inv() ** (-exponent)

        if exponent == 0:
            return self.ctx.one()

        # (c*x^k)^m
        if self._is_monomial():
            degree = (
                self._special_degree()
                * exponent
            )

            if degree >= self.ctx.n:
                return self.ctx.zero()

            coefficient = pow(
                self._special_coefficient(),
                exponent,
                self.ctx.mod,
            )

            return FPS(
                self.ctx,
                [],
                special=(
                    "monomial",
                    degree,
                    coefficient,
                ),
            )

        # (1-x^k)^m
        if self._is_one_minus_xk():
            return self._pow_one_minus_xk(
                exponent
            )

        if self.ctx.n == 0:
            return self.ctx.zero()

        v = self.valuation()

        if v == self.ctx.n:
            return self.ctx.zero()

        shift = v * exponent

        if shift >= self.ctx.n:
            return self.ctx.zero()

        if v > 0:
            target_n = self.ctx.n - shift

            reduced_ctx = FPSContext(
                target_n,
                self.ctx.mod,
            )

            base = reduced_ctx(self.a[v:])

            result = base._pow_nonnegative(
                exponent
            )

            return FPS(
                self.ctx,
                [0] * shift + result.a,
            )

        return self._pow_nonnegative(exponent)

    def _pow_nonnegative(
        self,
        exponent: int,
    ) -> "FPS":
        if exponent == 0:
            return self.ctx.one()

        if exponent == 1:
            return self.copy()

        if exponent.bit_length() <= 6:
            return self._pow_doubling(exponent)

        return self._pow_log_exp(exponent)

    def _pow_doubling(
        self,
        exponent: int,
    ) -> "FPS":
        result = self.ctx.one()
        base = self

        while exponent:
            if exponent & 1:
                result = result * base

            exponent >>= 1

            if exponent:
                base = base * base

        return result

    def _pow_log_exp(
        self,
        exponent: int,
    ) -> "FPS":
        mod = self.ctx.mod

        # f = c * g
        # g[0] = 1

        c = self.constant()

        if c == 0:
            raise ValueError(
                "_pow_log_exp requires non-zero constant term"
            )

        inv_c = pow(
            c,
            mod - 2,
            mod,
        )

        # g = f / c
        g = self * inv_c

        # g^k = exp(k * log(g))
        h = g.log() * exponent

        result = h.exp()

        # c^k
        coefficient = pow(
            c,
            exponent,
            mod,
        )

        return result * coefficient

    def _pow_one_minus_xk(
        self,
        exponent: int,
    ) -> "FPS":
        if exponent == 0:
            return self.ctx.one()

        k = self._special_degree()
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
                    * pow(
                        j,
                        self.ctx.mod - 2,
                        self.ctx.mod,
                    )
                    % self.ctx.mod
                )

        return FPS(self.ctx, out)

    # ------------------------------------------------------------
    # Shift
    # ------------------------------------------------------------

    def __lshift__(self, k: int) -> "FPS":
        if k < 0:
            return self >> (-k)

        self = self._normal()

        if k >= self.ctx.n or not self.a:
            return self.ctx.zero()

        return FPS(
            self.ctx,
            [0] * k + self.a,
        )

    def __rshift__(self, k: int) -> "FPS":
        if k < 0:
            return self << (-k)

        self = self._normal()

        if k >= len(self.a):
            return self.ctx.zero()

        return FPS(
            self.ctx,
            self.a[k:],
        )

    # ------------------------------------------------------------
    # Valuation / coefficient
    # ------------------------------------------------------------

    def valuation(self) -> int:
        if self._is_monomial():
            return self._special_degree()

        if not self.a:
            return self.ctx.n

        return next(
            (
                i
                for i, x in enumerate(self.a)
                if x
            ),
            self.ctx.n,
        )

    def constant(self) -> int:
        return self._coeff(0)

    # ------------------------------------------------------------
    # Calculus
    # ------------------------------------------------------------

    def derivative(self) -> "FPS":
        if self._special is not None:
            self = self._normal()

        if len(self.a) <= 1:
            return self.ctx.zero()
        
        return FPS(
            self.ctx,
            self._diff_list(self.a)
        )

    def _diff_list(self, a: list[int]) -> list[int]:
        n = len(a)

        if n == 0:
            return []

        out = [0] * n

        for i in range(n - 1):
            out[i] = (
                (i + 1)
                * a[i + 1]
                % self.ctx.mod
            )

        return out

    def integral(self) -> "FPS":
        n = self.ctx.n

        if n <= 1:
            return self.ctx.zero()

        mod = self.ctx.mod
        inv = self.ctx.inv_int

        out = [0] * n

        upper = min(len(self.a), n - 1)

        for i in range(upper):
            out[i + 1] = (
                self.a[i]
                * inv[i + 1]
                % mod
            )

        return FPS(self.ctx, out)

    def _integral_list(self, a: list[int]) -> list[int]:
        n = len(a)
        mod = self.ctx.mod
        inv = self.ctx.inv_int

        out = [0] * (n + 1)

        for i in range(n):
            out[i + 1] = (
                a[i]
                * inv[i + 1]
                % mod
            )

        return out

    # ------------------------------------------------------------
    # Inverse / log / exp
    # ------------------------------------------------------------

    def inv(self) -> "FPS":
        """Return the multiplicative inverse of this FPS.

        Requires self[0] != 0.

        Complexity:
            O(N log N)
        """
        n = self.ctx.n
        mod = self.ctx.mod

        if n == 0:
            return self.ctx.zero()

        if self.constant() == 0:
            raise ZeroDivisionError(
                "FPS with constant term 0 is not invertible"
            )

        g = [0] * n
        g[0] = pow(self.constant(), mod - 2, mod)

        k = 1

        # 1 / 4 modulo MOD
        inv4 = 748683265

        # This is 1 / (4 * k), effectively.
        factor = inv4

        while k < n:
            k2 = k << 1

            # --------------------------------------------------
            # F = self[:k2]
            # G = g[:k]
            # --------------------------------------------------
            F = self.list(0, k2)
            G = g[:k]

            # if len(F) < k2:
                # F.extend([0] * (k2 - len(F)))

            G.extend([0] * (k2 - k))

            butterfly(F)
            butterfly(G)

            # --------------------------------------------------
            # F = F * G
            # --------------------------------------------------
            for i in range(k2):
                F[i] = F[i] * G[i] % mod

            butterfly_inv(F)

            # Only the upper half is the error we need.
            for i in range(k):
                F[i] = 0

            butterfly(F)

            # --------------------------------------------------
            # F = F * G
            # --------------------------------------------------
            for i in range(k2):
                F[i] = F[i] * G[i] % mod

            butterfly_inv(F)

            upper = min(k2, n)

            for i in range(k, upper):
                g[i] = (
                    -F[i]
                    * factor
                    % mod
                )

            k = k2
            factor = factor * inv4 % mod

        return FPS(self.ctx, g)

    def log(self) -> "FPS":
        if self.constant() != 1:
            raise ValueError(
                "log(f) requires f[0] == 1"
            )

        n = self.ctx.n

        if n == 0:
            return self.ctx.zero()

        inverse = self.inv().list(0, n)
        derivative = self._diff_list(
            self.list(0, n)
        )

        product = convolution(
            inverse,
            derivative,
        )

        result = [0] * n
        inv_table = self.ctx.inv_int

        for i, value in enumerate(product):
            if i+1 >= n: break
            result[i + 1] = (
                value * inv_table[i + 1]
                % self.ctx.mod
            )

        return FPS(self.ctx, result)

    def exp(self) -> "FPS":
        """Return exp(self) modulo x^n.

        Requires self[0] == 0.

        This is a relaxed-convolution based fast FPS exponential.
        """
        n = self.ctx.n
        mod = self.ctx.mod

        if self.constant() != 0:
            raise ValueError(
                "exp(f) requires f[0] == 0"
            )

        if n == 0:
            return self.ctx.zero()

        # --------------------------------------------------
        # inverse of NTT lengths
        # --------------------------------------------------
        #
        # The algorithm needs inv[2], inv[4], ...
        # up to the largest NTT size.
        #
        # Prefer using the inverse table prepared in Context.
        #
        def intt(a: list[int]) -> None:
            if len(a) <= 1:
                return

            butterfly_inv(a)

            inv_len = self.ctx.inv_int[len(a)]

            for i in range(len(a)):
                a[i] = (
                    a[i] * inv_len
                ) % mod

        # --------------------------------------------------
        # b = exp(f) being constructed
        #
        # Initially:
        #   b = 1 + f[1] x
        # --------------------------------------------------
        b = [
            1,
            self._coeff(1) if n > 1 else 0,
        ]

        # --------------------------------------------------
        # c, z1, z2
        #
        # These are auxiliary series used to avoid repeatedly
        # computing a full inverse.
        # --------------------------------------------------
        c = [1]

        z2 = [1, 1]

        m = 2

        while m < n:
            double_m = m << 1

            # ==================================================
            # y = NTT(b padded to 2m)
            # ==================================================
            y = b + [0] * m
            butterfly(y)

            # ==================================================
            # Update c.
            #
            # z1 is the previous z2.
            # ==================================================
            z1 = z2

            z = [
                y[i] * z1[i] % mod
                for i in range(len(z1))
            ]

            intt(z)

            # Remove coefficients that are already known.
            half_m = m >> 1

            for i in range(half_m):
                z[i] = 0

            butterfly(z)

            for i in range(len(z1)):
                z[i] = (
                    z[i]
                    * (-z1[i])
                    % mod
                )

            intt(z)

            # c[m/2:] = z[m/2:]
            c[half_m:] = z[half_m:]

            # z2 = NTT(c padded to 2m)
            z2 = c + [0] * m
            butterfly(z2)

            # ==================================================
            # x = f'
            # ==================================================
            tmp = min(n, m)

            x = self.list(0, tmp)

            if len(x) < m:
                x.extend([0] * (m - len(x)))
            else:
                x = x[:m]

            x = self._diff_list(x)

            # --------------------------------------------------
            # Our diff_list keeps length m.
            # This is exactly what the supplied fast version
            # expects.
            # --------------------------------------------------
            butterfly(x)

            for i in range(len(x)):
                x[i] = (
                    y[i]
                    * x[i]
                    % mod
                )

            intt(x)

            # ==================================================
            # x -= b'
            # ==================================================
            for i in range(1, len(b)):
                x[i - 1] -= (
                    b[i] * i % mod
                )

            # ==================================================
            # Shift the upper half.
            #
            # We need:
            #
            #   x <- x shifted by m
            #
            # while keeping the old upper half.
            # ==================================================
            old_x = x[:]

            x += old_x

            x[-1] = 0

            for i in range(m - 1):
                x[i] = 0

            # ==================================================
            # Multiply by z2 in NTT domain.
            # ==================================================
            butterfly(x)

            for i in range(len(z2)):
                x[i] = (
                    x[i]
                    * z2[i]
                    % mod
                )

            intt(x)

            # ==================================================
            # Integral.
            #
            # x[i] <- x[i] / (i+1)
            #
            # x is currently length 2m.
            # ==================================================
            x.pop()

            x = self._integral_list(x)

            # Remove coefficients which have already been fixed.
            for i in range(m):
                x[i] = 0

            # Add the original f.
            upper = min(n, double_m)

            for i in range(m, upper):
                x[i] += self._coeff(i)

            # ==================================================
            # b <- b + correction
            #
            # b_new = b + ...
            # ==================================================
            butterfly(x)

            for i in range(len(y)):
                x[i] = (
                    x[i]
                    * y[i]
                    % mod
                )

            intt(x)

            b[m:] = x[m:]

            m = double_m

        return FPS(
            self.ctx,
            b[:n],
        )

    def sqrt(self) -> Union["FPS", None]:
        """Return a square root of this FPS modulo x^n.

        Returns None if no square root exists.

        Complexity:
            O(N log N)

        This is a specialized Newton iteration that simultaneously
        maintains the square root and its inverse, avoiding repeated
        generic FPS inverse/multiplication calls.
        """
        n = self.ctx.n
        mod = self.ctx.mod

        if n == 0:
            return self.ctx.zero()

        # --------------------------------------------------
        # Find valuation.
        # --------------------------------------------------
        leading = self.valuation()

        # Zero FPS.
        if leading == n:
            return self.ctx.zero()

        # Odd valuation -> no square root.
        if leading & 1:
            return None

        # sqrt(x^(2k) * h) = x^k * sqrt(h)
        shift = leading >> 1
        size = n - shift

        # --------------------------------------------------
        # h = self / x^leading
        #
        # h[0] != 0
        # --------------------------------------------------
        source = self.list(leading, n)
        if len(source) < size:
            source += [0] * (size - len(source))
        else:
            source = source[:size]

        # --------------------------------------------------
        # Square root of the leading coefficient.
        # --------------------------------------------------
        root = _mod_sqrt(source[0], self.ctx.mod)

        if root < 0:
            return None

        # --------------------------------------------------
        # result   = sqrt(h)
        # inverse  = 1 / result
        #
        # Initially:
        #
        # result[0]  = root
        # inverse[0] = 1 / root
        # --------------------------------------------------
        result = [0] * size
        inverse = [0] * size

        result[0] = root
        inverse[0] = pow(root, mod - 2, mod)

        inv2 = (mod + 1) // 2

        length = 1

        # NTT(result[:length])
        transformed_result = [root]

        # 1 / length
        inverse_length = 1

        while length < size:
            double_length = length << 1

            # ==================================================
            # Compute result^2 in NTT domain.
            #
            # transformed_result = NTT(result[:length])
            # ==================================================
            for i in range(length):
                value = transformed_result[i]
                transformed_result[i] = (
                    value * value % mod
                )

            butterfly_inv(transformed_result)

            for i in range(length):
                transformed_result[i] = (
                    transformed_result[i]
                    * inverse_length
                    % mod
                )

            # ==================================================
            # delta =
            #   ((result^2 - source) >> length)
            #
            # Only the newly needed coefficients are constructed.
            # ==================================================
            delta = [0] * double_length

            for i in range(length):
                value = (
                    transformed_result[i]
                    - source[i]
                )

                index = i + length

                if index < size:
                    value -= source[index]

                delta[index] = value

            # ==================================================
            # Convolve delta with inverse.
            #
            # delta <- delta / (result)
            #
            # in NTT.
            # ==================================================
            butterfly(delta)

            transformed_inverse = [0] * double_length
            transformed_inverse[:length] = inverse[:length]

            butterfly(transformed_inverse)

            for i in range(double_length):
                delta[i] = (
                    delta[i]
                    * transformed_inverse[i]
                    % mod
                )

            butterfly_inv(delta)

            inverse_double_length = (
                inverse_length * inv2 % mod
            )

            upper = min(double_length, size)

            # Newton:
            #
            # result_new
            #   = result - (result^2 - source)/(2 result)
            #
            for i in range(length, upper):
                result[i] = (
                    -delta[i]
                    * inverse_double_length
                    % mod
                    * inv2
                    % mod
                )

            # No more coefficients are needed.
            if double_length >= size:
                break

            # ==================================================
            # Extend result^{-1}.
            #
            # We want:
            #
            # inverse * result = 1
            #
            # and update inverse by Newton iteration.
            # ==================================================
            transformed_result = result[:double_length]

            butterfly(transformed_result)

            error = [
                transformed_result[i]
                * transformed_inverse[i]
                % mod
                for i in range(double_length)
            ]

            butterfly_inv(error)

            # Low coefficients already satisfy inverse * result = 1.
            for i in range(length):
                error[i] = 0

            for i in range(length, double_length):
                error[i] = (
                    error[i]
                    * inverse_double_length
                    % mod
                )

            butterfly(error)

            for i in range(double_length):
                error[i] = (
                    error[i]
                    * transformed_inverse[i]
                    % mod
                )

            butterfly_inv(error)

            for i in range(length, double_length):
                inverse[i] = (
                    -error[i]
                    * inverse_double_length
                    % mod
                )

            length = double_length
            inverse_length = inverse_double_length

        # Restore x^(leading / 2).
        return FPS(
            self.ctx,
            [0] * shift + result,
        )

    # ------------------------------------------------------------
    # Multiplication / division by 1-x^k
    # ------------------------------------------------------------

    def mul_1_xk(self, k: int) -> "FPS":
        if k <= 0:
            raise ValueError(
                "k must be positive"
            )

        n = self.ctx.n
        mod = self.ctx.mod

        a = [0] * n

        for i in range(n):
            value = self._coeff(i)

            if i >= k:
                value -= self._coeff(i - k)

            a[i] = value % mod

        return FPS(self.ctx, a)

    def div_1_xk(self, k: int) -> "FPS":
        if k <= 0:
            raise ValueError(
                "k must be positive"
            )

        n = self.ctx.n
        mod = self.ctx.mod

        a = [0] * n

        for i in range(n):
            value = self._coeff(i)

            if i >= k:
                value += a[i - k]

            a[i] = value % mod

        return FPS(self.ctx, a)

    # ------------------------------------------------------------
    # Misc.
    # ------------------------------------------------------------

    def pow_small(self, exponent: int) -> "FPS":
        """Alias for **, kept as a readable name for beginners."""
        return self ** exponent

    def __repr_polynomial__(self) -> str:
        if self._special is not None:
            return self._materialize().__repr_polynomial__()

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

        return (
            " + ".join(terms)
            if terms
            else "0"
        )

    def _check_ctx(self, other: "FPS") -> None:
        if self.ctx != other.ctx:
            raise ValueError(
                "FPS objects must belong to "
                "the same FPSContext"
            )

    def list(
        self,
        l = None,
        r = None,
    ) -> list[int]:
        """Return coefficients as a list.

        list()
            Return self.a directly.

        list(l, r)
            Return coefficients in [l, r).
            Missing coefficients are zero-padded.
        """

        if l is None and r is None:
            return self.a

        if l is None or r is None:
            raise TypeError(
                "list() takes either 0 or 2 arguments"
            )

        if l < 0:
            l += self.ctx.n

        if r < 0:
            r += self.ctx.n

        if not (0 <= l <= r):
            raise IndexError(
                "FPS coefficient slice out of range"
            )

        return [
            self._coeff(i)
            for i in range(l, r)
        ]


# A convenient top-level constructor for contest code.
def fps(coeffs: Iterable[int], n: int = 1_000_000, mod: int = 998244353) -> "FPS":
    return FPSContext(n+1, mod)(coeffs)

def getx(n: int = 1_000_000, mod: int = 998244353) -> "FPS":
    return FPSContext(n+1, mod).x()

def get1(n: int = 1_000_000, mod: int = 998244353) -> "FPS":
    return FPSContext(n+1, mod).one()