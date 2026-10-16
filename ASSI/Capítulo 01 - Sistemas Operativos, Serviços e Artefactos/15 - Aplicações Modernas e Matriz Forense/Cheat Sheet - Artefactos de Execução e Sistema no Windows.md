---
title: Cheat Sheet - Artefactos de Execução e Sistema no Windows
tipo: cheatsheet
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 15
fonte_aula: Artefactos Windows OS (Prof. Patrício Domingues)
tags:
  - assi
  - windows
  - forense
  - cheatsheet
  - resumo
  - prefetch
  - srum
  - vss
  - amcache
  - shimcache
  - jumplists
  - lnk
aliases:
  - Cheat Sheet Artefactos Windows
  - Resumo de Artefactos de Execução
  - Guia de Bolso Artefactos Windows
  - Cheat Sheet Parte 2
atualizado: 2026-10-07
---

# Cheat Sheet — Artefactos de Execução e Sistema no Windows

> [!TIP] Finalidade desta Folha de Consulta Rápida
> Este documento condensa a totalidade dos caminhos físicos, formatos binários, assinaturas mágicas (*magic bytes*), linhas de tempo de gravação, sintaxes CLI e armadilhas periciais lecionadas nos 158 diapositivos da segunda metade do Capítulo 1 (*"Artefactos Windows OS"*). Serve de guia de bolso rápido para resolução de exames práticos, incidentes de DFIR e laboratórios.

---

## 1. Matriz Mestre de Artefactos de Execução, Presença e Atividade

| Artefacto Forense | Localização Física no Disco | Motor / Formato | O que PROVA | O que NÃO PROVA |
| :--- | :--- | :--- | :--- | :--- |
| **[[Volume Shadow Service (VSS) - Arquitetura e Funcionamento\|VSS (Shadow Copies)]]** | `C:\System Volume Information` | Blocos NTFS diferenciais (*Copy-on-Write*) | Existência de versões históricas de ficheiros e hives em pontos anteriores no tempo. | Não garante que todos os ficheiros antigos existam (purge automático por quota FIFO). |
| **[[Serviço Prefetch e SysMain - Arquitetura e Funcionamento\|Prefetch]]** | `%WINDIR%\Prefetch\*.pf` | Binário comprimido **`MAM`** (W10/11) ou **`SCCA`** (W8.1) | **Execução efetiva do binário**, contadores de execução e últimas 8 datas de arranque. | **Não identifica a conta de utilizador** (artefacto global do sistema gerido por SysMain). |
| **[[Application Compatibility e ShimCache (AppCompatCache)\|ShimCache (AppCompatCache)]]** | `HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\AppCompatCache` (gravado no hive `SYSTEM`) | Buffer circular binário de 1024 entradas | **Presença e existência** do executável no disco local, partilha de rede UNC ou pen USB. | **Não prova execução no Windows 10/11** (`InsertFlag` foi removida; campo `Executed` do parser não é confiável). |
| **[[AmCache - Arquitetura, Hives e Evolução para SQLite\|Amcache]]** | `%WINDIR%\AppCompat\Programs\Amcache.hve` (e SQLite3 no W11 `>25H2`) | *Hive* independente **`REGF`** / Base **SQLite 3** | Existência de programas, controladores, dispositivos PnP e o seu **hash SHA-1**. | **Não prova execução pelo utilizador** (instaladores geram entradas de binários auxiliares não corridos). |
| **[[Jump Lists - Arquitetura, AppIDs e Carving\|Jump Lists (Auto)]]** | `%APPDATA%\...\Recent\AutomaticDestinations\` | **Compound File Binary (CFB / OLE)** | Abertura interativa de documentos por uma aplicação (`AppID`); **persiste após desinstalação**. | Não prova leitura integral do conteúdo do ficheiro. |
| **[[Jump Lists - Arquitetura, AppIDs e Carving\|Jump Lists (Custom)]]** | `%APPDATA%\...\Recent\CustomDestinations\` | Fluxo sequencial binário com trailer `AB FB BF BA` | Ações e ficheiros geridos especificamente pela aplicação. | Não inclui ficheiros não suportados pela aplicação. |
| **[[Ficheiros LNK (Shell Links) - Metadados e Formato Binário\|Ficheiros LNK]]** | `%APPDATA%\Microsoft\Windows\Recent\` (máx. 149) | Binário **`[MS-SHLLINK]`** (Magic: `4C 00 00 00`) | Acesso voluntário a ficheiros; recupera MAC timestamps, Serial USB e MAC address da NIC. | A GUI do Windows esconde comandos maliciosos além de 256 carateres. |
| **[[Caches de Ícones e Miniaturas (IconCache e Thumbcache)\|Thumbcache]]** | `%LOCALAPPDATA%\Microsoft\Windows\Explorer\thumbcache_*.db` | Bases de dados proprietárias por resolução | Conteúdo visual e existência do ficheiro (recuperável mesmo após eliminação). | **Não prova que o utilizador viu a imagem** (o Explorer gera miniaturas automaticamente ao abrir a pasta). |
| **[[Windows Activity Timeline - Arquitetura e Base SQLite\|Timeline]]** | `%LOCALAPPDATA%\ConnectedDevicesPlatform\...\ActivitiesCache.db` | Base relacional **SQLite 3** (+ WAL) | Sequência temporal de tarefas e **conteúdo do Clipboard (Win+V)** durante 12 horas. | No Windows 11 a utilidade é muito reduzida (sem sincronização cloud e eventos mínimos). |
| **[[System Resource Usage Monitor (SRUM) - Arquitetura e Base ESE\|SRUM]]** | `%WINDIR%\system32\sru\SRUDB.dat` | **Extensible Storage Engine (ESE / JET Blue)** | Consumo de CPU, **bytes enviados/recebidos na rede** e energia ao longo de 30–60 dias. | Não regista os argumentos da linha de comandos dos executáveis. |
| **[[Artefacto Forense do Bloco de Notas (Notepad Windows 11)\|Notepad TabState]]** | `%LOCALAPPDATA%\Packages\Microsoft.WindowsNotepad_...\LocalState\TabState` | Binário `NP` em UTF-16LE com inteiros **`uLEB128`** | **Texto não guardado (*unsaved text*)** e separadores que sobreviveram a encerramentos forçados. | Não preserva ficheiros formalmente fechados sem guardar antes de fechar a app. |

---

## 2. Linha do Tempo do "Tempo de Ativação" ($T_0 \to \text{Shutdown}$)

```mermaid
flowchart LR
    T0["Momento da Execução<br/><b>T = 0</b>"] --> UA["<b>~ 3s</b><br/>UserAssist"]
    UA --> PF["<b>~ 10s</b><br/>Prefetch (.pf)"]
    PF --> SRUM["<b>~ 1h</b><br/>SRUM (Minuto 30)"]
    SRUM --> AMC["<b>Após Tarefa Agendada</b><br/>Amcache (schtasks 24h)"]
    AMC --> SC["<b>Após Reinício / Shutdown</b><br/>ShimCache (Flush da RAM)"]
```

* **Live Triage ($< 10\text{s}$)**: Apenas `UserAssist` em disco.
* **Após 10 segundos**: `Prefetch` comitado no disco pelo `svchost.exe (-s SysMain)`.
* **Durante a Sessão**: `SRUM` acumula em memória e descarrega a cada hora (minuto 30); `Amcache` aguarda a tarefa agendada; `ShimCache` reside **exclusivamente na memória RAM**.
* **Puxar a ficha da tomada (*Cold Pull*)**: A **ShimCache é perdida para a sessão ativa**; o SRUM perde a fração da última hora.

---

## 3. Dicionário Rápido de Assinaturas Mágicas e Formatos Binários

| Artefacto / Estrutura | Assinatura Mágica (*Magic Bytes*) | Formato / Codificação | Particularidade Forense |
| :--- | :---: | :--- | :--- |
| **Ficheiros LNK** | `4C 00 00 00` | ASCII `'L'` (4 bytes) | Identifica Shell Links binários (`[MS-SHLLINK]`). |
| **IconCache Clássica** | `57 69 6E 34` | ASCII `'Win4'` | Presente no offset `0x04` do `IconCache.db` legado. |
| **Notepad W11 TabState** | `4E 50` | ASCII `'NP'` | Ficheiros `{GUID}.bin` em `LocalState\TabState`. |
| **Jump Lists Customizadas** | Trailer: `AB FB BF BA` | Fluxo sequencial | Quatro últimos octetos usados para **File Carving** de Jump Lists apagadas. |
| **Prefetch (Windows 8.1)** | `53 43 43 41` | ASCII `'SCCA'` | Formato nativo não comprimido (versões 26/30). |
| **Prefetch (Windows 10/11)** | `4D 41 4D 04` | ASCII `'MAM\x04'` | Formato comprimido proprietário da Microsoft (requer descompressão com `PECmd`). |
| **Amcache.hve** | `72 65 67 66` | ASCII `'regf'` | Estrutura binária de hive do Windows NT Registry. |
| **Base SRUM (`SRUDB.dat`)** | `EF CD AB 89` | ESE Database File | Formato de base transacional JET Blue da Microsoft. |
| **Inteiros uLEB128** | Bit 7 = Flag de Continuação | Little-Endian 7-bit | Codifica comprimentos e índices variáveis (ex.: $301_{10} = \texttt{AD 02}$). |

---

## 4. Guia Rápido de Linha de Comandos (CLI Cheat Sheet)

### 1. Volume Shadow Service (VSS)
```cmd
REM Listar todas as cópias de sombra e caminhos de dispositivo
vssadmin.exe list shadows

REM Inspecionar quotas de armazenamento do VSS
vssadmin.exe list shadowstorage

REM Montar shadow copy nativamente via CMD (NUNCA ESQUECER A BARRA FINAL \)
mklink /d SHADOW.shortcut \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy2\

REM Montar em massa todas as cópias da unidade C: via VSCMount (Eric Zimmerman)
vscmount.exe --dl C --mp C:\DEMO

REM Conceder acesso forense à pasta protegida System Volume Information
icacls "C:\System Volume Information" /grant UTILIZADOR:F /t
REM Restaurar permissões originais após a extração
icacls "C:\System Volume Information" /remove UTILIZADOR /t
```

### 2. Prefetch e SysMain
```cmd
REM Desativação efetiva do Prefetch (o Registry não funciona no W10/W11)
sc config SysMain start=disabled
sc stop SysMain

REM Processamento forense em massa de ficheiros .pf com PECmd (Eric Zimmerman)
PECmd.exe -d "C:\Windows\Prefetch" --csv "C:\Temp\Prefetch_CSV"

REM Descompactar um ficheiro .pf individual de formato MAM para SCCA
PECmd.exe -f "C:\Windows\Prefetch\CMD.EXE-4A81B364.pf" -o "C:\Temp\Decompressed"
```

### 3. ShimCache e AmCache
```cmd
REM Exportar a chave de ShimCache do Registry em formato texto
reg export "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\AppCompatCache" C:\Temp\shim.txt

REM Processar a ShimCache do hive SYSTEM com AppCompatCacheParser
AppCompatCacheParser.exe --csv "C:\Temp\Shim_Export"

REM Processar o hive Amcache.hve gerando as 8 tabelas CSV com AmcacheParser
AmcacheParser.exe -i --csv "C:\Temp\Amcache_Export" -f "C:\Windows\AppCompat\Programs\Amcache.hve"
```

### 4. Jump Lists e Atalhos LNK
```cmd
REM Extrair Jump Lists automáticas e customizadas com JLECmd
JLECmd.exe -d "%APPDATA%\Microsoft\Windows\Recent\AutomaticDestinations" --csv "C:\Temp\JL_Export" --mp -q

REM Extrair metadados completos de ficheiros LNK da pasta Recent com LECmd
LECmd.exe -d "%APPDATA%\Microsoft\Windows\Recent" --csv "C:\Temp\LNK_Export" -q

REM Inspeção rápida de LNK individual em Python
lnkparse3 "C:\Users\user\Desktop\suspeito.lnk"
```

### 5. Caches Gráficas, Timeline e SRUM
```cmd
REM Extrair miniaturas da pasta Explorer para galeria HTML com Thumbcache Viewer
thumbcache_viewer_cmd.exe -o "C:\Temp\Thumb_Export" -w -d "%LOCALAPPDATA%\Microsoft\Windows\Explorer"

REM Exportar a Windows Activity Timeline para CSV com WxTCmd
WxTCmd.exe -f "C:\Users\user\AppData\Local\ConnectedDevicesPlatform\L.user\ActivitiesCache.db" --csv "C:\Temp\Timeline_CSV"

REM Exportar consumo de energia e aplicações do SRUM nativamente via Windows
powercfg.exe /srumutil

REM Processamento pericial avançado de SRUDB.dat com SrumECmd (Eric Zimmerman)
SrumECmd.exe -f "C:\Windows\System32\SRU\SRUDB.dat" --csv "C:\Temp\SRUM_Export"

REM Reparar base ESE corrompida (Dirty Shutdown) antes de processar
esentutl.exe /r sru /d
```

### 6. Bloco de Notas (Windows 11)
```cmd
REM Extrair texto não gravado dos separadores do Bloco de Notas para CSV e JSONL
notepad_parser.exe -f csv -o "C:\Temp\notepad_conteudo.csv"
```

---

## 5. "Top 7" Armadilhas Forenses da Parte 2 (Perguntas Clássicas de Exame)

> [!CAUTION] Os 7 Erros Mais Frequentes em Perícia de Artefactos do Windows
> 
> 1. **Tentar provar execução com ShimCache ou AmCache no Windows 10/11**: Ambos os artefactos provam apenas que o ficheiro **existiu no disco ou em pen USB**. Não provam que o código correu em memória/CPU.
> 2. **Acreditar que o Registry desativa o Prefetch**: Definir `EnablePrefetcher = 0` no Registry é inútil no Windows 10/11 porque a rotina interna do *kernel* `PfSvSuperfetchCheckAndEnable` força o valor de volta para `3`. Apenas desativar o serviço `SysMain` surte efeito.
> 3. **Presumir que o Prefetch identifica a conta de utilizador**: O Prefetch é um artefacto global do sistema. Prova a execução e o carimbo de data/hora, mas **não identifica que utilizador fez o logon**.
> 4. **Concluir que o suspeito viu uma imagem pelo `thumbcache_*.db`**: O Windows Explorer gera miniaturas de forma autónoma em segundo plano ao abrir a pasta contentora. A presença da miniatura não prova visualização consciente.
> 5. **Confiar na interface gráfica de propriedades de um atalho `.lnk`**: A caixa de diálogo da GUI apenas apresenta os primeiros **256 carateres**, enquanto o formato LNK aceita até **4096 carateres**, permitindo camuflar comandos maliciosos extensos em PowerShell.
> 6. **Esquecer a barra final `\` no comando `mklink /d`**: Criar uma ligação simbólica para um volume VSS com `mklink /d SHADOW.shortcut \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopyX` falha ou gera um atalho quebrado se a barra final (`\`) for omitida.
> 7. **Tentar analisar uma base ESE em *Dirty Shutdown* sem reparação**: Extrair um `SRUDB.dat` de um sistema desligado abruptamente sem correr previamente `esentutl.exe /r sru /d` resultará em erros de leitura e perda dos registos da última hora.

---

## 6. Mapeamento das Aulas Práticas (Fichas 3 a 10)

| Ficha Laboratorial | Tema Central | Ferramentas Forenses Empregue |
| :---: | :--- | :--- |
| **Ficha 3 VSS** | Volume Shadow Service e Snapshots | `vssadmin`, `mklink /d`, `VSCMount`, `ShadowCopyView` |
| **Ficha 04 Prefetch** | Serviço Prefetch e SysMain | `WinPrefetchView`, `PECmd`, `sigcheck`, API programática |
| **Ficha 05 Shim & AmCache** | Infraestrutura de Compatibilidade | `AppCompatCacheParser`, `AmcacheParser`, `RegRipper`, VirusTotal |
| **Ficha 06 Jumplists** | Jump Lists Automáticas e Customizadas | `JLECmd`, `JumpList Explorer`, `JumpListsView` |
| **Ficha 07 Thumbcache** | Caches Gráficas e Atalhos | `Thumbcache Viewer` (`thumbcache_viewer_cmd.exe`), Windows Search |
| **Ficha 08 Timeline** | Windows Activity Timeline | `WxTCmd`, `Clippy`, SQLite Browser |
| **Ficha 09 SRUM** | Métricas de Recursos e Tráfego | `SrumECmd`, `powercfg /srumutil`, `esentutl`, `ESE Database Viewer` |
| **Ficha 10 Notepad** | Bloco de Notas W11 e uLEB128 | `notepad_parser`, `Notepad-State-Library`, HxD |

---

## Navegação

- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses|Voltar ao Índice do Capítulo 1]]
- [[Cheat Sheet - Registry e Forense|Consultar a Cheat Sheet da Parte 1 (Registry e Hives)]]
- [[Matriz de Correlação Forense e Cronologia de Ativação dos Artefactos]]
- [[Artefacto Forense do Bloco de Notas (Notepad Windows 11)]]
- [[Codificação uLEB128 em Estruturas de Dados do Windows]]
