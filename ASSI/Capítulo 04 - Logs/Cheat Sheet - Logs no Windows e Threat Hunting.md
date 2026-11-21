---
title: Cheat Sheet - Logs no Windows e Threat Hunting
tipo: cheatsheet
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 4
fonte_aula: EI_ASSI_1S2026-27_cap04_v01_LOGs_parte01_v1---ULO.pdf; EI_ASSI_1S2026-27_cap04_v01_LOGs_parte02_v1.pdf; Fichas 16–18
tags:
  - assi
  - cheatsheet
  - logs
  - evtx
  - event-id
  - sigma
  - sysmon
  - wer
  - etl
  - onedrive
aliases:
  - Cheat Sheet Capítulo 4 ASSI
  - Cheat Sheet Logs Windows
atualizado: 2026-11-21
---

# Cheat Sheet — Logs no Windows e Threat Hunting (ASSI Cap. 4)

Guia de consulta rápida do [[Capítulo 4 - Logs]] · Simulador interativo: [assi_logs_forense.html](../../_assets/assi_logs_forense.html).

---

## 1. Prazos de Retenção Legal / Normativa

| Enquadramento | Prazo |
| :--- | :--- |
| **HIPAA** / **GLBA** | `6 anos` |
| **ISO 27001** | `3 anos` |
| **PCI DSS** / **IPs em Portugal** | `1 ano` |
| **NIS2** | `6 a 18 meses` |

---

## 2. Caminhos Forenses Essenciais

| Artefacto | Localização |
| :--- | :--- |
| **Windows Event Logs (`.evtx`)** | `%SYSTEMROOT%\system32\winevt\Logs` |
| **Logs Ad-Hoc do Windows** | `%SYSTEMROOT%\Logs` |
| **Histórico PowerShell (`PSReadLine`)** | `%UserProfile%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\` *(sem timestamps)* |
| **Sysmon Log** | `%SYSTEMROOT%\system32\winevt\Logs\Microsoft-Windows-Sysmon%4Operational.evtx` |
| **Windows Error Reporting (`.wer`)** | `C:\ProgramData\Microsoft\Windows\WER\ReportArchive` *(UTF-16-LE)* |
| **Delivery Optimization (`.etl`)** | `C:\Windows\ServiceProfiles\NetworkService\AppData\Local\Microsoft\Windows\DeliveryOptimization\Logs` |
| **OneDrive Logs & SQLite** | `%LOCALAPPDATA%\Microsoft\OneDrive\logs\` (`Business1`/`Personal`) e `\settings\` |

---

## 3. Event IDs Críticos para Exame

*(Regra Win 2000/XP -> Vista+: **subtrair `4096`** nos IDs de `Security`, ex.: `4624 - 4096 = 528`.)*

| Log / Canal | Event ID | Significado |
| :--- | :---: | :--- |
| **`Security.evtx`** *(Admin)* | `4624` / `4625` | Logon com sucesso / Logon falhado |
| **`Security.evtx`** | `4648` / `4720` | Logon com credenciais explícitas / Conta criada |
| **`Security.evtx`** | `1102` | **Audit log limpo** (*The audit log was cleared*) |
| **`Security.evtx`** | `4698`–`4702` | Tarefa agendada: criada (`4698`), apagada (`4699`), ativada (`4700`), desativada (`4701`), atualizada (`4702`) |
| **`Task Scheduler Operational`** | `106` / `141` / `200` / `201` | Tarefa instalada / desinstalada / arranque / fim |
| **`PowerShell/Operational`** | `4103` / `4104` | Carregamento de módulos / Script block completo (v5+) |
| **`Windows PowerShell.evtx`** | `400` | Motor PowerShell — **`EngineVersion=2.0`** denuncia *downgrade* v2 |
| **`Partition%4Diagnostic` / `Storsvc`** | `1006` | Ligação de dispositivo de armazenamento USB (GPT=`0`, MBR=`1`; limpo em *major updates*) |
| **`Application.evtx`** | `1000` / `1002` / `1001` | App Crash/Error (`1000`) / App Hang (`1002`) / WER (`1001`, *Information*) |
| **`System.evtx`** | `1001` | **BSOD** (*Error*, origem `WER-SystemErrorReporting`) |

---

## 4. Comandos Essenciais por Ferramenta

| Ferramenta | Comando-Chave | Objetivo |
| :--- | :--- | :--- |
| **`wevtutil`** | `wevtutil qe System /count:30 /rd:true /f:text` | Exportar últimos 30 eventos em texto |
| **`wevtutil`** | `wevtutil sl Application /ms:33554432` | Redimensionar log (em bytes; mín. `1 MiB`) |
| **`wevtutil`** | `wevtutil cl Application` | Limpar log (requer Admin) |
| **`psloglist`** | `psloglist -l ficheiro.evtx -s -x -i 4624` | Ler `.evtx` em CSV estendido filtrado por ID |
| **PowerShell** | `Get-WinEvent -Path .\f.evtx -MaxEvents 100` | Substituto moderno do `Get-EventLog` (*deprecated*) |
| **`evtx_dump` + `jq`** | `evtx_dump.exe Security.evtx -o json --dont-show-record-number \| jq ".Event \| .System.EventID" \| sort /unique` | Listar Event IDs únicos via JSON |
| **`EvtxECmd`** | `EvtxECmd.exe -d %TEMP%\winMylogs --csv "%TEMP%\winlogs"` | Converter pasta de EVTX em CSV p/ `TimelineExplorer` |
| **`APT-Hunter`** | `apt-hunter -p Dir_LOGS -o Results` | Triagem de APTs em CSV/XLSX |
| **`Chainsaw`** | `chainsaw hunt logs/ -s sigma/ --mapping map.yml --csv --output out` | Threat hunting rápido (Rust) com regras SIGMA |
| **`Hayabusa`** | `hayabusa.exe csv-timeline -d logsDir -o out.csv` | Timeline `log2timeline` com regras SIGMA |
| **`Sysmon`** | `sysmon -accepteula -i sysmonconfig-export.xml` (`-c`, `-u`) | Instalar / atualizar / desinstalar serviço Sysmon |
| **`tracerpt`** | `tracerpt dosvc.etl -o -report` | Gerar relatório a partir de ficheiro `.etl` |
| **Delivery Opt.** | `Get-DeliveryOptimizationLog \| Where-Object Message -Like "*ExternalIpAddress*"` | Extrair IP externo dos últimos 28 dias (`dosvc*`) |
| **`OneDriveExplorer`** | `OneDriveExplorer.exe --LIVE LIVE --csv --output-dir c:\temp\out` | Decifrar/exportar logs `.odl` (chave em `general.keystore`) |
| **`sfk`** | `sfk hexfind -text "/SQLite format 3/" -dir . -stat` | Detetar bases SQLite por cabeçalho mágico |

---

## 5. Armadilhas Frequentes de Exame

1. **Gestão circular**: `.evtx` têm por omissão `1–20 MiB`; registos antigos são sobrescritos automaticamente.
2. **Limitação do `psloglist`**: só acede diretamente a 8 logs clássicos; canais modernos exigem `-l <caminho>`.
3. **`PSReadLine` sem timestamps**: regista comandos PowerShell v5+ por ordem, mas sem data/hora.
4. **BSOD vs. WER**: ambos usam Event ID `1001`, mas BSOD está em `System` (*Error*) e WER em `Application` (*Information*).
5. **WER**: 1.ª mensagem de envio remoto em canal aberto; Chrome/Firefox/LibreOffice não usam WER; caso **Storm-0558** (chave privada MSA exposta num *crash dump* em RAM em vez de HSM/TPM).
6. **Delivery Optimization**: `domgmt*` (`32 KiB`, `>1 ano`) vs. `dosvc*` (`ExternalIPAddress`, **apenas últimos 28 dias**).
7. **OneDrive**: desde abril 2022 os `.odl` são cifrados com **ECB 128 bits** (chave em `general.keystore`).

---

## Navegação

* [[Capítulo 4 - Logs|Voltar ao MOC do Capítulo 4]]
* [[00 ASSI|Voltar ao MOC Geral de ASSI]]
