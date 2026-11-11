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
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
atualizado: 2026-09-23
---

# Estrutura e Hives do Windows Registry

Base de dados hierárquica introduzida no Windows 95 para substituir ficheiros legados de configuração (`config.sys`, `autoexec.bat`, `.ini`), centralizando definições de sistema, utilizadores e serviços.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: O sistema operativo necessita de um repositório centralizado, transacional e gerido em memória pelo **Configuration Manager** (ao nível do *kernel*) para armazenar configurações de arranque, controladores de dispositivos, políticas de segurança e preferências de utilizador sem depender de ficheiros de texto dispersos.
> * **Porque importa (Forense)**: Concentra evidências de configuração global da máquina (`SYSTEM`, `SOFTWARE`, `SAM`, `SECURITY` em `%SystemRoot%\System32\config\`) e artefactos de atividade individual de cada utilizador (`NTUSER.DAT` e `USRCLASS.DAT`).
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Hives Lógicos vs. Ficheiros Físicos**: `HKCU` e `HKCC` são pontes virtuais/dinâmicas; numa perícia *offline* (*post-mortem*), não existe um ficheiro `HKCU` no disco — o perito recolhe `NTUSER.DAT` e `USRCLASS.DAT` do perfil do utilizador.
>   * **Hives Voláteis**: `HKLM\HARDWARE` e `HKLM\SYSTEM\Clone` existem apenas em memória RAM durante a execução do sistema, perdendo-se se a máquina for desligada sem aquisição volátil prévia.

---

## Mapa Rápido: "O que procuro?" $\rightarrow$ "Em que Hive Físico reside?"

| Pergunta do Investigador / O que procuro? | Hive Lógico (`regedit`) | Ficheiro Físico em Disco (Análise *Offline*) | Âmbito |
| :--- | :--- | :--- | :--- |
| Que serviços, drivers, interfaces de rede ou dispositivos USB foram ligados? | `HKLM\SYSTEM` | `%SystemRoot%\System32\config\system` | Máquina (Global) |
| Que software está instalado e quais as tarefas/chaves globais de arranque? | `HKLM\SOFTWARE` | `%SystemRoot%\System32\config\software` | Máquina (Global) |
| Que contas locais existem, respetivos RIDs/SIDs e hashes de palavras-passe? | `HKLM\SAM` | `%SystemRoot%\System32\config\sam` | Máquina (Global) |
| Quais as políticas de segurança locais, auditoria e segredos LSA? | `HKLM\SECURITY` | `%SystemRoot%\System32\config\security` | Máquina (Global) |
| Que programas o utilizador executou (`UserAssist`, `RunMRU`) ou ficheiros abriu (`RecentDocs`, `ComDlg32`)? | `HKCU` (ou `HKU\{SID}`) | `C:\Users\<username>\NTUSER.DAT` | Utilizador |
| Que pastas o utilizador navegou (`ShellBags`) ou que apps GUI invocou (`MuiCache`)? | `HKCU\Software\Classes` (`HKU\{SID}_Classes`) | `C:\Users\<username>\AppData\Local\Microsoft\Windows\USRCLASS.DAT` | Utilizador |
| Qual a configuração do perfil `LocalSystem` antes do início de sessão? | `HKU\.DEFAULT` | `%SystemRoot%\System32\config\default` | Sistema |
| Que hardware foi detetado no arranque atual? | `HKLM\HARDWARE` | *Nenhum (exclusivo em memória RAM — volátil)* | Volátil |

---

## Estrutura Lógica e Gestão pelo Kernel

A nível do núcleo do sistema operativo, a gestão de leitura, escrita, cache e controlo de acesso às chaves do Registry está a cargo do **Configuration Manager**. O Registry organiza-se de forma semelhante a um sistema de ficheiros:

* **Hives (Colmeias)**: Ramos de topo da hierarquia lógica (identificados pelo prefixo `HKEY_`).
* **Keys (Chaves) e Subkeys (Subchaves)**: Contentores organizacionais análogos a pastas ou diretórios, que podem conter outras subchaves ou valores (e possuem um carimbo temporal próprio de última escrita, *LastWriteTime*).
* **Values (Valores)**: Pares nome/dado associados a uma chave (análogos a ficheiros). Cada valor é obrigatoriamente composto por três elementos: **Nome**, **Tipo de Dados** e **Dado/Conteúdo**.

### Os Cinco Hives Principais (`HKEY_`)

| Hive Lógico           |  Sigla   | Conteúdo, Função e Mapeamento                                                                                                                                                                                        |
| :-------------------- | :------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `HKEY_CLASSES_ROOT`   | **HKCR** | Informações sobre tipos e associações de ficheiros, atalhos e registo de objetos COM. Determina a resposta do SO a ações do utilizador. É uma vista fundida entre `HKLM\SOFTWARE\Classes` e `HKCU\Software\Classes`. |
| `HKEY_CURRENT_USER`   | **HKCU** | Configurações do utilizador com sessão atualmente iniciada (ambiente de trabalho, diretórios pessoais, preferências). Vista virtual/dinâmica que aponta para `HKU\{SID}`.                                            |
| `HKEY_LOCAL_MACHINE`  | **HKLM** | Configurações globais do computador e do SO aplicáveis a todos os utilizadores (software instalado, hardware detetado, drivers e discos).                                                                            |
| `HKEY_USERS`          | **HKU**  | Perfis de configuração de todos os utilizadores ativos e carregados na máquina, identificados pelo respetivo **SID** (*Security Identifier*).                                                                        |
| `HKEY_CURRENT_CONFIG` | **HKCC** | Informações sobre o perfil de hardware corrente. É um *alias* dinâmico para `HKLM\SYSTEM\CurrentControlSet\Hardware Profiles\Current\`.                                                                              |

---

## Mapeamento Físico no Disco vs. Hives Voláteis

Contrariamente à vista unificada apresentada pelas ferramentas gráficas como o `regedit.exe`, o Registry está fragmentado em múltiplos ficheiros físicos no sistema de ficheiros:

### 1. Hives do Sistema (`%SystemRoot%\System32\config\`)

* `HKLM\SYSTEM` $\rightarrow$ `\system32\config\system` (controladores, serviços, `ControlSet`, dispositivos USB)
* `HKLM\SAM` $\rightarrow$ `\system32\config\sam` (*Security Accounts Manager* — utilizadores e grupos locais)
* `HKLM\SECURITY` $\rightarrow$ `\system32\config\security` (políticas de segurança locais e *Local Security Authority* — LSA)
* `HKLM\SOFTWARE` $\rightarrow$ `\system32\config\software` (aplicações instaladas e definições globais do SO)
* `HKU\.DEFAULT` $\rightarrow$ `\system32\config\default` (perfil padrão do sistema / conta `LocalSystem`)

### 2. Hives de Utilizador
Cada utilizador possui dois hives próprios que guardam as suas definições e artefactos periciais:

* `C:\Users\<username>\NTUSER.DAT`: carregado dinamicamente em `HKCU` (ou `HKU\{SID}`) aquando do logon interativo.
* `C:\Users\<username>\AppData\Local\Microsoft\Windows\USRCLASS.DAT`: mapeado em `HKU\{SID}_Classes` (e refletido em `HKCU\Software\Classes`), contém associações por utilizador e artefactos críticos como [[Artefacto Forense ShellBags|ShellBags]] e [[Artefactos Forenses de Execução e Persistência no Registry|MuiCache]].

### 3. Hives Voláteis (Apenas em RAM)
Certos hives não têm qualquer representação em ficheiro no disco, sendo criados e mantidos exclusivamente na memória RAM pelo *kernel* durante o arranque:

* `HKLM\HARDWARE`: povoado dinamicamente pelo detetor de hardware do SO a cada inicialização.
* `HKLM\SYSTEM\Clone`: mantido temporariamente em memória durante processos de inicialização.

---

## Auditoria de Montagem: Chave `hivelist`

Para auditar e confirmar em que ficheiros físicos cada hive lógico está montado num sistema ativo, o Windows mantém a lista de correspondência na chave:

```text
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\hivelist
```

### Anatomia do Comando de Consulta

```cmd
reg query HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\hivelist
```

* **`reg query`**: subcomando nativo do utilitário `reg.exe` para listar os valores contidos numa chave do Registry.
* **`...\Control\hivelist`**: caminho da chave que mapeia cada ramo carregado em memória para o caminho de dispositivo de bloco NT correspondente (ex.: `\Device\HarddiskVolume3\Windows\System32\config\SYSTEM` ou `\Device\HarddiskVolume3\Users\<user>\NTUSER.DAT`). Notar que `\REGISTRY\MACHINE\HARDWARE` surge associado a um valor vazio, confirmando a sua natureza puramente volátil.

---

## Implicações Forenses

1. **Vetor de Persistência e Ocultação**: Software malicioso manipula frequentemente chaves do Registry para garantir execução persistente no arranque (`Run`, `RunOnce`, serviços) ou adulterar configurações de defesa.
2. **Análise Offline vs. Live**: `HKCU` e `HKCC` são pontes virtuais. Numa análise pericial *post-mortem* (disco desligado ou imagem forense), o perito não extrai um ficheiro "HKCU", mas sim recolhe os ficheiros brutos `SYSTEM`, `SOFTWARE`, `SAM`, `SECURITY`, `NTUSER.DAT` e `USRCLASS.DAT` (juntamente com os respetivos ficheiros de transação `.LOG1` e `.LOG2`) para montagem em analisadores forenses.
3. **Bloqueio de Ficheiros em Sistema Vivo**: Em sistemas em execução, os ficheiros de hive estão abertos e bloqueados com acesso exclusivo pelo *kernel* (Configuration Manager). Cópias diretas com comandos comuns (`copy` / `xcopy`) falham; a aquisição *live* requer privilégios elevados, uso do serviço VSS (*Volume Shadow Copy*) ou ferramentas periciais adequadas (como o `RegistryExplorer` ou o `FTK Imager`).

---

## Perguntas de revisão

	1. **Qual o componente do kernel do Windows responsável pela gestão do Registry e porque é que os ficheiros de hive não podem ser copiados diretamente com o comando `copy` num sistema ativo?**

> [!success]- Ver Resposta
> O componente do *kernel* responsável é o **Configuration Manager**. Num sistema em execução, o Configuration Manager mantém os ficheiros físicos de hive (`SYSTEM`, `SOFTWARE`, `NTUSER.DAT`, etc.) abertos com bloqueio exclusivo de leitura/escrita. Para os extrair em análise *live*, é necessário recorrer ao serviço *Volume Shadow Copy* (VSS) ou a ferramentas forenses com acesso de baixo nível ao volume.

2. **Durante uma análise *post-mortem* a uma imagem de disco, um analista júnior procura o ficheiro correspondente ao hive `HKEY_CURRENT_USER` (`HKCU`) na pasta `\Windows\System32\config\`. Qual o erro conceptual desta abordagem e onde residem realmente os dados?**

> [!success]- Ver Resposta
> `HKCU` não é um ficheiro físico, mas sim uma vista virtual/dinâmica criada apenas quando um utilizador inicia sessão, apontando para `HKU\{SID}`. Além disso, os hives de utilizador não residem em `\System32\config\` (que guarda apenas hives de sistema), mas sim no diretório do perfil de cada utilizador: `C:\Users\<username>\NTUSER.DAT` e `C:\Users\<username>\AppData\Local\Microsoft\Windows\USRCLASS.DAT`.

3. **Qual a diferença forense entre os ficheiros `NTUSER.DAT` e `USRCLASS.DAT` de um mesmo utilizador?**

> [!success]- Ver Resposta
> Ambos pertencem ao perfil do utilizador, mas armazenam ramos distintos: o `NTUSER.DAT` (`C:\Users\<username>\`) guarda as configurações gerais de `HKCU` e artefactos como `UserAssist`, `RunMRU`, `RecentDocs`, `ComDlg32` e `TypedPaths`; já o `USRCLASS.DAT` (`...\AppData\Local\Microsoft\Windows\`) mapeia `HKU\{SID}_Classes` e armazena associações de classes por utilizador, bem como artefactos cruciais como **ShellBags** e **MuiCache**.

4. **O que distingue o hive `HKLM\HARDWARE` dos restantes hives de sistema e que consequência tem no desligamento abrupto de uma máquina?**

> [!success]- Ver Resposta
> `HKLM\HARDWARE` (tal como `HKLM\SYSTEM\Clone`) é um **hive volátil**, criado dinamicamente na memória RAM durante o arranque do sistema operativo sem ficheiro físico correspondente no disco. Se a máquina for desligada sem recolha prévia da memória ou exportação live, o seu conteúdo perde-se definitivamente.

5. **Em que chave do Registry é possível auditar a lista exata de todos os hives atualmente montados em memória e a sua correspondência com os caminhos físicos no disco?**

> [!success]- Ver Resposta
> Na chave `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\hivelist`.

## Notas relacionadas

- [[Tipos de Dados e Associação de Ficheiros no Registry]]
- [[Ferramentas de Análise e Extração do Registry]]
- [[Arquitetura 32 vs 64 bits no Registry e Executáveis (WOW6432Node)]]
- [[Ferramentas de Triagem Forense no Windows Registry (RegistryReport, ForensicUserInfo e WRR)]]
- [[Dispositivos de Arranque Forense - Disquetes DOS, Live CDs Linux, WinFE e USB]]
- [[Investigação Forense Digital - Análise Live vs Post-Mortem]]
- [[Diretrizes de Manuseamento - Identificação, Preservação, Isolamento e Correlação]]
- [[Camadas de Organização de Dados e Análise de Sistemas de Ficheiros]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
