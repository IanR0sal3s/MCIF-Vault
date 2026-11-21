---
title: Estrutura e Hives do Windows Registry
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 5
tipo: conceito
tags:
  - assi
  - windows
  - registry
  - forense
  - arquitetura
aliases:
  - Windows Registry
  - Hives do Registry
  - Registry Architecture
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v4.pdf
atualizado: 2026-11-21
---

# Estrutura e Hives do Windows Registry

Base de dados hierárquica introduzida no Windows 95 (substituindo `config.sys`, `autoexec.bat` e ficheiros `.ini`) que centraliza configurações de hardware, sistema operativo, aplicações e atividade de utilizadores. Ao nível do *kernel*, a sua gestão e controlo de acesso estão a cargo do **Configuration Manager**.

## 1. Anatomia Lógica: Hives, Chaves e Valores

O Registry funciona como uma árvore semelhante a um sistema de ficheiros:
* **Hives (Colmeias)**: raízes de topo (`HKEY_*`);
* **Chaves (*Keys*) e Subchaves**: contentores análogos a pastas (cada chave regista um *LastWriteTime*);
* **Valores (*Values*)**: pares armazenados dentro de uma chave, cada um com **três elementos**: **Nome**, **Tipo de Dados** e **Dado**.

---

## 2. Vistas Virtuais vs. Ficheiros Físicos vs. Hives Voláteis

Embora o `regedit` mostre uma árvore unificada com 5 ramos (`HKEY_*`), fisicamente o Registry está distribuído por vários ficheiros no disco — e alguns ramos são apenas atalhos em memória:

```mermaid
flowchart TB
    classDef virtual fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;
    classDef base fill:#ede7f6,stroke:#512da8,stroke-width:2px;
    classDef sysdisco fill:#f1f8e9,stroke:#388e3c,stroke-width:2px;
    classDef userdisco fill:#fffde7,stroke:#fbc02d,stroke-width:2px;

    subgraph Nivel1["1. Vistas Virtuais e Atalhos Dinâmicos (Criados em RAM)"]
        direction LR
        HKCC["<b>HKCC</b><br/><i>HKEY_CURRENT_CONFIG</i>"]
        HKCR["<b>HKCR</b><br/><i>HKEY_CLASSES_ROOT</i><br/>(Associações e Extensões)"]
        HKCU["<b>HKCU</b><br/><i>HKEY_CURRENT_USER</i>"]
    end

    subgraph Nivel2["2. Hives Lógicos Base (Estruturas Permanentes)"]
        direction LR
        HKLM["<b>HKLM</b><br/><i>HKEY_LOCAL_MACHINE</i><br/>(Global do Sistema)"]
        HKU["<b>HKU</b><br/><i>HKEY_USERS</i><br/>(Perfis por SID)"]
    end

    subgraph Nivel3["3. Ficheiros Físicos no Disco"]
        subgraph FichSistema["%SystemRoot%\System32\config\ (Ficheiros Globais da Máquina)"]
            direction TB
            F_SYS["SYSTEM"]
            F_SAM["SAM"]
            F_SEC["SECURITY"]
            F_SOFT["SOFTWARE"]
            F_DEF["DEFAULT (Perfil padrão)"]
        end

        subgraph FichUser["C:\Users\&lt;User&gt;\ (Ficheiros do Utilizador)"]
            direction TB
            F_NTU["NTUSER.DAT<br/>(Raiz do perfil)"]
            F_USRC["USRCLASS.DAT<br/>(AppData\Local\...\Windows\)"]
        end
    end

    %% Relações dos Atalhos / Vistas Virtuais
    HKCC -->|"Alias dinâmico para HKLM\SYSTEM\...\Hardware Profiles"| HKLM
    HKCU -->|"Ponteiro dinâmico para HKU\&lt;SID_Sessão_Ativa&gt;"| HKU

    %% A Fusão Virtual de HKCR
    HKCR -.->|"1. Definições Base da Máquina (HKLM\SOFTWARE\Classes)"| HKLM
    HKCR -.->|"2. Sobreposição com Prioridade (HKCU\Software\Classes)"| HKCU

    %% Mapeamento Físico de HKLM
    HKLM -->|"Kernel, drivers e serviços"| F_SYS
    HKLM -->|"Contas e hashes locais"| F_SAM
    HKLM -->|"Políticas de segurança e LSA"| F_SEC
    HKLM -->|"Aplicações instaladas e definições do SO"| F_SOFT

    %% Mapeamento Físico de HKU
    HKU -->|"HKU\.DEFAULT"| F_DEF
    HKU -->|"HKU\&lt;SID&gt; (Definições pessoais)"| F_NTU
    HKU -->|"HKU\&lt;SID&gt;_Classes (ShellBags e associações)"| F_USRC

    %% Aplicação de Cores
    class HKCC,HKCU,HKCR virtual;
    class HKLM,HKU base;
    class F_SYS,F_SAM,F_SEC,F_SOFT,F_DEF sysdisco;
    class F_NTU,F_USRC userdisco;
```

| Hive Lógico (`regedit`) | Natureza / Ficheiro Físico no Disco | O que guarda (visão prática) |
| :--- | :--- | :--- |
| **`HKLM\SYSTEM`** | `%SystemRoot%\System32\config\system` | Serviços, drivers, `ControlSet`, rede e dispositivos USB (`USBSTOR`). |
| **`HKLM\SOFTWARE`** | `%SystemRoot%\System32\config\software` | Software instalado e chaves globais de arranque/sistema. |
| **`HKLM\SAM`** | `%SystemRoot%\System32\config\sam` | Contas locais de utilizador, grupos e hashes de passwords. |
| **`HKLM\SECURITY`** | `%SystemRoot%\System32\config\security` | Políticas de segurança locais, auditoria e segredos LSA. |
| **`HKU\.DEFAULT`** | `%SystemRoot%\System32\config\default` | Perfil padrão do sistema (`LocalSystem`). |
| **`HKU\{SID}`** | `C:\Users\<user>\NTUSER.DAT` | Configurações e atividade do utilizador (`UserAssist`, `RunMRU`, `RecentDocs`, `ComDlg32`, `TypedPaths`). |
| **`HKU\{SID}_Classes`** | `C:\Users\<user>\AppData\Local\Microsoft\Windows\USRCLASS.DAT` | Associações por utilizador, [[Artefacto Forense ShellBags\|ShellBags]] e `MuiCache`. |
| **`HKCU`** (*Current User*) | **Vista virtual** (aponta para `HKU\{SID}` do utilizador ativo) | Não existe como ficheiro físico numa análise *offline* (usa-se `NTUSER.DAT`). |
| **`HKCC`** (*Current Config*) | **Vista virtual** (alias para `HKLM\SYSTEM\CurrentControlSet\Hardware Profiles\Current`) | Perfil de hardware ativo. |
| **`HKCR`** (*Classes Root*) | **Vista virtual** (funde `HKLM\SOFTWARE\Classes` + `HKCU\Software\Classes`) | Extensões e associações de ficheiros (com prioridade para `HKCU`). |
| **`HKLM\HARDWARE`** e **`HKLM\SYSTEM\Clone`** | **Hives voláteis** (apenas em RAM) | Recriados a cada arranque — perdem-se ao desligar a máquina. |

---

## 3. Chave `hivelist` e Implicações Forenses

Para confirmar exatamente que ficheiros físicos correspondem aos hives montados num sistema ativo, consulta-se a chave **`hivelist`**:

```cmd
reg query HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\hivelist
```
*(Repara que `\REGISTRY\MACHINE\HARDWARE` surge com valor vazio, confirmando que existe apenas em memória RAM.)*

> [!IMPORTANT] Análise *Live* vs. *Offline*
> * **Em sistema ativo (*live*)**: o Configuration Manager mantém os hives bloqueados em acesso exclusivo — `copy` ou `xcopy` falham; a extração exige **VSS** (*Volume Shadow Copy*) ou ferramentas forenses com acesso de baixo nível (`RegistryExplorer`, `FTK Imager`).
> * **Em análise *post-mortem* (*offline*)**: não existe um ficheiro "HKCU"; o perito recolhe os ficheiros físicos (`SYSTEM`, `SOFTWARE`, `SAM`, `SECURITY`, `NTUSER.DAT`, `USRCLASS.DAT`) juntamente com os logs de transação (`.LOG1` / `.LOG2`).

---

## Perguntas de revisão

1. **Porque é que não existe um ficheiro `HKCU` numa imagem forense *offline* e que dois ficheiros de utilizador deve o perito recolher?**

> [!success]- Ver Resposta
> Porque `HKCU` é uma vista virtual dinâmica que aponta para `HKU\{SID}` apenas quando o utilizador tem sessão iniciada. Em disco, os dados residem em `C:\Users\<user>\NTUSER.DAT` (atividade geral: `UserAssist`, `RunMRU`, `RecentDocs`) e `C:\Users\<user>\AppData\Local\Microsoft\Windows\USRCLASS.DAT` (`ShellBags`, `MuiCache`, associações).

2. **Que hives são puramente voláteis (existem apenas em RAM) e que chave do Registry lista o mapeamento de todos os hives montados?**

> [!success]- Ver Resposta
> Os hives voláteis são `HKLM\HARDWARE` e `HKLM\SYSTEM\Clone` (perdem-se ao desligar). O mapeamento completo reside em `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\hivelist`.

3. **Que componente do kernel gere o Registry e porque falha um `copy` normal sobre `SYSTEM` ou `NTUSER.DAT` num Windows em execução?**

> [!success]- Ver Resposta
> O **Configuration Manager**, que mantém os ficheiros físicos de hive bloqueados em acesso exclusivo durante a execução do SO (exigindo VSS ou ferramentas forenses de baixo nível para aquisição *live*).

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[UWP - Artefactos Forenses e Estrutura de Dados]] | `Bloco 04` |
| **Seguinte** | [[Tipos de Dados e Associação de Ficheiros no Registry]] | `mesmo bloco` |
| **Índice** | [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]] · [[00 ASSI]] | `Bloco 05` |

### Conceitos Relacionados

* [[Ferramentas de Análise e Extração do Registry]] · `mesmo bloco`
* [[Arquitetura 32 vs 64 bits no Registry e Executáveis (WOW6432Node)]] · `mesmo bloco`
* [[Cheat Sheet - Registry e Forense]] · `mesmo bloco`
* [[Ferramentas de Triagem Forense no Windows Registry (RegistryReport, ForensicUserInfo e WRR)]] · `AFD1 · Cap. 2`
* [[Dispositivos de Arranque Forense - Disquetes DOS, Live CDs Linux, WinFE e USB]] · `AFD1 · Cap. 2`
* [[Investigação Forense Digital - Análise Live vs Post-Mortem]] · `AFD1 · Cap. 1`
* [[Diretrizes de Manuseamento - Identificação, Preservação, Isolamento e Correlação]] · `AFD1 · Cap. 1`
* [[Camadas de Organização de Dados e Análise de Sistemas de Ficheiros]] · `AFD1 · Cap. 3`
