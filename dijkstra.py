'''
ダイクストラ法。
始点を固定した時にすべての頂点に対する最短経路を計算する。
O(|E|log|V|)でベルマンフォードより速いが、
負の辺が含まれる場合は使えない。

'''

import collections
import heapq


class Dijkstra():
    def __init__(self):
        self.e = collections.defaultdict(list)

    def add(self, u, v, d, directed=False):
        """
        Parameters
        ----------
        u:int
            from node
        v:int
            to node
        d:int
            cost
        directed:bool
            there is direction
        """
        if directed is False:
            self.e[u].append([v, d])
            self.e[v].append([u, d])
        else:
            self.e[u].append([v, d])

    def delete(self, u, v):
        """
        Parameters
        ----------
        u:int
            from node
        v:int
            to node
        """
        self.e[u] = [_ for _ in self.e[u] if _[0] != v]
        self.e[v] = [_ for _ in self.e[v] if _[0] != u]

    def Dijkstra_search(self, s):
        """
        Parameters
        ----------
        s:int
            start node

        Return
        ----------
        d:dict(int:int)
            shortest cost from start node to each node
            {to : cost}

        prev:dict(int:int)
            previous node on the shortest path
            {from : to}
        """
        d = collections.defaultdict(lambda: float('inf'))
        prev = collections.defaultdict(lambda: None)
        d[s] = 0
        q = []
        heapq.heappush(q, (0, s))  # (cost, 探索候補ノード)
        v = collections.defaultdict(bool)  # 確定済かどうか
        while len(q):
            # ノードuにおけるコストはk
            k, u = heapq.heappop(q)
            if v[u]:
                continue
            v[u] = True

            for uv, ud in self.e[u]:  # cost is ud from u to uv
                if v[uv]:
                    continue
                vd = k + ud
                if d[uv] > vd:
                    d[uv] = vd
                    prev[uv] = u
                    heapq.heappush(q, (vd, uv))

        return d, prev

    def getDijkstraShortestPath(self, start, goal):
        """
        Parameters
        ----------
        start:int
            start node
        goal:int
            goal node

        Return
        ----------
        ShortestPath:list(int)
            shortest path
        """
        _, prev = self.Dijkstra_search(start)
        shortestPath = []
        node = goal
        while node is not None:
            shortestPath.append(node)
            node = prev[node]
        return shortestPath[::-1]


'''
ABC051-D
N頂点M辺の重み付き無向連結グラフがあり、
頂点a_iから頂点b_iを重みc_iで結んでいる。
どの最短経路にも含まれない辺の数を求めよ。

term:
2<=N<=100
N-1<=M<=min(N(N-1)/2,1000)
1<=a_i,b_i<=N
1<=c_i<=10**3

input:
3 3
1 2 1
1 3 1
2 3 3

output:
    1
'''

N, M = map(int, input().split())
graph = Dijkstra()
for i in range(M):
    a, b, c = map(int, input().split())
    # 0-indexじゃなくてもいい
    graph.add(a, b, c, directed=False)

usedPaths = collections.defaultdict(set)
for i in range(1, N + 1):  # 0-indexじゃないので1~Nまで回す
    for j in range(i + 1, N + 1):
        path = graph.getDijkstraShortestPath(i, j)
        if len(path) == 2:
            usedPaths[path[0]].add(path[1])
            usedPaths[path[1]].add(path[0])
        else:
            for idx, v in enumerate(path[:-1]):
                usedPaths[v].add(path[idx + 1])
                usedPaths[path[idx + 1]].add(v)

ans = M - sum([len(a) for a in list(usedPaths.values())]) // 2
print(ans)
