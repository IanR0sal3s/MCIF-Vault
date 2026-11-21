---
title: Extração e Análise Offline de EVTX (evtx_dump, jq, FullEventLogView e EvtxECmd)
tipo: ferramenta
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 4
bloco: 1
fonte_aula: EI_ASSI_1S2026-27_cap04_v01_LOGs_parte01_v1---ULO.pdf; 16---MCIF_ASSI_1S2026-27_ficha_logs_v1---ULO.pdf
tags:
  - assi
  - logs
  - evtx
  - evtx_dump
  - jq
  - fulleventlogview
  - evtxecmd
  - timeline-explorer
  - ficha-16
aliases:
  - evtx_dump e jq
  - FullEventLogView
  - EvtxECmd
  - Ficha 16 ASSI
atualizado: 2026-11-21
---

# Extração e Análise Offline de EVTX (`evtx_dump`, `jq`, `FullEventLogView` e `EvtxECmd`)

Para analisar grandes volumes de ficheiros `.evtx` de forma rápida ou em triagem forense offline, recorre-se a ferramentas especializadas de conversão para JSON/CSV e agregação visual.

## 1. `evtx_dump` + `jq` (Extração Rápida em JSON)

* **`evtx_dump`** (open source em Rust): converte ficheiros `.evtx` para `JSON`, `JSONL` (sem indentação) ou `XML` com elevada velocidade.
  ```cmd
  evtx_dump.exe -f out.json -o json log.evtx
  ```
* **`jq`** (*JSON Query*, instalável no Windows via `winget install jqlang.jq`): permite filtrar campos específicos diretamente a partir do output de `evtx_dump` em pipeline. A flag `--dont-show-record-number` remove os cabeçalhos de texto para manter JSON válido para o `jq`.

**Pipelines úteis da aula:**

```cmd
:: Listar todos os Event IDs distintos em Security.evtx
evtx_dump.exe Security.evtx -o json --dont-show-record-number | jq ".Event | .System.EventID" | sort /unique

:: Extrair EventData apenas dos eventos 4616 e 4624
evtx_dump.exe Security.evtx -o json --dont-show-record-number | jq ".Event | select(.System.EventID==4616 or .System.EventID==4624) | .EventData"

:: Listar processos distintos referidos em Security.evtx
evtx_dump.exe Security.evtx -o json --dont-show-record-number | jq ".Event | .EventData.ProcessName" | sort /unique

:: Extrair AttachedFiles de crashes (Event ID 1001) em Application.evtx
evtx_dump.exe Application.evtx -o json --dont-show-record-number | jq ".Event | select(.System.EventID == 1001) | .EventData.AttachedFiles"
```

---

## 2. Ferramentas Práticas de Triagem (Ficha 16)

### `FullEventLogView` (NirSoft)
Permite agregar e consultar todos os registos do Windows Event Log numa única interface ou via CLI, filtrando por canal e exportando relatórios HTML:

```cmd
:: Filtrar apenas um canal específico (ex.: ligações Wi-Fi)
fulleventlogview.exe /ChannelFilter 2 /ChannelFilterStr Microsoft-Windows-WLAN-AutoConfig/Operational

:: Exportar o canal filtrado para HTML ordenado pela 1.ª coluna
fulleventlogview.exe /ChannelFilter 2 /ChannelFilterStr Microsoft-Windows-WLAN-AutoConfig/Operational /shtml %TEMP%\a.html /sort 1
```

### `EvtxECmd.exe` + `TimelineExplorer` (Eric Zimmerman)
Fluxo padrão de forense Windows para converter `.evtx` individuais ou diretórios inteiros em CSV estruturado e analisá-los em grelha interativa:

```cmd
:: Processar um único ficheiro EVTX para CSV
EvtxECmd.exe -f "C:\Windows\System32\winevt\Logs\Microsoft-Windows-PowerShell%4Operational.evtx" --csv "%TEMP%\winlogs"

:: Processar uma pasta completa com cópia dos logs para CSV
EvtxECmd.exe -d %TEMP%\winMylogs --csv "%TEMP%\winlogs"
```

O CSV gerado é aberto no **`TimelineExplorer`**, onde se pode agrupar por `EventId`, filtrar por texto/datas e correlacionar eventos rapidamente.

> [!NOTE] Prática da Ficha 16 (`OAlerts.evtx`)
> Ao fechar um documento modificado no Microsoft Word e confirmar a gravação na caixa de diálogo, o Microsoft Office regista o alerta no ficheiro **`OAlerts.evtx`** (`%SYSTEMROOT%\system32\winevt\Logs`), demonstrando como ações de interface do utilizador ficam documentadas em logs dedicados.

---

## Perguntas de revisão

1. **Porque se inclui `--dont-show-record-number` ao encaminhar o output do `evtx_dump` para o `jq`?**

> [!success]- Ver Resposta
> Porque remove a linha textual de número de registo que o `evtx_dump` imprime antes de cada evento, garantindo que o `jq` recebe apenas objetos JSON válidos.

2. **Qual a diferença entre as flags `-f` e `-d` no `EvtxECmd.exe`?**

> [!success]- Ver Resposta
> `-f` processa um único ficheiro `.evtx`, enquanto `-d` processa todos os ficheiros `.evtx` contidos numa diretoria, consolidando-os em CSV para análise no `TimelineExplorer`.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Ferramentas Nativas e CLI para EVTX (WEVTUtil, psloglist e PowerShell)]] | `mesmo bloco` |
| **Seguinte** | [[Deteção Forense de PowerShell e Persistência (Task Scheduler) em EVTX]] | `muda para Bloco 02` |
| **Índice** | [[Capítulo 4 - Logs]] · [[00 ASSI]] | `Bloco 01` |

### Conceitos Relacionados

* [[Eric Zimmerman bstrings - Parâmetros, Expressões Regulares e Exercícios]] · `ASSI · Cap. 3`
* [[Threat Hunting em EVTX - Regras SIGMA, APT-Hunter, Chainsaw e Hayabusa]] · `ASSI · Cap. 4`
