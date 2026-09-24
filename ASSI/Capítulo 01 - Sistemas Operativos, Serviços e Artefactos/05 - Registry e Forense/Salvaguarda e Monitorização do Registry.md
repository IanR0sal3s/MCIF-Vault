---
title: Salvaguarda e Monitorização do Registry
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
tipo: procedimento
tags:
  - windows
  - registry
  - backup
  - schtasks
  - procmon
  - sysmon
  - forense
aliases:
  - RegBack
  - schtasks
  - Sysmon
  - Procmon
  - Monitorização do Registry
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
fontes:
  - "https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon"
  - "https://github.com/SwiftOnSecurity/sysmon-config/blob/master/sysmonconfig-export.xml"
atualizado: 2026-09-23
---

# Salvaguarda e Monitorização do Registry

O Registry está no centro de quase todas as operações do Windows, tornando-se simultaneamente o alvo preferencial para garantir persistência maliciosa e uma fonte crítica de telemetria pericial. A administração segura exige conhecer como o sistema efetua cópias de segurança e como monitorizar as suas alterações em tempo real.

---

## Salvaguarda Automática do Registry (`RegBack`)

Historicamente (Windows 7 e primeiras versões do Windows 10), o sistema operativo mantinha cópias de segurança periódicas dos ficheiros de hive:
* **Processo**: tarefa automática `RegIdleBackup`, agendada para executar a cada 10 dias em períodos de inatividade.
* **Diretório de cópia**: `C:\Windows\System32\config\RegBack\`
* Ficheiros salvaguardados: `DEFAULT`, `SAM`, `SECURITY`, `SOFTWARE`, `SYSTEM`.

```cmd
REM Consultar estado da tarefa de salvaguarda
schtasks.exe /query /v /FO CSV | findstr /i "regIdleBackup"
```

> [!WARNING] Desativação a partir do Windows 10 versão 1803
> A partir do Windows 10 v1803 (abril de 2018), a Microsoft **desativou por defeito** o `RegIdleBackup` para reduzir a pegada de disco.
> * Na maioria dos sistemas modernos, a pasta `RegBack` existe, mas os ficheiros de hive no seu interior têm **0 KB**.
> * Para reativar em ambientes empresariais é necessário configurar o valor DWORD `EnablePeriodicBackup = 1` na chave `HKLM\System\CurrentControlSet\Control\Session Manager\Configuration Manager`.
> * *Valor forense*: caso esteja ativo, o `RegBack` fornece uma "cópia limpa" anterior à infeção por malware.

---

## Agendamento de Tarefas (`schtasks.exe`)

O utilitário de linha de comandos `schtasks` permite criar, alterar e auditar tarefas agendadas (análogo em CLI ao `taskschd.msc`):

```cmd
REM Listar todas as tarefas em formato CSV
schtasks /query /FO csv

REM Filtrar tarefas ativas prontas a executar
schtasks /query /FO csv | findstr /i "ready"

REM Filtrar tarefas desativadas ou em estado distinto de "ready"
schtasks /query /FO csv | findstr /v /i "ready"
```

* **Relevância para a persistência**: O agendador de tarefas é amplamente utilizado por agentes maliciosos para manter persistência no sistema através de tarefas que disparam no arranque, no logon ou em horários definidos.

---

## Monitorização da Atividade no Registry

### 1. Process Monitor (`procmon.exe`) — Análise Dinâmica
Utilitário da suite Sysinternals que interceta em tempo real a atividade de processos ao nível do kernel:
* Captura operações de Registry: `RegOpenKey`, `RegQueryKey`, `RegSetValue`, `RegDeleteKey`.
* Regista o processo de origem (PID, caminho), resultado da operação (`SUCCESS`, `NAME NOT FOUND`, `ACCESS DENIED`) e duração.
* Ideal para ambientes de triagem, análise dinâmica de malware e resolução de conflitos de permissões.

### 2. System Monitor (`sysmon.exe`) — Auditoria Contínua
Diferente do `procmon` (que é interativo), o **Sysmon** instala-se como um **serviço do Windows** e um controlador de dispositivo (*driver*) que monitoriza o sistema continuamente e grava eventos de segurança no Windows Event Log:

```text
Applications and Services Logs\Microsoft\Windows\Sysmon\Operational
```

#### Eventos do Registry monitorizados pelo Sysmon:
* **Event ID 12**: Criação ou eliminação de chaves/valores do Registry (*RegistryEvent - Object create and delete*).
* **Event ID 13**: Modificação de valor de chave (*RegistryEvent - Value Set*).
* **Event ID 14**: Mudança de nome de chave ou valor (*RegistryEvent - Key and Value Rename*).

#### Instalação e Configuração

O Sysmon requer um ficheiro de regras XML para filtrar eventos irrelevantes e focar em comportamentos suspeitos:

```cmd
REM Ver a configuração atual em vigor
sysmon.exe -c

REM Instalar o Sysmon com um ficheiro de configuração XML
sysmon.exe -accepteula -i sysmonconfig-export.xml

REM Desinstalar o serviço
sysmon.exe -u
```

* **Configuração de Referência**: Ficheiro de configuração recomendado do projeto comunitário **Swift On Security** (`https://github.com/SwiftOnSecurity/sysmon-config`), desenhado para detetar ataques de persistência sem saturar o registo de eventos.

## Notas relacionadas

- [[Estrutura e Hives do Windows Registry]]
- [[Ferramentas de Análise e Extração do Registry]]
- [[Artefactos Forenses de Execução e Persistência no Registry]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
