def ler_mapa(caminho_arquivo):
        with open(caminho_arquivo, 'r', encoding = 'utf-8') as arquivo:
            matriz = [linha.strip() for linha in arquivo if linha.strip()]
        if not matriz:
            return [], (0,0)
        num_linhas = len(matriz)
        num_colunas = len(matriz[0])
        todas_iguais = all(len(linha) == num_colunas for linha in matriz)
        if not todas_iguais:
            raise ValueError("O mapa tem linhas com tamanhos diferentes")
        return matriz, (num_linhas, num_colunas)

def encontrar_posicoes(mapa):
    allowed = {'I', 'F', 'W', 'S', 'G', 'T', '#'}
    I_pos = None
    F_pos = None
    T_positions = []
    for i, linha in enumerate(mapa):
        for j, ch in enumerate(linha):
            if ch not in allowed:
                raise ValueError(f"Caractere inválido '{ch}' em ({i},{j})")
            if ch == 'I':
                if I_pos is not None:
                    raise ValueError("Existe mais de uma posição 'I'")
                I_pos = (i, j)
            elif ch == 'F':
                if F_pos is not None:
                    raise ValueError("Existe mais de uma posição 'F'")
                F_pos = (i, j)
            elif ch == 'T':
                T_positions.append((i, j))
    if I_pos is None or F_pos is None:
        raise ValueError("O mapa deve conter exatamente 1 'I' e 1 'F'")
    if len(T_positions) != 2:
        raise ValueError(f"O mapa deve conter exatamente 2 'T' (achados: {len(T_positions)})")
    return I_pos, F_pos, T_positions

def reconstruir_caminho(prev, origem, destino):
    caminho = []
    # Caso Floyd: prev[origem] é uma linha da matriz (lista)
    if isinstance(prev[origem], list):
        atual = destino
        caminho.append(atual)
        while atual != origem:
            atual = prev[origem][atual]
            if atual == -1:
                return []
            caminho.append(atual)
        caminho.reverse()
        return caminho
    # Caso Dijkstra/Bellman-Ford: prev é um vetor unidimensional
    atual = destino
    caminho.append(atual)
    while atual != origem:
        atual = prev[atual]
        if atual == -1:
            return []
        caminho.append(atual)
    caminho.reverse()
    return caminho

def marcar_caminho(mapa_original, caminho_ids, colunas, ids_especiais):
    mapa = [list(linha) for linha in mapa_original]
    for id_atual in caminho_ids:
        if id_atual in ids_especiais:
            continue
        i = id_atual // colunas
        j = id_atual % colunas
        mapa[i][j] = '*'
    return mapa

def salvar_mapa(mapa_modificado, nome_arquivo_saida):
    with open(nome_arquivo_saida, 'w', encoding='utf-8') as arquivo:
        for linha in mapa_modificado:
            arquivo.write(''.join(linha) + '\n')