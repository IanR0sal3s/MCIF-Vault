---
title: Ficha Prática e Questionário — Windows Registry e Artefactos Forenses
tipo: exercicio
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 5
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
tags:
  - assi
  - windows
  - registry
  - userassist
  - shellbags
  - usbstor
  - wow64
  - lab
  - questionario
aliases:
  - Ficha Prática 02
  - Questionário Registry e Forense
  - Lab Registry e Artefactos
atualizado: 2026-10-13
---

# Ficha Prática e Questionário — Windows Registry e Artefactos Forenses

Guião prático de consolidação laboratorial e questionário de avaliação para os **Blocos 05 a 08** do Capítulo 1 (*Fundamentos do Registry, Aplicações Modernas, Timestamps, Artefactos de Utilizador e Dispositivos USB*).

---

## 1. Guião Prático de Laboratório

### Exercício 1: Extração e Inspeção de Chaves via CLI
1. **Consultar chaves de arranque automático no Registry**:
   ```cmd
   reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /s
   reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /s
   ```
2. **Exportar a subchave de serviços em formato texto legível**:
   ```cmd
   reg export "HKLM\SYSTEM\CurrentControlSet\Services\Spooler" C:\Temp\Spooler_Config.reg /y
   ```

---

### Exercício 2: Análise da Arquitetura e o Nó `WOW6432Node`
1. **Verificar a visão dividida do Registry em sistemas de 64 bits**:
   ```cmd
   REM Consultar software instalado nativo (64 bits)
   reg query "HKLM\SOFTWARE" /k /f "Microsoft"
   
   REM Consultar software legado redirecionado (32 bits)
   reg query "HKLM\SOFTWARE\WOW6432Node" /k /f "Microsoft"
   ```
2. **Identificação da arquitetura de binários PE com `exiftool` e `trid`**:
   ```cmd
   exiftool.exe trid.exe | findstr /i "Machine PE"
   trid.exe executavel_suspeito.exe
   ```
   * *Verificação no cabeçalho binário (HxD)*: Inspecione o offset `+4` após a assinatura `PE\0\0`:
     * `4C 01` $\to$ `IMAGE_FILE_MACHINE_I386` (32 bits).
     * `64 86` $\to$ `IMAGE_FILE_MACHINE_AMD64` (64 bits).

---

### Exercício 3: Conversão e Cálculo de Marcas Temporais (Timestamps)
O Windows Registry utiliza predominantemente o formato **FILETIME** (inteiro de 64 bits que conta intervalos de 100 nanossegundos decorridos desde 1 de janeiro de 1601 UTC).

1. **Converter um valor FILETIME hexadecimal via linha de comandos**:
   ```cmd
   REM Converter FILETIME com w32tm
   w32tm /ntte 0x01db1f349c258000
   ```
2. **Fórmula de conversão para UNIX Epoch (segundos desde 1970)**:
   $$\text{Unix Timestamp} = \frac{\text{FILETIME} - 116444736000000000}{10000000}$$

---

### Exercício 4: Parsing do Artefacto `UserAssist` (ROT13 e Estrutura `Count`)
1. **Localizar a chave no *hive* do utilizador**:
   $$\texttt{HKCU\textbackslash Software\textbackslash Microsoft\textbackslash Windows\textbackslash CurrentVersion\textbackslash Explorer\textbackslash UserAssist\textbackslash\{GUID\}\textbackslash Count}$$
2. **Desofuscação manual**:
   * O nome do valor encontra-se cifrado com **ROT13** (ex.: `P:\Jvaqbjf\flfgrz32\pzq.rkr` $\to$ `C:\Windows\system32\cmd.exe`).
3. **Análise pericial da estrutura binária `Count` (72 bytes no Windows 10/11)**:
   * **Offsets 4 a 7 (DWORD)**: Contador de execuções (*Session Count*).
   * **Offsets 12 a 15 (DWORD)**: Duração do foco da aplicação (*Focus Time* em milissegundos).
   * **Offsets 60 a 67 (FILETIME)**: Carimbo de data/hora da última execução da aplicação.

---

### Exercício 5: Reconstituição de Navegação de Pastas com `ShellBags` (`SBECmd`)
1. **Localização física dos hives envolvidos**:
   * Pastas do sistema: `C:\Users\<User>\NTUSER.DAT` (`Software\Microsoft\Windows\Shell\Bags`).
   * Pastas e arquivos ZIP: `C:\Users\<User>\AppData\Local\Microsoft\Windows\UsrClass.dat` (`Local Settings\Software\Microsoft\Windows\Shell\Bags`).
2. **Processamento em lote com a ferramenta `SBECmd` (Eric Zimmerman)**:
   ```cmd
   SBECmd.exe -d "C:\Users\<User>\AppData\Local\Microsoft\Windows" --csv "C:\Forensics\ShellBags_Out"
   ```
   * *Objetivo*: Provar que o utilizador navegou visualmente numa pasta específica ou acedeu a um arquivo `.zip` ou `.rar`, mesmo após as pastas terem sido eliminadas do disco.

---

### Exercício 6: Investigação Pericial de Dispositivos USB (`USBSTOR`)
1. **Consultar dispositivos de armazenamento registados**:
   ```cmd
   reg query "HKLM\SYSTEM\CurrentControlSet\Enum\USBSTOR" /s
   ```
2. **Distinguir Número de Série Real vs. Windows Assigned ID**:
   * **Número de Série Real**: O segundo caractere do número de série **NÃO** contém o símbolo `&` (ex.: `001428573194`).
   * **Número Atribuído pelo Sistema Operativo**: Se o segundo caractere for `&` (ex.: `7&2b8c91&0`), o fabricante da pen USB não gravou um número de série único de fábrica; o Windows gerou um identificador baseado no barramento local.
3. **Validar a data da primeira inserção do dispositivo**: Inspecionar o ficheiro de log `%WINDIR%\inf\setupapi.dev.log` procurando pelo Vendor ID (`VEN_`) e Product ID (`PROD_`).

---

## 2. Questionário de Avaliação e Cenários Forenses

### Questão 1
Um perito forense está a realizar triagem em tempo real (*live triage*) numa máquina suspeita com Windows 11 de 64 bits. Para extrair as chaves do Registry, o perito executa uma ferramenta forense compilada em **32 bits**. Que erro metodológico grave irá ocorrer durante esta extração?
* **A)** A ferramenta irá causar um ecrã azul da morte (*BSOD*) devido a incompatibilidade de instruções de CPU.
* **B)** Devido ao redirecionamento automático do WOW64, as chamadas a `HKLM\Software` serão redirecionadas para `HKLM\Software\WOW6432Node`, deixando o perito cego a todas as chaves nativas de 64 bits.
* **C)** O Windows 11 bloqueia a execução de binários de 32 bits a menos que estejam assinados digitalmente pela Microsoft.
* **D)** A ferramenta não conseguirá abrir o hive `SYSTEM` porque o Configuration Manager do Windows bloqueia leituras em modo não-exclusivo.

---

### Questão 2
Ao analisar a subchave `UserAssist` de um utilizador no ficheiro `NTUSER.DAT`, o perito descobre uma entrada com o nome cifrado `HRX_Nppf_P:\GlcreCebwrpg\cnd.rkr`. Aplicando a cifra ROT13, que caminho executável e que significado tem o prefixo `UEM_` (ou `HRX_` cifrado)?
* **A)** `C:\HyperProject\paq.exe`; o prefixo indica um erro de inicialização gráfica do processo.
* **B)** `C:\HyperProject\paq.exe`; o prefixo `UEM_runpath` é o marcador do UserAssist que comprova que o executável foi lançado interativamente a partir da interface gráfica do Windows Explorer.
* **C)** `C:\Temp\malware.exe`; o prefixo indica que o executável residia numa partilha de rede UNC.
* **D)** `C:\Users\Public\script.ps1`; o prefixo indica execução via linha de comandos do PowerShell.

---

### Questão 3
Em relação à estrutura binária do `UserAssist` (bloco `Count` de 72 bytes no Windows 10/11), qual das seguintes afirmações sobre o valor do contador de execuções (*Run Count*) está correta?
* **A)** O contador de execuções inicia no valor `1` e é incrementado em uma unidade cada vez que o executável é lançado.
* **B)** O contador de execuções do UserAssist inicia no valor base `5` no Windows 7 e `0` no Windows 10, mas apenas contabiliza processos iniciados pela interface gráfica (GUI), ignorando scripts e executáveis lançados via terminal CLI (`cmd.exe`/`PowerShell`).
* **C)** O contador de execuções apenas regista processos que falharam no encerramento.
* **D)** O UserAssist não armazena contadores de execução, apenas o carimbo temporal da primeira abertura.

---

### Questão 4
Ao examinar a chave `HKLM\SYSTEM\CurrentControlSet\Enum\USBSTOR` numa investigação de fuga de informação, o analista depara-se com as seguintes instâncias de números de série para dois dispositivos amovíveis:
1. Dispositivo A: `0707297390184042`
2. Dispositivo B: `7&19a58b0&0`

Qual a conclusão técnica rigorosa a incluir no relatório pericial?
* **A)** O Dispositivo A e o Dispositivo B possuem ambos números de série únicos gravados pelo fabricante.
* **B)** O Dispositivo A possui um número de série de fábrica único e identificável; o Dispositivo B não possui número de série de fábrica, tendo o sistema atribuído um identificador temporário (indicado pelo `&` no 2.º caractere).
* **C)** O Dispositivo B foi inserido através de uma porta USB 3.0, daí a presença do símbolo `&`.
* **D)** O Dispositivo A é um disco virtual VHD e o Dispositivo B é uma pen drive física legítima.

---

### Questão 5
Qual o papel do artefacto **ShellBags** (`BagMRU` e `Bags`) na reconstituição da atividade humana num computador investigado?
* **A)** Provar que ficheiros executáveis foram lançados com privilégios de administrador.
* **B)** Reconstituir o histórico de navegação e visualização de pastas no Windows Explorer (incluindo dimensões de janela, modo de visualização e caminhos de pastas), mesmo que as pastas ou unidades externas já tenham sido eliminadas do disco.
* **C)** Registar as credenciais NTLM de utilizadores que acederam a pastas partilhadas na rede.
* **D)** Criar pontos de restauro automáticos no subsistema VSS sempre que uma nova pasta é criada.

---

### Questão 6
A partir da compilação **Windows 10 versão 1803**, a tarefa agendada `RegIdleBackup` deixou de criar cópias de segurança automáticas dos hives do Registry na pasta `C:\Windows\System32\config\RegBack\`. Qual foi a motivação de engenharia da Microsoft para esta alteração e qual o impacto para a resposta a incidentes?
* **A)** A pasta causava conflito com o antivírus; agora o perito deve usar o VSS (*Volume Shadow Copies*) para recuperar versões históricas dos hives.
* **B)** A Microsoft reduziu o espaço em disco ocupado pelo SO (os ficheiros passaram a apresentar tamanho de 0 bytes); para obter cópias históricas de hives sem VSS, o administrador tem de ativar explicitamente a flag `EnableRegistryBackup = 1`.
* **C)** O Registry passou a ser gravado em formato SQLite e não suporta cópias de segurança em disco.
* **D)** As opções A e B estão corretas e complementam-se.

---

### Questão 7
Aplicações modernas empacotadas no formato **MSIX** (como o Bloco de Notas no Windows 11) não gravam as suas configurações diretamente no hive `NTUSER.DAT` tradicional. Onde reside o registo virtualizado destas aplicações?
* **A)** Num ficheiro SQLite em `%APPDATA%\MSIX\database.db`.
* **B)** No contentor isolado da aplicação, especificamente no ficheiro de hive virtualizado `User.dat` localizado sob `%LOCALAPPDATA%\Packages\<PackageFamilyName>\SystemAppData\Helium\`.
* **C)** Na partição reservada de arranque UEFI.
* **D)** Diretamente na memória RAM, sendo destruído quando o processo termina.

---

### Questão 8
Qual é a fórmula de cálculo e a resolução temporal nativa do formato **FILETIME** utilizado pelo Windows para carimbos de data/hora no Registry e no sistema de ficheiros NTFS?
* **A)** Segundos decorridos desde 1 de janeiro de 1970 UTC com precisão de 1 segundo.
* **B)** Contagem de intervalos de **100 nanossegundos** decorridos desde **1 de janeiro de 1601 UTC**.
* **C)** Milissegundos decorridos desde o último arranque do sistema operativo (*System Uptime*).
* **D)** Número de dias decorridos desde o calendário juliano.

---

## 3. Gabarito Comentado e Critérios de Correção

| Questão | Opção Correta | Fundamentação Técnica |
| :---: | :---: | :--- |
| **1** | **B** | O subsistema **WOW64** intercepta chamadas de 32 bits e redireciona `HKLM\Software` para `WOW6432Node`. Se a ferramenta forense for de 32 bits e não usar a flag `KEY_WOW64_64KEY`, não consegue ver as chaves nativas de 64 bits do sistema. |
| **2** | **B** | O prefixo `UEM_runpath` é adicionado pela shell gráfica do Explorer para itens lançados através da barra de tarefas, menu Iniciar ou duplo clique. A cifra ROT13 de `U` é `H`, de `E` é `R`, e de `M` é `X`. O caminho real é `C:\HyperProject\paq.exe`. |
| **3** | **B** | O UserAssist apenas monitoriza o Windows Explorer (GUI). Execuções através de terminal `cmd.exe`, scripts `.bat` ou serviços de background **não são registadas no UserAssist**. |
| **4** | **B** | Se o 2.º caractere for `&`, o número de série foi gerado aleatoriamente pelo sistema operativo com base no barramento USB porque a pen não possuía número de série gravado no chip pelo fabricante. |
| **5** | **B** | As chaves `BagMRU` e `Bags` guardam preferências de visualização de cada pasta aberta. Como sobrevivem à eliminação das pastas, permitem ao perito provar a existência pretérita de diretórios confidenciais. |
| **6** | **D** | A pasta `RegBack` foi mantida com ficheiros de 0 bytes por razões de retrocompatibilidade de espaço em disco pós-1803. O perito deve recorrer a Shadow Copies (VSS) ou à ativação manual de `EnableRegistryBackup`. |
| **7** | **B** | A tecnologia de virtualização de registo para MSIX denomina-se **Helium**, residindo no ficheiro `User.dat` dentro da pasta `SystemAppData\Helium\` de cada pacote. |
| **8** | **B** | O FILETIME é um inteiro de 64 bits baseado em intervalos de 100 nanossegundos com época de referência fixada em **01/01/1601 UTC**. |

---

## Navegação

- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses|Voltar ao Índice do Capítulo 1]]
- [[Cheat Sheet - Registry e Forense]]
- [[Estrutura e Hives do Windows Registry]]
- [[Tipos de Dados e Associação de Ficheiros no Registry]]
- [[Ferramentas de Análise e Extração do Registry]]
- [[Arquitetura 32 vs 64 bits no Registry e Executáveis (WOW6432Node)]]
- [[Artefacto Forense UserAssist]]
- [[Artefacto Forense ShellBags]]
- [[Artefactos Forenses de Dispositivos USB]]
- [[Marcadores Temporais no Windows (Timestamps)]]
