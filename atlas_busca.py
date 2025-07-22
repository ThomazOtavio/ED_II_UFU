import random
import time
import os
import heapq
import string
from collections import Counter

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


def menu():
    while True:
        print("\n=== ATLAS DA TERRA-MÉDIA ===")
        print("1. Busca Sequencial (Locais Desordenados)")
        print("2. Busca Binária (Locais Ordenados)")
        print("3. Busca em Texto (Rabin-Karp nos Contos)")
        print("4. Compressão e Descompressão Huffman")
        print("5. Cofre de Fragmentos (Tabela Hash)")
        print("6. Sair")

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
            print("Encerrando o Atlas.")
            break

        else:
            print("Opção inválida. Tente novamente.")
            
if __name__ == "__main__":
    menu()