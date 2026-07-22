#Versão Samuel
def dijkstra(V, adj, s):
    INF = 10**9
    dist = [INF] * V
    prev = [-1] * V
    dist[s] = 0
    prev[s] = s

    O = set(range(V))
    C = set()

    while C != set(range(V)):
        u = min(O, key=lambda x: dist[x])
        C.add(u)
        O.remove(u)

        for v, peso in adj[u]:
            if v not in C:
                if dist[v] > dist[u] + peso:
                    dist[v] = dist[u] + peso
                    prev[v] = u

    return dist, prev