---
title: Análise Forense de USB e Crashes nos Logs EVTX
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
  - usb
  - partition-diagnostic
  - crash
  - bsod
  - forense
aliases:
  - Logs USB EVTX
  - Partition Diagnostic EVTX
  - USBDriveLog
  - Logs de Crash e BSOD
atualizado: 2026-11-21
---

# Análise Forense de USB e Crashes nos Logs EVTX

Além de eventos de autenticação e persistência, os logs `.evtx` preservam evidências diretas da ligação de dispositivos de armazenamento externo e de falhas críticas de aplicações ou do sistema operativo.

## 1. Dispositivos USB de Armazenamento nos Logs EVTX

Dois logs EVTX — **ambos ativos por omissão** — registam a utilização de dispositivos de armazenamento persistente (discos, pens USB, cartões de memória) através do **Event ID `1006`**:

* `Microsoft-Windows-Partition%4Diagnostic.evtx` (`Microsoft-Windows-Partition/Diagnostic`)
* `Microsoft-Windows-Storsvc/Diagnostic`

### O que regista o `Partition%4Diagnostic.evtx`
* Identifica o número do disco (`0` corresponde ao disco de arranque do SO, marcado como *critical*), o tamanho do disco e o estilo de partição (`0` = **GPT**, `1` = **MBR**);
* Em dispositivos **MBR**, regista a identificação das três primeiras partições;
* Em dispositivos **GPT**, regista a assinatura e os 512 octetos da tabela de partição.

> [!WARNING] Volatilidade em Atualizações
> O log `Microsoft-Windows-Partition%4Diagnostic.evtx` é **apagado sempre que ocorre uma atualização *major* do Windows**.

### Ferramentas de Análise
* **`Partition%4DiagnosticParser`** (Python, *theAtropos4n6*): analisa `Microsoft-Windows-Partition%4Diagnostic.evtx` e gera um relatório HTML estruturado.
* **`USBDriveLog`** (NirSoft): ferramenta gráfica que agrega e explora ambos os logs (`Partition/Diagnostic` e `Storsvc/Diagnostic`).

---

## 2. Vestígios de Crash de Aplicações e BSOD em EVTX

Falhas de software, bloqueios de interface e ecrãs azuis (BSOD) ficam registados nos logs `Application` e `System`:

| Situação | Event ID | Nível | Log | Origem (*Source*) |
| :--- | :---: | :--- | :--- | :--- |
| **App Crash / App Error** | `1000` | Error | `Application` | `Application Error` |
| **App Hang** | `1002` | Error | `Application` | `Application Hang` |
| **BSOD** | `1001` | Error | `System` | `Microsoft-Windows-WER-SystemErrorReporting` |
| **WER (Relatório de Erro)** | `1001` | Information | `Application` | `Windows Error Reporting` |

**Extração rápida via `psloglist`**:
```cmd
psloglist -r -s -i 1000 application
psloglist -i 1001 application
```

---

## Perguntas de revisão

1. **Que Event ID e que dois canais EVTX permitem rastrear dispositivos USB de armazenamento, e que evento do sistema pode apagar esse histórico?**

> [!success]- Ver Resposta
> O **Event ID `1006`** nos logs `Microsoft-Windows-Partition/Diagnostic` e `Microsoft-Windows-Storsvc/Diagnostic` (ativos por omissão). O log `Partition%4Diagnostic.evtx` é apagado sempre que ocorre uma atualização *major* do Windows.

2. **Como distinguir nos logs um BSOD de um relatório WER de crash de aplicação, dado que ambos usam o Event ID `1001`?**

> [!success]- Ver Resposta
> Pelo canal e nível: o **BSOD** ocorre no log **`System`** (nível *Error*, origem `Microsoft-Windows-WER-SystemErrorReporting`), enquanto o **WER** de aplicação ocorre no log **`Application`** (nível *Information*, origem `Windows Error Reporting`).

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Deteção Forense de PowerShell e Persistência (Task Scheduler) em EVTX]] | `mesmo bloco` |
| **Seguinte** | [[Threat Hunting em EVTX - Regras SIGMA, APT-Hunter, Chainsaw e Hayabusa]] | `muda para Bloco 03` |
| **Índice** | [[Capítulo 4 - Logs]] · [[00 ASSI]] | `Bloco 02` |

### Conceitos Relacionados

* [[Artefactos Forenses de Dispositivos USB]] · `ASSI · Cap. 1`
* [[Memory Dumps (.dmp) e Windows Error Reporting (WER)]] · `ASSI · Cap. 4`
