import os
import sys
import time
import multiprocessing
from functools import partial

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
LIMITE_TEMPO = 600.0
REPETICOES = 10


def executar_com_timeout(func, *args, timeout=LIMITE_TEMPO):
    with multiprocessing.Manager() as manager:
        result_dict = manager.dict()
        finished = multiprocessing.Event()

        def target():
            try:
                res = func(*args)
                result_dict['resultado'] = res
            except Exception as e:
                result_dict['erro'] = str(e)
            finally:
                finished.set()

        p = multiprocessing.Process(target=target)
        p.start()
        inicio = time.perf_counter()
        finished.wait(timeout)
        fim = time.perf_counter()
        tempo_gasto = fim - inicio

        if not finished.is_set():
            p.terminate()
            p.join()
            return None, tempo_gasto, True
        else:
            p.join()
            if 'erro' in result_dict:
                raise RuntimeError(result_dict['erro'])
            return result_dict.get('resultado'), tempo_gasto, False


def executar_algoritmo_repeticoes(func, *args, repeticoes=REPETICOES):
    tempos = []
    resultado = None
    excedeu = False

    for i in range(repeticoes):
        res, tempo, excedeu_parcial = executar_com_timeout(func, *args)
        if excedeu_parcial:
            return None, LIMITE_TEMPO, True
        tempos.append(tempo)
        resultado = res

    tempo_medio = sum(tempos) / len(tempos)
    return resultado, tempo_medio, False


def nome_saida(arquivo_entrada, sufixo):
    base = os.path.splitext(os.path.basename(arquivo_entrada))[0]
    pasta = "saidas"
    os.makedirs(pasta, exist_ok=True)
    return os.path.join(pasta, f"{base}_{sufixo}.txt")


def imprimir_resultado(nome_algoritmo, custo, tempo_medio, excedeu=False):
    if excedeu:
        print(f"{nome_algoritmo}:")
        print("Custo: N/A")
        print(f"Tempo execução: TEMPO LIMITE (> {LIMITE_TEMPO} s)")
    else:
        print(f"{nome_algoritmo}:")
        print(f"Custo: {custo}")
        print(f"Tempo execução: {tempo_medio:.6f} s")
    print()


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
    V = len(adj)

    print(f"Arquivo: {caminho_arquivo}\n")

    res_dij, tempo_dij, excedeu_dij = executar_algoritmo_repeticoes(
        dijkstra, V, adj, id_inicio
    )
    if excedeu_dij:
        custo_dij = None
        prev_dij = None
    else:
        dist_dij, prev_dij = res_dij
        custo_dij = dist_dij[id_fim]
    imprimir_resultado("Dijkstra", custo_dij, tempo_dij, excedeu_dij)

    res_bf, tempo_bf, excedeu_bf = executar_algoritmo_repeticoes(
        bellman_ford, V, adj, id_inicio
    )
    if excedeu_bf:
        custo_bf = None
        prev_bf = None
    else:
        dist_bf, prev_bf = res_bf
        custo_bf = dist_bf[id_fim]
    imprimir_resultado("Bellman-Ford", custo_bf, tempo_bf, excedeu_bf)

    res_fw, tempo_fw, excedeu_fw = executar_algoritmo_repeticoes(
        floyd_warshall, V, matriz
    )
    if excedeu_fw:
        custo_fw = None
        prev_fw = None
    else:
        dist_fw, prev_fw = res_fw
        custo_fw = dist_fw[id_inicio][id_fim]
    imprimir_resultado("Floyd-Warshall", custo_fw, tempo_fw, excedeu_fw)

    id_portal1 = portais[0][0] * colunas + portais[0][1]
    id_portal2 = portais[1][0] * colunas + portais[1][1]
    ids_especiais = {id_inicio, id_fim, id_portal1, id_portal2}

    if not excedeu_dij and prev_dij is not None:
        caminho_dij = reconstruir_caminho(prev_dij, id_inicio, id_fim)
        if caminho_dij:
            mapa_dij = marcar_caminho(mapa, caminho_dij, colunas, ids_especiais)
            salvar_mapa(mapa_dij, nome_saida(caminho_arquivo, "dijkstra"))

    if not excedeu_bf and prev_bf is not None:
        caminho_bf = reconstruir_caminho(prev_bf, id_inicio, id_fim)
        if caminho_bf:
            mapa_bf = marcar_caminho(mapa, caminho_bf, colunas, ids_especiais)
            salvar_mapa(mapa_bf, nome_saida(caminho_arquivo, "bellman-ford"))

    if not excedeu_fw and prev_fw is not None:
        caminho_fw = reconstruir_caminho(prev_fw, id_inicio, id_fim)
        if caminho_fw:
            mapa_fw = marcar_caminho(mapa, caminho_fw, colunas, ids_especiais)
            salvar_mapa(mapa_fw, nome_saida(caminho_arquivo, "floyd"))

    print("Arquivos de saída gerados em:", os.path.abspath("saidas"))


if __name__ == "__main__":
    main()