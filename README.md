# A Guilda – RPG de Gerenciamento de Guilda

## 🎮 Tema do Projeto e Justificativa

**A Guilda** é um simulador de gerenciamento de uma guilda de aventureiros. O jogador assume o papel de mestre da guilda, controlando recursos, recrutando heróis, enviando missões e expandindo sua influência.

O projeto foi escolhido por permitir a aplicação prática e natural dos principais conceitos de Estruturas de Dados II. A ambientação gamificada torna o aprendizado mais lúdico, integrando algoritmos e estruturas em desafios reais dentro da simulação.

---

## 🧩 Visão Geral das Funcionalidades

1. **Cadastro e gestão de heróis**  
   - Nome, classe, nível, atributos e inventário.

2. **Sistema de busca (heróis, missões, itens)**  
   - Busca por nome, classe ou nível, usando algoritmos diversos (linear, binária, hash).

3. **Sistema de missões**  
   - Requisitos de nível e classe, duração, recompensa e perigos.

4. **Gestão de inventário**  
   - Sistema de mochila com limite de peso. Cada herói possui seu inventário.

5. **Simulação de combate e evolução**  
   - Batalhas simples com rolagens, cálculo de dano e XP.

6. **Relatório de desempenho da guilda**  
   - Histórico de missões, XP ganho, mortes, sucessos e falhas.

7. **Sistema de salvamento com compressão de dados (RLE ou Huffman)**  
   - Otimização no salvamento do estado da guilda.

8. **Mapa com caminhos e obstáculos (grafo)**  
   - Representação do mundo e cálculo de rotas com algoritmos como Dijkstra ou BFS.

---

## 📚 Integração da Ementa com o Projeto

| Tópico da Ementa                          | Aplicação no Projeto A Guida |
|------------------------------------------|-------------------------------|
| **Teoria da Complexidade**               | Determinar viabilidade de missões baseado em combinações de heróis (problemas com restrições). |
| **Busca Sequencial, Binária, Hashing**   | Sistema de busca de heróis, missões e itens. |
| **Busca em Texto**                       | Filtragem de logs ou nomes em registros da guilda. |
| **Compressão de Dados (RLE/Huffman)**    | Salvamento eficiente do estado da guilda. |
| **Grafos (rotas, conexões, caminhos)**   | Representação do mundo, planejamento de rotas. |
| **Algoritmos Gulosos**                   | Alocação rápida de recursos, escolha de heróis com melhores atributos para cada missão. |

---

## 🛠️ Tecnologias Escolhidas

- **Linguagem de Programação:** C++  
- **Compilador:** g++ (GCC)  
- **IDE:** Visual Studio Code 

---

## 📅 Próximas Etapas

- Início da codificação da primeira funcionalidade: Cadastro de heróis
- Definição de estruturas iniciais
- Implementação de sistema de busca básica
- Construção de grafo de mundo e missões

---

> Projeto criado como parte da disciplina **Estruturas de Dados II** – Universidade Federal de Uberlândia (UFU) – 2025  
> Aluno: **Thomaz Otávio Soares Figueiredo**
