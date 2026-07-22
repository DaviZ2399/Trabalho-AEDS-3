import os
import sys
import time

from utils import (
    ler_mapa,
    encontrar_posicoes,
    reconstruir_caminho,
    marcar_caminho,
    salvar_mapa,
)
from grafo import construir_grafo
from dijkstra import dijkstra
from bellmanford import bellman_ford
from floyd import floyd_warshall

INF = 10**9
LIMITE_TEMPO = 600


def executar_algoritmo_repeticoes(func, *args, repeticoes=10):
    """
    Executa um algoritmo 'repeticoes' vezes e retorna:
    - o resultado da última execução (ou da primeira, tanto faz)
    - o tempo médio
    - um booleano indicando se algum tempo excedeu o limite de 600s
    """
    tempos = []
    resultado = None
    excedeu_limite = False

    for _ in range(repeticoes):
        inicio = time.perf_counter()
        resultado = func(*args)
        fim = time.perf_counter()
        tempo = fim - inicio
        tempos.append(tempo)

        if tempo > LIMITE_TEMPO:
            excedeu_limite = True

    tempo_medio = sum(tempos) / len(tempos)
    return resultado, tempo_medio, excedeu_limite


def nome_saida(arquivo_entrada, sufixo):
    base = os.path.splitext(os.path.basename(arquivo_entrada))[0]
    pasta = "saidas"
    os.makedirs(pasta, exist_ok=True)
    return os.path.join(pasta, f"{base}_{sufixo}.txt")


def imprimir_resultado(nome_algoritmo, custo, tempo_medio, excedeu=False):
    if excedeu:
        print(f"{nome_algoritmo}: custo = {custo}; tempo médio = TEMPO LIMITE (>600s)")
    else:
        print(f"{nome_algoritmo}: custo = {custo}; tempo médio = {tempo_medio:.6f} s")


def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <caminho_do_mapa>")
        return

    caminho_arquivo = sys.argv[1]
    mapa, dims = ler_mapa(caminho_arquivo)
    linhas, colunas = dims
    pos_inicio, pos_fim, portais = encontrar_posicoes(mapa)
    adj, matriz, id_inicio, id_fim = construir_grafo(
        mapa, dims, portais, pos_inicio, pos_fim
    )
    (dist_dij, prev_dij), tempo_dij, excedeu_dij = executar_algoritmo_repeticoes(
        dijkstra, len(adj), adj, id_inicio
    )
    (dist_bf, prev_bf), tempo_bf, excedeu_bf = executar_algoritmo_repeticoes(
        bellman_ford, len(adj), adj, id_inicio
    )
    V = len(adj)
    if V > 500:
        dist_fw = None
        prev_fw = None
        tempo_fw = 0
        excedeu_fw = True
        custo_fw = "N/A"
    else:
        (dist_fw, prev_fw), tempo_fw, excedeu_fw = executar_algoritmo_repeticoes(
            floyd_warshall, V, matriz
        )
        custo_fw = dist_fw[id_inicio][id_fim]
    custo_dij = dist_dij[id_fim]
    custo_bf = dist_bf[id_fim]
    print(f"Arquivo: {caminho_arquivo}")
    imprimir_resultado("Dijkstra", custo_dij, tempo_dij, excedeu_dij)
    imprimir_resultado("Bellman-Ford", custo_bf, tempo_bf, excedeu_bf)

    if V > 500:
        print("Floyd-Warshall: custo = N/A; tempo médio = TEMPO LIMITE (V muito grande)")
    else:
        imprimir_resultado("Floyd-Warshall", custo_fw, tempo_fw, excedeu_fw)
    ids_especiais = {
        id_inicio,
        id_fim,
        portais[0][0] * colunas + portais[0][1],
        portais[1][0] * colunas + portais[1][1],
    }
    if not excedeu_dij and prev_dij is not None:
        caminho_dij = reconstruir_caminho(prev_dij, id_inicio, id_fim)
        if caminho_dij:
            mapa_dij = marcar_caminho(mapa, caminho_dij, linhas, colunas, ids_especiais)
            salvar_mapa(mapa_dij, nome_saida(caminho_arquivo, "dijkstra"))
    if not excedeu_bf and prev_bf is not None:
        caminho_bf = reconstruir_caminho(prev_bf, id_inicio, id_fim)
        if caminho_bf:
            mapa_bf = marcar_caminho(mapa, caminho_bf, linhas, colunas, ids_especiais)
            salvar_mapa(mapa_bf, nome_saida(caminho_arquivo, "bellman-ford"))
    if not excedeu_fw and prev_fw is not None and V <= 500:
        caminho_fw = reconstruir_caminho(prev_fw, id_inicio, id_fim)
        if caminho_fw:
            mapa_fw = marcar_caminho(mapa, caminho_fw, linhas, colunas, ids_especiais)
            salvar_mapa(mapa_fw, nome_saida(caminho_arquivo, "floyd"))

    print("Arquivos de saída gerados em:", os.path.abspath("saidas"))


if __name__ == "__main__":
    main()