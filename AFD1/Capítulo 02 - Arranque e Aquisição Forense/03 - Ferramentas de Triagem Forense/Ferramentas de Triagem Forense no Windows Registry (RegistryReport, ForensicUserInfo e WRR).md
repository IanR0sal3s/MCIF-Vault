---
title: Ferramentas de Triagem Forense no Windows Registry (RegistryReport, ForensicUserInfo e WRR)
tipo: ferramenta
mestrado: Cibersegurança e Informática Forense
uc: Análise Forense Digital I
sigla_uc: AFD1
capitulo: 2
bloco: 3
fonte_aula: MCIF – Digital Forensic Analysis 1 - Forensic Boot.pdf
tags:
  - afd1
  - forense
  - triagem
  - registry
  - sam
  - ntuser
  - registryreport
  - forensicuserinfo
  - mitec-wrr
aliases:
  - Triage Tools Windows Registry
  - RegistryReport
  - ForensicUserInfo
  - Mitec WRR
  - Windows Registry Recovery
atualizado: 2026-10-20
---

# Ferramentas de Triagem Forense no Windows Registry (RegistryReport, ForensicUserInfo e WRR)

As **ferramentas de triagem forense para o Windows Registry (*Forensic Triage Tools — Windows Registry*)** permitem analisar rapidamente os ficheiros de *hive* extraídos de um sistema (`SAM`, `SOFTWARE`, `SYSTEM` e `NTUSER.DAT`) — por exemplo, a partir de um arranque com **WinFE** ou de uma imagem montada — sem depender do sistema operativo instalado, automatizando a geração de relatórios sobre contas de utilizador, *hashes* de palavras-passe, software instalado, serviços, arranque automático e configuração de rede.

---

## Quadro Comparativo das Ferramentas de Triagem do Registry

| Ferramenta | Fonte Oficial | Hives Requeridos | Foco Principal na Triagem |
| :--- | :--- | :--- | :--- |
| **RegistryReport** | `https://www.gaijin.at/getit?id=registryreport` | `SAM`, `SOFTWARE`, `SYSTEM`, `NTUSER.DAT` | Geração de relatórios configuráveis e pesquisáveis (SO, software instalado, última atividade e definições do utilizador) em modo estritamente *offline*. |
| **ForensicUserInfo** | `https://github.com/woanware/ForensicUserInfo/releases/` | `SAM`, `SOFTWARE`, `SYSTEM` | Extração rápida de metadados de contas locais, `RID`, `LM/NT Hashes`, datas de login/reset/expiração, contadores de acessos e grupos. |
| **Mitec WRR** (*Windows Registry Recovery*) | `http://www.mitec.cz/wrr.html` | Hives individuais ou conjuntos (ex.: `NTUSER.DAT`, `SAM`, `SYSTEM`, `SOFTWARE`) | Recuperação e exploração visual da configuração de máquinas bloqueadas (*crashed*), cobrindo desde hardware e rede até *Startup*, serviços e dados brutos (*Raw Data*). |

---

## 1. RegistryReport

* **Página oficial**: `https://www.gaijin.at/getit?id=registryreport`
* **Ficheiros de Registry necessários**: `SAM`, `SOFTWARE`, `SYSTEM` e `NTUSER.DAT`.
* **Modo de Operação Offline**: **Não processa os ficheiros de registo do sistema operativo em execução** (*doesn't process the registry files of the running operating system*) — exige ficheiros de *hive* extraídos ou acedidos a partir de outro ambiente (como WinFE).
* **Informação Extraída** (suporta sistemas Windows 2000 ou superior):
  * Informação sobre o **sistema operativo** (*operating system*).
  * **Software instalado** (*installed software*).
  * **Última atividade do utilizador** (*last user activity*).
  * **Definições do utilizador** (*user settings*).
  * Muitos outros detalhes técnicos do sistema.
* **Personalização e Exportação**:
  * A quantidade de informação apresentada para cada categoria pode ser configurada na caixa de diálogo de definições (*settings dialog*).
  * Permite **guardar, imprimir e pesquisar** no relatório gerado.

---

## 2. ForensicUserInfo

* **Página oficial**: `https://github.com/woanware/ForensicUserInfo/releases/`
* **Ficheiros de Registry necessários**: `SAM`, `SOFTWARE` e `SYSTEM`.
* **Informação Extraída sobre Contas de Utilizador**:
  * **Identificação**: `RID` (*Relative Identifier*, ex.: `500` para `Administrator`, `501` para `Guest`, `1000+` para contas criadas), `Login Name`, `Name`, `Description` e `User Comment`.
  * **Credenciais Criptográficas**: **`LM Hash`** e **`NT Hash`** (resumos criptográficos das palavras-passe locais armazenados na `SAM`).
  * **Cronologia de Autenticação**:
    * *Last Login Date* (Data do último início de sessão).
    * *Password Reset Date* (Data da última reposição de palavra-passe).
    * *Account Expiry Date* (Data de expiração da conta).
    * *Login Fail Date* (Data da última falha de autenticação).
  * **Métricas e Perfil**:
    * *Login Count* (Contador de logins bem-sucedidos).
    * *Failed Logins* (Contador de tentativas falhadas).
    * *Profile Path* (Caminho do perfil no disco) e *Groups* (Grupos de segurança a que pertence, além de políticas como *Password Required*).

---

## 3. Mitec WRR (*Windows Registry Recovery*)

* **Página oficial**: `http://www.mitec.cz/wrr.html`
* **Objetivo**: Concebida para a recuperação de dados de configuração do Registry a partir de máquinas que sofreram falhas críticas (*crashed machine registry configuration data recovery*), sendo excelente para triagem pericial.
* **Módulos de Exploração Disponíveis**:
  * **File Information**: Metadados internos do ficheiro de *hive* carregado (ex.: tipo *Windows NT Registry*, data de última modificação, nome interno do *hive*, *checksum*, número de chaves e *HBINs*, e resumos criptográficos `CRC32`, `MD4`, `MD5` e `SHA1` do próprio ficheiro).
  * **SAM**: Contas de utilizador e políticas de segurança locais.
  * **Security Record Explorer**: Inspeção de registos de segurança.
  * **Windows Installation**: Dados da instalação do Windows (chave de produto, proprietário registado, data de instalação, versão).
  * **Hardware** e **User Data**: Inventário de componentes físicos e dados do perfil.
  * **Startup Applications**: Aplicações configuradas para arranque automático (persistência).
  * **Services and Drivers**: Serviços de sistema e controladores de kernel registados.
  * **Network Configuration** e **Windows Firewall Settings**: Interfaces de rede, endereços IP e regras de firewall.
  * **Environment** e **Shell Folders**: Variáveis de ambiente e mapeamento de pastas especiais da Shell.
  * **Outlook Express** e **Raw Data**: Configurações de cliente de e-mail legado e visualização bruta das chaves/valores (com opção de exportação para o formato `REGEDIT4`).

---

## Implicações Forenses

* **Bloqueio de Hives em Sistemas Live**: Num sistema Windows em execução normal, o kernel mantém um bloqueio exclusivo (*file lock*) sobre os ficheiros `C:\Windows\System32\config\SAM`, `SYSTEM`, `SOFTWARE` e `C:\Users\<user>\NTUSER.DAT` (razão pela qual o `RegistryReport` não lê o SO em execução). Para os analisar em triagem, o perito deve arrancar a máquina com um ambiente **WinFE** ou Live USB Linux (onde os ficheiros do disco interno estão inativos e acessíveis) ou copiá-los através do **FTK Imager Lite** (que lê ao nível dos setores do sistema de ficheiros contornando o bloqueio da API Win32).
* **Deteção Rápida de Contas Maliciosas (`ForensicUserInfo`)**: Na captura de ecrã da aula relativa ao `ForensicUserInfo`, observa-se imediatamente a conta suspeita `RID 1003 — Mr. Evil` com `Password not required`. A triagem das contas na `SAM` permite detetar em segundos contas *backdoor* criadas por atacantes, verificar se a conta `Guest` (`RID 501`) foi ativada e extrair os `NT Hashes` para auditoria de força de passwords.

---

## Além da aula

* **Integração Direta com o Estudo do Windows Registry em [[00 ASSI|ASSI]]**:
  * A localização física dos ficheiros `SAM`, `SYSTEM`, `SOFTWARE` (em `%SystemRoot%\System32\config\`) e `NTUSER.DAT` (em `%UserProfile%\`) e o seu mapeamento lógico nas árvores `HKLM` e `HKCU` são estudados detalhadamente em [[Estrutura e Hives do Windows Registry]] e sintetizados na [[Cheat Sheet - Registry e Forense]] (Bloco 05 de ASSI).
  * As ferramentas de triagem deste capítulo complementam o ecossistema estudado em [[Ferramentas de Análise e Extração do Registry]] (onde se abordam o **Registry Explorer** de Eric Zimmerman, o **RegRipper** e o **RegScanner** da NirSoft):
    * O módulo **Startup Applications** do *Mitec WRR* inspeciona as chaves `Run` e `RunOnce` detalhadas em [[Artefactos Forenses de Execução e Persistência no Registry]].
    * A secção de **última atividade do utilizador** do *RegistryReport* agrega artefactos residentes no `NTUSER.DAT`, como [[Artefacto Forense UserAssist|UserAssist]] e [[Artefactos Forenses de Interação do Utilizador (MRU e TypedPaths)|Listas MRU e TypedPaths]].
    * Os metadados temporais de *Last Login Date*, *Password Reset Date* e *InstallDate* extraídos pelo `ForensicUserInfo` e pelo `Mitec WRR` estão armazenados internamente em formato binário `FILETIME` (64 bits Little-Endian) ou *Unix Epoch* (32 bits), cuja descodificação matemática é estudada em [[Marcadores Temporais no Windows (Timestamps)]] (ASSI) e [[Representação Forense de Data e Hora (Timestamps e SQLite)]] (AFD1 Cap. 3).

---

## Perguntas de revisão

- Que ficheiros de *hive* do Windows Registry são exigidos pelo `RegistryReport` e porque é que esta ferramenta não analisa diretamente o Registry do sistema operativo onde está a correr?
- Que informações críticas sobre contas de utilizador e autenticação são extraídas pela ferramenta `ForensicUserInfo` a partir dos hives `SAM`, `SOFTWARE` e `SYSTEM`?
- Para que cenário foi desenhada a ferramenta `Mitec WRR` (*Windows Registry Recovery*) e que categorias de configuração do sistema permite inspecionar?

## Notas relacionadas

- [[Ferramentas Portáteis de Triagem, Pesquisa e FTK Imager Lite]]
- [[Dispositivos de Arranque Forense - Disquetes DOS, Live CDs Linux, WinFE e USB]]
- [[Diretrizes de Manuseamento - Identificação, Preservação, Isolamento e Correlação]]
- [[Estrutura e Hives do Windows Registry]]
- [[Ferramentas de Análise e Extração do Registry]]
- [[Cheat Sheet - Registry e Forense]]
- [[Artefactos Forenses de Execução e Persistência no Registry]]
- [[Artefactos Forenses de Interação do Utilizador (MRU e TypedPaths)]]
- [[Artefacto Forense UserAssist]]
- [[Marcadores Temporais no Windows (Timestamps)]]
- [[Representação Forense de Data e Hora (Timestamps e SQLite)]]
- [[Capítulo 2 - Arranque e Aquisição Forense]]
