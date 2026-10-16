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
atualizado: 2026-10-07
---

# Capítulo 1 — Sistemas Operativos, Serviços e Artefactos Forenses

Índice temático e encadeamento pedagógico do programa completo do Capítulo 1 (*Sistemas Operativos, Serviços e Artefactos Forenses no Windows*, lecionado pelo Prof. Patrício Domingues). 

As notas encontram-se estruturadas por blocos temáticos numerados na pasta `ASSI/Capítulo 01 - Sistemas Operativos, Serviços e Artefactos/`, cobrindo os fundamentos de arranque, serviços, Registry e os artefactos do sistema e do utilizador.

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
| [[Ficha Prática e Questionário - Serviços e Windows Search]] | Guião prático (Laboratório 1) e questionário de avaliação sobre processos, serviços e WSearch |

---

## 4. Aplicações Modernas UWP (04 - Aplicações Modernas (UWP e MSIX))

| Nota | Descrição e Foco Técnico |
| :--- | :--- |
| [[Aplicações UWP (Universal Windows Platform) - Visão Geral]] | Modelo Sandbox, WinRT, pacotes APPX, `tasklist /APPS`, permissões do `TrustedInstaller` |
| [[UWP - Artefactos Forenses e Estrutura de Dados]] | Pastas `Packages`, State Repository (`.srd` SQLite), `settings.dat` e `swapfile.sys` |

---

> [!TIP] Folha de Consulta Rápida (Cheat Sheet)
> Para uma síntese rápida de todos os caminhos, ficheiros de hive, estruturas binárias (SYSTEMTIME, UserAssist), matriz de artefactos forenses e comandos CLI, consulta a **[[Cheat Sheet - Registry e Forense]]**.

## 5. Fundamentos e Ferramentas do Registry (05 - Fundamentos e Ferramentas do Registry)

| Nota | Descrição e Foco Técnico |
| :--- | :--- |
| [[Estrutura e Hives do Windows Registry]] | Base hierárquica, Configuration Manager, 5 Hives lógicos, ficheiros no disco, hives voláteis e `hivelist` |
| [[Tipos de Dados e Associação de Ficheiros no Registry]] | Tipos de valores (`REG_SZ`, `REG_DWORD`, etc.), `HKCR`, comandos `assoc` e `ftype` |
| [[Ferramentas de Análise e Extração do Registry]] | CLI (`reg query`, `reg export`), GUI (`regedit`, `RegScanner`), `RegistryExplorer` (Zimmerman) e `RegRipper` |
| [[Arquitetura 32 vs 64 bits no Registry e Executáveis (WOW6432Node)]] | Redirecionamento WOW64, limitação de ferramentas 32-bit, identificação de PE via HxD, `exiftool` e `trid` |
| [[Ficha Prática e Questionário - Windows Registry e Artefactos Forenses]] | Guião prático e questionário de avaliação para os blocos de Registry (05 a 08: Hives, WOW64, UserAssist, ShellBags e USB) |

---

## 6. Aplicações Modernas, Timestamps e Monitorização (06 - Aplicações Modernas, Timestamps e Monitorização)

| Nota | Descrição e Foco Técnico |
| :--- | :--- |
| [[Registry em Aplicações Modernas (MSIX e Helium)]] | Pacotes MSIX em contentores, Registry virtualizado em `Helium` (`User.dat`), caso de estudo do Bloco de Notas |
| [[Marcadores Temporais no Windows (Timestamps)]] | Formatos numéricos: UNIX Epoch, FILETIME64, struct `SYSTEMTIME` (128-bit); ferramentas `w32tm`, `DCODE`, `cyberchef` |
| [[Salvaguarda e Monitorização do Registry]] | `RegIdleBackup`/`RegBack` (desativação pós-1803), `schtasks`, análise dinâmica com `procmon` e auditoria com `sysmon` |

---

## 7. Artefactos Forenses de Utilizador e Navegação (07 - Artefactos Forenses de Utilizador e Navegação)

| Nota                                                                  | Descrição e Foco Técnico                                                                                                          |
| :-------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------- |
| [[Artefactos Forenses de Execução e Persistência no Registry]]        | Chaves `Run`/`RunOnce`, Sysinternals `autoruns`, `LogonStats` (1.º login), Cache MUI (`UsrClass.dat`) e `RecentApps`              |
| [[Artefactos Forenses de Interação do Utilizador (MRU e TypedPaths)]] | Listas MRU: `RunMRU` (`MRUList`), `RecentDocs` (`MRUListEx`), `ComDlg32`, caminhos digitados em `TypedPaths`                      |
| [[Artefacto Forense UserAssist]]                                      | Telemetria de apps GUI no Explorer, subchaves GUID, cifra ROT13, estrutura binária `Count` (72 bytes) e falsos positivos          |
| [[Artefacto Forense ShellBags]]                                       | Histórico de layout e navegação em pastas (`BagMRU`/`Bags`), suporte a arquivos comprimidos (ZIP, e 7z/RAR no W11 22H2), `SBECmd` |

---

## 8. Caso de Estudo: Dispositivos USB (08 - Artefactos Forenses de Dispositivos USB)

| Nota | Descrição e Foco Técnico |
| :--- | :--- |
| [[Artefactos Forenses de Dispositivos USB]] | Apreensão pericial, chave `USBSTOR`, distinção entre Serial Number Real vs. Windows Assigned Device ID, `setupapi.dev.log` e `WLEAPP` |

---

## 9. VSS e Linha do Tempo Live (09 - VSS e Linha do Tempo Live)

| Nota                                                           | Descrição e Foco Técnico                                                                                                             |
| :------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------- |
| [[LastActivityView e Reconstituição Temporal Live]]            | Triagem rápida de atividade *live*, agregação multi-fonte (Prefetch, Registry, Minidump), automação CLI (`/stab`)                    |
| [[Volume Shadow Service (VSS) - Arquitetura e Funcionamento]]  | Snapshots de ficheiros em estado *locked*, arquitetura (VSS Service `VSSVC.exe`, Writers, Requestor, Providers), quotas na GUI       |
| [[Gestão e Manipulação de VSS (CLI, PowerShell e Permissões)]] | Manipulação por `vssadmin`, automação em PowerShell WMI, vetor de ransomware (`wmic /nointeractive`), permissões com `icacls`        |
| [[Acesso Forense e Montagem de Shadow Copies]]                 | Montagem nativa com `mklink /d` (barra final `\`), ferramentas `VSCMount` (Eric Zimmerman) e `ShadowCopyView` (NirSoft); Ficha 3 VSS |

---

## 10. Execução e Otimização do Sistema (10 - Prefetch e SysMain)

| Nota | Descrição e Foco Técnico |
| :--- | :--- |
| [[Taxonomia dos Artefactos de Execução no Windows]] | Classificação em System, Registry e User artifacts (Singh & Singh), motivações de engenharia (UX e retrocompatibilidade) |
| [[Serviço Prefetch e SysMain - Arquitetura e Funcionamento]] | Redução de tempo de carregamento e boot, evolução SuperFetch/SysMain, limites (1024), escrita exclusiva por `svchost.exe (-s SysMain)`, armadilha de `EnablePrefetcher` |
| [[Estrutura Interna e Algoritmo de Hashing do Prefetch]] | Algoritmo de hash (314159/37), exceção para executáveis anfitriões CLI, compressão MAM vs SCCA, 8 marcas temporais de execução, ausência de vínculo a utilizador |
| [[Análise Forense e Criação a Pedido do Prefetch]] | Análise com `WinPrefetchView` e `PECmd` (Zimmerman), validação de integridade com `sigcheck`, criação programática via APIs `OperationStart`/`OperationEnd` (`Op-*.pf`); Ficha 04 |

---

## 11. Infraestrutura de Compatibilidade (11 - ShimCache e AmCache)

| Nota | Descrição e Foco Técnico |
| :--- | :--- |
| [[Application Compatibility e ShimCache (AppCompatCache)]] | Infraestrutura de shims, `PcaSvc` e `sysmain.sdb`, retenção na RAM e escrita no shutdown (`SYSTEM`), buffer circular (1024), remoção da InsertFlag no W10/W11 |
| [[AmCache - Arquitetura, Hives e Evolução para SQLite]] | Histórico (`RecentFileCache.bcf` W7 vs `Amcache.hve` REGF W8+), tarefas agendadas, hash SHA-1 e VirusTotal, evolução para SQLite3 no Windows 11 (>25H2) |
| [[Extração da AmCache e Comparação Forense com a ShimCache]] | Extração de ficheiros bloqueados, parsing com `AmcacheParser` (Zimmerman) e `RegRipper`, tabela comparativa, regra de ouro (prova de existência vs. execução); Ficha 05 |
| [[Mecanismos de Compatibilidade no Windows (WOW64, Shims, PCA, ShimCache e AmCache)]] | Síntese e visão integrada: pirâmide de compatibilidade (WOW64, Shims/sysmain.sdb, PcaSvc, ShimCache, AmCache), fluxo de execução e correlação forense |
| [[Ficha Prática e Questionário - Execução e Compatibilidade (Prefetch, ShimCache e AmCache)]] | Guião prático e questionário de avaliação sobre VSS, Prefetch, ShimCache e AmCache (Fichas 3, 4 e 5) |

---

## 12. Interação do Utilizador e Atalhos (12 - Jump Lists e Ficheiros LNK)

| Nota                                                          | Descrição e Foco Técnico                                                                                                                                                                 |
| :------------------------------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [[Jump Lists - Arquitetura, AppIDs e Carving]]                | Listas automáticas (CFB/OLE) vs customizadas, catálogo de AppIDs, persistência pós-desinstalação, trailer de carving `AB FB BF BA`, ferramentas `JLECmd` e `JumpList Explorer`; Ficha 06 |
| [[Ficheiros LNK (Shell Links) - Metadados e Formato Binário]] | Assinatura `4C 00 00 00`, metadados recuperáveis (MAC timestamps, volume serial, MAC address NIC), pasta `Recent` (limite 149), parsing com `LECmd` e `LnkParse3`                        |
| [[Abuso e Vetores de Ataque com Ficheiros LNK]]               | Engenharia social com ícones trocados, execução de LOLBins, campanhas Emotet e APT10, payload embutido (`findstr`), vulnerabilidade de truncagem visual (256 vs. 4096 carateres)         |

---

## 13. Caches de Shell e Visualização (13 - Caches Gráficas e Miniaturas)

| Nota | Descrição e Foco Técnico |
| :--- | :--- |
| [[Caches de Ícones e Miniaturas (IconCache e Thumbcache)]] | Evolução histórica (`ShellIconCache`, `IconCache.db` com magic `Win4`), pasta Explorer (`thumbcache_*.db`), ferramentas `thumbcache viewer` (GUI/CLI), mapeamento com Windows Search (`Windows.db`), ressalva probatória de visualização; Ficha 07 |

---

## 14. Monitorização de Atividade e Recursos (14 - Windows Activity Timeline e SRUM)

| Nota | Descrição e Foco Técnico |
| :--- | :--- |
| [[Windows Activity Timeline - Arquitetura e Base SQLite]] | SQLite `ActivitiesCache.db`, serviço UWP `CDPUserSvc`, campo `PlatformDeviceId` (Base64), chave `TaskFlow\DeviceCache`, utilidade reduzida no W11, parsing com `WxTCmd`; Ficha 08 |
| [[Recuperação de Clipboard e Sincronização na Timeline]] | Extração de área de transferência da coluna `ClipboardPayload`, requisitos (Win+V e Cloud Sync), payload JSON Base64 (12h de retenção), ferramenta `Clippy` (DB e WAL) |
| [[System Resource Usage Monitor (SRUM) - Arquitetura e Base ESE]] | Base ESE `SRUDB.dat`, serviço DPS (`nduprov.dll`, etc.), armazenamento diferido (Registry e descarga ao minuto 30), tabelas GUID de CPU/rede/energia, mapeamento `SruDbIdMapTable`, reparação com `esentutl`; Ficha 09 |
| [[Análise Forense do SRUM e Ferramentas Nativas (powercfg)]] | Limitações do Task Manager, utilitário nativo `powercfg` (`/energy`, `/srumutil` para CSV, `/batteryReport`), NirSoft `ESE Database Viewer` (UTF-16), exportação profissional com `SrumECmd` (Zimmerman) e deteção de exfiltração |

---

> [!TIP] Folha de Consulta Rápida — Parte 2 (Execução e Sistema)
> Para uma síntese rápida de todos os caminhos de artefactos, motores (ESE, SQLite, CFB), assinaturas binárias (MAM, SCCA, 4C 00 00 00, NP, uLEB128), matriz cronológica de ativação e comandos CLI, consulta a **[[Cheat Sheet - Artefactos de Execução e Sistema no Windows]]**.

## 15. Aplicações Modernas e Matriz Forense (15 - Aplicações Modernas e Matriz Forense)

| Nota | Descrição e Foco Técnico |
| :--- | :--- |
| [[Artefacto Forense do Bloco de Notas (Notepad Windows 11)]] | Aplicação UWP/MSIX, pasta `LocalState\TabState`, persistência de texto não gravado (*unsaved text*), estrutura binária `NP` em UTF-16LE, parsers `notepad_parser` e `Notepad-State-Library`; Ficha 10 |
| [[Codificação uLEB128 em Estruturas de Dados do Windows]] | Algoritmo *Unsigned Little Endian Base 128*, regra dos 7 bits e MSB continuation bit, passo a passo de codificação do valor decimal 301 (`AD 02`), implementação de leitura pericial |
| [[Matriz de Correlação Forense e Cronologia de Ativação dos Artefactos]] | Linha do tempo de ativação ($T_0 \to$ UserAssist $\approx 3\text{s} \to$ Prefetch $\approx 10\text{s} \to$ SRUM $\approx 1\text{h} \to$ Amcache $\to$ Shimcache no shutdown), tabela consolidada W10/W11 e pastas críticas de sistema |
| [[Ficha Prática e Questionário - Shell, Atividade e Matriz Forense]] | Desafio forense integrado e questionário de avaliação sobre Jump Lists, LNKs, Caches, SRUM, Notepad W11 e Matriz de Ativação (Fichas 6 a 10) |

---

## 16. Fichas Práticas e Questionários de Avaliação

Guiões laboratoriais integrados com exercícios práticos e questionários de exame resolvidos e comentados:

| Ficha / Questionário | Blocos Abrangidos | Tópicos Centrais e Ferramentas Forenses |
| :--- | :---: | :--- |
| [[Ficha Prática e Questionário - Serviços e Windows Search]] | 02 e 03 | Auditoria com `sc`/`net`, processos em `svchost.exe`, comandos `forfiles`, extração do Windows Search (`Windows.edb`/`Windows.db`) com `sidr`; Laboratório 1 |
| [[Ficha Prática e Questionário - Windows Registry e Artefactos Forenses]] | 05 a 08 | Extração de Hives, nós `WOW6432Node`, timestamps FILETIME/UNIX, `UserAssist` (ROT13 + struct Count), `ShellBags` (`SBECmd`), `USBSTOR` e identificação de números de série USB |
| [[Ficha Prática e Questionário - Execução e Compatibilidade (Prefetch, ShimCache e AmCache)]] | 09 a 11 | Descompressão MAM com `PECmd`, parsing com `AppCompatCacheParser` e `AmcacheParser`, resolução de *file in use* com VSS (`mklink`), VirusTotal e Regra de Ouro (Existência vs Execução); Fichas 3, 4 e 5 |
| [[Ficha Prática e Questionário - Shell, Atividade e Matriz Forense]] | 12 a 15 | Atalhos maliciosos LNK com `LECmd` (discrepância 256 vs 4096 carateres), Jump Lists (`JLECmd` e trailer `AB FB BF BA`), `Thumbcache Viewer`, quantificação de exfiltração no SRUM (`SrumECmd`), Notepad W11 `TabState`, decodificação manual de `uLEB128` e desafio pericial de reconstituição temporal; Fichas 6 a 10 |

---

## Navegação

- [[00 ASSI|Voltar ao MOC Geral de ASSI]]
- [[Home|Voltar ao Hub Central do MCIF]]







