# 📜 Atlas da Terra-média – Enciclopédia Interativa de Arda

## 🏰 Tema do Projeto e Justificativa

O **Atlas da Terra-média** será um sistema interativo que permite consultar, pesquisar e explorar as localidades, povos, linhagens, eventos históricos e culturas do universo de Arda, baseado nas obras de J.R.R. Tolkien (*O Silmarillion*, *O Hobbit*, *O Senhor dos Anéis* e outros).

Este tema foi escolhido por possibilitar a aplicação natural dos conceitos de **Estruturas de Dados II** em um contexto rico em relações, buscas e conexões. O sistema simulará a exploração da história da Terra-média como um verdadeiro navegador de lore, valorizando a consulta eficiente de informações.

---

## 🧩 Visão Geral das Funcionalidades

1. **Enciclopédia de Locais da Terra-média**  
   - Consulta de locais históricos com descrição, eventos associados e povos relacionados.

2. **Registro Genealógico (Linhagens)**  
   - Representação das árvores genealógicas dos principais personagens.

3. **Conexões entre Povos e Reinos**  
   - Relações políticas, culturais e migratórias ao longo das Eras.

4. **Linha do Tempo de Eventos Históricos**  
   - Sequência cronológica de guerras, fundações e eventos marcantes.

5. **Sistema de Busca Avançada**  
   - Pesquisa eficiente por nomes, raças, eras e categorias (busca textual e hash).

6. **Relatórios Estatísticos da Lore**  
   - Dados analíticos sobre populações, eventos e relevância histórica.

7. **Sistema de Salvamento com Compressão de Dados**  
   - Compressão da base de dados utilizando Huffman ou RLE.

8. **Mapa Conceitual (Grafo de Conexões)**  
   - Relações entre personagens, reinos e povos modeladas como um grafo.

---

## 📚 Integração da Ementa com o Projeto

| Tópico da Ementa                       | Aplicação no Projeto Atlas da Terra-média                                  |
|-----------------------------------------|----------------------------------------------------------------------------|
| **Teoria da Complexidade**             | Consultas e análises de grandes árvores e grafos históricos.               |
| **Busca Sequencial, Binária, Hashing** | Busca por localidades, personagens, eventos e raças.                      |
| **Busca em Texto**                     | Filtros por palavras e frases dentro da lore.                              |
| **Compressão de Dados (RLE/Huffman)**  | Salvamento comprimido da base de dados.                                    |
| **Grafos (caminhos, conexões, redes)** | Representação de relações políticas e genealógicas.                        |
| **Algoritmos Gulosos**                 | Sugestão de rotas de leitura otimizadas pela relevância histórica.         |

---

## 🛠️ Tecnologias Escolhidas

- **Linguagem de Programação:** Python 3.x  
- **IDE:** PyCharm  
- **Ambiente de Execução:** PyCharm 
- **Bibliotecas Possíveis:** `collections`, `heapq`, `networkx`, `pickle` ou `json`, `zlib`

---

## 📅 Próximas Etapas

- Definição de classes básicas (`Local`, `Evento`, `Personagem`, `Povo`).
- Implementação inicial do sistema de busca textual.
- Criação da estrutura de grafo com `networkx` (opcional).
- Implementação do módulo de compressão e salvamento.
- Protótipo básico no terminal.

---

> Projeto desenvolvido como parte da disciplina **Estruturas de Dados II** – Universidade Federal de Uberlândia (UFU) – 2025  
> Aluno: **Thomaz Otávio Soares Figueiredo**
