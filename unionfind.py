class UnionFind():
    def __init__(self, n):
        """
        Parameters
        ----------
        n:int
            the number of node
        """
        self.par = [-1] * n  # -self.par[i] means the tree size

    def find(self, x):
        """
        Parameters
        ----------
        x:int
            target node

        Return
        ----------
        res:int
            root node
        """
        if self.par[x] < 0:
            return x
        else:
            self.par[x] = self.find(self.par[x])
            return self.par[x]

    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)
        if x != y:
            if self.par[x] > self.par[y]:  # lesser has many nodes
                x, y = y, x
            self.par[x] += self.par[y]
            self.par[y] = x

    def is_same(self, x, y):
        return self.find(x) == self.find(y)

    def size(self, x):
        '''
        Parameters
        ----------
        x:int
            target node

        Return
        ----------
        x:int
            size of  group  to which belongs
        '''
        return - self.par[self.find(x)]


n, m = 5, 3  # map(int, input().split()) n:ノードの数, m:パスの数
uf1 = UnionFind(n)
for i, j in [[1, 2], [5, 4], [4, 1]]:  # range(m):
    a, b = i, j  # map(int, input().split()) #a,b:つながっている辺
    uf1.union(a - 1, b - 1)
for i in range(n):
    uf1.find(i)  # 一周findすることによって接続漏れをなくす。

print(uf1.par)  # [4, 4, -1, 4, -4]
# 正の要素は子。根のindexを示す。
# 負の要素は根。所属する個数*(-1)になっている。
