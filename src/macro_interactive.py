# name: Interactive Macro
# prefix: macro_interactive
# ---
from collections import deque, defaultdict, Counter
from bisect import bisect_left, bisect_right
from itertools import permutations, combinations, groupby
from functools import cache
from heapq import heappop, heappush
import math, sys
_int = lambda x: int(x)-1
MOD = 998244353 #10**9+7
INF = 1<<60
Yes, No = "Yes", "No"

debug = False # 変更不可

if sys.argv[-1] == "MY_JUDGE":
    debug = True

# テスト環境用の変数宣言。
N = 1729

def input_prod_values():
    # TODO: 本番環境の変数入力を書く。
    global N
    N = int(input())

from random import *
def randomize_test_values():
    # TODO: テスト環境の変数をランダムに決める。
    global N
    N = randint(1, 100)

def print_test_values():
    # TODO: テスト環境の変数出力を書く。
    print(N)

def ask(): # TODO: 引数を任意に決める。
    res = None
    if debug:
        # TODO: テスト環境の変数を元に聞かれている質問に答える処理を書く。
        res = 0
    else:
        # TODO: ジャッジに聞く処理を書く。出力はsend_judgeを使う。
        res = 0
    return res

def solve():
    ans = None
    # TODO: 問題を解く処理を書く。ジャッジに聞くときはask()を使う。
    return ans

def check(ans):
    # TODO: 答えをテスト環境の変数と比べて正誤判定をする。正解ならTrue。
    return True

if debug:
    T = 1000
    for _ in range(T):
        randomize_test_values()
        ans = solve()
        if check(ans): continue
        print_test_values()
        break
    else:
        print("Test passed.")
else:
    input_prod_values()
    ans = solve()
    # TODO: 本番環境の答え出力の処理を書く。