---
title: UWP - Artefactos Forenses e Estrutura de Dados
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 4
tipo: procedimento
tags:
  - assi
  - forense
  - windows
  - uwp
  - appx
  - sqlite
aliases:
  - UWP Forensics
  - Artefactos UWP
  - StateRepository
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v4.pdf
fontes:
  - "Yogesh Khatri, AppxAnalysis (Magnet Summit 2019), https://github.com/ydkhatri/Appx-Analysis"
atualizado: 2026-11-21
---

# Artefactos Forenses em Aplicações UWP

A análise forense de [[Aplicações UWP (Universal Windows Platform) - Visão Geral|aplicações UWP]] concentra-se em **três fontes principais**: a pasta de pacotes do utilizador, as bases SQLite3 do *State Repository* e o ficheiro de memória virtual `swapfile.sys`.

## 1. Mapa dos 3 Locais Forenses UWP

| Fonte Forense | Localização no Disco | Formato / Motor | O que revela |
| :--- | :--- | :--- | :--- |
| **1. Dados por utilizador** | `C:\Users\%username%\AppData\Local\Packages\<APP>\` | Ficheiros da app + **`Settings\settings.dat`** (ficheiro de **Registry**) | Dados locais e configurações privadas de cada aplicação UWP. |
| **2. Inventário global (*State Repository*)** | `C:\ProgramData\Microsoft\Windows\AppRepository\Packages\` | **SQLite3** (`StateRepository-Machine.srd` e `StateRepository-Deployment.srd`) | Listagem e histórico global de aplicações APPX instaladas na máquina. |
| **3. Memória virtual** | `C:\swapfile.sys` | Ficheiro de paginação dedicado | Memória virtual usada por aplicações UWP (permite pesquisa de *strings*). |

> [!IMPORTANT] Armadilha de Exame: `settings.dat` vs. `.srd`
> O ficheiro `%LocalAppData%\Packages\<APP>\Settings\settings.dat` **não é SQLite** — é um **ficheiro de Registry** privado da aplicação. Já `StateRepository-Machine.srd` e `StateRepository-Deployment.srd` são bases de dados **SQLite3** (analisáveis com *DB Browser for SQLite* ou os scripts *AppxAnalysis* de Yogesh Khatri).

---

## Perguntas de revisão

1. **Qual o formato interno de `settings.dat` face a `StateRepository-Machine.srd` e `StateRepository-Deployment.srd`?**

> [!success]- Ver Resposta
> `settings.dat` (`%LocalAppData%\Packages\<APP>\Settings\`) é um **ficheiro de Registry**; os ficheiros `.srd` em `C:\ProgramData\Microsoft\Windows\AppRepository\Packages\` são bases de dados **SQLite3**.

2. **Que ficheiro de paginação utilizam as aplicações UWP para memória virtual?**

> [!success]- Ver Resposta
> O ficheiro **`swapfile.sys`** (distinto do `pagefile.sys` tradicional).

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Aplicações UWP (Universal Windows Platform) - Visão Geral]] | `mesmo bloco` |
| **Seguinte** | [[Estrutura e Hives do Windows Registry]] | `muda para Bloco 05` |
| **Índice** | [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]] · [[00 ASSI]] | `Bloco 04` |

### Conceitos Relacionados

* [[Registry em Aplicações Modernas (MSIX e Helium)]] · `Bloco 06`
* [[Camadas de Organização de Dados e Análise de Sistemas de Ficheiros]] · `AFD1 · Cap. 3`
* [[Diretrizes de Manuseamento - Identificação, Preservação, Isolamento e Correlação]] · `AFD1 · Cap. 1`
* [[Timestamps e Épocas Temporais (UNIX Epoch vs. Windows FILETIME)]] · `Comum/`
