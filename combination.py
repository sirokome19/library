'''
参照：https://drken1215.hatenablog.com/entry/2018/06/08/210000

nCk mod pを求める。

nCk= n!/k!(n-k)!を考えるが、単純計算だと途中の桁が膨大になり計算が間に合わない。
そこで計算中にmodをとるが、割り算にmodを適用するためには逆元を求める必要がある。

dpの要領で1<=i<=Nにおけるi!とその逆元をすべて求めていくので、O(N)。
i=Nの逆元を求めるだけならO(logN)でできるので、N>=10**7のときは
個別に逆元を求める必要がある。
'''

from collections import defaultdict, deque
import sys, bisect, math, itertools
from functools import lru_cache
# @lru_cache(maxsize=None)
sys.setrecursionlimit(10**8)
input = sys.stdin.readline
INF = float('inf')
mod = 10**9 + 7
eps = 10**-7


def inp():
    '''
    一つの整数
    '''
    return int(input())


def inpl():
    '''
    一行に複数の整数
    '''
    return list(map(int, input().split()))


class combination():
    def __init__(self, mod):
        '''
        modを指定して初期化
        '''
        self.mod = mod
        self.fac = [1, 1]  # 階乗テーブル
        self.ifac = [1, 1]  # 階乗の逆元テーブル
        self.inv = [0, 1]  # 逆元計算用

    def calc(self, n, k):
        '''
        nCk%modを計算する
        '''
        if k < 0 or n < k:
            return 0
        self._make_tables(n)  # テーブル作成
        k = min(k, n - k)
        return self.fac[n] * (self.ifac[k] * self.ifac[n - k] %
                              self.mod) % self.mod

    def factorial(self, n):
        '''
        n!%modを計算する
        '''
        self._make_tables(n)
        return self.fac[n]

    def _make_tables(self, n):
        '''
        階乗テーブル・階乗の逆元テーブルを作成
        '''
        for i in range(len(self.fac), n + 1):
            self.fac.append((self.fac[-1] * i) % self.mod)
            self.inv.append(
                (-self.inv[self.mod % i] * (self.mod // i)) % self.mod)
            self.ifac.append((self.ifac[-1] * self.inv[-1]) % self.mod)


comb = combination(mod)

x, y = inpl()
if x > y:
    x, y = y, x
dist = x + y
if dist % 3:
    print(0)
    exit()
total = int((x + y) // 3)
n = x - total
if y > 2 * x:
    print(0)
    exit()

print(comb.calc(total, n))
