'''
ベルマンフォード法。
始点を固定した時にすべての頂点に対する最短経路を計算する。
負の辺が使われている場合に使う。
負のループがどこかにあればそれだけで検出する。
listによる実装なので0-indexが使えないが、defaultdictにすればどちらでもよくなる。
実装しろ。

O(|E||V|)
'''


class BellmanFord():
    def __init__(self, N):
        '''
        Parameters
        ----------
        N:int
            the number of nodes
        '''
        self.N = N
        self.edges = []

    def add(self, u, v, d, directed=False):
        '''
        Parameters
        ----------
        u:int
            from node (not 0-index)
        v:int
            to node (not 0-index)
        d:int
            cost
        directed:bool
            there is direction
        '''
        if directed is False:
            self.edges.append([u, v, d])
            self.edges.append([v, u, d])
        else:
            self.edges.append([u, v, d])

    def calc(self, s):
        '''
        Parameters
        ----------
        s:int
            start index (not 0-index)

        Returns
        ----------
        list or bool
            d[i] is shortest distances from node[s] to node[i]
            if there is negative loop, return False
        '''
        dist = [float('inf') for i in range(self.N)]
        dist[s - 1] = 0
        # 辺の緩和
        for i in range(self.N):
            for edge in self.edges:
                frm, to, cost = edge[0] - 1, edge[1] - 1, edge[2]
                # dist[frm]!=inf ->sから到達可能を意味する
                if dist[frm] != float('inf') and dist[to] > dist[frm] + cost:
                    dist[to] = dist[frm] + cost
                    # どこに負のループがあっても検出する
                    # if i == self.N - 1: return False

                    # 頂点1から頂点Nに行く際に負のループがあるときだけ検出する
                    if i == self.N - 1 and to == self.N - 1:
                        return False
        return dist


'''
ABC061-D
N頂点M辺の重み付き有向グラフがあり、
頂点a_iから頂点b_iを重みc_iで結んでいる。
その辺を移動したときスコアc_iが加算される。
頂点1から始まり、頂点Nに駒があるときゲームを終了できる。
頂点1からNまで移動できることは保証されている。
ゲーム終了時のスコアを最大にするような行動をとった時の最大スコアを出力せよ。
スコアが無限に大きくなる場合はinfを出力せよ。

term:
2<=N<=1000
1<=M<=min(N(N-1)/2,2000)
1<=a_i,b_i<=N
-10**9<=c_i<=10**9

input:
    3 3
    1 2 4
    2 3 3
    1 3 5

output:
    7
'''

import sys
sys.setrecursionlimit(10**8)
input = sys.stdin.readline


def inpl():
    '''
    一行に複数の整数
    '''
    return list(map(int, input().split()))


n, m = inpl()
graph = BellmanFord(n)
for _ in range(m):
    a, b, c = inpl()
    graph.add(a, b, -c, directed=True)  # \sum c_iを最大化する
result = graph.calc(1)
if result:
    print(-result[-1])
else:
    print("inf")

'''
負になる閉路に頂点Nが入っていなければその閉路を経由して頂点Nにたどりつけない。
そのためこの問題では頂点Nが入っていない閉路は考慮しなくてよくなる。
'''
