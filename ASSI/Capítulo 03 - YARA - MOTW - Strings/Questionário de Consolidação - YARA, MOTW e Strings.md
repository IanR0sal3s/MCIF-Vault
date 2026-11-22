---
title: Questionário de Consolidação - YARA, MOTW e Strings
tipo: exercicio
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 3
fonte_aula: 01_MCIF_ASSI_1S2026-27_YARA+LOKI_PT_v1---ULO.pdf; 02_MCIF_ASSI_1s2026-27_MOTW_v1---ULO.pdf; 03_MCIF_ASSI_1S2026-27_strings_v1---ULO.pdf
tags:
  - assi
  - exercicio
  - questionario
  - revisao
  - yara
  - loki
  - motw
  - ads
  - strings
aliases:
  - Questionário Capítulo 3 ASSI
  - Revisão YARA MOTW Strings
atualizado: 2026-11-22
---

# Questionário de Consolidação — YARA, MOTW e Strings

Autoavaliação estilo exame (Grupo I — escolha múltipla + Grupo II — resposta aberta curta) para validar a compreensão dos **Blocos 01 a 03** do [[Capítulo 3 - YARA - MOTW - Strings]].

---

## Grupo I — Escolha Múltipla

### 1. YARA: `$mz = { 4D 5A }` vs. `uint16(0) == 0x5a4d`
Porque aparece `0x5a4d` na condição `uint16(0) == 0x5a4d` de uma regra YARA quando os dois primeiros bytes de um executável Windows são `4D 5A` (`MZ`)?
* **A)** Porque o YARA cifra automaticamente os primeiros 2 bytes em ROT13.
* **B)** Porque `uint16(0)` lê um inteiro sem sinal de 16 bits em **Little-Endian** (o byte `4D` no offset `0` é o menos significativo e `5A` o mais significativo), ao contrário de `{ 4D 5A }` em `strings:` que lê bytes sequencialmente.
* **C)** Porque `0x5a4d` identifica apenas ficheiros Linux ELF.
* **D)** Porque a secção `meta:` inverte os endereços antes da compilação.

### 2. Modificadores YARA (`wide`, `base64`, `fullword`)
Porque é que a declaração `$a = "This program cannot" base64` faz o YARA procurar **três** sequências Base64 distintas?
* **A)** Porque procura em ASCII, UTF-16 e UTF-32 em simultâneo.
* **B)** Porque o Base64 converte blocos de **3 octetos (24 bits)** em 4 caracteres de 6 bits; consoante o deslocamento inicial (`0`, `1` ou `2` bytes) no fluxo original, resultam 3 alinhamentos distintos.
* **C)** Porque o modificador `base64` ativa automaticamente `nocase` e `fullword`.
* **D)** Porque o YARA só aceita 3 strings por regra.

### 3. `yara` vs. `yarac` e Flags `-c` vs. `-C`
Qual a diferença entre `yara -c` e `yara -C` no YARA clássico?
* **A)** `-c` compila regras; `-C` limpa a cache.
* **B)** `-c` imprime apenas a **contagem** de correspondências por ficheiro; `-C` carrega ficheiros de **regras pré-compiladas** com `yarac`.
* **C)** `-c` ativa *case-sensitive*; `-C` nega a condição da regra.
* **D)** Ambas têm o mesmo efeito; apenas diferem entre Windows e Linux.

### 4. `YARA-X` (`yr`) e `Loki-RS`
Qual afirmação descreve corretamente o `YARA-X` e o `Loki-RS`?
* **A)** Ambos são reescritas em **Rust** visando maior desempenho e segurança de memória; o `YARA-X` unifica tudo na CLI **`yr`** (`yr scan`, `yr compile`, `yr fmt`) e o `Loki-RS` separa a atualização (`loki-util.exe --update`) do varrimento (`loki.exe`).
* **B)** O `YARA-X` é escrito em Python e substitui o `LOKI`.
* **C)** O `Loki-RS` grava apenas em memória RAM por omissão, nunca criando ficheiros locais.
* **D)** O `YARA` clássico (v4.x) é a única versão em desenvolvimento ativo pela VirusTotal.

### 5. Os 4 Métodos de Deteção do Scanner `LOKI`
Qual das opções lista corretamente os **4 métodos de deteção** do `LOKI`?
* **A)** Prefetch, ShimCache, AmCache e SRUM.
* **B)** **File Name IOC (Regex)**, **YARA Rule Check** (disco e memória), **Hash Check** (MD5/SHA1/SHA256) e **C2 Back Connect Check**.
* **C)** Port Scanning, Brute Force, Sniffing e Spoofing.
* **D)** Apenas regras YARA e verificação de assinaturas digitais Authenticode.

### 6. `Alternate Data Streams` (ADS) no NTFS vs. FAT
O que acontece às *Alternate Data Streams* (incluindo `Zone.Identifier`) quando um ficheiro é copiado de um volume **NTFS** para uma pen USB formatada em **FAT32**?
* **A)** São convertidas automaticamente em ficheiros `.txt` ocultos.
* **B)** São **eliminadas silenciosamente**, porque o sistema FAT suporta apenas um fluxo único de dados por ficheiro.
* **C)** São comprimidas num ficheiro `.zip` com a mesma `ZoneId`.
* **D)** O Windows recusa sempre a cópia de ficheiros com ADS para FAT32.

### 7. Ransomware `WastedLocker` e `AlternateStreamView`
No caso `WastedLocker` (2020), como ocultou e executou o atacante o *payload* usando ADS?
* **A)** Escondeu o *payload* numa ADS de um ficheiro legítimo copiado de `System32` para `%APPDATA%` e usou cópias de `WINMM.DLL` e `WINSAT.EXE` em `%TEMP%` para o executar diretamente a partir da ADS.
* **B)** Gravou o *payload* no ficheiro `hosts` e executou-o via `certutil`.
* **C)** Inseriu o *payload* na chave `ZoneId=4` do navegador Edge.
* **D)** Utilizou `streams.exe -d` para executar o binário em memória.

### 8. `Mark of the Web` (`Zone.Identifier`) — Edge vs. Brave
Ao inspecionar com `Get-Content -Path ficheiro -Stream Zone.Identifier` um ficheiro descarregado da Internet, qual a diferença entre o **Microsoft Edge** e o **Brave**?
* **A)** O Brave não cria a stream `Zone.Identifier`.
* **B)** O **Edge** é verboso (grava `ZoneId=3`, `ReferrerUrl` e `HostUrl` completos, podendo expor parâmetros/coordenadas); o **Brave** marca `ZoneId=3`, omite `ReferrerUrl` e anonimiza com `HostUrl=about:internet`.
* **C)** O Edge atribui `ZoneId=0` e o Brave atribui `ZoneId=4`.
* **D)** Ambos gravam exatamente os mesmos metadados.

### 9. Comando Unix `strings` e Acentuação Portuguesa
Porque corta `strings teste.txt` palavras portuguesas acentuadas (ex.: `acentuação` $\to$ `acentua`) e como corrigir?
* **A)** Porque o comprimento mínimo padrão é `10`; corrige-se com `-n 4`.
* **B)** Porque assume **ASCII 7 bits (`-e s`)** por omissão e trata bytes com o 8.º bit ativo como terminadores; corrige-se com **`strings -e S teste.txt`** (8 bits).
* **C)** Porque o ficheiro está cifrado; corrige-se com `-o`.
* **D)** Porque o `strings` do Linux só lê ficheiros UTF-16LE.

### 10. `bstrings` (Eric Zimmerman)
O que executa o comando `bstrings --lr reg_path -f C:\Windows\notepad.exe`?
* **A)** Procura a string literal `"reg_path"` no ficheiro `notepad.exe`.
* **B)** Aplica a **expressão regular integrada (`--lr`)** `reg_path` (listada via `bstrings -p`) para extrair caminhos do **Windows Registry** embutidos em `notepad.exe`.
* **C)** Lista as 27 expressões regulares integradas e grava-as em `notepad.exe`.
* **D)** Desativa a pesquisa Unicode e extrai apenas strings com menos de 3 caracteres.

---

## Grupo II — Resposta Aberta Curta

### 11. Porque é que um ficheiro extraído de um `.zip` descarregado da Internet pode surgir sem `MOTW` (7-Zip) e que implicação de segurança tem isso?
> [!success]- Ver Tópicos de Resposta
> O navegador grava `Zone.Identifier` (`ZoneId=3`) no arquivo `.zip`. Enquanto o descompactador nativo do Windows propaga a MOTW para os ficheiros extraídos, o **7-Zip por omissão NÃO propaga** (`Options` $\to$ `7-Zip` $\to$ `Propagate Zone.Id stream: No`, alterável para `Yes` ou `For Office files`). Sem MOTW, o Windows e o Office tratam os ficheiros extraídos (ex.: executáveis, `.lnk`, documentos com macros) como se fossem locais, contornando avisos de origem Web e *Protected View* (ficando dependentes apenas de camadas como SmartScreen/Defender).

### 12. Explique a diferença de comportamento padrão entre o `strings` do Unix/Linux e o `strings.exe` da Sysinternals, e porque ambos falham em ficheiros cifrados ou empacotados com UPX.
> [!success]- Ver Tópicos de Resposta
> * **Unix `strings` vs. Sysinternals `strings.exe`:** o Unix procura apenas **ASCII 7 bits** com comprimento mínimo de **`4`** caracteres por omissão; o Sysinternals procura **ANSI (ASCII) + Unicode (UTF-16)** em simultâneo com comprimento mínimo de **`3`** caracteres por omissão (além de suportar `-s` recursivo e `-nobanner`).
> * **Cifrados / UPX:** ficheiros cifrados ou comprimidos/empacotados (`UPX`, alta entropia $\approx 7.9\text{ bits/byte}$) transformam o texto original em sequências pseudo-aleatórias, pelo que o `strings` não recupera texto claro útil (no caso do `UPX`, é necessário detetar o empacotador — ex.: via regra YARA `upx_packed` — e descompactar antes de correr `strings`).

---

## Gabarito — Grupo I

| # | Resposta | Referência para Rever |
| :---: | :---: | :--- |
| **1** | **B** | [[YARA - Introdução, Estrutura de Regras, Metadados e Condições]] |
| **2** | **B** | [[YARA - Tipos de Strings, Modificadores, Formato Hexadecimal, Base64 e Regex]] |
| **3** | **B** | [[Execução e Compilação no YARA (yara e yarac), Casos Reais (UPX, WannaCry) e LLMs]] |
| **4** | **A** | [[YARA-X (Reimplementação em Rust) e Ferramenta CLI yr]] · [[Loki-RS (Versão Rust) - Compilação, Atualização e Parâmetros CLI]] |
| **5** | **B** | [[Scanner de IOCs LOKI (Versão Python) - Métodos de Deteção e Configuração]] |
| **6** | **B** | [[Alternate Data Streams (ADS) no NTFS - Arquitetura, Manipulação em CMD e PowerShell]] |
| **7** | **A** | [[Ferramentas Gráficas de Análise de ADS e Caso de Estudo WastedLocker]] |
| **8** | **B** | [[Mark of the Web (MOTW) e Zone.Identifier - Formato, Zonas URLZONE e Verbosidade dos Browsers]] |
| **9** | **B** | [[Conceito de Strings e Comando strings em Unix-Linux]] |
| **10** | **B** | [[Eric Zimmerman bstrings - Parâmetros, Expressões Regulares e Exercícios]] |

---

## Navegação

- [[Capítulo 3 - YARA - MOTW - Strings|Voltar ao MOC do Capítulo 3]]
- [[Cheat Sheet - YARA, MOTW e Extração de Strings|Consultar a Cheat Sheet do Capítulo 3]]
- [[00 ASSI|Voltar ao Índice Geral de ASSI]]
