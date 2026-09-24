---
title: Serviço BITS
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
tipo: procedimento
tags:
  - windows
  - servicos
  - bits
  - lolbin
  - ese
  - forense
aliases:
  - BITS
  - Background Intelligent Transfer Service
  - bitsadmin
  - BitsParser
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
fontes:
  - "https://github.com/fireeye/BitsParser/tree/master"
atualizado: 2026-09-24
---

# BITS — Background Intelligent Transfer Service

O **Background Intelligent Transfer Service (BITS)** é um serviço essencial do Windows concebido para transferir ficheiros de grande dimensão através da rede em segundo plano (*background*), otimizando a utilização de largura de banda:
* **Uso de Largura de Banda Ociosa**: O BITS monitoriza o tráfego de rede e utiliza apenas a largura de banda livre, reduzindo a velocidade de transferência quando outras aplicações em primeiro plano necessitam da ligação.
* **Resiliência e Retoma Automática**: Suporta a suspensão e retoma transparente de descarregamentos ou carregamentos caso ocorram quebras de conectividade, encerramento de sessão ou reinício do sistema operativo.
* **Aplicações Utilizadoras**: É o mecanismo primário do **Windows Update** e da **Microsoft Store**, sendo igualmente utilizado por aplicações de terceiros e navegadores como Google Chrome, Mozilla Firefox, Microsoft Edge, OneDrive e Adobe.

O BITS opera como um processo partilhado alojado numa instância de [[svchost.exe]] (`svchost.exe -k netsvcs -p`).

---

## Consulta de Estado Operacional

Para verificar o estado do serviço através da linha de comandos:

```cmd
sc query bits
```

---

## O Utilitário `bitsadmin.exe`

Historicamente, o Windows disponibiliza o utilitário de consola **`bitsadmin`** para gerir, criar e monitorizar tarefas de transferência BITS:

```cmd
REM Sintaxe geral para descarregamento de ficheiro
bitsadmin /transfer <NomeDaTarefa> /download /priority normal <URL_Remota> <Caminho_Local_Completo>
```

### Exemplo Prático de Descarregamento

```cmd
bitsadmin /transfer RadaresLRA /download /priority normal "https://radaresavista.pt/wp-content/uploads/2020/11/Distrito-Leiria.pdf" c:\temp\radares_LRA.pdf
```

* O parâmetro `/priority` define a urgência da tarefa (`foreground`, `high`, `normal` ou `low`).
* O caminho de destino local deve ser especificado de forma absoluta.

---

## Abuso Malicioso: Living off the Land (LOLBIN)

> [!WARNING] Vetor de Exfiltração e Descarregamento Malicioso
> O BITS é frequentemente classificado como um **LOLBIN (*Living off the Land Binary*)**. Como se trata de um componente legítimo e assinado pela Microsoft presente em qualquer instalação Windows:
> * Agentes maliciosos utilizam o BITS para descarregar *payloads* adicionais ou **exfiltrar ficheiros sensíveis** para a Internet.
> * As transferências contornam frequentemente controlos simples de firewall e regras perimetrais, uma vez que o tráfego de rede tem origem no próprio processo confiável do sistema operativo (`svchost.exe`).
> * As tarefas BITS podem ser configuradas com parâmetros de persistência, reexecutando comandos assim que a transferência for concluída.

---

## Investigação Forense e Artefactos de Transferência

Para auditar o histórico de transferências efetuadas via BITS num sistema sob investigação pericial, analisam-se duas fontes principais de evidência:

### 1. Windows Event Log
O sistema regista eventos operacionais detalhados de transferências BITS no canal dedicado:
* **Caminho**: `Event Viewer` $\rightarrow$ `Applications and Services Logs` $\rightarrow$ `Microsoft-Windows-Bits-Client/Operational`
* **Event ID 3**: Transferência iniciada.
* **Event ID 4**: Transferência concluída com sucesso. Regista o identificador do trabalho (*Job ID*), a conta de utilizador que requisitou a transferência e o número de ficheiros.
* **Event ID 59 / 60**: Alterações de estado e notificações.

### 2. Base de Dados ESE (`qmgr.db`)
O BITS armazena o estado persistente de todas as tarefas de transferência em ficheiros de base de dados do tipo **ESE (*Extended Storage Engine*)** localizados em:

```text
C:\ProgramData\Microsoft\Network\Downloader\
```

* **Ficheiros Principais**:
  * `qmgr.db`: Base de dados ESE principal que contém as tabelas de tarefas (`Jobs`) e ficheiros (`Files`).
  * `edb.log`: Ficheiro de transações *write-ahead* da base de dados.

### 3. Extração Forense com o `BitsParser`

Para extrair dados do ficheiro `qmgr.db` numa análise *post-mortem*, utiliza-se o analisador em Python **BitsParser** (FireEye):

```bash
# Extração estruturada de tarefas ativas e recentes para formato JSON
python BitsParser.py -i qmgr.db

# Ativação do modo de "carving" para recuperar entradas apagadas ainda presentes na base de dados
python BitsParser.py --carvedb -i qmgr.db
```

O relatório em JSON revela dados cruciais: URL de origem (`SourceURL`), caminho de destino no disco (`DestFile`), dimensões (`TransferByteSize`), carimbo temporal de criação (`CreationTime`) e o identificador do volume (`VolumeGUID`).

## Notas relacionadas

- [[svchost.exe]]
- [[Serviços Windows]]
- [[Serviço Delivery Optimization]]
- [[Windows Search]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
