---
title: Ficha Prática e Questionário — Shell, Atividade e Matriz Forense
tipo: exercicio
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 15
fonte_aula: Artefactos Windows OS (Prof. Patrício Domingues)
tags:
  - assi
  - windows
  - lnk
  - jumplists
  - srum
  - notepad
  - uleb128
  - correlacao
  - lab
  - questionario
aliases:
  - Ficha Prática 04
  - Questionário Matriz Forense e Atividade
  - Lab Shell e Atividade
atualizado: 2026-10-13
---

# Ficha Prática e Questionário — Shell, Atividade e Matriz Forense

Guião prático de consolidação laboratorial e questionário de avaliação para os **Blocos 12 a 15** do Capítulo 1 (*Jump Lists, Ficheiros LNK, Caches Gráficas, Windows Timeline, SRUM, Bloco de Notas W11, uLEB128 e Matriz de Correlação — Fichas Laboratoriais 6 a 10*).

---

## 1. Guião Prático de Laboratório (Fichas 6 a 10)

### Exercício 1: Auditoria Pericial de Atalhos Maliciosos LNK (`LECmd`)
1. **Localização física dos ficheiros LNK recentes**:
   ```text
   %APPDATA%\Microsoft\Windows\Recent\
   ```
2. **Processar o atalho suspeito com o utilitário `LECmd` (Eric Zimmerman)**:
   ```cmd
   LECmd.exe -f "C:\Caminho\Fatura_Pendente.pdf.lnk"
   ```
   * *Campos Forenses Chave*:
     * **Header Signature**: Deve validar a assinatura binária `4C 00 00 00`.
     * **Link Target ID List**: Dados do volume de origem (número de série do volume, endereço MAC da placa de rede onde o LNK foi criado e carimbos temporais MAC).
     * **Command Line Arguments**: Extrai a totalidade dos argumentos para além dos 256 carateres visíveis na janela de propriedades da GUI (suportando até 4096 carateres).
     * **Extra Blocks**: Identificação de dados anexados ao final do ficheiro (*overlay data* extraídos por comandos como `findstr`).

---

### Exercício 2: Extração de Jump Lists e Carving (`JLECmd`)
1. **Diferença de caminhos e formatos**:
   * Listas Automáticas (`.automaticDestinations-ms`, contentor CFB/OLE `D0 CF 11 E0`): `%APPDATA%\Microsoft\Windows\Recent\AutomaticDestinations\`
   * Listas Customizadas (`.customDestinations-ms`, estruturas LNK sequenciais): `%APPDATA%\Microsoft\Windows\Recent\CustomDestinations\`
2. **Processar as Jump Lists em lote exportando para CSV**:
   ```cmd
   JLECmd.exe -d "%APPDATA%\Microsoft\Windows\Recent\AutomaticDestinations" --csv "C:\Forensics\JumpLists_Out"
   ```
3. **Carving de Jump Lists eliminadas**:
   * No editor hexadecimal (HxD), localizar ficheiros `.customDestinations-ms` em espaço não-alocado procurando pelo cabeçalho `02 00 00 00 01` (seguido de blocos LNK `4C 00 00 00`) e pelo marcador de fim (*trailer*) característico das Custom Jump Lists:
     ```text
     Cabeçalho: 02 00 00 00 01  |  Trailer final: AB FB BF BA
     ```

---

### Exercício 3: Quantificação de Exfiltração de Dados no SRUM (`SrumECmd`)
O **SRUM** (*System Resource Usage Monitor*) regista o consumo de CPU, dados de rede e bateria na base de dados ESE `C:\Windows\System32\sru\SRUDB.dat`.

1. **Reparação obrigatória em caso de encerramento não ordeiro (*Dirty Shutdown*)**:
   ```cmd
   esentutl.exe /r sru /d "C:\Forensics\SRU"
   ```
2. **Extração das métricas históricas de consumo com `SrumECmd`**:
   ```cmd
   SrumECmd.exe -f "C:\Forensics\SRUDB.dat" -r "C:\Forensics\SOFTWARE" --csv "C:\Forensics\SRUM_Export"
   ```
3. **Análise da tabela de tráfego de rede (`Network Data Usage`)**:
   * Abrir o ficheiro `NetworkUsages.csv`.
   * Filtrar pelo executável suspeito (ex.: `rclone.exe`, `curl.exe` ou malware).
   * Somar a coluna `BytesSent` para apurar matematicamente o **volume exato de dados exfiltrados** pela aplicação ao longo dos últimos 30 a 60 dias.

---

### Exercício 4: Recuperação de Texto Não Gravado no Bloco de Notas W11
Nas versões modernas do Windows 11, o Bloco de Notas preserva ficheiros de texto mesmo que o utilizador nunca tenha clicado em "Guardar".

1. **Localização física dos separadores ativos (*TabState*)**:
   ```text
   %LOCALAPPDATA%\Packages\Microsoft.WindowsNotepad_8wekyb3d8bbwe\LocalState\TabState\
   ```
2. **Inspeção dos ficheiros `{GUID}.bin` no HxD**:
   * **Assinatura binária inicial**: `4E 50` (ASCII: `NP`).
   * **Codificação dos dados**: Texto armazenado em formato **UTF-16LE** (dois bytes por caractere).
3. **Decodificação manual de inteiros com codificação `uLEB128`**:
   * Se o comprimento do texto estiver codificado como o par de bytes `AD 02`:
     1. Converter para binário: `AD = 10101101`, `02 = 00000010`.
     2. Descartar o bit mais significativo (MSB) de continuação de cada byte: `0101101` e `0000010`.
     3. Inverter a ordem (*Little-Endian*): `0000010` seguido de `0101101` $\to$ `00000100101101`.
     4. Converter para decimal: $256 + 32 + 8 + 4 + 1 = \mathbf{301}$ carateres.

---

## 2. Questionário de Avaliação e Cenários Forenses

### Questão 1 (A Armadilha Visual dos Atalhos LNK)
Um atacante do grupo APT10 enviou a uma empresa um atalho LNK malicioso. Quando o administrador de sistemas abriu a janela de propriedades do ficheiro no Windows Explorer, o campo "Target" mostrava apenas:
`C:\Windows\System32\cmd.exe`
No entanto, o clique no ficheiro provocou a descarrega e execução de um trojan em PowerShell. Qual é a vulnerabilidade explorada e como deve o perito extrair o comando real?
* **A)** A vulnerabilidade reside no facto de o Windows Explorer cortar o campo "Target" aos **256 carateres**, enquanto o formato binário LNK aceita **até 4096 carateres**; o atacante inseriu centenas de espaços em branco para esconder o script em PowerShell, que pode ser extraído na íntegra com a ferramenta `LECmd`.
* **B)** O atacante explorou uma falha zero-day no kernel do Windows que apaga as propriedades de ficheiros.
* **C)** O Windows Explorer não suporta atalhos criados em Linux.
* **D)** O comando só pode ser visualizado se a extensão do ficheiro for renomeada para `.bat`.

---

### Questão 2 (Carving de Jump Lists)
Numa investigação forense, o suspeito eliminou os ficheiros da pasta `%APPDATA%\Microsoft\Windows\Recent\CustomDestinations\` para destruir provas de tarefas e atalhos afixados (*pinned*). Que assinaturas hexadecimais de cabeçalho e de fecho (*trailer*) deve o perito utilizar no carving em espaço não-alocado para recuperar ficheiros `.customDestinations-ms` (que concatenam estruturas LNK `4C 00 00 00`)?
* **A)** `50 4B 03 04` (formato ZIP).
* **B)** Cabeçalho `02 00 00 00 01` (seguido de blocos LNK `4C 00 00 00`) e o trailer de fecho `AB FB BF BA`.
* **C)** `4E 50` (Bloco de Notas).
* **D)** `D0 CF 11 E0` (exclusivo dos contentores OLE/CFB das `AutomaticDestinations`, sem o trailer `AB FB BF BA`).

---

### Questão 3 (O Valor Probatório do Thumbcache)
Ao examinar a base de dados de miniaturas `thumbcache_256.db` do computador de um suspeito, o perito localiza miniaturas de fotografias comprometedoras. Qual das seguintes conclusões é a única **tecnicamente admissível** em tribunal?
* **A)** O perito pode afirmar que o suspeito abriu, visualizou e editou conscientemente cada uma daquelas imagens no ecrã.
* **B)** O perito pode afirmar que as imagens **existiram no sistema ou foram apresentadas numa pasta visualizada pelo Explorer**, mas a presença no `thumbcache` **não prova que o utilizador tenha aberto ou visualizado conscientemente o ficheiro individualmente**, pois o Explorer gera miniaturas de forma automática para todos os ficheiros da diretoria aberta.
* **C)** A miniatura prova que o utilizador descarregou os ficheiros diretamente através do Microsoft Edge.
* **D)** A presença na cache de miniaturas comprova a impressão física das fotografias.

---

### Questão 4 (Ciclo de Descarga e Persistência do SRUM)
O SRUM monitoriza continuamente a atividade dos processos no sistema. Se um analista forense estiver a investigar uma máquina suspeita e pretender analisar o tráfego gerado nos últimos 15 minutos, porque é que o ficheiro `SRUDB.dat` no disco pode não refletir esse consumo?
* **A)** Porque o SRUM apenas grava os dados no disco uma vez por dia às 00:00.
* **B)** Porque as métricas acumulam-se temporariamente em memória e no hive `SOFTWARE`, sendo descarregadas para o ficheiro físico `SRUDB.dat` num ciclo horário regular ao **minuto 30 de cada hora** e aquando do encerramento da máquina.
* **C)** Porque o SRUM só monitoriza placas de rede sem fios (Wi-Fi).
* **D)** Porque o ficheiro `SRUDB.dat` é volátil e desaparece após o reinício.

---

### Questão 5 (A Matriz de Cronologia de Ativação dos Artefactos)
Após a execução de um ficheiro executável malicioso num sistema Windows 11, qual é a **ordem cronológica correta** em que os artefactos comutam e persistem definitivamente os dados no disco rígido?
* **A)** ShimCache (imediato) $\to$ AmCache (10s) $\to$ Prefetch (1h) $\to$ SRUM (no shutdown).
* **B)** UserAssist ($\approx 3\text{ s}$) $\to$ Prefetch ($\approx 10\text{ s}$) $\to$ SRUM ($\approx 1\text{ h}$ / minuto 30) $\to$ AmCache (tarefa agendada $\approx 24\text{ h}$) $\to$ ShimCache (exclusivamente no encerramento/shutdown).
* **C)** Prefetch (no encerramento) $\to$ UserAssist (1h) $\to$ ShimCache (10s).
* **D)** Todos os artefactos são gravados em simultâneo no momento exato do clique ($T = 0$).

---

### Questão 6 (Decodificação de Dados em `uLEB128`)
O formato `uLEB128` (*Unsigned Little Endian Base 128*) é amplamente utilizado em estruturas internas do Windows (como no Bloco de Notas W11 e em componentes DWARF). Como se caracteriza matematicamente esta codificação?
* **A)** Cada número inteiro é codificado obrigatoriamente num bloco fixo de 8 bytes (64 bits).
* **B)** Cada byte utiliza 7 bits para armazenar dados e o bit mais significativo (MSB - bit 7) como indicador de continuação: se o MSB for `1`, significa que o número continua no byte seguinte; se for `0`, representa o byte final.
* **C)** É uma cifra de substituição idêntica ao ROT13.
* **D)** É uma técnica de compressão exclusiva para formatos de imagem PNG.

---

### Questão 7 (A Armadilha do *Dirty Shutdown* em Bases de Dados ESE)
Ao tentar abrir o ficheiro `SRUDB.dat` de um sistema desligado forçadamente com ferramentas que não suportam transações pendentes, a base devolve um erro de corrupção. Qual é o procedimento forense padrão para recuperar os dados com integridade?
* **A)** Eliminar os ficheiros de log e reconstruir a base no SQLite.
* **B)** Executar a ferramenta nativa `esentutl.exe /r sru /d` para efetuar a recuperação suave (*soft recovery*) aplicando as transações pendentes dos ficheiros de log (`sru*.log`) à base de dados.
* **C)** Converter a base de dados para formato texto através do PowerShell.
* **D)** Os dados de uma base em *dirty shutdown* são irrecuperáveis e devem ser descartados.

---

### Questão 8 (Sinergia no Vetor LNK da Campanha Emotet)
Na famosa cadeia de infeção do malware **Emotet**, os atacantes recorreram ao ficheiro de atalho LNK para iniciar a execução. Qual foi o mecanismo que permitiu ao atacante contornar o bloqueio de extensões executáveis e colocar código em execução sem descarregar um script externo adicional?
* **A)** O atalho LNK foi assinado digitalmente pelo Windows Update.
* **B)** O código malicioso em VBScript foi embutido no final do próprio ficheiro `.lnk` (*overlay data*) precedido por uma etiqueta de texto, e o atalho invocava o `cmd.exe` nativo com o utilitário `findstr` para extrair esse código para a pasta `%TEMP%` e executá-lo via `wscript.exe`.
* **C)** O ficheiro LNK transformou-se automaticamente num ficheiro `.exe` em memória.
* **D)** O Emotet utilizava o protocolo de transferência de ficheiros FTP embutido no Explorer.

---

## 3. Gabarito Comentado e Critérios de Correção

| Questão | Opção Correta | Fundamentação Técnica |
| :---: | :---: | :--- |
| **1** | **A** | A interface gráfica do Windows Explorer corta a caixa de texto de destino aos 256 carateres. A especificação binária suporta até 4096 carateres. O atacante coloca espaços para empurrar o payload em PowerShell para fora do campo visível. O `LECmd` descodifica a totalidade do comando. |
| **2** | **B** | Os ficheiros `.customDestinations-ms` organizam múltiplos fluxos `SHLLINK` (`4C 00 00 00`) de forma sequencial, iniciando com o cabeçalho `02 00 00 00 01` e encerrando com o trailer `AB FB BF BA` (já as `AutomaticDestinations` usam o contentor CFB/OLE `D0 CF 11 E0`). |
| **3** | **B** | As miniaturas são geradas automaticamente pelo Explorer para acelerar a experiência de navegação sempre que uma pasta que contenha ficheiros gráficos é aberta. A existência da miniatura não comprova que o utilizador tenha aberto ou visualizado a imagem individualmente. |
| **4** | **B** | O serviço DPS retém as métricas em RAM e no hive `SOFTWARE`, descarregando para o ficheiro físico `SRUDB.dat` apenas ao **minuto 30 de cada hora** e antes do encerramento regular do sistema. |
| **5** | **B** | Esta é a cronologia fundamental sistematizada na aula: $T_0 \to \text{UserAssist } (\approx 3\text{s}) \to \text{Prefetch } (\approx 10\text{s}) \to \text{SRUM } (\approx 1\text{h}) \to \text{AmCache } (\text{tarefa diária}) \to \text{ShimCache } (\text{apenas no shutdown})$. |
| **6** | **B** | O uLEB128 armazena números de tamanho variável em grupos de 7 bits, usando o 8.º bit (MSB) como bandeira de continuação (`1` continua, `0` termina). A ordem dos bytes é Little-Endian. |
| **7** | **B** | O motor ESE do Windows utiliza transações atómicas com Write-Ahead Logging. Se o computador for desligado subitamente, a base fica em estado de *Dirty Shutdown*. O comando `esentutl /r sru /d` aplica os logs em falta e coloca a base em estado *Clean Shutdown*. |
| **8** | **B** | O formato LNK ignora bytes excedentes além das estruturas declaradas nos cabeçalhos. O Emotet embutiu o script no próprio LNK e utilizou o utilitário nativo assinado `findstr` para o isolar e executar, constituindo um exemplo clássico de técnica LOLBin combinada. |

---

## Navegação

- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses|Voltar ao Índice do Capítulo 1]]
- [[Cheat Sheet - Artefactos de Execução e Sistema no Windows]]
- [[Matriz de Correlação Forense e Cronologia de Ativação dos Artefactos]]
- [[Ficheiros LNK (Shell Links) - Metadados e Formato Binário]]
- [[Abuso e Vetores de Ataque com Ficheiros LNK]]
- [[Jump Lists - Arquitetura, AppIDs e Carving]]
- [[Caches de Ícones e Miniaturas (IconCache e Thumbcache)]]
- [[Windows Activity Timeline - Arquitetura e Base SQLite]]
- [[System Resource Usage Monitor (SRUM) - Arquitetura e Base ESE]]
- [[Artefacto Forense do Bloco de Notas (Notepad Windows 11)]]
- [[Codificação uLEB128 em Estruturas de Dados do Windows]]
