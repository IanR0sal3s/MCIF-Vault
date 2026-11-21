---
title: Ferramentas Nativas e CLI para EVTX (WEVTUtil, psloglist e PowerShell)
tipo: ferramenta
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 4
bloco: 1
fonte_aula: EI_ASSI_1S2026-27_cap04_v01_LOGs_parte01_v1---ULO.pdf
tags:
  - assi
  - logs
  - evtx
  - wevtutil
  - psloglist
  - powershell
  - cli
aliases:
  - WEVTUtil
  - psloglist
  - Get-WinEvent
  - PowerShell Event Logs
atualizado: 2026-11-21
---

# Ferramentas Nativas e CLI para EVTX (`WEVTUtil`, `psloglist` e PowerShell)

A consulta, configuração e limpeza de Windows Event Logs em linha de comando ou scripts realiza-se através do utilitário nativo `wevtutil`, do `psloglist` (Sysinternals) e dos cmdlets PowerShell (`Get-WinEvent`).

## 1. `WEVTUtil` (Utilitário Nativo do Windows)

Ferramenta CLI muito versátil (requer privilégios de administrador para a maioria das operações de escrita ou consulta a `Security`).

| Operação | Exemplo de Comando | Notas |
| :--- | :--- | :--- |
| **Listar canais de log** | `wevtutil el` | Pode combinar-se com `sfk filter +count` (~1100+ logs no W10/W11). |
| **Listar publicadores** | `wevtutil ep` (`enum-publishers`) | Serviços/aplicações que escrevem no Event Log. |
| **Consultar configuração** | `wevtutil gl Application` | Mostra `logFileName`, `retention`, `autoBackup` e `maxSize`. |
| **Alterar tamanho máximo** | `wevtutil sl Application /ms:33554432` | Valor em bytes (`32 MiB`); mínimo permitido é `1 MiB` (`1048576`). |
| **Consultar / exportar eventos** | `wevtutil qe System /count:30 /rd:true /f:text > out.txt` | `/rd:true` ordena do mais recente para o mais antigo; omissão de `/f:` gera `XML`. |
| **Filtrar por Event ID (XPath)** | `wevtutil qe System /count:50 /rd:true /q:"Event[System[(EventID=12)]]"` | Exemplo: últimos 50 eventos de arranque (*startup*). |
| **Limpar um log** | `wevtutil cl Application` | Requer CMD com privilégios de administrador. |

---

## 2. `psloglist` (Sysinternals)

Utilitário CLI focado em exportação rápida (especialmente em formato CSV) e filtragem simples.

| Flag | Função | Exemplo |
| :--- | :--- | :--- |
| `-s` / `-x` | Formato CSV / informação estendida | `psloglist -s -x security` |
| `-t <char>` | Define separador CSV personalizado | `psloglist -s -t #` |
| `-i` / `-e` | Incluir / excluir lista de Event IDs | `psloglist -i 4624,4625 security` |
| `-o <str>` | Filtrar por origem/string | `psloglist -s -o "disk"` |
| `-f ew` | Apenas erros (`e`) e avisos (`w`) | `psloglist -f ew` |
| `-h <n>` / `-b <data>` | Últimas `n` horas / anteriores a `mm/dd/YYYY` | `psloglist /h 2 security` |
| `-r` / `-w` | Ordem inversa (*reverse*) / aguarda novas entradas | `psloglist -r -s -i 1000 application` |
| `-l <ficheiro>` | Ler a partir de um ficheiro `.evtx` específico | `psloglist -l ficheiro.evtx -s -x` |

> [!WARNING] Limitação Importante do `psloglist`
> Por omissão, o `psloglist` só acede diretamente a um conjunto restrito de logs clássicos (`Application`, `HardwareEvents`, `Internet Explorer`, `Key Management Service`, `OAlerts`, `Security`, `System`, `Windows PowerShell`). Para analisar qualquer outro canal moderno é obrigatório usar `-l <caminhoCompleto>`.

---

## 3. PowerShell e Windows Event Logs

O cmdlet clássico `Get-EventLog` está ***deprecated***; deve usar-se **`Get-WinEvent`** (que suporta todos os canais `.evtx` e ficheiros offline).

* **Listar todos os logs e o respetivo volume**:
  ```powershell
  Get-WinEvent -ListLog * | Select-Object LogName, RecordCount, MaximumSizeInBytes | Sort-Object RecordCount -Descending | Format-Table -AutoSize
  ```
* **Propriedades de um log**: `Get-WinEvent -ListLog System | Format-List -Property *`
* **Ler ficheiro `.evtx` offline e exportar para CSV**:
  ```powershell
  Get-WinEvent -Path .\ficheiro.evtx | Select-Object -First 10 | Export-Csv a.csv
  Get-WinEvent -Path 'OAlerts.evtx' -MaxEvents 100
  ```
  *(O ficheiro `OAlerts.evtx` regista caixas de alerta/diálogo das aplicações Microsoft Office.)*
* **Escrever entrada sintética**:
  ```powershell
  Write-EventLog "OAlerts" -Source "Microsoft Office 15 Alerts" -EventID 300 -Message "fake message"
  ```
* **Limpar logs** (individual ou em massa — técnica usada por *red teams* / atacantes):
  ```powershell
  Clear-EventLog -LogName Security
  wevtutil el | ForEach-Object { wevtutil cl "$_" }
  ```
  *(Limpar o log `Security` gera automaticamente uma entrada de auditoria — Event ID `1102` — a indicar que o log foi limpo.)*

---

## Perguntas de revisão

1. **Qual a principal limitação do `psloglist` face ao `wevtutil` ou `Get-WinEvent`, e como contorná-la?**

> [!success]- Ver Resposta
> O `psloglist` apenas consulta diretamente 8 logs clássicos (`Application`, `System`, `Security`, `OAlerts`, `Windows PowerShell`, etc.). Para ler outros canais modernos é necessário apontar diretamente para o ficheiro com a opção `-l <ficheiro.evtx>`.

2. **Que cmdlet PowerShell substitui o `Get-EventLog` (*deprecated*) e que comando limpa todos os logs do sistema de uma vez?**

> [!success]- Ver Resposta
> Deve usar-se `Get-WinEvent`. A limpeza em massa faz-se com `wevtutil el | ForEach-Object { wevtutil cl "$_" }`.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Windows Event Log - Arquitetura, Retenção e Event IDs Críticos]] | `mesmo bloco` |
| **Seguinte** | [[Extração e Análise Offline de EVTX (evtx_dump, jq, FullEventLogView e EvtxECmd)]] | `mesmo bloco` |
| **Índice** | [[Capítulo 4 - Logs]] · [[00 ASSI]] | `Bloco 01` |

### Conceitos Relacionados

* [[Processos e linha de comandos no Windows]] · `ASSI · Cap. 1`
* [[Extração de Strings no Windows - Sysinternals strings e Swiss File Knife (sfk)]] · `ASSI · Cap. 3`
