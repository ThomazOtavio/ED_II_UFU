# 📜 Atlas da Terra-Média – Módulo 1: Busca de Dados

Este projeto é parte do **Atlas da Terra-Média**, um software que organiza e consulta registros históricos do universo criado por Tolkien.

## 🛠️ Arquitetura do Módulo

O sistema consiste em um menu interativo, no qual o usuário pode escolher entre diferentes algoritmos de busca para localizar informações nas bases de dados da Terra-Média:

- **Busca Sequencial:** Aplicada sobre uma lista desordenada de localidades.
- **Busca Binária:** Aplicada sobre uma lista alfabeticamente ordenada de localidades.
- **Busca em Texto (Rabin-Karp):** Aplicada sobre textos extensos contendo registros históricos, buscando fragmentos de texto específicos.

Os arquivos `.txt` localizados na pasta `dados/` armazenam as informações utilizadas pelo programa.

---

## 📊 Algoritmos Implementados

| Algoritmo         | Aplicação                                 | Complexidade (Big O)        |
|-------------------|-------------------------------------------|-----------------------------|
| Busca Sequencial  | Localização em listas desordenadas        | O(n)                        |
| Busca Binária     | Localização em listas ordenadas           | O(log n)                    |
| Rabin-Karp        | Busca de padrões em grandes textos        | O(n + m) (hashing eficiente)|

---

## 📁 Dados de Entrada

Os arquivos `.txt` podem ser modificados livremente para testar diferentes cenários. Por padrão, eles contêm dados relacionados à Terra-Média:

- **fragmentos_desordenados.txt** – Lista desordenada de localidades.
- **fragmentos_ordenados.txt** – Lista ordenada de localidades.
- **tomos_antigos.txt** – Texto longo com registros históricos.
- **marcas_corrompidas.txt** – Fragmentos de texto a serem buscados no tomo.

---

## ▶️ Como Executar

Requisitos:
- Python 3.x
- IDE recomendada: VS Code

Execute com:

```bash
python atlas_busca.py
