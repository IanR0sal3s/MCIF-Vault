---
title: Processos e linha de comandos no Windows
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 2
tipo: procedimento
tags:
  - assi
  - windows
  - processos
  - sysinternals
  - cli
aliases:
  - Processos Windows
  - Linha de Comandos
  - tasklist
  - pslist
  - btop4win
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v4.pdf
fontes:
  - "https://github.com/aristocratos/btop4win"
atualizado: 2026-11-21
---

# Processos e Linha de Comandos no Windows

A linha de comandos do Windows (`cmd.exe`) e os utilitários de inspeção de processos (`tasklist`, suite Sysinternals e `btop4win`) permitem listar processos em execução, serviços alojados, DLLs carregadas e automatizar tarefas de administração.

## 1. Consola e Regra de Espaços em Caminhos

* **Acesso**: `Win + R` → `cmd` (usar em **modo administrador** para operações de gestão/auditoria).
* **Espaços em nomes**: no `cmd`, o espaço separa argumentos — `dir Pasta 1` é interpretado como dois parâmetros (`Pasta` e `1`). Recomenda-se usar sublinhados (`_`) ou delimitar sempre entre aspas (`dir "Pasta 1"`).

---

## 2. Utilitários de Listagem de Processos

| Ferramenta | Origem | Função Principal |
| :--- | :--- | :--- |
| **`tasklist`** | Nativo (CLI) | Lista processos em execução com filtros, serviços, DLLs e apps UWP. |
| **Gestor de Tarefas** | Nativo (`Ctrl+Shift+Esc`) | Monitorização gráfica de processos e recursos. |
| **Process Explorer** | Sysinternals (GUI) | Árvore de processos pai-filho, DLLs e localizador de processos. |
| **`pslist`** | Sysinternals (CLI) | Listagem flexível de processos, *threads*, memória, árvore e hosts remotos. |
| **`pskill`, `psexec`, `psservice`** | Sysinternals (CLI) | Terminar processos, execução remota e gestão de serviços. |
| **`btop++` (`btop4win`)** | Open-source (TUI) | Monitor de recursos e processos em modo texto. |

---

## 3. Comando `tasklist` (Nativo)

```cmd
tasklist                                     :: Lista processos ativos (/V para modo verboso)
tasklist /SVC                                :: Lista serviços hospedados por cada processo (ex.: svchost.exe)
tasklist /M                                  :: Lista processos e DLLs carregadas
tasklist /APPS                               :: Lista processos ligados a apps Windows UWP
tasklist /FI "MEMUSAGE ge 45000"             :: Processos com uso de memória >= 45000 KB (~45 MB)
tasklist /APPS /FI "MEMUSAGE ge 45000"       :: Apps UWP com >= ~45 MB de memória
tasklist /FI "IMAGENAME eq notepad.exe"      :: Filtra por nome de executável
tasklist /svc | find /c "svchost.exe"        :: Conta instâncias de svchost.exe em execução
```

---

## 4. Suite Sysinternals: `pslist` e Risco do `psexec`

```cmd
pslist [-d] [-m] [-x] [-t] [-e] [-s [n] [-r n]] [\\computer [-u user] [-p pass]] [name|pid]
```

* **`-d`**: detalhe de *threads* · **`-m`**: detalhe de memória · **`-x`**: processos + memória + *threads* · **`-t`**: árvore de processos · **`-e`**: correspondência exata do nome · **`-s [n]`** / **`-r n`**: modo *task-manager* por `n` segundos com taxa de atualização `r` · **`\\computer`**: consulta remota.

> [!WARNING] Abuso do `psexec`
> O **`psexec`** (Sysinternals) é frequentemente empregue por atacantes para executar processos remotamente em redes Windows (movimento lateral).

---

## 5. Atalhos Windows Úteis

`Win + V` (clipboard multinível) · `Win + .` (emojis) · `Win + E` (Explorador) · `Win + Q` (Pesquisa Windows) · `Win + Shift + S` (captura de ecrã / OCR) · `Win + N` (notificações).

---

## Perguntas de revisão

1. **Qual é a principal funcionalidade do comando nativo `tasklist` e o que mostram as flags `/SVC`, `/M` e `/APPS`?**

> [!success]- Ver Resposta
> O `tasklist` exibe a lista de processos em execução no sistema. `/SVC` mostra os serviços alojados em cada processo, `/M` lista as DLLs carregadas e `/APPS` lista os processos de aplicações UWP.

2. **Na ferramenta `pslist`, que informação devolvem os parâmetros `-t`, `-x` e `-e`?**

> [!success]- Ver Resposta
> `-t` mostra a árvore de processos (pai-filho), `-x` combina processos, memória e *threads*, e `-e` exige correspondência exata do nome do processo.

3. **Porque é que o `psexec` merece especial atenção em cibersegurança?**

> [!success]- Ver Resposta
> Porque, embora seja um utilitário legítimo da Sysinternals, é frequentemente usado por atacantes para executar processos remotamente em redes Windows.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[PKfail - Vulnerabilidade do UEFI Secure Boot]] | `Bloco 01` |
| **Seguinte** | [[Comando forfiles]] | `mesmo bloco` |
| **Índice** | [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]] · [[00 ASSI]] | `Bloco 02` |

### Conceitos Relacionados

* [[Serviços Windows]] · `Bloco 03`
* [[svchost.exe]] · `Bloco 03`
* [[Aplicações UWP (Universal Windows Platform) - Visão Geral]] · `Bloco 04`
* [[Investigação Forense Digital - Análise Live vs Post-Mortem]] · `AFD1 · Cap. 1`
* [[Diretrizes de Manuseamento - Identificação, Preservação, Isolamento e Correlação]] · `AFD1 · Cap. 1`
