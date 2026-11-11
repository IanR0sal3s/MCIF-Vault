---
title: Cheat Sheet - YARA, MOTW e Extração de Strings
tipo: cheatsheet
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 3
bloco: 1
fonte_aula: YARA & LOKI; Microsoft's Mark Of The Web (MOTW); "strings" utilities
tags:
  - assi
  - forense
  - cheatsheet
  - resumo
  - yara
  - yara-x
  - loki
  - ads
  - motw
  - strings
  - bstrings
aliases:
  - Cheat Sheet Capítulo 3 ASSI
  - Cheat Sheet YARA MOTW Strings
  - Resumo YARA LOKI MOTW bstrings
atualizado: 2026-11-11
---

# Cheat Sheet — YARA, MOTW e Extração de Strings

Guia de consulta rápida do Capítulo 3 de ASSI, condensando regras e modificadores YARA/YARA-X, métodos do scanner LOKI/`Loki-RS`, manipulação de NTFS ADS, análise de `Zone.Identifier` (MOTW), exceções (`7-Zip`, `certutil`), SmartScreen, extração de strings (`strings`, `strings.exe`, `sfk`, `bstrings`) e armadilhas de exame.

> [!TIP] Finalidade desta Folha de Consulta Rápida
> Este documento sintetiza os **76 diapositivos** do Capítulo 3 (`35` de *YARA & LOKI* + `25` de *MOTW / ADS* + `16` de *"strings" utilities*), as referências laboratoriais das **Fichas 14 e 15** e todas as **13 notas atómicas** dos Blocos `01` a `03`. Serve de guia de bolso para revisão rápida, exame e triagem forense.

---

## 1. Bloco 01 — YARA, YARA-X (`yr`) e LOKI

### Anatomia Rápida de uma Regra YARA

O **YARA** (VirusTotal, lançado em **2013**, licença **BSD-3**, em *maintenance mode* desde **2025**) realiza deteção baseada em assinatura com resultado estritamente **binário** (positivo ou negativo), usando sintaxe inspirada em **C** (`{ ... }`, `//`, `/* ... */`) e **PERL** (`/.../`) ([[YARA - Introdução, Estrutura de Regras, Metadados e Condições]]):

```yara
rule nome_regra : tag_opcional {
    meta:       // Documentação apenas — NÃO interfere na avaliação booleana
        author = "Florian Roth"
        date = "2016-12-29"
        description = "..."
        hash1 = "9f918fb7..."
        TLP = "WHITE"
        threat_level = 3
        in_the_wild = true

    strings:    // Padrões em 3 formatos: texto ("..."), hex ({ ... }) ou regex (/.../)
        $a1 = "string" ascii wide fullword nocase
        $hex = { E2 34 ?? C8 A? FB }
        $re = /([0-9]{1,3}\.){3}[0-9]{1,3}/ wide ascii

    condition:  // Critério booleano (curto-circuito PE + tamanho + quantificadores)
        uint16(0) == 0x5a4d and filesize < 300KB and (any of $a* or 2 of ($hex, $re))
}
```

### Modificadores de Strings, Hexadecimal, Base64 e Regex Essenciais

| Tipo / Mecanismo | Sintaxe / Exemplo | Funcionamento Técnico e Regras de Exame ([[YARA - Tipos de Strings, Modificadores, Formato Hexadecimal, Base64 e Regex\|Tipos de Strings]]) |
| :--- | :--- | :--- |
| **`ascii`** *(padrão)* | `$s1 = "In.pdb" fullword ascii` | Procura texto com **1 byte por caracter** (comportamento predefinido se `wide` for omitido). |
| **`wide`** | `$s2 = "Self Process" wide` | Procura texto em **UTF-16 / Unicode** (**2 bytes por caracter**, intercalado com `0x00`, nativo da API Win32). |
| **`wide ascii`** | `$a1 = "string" ascii wide` | Procura **simultaneamente** a codificação Unicode (2 bytes) e ASCII (1 byte). |
| **`nocase`** | `$d1 = "evilsite1.com" nocase` | Desativa distinção entre maiúsculas e minúsculas (*case-insensitive*). |
| **`fullword`** | `$x2 = "taskdl.exe" fullword ascii` | Exige fronteiras de caracteres **não alfanuméricos** antes e depois da string (palavra inteira). |
| **`base64`** | `$a = "This program cannot" base64` | Gera e procura **3 permutações de alinhamento** (deslocamentos de `0`, `1` e `2` bytes nos grupos $3\times 8\text{ bits} = 4\times 6\text{ bits}$): `VGhpcyBwcm9ncmFtIGNhbm5vd`, `RoaXMgcHJvZ3JhbSBjYW5ub3`, `UaGlzIHByb2dyYW0gY2Fubm90` (ex. base `"Man"` `0x4d 0x61 0x6e` $\to$ `TWFu`). |
| **Hex *Wildcards*** | `{ E2 34 ?? C8 A? FB }` | **`??`** substitui **1 byte completo** (`00`–`FF`); **`A?`** fixa o 1.º *nibble* e aceita qualquer 2.º *nibble* (`A0`–`AF`). |
| **Hex *Jumps*** | `{ F4 23 [4-6] 62 B4 }` | **`[4-6]`** aceita salto variável de **4 a 6 octetos** arbitrários entre os padrões. |
| **Regex `/.../`** | `/md5: [0-9a-zA-Z]{32}/`<br>`/state: (on\|off)/` | Âncoras `^` (início) e `$` (fim); escape `\`; grupos `()`, alternância `\|`, classes `[]`, `\w`/`\W`, `\s`/`\S`, `\d`/`\D`; quantificadores `*` ($0+$), `+` ($1+$), `?` ($0$–$1$), `{n}`, `{n,}`, `{,m}`, `{n,m}`. |

### Regra de Ouro PE (`strings` vs. `condition`), `yara`/`yarac` e Alerta sobre LLMs

* **`strings { 4D 5A }` vs. `condition: uint16(0) == 0x5a4d`**:
  * Na secção **`strings:`**, `$mz = { 4D 5A }` (ou `"MZ"`) especifica os dois primeiros bytes de um executável Windows **na ordem literal do disco** (offset `0x00`: `4D 5A`);
  * Na secção **`condition:`**, **`uint16(0) == 0x5a4d`** lê um inteiro sem sinal de 16 bits no offset `0` em **Little-Endian**, invertendo `4D 5A` para **`0x5a4d`** ([[YARA - Introdução, Estrutura de Regras, Metadados e Condições]]).
* **Otimização por Curto-Circuito (`uint16(0)` + `filesize` + `N of them`)**:
  * Colocar **`uint16(0) == 0x5a4d and filesize < 300KB`** antes de **`4 of them`** (como em `GRIZZLY_STEPPE_Malware_1`) descarta ficheiros não-PE ou acima de 300 KB antes de pesquisar strings.
  * Outros padrões de condição da aula: posição exata (`$mz at 0` em `upx_packed`), intervalo de bytes (`$a in (0..100)` em `silent_banker2`, `$upx0 in (0..1024)` e `$upx1 in (0..1024)` em `upx_packed`), tuplos/grupos (`2 of ($domain1, $domain2, $domain3)` em `silent_banker`, `1 of ($x*) and 1 of ($s*) or 3 of ($op*)` em `WannaCry_Ransomware`).
* **Compilação e Execução (`yara` vs. `yarac`)** ([[Execução e Compilação no YARA (yara e yarac), Casos Reais (UPX, WannaCry) e LLMs]]):
  * Compilar uma vez com **`yarac rule.yar rule.yarac`** e correr em sistemas contínuos (firewalls, gateways de e-mail) com **`yara -C rule.yarac INPUT`** evita o *parsing* repetido das regras de texto.
  * Flags principais do `yara`: **`-r`** (recursivo), **`-n`** (negação — mostra ficheiros que **não** cumprem), **`-c`** (contagem de *matches*), **`-C`** (regras compiladas), **`-m`** (metadados), **`-s`** (strings e offsets exatos), **`-g`** (tags), **`-p N`** (*threads*), **`-f`** (*fast-scan*).
* **Alerta sobre Regras Geradas por LLMs (`T1055.002`)**: *"One needs to validate and test the rule!"* — no exemplo gerado por ChatGPT (`detect_T1055_002`), a condição `any of ($dll_name, $create_remote_thread_api, $open_process_api)` incluindo `$dll_name = "kernel32.dll"` dispararia em praticamente todos os executáveis legítimos do Windows.

### Comparação: YARA Clássico (v4.x) vs. YARA-X (`yr`)

| Característica | YARA Clássico (v4.x) | YARA-X (`https://virustotal.github.io/yara-x/`) |
| :--- | :--- | :--- |
| **Linguagem Base** | **C** (gestão manual de memória) | **Rust** (segurança nativa de memória — evita *buffer overflows* e *use-after-free*) |
| **Interface CLI** | Binários separados **`yara`** e **`yarac`** | Binário unificado **`yr`** (com suporte Python, Go, C/C++, JS/TS) |
| **Desempenho Regex** | Lento em expressões regulares complexas | **Otimizado** (sub-segundo em ficheiros grandes; usado em produção na VirusTotal) |
| **Diagnóstico de Erros** | Mensagens genéricas de compilação | **Apontadores exatos de linha, coluna e sugestões** |
| **Estado do Projeto** | ***Maintenance mode*** desde 2025 | **Desenvolvimento ativo e foco principal** |
| **Subcomandos `yr`** | — | **`scan`** (`--output-format json`), **`fmt`**, **`compile`**, **`dump`** (dados de módulos `pe`/`elf`/`dotnet`), **`deps`**, **`fix`**, **`completion`**, **`help`** ([[YARA-X (Reimplementação em Rust) e Ferramenta CLI yr\|Detalhes yr]]) |

### LOKI (Versão Python) e `Loki-RS` (Versão Rust — Ficha 14)

O **LOKI** (*Simple IOC and Incident Response Scanner*, de **Florian Roth / `@cyb3rops`**) analisa **ficheiros em disco** e **processos em memória RAM** (exige consola com privilégios de **Administrador**) cruzando **4 métodos de deteção**:

| # | Método de Deteção LOKI | Mecanismo Técnico | Ficheiro na `signature-base` |
| :---: | :--- | :--- | :--- |
| **1** | **File Name IOC** | Expressões regulares sobre **nomes de ficheiros e caminhos completos**. | `filename-iocs.txt` |
| **2** | **Yara Rule Check** | Assinaturas YARA sobre **dados no disco** e **memória de processos em execução**. | `*.yar` |
| **3** | **Hash Check** | Compara resumos **MD5, SHA1 e SHA256** de ficheiros com IOCs conhecidos. | `hash-iocs.txt`, `otx-hash-iocs.txt` |
| **4** | **C2 Back Connect Check** | Inspeciona conexões de rede ativas dos processos face a **IPs/domínios C2**. | `c2-iocs.txt` |

* **LOKI Python (`loki.py` / `loki.exe`)** ([[Scanner de IOCs LOKI (Versão Python) - Métodos de Deteção e Configuração]]):
  * Configuração em YAML com 3 secções: `rules:` (`yara_rules`), `targets:` (`files`, `processes: true`) e `verbosity:` (`info`/`error`/`debug`);
  * Lança no arranque o binário **`pe-sieve64.exe`** (`tools\pe-sieve64.exe`, de *hasherezade*) para detetar injeção de código, *process hollowing* e DLLs maliciosas em memória (`--nopesieve` desativa; `--pesieveshellc` ativa deteção de *shellcode*);
  * Se `signature-base` não existir ou estiver vazia (ou com `--update`), o **`LOKI UPGRADER`** descarrega automaticamente `signature-base` do GitHub; limite de tamanho padrão **`-s 5000`** KB ($\approx 5\text{ MB}$).
* **`Loki-RS` (`Neo23x0/Loki-RS`, Rust multi-thread — Ficha 14)** ([[Loki-RS (Versão Rust) - Compilação, Atualização e Parâmetros CLI]]):
  * **Compilação**: `cargo b --release`; **Atualização (separada do scanner)**: `loki-util.exe --update`; **Execução**: `loki.exe -f c:\PASTA` (atenção: se `-f` for omitido, analisa o **sistema inteiro** por omissão);
  * ***Scan Control***: `--no-procs`, `--no-fs`, `--no-archive` (ignora ZIPs), `--scan-hard-drives`, `--scan-all-drives`, **`--scan-all-files`** (varre todos os ficheiros independentemente do tipo/extensão);
  * ***Output Options***: `-l` / **`--no-log`**, `-j` / **`--no-jsonl`**, **`--no-html`**, **`-r host:port`** (envio remoto), `-p udp|tcp`, `--remote-format syslog|json`, `--no-tui`.

---

## 2. Bloco 02 — NTFS ADS (`$DATA`), WastedLocker, MOTW (`Zone.Identifier`) e SmartScreen

### Arquitetura NTFS (`$DATA`) e Tabela Rápida CMD vs. PowerShell

* **FAT vs. NTFS**: O sistema **FAT** suporta apenas `Attributes` + `Data` (fluxo único). O **NTFS** guarda os dados visíveis do ficheiro no atributo **`$DATA`** (fluxo principal sem nome `:$DATA`) e permite múltiplos fluxos ocultos (**Alternate Data Streams — ADS**).
* **Tamanho oculto e perda ao copiar**: O comando `dir` normal e o sumário de `dir /r` (`1 File(s) X bytes`) **não contabilizam** os bytes das ADS. Copiar um ficheiro NTFS para uma pen **FAT/FAT32** elimina silenciosamente todas as ADS (incluindo a MOTW).

| Operação sobre ADS | CMD / Sysinternals ([[Alternate Data Streams (ADS) no NTFS - Arquitetura, Manipulação em CMD e PowerShell\|Guia ADS]]) | PowerShell (`-Stream`) |
| :--- | :--- | :--- |
| **Criar ADS de texto** | `echo "dados para ADS" > exemplo.txt:exemploADS` | *(Redirecionar em CMD ou criar via GUI `ADS Manager`)* |
| **Ocultar executável (EXE) em ADS** | `type nc.exe > ficheiro.txt:nc.exe` | *(Cópia binária via CMD `type` ou botão `Load...` em GUI)* |
| **Listar todas as streams** | `dir /r` | `Get-Item -Path ficheiro -Stream *`<br>`Get-Item -Path FICHEIRO -Stream * \| Select-Object -Property Filename, Stream, Length` |
| **Ler conteúdo de uma ADS** | `more < NomeFicheiro:NomeADS` | `Get-Content -Path ficheiro -Stream Zone.Identifier` |
| **Apagar todas as ADS (e a MOTW)** | `streams.exe -d ficheiro_com_stream` *(Sysinternals — sem nativo no CMD)* | *(Ou botão `Delete` no `Alternate Data Stream Manager`)* |

### Ferramentas Gráficas e Caso de Estudo `WastedLocker` (2020)

* **Ferramentas GUI** ([[Ferramentas Gráficas de Análise de ADS e Caso de Estudo WastedLocker]]):
  * **`AlternateStreamView` (NirSoft)**: pesquisa recursivamente todas as ADS e mostra `Stream Name`, `Stream Size` (lógico), `Stream Allocated Size`, `File Created Time`, `File Modified Time` e **`Entry Modified`** (timestamp da entrada na MFT).
  * **`Alternate Data Stream Manager` (Dmitry Brant)**: exibe o fluxo principal `<unnamed>` e as ADS; oferece botões **`New`**, **`Rename`**, **`Delete`**, **`Load...`**, **`Export...`** e pré-visualização **`Text preview`** / **`Hex preview`**.
* **Cadeia de Ataque do Ransomware `WastedLocker` (2020 — 4 Passos)**:
  1. Copia um ficheiro legítimo (qualquer) de `Windows\System32` para **`%APPDATA%`** com **nome oculto e aleatório**;
  2. Oculta a *payload* do ransomware dentro de uma **ADS** desse ficheiro em `%APPDATA%`;
  3. Cria uma pasta em **`%TEMP%`** com cópias de **`WINMM.DLL`** e **`WINSAT.EXE`**;
  4. Usa a `WINMM.DLL` copiada (carregada pelo `WINSAT.EXE`) para **executar o ransomware diretamente a partir da ADS**, evitando deteção baseada em ficheiros.
* **Pista Forense `Entry Modified` na MFT**: Ao copiar um ficheiro antigo do `System32`, `File Created` e `File Modified` preservam as datas originais, mas anexar a ADS atualiza **`Entry Modified`** na MFT, revelando o instante exato da criação da stream oculta.

### Mark of the Web (`MOTW`), `Zone.Identifier`, Zonas `URLZONE_*` e Browsers

A **MOTW** (desde o **Windows XP SP2**) grava a proveniência do ficheiro na ADS `:Zone.Identifier:$DATA` no formato `[ZoneTransfer]\nZoneId=x`, sendo as permissões por zona configuradas em **`Internet Properties`** (`inetcpl.cpl` $\to$ `Security`) ([[Mark of the Web (MOTW) e Zone.Identifier - Formato, Zonas URLZONE e Verbosidade dos Browsers]]):

| `ZoneId` | Designação da Zona | Constante `URLZONE_*` | Significado e Nível de Confiança |
| :---: | :--- | :--- | :--- |
| *(Sem ID)* | *(Sem classificação)* | **`URLZONE_INVALID`** | Sem classificação de zona válida atribuída. |
| **`0`** | *My Computer* | **`URLZONE_LOCAL_MACHINE`** | **Máquina local** (ficheiros originados no próprio computador). |
| **`1`** | *Local Intranet Zone* | **`URLZONE_INTRANET`** | **Intranet** (rede local corporativa e partilhas internas). |
| **`2`** | *Trusted sites Zone* | **`URLZONE_TRUSTED`** | **Sítios confiáveis** (explicitamente assinalados como fidedignos). |
| **`3`** | *Internet Zone* | **`URLZONE_INTERNET`** | **Sítios web (não confiáveis)** — zona padrão aplicada aos downloads da Internet. |
| **`4`** | *Restricted Sites Zone* | **`URLZONE_UNTRUSTED`** | **Sítios NÃO confiáveis** (explicitamente restritos ou perigosos). |

* **Verbosidade dos Browsers**:
  * **Edge / IE / Chrome** (verbosos): registam `ZoneId=3`, `ReferrerUrl` e `HostUrl` completo (caso **ViaMichelin** na aula: imagem `.png` preservou `ReferrerUrl=https://www.google.com/` e `HostUrl=...&lat=39.74563&lon=-8.81203...` em Leiria).
  * **Brave** (privacidade): regista `ZoneId=3`, omite `ReferrerUrl` e substitui a origem por **`HostUrl=about:internet`**.
* **As 6 Propriedades da `Zone.Identifier`**: **`ZoneId`**, **`AppZoneId`**, **`HostIpAddress`**, **`HostUrl`**, **`LastWriterPackageFamilyName`** (identifica o pacote UWP/MSIX que gravou a stream) e **`ReferrerUrl`**.

### Exceções à MOTW e Microsoft Defender SmartScreen (Ficha 15)

| Vetor / Ferramenta | Comportamento face à MOTW (`Zone.Identifier`) | Implicação de Segurança / Forense ([[Exceções à MOTW (Ficheiros Compactados, 7-Zip, certutil LOLBin) e Microsoft Defender SmartScreen\|Exceções MOTW]]) |
| :--- | :--- | :--- |
| **Explorer (Nativo Windows)** | **Propaga** a `Zone.Identifier` de `.zip` para os ficheiros extraídos. | Mantém proteção de avisos / *Protected View* nos ficheiros extraídos. |
| **7-Zip (`7Z`)** | **Não propaga por omissão** (`Propagate Zone.Id stream = * No`). | Ficheiros extraídos de `.zip` Web ficam sem MOTW; configurar `Yes` ou `For Office files` em `Options` $\to$ `7-Zip`. |
| **`certutil.exe` (LOLBin)** | **Não acrescenta** MOTW no download (`-verifyctl -f` / `-urlcache -split -f`). | Binário nativo assinado abusado em *Living off the Land*; o Windows Defender bloqueia com `Access is denied.`. |
| **`curl` / `wget`** | **Não acrescentam** `Zone.Identifier` aos ficheiros descarregados. | Transferências via CLI deixam binários sem marca de origem Web. |
| **`streams.exe -d` / FAT32** | **Removem** todas as ADS existentes (incluindo `Zone.Identifier`). | Apagar streams limpa a proveniência Web e anula bloqueios baseados na MOTW. |

* **Microsoft Defender SmartScreen** (*Reputation-based system* no Windows 10/11): consulta uma base de dados na *cloud* avaliando **(1) o n.º de downloads** do ficheiro e **(2) a reputação do sítio web** de origem. Controlos em *Windows Security $\to$ Reputation-based protection*: **`Check apps and files`**, **`SmartScreen for Microsoft Edge`** e **`Phishing protection`**.

---

## 3. Bloco 03 — Extração e Pesquisa de Strings (`strings`, `strings.exe`, `sfk`, `bstrings`)

> [!IMPORTANT] Limitação Fundamental
> O comando `strings` **não produz resultados úteis com ficheiros cifrados** (os dados assemelham-se a ruído pseudoaleatório) nem extrai as strings originais de executáveis comprimidos com empacotadores como o **UPX** antes de serem descompactados.

| Ferramenta | Mín. Padrão | Codificação Padrão | Flags de Codificação e Offsets | Pesquisa, Filtros e Opções Críticas |
| :--- | :---: | :--- | :--- | :--- |
| **Unix/Linux `strings`** ([[Conceito de Strings e Comando strings em Unix-Linux\|Unix]]) | **`4`** (`-n`) | **ASCII 7-bit** (`-e s`) | **`-e S`** (8-bit: preserva acentos PT em `teste.txt`), `-e b`/`l` (UTF-16 BE/LE), `-e B`/`L` (UTF-32 BE/LE); **`-o`** (octal), **`-t d`/`o`/`x`** | **`-d`** (só secções de dados inicializados), **`-s`** (separador de saída), `strings file \| grep ...`. |
| **Sysinternals `strings.exe`** (`v2.54`) ([[Extração de Strings no Windows - Sysinternals strings e Swiss File Knife (sfk)\|Sysinternals]]) | **`3`** (`-n`) | **ANSI + Unicode** (ambas) | **`-a`** (só ASCII), **`-u`** (só Unicode), **`-o`** (offset), `-f <offset>` (início), `-b <bytes>` (bytes a varrer) | **`-s`** (recursivo em subdiretorias), **`-nobanner`** (suprime cabeçalho em scripts/pipes). |
| **Swiss File Knife (`sfk strings`)** ([[Extração de Strings no Windows - Sysinternals strings e Swiss File Knife (sfk)\|sfk]]) | Padrão `sfk` | Texto / binário | Extração e filtragem direta sem `grep` | **`+filter -+WORD`** (filtro interno); **`\| sfk filter -ls+WORD`** (`ls` = *line start*, início de linha). |
| **Zimmerman `bstrings`** (`v1.5.1.0`) ([[Eric Zimmerman bstrings - Parâmetros, Expressões Regulares e Exercícios\|bstrings]]) | **`3`** (`-m`)<br>+ máx. **`-x`** | **ASCII (`-a true`) + Unicode (`-u true`)** | `-a false` / `-u false`; `--ar` (`[\x20 -\x7E]`), `--ur` (`[\u0020-\u007E]`); **`-b`** *chunk* `1`–`1024` MB (padrão `512`) | **`-f`** (ficheiro) vs. **`-d`** (pasta recursiva); **`-o`** (gravar); **`-q`** (*quiet* sem header/totais) vs. **`-s`** (*really quiet* sem consola, acelera `-o`); **`--ls`** / **`--fs`**; **`--lr`** / **`--fr`**; **`-p`** (**27 regex**). |

### Padrões Integrados de Destaque no `bstrings -p` (`--lr <Name>`)

Ao executar **`bstrings -p`**, são listadas **27 expressões regulares integradas** invocáveis via **`--lr <Name>`**:

| Categoria | `Name` (`--lr <Name>`) | Alvo Forense Principal |
| :--- | :--- | :--- |
| **Sistema Windows & Rede** | **`reg_path`**, **`win_path`**, **`unc`**, **`sid`**, **`bitlocker`**, **`var_set`**, **`guid`**, **`ipv4`**, **`ipv6`**, **`mac`**, **`url3986`**, **`urlUser`** | Hives/chaves do Registry, caminhos locais/UNC, SIDs (`S-1-5-...`), chaves de recuperação BitLocker, variáveis (`OS=Windows_NT`), GUIDs, IPs, MACs e URLs RFC 3986. |
| **Criptomoedas & Dados** | **`bitcoin`**, **`monero`**, **`aeon`**, **`bytecoin`**, **`dashcoin`**, **`dashcoin2`**, **`fantomcoin`**, **`sumokoin`**, **`b64`**, **`email`**, **`cc`**, **`ssn`**, **`usPhone`**, **`xml`**, **`zip`** | Carteiras digitais (Bitcoin, Monero, etc.), cadeias Base64 válidas, e-mails, cartões de crédito, SSN/telefones EUA, etiquetas XML/HTML e códigos postais. |

---

## 4. Guia Rápido de Linha de Comandos (CLI Cheat Sheet)

### 1. YARA, `yarac` e YARA-X (`yr`)

```bash
# Compilar regras YARA uma vez e executar usando a versão compilada (-C)
yarac rule.yar rule.yarac
yara -C rule.yarac INPUT

# Varrimento recursivo (-r), contagem (-c), negação (-n), metadados/strings (-m -s)
yara exemplo.yara -r c:\windows
yara exemplo.yara -n -r DIRS_to_SEARCH
yara suspicious_strings.yar -c -r DIR
yara -m -s -r regra.yar amostras/

# YARA-X (yr): análise com saída JSON, formatação, compilação e inspeção de módulos
yr scan --output-format json regras.yar amostras/
yr fmt regras_malware.yar
yr compile regras.yar -o regras.yarc
yr dump amostra.exe
```

### 2. LOKI (Python) e `Loki-RS` (Rust)

```cmd
REM LOKI Python (consola Administrador): atualizar signature-base e varrer com limite 5000 KB
loki.py --update
loki.py -p C:\PastaSuspeita -s 5000 -l C:\Temp\loki.log

REM Loki-RS (Rust): compilar em modo release, atualizar IOCs/regras e varrer pasta
cargo b --release
loki-util.exe --update
loki.exe -f c:\PASTA

REM Loki-RS em triagem live sem escrever ficheiros locais, enviando JSON via TCP remoto
loki.exe --no-log --no-jsonl --no-html -r 192.168.1.10:514 -p tcp --remote-format json
```

### 3. NTFS ADS, MOTW (`Zone.Identifier`) e `certutil` LOLBin

```cmd
REM CMD: criar ADS, ocultar EXE numa ADS, listar streams (dir /r), ler e apagar ADS
echo "dados para ADS" > exemplo.txt:exemploADS
type nc.exe > ficheiro.txt:nc.exe
dir /r
more < NomeFicheiro:NomeADS
streams.exe -d ficheiro_com_stream

REM LOLBin: transferências via certutil.exe não criam MOTW (bloqueado por AV moderno)
certutil.exe -verifyctl -f URL
certutil.exe -urlcache -split -f URL
```

```powershell
# PowerShell: listar todas as streams de um ficheiro e ler a stream Zone.Identifier (MOTW)
Get-Item -Path FICHEIRO -Stream * | Select-Object -Property Filename, Stream, Length
Get-Content -Path FICHEIRO -Stream Zone.Identifier
```

### 4. Extração de Strings (`strings`, `strings.exe`, `sfk`, `bstrings`)

```bash
# Unix/Linux strings: comprimento mínimo 6, offset decimal em dados inicializados, 8-bit (acentos PT) e grep
strings -n 6 /bin/ls | more
strings -t d -d /bin/ls
strings -e S teste.txt
strings file | grep "padrao"
```

```cmd
REM Windows Sysinternals strings.exe (ANSI+Unicode por omissão, min=3) sem banner e recursivo
strings.exe -nobanner -s -n 4 C:\PastaAlvo

REM Swiss File Knife (sfk): filtro interno vs. filtro por início de linha (ls = line start)
sfk strings FILE +filter -+WORD
sfk strings FILE | sfk filter -ls+WORD

REM Eric Zimmerman bstrings: listar 27 regex (-p), intervalo [10..15] e pesquisa por padrões integrados
bstrings -p
bstrings -m 10 -x 15 -f FILE
bstrings -m 10 -f c:\windows\notepad.exe
bstrings --lr reg_path -f c:\windows\notepad.exe
bstrings --lr bitcoin -f c:\windows\notepad.exe
bstrings -d DIR --fs file_with_strings_to_search -s -o out.txt
```

---

## 5. "Top 8" Armadilhas Clássicas de Exame do Capítulo 3

> [!CAUTION] Os 8 Erros Mais Frequentes no Capítulo 3 de ASSI
>
> 1. **Trocar a ordem de bytes entre `strings:` (`4D 5A`) e `condition:` (`uint16(0) == 0x5a4d`)**: Na secção `strings:`, os bytes seguem a ordem exata no disco (`{ 4D 5A }` = `MZ`); já `uint16(0)` na `condition:` interpreta 2 bytes como inteiro **Little-Endian**, invertendo para **`0x5a4d`**.
> 2. **Omitir `wide` em regras YARA para Windows ou confiar sem testar em regras de LLMs**: Por omissão, o YARA procura apenas **ASCII** (1 byte), falhando strings UTF-16 (`wide`) típicas da API Win32; além disso, regras geradas por LLMs (como `T1055.002` com `any of ($dll_name, ...)` contendo `"kernel32.dll"`) produzem falsos positivos em quase todos os binários Windows — validar e testar sempre!
> 3. **Esquecer que `base64` procura 3 alinhamentos no YARA ou omitir `-f` no `Loki-RS`**: O modificador `base64` testa as **3 permutações** de deslocamento de bits (`0`, `1`, `2` bytes), não apenas uma; no **`loki.exe` (`Loki-RS`)**, omitir **`-f`** faz o scanner analisar o **sistema inteiro** por omissão (e em resposta *live* deve usar `--no-log --no-jsonl --no-html` + `-r` para evitar escrita local).
> 4. **Confiar no tamanho reportado pelo `dir` normal (ou sumário do `dir /r`) e copiar provas NTFS para FAT32**: O tamanho principal do ficheiro **não soma** os bytes escondidos em ADS (`dir /r` lista as streams à parte, mas o sumário conta apenas `:$DATA`), e copiar para um volume **FAT/FAT32** (ou correr `streams.exe -d`) apaga silenciosamente todas as ADS e a MOTW.
> 5. **Assumir que a ausência de `Zone.Identifier` prova origem local ou que todos os browsers registam o mesmo**: O **7-Zip** tem `Propagate Zone.Id stream = No` por omissão (ao contrário do descompactador nativo do Windows), e **`certutil`**, **`curl`** e **`wget`** não escrevem MOTW; adicionalmente, o **Brave** anonimiza `HostUrl=about:internet` sem `ReferrerUrl`, enquanto Edge/Chrome gravam URLs completos (até coordenadas GPS).
> 6. **Ignorar o campo `Entry Modified` da MFT perante táticas como o `WastedLocker`**: Copiar um binário legítimo do `System32` mantém os carimbos `File Created/Modified` antigos, mas injetar a *payload* numa ADS atualiza de imediato **`Entry Modified`** na MFT (visível no `AlternateStreamView`), denunciando a ocultação.
> 7. **Confundir o comportamento padrão de `strings` (Linux) com `strings.exe` / `bstrings` (Windows)**: O `strings` Unix usa tamanho mínimo **`4`**, procura apenas **ASCII 7-bit** (cortando palavras portuguesas acentuadas se faltar **`-e S`**) e imprime offsets em octal com `-o`; já `strings.exe` e `bstrings` usam mínimo **`3`** e pesquisam **ANSI + Unicode** por omissão. Nenhum deles extrai texto claro útil de **ficheiros cifrados** (nem de executáveis empacotados com **UPX** antes de `upx -d`).
> 8. **Trocar `-q` por `-s` ou `--ls` por `--lr` no `bstrings` (e `-ls+WORD` no `sfk`)**: No `bstrings`, **`-q`** omite apenas cabeçalho e total de *hits*, enquanto **`-s`** desativa a saída na consola para acelerar a gravação com **`-o`**; **`--ls`** procura texto literal e **`--lr`** aplica uma regex (incluindo os 27 nomes do `bstrings -p` como `reg_path` ou `bitcoin`). No `sfk`, `-ls+WORD` significa ***line start*** (linhas começadas por `WORD`).

---

## Navegação

- [[Capítulo 3 - YARA - MOTW - Strings|Voltar ao Índice do Capítulo 3]]
- [[Cheat Sheet - Registry e Forense|Consultar Cheat Sheet Cap. 1 Parte 1 (Registry)]]
- [[Cheat Sheet - Artefactos de Execução e Sistema no Windows|Consultar Cheat Sheet Cap. 1 Parte 2 (Artefactos Windows)]]
- [[Cheat Sheet - Administração de Sistemas e Controlo de Acessos|Consultar Cheat Sheet Cap. 2 (Administração de Sistemas)]]
- [[YARA - Introdução, Estrutura de Regras, Metadados e Condições]]
- [[YARA - Tipos de Strings, Modificadores, Formato Hexadecimal, Base64 e Regex]]
- [[Execução e Compilação no YARA (yara e yarac), Casos Reais (UPX, WannaCry) e LLMs]]
- [[YARA-X (Reimplementação em Rust) e Ferramenta CLI yr]]
- [[Scanner de IOCs LOKI (Versão Python) - Métodos de Deteção e Configuração]]
- [[Loki-RS (Versão Rust) - Compilação, Atualização e Parâmetros CLI]]
- [[Alternate Data Streams (ADS) no NTFS - Arquitetura, Manipulação em CMD e PowerShell]]
- [[Ferramentas Gráficas de Análise de ADS e Caso de Estudo WastedLocker]]
- [[Mark of the Web (MOTW) e Zone.Identifier - Formato, Zonas URLZONE e Verbosidade dos Browsers]]
- [[Exceções à MOTW (Ficheiros Compactados, 7-Zip, certutil LOLBin) e Microsoft Defender SmartScreen]]
- [[Conceito de Strings e Comando strings em Unix-Linux]]
- [[Extração de Strings no Windows - Sysinternals strings e Swiss File Knife (sfk)]]
- [[Eric Zimmerman bstrings - Parâmetros, Expressões Regulares e Exercícios]]
