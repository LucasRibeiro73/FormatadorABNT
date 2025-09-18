# 📚 Formatador ABNT com Python

![Status do Projeto](https://img.shields.io/badge/Status-Concluído-4CAF50?style=for-the-badge)

_Um script de automação desenvolvido para otimizar a formatação de trabalhos acadêmicos, demonstrando habilidades em manipulação de documentos e lógica de programação em Python._

![Demonstração do Formatador ABNT](https://i.imgur.com/sYvYfUu.png)

---

## 🎯 Sobre o Projeto

Este projeto foi concebido como uma solução prática para um desafio comum a todos os estudantes e pesquisadores brasileiros: a formatação de documentos segundo as normas da ABNT. Mais do que uma ferramenta, o Formatador ABNT é um **case de estudo sobre automação e parsing de texto**, onde apliquei meus conhecimentos em Python para transformar uma tarefa manual, repetitiva e suscetível a erros em um processo automatizado, rápido e eficiente.

A motivação foi desenvolver uma solução robusta que me permitisse aprofundar em conceitos de manipulação de arquivos, estruturas de dados e aplicação de regras de negócio complexas através de algoritmos.

---

## 💡 Problema Abordado

A formatação manual de um trabalho acadêmico pode consumir horas preciosas que poderiam ser dedicadas à pesquisa e escrita. A necessidade de seguir regras estritas de espaçamento, margens, citações e referências torna o processo cansativo e pode levar a inconsistências que impactam a avaliação final do trabalho. O objetivo deste projeto foi eliminar essa dor, criando um sistema que cuida da forma para que o autor possa focar no conteúdo.

---

## 🛠️ Tecnologias e Conceitos Aplicados

Este projeto foi uma excelente oportunidade para aplicar e aprofundar meus conhecimentos nas seguintes áreas:

* **Linguagem Principal:**
    * `Python 3.12.5`: Utilizado pela sua simplicidade, robustez e pelo vasto ecossistema de bibliotecas.

* **Bibliotecas Chave:**
    * `python-docx`: Para a manipulação direta de documentos `.docx`, permitindo a leitura de parágrafos, alteração de estilos, ajuste de fontes, margens e outras propriedades do documento.

* **Conceitos de Engenharia de Software:**
    * **Automação de Tarefas:** O core do projeto, criando um script que executa uma sequência de passos lógicos sem intervenção manual.
    * **Parsing e Análise de Texto:** Desenvolvimento de lógica para identificar padrões no texto, como citações, títulos e referências, para aplicar a formatação correta.
    * **Programação Estruturada:** Organização do código em funções modulares e reutilizáveis, cada uma responsável por uma regra específica da ABNT.
    * **Manipulação de Arquivos (I/O):** Leitura do documento original e criação de um novo arquivo com a formatação aplicada, preservando o conteúdo original.

---

## 🚀 Desafios e Aprendizados

Durante o desenvolvimento, enfrentei desafios interessantes que foram cruciais para meu crescimento:

* **Desafio:** Traduzir a complexidade e as exceções das regras da ABNT (como citações com mais de 3 linhas, notas de rodapé, etc.) em algoritmos eficientes e sem bugs.
* **Aprendizado:** Aprofundei minha capacidade de **abstração e modelagem de problemas**, quebrando um grande desafio em pequenas funções gerenciáveis. Melhorei significativamente minha habilidade de depuração e testes iterativos.

* **Desafio:** Interagir com a estrutura interna de um arquivo `.docx` através da biblioteca `python-docx`, entendendo como estilos e formatações são aplicados em um nível mais baixo.
* **Aprendizado:** Ganhei experiência prática com a **manipulação de formatos de arquivo complexos (OOXML)**, uma habilidade valiosa para projetos de automação e integração de sistemas.

---

## 📈 Evolução do Projeto (Próximos Passos)

Embora a versão atual seja funcional, enxergo diversas oportunidades de evolução que pretendo explorar:

* [ ] **Interface Gráfica (GUI):** Desenvolver uma interface amigável com `Tkinter` ou `PyQt` para que usuários não-técnicos possam usar a ferramenta facilmente.
* [ ] **Versão Web:** Criar uma API com `Flask` ou `Django` para permitir o upload de documentos e formatação online.
* [ ] **Suporte a Outros Formatos:** Adicionar compatibilidade com arquivos `.odt` (LibreOffice) ou até mesmo integração com `LaTeX`.

---

## 📬 Contato

**Lucas Ribeiro**

* **LinkedIn:** [https://www.linkedin.com/in/lucas-ribeiro-7218a0153/](https://www.linkedin.com/in/lucas-ribeiro-7218a0153/)
* **Email:** Lucas.mribeiro.dev@gmail.com