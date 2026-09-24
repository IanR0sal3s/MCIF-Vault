---
title: Estrutura e Hives do Windows Registry
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
tipo: conceito
tags:
  - windows
  - registry
  - forense
  - arquitetura
aliases:
  - Windows Registry
  - Hives do Registry
  - Registry Architecture
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
atualizado: 2026-09-23
---

# Estrutura e Hives do Windows Registry

Base de dados hierárquica introduzida no Windows 95 para substituir ficheiros legados de inicialização e configuração (`config.sys`, `autoexec.bat` e ficheiros `.ini`). Centraliza informações sobre hardware, sistema operativo, programas instalados, contas de utilizador, serviços e histórico de atividade.

A nível do núcleo do sistema operativo, a gestão de leitura, escrita e controlo de acesso às chaves do Registry está a cargo do **Configuration Manager**.

## Estrutura Lógica

O Registry organiza-se de forma semelhante a um sistema de ficheiros:
* **Hives (Colmeias)**: Ramos de topo da hierarquia lógica.
* **Keys (Chaves) e Subkeys (Subchaves)**: Contentores organizacionais análogos a pastas.
* **Values (Valores)**: Pares nome/dado associados a uma chave. Cada valor é composto por três elementos: **Nome**, **Tipo de Dados** e **Dado/Conteúdo**.

### Os Cinco Hives Principais (`HKEY_`)

| Hive Lógico | Sigla | Conteúdo e Função |
| :--- | :--- | :--- |
| `HKEY_CLASSES_ROOT` | **HKCR** | Informações sobre tipos e associações de ficheiros, atalhos e registo de objetos COM. Determina a resposta do SO a ações do utilizador. |
| `HKEY_CURRENT_USER` | **HKCU** | Configurações do utilizador com sessão atualmente iniciada (ambiente de trabalho, diretórios pessoais, preferências). Vista virtual/dinâmica. |
| `HKEY_LOCAL_MACHINE` | **HKLM** | Configurações globais do computador e do SO aplicáveis a todos os utilizadores (software instalado, hardware detetado, drivers e discos). |
| `HKEY_USERS` | **HKU** | Perfis de configuração de todos os utilizadores ativos e carregados na máquina, identificados pelo respetivo **SID** (*Security Identifier*). |
| `HKEY_CURRENT_CONFIG` | **HKCC** | Informações sobre o perfil de hardware corrente. É um *alias* dinâmico para `HKLM\SYSTEM\CurrentControlSet\Hardware Profiles\Current\`. |

## Mapeamento Físico no Disco

Contrariamente à vista unificada apresentada pelas ferramentas gráficas, o Registry é fragmentado em múltiplos ficheiros físicos no sistema de ficheiros:

### Hives do Sistema (`%SystemRoot%\System32\config\`)
* `HKLM\SYSTEM` $\rightarrow$ `\system32\config\system`
* `HKLM\SAM` $\rightarrow$ `\system32\config\sam` (Security Accounts Manager)
* `HKLM\SECURITY` $\rightarrow$ `\system32\config\security` (políticas de segurança locais e LSA)
* `HKLM\SOFTWARE` $\rightarrow$ `\system32\config\software` (aplicações e definições de SO)
* `HKU\.DEFAULT` $\rightarrow$ `\system32\config\default` (perfil padrão do sistema / LocalSystem)

### Hives de Utilizador
Cada utilizador possui dois hives próprios que guardam as suas definições e artefactos:
* `C:\Users\<username>\NTUSER.DAT`: carregado dinamicamente em `HKCU` (ou `HKU\{SID}`) aquando do logon.
* `C:\Users\<username>\AppData\Local\Microsoft\Windows\USRCLASS.DAT`: mapeado em `HKU\{SID}_Classes`, contém associações por utilizador e artefactos como [[Artefacto Forense ShellBags|ShellBags]] e [[Artefactos Forenses de Execução e Persistência no Registry|MuiCache]].

### Hives Voláteis
Certos hives não têm representação em ficheiro no disco, sendo criados e mantidos exclusivamente na memória RAM pelo kernel durante o arranque:
* `HKLM\HARDWARE`: povoado dinamicamente pelo detetor de hardware do SO.
* `HKLM\SYSTEM\Clone`: mantido em memória durante processos de inicialização.

## Chave `hivelist`

Para auditar e confirmar em que ficheiros físicos cada hive está montado num sistema ativo, o Windows mantém a lista completa na chave:

```text
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\hivelist
```

A consulta desta chave (via `reg query` ou ferramenta pericial) revela o mapeamento dos dispositivos de bloco NT (`\Device\HarddiskVolume...`) para cada ficheiro de configuração.

## Implicações Forenses

1. **Vetor de Persistência e Ocultação**: Software malicioso manipula frequentemente chaves do Registry para garantir execução persistente no arranque ou adulterar configurações de defesa.
2. **Análise Offline vs. Live**: `HKCU` e `HKCC` são pontes virtuais. Numa análise pericial *post-mortem* (disco desligado ou imagem forense), o perito não extrai um ficheiro "HKCU", mas sim recolhe os ficheiros brutos `SYSTEM`, `SOFTWARE`, `NTUSER.DAT` e `USRCLASS.DAT` para montagem em analisadores forenses.
3. **Bloqueio de Ficheiros**: Em sistemas em execução, os ficheiros de hive estão bloqueados com acesso exclusivo pelo kernel. Cópias diretas requerem privilégios elevados, uso do serviço VSS (*Volume Shadow Copy*) ou ferramentas periciais adequadas.

## Notas relacionadas

- [[Tipos de Dados e Associação de Ficheiros no Registry]]
- [[Ferramentas de Análise e Extração do Registry]]
- [[Arquitetura 32 vs 64 bits no Registry e Executáveis (WOW6432Node)]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
