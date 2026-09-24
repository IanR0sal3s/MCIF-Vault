---
title: Home
tipo: indice
tags:
  - moc
  - mcif
atualizado: 2026-09-23
---

# MCIF Vault — Base de Conhecimento Colaborativa

Repositório aberto e colaborativo de notas de estudo e investigação para o **Mestrado em Cibersegurança e Informática Forense (MCIF)**.

Este espaço foi desenhado para ser partilhado e expandido pela comunidade de estudantes e investigadores, servindo como uma fonte central, limpa e estruturada de conhecimento técnico.

> [!NOTE] Guia do Repositório
> Para detalhes completos sobre a arquitetura de MOCs, estrutura de diretórios e boas práticas de contribuição no GitHub, consulta o [[README|Guia do Repositório (README)]].

---

## 📚 Unidades Curriculares

| Sigla    | Unidade Curricular                                          | Docente            | Semestre | Estado                          |
| :------- | :---------------------------------------------------------- | :----------------- | :------- | :------------------------------ |
| **ASSI** | [[00 ASSI]] (Administração Segura de Sistemas Informáticos) | Patrício Domingues | S1       | Concluído (Capítulo 1 — 180 slides) |
| *PARSI*  | *Políticas e Análise de Risco na Segurança de Informação*   | Nuno Salvador      | S1       | Planeado                        |
| *AFD1*   | *Análise Forense Digital I*                                 | Miguel Frade       | S1       | Planeado                        |
| *SRC*    | *Segurança em Redes de Computadores*                        | Luís frazão        | S1       | Planeado                        |
| *COD1*   | *Cibersegurança Ofensiva e Defensiva I*                     | Leonel Santos      | S1       | Planeado                        |

---

## 🛠️ Guia do Colaborador (Como Contribuir)

Para manter o repositório consistente, fiável e navegável tanto no GitHub como no Obsidian, todos os contributos devem seguir estas diretrizes:

### 1. Estrutura e Organização de Pastas
* Cada Unidade Curricular tem a sua pasta de topo com a respetiva sigla (ex.: `ASSI/`).
* Na raiz da UC reside o ficheiro MOC principal (`00 <SIGLA>.md`).
* Os conteúdos organizam-se por pastas de capítulos numeradas (`Capítulo 01 - Nome/`), e debaixo destes em **blocos temáticos numerados** (ex.: `01 - Arranque e UEFI/`, `02 - Processos.../`).
* Esta numeração assegura uma ordem cronológica intuitiva tanto no Obsidian como no explorador de ficheiros do GitHub.

### 2. Princípio da Atomicidade
* **Uma ideia central por nota**: crie notas focadas em vez de documentos longos e monolíticos.
* O título do ficheiro deve ser autoexplicativo e corresponder exatamente ao conceito para facilitar ligações do tipo `[[Conceito]]`.
* Use o campo `aliases` no cabeçalho YAML para sinónimos, siglas ou variações em inglês.

### 3. Rigor nos Conteúdos (Aula vs. Extensões)
* **O que foi lecionado vem sempre primeiro**: a base de cada nota deve refletir fielmente os slides, demonstrações e laboratórios da UC.
* Informação complementar, ferramentas adicionais e aprofundamentos devem ser colocados sob uma secção designada `## Além da aula` para distinguir o programa oficial de contributos externos.

### 4. Template Obrigatório
* Toda a nova nota deve utilizar o modelo `_templates/Nota de estudo.md`.
* Mantenha o cabeçalho YAML preenchido (`mestrado`, `uc`, `sigla_uc`, `capitulo`, `tipo`, `tags`, `fonte_aula`, `atualizado`).

### 5. Estilo de Escrita
* **Sem emojis decorativos** no corpo de notas técnicas.
* Callouts do GitHub/Obsidian (`> [!NOTE]`, `> [!WARNING]`, `> [!IMPORTANT]`) apenas para avisos factuais ou alertas de segurança.
* Links internos com formato wikilink: `[[Nome Exato da Nota]]`.

---

## ⚙️ Configuração Recomendada do Obsidian

Ao clonar este repositório para a sua máquina, configure o Obsidian em **Definições (Settings)**:
1. **Ficheiros e Ligações (Files and links)**:
   * *Local predefinido para novas notas (Default location for new notes)*: Selecionar **"Mesma pasta do ficheiro atual" (Same folder as current file)**. Isto evita que ao clicar em ligações ainda inexistentes sejam criados ficheiros vazios na raiz do vault.
   * *Formato da ligação de novas notas (New link format)*: **"Caminho relativo mais curto" (Shortest path when possible)**.
