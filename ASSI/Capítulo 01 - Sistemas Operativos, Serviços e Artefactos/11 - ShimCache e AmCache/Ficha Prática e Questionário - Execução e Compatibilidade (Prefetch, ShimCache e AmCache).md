---
title: Ficha Prática e Questionário — Execução e Compatibilidade (Prefetch, ShimCache e AmCache)
tipo: exercicio
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 11
fonte_aula: Artefactos Windows OS (Prof. Patrício Domingues)
tags:
  - assi
  - windows
  - prefetch
  - shimcache
  - amcache
  - vss
  - execucao
  - lab
  - questionario
aliases:
  - Ficha Prática 03
  - Questionário Execução e Compatibilidade
  - Lab Prefetch ShimCache AmCache
atualizado: 2026-10-13
---

# Ficha Prática e Questionário — Execução e Compatibilidade (Prefetch, ShimCache e AmCache)

Guião prático de consolidação laboratorial e questionário de avaliação para os **Blocos 09, 10 e 11** do Capítulo 1 (*Volume Shadow Service, Prefetch e SysMain, ShimCache e AmCache — Fichas Laboratoriais 3, 4 e 5*).

---

## 1. Guião Prático de Laboratório (Fichas 3, 4 e 5)

### Exercício 1: Extração de Ficheiros Bloqueados via VSS (Ficha 3 VSS)
Em sistemas ativos, ficheiros críticos como `Amcache.hve` e os hives do Registry estão bloqueados pelo kernel.

1. **Criar um snapshot do volume de sistema `C:` (PowerShell com privilégios de Administrador)**:
   ```powershell
   (Get-WmiObject -List Win32_ShadowCopy).Create("C:\", "ClientAccessible")
   ```
   *(Nota: o comando `vssadmin create shadow /for=C:` apenas está disponível em edições Windows Server).*
2. **Identificar o caminho do volume shadow**:
   ```cmd
   vssadmin list shadows
   REM Exemplo: \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1
   ```
3. **Criar uma ligação simbólica de diretório (*Symlink*) com barra final obrigatória**:
   ```cmd
   mklink /d C:\VSS_Mount \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\
   ```
4. **Extrair com sucesso os ficheiros previamente bloqueados**:
   ```cmd
   copy C:\VSS_Mount\Windows\AppCompat\Programs\Amcache.hve C:\Forensics\
   copy C:\VSS_Mount\Windows\System32\config\SYSTEM C:\Forensics\
   ```

---

### Exercício 2: Análise Forense de Prefetch com `PECmd` (Ficha 04 Prefetch)
O serviço **SysMain** cria ficheiros com extensão `.pf` comprimidos com o algoritmo proprietário **MAM** no Windows 10 e 11.

1. **Localização física dos ficheiros**: `%WINDIR%\Prefetch\*.pf`.
2. **Processar um ficheiro `.pf` individual com o utilitário `PECmd`**:
   ```cmd
   PECmd.exe -f "C:\Windows\Prefetch\CMD.EXE-A1B2C3D4.pf"
   ```
   * *Metadados Críticos*:
     * **Run Count**: Número total de vezes que o executável correu.
     * **Last Run**: Carimbos das últimas 8 execuções (no Windows 8.1+).
     * **Loaded Files**: Lista completa de ficheiros e DLLs carregadas nos primeiros 10 segundos de vida do processo.
3. **Processamento em lote exportando para CSV**:
   ```cmd
   PECmd.exe -d "C:\Windows\Prefetch" --csv "C:\Forensics\Prefetch_Export"
   ```

---

### Exercício 3: Extração da ShimCache com `AppCompatCacheParser` (Ficha 05)
1. **Localização lógica no hive `SYSTEM`**:
   ```text
   HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\AppCompatCache
   ```
2. **Execução da ferramenta `AppCompatCacheParser`**:
   ```cmd
   AppCompatCacheParser.exe -f "C:\Forensics\SYSTEM" --csv "C:\Forensics\Shim_Export"
   ```
3. **Análise pericial dos dados extraídos**:
   * Abrir o ficheiro CSV gerado.
   * Verificar a coluna `Path` (caminho completo do binário em disco, unidades USB ou partilhas UNC).
   * Inspecionar `LastModifiedTimeUTC`: corresponde à **data de modificação do ficheiro em disco** e **NÃO** ao momento em que entrou na cache.

---

### Exercício 4: Extração da AmCache e Triagem de Ameaças (Ficha 05)
1. **Processar o hive `Amcache.hve` com `AmcacheParser`**:
   ```cmd
   AmcacheParser.exe -f "C:\Forensics\Amcache.hve" -i --csv "C:\Forensics\Amcache_Export"
   ```
2. **Investigação direcionada em CSVs especializados**:
   * **`UnassociatedFileEntries.csv`**: Ficheiros executáveis autónomos que não pertencem a pacotes instalados oficialmente (local onde habitualmente residem ferramentas de ataque portáteis e malwares).
   * **Coluna `SHA1`**: Hash criptográfico de integridade do ficheiro.
3. **Validação contra bases de Threat Intelligence**:
   * Copiar o hash SHA-1 de uma entrada desconhecida e pesquisar na API ou interface do **VirusTotal**.

---

## 2. Questionário de Avaliação e Cenários Forenses

### Questão 1 (A Regra de Ouro de DFIR)
Num exame pericial de um ransomware em Windows 11, o analista encontra uma entrada para o executável `locker.exe` na ShimCache (`AppCompatCache`) e no `Amcache.hve`. O analista afirma no seu relatório que "o ransomware foi indiscutivelmente executado no computador". Esta conclusão é correta à luz das regras periciais?
* **A)** Sim, porque estar na ShimCache e na AmCache constitui prova material irrefutável de execução em qualquer versão do Windows.
* **B)** Não. Nos sistemas operativos modernos (Windows 10 e 11), a ShimCache e a AmCache provam apenas a **existência e presença** do ficheiro no disco; para provar execução real é obrigatório cruzar com Prefetch, UserAssist, SRUM ou Event Logs.
* **C)** Não, porque a AmCache apenas regista programas assinados digitalmente pela Microsoft.
* **D)** Sim, mas apenas se o ficheiro `locker.exe` estivesse localizado na pasta `%TEMP%`.

---

### Questão 2 (Armadilha de Resposta a Incidentes: Hard Power-Off)
Durante a apreensão de um computador portátil alvo de ataque, um técnico de suporte puxou o cabo de alimentação e retirou a bateria (*hard power-off*) para evitar a encriptação de ficheiros. Qual é o impacto direto desta ação na recuperação da **ShimCache** face ao **Prefetch**?
* **A)** A ShimCache e o Prefetch perdem ambos todos os dados da sessão.
* **B)** O Prefetch é destruído, mas a ShimCache mantém-se intacta porque é gravada no disco em tempo real a cada clique.
* **C)** A ShimCache em disco **não conterá os registos da sessão corrente**, porque os dados residiam na memória RAM do kernel e só seriam descarregados para o Registry no encerramento ordeiro; já o Prefetch preservará a execução de processos que tenham corrido há mais de 10 segundos.
* **D)** A perda da alimentação força a conversão imediata da ShimCache para formato SQLite.

---

### Questão 3 (A Falácia da Coluna `Executed`)
Ao analisar o relatório gerado pela ferramenta `AppCompatCacheParser` de Eric Zimmerman num sistema Windows 10, o investigador observa o valor `True` na coluna `Executed` para um binário suspeito. Pode esta coluna ser utilizada como prova definitiva de execução perante um tribunal?
* **A)** Sim, a coluna `Executed` é calculada através de uma chave criptográfica inviolável do kernel.
* **B)** Não. A `InsertFlag` foi formalmente removida no Windows 10/11; o campo `Executed` do parser baseia-se em heurísticas dos últimos 4 octetos (`01 00 00 00`) que não oferecem garantia judicial estrita.
* **C)** Sim, desde que o ficheiro tenha sido compilado em 64 bits.
* **D)** Não, porque o `AppCompatCacheParser` só suporta Windows XP.

---

### Questão 4 (Mito da Desativação do Prefetch via Registry)
Um administrador de sistemas tenta desativar o Prefetch definindo a chave `EnablePrefetcher = 0` no Registry do Windows 11. O que acontece na realidade após o reinício da máquina?
* **A)** O Prefetch é desativado com sucesso e todos os ficheiros `.pf` são eliminados.
* **B)** O sistema operativo entra em modo de recuperação.
* **C)** A rotina interna do *kernel* `PfSvSuperfetchCheckAndEnable` força o valor de volta para `3` se o serviço `SysMain` estiver em execução; a única forma eficaz de desativar o Prefetch é desativando o próprio serviço `SysMain`.
* **D)** O Prefetch passa a gravar exclusivamente em memória RAM.

---

### Questão 5 (Distinção de Falsos Gémeos: `sysmain.sdb` vs. `SysMain`)
Qual é a demarcação técnica exata entre o ficheiro `%WINDIR%\AppPatch\sysmain.sdb` e o serviço do sistema `SysMain`?
* **A)** São dois nomes para o mesmo componente de gestão de ficheiros comprimidos.
* **B)** `sysmain.sdb` é a base de dados de Shims (regras de retrocompatibilidade de aplicações); o serviço `SysMain` (antigo SuperFetch) gere a otimização de memória RAM e a escrita dos ficheiros do Prefetch.
* **C)** O serviço `SysMain` monitoriza conexões de rede e `sysmain.sdb` é a base de dados de firewall.
* **D)** `sysmain.sdb` é o ficheiro de arranque do UEFI Secure Boot.

---

### Questão 6 (Evolução Tecnológica da AmCache)
Qual das seguintes opções resume com rigor a evolução histórica dos ficheiros onde o sistema Windows armazena a AmCache?
* **A)** Windows XP (`Amcache.db`) $\to$ Windows 7 (`Amcache.hve`) $\to$ Windows 11 (`Amcache.xml`).
* **B)** Windows 7 (`RecentFileCache.bcf`) $\to$ Windows 8/10/11 inicial (`Amcache.hve` - hive REGF) $\to$ Windows 11 recente (>25H2) (Bases de dados relacionais **SQLite 3** como `DeviceCensus.db` e `InventoryApplicationFile.db`).
* **C)** O formato nunca sofreu alterações desde o Windows 2000, permanecendo sempre em ficheiros `.bcf`.
* **D)** A AmCache residiu sempre no hive `SYSTEM` conjuntamente com a ShimCache.

---

### Questão 7 (Cálculo de Hash do Prefetch em Processos Anfitriões)
No cálculo do hash de 8 caracteres hexadecimais que acompanha o nome de um ficheiro `.pf` (ex.: `SVCHOST.EXE-4327296F.pf`), que regra de exceção aplica o Windows aos processos anfitriões/encapsuladores (`svchost.exe`, `dllhost.exe`, `mmc.exe` e `rundll32.exe`)?
* **A)** O hash é gerado com base no nome do utilizador com sessão iniciada.
* **B)** O hash é calculado incluindo os argumentos da linha de comandos na fórmula matemática, gerando múltiplos ficheiros `.pf` distintos consoante os parâmetros; já nos restantes executáveis (incluindo `cmd.exe` e `powershell.exe`), o hash baseia-se unicamente no caminho absoluto do binário.
* **C)** O hash é omitido e substituído pelo PID do processo.
* **D)** O hash é o hash MD5 dos primeiros 512 bytes do binário.

---

### Questão 8 (Diferença Operacional entre ShimCache e AmCache)
Qual a principal razão técnica pela qual o `Amcache.hve` é mais valioso que a `ShimCache` para a identificação de binários de origem desconhecida ou ferramentas de ataque portáteis?
* **A)** Porque a ShimCache é limitada a 1024 entradas e não armazena hashes criptográficos, enquanto a AmCache preserva o **hash SHA-1** e metadados detalhados do cabeçalho PE (como fabricante, data de compilação e versão).
* **B)** Porque a ShimCache apenas funciona com software da Microsoft.
* **C)** Porque a AmCache regista os argumentos completos de execução da linha de comandos.
* **D)** Porque a ShimCache é apagada todos os dias à meia-noite pelo escalonador de tarefas.

---

## 3. Gabarito Comentado e Critérios de Correção

| Questão | Opção Correta | Fundamentação Técnica |
| :---: | :---: | :--- |
| **1** | **B** | No Windows 10 e 11, nem a ShimCache nem a AmCache provam execução. Apenas comprovam a presença do executável no disco (pode ter sido copiado por instalador, descompactado ou verificado pelo Defender). Provar execução exige Prefetch, UserAssist, SRUM ou logs 4688/Sysmon. |
| **2** | **C** | A ShimCache é mantida exclusivamente em **RAM (Kernel Space)** durante a sessão e só desce ao Registry no encerramento normal. Um desligamento forçado descarta as entradas da sessão em curso. O Prefetch é persistido em disco $\approx 10\text{ s}$ após o arranque do executável. |
| **3** | **B** | A `InsertFlag` foi eliminada nas compilações modernas do Windows. O campo `Executed` do `AppCompatCacheParser` é um indicador auxiliar não fiável, não devendo ser usado isoladamente como prova judicial de execução. |
| **4** | **C** | A rotina interna `PfSvSuperfetchCheckAndEnable` anula alterações no Registry forçando o valor para `3` se o serviço `SysMain` estiver ativo. Apenas parando e desativando o serviço `SysMain` se desliga o Prefetch. |
| **5** | **B** | Nomes quase iguais, mas sistemas independentes: `sysmain.sdb` é a base de dados de Shims (compatibilidade aplicacional); `SysMain` é o serviço de SuperFetch/Prefetch (gestão de RAM e arranque). |
| **6** | **B** | A evolução é: binário simples `RecentFileCache.bcf` no W7 $\to$ hive independente `Amcache.hve` do W8 ao W11 $\to$ migração para **SQLite 3** (`Inventory*.db`) nas versões mais recentes do Windows 11 (>25H2). |
| **7** | **B** | Para a generalidade dos programas (incluindo `cmd.exe` e `powershell.exe`), o hash do Prefetch baseia-se apenas no caminho do ficheiro. Mas para processos anfitriões (`svchost.exe`, `dllhost.exe`, `mmc.exe`, `rundll32.exe`), o Windows inclui os argumentos na função de hash, gerando ficheiros `.pf` separados por serviço/biblioteca. |
| **8** | **A** | A ShimCache tem limite circular de 1024 entradas e guarda apenas caminhos e timestamps de modificação. O AmCache guarda um inventário muito mais vasto com **Hashes SHA-1**, viabilizando triagem direta no VirusTotal. |

---

## Navegação

- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses|Voltar ao Índice do Capítulo 1]]
- [[Cheat Sheet - Artefactos de Execução e Sistema no Windows]]
- [[Application Compatibility e ShimCache (AppCompatCache)]]
- [[AmCache - Arquitetura, Hives e Evolução para SQLite]]
- [[Extração da AmCache e Comparação Forense com a ShimCache]]
- [[Mecanismos de Compatibilidade no Windows (WOW64, Shims, PCA, ShimCache e AmCache)]]
- [[Serviço Prefetch e SysMain - Arquitetura e Funcionamento]]
- [[Volume Shadow Service (VSS) - Arquitetura e Funcionamento]]
