---
title: Ficha Prática e Questionário — Serviços e Windows Search
tipo: exercicio
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 3
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
tags:
  - assi
  - windows
  - servicos
  - wsearch
  - cli
  - sidr
  - lab
  - questionario
aliases:
  - Ficha Prática 01
  - Lab 1 Windows Search
  - Questionário Serviços Windows
atualizado: 2026-10-13
---

# Ficha Prática e Questionário — Serviços e Windows Search

Guião prático de consolidação laboratorial e questionário de avaliação para os **Blocos 02 e 03** do Capítulo 1 (*Processos, Linha de Comandos, Serviços do Windows e Windows Search*).

---

## 1. Guião Prático de Laboratório (Laboratório 1)

### Exercício 1: Quantificação e Auditoria de Serviços via Linha de Comandos
Em contexto de resposta a incidentes, a enumeração não-interativa de serviços permite detetar rapidamente serviços maliciosos ou desnecessários.

1. **Quantificar serviços totais vs. ativos** com o utilitário Sysinternals `psservice`:
   ```cmd
   REM Contar serviços registados no sistema
   psservice | findstr /i "SERVICE_NAME" | find /c /v ""

   REM Contar serviços atualmente em execução (Running)
   psservice | findstr /i "STATE" | findstr /i "RUNNING" | find /c /v ""
   ```
2. **Identificar processos anfitriões partilhados** através de `tasklist /svc`:
   ```cmd
   REM Filtrar todos os serviços a correr debaixo de instâncias svchost.exe
   tasklist /fi "IMAGENAME eq svchost.exe" /svc
   ```

---

### Exercício 2: Inspeção Granular e Endurecimento com `sc.exe`
O utilitário `sc.exe` comunica diretamente com o **Service Control Manager** (`services.exe`).

1. **Inspecionar a configuração do serviço de impressão (`Spooler`)**:
   ```cmd
   sc qc Spooler
   ```
   * *Verificação*: Analise o campo `BINARY_PATH_NAME`, o `START_TYPE` (2 = Auto Start) e o `SERVICE_START_NAME` (`LocalSystem`).
2. **Aplicar endurecimento (*hardening*)** num servidor que não desempenha funções de impressão:
   ```cmd
   REM Parar o serviço ativo
   sc stop Spooler

   REM Desativar o arranque automático (atenção: espaço obrigatório após start=)
   sc config Spooler start= disabled
   ```

---

### Exercício 3: Automação e Filtragem por Datas com `forfiles`
O comando `forfiles` permite iterar recursivamente em ficheiros e executar comandos por critérios temporais.

1. **Localizar e exportar todos os ficheiros modificados nos últimos 7 dias** na pasta temporária:
   ```cmd
   forfiles /p C:\Windows\Temp /s /d -7 /m *.* /c "cmd /c echo @path @fdate @ftime @fsize" > C:\Temp\Auditoria_Temp.txt
   ```
2. **Listar ficheiros executáveis `.exe` criados antes de determinada data**:
   ```cmd
   forfiles /p C:\Users\Public /m *.exe /d -30 /c "cmd /c echo Executável antigo detetado: @path"
   ```

---

### Exercício 4: Extração Forense do Windows Search com `sidr`
O **Windows Search** indexa conteúdos de ficheiros e histórico de navegação no ficheiro `Windows.edb` (Windows 10) ou `Windows.db` (Windows 11).

1. **Localização física da base de dados**:
   $$\texttt{C:\textbackslash ProgramData\textbackslash Microsoft\textbackslash Search\textbackslash Data\textbackslash Applications\textbackslash Windows\textbackslash}$$
2. **Extração de relatórios CSV** utilizando o utilitário `sidr`:
   ```cmd
   sidr.exe -f csv "C:\ProgramData\Microsoft\Search\Data\Applications\Windows" -o "C:\Forensics\Relatorio_WSearch"
   ```
3. **Análise dos relatórios gerados**:
   * Abrir o ficheiro `File_Report.csv` e filtrar por extensões confidenciais (`.kdbx`, `.pdf`, `.docx`, `.pem`).
   * Abrir `Internet_History_Report.csv` e verificar pesquisas efetuadas a partir da barra de endereços do Edge.

---

### Exercício 5: Validação Binária de Assinatura (EDB vs. SQLite3)
1. Abrir o ficheiro `Windows.db` do Windows 11 num editor hexadecimal (HxD).
2. Confirmar a sequência de **Magic Bytes** no início do ficheiro:
   ```text
   Offset 0x00: 53 51 4C 69 74 65 20 66 6F 72 6D 61 74 20 33 00
   ASCII:       SQLite format 3.
   ```
3. Identificar a presença dos ficheiros de apoio **`Windows.db-wal`** (*Write-Ahead Logging*) e **`Windows.db-shm`** (*Shared Memory*), obrigatórios para garantir a integridade transacional na aquisição.

---

## 2. Questionário de Avaliação e Cenários Forenses

### Questão 1
Durante a análise de um controlador de domínio comprometido, o perito verifica que o serviço **Spooler** (`Print Spooler`) está ativo sob a conta `LocalSystem`. Porque é que este serviço constitui um vetor crítico de elevação de privilégios e qual o comando correto para o desativar permanentemente?
* **A)** Porque corre em modo interativo de utilizador; comando `net stop Spooler /permanent`.
* **B)** Porque corre como `LocalSystem`, possui histórico de falhas de execução remota (ex.: *PrintNightmare*) e deve ser desativado com `sc config Spooler start= disabled`.
* **C)** Porque impede o bloqueio de portas SMB; comando `sc delete Spooler`.
* **D)** Porque permite a injeção direta de DLLs no Registry; comando `reg delete HKLM\SYSTEM\Services\Spooler`.

---

### Questão 2
O serviço **BITS** (*Background Intelligent Transfer Service*) é frequentemente categorizado na literatura pericial como um vetor **LOLBin** (*Living off the Land*). Qual das seguintes afirmações justifica tecnicamente essa classificação?
* **A)** O BITS consegue descarregar e executar ficheiros a partir da Internet contornando a firewall através de janelas de largura de banda ociosa, preservando trabalhos em tarefas registadas na base `qmgr.db`.
* **B)** O BITS desativa automaticamente o Windows Defender durante o descarregamento de pacotes `.cab`.
* **C)** O BITS substitui diretamente o processo `svchost.exe` por um binário arbitrário escolhido pelo atacante.
* **D)** O BITS apenas funciona se o utilizador possuir privilégios de administrador de domínio.

---

### Questão 3
No comando `forfiles /p C:\Windows\System32 /m *.dll /d +15 /c "cmd /c echo @file"`, qual é o efeito prático do argumento `/d +15`?
* **A)** Seleciona ficheiros modificados nos últimos 15 dias.
* **B)** Seleciona ficheiros com tamanho superior a 15 Megabytes.
* **C)** Seleciona ficheiros com carimbo de modificação posterior ou igual à data atual mais 15 dias (geralmente gerado por *timestomping* ou datas futuras).
* **D)** Adiciona 15 horas à marca temporal exibida em `@ftime`.

---

### Questão 4
Na transição do **Windows 10** para o **Windows 11**, o mecanismo interno de indexação do **Windows Search** sofreu uma mutação estrutural profunda. Qual é a principal diferença entre os dois formatos?
* **A)** O Windows 10 utilizava texto plano XML; o Windows 11 utiliza uma base binária proprietária não descodificável.
* **B)** O Windows 10 utilizava o motor ESE (`Windows.edb`) onde um registo continha todas as propriedades do ficheiro; o Windows 11 utiliza SQLite3 (`Windows.db`) onde os dados foram normalizados em múltiplos registos associados a `ColumnId`.
* **C)** O Windows 10 gravava o histórico de pesquisa no Registry; o Windows 11 grava em ficheiros JSON.
* **D)** O Windows 11 descontinuou por completo o serviço `WSearch`, delegando a indexação no `SysMain`.

---

### Questão 5
Ao efetuar a recolha forense de uma base de dados SQLite do Windows Search (`Windows.db`) num sistema ativo, o perito copiou apenas o ficheiro `.db`. Ao abrir a base no *DB Browser for SQLite*, verificou que os registos mais recentes não estavam visíveis. Qual foi a falha cometida na aquisição?
* **A)** O ficheiro precisava de ser renomeado para `.edb` antes de abrir.
* **B)** Não foram recolhidos os ficheiros complementares `Windows.db-wal` (transações pendentes) e `Windows.db-shm` (memória partilhada).
* **C)** O SQLite exige que o serviço `WSearch` seja parado com `net stop` para descarregar dados para o Registry.
* **D)** As bases do Windows 11 só podem ser abertas após conversão com a ferramenta `esentutl`.

---

### Questão 6
Qual é a finalidade técnica do argumento `/svc` na execução do comando `tasklist /svc`?
* **A)** Listar apenas os processos que consomem tráfego de rede ativo.
* **B)** Discriminar os serviços específicos do Windows alojados no interior de cada instância do processo partilhado `svchost.exe`.
* **C)** Forçar a paragem forçada de qualquer serviço em estado *Pending*.
* **D)** Gravar o registo de serviços num ficheiro de auditoria em `%WINDIR%\System32`.

---

## 3. Gabarito Comentado e Critérios de Correção

| Questão | Opção Correta | Fundamentação Técnica |
| :---: | :---: | :--- |
| **1** | **B** | O *Print Spooler* corre com os privilégios máximos de `LocalSystem`. Em máquinas que não sejam servidores de impressão (ex.: DC), deve ser desativado com `sc config Spooler start= disabled` (reparar no espaço obrigatório após o `=`). |
| **2** | **A** | O BITS é uma ferramenta legítima do SO usada para downloads em segundo plano. Atacantes utilizam-no para transferir payloads (LOLBin) e manter persistência através de tarefas agendadas armazenadas na base `qmgr.db`. |
| **3** | **C** | No utilitário `forfiles`, o prefixo `+` com um valor numérico refere-se a datas posteriores ou futuras em relação à data atual, sendo uma técnica padrão para identificar anomalias temporais (*timestomping* intencional). |
| **4** | **B** | O Windows 10 utilizava o motor ESE (*Extensible Storage Engine* - `Windows.edb`). O Windows 11 migrou para **SQLite3** (`Windows.db`), alterando a estrutura de um registo consolidado para uma estrutura normalizada de linhas/propriedades (`ColumnId`). |
| **5** | **B** | Em bases de dados SQLite com modo WAL (*Write-Ahead Logging*), as gravações mais recentes residem no ficheiro `*.db-wal` antes de serem consolidadas no ficheiro principal `*.db`. Ignorar o WAL resulta em perda imediata de evidências recentes. |
| **6** | **B** | Como dezenas de serviços partilham o mesmo binário `svchost.exe`, o comando simples `tasklist` apenas exibe o nome `svchost.exe`. O parâmetro `/svc` mapeia cada PID aos nomes dos serviços concretos hospedados naquela instância. |

---

## Navegação

- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses|Voltar ao Índice do Capítulo 1]]
- [[Serviços Windows]]
- [[svchost.exe]]
- [[Serviço BITS]]
- [[Windows Search]]
- [[Processos e linha de comandos no Windows]]
- [[Comando forfiles]]
