'''
区間加算と区間内の最小値取得ができる非再帰版遅延評価セグメント木。
0-indexで書かれているのでdata[-1]は必ずinit_valになり、data[0]がroot。
さらに、入力データはdata[N0-1]からはじまる。
加算時にそれぞれに伝搬せずに、ボトムアップにdataを更新するときだけ考慮する。
_segfuncを書き換えれば最大値を保持したりいろいろできる。
ただ、区間積にするならupdateや_propagates, init_valも書き換える必要がある。
updateのタイミング的にsegfunc(x,y)+z=segfunc(x+z,y+z)のものしか通らないかも
'''

import sys
readline = sys.stdin.readline
write = sys.stdout.write
INF = 2**31 - 1


class RAQ():
    def __init__(self, N, identity):
        """
        Parameters
        ----------
        N: int
            the number of nodes

        identity: int
            queries' identity element
            query = max -> -inf
            query = min -> inf
        """
        self.N = N
        self.depth = (N - 1).bit_length()
        self.N0 = 2 ** self.depth
        self.identity = identity
        self.init_val = 0
        self.data = [self.init_val] * (2 * self.N0)
        self.lazy = [self.init_val] * (2 * self.N0)

    def init_list(self, list):
        """init list directly

        Args:
            list (list(int)): init list
        """
        for i in range(self.N):
            self.update(i, i + 1, list[i])

    def _segfunc(self, left, right):
        res = min(left, right)
        return res

    def _generate_index(self, l, r):
        """
        Parameters
        ----------
        l,r: int
            target range [l,r) (0-index)

        Return
        ----------
        res: iter(int)
            actually update index
        """
        L = l + self.N0
        R = r + self.N0
        lm = (L // (L & -L)) >> 1  # update target
        rm = (R // (R & -R)) >> 1
        while L < R:
            if R <= rm:
                yield R
            if L <= lm:
                yield L
            L >>= 1
            R >>= 1
        while L:
            yield L
            L >>= 1

    def _propagates(self, *ids):
        """
        Parameters
        ----------
        ids: iter(int)
            update target
        """
        for i in reversed(ids):
            v = self.lazy[i - 1]
            if not v:
                continue
            self.lazy[2 * i - 1] += v
            self.lazy[2 * i] += v
            self.data[2 * i - 1] += v
            self.data[2 * i] += v
            self.lazy[i - 1] = self.init_val

    def update(self, l, r, x):
        """
        Parameters
        ----------
        l,r: int
            target range [l,r) (0-index)
        x: int
            add value
        """
        L = self.N0 + l
        R = self.N0 + r
        while L < R:
            if R & 1:
                R -= 1
                self.lazy[R - 1] += x
                self.data[R - 1] += x
            if L & 1:
                self.lazy[L - 1] += x
                self.data[L - 1] += x
                L += 1
            L >>= 1
            R >>= 1
        for i in self._generate_index(l, r):
            self.data[i - 1] = self._segfunc(self.data[2 * i - 1], self.data[2 * i]) + self.lazy[i - 1]

    def query(self, l, r):
        """
        Parameters
        ----------
        l,r: int
            target range [l,r) (0-index)

        Return
        ----------
        res: int
        """
        self._propagates(*self._generate_index(l, r))
        L = self.N0 + l
        R = self.N0 + r

        s = self.identity
        while L < R:
            if R & 1:
                R -= 1
                s = self._segfunc(s, self.data[R - 1])
            if L & 1:
                s = self._segfunc(s, self.data[L - 1])
                L += 1
            L >>= 1
            R >>= 1
        return s

    def get_list(self):
        """get all list

        Returns:
            list(int): origin list
        """
        for i in range(self.N):
            self._propagates(*self._generate_index(i, i + 1))
        return self.data[self.N0 - 1:self.N0 + self.N - 1]


N, Q = map(int, input().split())
ans = []
st = RAQ(N, INF)
for q in range(Q):
    t, *cmd = map(int, readline().split())
    if t:
        s, t = cmd
        ans.append(str(st.query(s, t + 1)))  # queryは[l,r)
    else:
        s, t, x = cmd
        st.update(s, t + 1, x)  # updateは[l,r)

print("\n".join(ans))
# print("\n")

'''
AOJ RMQ and RAQ
数列A=[a_0,a_1,...,a_n-1]に対し、以下のクエリを処理せよ。
なお、a_iはすべて0で初期化されている。
    type 0: [s,t]にxを加算する。
    type 1: [s,t]の最小値を出力する。

term:
    1<=n<=10**5
    1<=q<=10**5
    -10**3<=x<=10**3

input:
    6 7
    0 1 3 1
    0 2 4 -2
    1 0 5
    1 0 1
    0 3 5 3
    1 3 4
    1 0 5

output:
    -2
    0
    1
    -1
'''
