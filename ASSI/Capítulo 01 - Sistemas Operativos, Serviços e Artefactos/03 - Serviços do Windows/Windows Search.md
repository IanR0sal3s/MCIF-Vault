---
title: Windows Search
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 3
tipo: procedimento
tags:
  - assi
  - windows
  - wsearch
  - ese
  - sqlite
  - forense
aliases:
  - WSearch
  - Windows Search Service
  - sidr
  - WinSearchDBAnalyzer
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v4.pdf
fontes:
  - "Chivers, H. and Hargreaves, C. Forensic data recovery from the Windows Search database. Digital Investigation 7.3 (2011): 114–126"
  - "https://github.com/strozfriedberg/sidr"
atualizado: 2026-11-21
---

# Windows Search (`WSearch`)

O **Windows Search (`WSearch`)** é o serviço do Windows que indexa ficheiros e metadados numa base de dados para fornecer pesquisas rápidas (Barra de tarefas `Win + Q`, Explorador `F3`, barra de endereço do Edge e Outlook). Por reter nomes, caminhos e metadados mesmo após eliminação de ficheiros, é um artefacto forense valioso.

## 1. Localização, Âmbito e Controlo do Serviço

* **Localização (W10 e W11)**: `%AllUsersProfile%\Microsoft\Search\Data\Applications\Windows\` (`C:\ProgramData\Microsoft\Search\Data\Applications\Windows\`).
* **Indexado por omissão (W11)**: `C:\Users\*` (**exceto `AppData`**) e `Start Menu`.
* **Configuração gráfica**: `Win + Q` → `indexing` ou `control srchadmin.dll` (permite restringir diretórios/tipos ou desativar quando o índice cresce de forma anómala).
* **Controlo CLI (modo administrador)**:
  ```cmd
  sc query wsearch
  sc config WSearch start= disabled
  sc stop WSearch
  ```

---

## 2. Windows 10 (ESE) vs. Windows 11 (SQLite3)

| Critério | Windows 10 | Windows 11 |
| :--- | :--- | :--- |
| **Motor de BD** | **ESE** (*Extended Storage Engine* — usado também em AD, Edge, SRUM) | **SQLite3** (magic number `53 51 4C 69 74 65 20 66 6F 72 6D 61 74 20 33` = ASCII `SQLite format 3`, verificável no `HxD`) |
| **Ficheiros** | **`Windows.edb`** | **`Windows.db`**, **`Windows-gather.db`**, **`Windows-usn.db`** (+ logs `.db-shm` e `.db-wal`) |
| **Estrutura** | **1 registo por ficheiro** (tabelas `SystemIndex_Gthr`, `SystemIndex_GthrPth`, `SystemIndex_PropertyStore`) | **1 campo/propriedade por registo** (um registo do W10 desdobra-se em vários registos no W11) |
| **Ferramentas** | **`WinSearchDBAnalyzer`** (recupera registos apagados e lê sistemas ativos) e **`sidr`** | **`DB Browser for SQLite`** e **`sidr`** |

---

## 3. Extração Forense com `sidr` (*Search Index DB Reporter*)

Ferramenta open source em Rust que suporta **W10 e W11** e exporta para JSON ou CSV:

```cmd
sidr.exe -f json InputDIR
sidr.exe -f csv InputDIR -o Saida_DIR
```

Gera relatórios de **ficheiros indexados**, **atividade** (`activity`) e **histórico de pesquisas** efetuadas na barra de endereços do **Microsoft Edge** (*Internet history*).

---

## Perguntas de revisão

1. **Qual é a principal função do serviço `WSearch` e que pastas indexa por omissão no Windows 11 (com que exceção)?**

> [!success]- Ver Resposta
> Indexa ficheiros e metadados numa base de dados para permitir pesquisas rápidas. No Windows 11 indexa o *Start Menu* e `C:\Users\*`, **exceto a pasta `AppData`**.

2. **O que mudou na base de dados do Windows Search entre o Windows 10 e o Windows 11?**

> [!success]- Ver Resposta
> No **Windows 10** usa motor **ESE** (`Windows.edb`, 1 registo por ficheiro); no **Windows 11** passou para **SQLite3** (`Windows.db`, `Windows-gather.db` e `Windows-usn.db`, acompanhados de `.db-shm`/`.db-wal`, com 1 campo por registo).

3. **Como confirmar num editor hexadecimal que um ficheiro é uma base SQLite3 e que ferramenta extrai dados do Windows Search tanto em W10 como em W11?**

> [!success]- Ver Resposta
> Pelo *magic number* inicial `SQLite format 3` (`53 51 4C 69 74 65 20 66 6F 72 6D 61 74 20 33`). A ferramenta **`sidr`** (`sidr.exe -f csv InputDIR -o Saida_DIR`) suporta ambos.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Serviço Delivery Optimization]] | `mesmo bloco` |
| **Seguinte** | [[Ficha Prática e Questionário - Serviços e Windows Search]] | `mesmo bloco` |
| **Índice** | [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]] · [[00 ASSI]] | `Bloco 03` |

### Conceitos Relacionados

* [[Serviços Windows]] · `mesmo bloco`
* [[Serviço BITS]] · `mesmo bloco`
* [[Caches de Ícones e Miniaturas (IconCache e Thumbcache)]] · `Bloco 13`
* [[Pesquisa de Evidências e Reconstrução de Eventos]] · `AFD1 · Cap. 1`
* [[Camadas de Organização de Dados e Análise de Sistemas de Ficheiros]] · `AFD1 · Cap. 3`
* [[Timestamps e Épocas Temporais (UNIX Epoch vs. Windows FILETIME)]] · `Comum/`
* [[Sistemas de Numeração e Conversão entre Bases]] · `AFD1 · Cap. 3`
