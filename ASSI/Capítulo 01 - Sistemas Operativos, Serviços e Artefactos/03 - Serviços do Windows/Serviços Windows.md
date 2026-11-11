---
title: Serviços Windows
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 3
tipo: conceito
tags:
  - assi
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

Os **Serviços do Windows** (equivalentes aos *daemons* em sistemas Unix/Linux) são programas em segundo plano que operam de forma não interativa para assegurar funções contínuas de rede, hardware, segurança e infraestrutura.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: O sistema operativo necessita de executar tarefas críticas continuamente desde o arranque (como DHCP, DNS, firewall ou criptografia BitLocker) independentemente de existir ou não uma sessão gráfica de utilizador iniciada, sendo todos os serviços geridos centralmente pelo **Service Control Manager** (`scm.exe` / `services.exe`).
> * **Porque importa (Forense / Segurança)**: A criação ou modificação de serviços é um dos mecanismos clássicos de persistência e elevação de privilégios (`LocalSystem`), e serviços desnecessários ativos (como o `Spooler` em Controladores de Domínio) expõem superfícies críticas de ataque (*PrintNightmare*).
> * **Pontos Críticos para Exame**:
>   * Sintaxe estrita do `sc config`: é **obrigatório incluir um espaço após o sinal de igual** (ex.: `sc config Spooler start= disabled`).
>   * Diferença entre `sc qc <servico>` (consulta a configuração estática: binário, dependências, conta e tipo de arranque) e `sc query <servico>` (consulta o estado dinâmico de execução).

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

### 2. Comparação e Anatomia dos Utilitários CLI (`net.exe` vs. `sc.exe`)

| Característica | `net.exe` (`net start` / `net stop`) | `sc.exe` (*Service Control*) |
| :--- | :--- | :--- |
| **Nível de Controlo** | Básico: apenas controlo de estado imediato (iniciar, parar, pausar, continuar). | Granular: comunica diretamente com o **Service Control Manager** (`scm.exe` / `services.exe`). |
| **Alteração de Arranque / Registo** | Não suporta alterar tipo de arranque nem eliminar serviços. | Suporta reconfigurar arranque (`sc config`), consultar configuração (`sc qc`) e remover (`sc delete`). |

#### Comandos `net.exe` (exigem privilégios de Administrador)

```cmd
REM Listar serviços iniciados
net start

REM Controlar a execução de um serviço
net start nome_servico
net stop nome_servico
net pause nome_servico
net continue nome_servico
```

#### Anatomia do Comando `sc.exe` (Service Control)

```cmd
sc <subcomando> <nome_servico> [parametro= valor]
```

* **`query` / `queryex`**: mostra o estado operacional atual (`RUNNING`, `STOPPED`) e, no caso de `queryex`, o **PID** e flags estendidas.
* **`qc`** (*Query Config*): extrai a configuração persistente do serviço no Registry (`BINARY_PATH_NAME`, `START_TYPE`, `DEPENDENCIES`, `SERVICE_START_NAME`).
* **`config`**: modifica parâmetros permanentes do serviço (atenção à regra sintática: `start= disabled` exige um espaço após o `=`).

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

| Campo Devolvido (`sc qc`) | Valor no Serviço `Spooler` | Significado Técnico e Forense |
| :--- | :--- | :--- |
| **`BINARY_PATH_NAME`** | `C:\Windows\System32\spoolsv.exe` | Executável invocado pelo SCM ao iniciar o serviço. |
| **`TYPE`** | `110  WIN32_OWN_PROCESS (interactive)` | O serviço corre num processo exclusivo e dedicado, separado de outros serviços. |
| **`START_TYPE`** | `2   AUTO_START` | Inicializado automaticamente durante o arranque do sistema operativo. |
| **`ERROR_CONTROL`** | `1   NORMAL` | Se o serviço falhar no arranque, o Windows regista um erro no Event Log mas prossegue o arranque normalmente. |
| **`DEPENDENCIES`** | `RPCSS` e `HTTP` | Depende da inicialização prévia dos serviços Remote Procedure Call (`RPCSS`) e `HTTP`. |
| **`SERVICE_START_NAME`** | `LocalSystem` | Corre sob a conta interna de maior privilégio do sistema local. |

> [!WARNING] Vetor Histórico de Ataque
> O Print Spooler é historicamente alvo frequente de vulnerabilidades graves de execução remota de código e elevação local de privilégios (como o *PrintNightmare*). Em servidores de infraestrutura que não operem como servidores de impressão (ex.: Controladores de Domínio Active Directory), a boa prática de endurecimento (*hardening*) dita a desativação expressa deste serviço (`sc config Spooler start= disabled`).

---

## Perguntas de revisão

1. **Qual é a diferença entre os comandos `sc query Spooler` e `sc qc Spooler`?**

> [!success]- Ver Resposta
> * **`sc query Spooler`**: consulta o **estado dinâmico atual** do serviço (ex.: se está `RUNNING` ou `STOPPED`).
> * **`sc qc Spooler`** (*Query Configuration*): consulta a **configuração estática** do serviço registada no sistema (caminho do binário `BINARY_PATH_NAME`, tipo de processo `WIN32_OWN_PROCESS`, tipo de arranque `AUTO_START`, dependências e conta `SERVICE_START_NAME`).

2. **Qual é o comando exato de linha de comandos para desativar permanentemente o arranque automático do serviço Print Spooler num servidor Windows?**

> [!success]- Ver Resposta
> `sc config Spooler start= disabled` (respeitando obrigatoriamente o espaço em branco imediatamente após `start=`).

3. **Como se pode contabilizar na linha de comandos o número aproximado de serviços registados e o número de serviços em execução recorrendo à ferramenta `psservice` (Sysinternals)?**

> [!success]- Ver Resposta
> * Serviços registados: `psservice | findstr /i "SERVICE_NAME"` (~240 no Windows 10; ~294 no Windows 11).
> * Serviços em execução: `psservice | findstr /i "Running"` (~101 no Windows 10; ~158 no Windows 11).

4. **Por que razão o serviço `Spooler` representa um risco elevado de segurança quando explorado e que privilégio detém por omissão?**

> [!success]- Ver Resposta
> Porque corre sob a conta `LocalSystem` (`SERVICE_START_NAME: LocalSystem`), que detém o privilégio máximo no sistema local; vulnerabilidades como o *PrintNightmare* permitem a um atacante executar código arbitrário ou elevar privilégios diretamente para `SYSTEM`.

## Notas relacionadas

- [[svchost.exe]]
- [[Serviço BITS]]
- [[Serviço Delivery Optimization]]
- [[Windows Search]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
