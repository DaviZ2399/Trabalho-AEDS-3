#Versão Samuel
def floyd_warshall(V, matriz):
    INF = 10**9
    dist = [[INF] * V for _ in range(V)]
    prev = [[-1] * V for _ in range(V)]

    for i in range(V):
        for j in range(V):
            if i == j:
                dist[i][j] = 0
                prev[i][j] = i
            elif matriz[i][j] != INF:
                dist[i][j] = matriz[i][j]
                prev[i][j] = i
            else:
                dist[i][j] = INF
                prev[i][j] = -1

    for k in range(V):
        for i in range(V):
            for j in range(V):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    prev[i][j] = prev[k][j]

    return dist, prev