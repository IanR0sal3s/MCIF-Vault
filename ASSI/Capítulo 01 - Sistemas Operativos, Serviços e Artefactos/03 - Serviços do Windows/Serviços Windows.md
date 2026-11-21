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
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v4.pdf
atualizado: 2026-11-21
---

# Serviços do Windows

Os **Serviços do Windows** (equivalentes aos *daemons* em Unix/Linux) executam em segundo plano de forma **não interativa** (sem input do utilizador) e podem iniciar automaticamente no arranque do sistema operativo.

## 1. Dimensão e Exemplos Típicos

Um sistema Windows mantém centenas de serviços (contáveis via `psservice` da Sysinternals):
* **Registados** (`psservice | findstr /i "SERVICE_NAME"`): ~240 no W10 (v1703) · ~294 no W11 (v23H2);
* **Em execução** (`psservice | findstr /i "Running"`): ~101 no W10 (v1703) · ~158 no W11 (v23H2).

| Serviço | Função |
| :--- | :--- |
| **`BDESVC`** | BitLocker Drive Encryption Service |
| **`BFE`** | Base Filtering Engine (políticas de firewall e IPsec) |
| **`BITS`** | [[Serviço BITS|Background Intelligent Transfer Service]] |
| **`CertPropSvc`** | Copia certificados de *smart cards* (ex.: Cartão de Cidadão) para o repositório do utilizador |
| **`DiagTrack`** | Connected User Experiences and Telemetry |
| **`Dhcp` / `Dnscache`** | Cliente DHCP / Cliente DNS |
| **`wuauserv`** | Windows Update |
| **`Spooler`** | Print Spooler (`spoolsv.exe`) — gere tarefas de impressão |
| **`WSearch`** | [[Windows Search]] — indexação de ficheiros |
| **`DoSvc`** | [[Serviço Delivery Optimization]] — distribuição P2P de updates |

---

## 2. Gestão Gráfica e Linha de Comandos (`net` e `sc`)

* **Interfaces gráficas**: **Gestor de Tarefas** (W11 inclui separador *Serviços*) e **MMC** (`services.msc` via `Win + R`).
* **`net` (modo administrador)** — controlo básico de execução:
  ```cmd
  net start                    :: Lista serviços em execução
  net stop|start|pause|continue nome_servico
  ```
* **`sc` (*Service Control*)** — interage diretamente com o gestor de serviços (`scm.exe`):
  ```cmd
  sc query nome_servico        :: Estado dinâmico atual (RUNNING / STOPPED)
  sc queryex nome_servico      :: Estado estendido (inclui PID)
  sc qc nome_servico           :: Configuração estática (executável, arranque, dependências, conta)
  sc start|stop|pause|delete nome_servico
  sc create nome_servico
  ```

---

## 3. Caso de Estudo: `Spooler` (`sc qc Spooler`)

O comando `sc qc <serviço>` revela o executável associado (`BINARY_PATH_NAME`) e os parâmetros de segurança:
* **`BINARY_PATH_NAME`**: `C:\Windows\System32\spoolsv.exe`
* **`TYPE`**: `WIN32_OWN_PROCESS` (corre em processo próprio) + `Interactive` (autorizado a interagir com ambiente gráfico)
* **`START_TYPE`**: `AUTO_START` (arranca com o SO)
* **`ERROR_CONTROL`**: `1 Normal` (falha não impede o arranque normal do Windows)
* **`DEPENDENCIES`**: `RPCss` e `HTTP`
* **`SERVICE_START_NAME`**: **`LocalSystem`** (elevado privilégio — motivo pelo qual o `Spooler` é alvo frequente de ataques e falhas).

---

## Perguntas de revisão

1. **Qual a diferença entre `sc query Spooler` e `sc qc Spooler`?**

> [!success]- Ver Resposta
> `sc query` consulta o **estado atual** do serviço (ex.: `RUNNING`/`STOPPED`), enquanto `sc qc` (*Query Config*) consulta a **configuração persistente** (executável `BINARY_PATH_NAME`, tipo de processo, arranque, dependências e conta `SERVICE_START_NAME`).

2. **Porque é que o serviço `Spooler` (`spoolsv.exe`) é considerado de alto risco quando contém vulnerabilidades?**

> [!success]- Ver Resposta
> Porque corre sob a conta **`LocalSystem`** (elevado privilégio no sistema local), além de interagir com drivers de impressora e arrancar automaticamente com o SO.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Comando forfiles]] | `Bloco 02` |
| **Seguinte** | [[svchost.exe]] | `mesmo bloco` |
| **Índice** | [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]] · [[00 ASSI]] | `Bloco 03` |

### Conceitos Relacionados

* [[Serviço BITS]] · `mesmo bloco`
* [[Serviço Delivery Optimization]] · `mesmo bloco`
* [[Windows Search]] · `mesmo bloco`
