---
title: Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses
tipo: indice
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
tags:
  - moc
  - assi
  - windows
  - forense
aliases:
  - Capítulo 1 ASSI
  - MOC Capítulo 1
atualizado: 2026-09-23
---

# Capítulo 1 — Sistemas Operativos, Serviços e Artefactos Forenses

Índice temático e encadeamento pedagógico do programa completo do Capítulo 1 (*Serviços & Artefactos Forenses no Windows*, 180 slides, Prof. Patrício Domingues). 

As notas encontram-se estruturadas por blocos temáticos numerados na pasta `ASSI/Capítulo 01 - Sistemas Operativos, Serviços e Artefactos/`.

---

## 1. Arranque do Windows e PKfail (01 - Arranque e UEFI)

| Nota | Descrição e Foco Técnico |
| :--- | :--- |
| [[UEFI Secure Boot]] | Validação modular do arranque por assinatura digital |
| [[UEFI Secure Boot - Chaves e Hierarquia]] | Hierarquia de validação: PK, KEK, `db`, `dbx` |
| [[PKfail - Vulnerabilidade do UEFI Secure Boot]] | Chave de teste AMI usada como Platform Key em ~850 modelos |
| [[PKfail - Cadeia de Ataque e Deteção Forense]] | Exploração de bootkits; deteção via `IsBootSecure` e `sigcheck` |

---

## 2. Linha de Comandos e Processos (02 - Processos e Linha de Comandos)

| Nota | Descrição e Foco Técnico |
| :--- | :--- |
| [[Processos e linha de comandos no Windows]] | Interação CLI, `tasklist` e filtros, Sysinternals (`pslist`, `psexec`), atalhos |
| [[Comando forfiles]] | Automação e iteração de ficheiros por data (`/D`) e máscara (`/M`) |

---

## 3. Serviços do Windows e Pesquisa (03 - Serviços do Windows)

| Nota | Descrição e Foco Técnico |
| :--- | :--- |
| [[Serviços Windows]] | Conceito de serviço, CLI (`sc`, `net`), gestão de dependências e Spooler |
| [[svchost.exe]] | Anfitrião partilhado de serviços DLL; auditoria via Registry e `tasklist /svc` |
| [[Serviço BITS]] | Transferências em background; vetor LOL; base ESE `qmgr.db` e `BitsParser` |
| [[Serviço Delivery Optimization]] | Protocolo P2P (BitTorrent) no Windows Update |
| [[Windows Search]] | Mecanismos de indexação: ESE (`Windows.edb`) vs SQLite3 (`Windows.db`); extração com `sidr` e `WinSearchDBAnalyzer`; Laboratório 1 |

---

## 4. Aplicações Modernas UWP (04 - Aplicações Modernas)

| Nota | Descrição e Foco Técnico |
| :--- | :--- |
| [[Aplicações UWP (Universal Windows Platform) - Visão Geral]] | Modelo Sandbox, WinRT, pacotes APPX, `tasklist /APPS`, permissões do `TrustedInstaller` |
| [[UWP - Artefactos Forenses e Estrutura de Dados]] | Pastas `Packages`, State Repository (`.srd` SQLite), `settings.dat` e `swapfile.sys` |

---

## 5. Fundamentos e Ferramentas do Registry (05 - Registry e Forense)

| Nota | Descrição e Foco Técnico |
| :--- | :--- |
| [[Estrutura e Hives do Windows Registry]] | Base hierárquica, Configuration Manager, 5 Hives lógicos, ficheiros no disco, hives voláteis e `hivelist` |
| [[Tipos de Dados e Associação de Ficheiros no Registry]] | Tipos de valores (`REG_SZ`, `REG_DWORD`, etc.), `HKCR`, comandos `assoc` e `ftype` |
| [[Ferramentas de Análise e Extração do Registry]] | CLI (`reg query`, `reg export`), GUI (`regedit`, `RegScanner`), `RegistryExplorer` (Zimmerman) e `RegRipper` |
| [[Arquitetura 32 vs 64 bits no Registry e Executáveis (WOW6432Node)]] | Redirecionamento WOW64, limitação de ferramentas 32-bit, identificação de PE via HxD, `exiftool` e `trid` |

---

## 6. Aplicações Modernas, Timestamps e Monitorização (05 - Registry e Forense)

| Nota | Descrição e Foco Técnico |
| :--- | :--- |
| [[Registry em Aplicações Modernas (MSIX e Helium)]] | Pacotes MSIX em contentores, Registry virtualizado em `Helium` (`User.dat`), caso de estudo do Bloco de Notas |
| [[Marcadores Temporais no Windows (Timestamps)]] | Formatos numéricos: UNIX Epoch, FILETIME64, struct `SYSTEMTIME` (128-bit); ferramentas `w32tm`, `DCODE`, `cyberchef` |
| [[Salvaguarda e Monitorização do Registry]] | `RegIdleBackup`/`RegBack` (desativação pós-1803), `schtasks`, análise dinâmica com `procmon` e auditoria com `sysmon` |

---

## 7. Artefactos Forenses de Utilizador e Navegação (05 - Registry e Forense)

| Nota | Descrição e Foco Técnico |
| :--- | :--- |
| [[Artefactos Forenses de Execução e Persistência no Registry]] | Chaves `Run`/`RunOnce`, Sysinternals `autoruns`, `LogonStats` (1.º login), Cache MUI (`UsrClass.dat`) e `RecentApps` |
| [[Artefactos Forenses de Interação do Utilizador (MRU e TypedPaths)]] | Listas MRU: `RunMRU` (`MRUList`), `RecentDocs` (`MRUListEx`), `ComDlg32`, caminhos digitados em `TypedPaths` |
| [[Artefacto Forense UserAssist]] | Telemetria de apps GUI no Explorer, subchaves GUID, cifra ROT13, estrutura binária `Count` (72 bytes) e falsos positivos |
| [[Artefacto Forense ShellBags]] | Histórico de layout e navegação em pastas (`BagMRU`/`Bags`), suporte a arquivos comprimidos (ZIP, e 7z/RAR no W11 22H2), `SBECmd` |

---

## 8. Caso de Estudo: Dispositivos USB (05 - Registry e Forense)

| Nota | Descrição e Foco Técnico |
| :--- | :--- |
| [[Artefactos Forenses de Dispositivos USB]] | Apreensão pericial, chave `USBSTOR`, distinção entre Serial Number Real vs. Windows Assigned Device ID, `setupapi.dev.log` e `WLEAPP` |

---

## Navegação

- [[00 ASSI|Voltar ao MOC Geral de ASSI]]
- [[Home|Voltar ao Hub Central do MCIF]]
