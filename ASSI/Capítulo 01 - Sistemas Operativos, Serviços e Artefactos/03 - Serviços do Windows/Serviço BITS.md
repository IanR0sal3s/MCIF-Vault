---
title: Serviço BITS
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 3
tipo: procedimento
tags:
  - assi
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

O **Background Intelligent Transfer Service (BITS)** é o serviço do Windows que transfere ficheiros em segundo plano utilizando largura de banda ociosa, garantindo retoma automática após quebras de rede ou reinícios.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: Descarregar atualizações pesadas (Windows Update, Microsoft Store, browsers) sem degradar a experiência do utilizador exige um gestor assíncrono que ajuste a taxa de transferência à largura de banda livre e persista o estado dos *jobs* em disco (`qmgr.db`).
> * **Porque importa (Forense / Segurança)**: Por correr dentro de um processo confiável ([[svchost.exe]]) e persistir após reinícios, o BITS é frequentemente abusado como **LOLBIN** (via `bitsadmin`) para descarregar *malware* ou exfiltrar dados contornando firewalls.
> * **Pontos Críticos para Exame**:
>   * Fontes de evidência forense: **Event Log** (`Microsoft-Windows-Bits-Client/Operational`, **Event ID 3** = iniciada, **Event ID 4** = concluída, **59/60** = estado) e base de dados **ESE `qmgr.db`** em `C:\ProgramData\Microsoft\Network\Downloader\`.
>   * Extração *post-mortem* de tarefas ativas e apagadas em `qmgr.db`: **`BitsParser.py`** (opção `--carvedb` para recuperar registos eliminados).

---

## Características Arquiteturais e Estado Operacional

O BITS otimiza a utilização de largura de banda através de três propriedades fundamentais:

* **Uso de Largura de Banda Ociosa**: O BITS monitoriza o tráfego de rede e utiliza apenas a largura de banda livre, reduzindo a velocidade de transferência quando outras aplicações em primeiro plano necessitam da ligação.
* **Resiliência e Retoma Automática**: Suporta a suspensão e retoma transparente de descarregamentos ou carregamentos caso ocorram quebras de conectividade, encerramento de sessão ou reinício do sistema operativo.
* **Aplicações Utilizadoras**: É o mecanismo primário do **Windows Update** e da **Microsoft Store**, sendo igualmente utilizado por aplicações de terceiros e navegadores como Google Chrome, Mozilla Firefox, Microsoft Edge, OneDrive e Adobe.

O BITS opera como um processo partilhado alojado numa instância de [[svchost.exe]] (`svchost.exe -k netsvcs -p`). Para verificar o estado do serviço através da linha de comandos:

```cmd
sc query bits
```

---

## O Utilitário `bitsadmin.exe`

Historicamente, o Windows disponibiliza o utilitário de consola **`bitsadmin`** para gerir, criar e monitorizar tarefas de transferência BITS.

### Anatomia do Comando `bitsadmin`

```cmd
bitsadmin /transfer <NomeDaTarefa> /download /priority normal <URL_Remota> <Caminho_Local_Completo>
```

| Parâmetro / Argumento | Função Operacional |
| :--- | :--- |
| **`/transfer <NomeDaTarefa>`** | Cria e executa uma tarefa de transferência identificada pelo nome atribuído (ex.: `RadaresLRA`). |
| **`/download`** | Especifica a direção da transferência (descarregamento remoto para a máquina local). |
| **`/priority <nivel>`** | Define a urgência da tarefa face à largura de banda disponível (`foreground`, `high`, `normal` ou `low`). |
| **`<URL_Remota>`** | Endereço HTTP/HTTPS ou caminho UNC de origem do ficheiro. |
| **`<Caminho_Local_Completo>`** | Destino local no disco; **deve ser obrigatoriamente especificado como caminho absoluto**. |

### Exemplo Prático de Descarregamento

```cmd
bitsadmin /transfer RadaresLRA /download /priority normal "https://radaresavista.pt/wp-content/uploads/2020/11/Distrito-Leiria.pdf" c:\temp\radares_LRA.pdf
```

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

| Fonte de Evidência | Caminho / Localização | Informação Pericial Extraída |
| :--- | :--- | :--- |
| **1. Windows Event Log** | `Event Viewer` $\rightarrow$ `Applications and Services Logs` $\rightarrow$ `Microsoft-Windows-Bits-Client/Operational` | **Event ID 3** (início), **Event ID 4** (conclusão com *Job ID*, utilizador e n.º de ficheiros), **Event ID 59 / 60** (alterações de estado). |
| **2. Base de Dados ESE (`qmgr.db`)** | `C:\ProgramData\Microsoft\Network\Downloader\` (`qmgr.db` e `edb.log`) | Tabelas persistentes `Jobs` e `Files`: `SourceURL`, `DestFile`, `TransferByteSize`, `CreationTime` e `VolumeGUID`. |

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

---

## Perguntas de revisão

1. **Por que motivo o serviço BITS e o utilitário `bitsadmin` são frequentemente explorados como LOLBINs por atacantes?**

> [!success]- Ver Resposta
> Porque são componentes nativos assinados pela Microsoft e as transferências de rede são executadas pelo processo legítimo `svchost.exe` (`svchost.exe -k netsvcs -p`). Isto permite descarregar *malware* ou exfiltrar dados contornando firewalls baseadas em aplicação, mantendo resiliência a reinícios e permitindo agendar a execução de comandos após a conclusão do *job*.

2. **Onde reside a base de dados persistente do BITS no disco, que motor de base de dados utiliza e que ferramenta permite recuperar tarefas já apagadas?**

> [!success]- Ver Resposta
> Reside em `C:\ProgramData\Microsoft\Network\Downloader\` no ficheiro **`qmgr.db`** (acompanhado por `edb.log`), gerido pelo motor **ESE (*Extended Storage Engine*)**. Para recuperar tarefas apagadas realiza-se *carving* com a ferramenta **`BitsParser`** usando o comando `python BitsParser.py --carvedb -i qmgr.db`.

3. **Quais são os Event IDs mais relevantes no canal `Microsoft-Windows-Bits-Client/Operational` durante uma análise forense ao Event Log?**

> [!success]- Ver Resposta
> * **Event ID 3**: Transferência iniciada.
> * **Event ID 4**: Transferência concluída com sucesso (identifica o *Job ID*, a conta de utilizador responsável e o número de ficheiros).
> * **Event ID 59 e 60**: Alterações de estado e notificações de transferência.

## Notas relacionadas

- [[svchost.exe]]
- [[Serviços Windows]]
- [[Serviço Delivery Optimization]]
- [[Windows Search]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
