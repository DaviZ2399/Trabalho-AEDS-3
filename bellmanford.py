#Versão Samuel
def bellman_ford(V, adj, s):
    INF = 10**9
    dist = [INF] * V
    prev = [-1] * V
    dist[s] = 0
    prev[s] = s

    for _ in range(V - 1):
        atualizou = False
        for u in range(V):
            for v, peso in adj[u]:
                if dist[v] > dist[u] + peso:
                    dist[v] = dist[u] + peso
                    prev[v] = u
                    atualizou = True
        if not atualizou:
            break

    return dist, prev