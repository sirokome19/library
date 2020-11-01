'''
区間加算と区間内の最小値取得ができる非再帰版遅延評価セグメント木。
0-indexで書かれているのでdata[-1]は必ずinit_valになり、data[0]がroot。
さらに、入力データはdata[N0-1]からはじまる。
_segfuncを書き換えれば最大値を保持したりいろいろできる。
'''

import sys
readline = sys.stdin.readline
write = sys.stdout.write
INF = 2**31 - 1


class RUQ():
    def __init__(self, N, init_val):
        self.N = N
        self.depth = (self.N - 1).bit_length()
        self.N0 = 2 ** self.depth
        self.init_val = init_val
        self.data = [self.init_val] * (2 * self.N0)
        self.lazy = [None] * (2 * self.N0)

    def _segfunc(self, left, right):
        res = min(left, right)
        return res

    def _generate_index(self, l, r):
        """
        Parameters
        ----------
        l,r: int
            target range [l,r)

        Return
        ----------
        res: iter(int)
            actually update index
        """
        L = l + self.N0
        R = r + self.N0
        lm = (L // (L & -L)) >> 1
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
            if v is None:
                continue
            self.lazy[2 * i - 1] = self.data[2 * i - 1] = self.lazy[2 * i] = self.data[2 * i] = v
            self.lazy[i - 1] = None

    def update(self, l, r, x):
        """update range

        Args:
            l (int): target range [l,r)
            r (int): target range [l,r)
            x (int): update_value
        """
        *ids, = self._generate_index(l, r)
        self._propagates(*ids)

        L = self.N0 + l
        R = self.N0 + r
        while L < R:
            if R & 1:
                R -= 1
                self.lazy[R - 1] = self.data[R - 1] = x
            if L & 1:
                self.lazy[L - 1] = self.data[L - 1] = x
                L += 1
            L >>= 1
            R >>= 1
        for i in ids:
            self.data[i - 1] = self._segfunc(self.data[2 * i - 1], self.data[2 * i])

    def query(self, l, r):
        """get value from range [l,r)

        Args:
            l (int): [l,r)
            r (int): [l,r)

        Returns:
            int: value
        """
        self._propagates(*self._generate_index(l, r))
        L = self.N0 + l
        R = self.N0 + r

        s = self.init_val
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
st = RUQ(N, INF)
ans = []
for q in range(Q):
    print(st.get_list())
    t, *cmd = map(int, readline().split())
    if t:
        s, t = cmd
        ans.append(str(st.query(s, t + 1)))
    else:
        s, t, x = cmd
        st.update(s, t + 1, x)
print(st.get_list())


write("\n".join(ans))
'''
AOJ RMQ and RUQ
数列A=[a_0,a_1,...,a_n-1]に対し、以下のクエリを処理せよ。
なお、a_iはすべて2**31-1で初期化されている。
    type 0: [s,t]にxを代入する。
    type 1: [s,t]の最小値を出力する。

term:
    1<=n<=10**5
    1<=q<=10**5
    -10**3<=x<=10**3

input:
    3 5
    0 0 1 1
    0 1 2 3
    0 2 2 2
    1 0 2
    1 1 2

output:
    1
    2
'''
