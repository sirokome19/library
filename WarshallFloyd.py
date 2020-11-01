'''
ワーシャルフロイド法
そんなに使用頻度は高くないが実装コストが低い。
本来は無向グラフを想定するが、有向グラフでも使える。
'''

class WarshallFloyd():
    def __init__(self, N):
        """
        Parameters
        ----------
        N:int
            the number of node
        """
        self.N = N
        self.d = [[float("inf") for i in range(N)]
                  for i in range(N)]  # d[u][v] : 辺uvのコスト(存在しないときはinf)

    def add(self, u, v, c, directed=False):
        """
        Parameters
        ----------
        u:int
            from node (0-index)
        v:int
            to node (0-index)
        d:int
            cost
        directed:bool
            there is direction
        """
        self.directed=directed
        if directed is False:
            self.d[u][v] = c
            self.d[v][u] = c
        else:
            self.d[u][v] = c

    def WarshallFloyd_search(self):
        """
        Return
        ----------
        hasNegativecycle:bool
            whether graph has negative loop
        d:list[u][v]
            the shortest cost from node u to node v
        """
        for k in range(self.N):
            for i in range(self.N):
                for j in range(self.N):
                    self.d[i][j] = min(self.d[i][j], self.d[i][k] + self.d[k][j]) if i!=j else 0

        hasNegativeCycle = False
        if self.directed is False: # non-directional graph
            return hasNegativeCycle, self.d
        
        # for find negative loop
        for i in range(self.N):
            if self.d[i][i] < 0:
                hasNegativeCycle = True
                break
        return hasNegativeCycle, self.d

'''
ABC012-D
N個のバス停とそれらをつなぐM個の経路がある。
バス停a_iからバス停b_iへはt_i分かかる。
あるバス停に住んだ時、最も時間のかかるバス停までは最短で何分かかるか。

term:
2<=N<=300
N-1<=M<=44850
1<=a_i,b_i<=N
1<=t_i<=10**3

input:
3 2
1 2 10
2 3 10

output:
    10
'''

N, M = map(int, input().split())
graph = WarshallFloyd(N)
for _ in range(M):
    a, b, t = map(int,input().split())
    graph.add(a-1,b-1,t)

hasNegativeCycle, d = graph.WarshallFloyd_search()
#max(d[i]):iから最も遠い点のコスト
ans = sorted([[i, max(d[i])] for i in range(N)], key=lambda x: x[1])
print(ans[0][1])
