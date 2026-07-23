from typing import List, Tuple

INF = 10**9

def construir_grafo(mapa: List[str], dims: Tuple[int, int], portais: List[Tuple[int,int]],
                    pos_inicio: Tuple[int,int], pos_fim: Tuple[int,int]):
    linhas, colunas = dims
    V = linhas * colunas

    def id_of(i, j): return i * colunas + j

    adj: List[List[Tuple[int,int]]] = [[] for _ in range(V)]
    matriz: List[List[int]] = [[INF] * V for _ in range(V)]
    for v in range(V):
        matriz[v][v] = 0

    allowed_cost = {'W': 7, 'S': 4, 'G': 1}
    

    t1_pos, t2_pos = portais[0], portais[1]

    for i in range(linhas):
        for j in range(colunas):
            origem_ch = mapa[i][j]
            if origem_ch == '#' or origem_ch == 'T':
                continue
            
            id_origem = id_of(i, j)
            
            for di, dj in ((-1,0), (1,0), (0,-1), (0,1)):
                ni, nj = i + di, j + dj
                if not (0 <= ni < linhas and 0 <= nj < colunas):
                    continue
                
                viz_ch = mapa[ni][nj]
                if viz_ch == '#':
                    continue
                

                if viz_ch == 'T':
                    custo = 0
                    real_ni, real_nj = t2_pos if (ni, nj) == t1_pos else t1_pos
                elif viz_ch in ('I', 'F'):
                    custo = 0
                    real_ni, real_nj = ni, nj
                elif viz_ch in allowed_cost:
                    custo = allowed_cost[viz_ch]
                    real_ni, real_nj = ni, nj
                else:
                    raise ValueError(f"Caractere inválido '{viz_ch}' em ({ni},{nj})")

                id_destino = id_of(real_ni, real_nj)
                
                adj[id_origem].append((id_destino, custo))
                if custo < matriz[id_origem][id_destino]:
                    matriz[id_origem][id_destino] = custo

    id_inicio = id_of(*pos_inicio)
    id_fim = id_of(*pos_fim)
    return adj, matriz, id_inicio, id_fim