# name: Bit Set
# prefix: bitset
# ---
# https://github.com/manuo-git/python-lib/blob/main/src/bitset.py
MAXBIT = 100_010

_BS_BITS = 63
_BS_MASK = (1 << _BS_BITS) - 1


class bitset:
    _max_bit: int
    _bs_len: int
    a: list[int]

    def __init__(self, value: int = 0, max_bit: int = MAXBIT):
        self._max_bit = max_bit
        self._bs_len = (max_bit + _BS_BITS - 1) // _BS_BITS
        self.a = [0] * self._bs_len

        # int の下位64ビットで初期化
        if self._bs_len:
            self.a[0] = value & _BS_MASK
            if value < 0 and self._bs_len > 1:
                self.a[1] = 1

        self._trim()

    # --------------------------------------------------------
    # 内部処理
    # --------------------------------------------------------

    def _trim(self):
        r = self._max_bit % _BS_BITS
        if r and self._bs_len:
            self.a[-1] &= (1 << r) - 1

    def _check_pos(self, pos: int):
        if pos < 0 or pos >= self._max_bit:
            raise IndexError("bitset index out of range")

    def _test(self, pos: int) -> bool:
        self._check_pos(pos)
        return bool((self.a[pos // _BS_BITS] >> (pos % _BS_BITS)) & 1)

    # --------------------------------------------------------
    # 構築
    # --------------------------------------------------------

    @staticmethod
    def from_string(s: str):
        bs = bitset()

        for c in s:
            if c != "0" and c != "1":
                raise ValueError("invalid bitset string")

        m = min(MAXBIT, len(s))
        for i in range(m):
            if s[len(s) - 1 - i] == "1":
                bs.a[i // _BS_BITS] |= 1 << (i % _BS_BITS)

        return bs

    def copy(self):
        res = bitset()
        for i in range(self._bs_len):
            res.a[i] = self.a[i]
        return res

    # --------------------------------------------------------
    # 要素アクセス
    # --------------------------------------------------------

    def size(self) -> int:
        return self._max_bit

    def __len__(self) -> int:
        return self._max_bit

    def __getitem__(self, pos: int) -> bool:
        return self._test(pos)

    def __setitem__(self, pos: int, val: int):
        self._check_pos(pos)

        i = pos // _BS_BITS
        mask = 1 << (pos % _BS_BITS)

        if val:
            self.a[i] |= mask
        else:
            self.a[i] &= _BS_MASK ^ mask

    # --------------------------------------------------------
    # set / reset / flip
    # --------------------------------------------------------

    def set(self, pos: int = -1, val: bool = True):
        """
        bi |= 1<<pos
        """
        if pos == -1:
            for i in range(self._bs_len):
                self.a[i] = _BS_MASK
            self._trim()
            return self

        self._check_pos(pos)
        i = pos // _BS_BITS
        mask = 1 << (pos % _BS_BITS)

        if val:
            self.a[i] |= mask
        else:
            self.a[i] &= _BS_MASK ^ mask

        return self

    def reset(self, pos: int = -1):
        """
        bi &= MASK&(1<<pos)
        """
        if pos == -1:
            for i in range(self._bs_len):
                self.a[i] = 0
            return self

        self._check_pos(pos)
        i = pos // _BS_BITS
        mask = 1 << (pos % _BS_BITS)

        self.a[i] &= _BS_MASK ^ mask
        return self

    def flip(self, pos: int = -1):
        """
        bi ^= 1<<pos
        """
        if pos == -1:
            for i in range(self._bs_len):
                self.a[i] ^= _BS_MASK
            self._trim()
            return self

        self._check_pos(pos)
        i = pos // _BS_BITS
        self.a[i] ^= 1 << (pos % _BS_BITS)

        return self

    # --------------------------------------------------------
    # 集合の状態
    # --------------------------------------------------------

    def bit_count(self) -> int:
        res = 0
        for x in self.a:
            res += x.bit_count()
        return res

    def bit_length(self) -> int:
        for i in range(self._bs_len - 1, -1, -1):
            x = self.a[i]
            if x:
                return i * _BS_BITS + x.bit_length()
        return 0

    def any(self) -> bool:
        for x in self.a:
            if x:
                return True
        return False

    def none(self) -> bool:
        return not self.any()

    def all(self) -> bool:
        if self._max_bit == 0:
            return True

        last = self._bs_len - 1

        for i in range(last):
            if self.a[i] != _BS_MASK:
                return False

        r = self._max_bit % _BS_BITS
        last_mask = _BS_MASK if r == 0 else (1 << r) - 1

        return self.a[last] == last_mask

    # --------------------------------------------------------
    # ビット演算
    # --------------------------------------------------------

    def __and__(self, other: bitset):
        if self._max_bit != other._max_bit:
            raise ValueError("bitset max_bit mismatch")
        res = bitset()

        for i in range(self._bs_len):
            res.a[i] = self.a[i] & other.a[i]

        return res

    def __or__(self, other: bitset):
        if self._max_bit != other._max_bit:
            raise ValueError("bitset max_bit mismatch")
        res = bitset()

        for i in range(self._bs_len):
            res.a[i] = self.a[i] | other.a[i]

        return res

    def __xor__(self, other: bitset):
        if self._max_bit != other._max_bit:
            raise ValueError("bitset max_bit mismatch")
        res = bitset()

        for i in range(self._bs_len):
            res.a[i] = self.a[i] ^ other.a[i]

        return res

    def __invert__(self):
        res = bitset()

        for i in range(self._bs_len):
            res.a[i] = self.a[i] ^ _BS_MASK

        res._trim()
        return res

    # --------------------------------------------------------
    # 複合代入演算子
    # --------------------------------------------------------

    def __iand__(self, other: bitset):
        if self._max_bit != other._max_bit:
            raise ValueError("bitset max_bit mismatch")
        for i in range(self._bs_len):
            self.a[i] &= other.a[i]
        return self

    def __ior__(self, other: bitset):
        if self._max_bit != other._max_bit:
            raise ValueError("bitset max_bit mismatch")
        for i in range(self._bs_len):
            self.a[i] |= other.a[i]
        return self

    def __ixor__(self, other: bitset):
        if self._max_bit != other._max_bit:
            raise ValueError("bitset max_bit mismatch")
        for i in range(self._bs_len):
            self.a[i] ^= other.a[i]
        return self

    # --------------------------------------------------------
    # 左シフト
    # --------------------------------------------------------

    def __lshift__(self, k: int):
        if k < 0:
            raise ValueError("negative shift count")

        res = bitset()

        if k >= self._max_bit:
            return res

        q = k // _BS_BITS
        r = k % _BS_BITS

        if r == 0:
            for i in range(self._bs_len):
                j = i + q
                if j < self._bs_len:
                    res.a[j] = self.a[i]

        else:
            low_mask = (1 << (_BS_BITS - r)) - 1

            for i in range(self._bs_len):
                j = i + q
                if j >= self._bs_len:
                    continue

                x = self.a[i]

                res.a[j] |= (x & low_mask) << r

                if j + 1 < self._bs_len:
                    res.a[j + 1] |= x >> (_BS_BITS - r)

        res._trim()
        return res

    # --------------------------------------------------------
    # 右シフト
    # --------------------------------------------------------

    def __rshift__(self, k: int):
        if k < 0:
            raise ValueError("negative shift count")

        res = bitset()

        if k >= self._max_bit:
            return res

        q = k // _BS_BITS
        r = k % _BS_BITS

        if r == 0:
            for i in range(self._bs_len):
                src = i + q
                if src < self._bs_len:
                    res.a[i] = self.a[src]

        else:
            low_mask = (1 << r) - 1

            for i in range(self._bs_len):
                src = i + q
                if src >= self._bs_len:
                    continue

                res.a[i] = self.a[src] >> r

                if src + 1 < self._bs_len:
                    res.a[i] |= (
                        (self.a[src + 1] & low_mask)
                        << (_BS_BITS - r)
                    )

        res._trim()
        return res

    # --------------------------------------------------------
    # 複合シフト代入
    # --------------------------------------------------------

    def __ilshift__(self, k: int):
        res = self << k
        self.a = res.a
        return self

    def __irshift__(self, k: int):
        res = self >> k
        self.a = res.a
        return self

    # --------------------------------------------------------
    # 整数変換
    # --------------------------------------------------------

    def to_int(self) -> int:
        for i in range(1, self._bs_len):
            if self.a[i]:
                raise OverflowError("bitset does not fit in int")

        return self.a[0] if self._bs_len else 0

    # --------------------------------------------------------
    # 文字列変換
    # --------------------------------------------------------

    def to_string(self) -> str:
        chars = ["0"] * self._max_bit

        for i in range(self._max_bit):
            if (self.a[i // _BS_BITS] >> (i % _BS_BITS)) & 1:
                chars[self._max_bit - 1 - i] = "1"

        return "".join(chars)

    def __str__(self) -> str:
        return self.to_string()

    def __repr__(self) -> str:
        return f"bitset('{self.to_string()}')"

    # --------------------------------------------------------
    # 比較
    # --------------------------------------------------------

    def __eq__(self, other: bitset) -> bool:
        for i in range(self._bs_len):
            if self.a[i] != other.a[i]:
                return False
        return True

    def __ne__(self, other: bitset) -> bool:
        return not self == other
    
    # --------------------------------------------------------
    # OR + 左右シフト（in-place）
    # --------------------------------------------------------

    def or_lshift(self, k: int):
        """
        self |= self << k
        """
        if k < 0:
            raise ValueError("negative shift count")
        if k == 0 or k >= self._max_bit:
            return self

        q = k // _BS_BITS
        r = k % _BS_BITS

        if r == 0:
            j = self._bs_len - 1
            while j >= q:
                self.a[j] |= self.a[j - q]
                j -= 1
        else:
            shift = _BS_BITS - r
            low_mask = (1 << shift) - 1

            j = self._bs_len - 1
            while j >= q:
                src = j - q
                x = self.a[src]

                v = (x & low_mask) << r
                if src > 0:
                    v |= self.a[src - 1] >> shift

                self.a[j] |= v
                j -= 1

        self._trim()
        return self

    def or_rshift(self, k: int):
        """
        self |= self >> k
        """
        if k < 0:
            raise ValueError("negative shift count")
        if k == 0 or k >= self._max_bit:
            return self

        q = k // _BS_BITS
        r = k % _BS_BITS

        if r == 0:
            i = 0
            while i + q < self._bs_len:
                self.a[i] |= self.a[i + q]
                i += 1
        else:
            shift = _BS_BITS - r
            low_mask = (1 << r) - 1

            i = 0
            while i + q < self._bs_len:
                src = i + q
                x = self.a[src]

                v = x >> r
                if src + 1 < self._bs_len:
                    v |= (self.a[src + 1] & low_mask) << shift

                self.a[i] |= v
                i += 1

        self._trim()
        return self

    def or_shift(self, k: int):
        if k >= 0:
            self.or_lshift(k)
        else:
            self.or_rshift(-k)
    
    # --------------------------------------------------------
    # dp用
    # --------------------------------------------------------
    """
    dp = bitset()
    dp.set(0) # setするbitを指定。この場合int(1)

    dp = bitset(1) # 初期値を設定。これでも良い

    dp = bitset(1, MAXBIT) # max_bitを設定することもできる

    dp.or_rshift(k) # dp |= dp >> k
    dp.or_lshift(k) # dp |= dp << k

    dp.or_shift(k) # kが負の時にも対応したor_lshift()
    """