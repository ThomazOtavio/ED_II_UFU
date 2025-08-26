import random
import time
import os
import heapq
import string
from collections import Counter
from collections import deque

DIRETORIO_DADOS = "./dados/"
DIRETORIO_CONTOS = "./contos/"
DIRETORIO_COMP = "./arq_comprimidos/"

def ler_lista_txt(nome_arquivo):
    caminho = os.path.join(DIRETORIO_DADOS, nome_arquivo)
    with open(caminho, 'r', encoding='utf-8') as arquivo:
        return [linha.strip() for linha in arquivo.readlines() if linha.strip()]

def ler_texto_txt(nome_arquivo):
    caminho = os.path.join(DIRETORIO_DADOS, nome_arquivo)
    with open(caminho, 'r', encoding='utf-8') as arquivo:
        return arquivo.read()

# --------------------- BUSCA SEQUENCIAL ------------------------

def busca_sequencial(fragmentos, alvo):
    comparacoes = 0
    for i, item in enumerate(fragmentos):
        comparacoes += 1
        if item == alvo:
            return i, comparacoes
    return -1, comparacoes

# --------------------- BUSCA BINARIA ------------------------

def busca_binaria(fragmentos_ordenados, alvo):
    inicio = 0
    fim = len(fragmentos_ordenados) - 1
    comparacoes = 0

    while inicio <= fim:
        meio = (inicio + fim) // 2
        comparacoes += 1
    
        if fragmentos_ordenados[meio] == alvo:
            return meio, comparacoes
        elif fragmentos_ordenados[meio] < alvo:
            inicio = meio + 1
        else:
            fim = meio - 1

    return -1, comparacoes

# --------------------- RABIN-KARP ------------------------

def rabin_karp(texto, padrao):
    d = 256
    q = 101
    n = len(texto)
    m = len(padrao)
    h = pow(d, m-1) % q
    p = 0
    t = 0
    posicoes = []

    for i in range(m):
        p = (d * p + ord(padrao[i])) % q
        t = (d * t + ord(texto[i])) % q

    for s in range(n - m + 1):
        if p == t:
            if texto[s:s+m] == padrao:
                posicoes.append(s)
        if s < n - m:
            t = (t - h * ord(texto[s])) % q
            t = (t * d + ord(texto[s + m])) % q
            t = (t + q) % q

    return posicoes

def menu_rabin_karp():
    arquivos_contos = [arq for arq in os.listdir(DIRETORIO_CONTOS) if arq.endswith('.txt')]

    if not arquivos_contos:
        print("\nNenhum conto disponível.")
        return

    print("\n=== LISTA DE CONTOS DISPONÍVEIS ===")
    for idx, nome_arquivo in enumerate(arquivos_contos, 1):
        print(f"{idx}. {nome_arquivo.replace('.txt', '')}")

    try:
        escolha = int(input("Escolha o número do conto: "))
        if 1 <= escolha <= len(arquivos_contos):
            nome_arquivo = arquivos_contos[escolha - 1]
        else:
            print("Escolha inválida.")
            return
    except ValueError:
        print("Entrada inválida.")
        return

    termo_busca = input("Digite a palavra ou expressão que deseja buscar: ")

    caminho_arquivo = os.path.join(DIRETORIO_CONTOS, nome_arquivo)
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        texto = arquivo.read()

    posicoes = rabin_karp(texto, termo_busca)

    print(f"\n'{termo_busca}' encontrado {len(posicoes)} vez(es) no conto '{nome_arquivo.replace('.txt', '')}'.")
    if posicoes:
        print(f"Posições aproximadas no texto: {posicoes[:10]}{'...' if len(posicoes) > 10 else ''}")

    print("\nBusca concluída.")

    # --------------------- COMPRESSÃO HUFFMAN ------------------------

class Huffman:
    def __init__(self, caractere, frequencia):
        self.caractere = caractere
        self.frequencia = frequencia
        self.esquerda = None
        self.direita = None

    def __lt__(self, outro):
        return self.frequencia < outro.frequencia

# --------------------- HUFFMAN ------------------------

def arvore_huffman(texto):
    frequencias = Counter(texto)
    fila = [Huffman(char, freq) for char, freq in frequencias.items()]
    heapq.heapify(fila)

    while len(fila) > 1:
        no1 = heapq.heappop(fila)
        no2 = heapq.heappop(fila)
        novo_no = Huffman(None, no1.frequencia + no2.frequencia)
        novo_no.esquerda = no1
        novo_no.direita = no2
        heapq.heappush(fila, novo_no)

    return fila[0]

def gerador_codigos(no, codigo_atual="", tabela=None):
    if tabela is None:
        tabela = {}
    if no is not None:
        if no.caractere is not None:
            tabela[no.caractere] = codigo_atual
        gerador_codigos(no.esquerda, codigo_atual + "0", tabela)
        gerador_codigos(no.direita, codigo_atual + "1", tabela)
    return tabela

def comprimir_conto(nome_arquivo):
    caminho_entrada = os.path.join(DIRETORIO_CONTOS, nome_arquivo)
    with open(caminho_entrada, 'r', encoding='utf-8') as arquivo:
        texto_original = arquivo.read()

    raiz = arvore_huffman(texto_original)
    tabela_codigos = gerador_codigos(raiz)
    texto_codificado = ''.join(tabela_codigos[char] for char in texto_original)

    nome_saida = nome_arquivo.replace('.txt', '_comprimido.txt')
    caminho_saida = os.path.join(DIRETORIO_COMP, nome_saida)
    with open(caminho_saida, 'w', encoding='utf-8') as arquivo_saida:
        arquivo_saida.write(texto_codificado)

    print(f"\nArquivo comprimido salvo em: {caminho_saida}")
    print(f"Tamanho original: {len(texto_original) * 8} bits")
    print(f"Tamanho comprimido: {len(texto_codificado)} bits")
    print(f"Taxa de compressão: {100 - (len(texto_codificado) / (len(texto_original) * 8)) * 100:.2f}%")

    print("\n--- FRAGMENTO DO ARQUIVO COMPRIMIDO ---")
    print(texto_codificado[:100] + ('...' if len(texto_codificado) > 100 else ''))
    print("----------------------------------------")

    return raiz, texto_codificado, caminho_saida

def descomprimir_conto(raiz, texto_codificado, caminho_arquivo_comprimido):
    resultado = []
    no = raiz
    for bit in texto_codificado:
        no = no.esquerda if bit == "0" else no.direita
        if no.caractere is not None:
            resultado.append(no.caractere)
            no = raiz

    texto_descomprimido = ''.join(resultado)

    print("\n--- TEXTO DESCOMPRIMIDO (INÍCIO) ---")
    print(texto_descomprimido[:500])
    print("\n--- FIM DO TRECHO ---")

    if os.path.exists(caminho_arquivo_comprimido):
        os.remove(caminho_arquivo_comprimido)
        print(f"\nArquivo comprimido '{caminho_arquivo_comprimido}' deletado após descompressão.")

def menu_huffman():
    arquivos_contos = [arq for arq in os.listdir(DIRETORIO_CONTOS) if arq.endswith('.txt')]

    if not arquivos_contos:
        print("\nNenhum conto disponível.")
        return

    print("\n=== LISTA DE CONTOS DISPONÍVEIS ===")
    for idx, nome_arquivo in enumerate(arquivos_contos, 1):
        print(f"{idx}. {nome_arquivo}")

    try:
        escolha = int(input("Escolha o número do conto para compressão: "))
        if 1 <= escolha <= len(arquivos_contos):
            nome_arquivo = arquivos_contos[escolha - 1]
        else:
            print("Escolha inválida.")
            return
    except ValueError:
        print("Entrada inválida.")
        return

    raiz, texto_codificado, caminho_arquivo_comprimido = comprimir_conto(nome_arquivo)

    opcao = input("\nDeseja descomprimir e visualizar o texto? (s/n): ").strip().lower()
    if opcao == 's':
        descomprimir_conto(raiz, texto_codificado, caminho_arquivo_comprimido)

# --------------------- TABELA HASH ------------------------

class TabelaHash:
    def __init__(self, tamanho=20):
        self.tamanho = tamanho
        self.tabela = [[] for _ in range(tamanho)]
        self.colisoes = 0

    def hash_extração(self, chave):
        chave_str = str(chave)
        digitos = ''.join([c for c in chave_str if c.isdigit()])
        if digitos:
            return int(digitos) % self.tamanho
        else:
            return sum(ord(c) for c in chave_str) % self.tamanho

    def hash_enlacamento_deslocado(self, chave):
        chave_str = str(chave)
        soma = sum(ord(c) for c in chave_str)
        deslocado = (soma * 3) % 47
        return deslocado % self.tamanho

    def inserir_fragmento(self, chave, valor, modo="extração"):
        if modo == "extração":
            indice = self.hash_extração(chave)
        else:
            indice = self.hash_enlacamento_deslocado(chave)

        if self.tabela[indice]:
            self.colisoes += 1

        self.tabela[indice].append((chave, valor))
        print(f"'{chave}' inserido na posição {indice}.")

    def buscar_fragmento(self, chave, modo="extração"):
        if modo == "extração":
            indice = self.hash_extração(chave)
        else:
            indice = self.hash_enlacamento_deslocado(chave)

        for k, v in self.tabela[indice]:
            if k == chave:
                return v

        return None

    def exibir_tabela(self):
        print("\n--- TABELA HASH ---")
        for i, lista in enumerate(self.tabela):
            print(f"[{i}]: {lista}")
        print(f"Colisões registradas: {self.colisoes}")

def menu_tabela_hash():
    tabela = TabelaHash(tamanho=50)

    while True:
        print("\n--- Cofre de Fragmentos (Hash) ---")
        print("1. Inserir Fragmento")
        print("2. Buscar Fragmento")
        print("3. Exibir Tabela")
        print("4. Teste Automático")
        print("5. Voltar ao menu principal")
        sub_opcao = input("Escolha uma opção: ")

        if sub_opcao == '1':
            chave = input("Digite a chave do fragmento: ")
            valor = input("Digite o valor do fragmento: ")
            tabela.inserir_fragmento(chave, valor)
            print("Fragmento armazenado com sucesso.")

        elif sub_opcao == '2':
            chave = input("Digite a chave do fragmento a buscar: ")
            resultado = tabela.buscar_fragmento(chave)
            if resultado is not None:
                print(f"Fragmento encontrado: {resultado}")
            else:
                print("Fragmento não encontrado.")

        elif sub_opcao == '3':
            tabela.exibir_tabela()

        elif sub_opcao == '4':
            print("\nEscolha a quantidade de entradas para o teste:")
            print("1. 25 entradas")
            print("2. 50 entradas")
            print("3. 75 entradas")
            print("4. 100 entradas")
            opcao_teste = input("Escolha uma opção: ")

            if opcao_teste == '1':
                qtd = 25
            elif opcao_teste == '2':
                qtd = 50
            elif opcao_teste == '3':
                qtd = 75
            elif opcao_teste == '4':
                qtd = 100
            else:
                print("Opção inválida.")
                continue

            print(f"\nInserindo {qtd} entradas aleatórias na Tabela Hash...")

            for _ in range(qtd):
                chave = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                valor = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
                tabela.inserir_fragmento(chave, valor)

            tabela.exibir_tabela()

        elif sub_opcao == '5':
            break

        else:
            print("Opção inválida. Tente novamente.")

# --------------------- GRAFOS ------------------------

class UnionFind:
    def __init__(self, n):
        self.pai = list(range(n)) 
        self.rank = [0] * n 

    def encontrar(self, u):
        if self.pai[u] != u:
            self.pai[u] = self.encontrar(self.pai[u]) 
        return self.pai[u]

    def unir(self, u, v):
        raiz_u = self.encontrar(u)
        raiz_v = self.encontrar(v)

        if raiz_u != raiz_v:
            if self.rank[raiz_u] > self.rank[raiz_v]:
                self.pai[raiz_v] = raiz_u
            elif self.rank[raiz_u] < self.rank[raiz_v]:
                self.pai[raiz_u] = raiz_v
            else:
                self.pai[raiz_v] = raiz_u
                self.rank[raiz_u] += 1

def kruskal(grafo):
    arestas = []
    for cidade1, adjacentes in grafo.lista_adj.items():
        for cidade2, peso in adjacentes:
            arestas.append((peso, cidade1, cidade2))

    arestas.sort()

    uf = UnionFind(len(grafo.cidades))
    
    arvore_geradora = []
    
    for peso, cidade1, cidade2 in arestas:
        u = grafo.cidades.index(cidade1)
        v = grafo.cidades.index(cidade2)

        if uf.encontrar(u) != uf.encontrar(v):
            arvore_geradora.append((cidade1, cidade2, peso))
            uf.unir(u, v)

    return arvore_geradora

def prim(grafo, cidade_inicial):
    visitado = {cidade: False for cidade in grafo.cidades}
    cidade_inicial_idx = grafo.cidades.index(cidade_inicial)
    min_heap = [(0, cidade_inicial)]
    arvore_geradora = []

    while min_heap:
        peso, cidade_atual = heapq.heappop(min_heap)
        if visitado[cidade_atual]:
            continue

        visitado[cidade_atual] = True

        for vizinho, peso in grafo.lista_adj[cidade_atual]:
            if not visitado[vizinho]:
                heapq.heappush(min_heap, (peso, vizinho))
                arvore_geradora.append((cidade_atual, vizinho, peso))

    return arvore_geradora

class Grafo:
    def __init__(self, cidades):
        self.cidades = cidades
        self.num_cidades = len(cidades)
        
        self.matriz_adj = [[0 for _ in range(self.num_cidades)] for _ in range(self.num_cidades)]
        
        self.lista_adj = {cidade: [] for cidade in cidades}
        self.grau_entrada = {cidade: 0 for cidade in cidades} 

    def adicionar_aresta(self, cidade1, cidade2, peso):
        i = self.cidades.index(cidade1)
        j = self.cidades.index(cidade2)
        
        self.matriz_adj[i][j] = peso
        self.matriz_adj[j][i] = peso  

        self.lista_adj[cidade1].append((cidade2, peso))
        self.lista_adj[cidade2].append((cidade1, peso))  
        
        self.grau_entrada[cidade2] += 1

    def remover_aresta(self, cidade1, cidade2):
        i = self.cidades.index(cidade1)
        j = self.cidades.index(cidade2)

        self.matriz_adj[i][j] = 0
        self.matriz_adj[j][i] = 0

        self.lista_adj[cidade1] = [cidade for cidade, _ in self.lista_adj[cidade1] if cidade != cidade2]
        self.lista_adj[cidade2] = [cidade for cidade, _ in self.lista_adj[cidade2] if cidade != cidade1]
        
        self.grau_entrada[cidade2] -= 1

    def exibir_matriz(self):
        print("Matriz de Adjacência:")
        for linha in self.matriz_adj:
            print(linha)

    def exibir_lista(self):
        print("Lista de Adjacência:")
        for cidade, adjacentes in self.lista_adj.items():
            print(f"{cidade}: {adjacentes}")

    def ordenacao_topologica(self):
        fila = deque([cidade for cidade in self.cidades if self.grau_entrada[cidade] == 0])
        ordenacao = []
        
        while fila:
            cidade_atual = fila.popleft()
            ordenacao.append(cidade_atual)
            
            for vizinho, _ in self.lista_adj[cidade_atual]:
                self.grau_entrada[vizinho] -= 1
                if self.grau_entrada[vizinho] == 0:
                    fila.append(vizinho)
        
        if len(ordenacao) == self.num_cidades:
            print("\nOrdenação Topológica:")
            print(" -> ".join(ordenacao))
        else:
            print("\nO grafo contém ciclos, logo não pode ser ordenado topologicamente.")

    def colorir_grafo(self):
        nomes_cores = ["Amarelo", "Vermelho", "Azul", "Verde", "Roxo", "Laranja", "Cinza", "Preto"]
    
        cidades_ordenadas = sorted(self.cidades, key=lambda cidade: len(self.lista_adj[cidade]), reverse=True)
    
        cores = {cidade: None for cidade in self.cidades}

        for cidade in cidades_ordenadas:
            vizinhos = [vizinhos for vizinhos, _ in self.lista_adj[cidade]]
            cores_usadas = {cores[vizinhos] for vizinhos in vizinhos if cores[vizinhos] is not None}
        
            cor = 0
            while cor < len(nomes_cores) and nomes_cores[cor] in cores_usadas:
                cor += 1
        
            if cor >= len(nomes_cores):
                print("Aviso: Número insuficiente de cores disponíveis para colorir o grafo.")
            
            cores[cidade] = nomes_cores[cor]
    
        print("\nColoração do grafo (Cidades e suas cores):")
        for cidade, cor in cores.items():
            print(f"{cidade}: {cor}")

    def dfs(self, cidade_inicial, visitado=None):
        if visitado is None:
            visitado = set()
        visitado.add(cidade_inicial)
        for vizinho, _ in self.lista_adj[cidade_inicial]:
            if vizinho not in visitado:
                self.dfs(vizinho, visitado)
        return visitado

    def bfs(self, cidade_inicial):
        visitado = set()
        fila = deque([cidade_inicial])
        distancias = {cidade_inicial: 0}
        while fila:
            cidade_atual = fila.popleft()
            for vizinho, _ in self.lista_adj[cidade_atual]:
                if vizinho not in visitado:
                    visitado.add(vizinho)
                    distancias[vizinho] = distancias[cidade_atual] + 1
                    fila.append(vizinho)
        return distancias

    def dijkstra(self, cidade_inicial):
        distancias = {cidade: float('inf') for cidade in self.cidades}
        distancias[cidade_inicial] = 0
        caminho = {cidade: None for cidade in self.cidades}
        pq = [(0, cidade_inicial)]

        while pq:
            (dist, cidade_atual) = heapq.heappop(pq)
            
            for vizinho, peso in self.lista_adj[cidade_atual]:
                distancia = dist + peso
                if distancia < distancias[vizinho]:
                    distancias[vizinho] = distancia
                    caminho[vizinho] = cidade_atual
                    heapq.heappush(pq, (distancia, vizinho))
        return distancias, caminho

def menu_mapas():
    print("\n=== MENU DE MANIPULAÇÃO DE MAPA ===")
    
    cidades = [
        "Amon Hen", "Anduin", "Angband", "Annuminas", "Barad-dûr", 
        "Bree", "Caras Galadhon", "Gondolin", "Edoras", "Rivendell"
    ]
    
    mapa = Grafo(cidades)

    mapa.adicionar_aresta("Amon Hen", "Anduin", 5)
    mapa.adicionar_aresta("Anduin", "Angband", 10)
    mapa.adicionar_aresta("Angband", "Annuminas", 15)
    mapa.adicionar_aresta("Barad-dûr", "Bree", 8)
    mapa.adicionar_aresta("Bree", "Caras Galadhon", 12)
    mapa.adicionar_aresta("Caras Galadhon", "Gondolin", 20)
    mapa.adicionar_aresta("Gondolin", "Edoras", 30)
    mapa.adicionar_aresta("Edoras", "Rivendell", 18)
    mapa.adicionar_aresta("Amon Hen", "Gondolin", 25)
    
    print("\nMapa Inicial (Matriz de Adjacência):")
    mapa.exibir_matriz()
    
    print("\nMapa Inicial (Lista de Adjacência):")
    mapa.exibir_lista()

    while True:
        print("\n1. Adicionar Cidade")
        print("2. Remover Cidade")
        print("3. Adicionar Estrada (Rota)")
        print("4. Remover Estrada (Rota)")
        print("5. Exibir Mapa (Matriz de Adjacência)")
        print("6. Exibir Mapa (Lista de Adjacência)")
        print("7. Voltar ao Menu Principal")

        sub_escolha = input("Escolha uma opção: ")

        if sub_escolha == '1':
            cidade = input("Digite o nome da cidade a ser adicionada: ")
            if cidade not in mapa.cidades:
                mapa.cidades.append(cidade)
                mapa.lista_adj[cidade] = []
                print(f"Cidade '{cidade}' adicionada com sucesso!")
            else:
                print("Cidade já existe no mapa.")

        elif sub_escolha == '2':
            cidade = input("Digite o nome da cidade a ser removida: ")
            if cidade in mapa.cidades:
                mapa.cidades.remove(cidade)
                del mapa.lista_adj[cidade]
                for adjacentes in mapa.lista_adj.values():
                    if cidade in adjacentes:
                        adjacentes.remove(cidade)
                print(f"Cidade '{cidade}' removida com sucesso!")
            else:
                print("Cidade não encontrada.")

        elif sub_escolha == '3':
            cidade1 = input("Digite o nome da cidade 1: ")
            cidade2 = input("Digite o nome da cidade 2: ")
            peso = int(input(f"Digite o peso (distância) entre {cidade1} e {cidade2}: "))
            if cidade1 in mapa.cidades and cidade2 in mapa.cidades:
                mapa.adicionar_aresta(cidade1, cidade2, peso)
                print(f"Estrada entre '{cidade1}' e '{cidade2}' com distância {peso} adicionada com sucesso!")
            else:
                print("Uma ou ambas as cidades não foram encontradas no mapa.")

        elif sub_escolha == '4':
            cidade1 = input("Digite o nome da cidade 1: ")
            cidade2 = input("Digite o nome da cidade 2: ")
            if cidade1 in mapa.cidades and cidade2 in mapa.cidades:
                mapa.remover_aresta(cidade1, cidade2)
                print(f"Estrada entre '{cidade1}' e '{cidade2}' removida com sucesso!")
            else:
                print("Uma ou ambas as cidades não foram encontradas no mapa.")

        elif sub_escolha == '5':
            mapa.exibir_matriz()

        elif sub_escolha == '6':
            mapa.exibir_lista()

        elif sub_escolha == '7':
            return mapa

        else:
            print("Opção inválida. Tente novamente.")

# --------------------- NAVEGAÇÃO ------------------------

def exibir_caminho(caminho, cidade_inicial, cidade_destino):
    caminho_percorrido = []
    cidade = cidade_destino
    while cidade != cidade_inicial:
        caminho_percorrido.append(cidade)
        cidade = caminho[cidade]
    caminho_percorrido.append(cidade_inicial)
    caminho_percorrido.reverse()
    return caminho_percorrido

def menu_navegacao():
    cidades = [
        "Amon Hen", "Anduin", "Angband", "Annuminas", "Barad-dûr", 
        "Bree", "Caras Galadhon", "Gondolin", "Edoras", "Rivendell"
    ]
    mapa = Grafo(cidades)

    mapa.adicionar_aresta("Amon Hen", "Anduin", 5)
    mapa.adicionar_aresta("Anduin", "Angband", 10)
    mapa.adicionar_aresta("Angband", "Annuminas", 15)
    mapa.adicionar_aresta("Barad-dûr", "Bree", 8)
    mapa.adicionar_aresta("Bree", "Caras Galadhon", 12)
    mapa.adicionar_aresta("Caras Galadhon", "Gondolin", 20)
    mapa.adicionar_aresta("Gondolin", "Edoras", 30)
    mapa.adicionar_aresta("Edoras", "Rivendell", 18)
    mapa.adicionar_aresta("Amon Hen", "Gondolin", 25)

    while True:
        print("\n=== MENU DE NAVEGAÇÃO E CAMINHOS ÓTIMOS ===")
        print("1. Pesquisa de Profundidade (DFS)")
        print("2. Pesquisa em Largura (BFS)")
        print("3. Caminho de Menor Custo (Dijkstra)")
        print("4. Colorir Grafo (Welch-Powell)")
        print("5. Ordenação Topológica (Kahn)")
        print("6. Árvore Geradora Mínima (Kruskal)")
        print("7. Árvore Geradora Mínima (Prim)")
        print("8. Voltar ao Menu Principal")

        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            cidade_inicial = input("Digite a cidade inicial: ")
            if cidade_inicial not in mapa.cidades:
                print(f"Cidade '{cidade_inicial}' não encontrada no mapa.")
                continue
            visitado = mapa.dfs(cidade_inicial)
            print(f"Cidades visitadas (DFS): {', '.join(visitado)}")

        elif escolha == '2':
            cidade_inicial = input("Digite a cidade inicial: ")
            if cidade_inicial not in mapa.cidades:
                print(f"Cidade '{cidade_inicial}' não encontrada no mapa.")
                continue
            distancias = mapa.bfs(cidade_inicial)
            print(f"Distâncias a partir de {cidade_inicial} (BFS):")
            for cidade, distancia in distancias.items():
                print(f"{cidade}: {distancia} saltos")

        elif escolha == '3':
            cidade_inicial = input("Digite a cidade inicial: ")
            if cidade_inicial not in mapa.cidades:
                print(f"Cidade '{cidade_inicial}' não encontrada no mapa.")
                continue
            distancias, caminho = mapa.dijkstra(cidade_inicial)
            print(f"Distâncias mínimas a partir de {cidade_inicial} (Dijkstra): {distancias}")
            cidade_destino = input("Digite a cidade de destino para visualizar o caminho: ")
            if cidade_destino not in mapa.cidades:
                print(f"Cidade '{cidade_destino}' não encontrada no mapa.")
                continue
            caminho_percorrido = exibir_caminho(caminho, cidade_inicial, cidade_destino)
            print(f"Caminho percorrido (Dijkstra): {' -> '.join(caminho_percorrido)}")

        elif escolha == '4':
            mapa.colorir_grafo()

        elif escolha == '5':
            mapa.ordenacao_topologica()

        elif escolha == '6':
            arvore_geradora_kruskal = kruskal(mapa)
            print("\nÁrvore Geradora Mínima (Kruskal):")
            for cidade1, cidade2, peso in arvore_geradora_kruskal:
                print(f"{cidade1} - {cidade2} : {peso}")

        elif escolha == '7':
            cidade_inicial = input("Digite a cidade inicial para Prim: ")
            arvore_geradora_prim = prim(mapa, cidade_inicial)
            print("\nÁrvore Geradora Mínima (Prim):")
            for cidade1, cidade2, peso in arvore_geradora_prim:
                print(f"{cidade1} - {cidade2} : {peso}")

        elif escolha == '8':
            break

        else:
            print("Opção inválida. Tente novamente.")

# --------------------- MENU PRINCIPAL ------------------------

def menu():
    mapa = None
    while True:
        print("\n=== ATLAS DA TERRA-MÉDIA ===")
        print("1. Busca Sequencial (Locais Desordenados)")
        print("2. Busca Binária (Locais Ordenados)")
        print("3. Busca em Texto (Rabin-Karp nos Contos)")
        print("4. Compressão e Descompressão Huffman")
        print("5. Cofre de Fragmentos (Tabela Hash)")
        print("6. Manipulação do Mapa (Cidades e Estradas)")
        print("7. Navegação e Caminhos Ótimos") 
        print("8. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            fragmentos = ler_lista_txt("fragmentos_desordenados.txt")
            alvo = input("Digite o nome do local a buscar: ")
            inicio_tempo = time.time()
            posicao, comparacoes = busca_sequencial(fragmentos, alvo)
            fim_tempo = time.time()
            if posicao != -1:
                print(f"\n'{alvo}' encontrado na posição {posicao}. Comparações: {comparacoes}")
            else:
                print(f"\n'{alvo}' não encontrado. Comparações: {comparacoes}")
            print(f"Tempo: {(fim_tempo - inicio_tempo):.6f} segundos")

        elif escolha == '2':
            fragmentos_ordenados = ler_lista_txt("fragmentos_ordenados.txt")
            alvo = input("Digite o nome do local a buscar: ")
            inicio_tempo = time.time()
            posicao, comparacoes = busca_binaria(fragmentos_ordenados, alvo)
            fim_tempo = time.time()
            if posicao != -1:
                print(f"\n'{alvo}' encontrado na posição {posicao}. Comparações: {comparacoes}")
            else:
                print(f"\n'{alvo}' não encontrado. Comparações: {comparacoes}")
            print(f"Tempo: {(fim_tempo - inicio_tempo):.6f} segundos")

        elif escolha == '3':
            menu_rabin_karp()

        elif escolha == '4':
            menu_huffman()

        elif escolha == '5':
            menu_tabela_hash()

        elif escolha == '6':
            mapa = menu_mapas()

        elif escolha == '7':
            menu_navegacao()

        elif escolha == '8':
            print("Encerrando o Atlas.")
            break

        else:
            print("Opção inválida. Tente novamente.")
            
if __name__ == "__main__":
    menu()