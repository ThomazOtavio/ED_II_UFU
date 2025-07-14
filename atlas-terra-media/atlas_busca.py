# atlas_busca.py

import time
import os

DIRETORIO_DADOS = "./dados/"

def ler_lista_txt(nome_arquivo):
    caminho = os.path.join(DIRETORIO_DADOS, nome_arquivo)
    with open(caminho, 'r', encoding='utf-8') as arquivo:
        return [linha.strip() for linha in arquivo.readlines() if linha.strip()]

def ler_texto_txt(nome_arquivo):
    caminho = os.path.join(DIRETORIO_DADOS, nome_arquivo)
    with open(caminho, 'r', encoding='utf-8') as arquivo:
        return arquivo.read()


def busca_sequencial(fragmentos, alvo):
    comparacoes = 0
    for i, item in enumerate(fragmentos):
        comparacoes += 1
        if item == alvo:
            return i, comparacoes
    return -1, comparacoes


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
            t = (d * (t - ord(texto[s]) * h) + ord(texto[s + m])) % q
            if t < 0:
                t += q

    return posicoes


def menu():
    while True:
        print("\n=== ATLAS DA TERRA-MÉDIA ===")
        print("1. Busca Sequencial (Locais Desordenados)")
        print("2. Busca Binária (Locais Ordenados)")
        print("3. Busca em Texto (Rabin-Karp)")
        print("4. Sair")

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
            texto = ler_texto_txt("tomos_antigos.txt")
            marcas = ler_lista_txt("marcas_corrompidas.txt")
            print("\nBuscando marcas corrompidas...")
            for marca in marcas:
                posicoes = rabin_karp(texto, marca)
                if posicoes:
                    print(f"'{marca}': {len(posicoes)} ocorrência(s).")
                else:
                    print(f"'{marca}': Nenhuma ocorrência.")
            print("\nBusca concluída.")

        elif escolha == '4':
            print("Encerrando o Atlas.")
            break

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()
