---
title: Deteção Forense de PowerShell e Persistência (Task Scheduler) em EVTX
tipo: analise
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 4
bloco: 2
fonte_aula: EI_ASSI_1S2026-27_cap04_v01_LOGs_parte01_v1---ULO.pdf
tags:
  - assi
  - logs
  - evtx
  - powershell
  - downgrade
  - psreadline
  - task-scheduler
  - persistencia
  - forense
aliases:
  - Logs PowerShell
  - PowerShell Downgrade Attack
  - PSReadLine
  - Persistência Task Scheduler
atualizado: 2026-11-21
---

# Deteção Forense de PowerShell e Persistência (Task Scheduler) em EVTX

Atacantes utilizam frequentemente o PowerShell para execução ofensiva e o Task Scheduler para obter persistência. Ambos deixam vestígios específicos em logs `.evtx` e ficheiros auxiliares.

## 1. Atividade PowerShell e Ataque de Downgrade

A partir da **versão 5**, o PowerShell regista comandos e scripts executados em logs operacionais dedicados:
* **PowerShell v5**: `Microsoft-Windows-PowerShell/Operational.evtx`
* **PowerShell v6 / v7**: `Microsoft-Windows-PowerShellCore/Operational.evtx`

| Event ID | Log | Significado |
| :---: | :--- | :--- |
| **4103** | `PowerShell/Operational` | Carregamento/execução de módulos (*Module Logging*). |
| **4104** | `PowerShell/Operational` | Registo completo do script executado (*Script Block Logging*). |
| **400** | `Windows PowerShell.evtx` | Início do motor PowerShell — revela **`EngineVersion=2.0`** ou **`HostVersion=2.0`** em caso de *downgrade*. |

### Evasão por Downgrade (PowerShell v2)
Para contornar o registo detalhado (`4103`/`4104`), agentes maliciosos executam `PowerShell -version 2`, versão que não grava esses logs. Contudo, a própria mudança de motor fica denunciada no **`Windows PowerShell.evtx`** através do **Event ID `400`** com `EngineVersion=2.0`. Para verificar a versão atual em consola usa-se `$PSVersionTable`.

### Histórico `PSReadLine`
A partir do PowerShell v5, os comandos interativos executados na consola são guardados em texto simples na pasta:
`%UserProfile%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\`

> [!IMPORTANT] Limitação Forense do `PSReadLine`
> Tal como o `.bash_history` em Linux, o ficheiro do `PSReadLine` regista os comandos pela ordem de execução, mas **sem marcadores temporais (timestamps)**.

---

## 2. Persistência via Task Scheduler

Software malicioso recorre ao Task Scheduler (`taskschd.msc` ou CLI `schtasks` / `schtasks /query /FO CSV`) para garantir execução periódica ou descarregar componentes adicionais. A deteção forense cruza dois logs:

### A) `Security.evtx` (Auditoria de Tarefas)
| Event ID | Significado |
| :---: | :--- |
| **4698** | Criação de uma tarefa agendada (*A scheduled task was created*) |
| **4699** | Remoção de uma tarefa agendada |
| **4700** | Ativação de uma tarefa |
| **4701** | Desativação de uma tarefa |
| **4702** | Atualização de uma tarefa |

Os eventos **`4698`** e **`4699`** são prioritários na suspeita de *malware*. O evento `4698` identifica quem criou a tarefa (`Security ID`, `Account Name`, `Account Domain` e `Logon ID`). Exemplo de extração rápida:
```cmd
psloglist security -x -i 4698,4699,4700,4701,4702 -s
```

### B) `Task Scheduler Operational Log`
Complementa o `Security.evtx` com o ciclo de vida operacional da tarefa:
* **Event ID `106`**: tarefa instalada;
* **Event ID `141`**: tarefa desinstalada;
* **Event ID `200`**: registo temporal do arranque da tarefa;
* **Event ID `201`**: registo temporal do fim da tarefa.

---

## Perguntas de revisão

1. **Porque é que um atacante tenta executar `PowerShell -version 2` e como pode o analista detetar essa tentativa?**

> [!success]- Ver Resposta
> A versão 2 não regista os eventos `4103` (módulos) nem `4104` (script block). Porém, o *downgrade* fica registado no `Windows PowerShell.evtx` através do **Event ID `400`** com `EngineVersion=2.0` ou `HostVersion=2.0`.

2. **Que Event IDs distinguem a criação/remoção de uma tarefa agendada no `Security.evtx` vs. no `Task Scheduler Operational Log`?**

> [!success]- Ver Resposta
> No `Security.evtx`: **`4698`** (criação) e **`4699`** (remoção). No `Task Scheduler Operational Log`: **`106`** (instalação) e **`141`** (desinstalação), além de `200`/`201` para arranque e fim de execução.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Extração e Análise Offline de EVTX (evtx_dump, jq, FullEventLogView e EvtxECmd)]] | `muda do Bloco 01` |
| **Seguinte** | [[Análise Forense de USB e Crashes nos Logs EVTX]] | `mesmo bloco` |
| **Índice** | [[Capítulo 4 - Logs]] · [[00 ASSI]] | `Bloco 02` |

### Conceitos Relacionados

* [[Artefactos Forenses de Execução e Persistência no Registry]] · `ASSI · Cap. 1`
* [[Ferramentas Nativas e CLI para EVTX (WEVTUtil, psloglist e PowerShell)]] · `ASSI · Cap. 4`
