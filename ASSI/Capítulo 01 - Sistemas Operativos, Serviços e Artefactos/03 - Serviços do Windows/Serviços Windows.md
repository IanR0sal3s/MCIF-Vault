---
title: Serviços Windows
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
tipo: conceito
tags:
  - windows
  - servicos
  - scm
  - spooler
  - daemon
aliases:
  - Serviços Windows
  - Windows Services
  - sc.exe
  - net start
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
atualizado: 2026-09-24
---

# Serviços do Windows

Os **Serviços do Windows** são programas em segundo plano que operam de forma **não interativa** (sem interface direta com o utilizador e sem depender de sessões gráficas abertas). Tipicamente iniciam com o arranque do sistema operativo e desempenham funções contínuas de infraestrutura, rede, gestão de hardware e segurança.

No ecossistema Unix/Linux, correspondem diretamente ao conceito de ***daemons***.

---

## Quantidade e Ordem de Grandeza de Serviços

Um sistema operativo Windows moderno mantém centenas de serviços registados, variando consoante a versão do sistema e as aplicações instaladas. A ferramenta **`psservice`** (Sysinternals) permite quantificar os serviços registados e os serviços em estado ativo (*Running*):

| Critério de Pesquisa (`psservice`) | Windows 10 (v1703) | Windows 11 (v23H2) |
| :--- | :---: | :---: |
| **Serviços Registados** (`psservice \| findstr /i "SERVICE_NAME"`) | ~240 | ~294 |
| **Serviços em Execução** (`psservice \| findstr /i "Running"`) | ~101 | ~158 |

*(Estes valores representam ordens de grandeza observadas em ambientes de teste de referência).*

---

## Exemplos Típicos de Serviços do Sistema

| Serviço | Nome Interno | Descrição e Função |
| :--- | :--- | :--- |
| **Adobe Acrobat Update Service** | `AdobeARMservice` | Gestão de atualizações automáticas de produtos Adobe. |
| **Windows Audio** | `Audiosrv` | Gestão e encaminhamento de áudio para aplicações e dispositivos. |
| **BitLocker Drive Encryption** | `BDESVC` | Gestão de encriptação de volumes de armazenamento. |
| **Base Filtering Engine** | `BFE` | Gestor de políticas de filtragem de pacotes, firewall do Windows e IPsec. |
| **Background Intelligent Transfer Service** | `BITS` | Transferência inteligente de ficheiros em segundo plano ([[Serviço BITS]]). |
| **Certificate Propagation** | `CertPropSvc` | Propagação de certificados de segurança a partir de *Smart Cards* (ex.: Cartão de Cidadão) para o repositório de certificados do utilizador. |
| **Microsoft Office Click-to-Run** | `ClickToRunSvc` | Gestão de atualizações e streaming de componentes do Microsoft Office. |
| **Dropbox Update Service** | `Dbupdate` | Serviço de atualização automática do cliente Dropbox. |
| **DHCP Client** | `Dhcp` | Registo de rede e obtenção de configurações dinâmicas de IP via DHCP. |
| **Connected User Experiences and Telemetry** | `DiagTrack` | Serviço de telemetria, diagnóstico e recolha de dados de experiência. |
| **DNS Client** | `Dnscache` | Resolução e colocação em memória cache de nomes de domínio DNS. |
| **Windows Update** | `wuauserv` | Deteção, descarregamento e instalação de atualizações do Windows. |
| **Print Spooler** | `Spooler` | Gestão das tarefas de impressão e interação com drivers de impressora. |
| **Windows Search** | `WSearch` | Indexação de conteúdos e metadados de ficheiros ([[Windows Search]]). |
| **Delivery Optimization** | `DoSvc` | Otimização de entrega de atualizações via rede local P2P ([[Serviço Delivery Optimization]]). |

---

## Gestão e Interfaces de Administração

### 1. Interfaces Gráficas
* **Consola de Gestão MMC (`services.msc`)**: Interface gráfica padrão que permite inspecionar propriedades, tipo de arranque (Automático, Manual, Desativado), dependências e credenciais de início de sessão de cada serviço.
* **Gestor de Tarefas (`Task Manager`)**: No Windows 11, inclui um separador lateral dedicado à monitorização do estado de serviços e associação a PIDs.

### 2. Utilitário `net.exe`
Comandos simplificados para controlo de estado operacional (exigem privilégios de administrador):

```cmd
REM Listar serviços iniciados
net start

REM Controlar a execução de um serviço
net start nome_servico
net stop nome_servico
net pause nome_servico
net continue nome_servico
```

### 3. Utilitário `sc.exe` (Service Control)
Utilitário de controlo granular que comunica diretamente com o **Service Control Manager** (`scm.exe` / `services.exe`):

```cmd
REM Consultar estado detalhado de um serviço
sc query nome_servico
sc queryex nome_servico

REM Consultar a configuração completa (caminho do binário, tipo de processo, dependências)
sc qc nome_servico

REM Iniciar, parar ou eliminar um serviço
sc start nome_servico
sc stop nome_servico
sc delete nome_servico

REM Alterar o tipo de arranque (atenção: espaço obrigatório após start=)
sc config nome_servico start= disabled
```

---

## Caso de Estudo: O Serviço Spooler (`spoolsv.exe`)

A inspeção do serviço de impressão através de `sc qc Spooler` ilustra a estrutura de configuração de um serviço com processo autónomo:

```cmd
sc qc Spooler
```

Campos chave devolvidos:
* **`BINARY_PATH_NAME`**: `C:\Windows\System32\spoolsv.exe`.
* **`TYPE`**: `110  WIN32_OWN_PROCESS (interactive)` — o serviço corre num processo exclusivo, separado de outros serviços.
* **`START_TYPE`**: `2   AUTO_START` — inicializado automaticamente durante o arranque do sistema.
* **`ERROR_CONTROL`**: `1   NORMAL` — se o serviço falhar no arranque, o Windows regista um erro no Event Log mas prossegue o arranque normalmente.
* **`DEPENDENCIES`**: Depende da inicialização prévia dos serviços `RPCSS` (Remote Procedure Call) e `HTTP`.
* **`SERVICE_START_NAME`**: `LocalSystem` — corre sob a conta de maior privilégio do sistema local.

> [!WARNING] Vetor Histórico de Ataque
> O Print Spooler é historicamente alvo frequente de vulnerabilidades graves de execução remota de código e elevação local de privilégios (como o *PrintNightmare*). Em servidores de infraestrutura que não operem como servidores de impressão (ex.: Controladores de Domínio Active Directory), a boa prática de endurecimento (*hardening*) dita a desativação expressa deste serviço (`sc config Spooler start= disabled`).

## Notas relacionadas

- [[svchost.exe]]
- [[Serviço BITS]]
- [[Serviço Delivery Optimization]]
- [[Windows Search]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
