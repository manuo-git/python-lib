# name: Bit Set
# prefix: bitset
# ---
MAXBIT = $1
WORD = 60
WORDS = (MAXBIT + WORD-1) // WORD
MASK = (1<<WORD)-1
class bitset:
    data: list[int]

    # --- コンストラクタ ---
    def __init__(self):
        self.data = [0]*WORDS

    def __init__(self, value: int):
        self.data = [0]*WORDS
        if WORDS > 0: self.data[0] = value
        self._trim() # MAXBITを超えるビットをクリア

    def _trim(self):
        extra_bits = MAXBIT % WORD
        if extra_bits != 0 and WORDS > 0:
            mask = (1<<extra_bits)-1
            self.data[WORDS-1] &= mask

    def add(self, idx: int):
        if 0 <= idx < MAXBIT:
            self.data[idx//WORD] |= 1<<(idx%WORD)

    def mask(k: int) -> bitset:
        res = bitset(0)
        if k <= 0: return res
        if k > MAXBIT: k = MAXBIT

        full_words = k // WORD
        rem_bits = k % WORD

        for i in range(full_words):
            if i < WORDS:
                res.data[i] = MASK

        if rem_bits > 0 and full_words < WORDS:
            res.data[full_words] = (1<<rem_bits)-1

        return res

    # --- ビット演算 ---

    def __or__(self, other: bitset) -> bitset:
        res = bitset()
        res.data = [self.data[i] | other.data[i] for i in range(WORDS)]
        return res

    def __and__(self, other: bitset) -> bitset:
        res = bitset()
        res.data = [self.data[i] & other.data[i] for i in range(WORDS)]
        return res

    def __xor__(self, other: bitset) -> bitset:
        res = bitset()
        res.data = [self.data[i] ^ other.data[i] for i in range(WORDS)]
        return res

    def __invert__(self) -> bitset:
        res = bitset()
        res.data = [~self.data[i]&MASK for i in range(WORDS)]
        res._trim()
        return res

    def __lshift__(self, shift: int) -> bitset:
        res = bitset()
        if shift <= 0:
            for i in range(WORDS): res.data[i] = self.data[i]
            return res
        if shift >= MAXBIT: return res

        word_shift = shift // WORD
        bit_shift = shift % WORD
        w_len = WORDS

        for i in range(w_len):
            if i + word_shift < w_len:
                res.data[i + word_shift] |= self.data[i]<<bit_shift&MASK
            if bit_shift > 0 and i + word_shift + 1 < w_len:
                res.data[i + word_shift + 1] |= self.data[i]>>(WORD - bit_shift)
        
        res._trim()
        return res

    def __rshift__(self, shift: int) -> bitset:
        res = bitset()
        if shift <= 0:
            for i in range(WORDS): res.data[i] = self.data[i]
            return res
        if shift >= MAXBIT: return res

        word_shift = shift // WORD
        bit_shift = shift % WORD
        w_len = WORDS

        for i in range(w_len):
            if i - word_shift >= 0:
                res.data[i - word_shift] |= self.data[i]>>bit_shift
            if bit_shift > 0 and i - word_shift - 1 >= 0:
                res.data[i - word_shift - 1] |= self.data[i]<<(WORD-bit_shift)&MASK
        
        return res

    # --- ユーティリティメソッド ---

    def bit_count(self) -> int:
        """ 立っているビット数を数える (Pythonの int.bit_count に相当) """
        total = 0
        for i in range(WORDS):
            total += self.data[i].bit_count()
        return total

    def bit_length(self) -> int:
        """ 最高位のビットが立っている位置を返す """
        for i in reversed(range(WORDS)):
            if self.data[i] != 0:
                return i * WORD + self.data[i].bit_length()
        return 0

    def __str__(self) -> str:
        parts = []
        for i in reversed(range(WORDS)):
            b_str = bin(self.data[i])[2:]
            parts.append(b_str.zfill(WORD))
        full_bin = "".join(parts)[-MAXBIT:]
        return f"bitset[{MAXBIT}](0b{full_bin})"