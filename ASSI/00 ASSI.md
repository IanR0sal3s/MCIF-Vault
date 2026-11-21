---
title: ASSI — Administração Segura de Sistemas Informáticos
tipo: indice
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
tags:
  - moc
  - assi
aliases:
  - ASSI
  - 00 ASSI
  - Administração Segura de Sistemas Informáticos
atualizado: 2026-11-21
---

# Administração Segura de Sistemas Informáticos (ASSI)

Unidade curricular do **Mestrado em Cibersegurança e Informática Forense (MCIF)** da **Escola Superior de Tecnologia e Gestão (ESTG)** do **Politécnico de Leiria**.

* **Docente**: Patrício Domingues (Departamento de Engenharia Informática - DEI)
* **Semestre**: 1.º Semestre

---

## 📖 Programa e Capítulos

| Capítulo | Designação | Estado / Cobertura |
| :--- | :--- | :--- |
| **[[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]** | **Sistemas Operativos, Serviços e Artefactos Forenses no Windows**<br/>• **Parte 1**: Arranque, UEFI/PKfail, Processos, Serviços, UWP, Registry e Dispositivos USB (170 slides)<br/>• **Parte 2**: VSS, Prefetch, ShimCache, AmCache, Jump Lists, LNK, Caches Gráficas, Timeline, SRUM, Bloco de Notas W11 e Matriz Forense (158 slides) | Concluído (328 slides mapeados, 47 notas temáticas + 4 Fichas Práticas + 2 Cheat Sheets) |
| **[[Capítulo 2 - Administração de Sistemas]]** | **Administração de Sistemas (*System and Data Management & Access Control*)**<br/>• **Parte A (*System and Data Management*)**: Decommissioning, destruição de papel (`P-1`–`P-7`), *Evil Maid*/*Burner Phones*, sanitização de HDDs e SSDs/NVMe, gestão de ativos, segurança USB (`VeraCrypt`, `BadUSB`, `ValiDrive` — Ficha 11), Hardening, `YellowKey`, CVE/CVSS/CWE, licenciamento e fugas `SAS Tokens` (62 slides)<br/>• **Parte B (*Access Control*)**: Engenharia social (*phishing*, *smishing*, `SMS Blaster`, *quishing*, BEC/*deepfake*), diretrizes NIST `SP 800-63-4`, `bcrypt` (`Okta`), `FortiBleed`, entropia (`Coldcard`), higiene e `KeePassXC` (Ficha 10), `SS7`/`SIM-Jacking`, `TOTP`, `Passkeys` (Ficha 11), *salting*, *key stretching* e `hashcat` (119 slides) | Concluído (181 slides mapeados, 25 notas atómicas + 1 Cheat Sheet) |
| **[[Capítulo 3 - YARA - MOTW - Strings]]** | **YARA, LOKI, Alternate Data Streams (ADS), Mark of the Web (MOTW) e Utilitários de Extração de Strings**<br/>• **Bloco 01**: Pesquisa de Padrões, Malware e IOCs (`YARA`, `yarac`, `YARA-X` / `yr`, `LOKI` Python e `Loki-RS` em Rust — 35 slides, Ficha 14)<br/>• **Bloco 02**: Fluxos Alternativos NTFS (`ADS`), caso `WastedLocker`, `Mark of the Web (MOTW)` / `Zone.Identifier`, exceções (`7-Zip`, `certutil`) e `SmartScreen` (25 slides, Ficha 15)<br/>• **Bloco 03**: Extração e Pesquisa de Strings (`strings` Unix/Linux, Sysinternals `strings.exe`, `sfk strings` e `bstrings` de Eric Zimmerman — 16 slides) | Concluído (76 slides mapeados, 13 notas atómicas + 1 Cheat Sheet) |
| **[[Capítulo 4 - Logs]]** | **Logs no Windows, Threat Hunting e Logs Ad-Hoc**<br/>• **Parte 1 (EVTX & Threat Hunting)**: Retenção legal, `.evt` vs. `.evtx`, Event IDs críticos, `WEVTUtil`, `psloglist`, `Get-WinEvent`, `evtx_dump`+`jq`, Ficha 16 (`FullEventLogView`, `EvtxECmd`), casos USB/PowerShell/Task Scheduler/Crashes, regras `SIGMA`, `APT-Hunter`, `Chainsaw`, `Hayabusa` e `Sysmon` (93 slides, Fichas 16 e 17)<br/>• **Parte 2 (Logs Ad-Hoc)**: Memory dumps (`.dmp`), `WER` e caso **Storm-0558**, `ETL` / Delivery Optimization (`ExternalIPAddress`), OneDrive (`.odl`/SQLite/`OneDriveExplorer`) e privacidade em veículos (34 slides, Ficha 18) | Concluído (127 slides mapeados, 10 notas essenciais + 1 Cheat Sheet) |

### 📑 Folhas de Consulta Rápida (Cheat Sheets de Apoio)

* **[[Cheat Sheet - Registry e Forense]]**: Guia de bolso para Hives lógicos/físicos, UserAssist, ShellBags, USBSTOR, Timestamps e comandos CLI.
* **[[Cheat Sheet - Artefactos de Execução e Sistema no Windows]]**: Guia de bolso para VSS, Prefetch (MAM), ShimCache, AmCache (SHA-1/SQLite), Jump Lists (CFB), LNKs, Thumbnails, Timeline, SRUM (ESE) e Linha do Tempo de Ativação.
* **[[Cheat Sheet - Administração de Sistemas e Controlo de Acessos]]**: Guia de bolso do Capítulo 2 para sanitização (HDD/SSD/NVMe), segurança USB, Hardening/`YellowKey`, CVE/CVSS/CWE, NIST, Entropia, `TOTP`/`Passkeys`, `hashcat` e os 31 casos de estudo.
* **[[Cheat Sheet - YARA, MOTW e Extração de Strings]]**: Guia de bolso do Capítulo 3 para sintaxe YARA/`yr`, scanners LOKI/`Loki-RS`, ADS em CMD/PowerShell, `WastedLocker`, `Zone.Identifier`, exceções `7-Zip`/`certutil` e comparativo `strings`/`sfk`/`bstrings`.
* **[[Cheat Sheet - Logs no Windows e Threat Hunting]]**: Guia de bolso do Capítulo 4 para prazos de retenção, caminhos forenses, Event IDs críticos, comandos CLI/Threat Hunting (`wevtutil`, `psloglist`, `jq`, `Chainsaw`, `Hayabusa`, `Sysmon`, `tracerpt`) e armadilhas de exame.

### 🧪 Fichas Práticas e Questionários de Avaliação (Capítulo 1)

* **[[Ficha Prática e Questionário - Serviços e Windows Search]]**: Laboratório 1 — Serviços, Processos, CLI e Windows Search (`sidr`).
* **[[Ficha Prática e Questionário - Windows Registry e Artefactos Forenses]]**: Laboratório do Registry — Hives, WOW64, UserAssist (ROT13), ShellBags e USB.
* **[[Ficha Prática e Questionário - Execução e Compatibilidade (Prefetch, ShimCache e AmCache)]]**: Fichas 3, 4 e 5 — VSS, Prefetch (`PECmd`), ShimCache, AmCache e Regra de Ouro.
* **[[Ficha Prática e Questionário - Shell, Atividade e Matriz Forense]]**: Fichas 6 a 10 — LNKs (`LECmd`), Jump Lists, Thumbcache, SRUM, Notepad W11, uLEB128 e Reconstituição Temporal.

---

## 🔗 Recursos e Fontes Oficiais

* **Moodle da UC**: Materiais oficiais, guiões práticos, anúncios e apresentações disponibilizados pelo docente na plataforma institucional de e-learning do Politécnico de Leiria.
* **Apresentações de Apoio (Capítulo 1)**:
  * Parte 1: `01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf` (170 páginas / slides 1–171).
  * Parte 2: `Artefactos Windows OS` (158 slides).
* **Apresentações de Apoio (Capítulo 2)**:
  * Parte A: `System Administration — System and Data Management` (62 slides — Ficha 11 Validrive).
  * Parte B: `System Administration — Access Control` (119 slides — Ficha 10 keepassXC + entropy; Ficha 11 2FA, PassKey).
* **Apresentações de Apoio (Capítulo 3)**:
  * Bloco 01: `YARA & LOKI` (35 slides — Ficha de trabalho 14).
  * Bloco 02: `Microsoft's Mark Of The Web (MOTW) / Alternate Data Stream (ADS)` (25 slides — Ficha 15).
  * Bloco 03: `"strings" utilities` (16 slides).
* **Apresentações de Apoio (Capítulo 4)**:
  * Parte 1: `EI_ASSI_1S2026-27_cap04_v01_LOGs_parte01_v1---ULO.pdf` (93 slides — Fichas 16 e 17).
  * Parte 2: `EI_ASSI_1S2026-27_cap04_v01_LOGs_parte02_v1.pdf` (34 slides — Ficha 18).
* **Fichas Laboratoriais Mapeadas**: Fichas 1 a 10 integradas no Capítulo 1; Fichas 10 e 11 integradas no Capítulo 2; Fichas 14 e 15 referenciadas no Capítulo 3; Fichas 16, 17 e 18 integradas no Capítulo 4.

---

## 🧭 Navegação

* [[Home|Voltar ao Hub Central do MCIF]]

