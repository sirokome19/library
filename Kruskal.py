'''
クラスカル法
辺をコストの小さい順に見ていき、閉路ができなければ追加する。
追加前にuとvが同じ連結成分に属していなければ、eを追加しても閉路はできない。
したがってuとvが同じ連結成分に属しているか否かを判定するためにUnionFindを利用する。
辺をソートするためO(ElogV)
'''


class Kruskal_UnionFind():
    def __init__(self, N):
        """
        Parameters
        ----------
        n:int
            the number of nodes
        """
        self.edges = []
        self.rank = [0] * N
        self.par = [i for i in range(N)]
        self.counter = [1] * N

    def add(self, u, v, d):
        """
        Parameters
        ----------
        u:int
            from node (0-index)
        v:int
            to node (0-index)
        d:int
            cost
        """
        self.edges.append([u, v, d])

    def _find(self, x):
        if self.par[x] == x:
            return x
        else:
            self.par[x] = self._find(self.par[x])
            return self.par[x]

    def _unite(self, x, y):
        x = self._find(x)
        y = self._find(y)
        if x != y:
            z = self.counter[x] + self.counter[y]
            self.counter[x], self.counter[y] = z, z
        if self.rank[x] < self.rank[y]:
            self.par[x] = y
        else:
            self.par[y] = x
            if self.rank[x] == self.rank[y]:
                self.rank[x] += 1

    def _size(self, x):
        x = self._find(x)
        return self.counter[x]

    def _same(self, x, y):
        return self._find(x) == self._find(y)

    def Kruskal(self):
        """
        Return
        ----------
        res:int
            sum of cost
        """
        edges = sorted(self.edges, key=lambda x: x[2])  # costでself.edgesをソートする
        res = 0
        for e in edges:
            if not self._same(e[0], e[1]):
                self._unite(e[0], e[1])
                res += e[2]
        return res


'''
ABC065-D
平面上にN個の街がある。
i番目の街は座標(x_i,y_i)にあり、重複することもある。
座標(a,b)と座標(c,d)の間に橋をかけるにはmin(|a-c|,|b-d|)円かかる。
任意の2つの街を道を何本か通ることで行き来できるようにするためには、
最低何円必要でしょうか。

term:
2<=N<=10**5
0<=x_i,y_i<=10**9

input:
3
1 5
3 9
7 8

output:
    3
'''

N = int(input())
XY = [[i] + list(map(int, input().split())) for i in range(N)]  # [[idx, x_i, y_i],...]
graph = Kruskal_UnionFind(N)
XY = sorted(XY, key=lambda x: x[1])  # x_iについてsort
X_costs = [[XY[i - 1][0], XY[i][0], abs(XY[i - 1][1] - XY[i][1])] for i in range(1, N)]
# X_costs = [[from_idx, to_idx, x_cost],...] x_costについてsortされている
XY = sorted(XY, key=lambda x: x[2])  # y_iについてsort
Y_costs = [[XY[i - 1][0], XY[i][0], abs(XY[i - 1][2] - XY[i][2])] for i in range(1, N)]
# Y_costs = [[from_idx, to_idx, x_cost],...] y_costについてsortされている

for i in range(N - 1):
    x0, x1, d = X_costs[i]
    graph.add(x0, x1, d)
    y0, y1, d = Y_costs[i]
    graph.add(y0, y1, d)

print(graph.Kruskal())


'''
この問題ではnodeに番号がないため、idxをつけることでnodeに番号を振っている。
また、x,yのうち最小をとるという条件から、二重辺と見てもどうせコストの大きい方は捨てられるので題意に沿う。

今回は頂点のみが与えられており、メッシュ状に張るとそれだけで|E|=V(V-1)になって間に合わない。
そこで、辺のとり方を工夫する必要があるが、コストを最小にするためにはxの距離が最小またはyの距離が最小である必要がある。
したがってxでsortしたときの隣同士とyでsortしたときの隣同士のみをとればよい。

もし与えられている辺があった場合でO(ElogV)に間に合うのであればすべてgraph.addすればいい。
'''
