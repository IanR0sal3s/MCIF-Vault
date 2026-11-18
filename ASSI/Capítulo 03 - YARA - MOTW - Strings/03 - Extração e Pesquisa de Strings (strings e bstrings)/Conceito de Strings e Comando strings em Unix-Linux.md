---
title: Conceito de Strings e Comando strings em Unix-Linux
tipo: ferramenta
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 3
bloco: 3
fonte_aula: '"strings" utilities (Prof. Patrício Domingues)'
tags:
  - assi
  - forense
  - strings
  - linux
  - unix
  - codificacao
  - grep
aliases:
  - Comando strings
  - Unix strings
  - Conceito de Strings
  - strings -e S
atualizado: 2026-11-11
---

# Conceito de Strings e Comando `strings` em Unix/Linux

O comando Unix/Linux **`strings`** extrai sequências de caracteres imprimíveis de ficheiros de texto e binários para revelar contexto forense, suportando controlo de *offsets*, secções e codificações.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: Ficheiros binários compilados misturam código máquina com mensagens de erro, caminhos, URLs e nomes de funções; o `strings` varre o fluxo de bytes procurando sequências contíguas imprimíveis terminadas por um carácter não imprimível.
> * **Porque importa (Forense)**: Fornece contexto imediato na triagem de binários suspeitos e *malware* sem exigir engenharia inversa completa, sendo frequentemente combinado em *pipeline* (`strings file | grep ...`) para localizar indicadores de compromisso.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Comprimento mínimo padrão (`4`)**: sequências com menos de `4` caracteres são ignoradas por omissão (alterável com `-n`).
>   * **Acentos portugueses e codificação `-e`**: por omissão pesquisa apenas **ASCII 7 bits** (`-e s`); caracteres acentuados (`é`, `ç`, `ã`, `á`) têm o 8.º bit ativo e cortam as palavras a meio a menos que se passe **`-e S`** (*8-bit*).
>   * **Offsets em octal por omissão (`-o`)**: `-o` apresenta deslocamentos em **octal** (`433341` octal = `145121` decimal com `-t d`).
>   * **Limitação em ficheiros cifrados**: o `strings` **não produz resultados úteis com ficheiros cifrados**, pois os dados transformam-se em sequências pseudo-aleatórias sem texto legível.

---

## 1. Conceito de *String* e Contexto em Ficheiros Binários (Slide 2)

* **Definição de *String***: conjunto de caracteres imprimíveis consecutivos.
* **Ficheiros de Texto vs. Ficheiros Binários**:
  * **Ficheiros de texto**: são inteiramente compostos por *strings*, podendo a codificação variar (**[[Codificação de Caracteres - ASCII, Latin-1 e Unicode|ASCII, UTF-8, UTF-16]]**, etc.);
  * **Ficheiros binários (ex.: executáveis)**: embora compostos maioritariamente por código máquina, **também contêm *strings***.
* **Utilidade Forense**: num executável malicioso, as *strings* extraídas fornecem pistas valiosas sobre as **funções invocadas**, bibliotecas importadas, nomes de ficheiros e mensagens de estado.

**Exemplo ilustrado no Slide 2** (extração de *strings* de um binário relacionado com `bugreportz`):

```text
bugreport.zip
bugreportz -p
Bugreport is in progress and it could take minutes to complete.
Please be patient and do not cancel or disconnect your device until it completes.
bugreportz
[%3d%%] %s
```

---

## 2. O Comando `strings` em Unix/Linux: Uso Básico e `man strings(1)` (Slide 3)

### Uso simples

```bash
strings file
```

### Comprimento mínimo (`-n`)

* Define o comprimento mínimo de caracteres imprimíveis consecutivos para que uma sequência seja considerada uma *string*;
* **Por omissão, o valor predefinido no Unix é de `4` caracteres**.

#### Exemplo da aula (`strings -n 6 /bin/ls`)

```bash
strings -n 6 /bin/ls | more
```

Extrai de `/bin/ls` apenas *strings* com 6 ou mais caracteres, revelando o *dynamic linker* e as funções da biblioteca C invocadas pelo binário `ls`:

```text
/lib64/ld-linux-x86-64.so.2
_ITM_deregisterTMCloneTable
__gmon_start__
_ITM_registerTMCloneTable
fgetfilecon
freecon
lgetfilecon
fflush
strcpy
gmtime_r
__printf_chk
fnmatch
readdir
setlocale
mbrtowc
strncmp
optind
strrchr
fflush_unlocked
dcgettext
stpncpy
getpwuid
fputc_unlocked
closedir
```

### Sinopse Completa do `man strings(1)` (Slides 3 e 16)

```text
strings [-afovV] [-min-len]
        [-n min-len] [--bytes=min-len]
        [-t radix] [--radix=radix]
        [-e encoding] [--encoding=encoding]
        [-U method] [--unicode=method]
        [-] [--all] [--print-file-name]
        [-T bfdname] [--target=bfdname]
        [-w] [--include-all-whitespace]
        [-s] [--output-separator sep_string]
        [--help] [--version] file...
```

* Como descrito na `man page`, para cada ficheiro indicado, o GNU `strings` imprime as sequências de caracteres imprimíveis com pelo menos 4 caracteres (ou o número dado nas opções) seguidas por um carácter não imprimível. Consoante a configuração do `strings`, por omissão exibe todas as sequências imprimíveis encontradas ou apenas as que residem em secções de dados inicializados e carregáveis (*loadable, initialized data sections*).

---

## 3. Anatomia de Opções, *Offsets*, Secções e Separador (Slides 3–5)

### A. Anatomia de Opções Principais

| Opção | Argumento / Padrão | Função Operacional |
| :--- | :--- | :--- |
| **`-n`** / `--bytes=` | `min-len` (padrão: **`4`**) | Define o comprimento mínimo da sequência imprimível para ser considerada uma *string*. |
| **`-o`** | — | Mostra o *offset* (deslocamento no ficheiro) antes de cada *string* em base **octal**. |
| **`-t`** / `--radix=` | `d`, `o` ou `x` | Mostra o *offset* na base selecionada: **`d`** (decimal), **`o`** (octal) ou **`x`** (hexadecimal). |
| **`-d`** | — | Analisa exclusivamente as **secções de dados inicializados** do binário. |
| **`-s`** / `--output-separator` | `sep_string` | Substitui a mudança de linha predefinida pelo separador indicado. |
| **`-e`** / `--encoding=` | `s`, `S`, `b`, `l`, `B`, `L` | Seleciona a codificação: `s` (7-bit, padrão), `S` (8-bit), `b`/`l` (16-bit BE/LE), `B`/`L` (32-bit BE/LE). |

### B. Exemplos e Saídas Demonstradas na Aula (`-o`, `-t base`, `-d`, `-s` — Slide 4)

| Opção | Exemplo da Aula | Saída Demonstrada no Slide 4 |
| :--- | :--- | :--- |
| **`-o`** | `strings -o /bin/ls` | Offset em **octal** antes de cada *string*:<br>`433341 .rodata`<br>`433351 .eh_frame_hdr`<br>`433367 .eh_frame`<br>`433401 .init_array` |
| **`-t base`** | `strings -t d /bin/ls` | Offset na base numérica selecionada (**`d`** decimal, **`o`** octal, **`x`** hexadecimal — ver [[Sistemas de Numeração e Conversão entre Bases]]). Saída com `-t d`:<br>`145121 .rodata` *(nota: $433341_8 = 145121_{10}$)*<br>`145129 .eh_frame_hdr`<br>`145143 .eh_frame`<br>`145153 .init_array` |
| **`-d`** | `strings -t d -d /bin/ls` | Exclusivamente secções de dados inicializados:<br>`122711 %s, %s, %s, %s,`<br>`122727 %s, %s, and others.`<br>`122752 General help using GNU software: <%s>`<br>`122848 Copyright %s %d Free Software Foundation, Inc.`<br>`122895 memory exhausted` |
| **`-s separator`** | `strings -s: file`<br>*(ou `-s\|`)* | Concatena os resultados na mesma linha com o separador indicado:<br>`121 .rodata\| 145129 .eh_frame_hdr\| 145143 .eh_frame\| ...` |

---

## 4. Codificações de Caracteres (`-e`) — Caso Prático com Acentos (Slide 5)

Os ficheiros podem utilizar diferentes codificações de caracteres (**[[Codificação de Caracteres - ASCII, Latin-1 e Unicode|ASCII 7 bits, ASCII 8 bits, UTF-8, UTF-16 BE/LE, UTF-32 BE/LE]]**, etc.). A opção **`-e`** especifica a codificação a procurar:

* **`s`**: caracteres de **7 bits** (ASCII padrão — valor por omissão);
* **`S`**: caracteres de **8 bits** (ex.: ISO-8859-1 / Latin-1 / bytes estendidos);
* **`b` / `l`**: UTF-16 (16-bit) Big-Endian (`b`) ou Little-Endian (`l`);
* **`B` / `L`**: UTF-32 (32-bit) Big-Endian (`B`) ou Little-Endian (`L`).

### Demonstração Prática da Aula (`teste.txt` com Acentuação Portuguesa)

Considere-se o ficheiro `teste.txt` com o seguinte conteúdo (`cat teste.txt`):

```text
isto é um teste
Uma palavra com acentuação.
A palavra perspicácia.
Ter-nos-á premiado com prémio da educação.
```

**1. Com `-e S` (`strings -eS teste.txt` — codificação de 8 bits):**

Reconhece todos os caracteres acentuados como imprimíveis, mantendo as 4 frases completas:

```text
isto é um teste
Uma palavra com acentuação.
A palavra perspicácia.
Ter-nos-á premiado com prémio da educação.
```

**2. Sem indicar codificação (`strings teste.txt` — assume 7 bits por omissão):**

Como os caracteres acentuados (`é`, `ç`, `ã`, `á`) têm o 8.º bit ativo, o `strings` trata-os como **não imprimíveis** (terminadores de string), cortando as palavras a meio e descartando fragmentos com menos de 4 caracteres (como `"ção."`):

```text
isto 
 um teste
Uma palavra com acentua
A palavra perspic
cia.
Ter-nos-
 premiado com pr
mio da educa
```

---

## 5. Combinação com `grep` e Limitação em Ficheiros Cifrados (Slide 6)

### Combinação com `grep`

Para procurar uma *string* ou conjunto de *strings* específico dentro de um ficheiro binário, canaliza-se a saída de `strings` para o comando `grep`:

```bash
strings file | grep ...
```

### Limitação do `strings` em Ficheiros Cifrados

> [!WARNING] Ficheiros Cifrados
> **O comando `strings` não produz resultados úteis com ficheiros cifrados**, uma vez que a cifragem transforma os dados numa sequência pseudo-aleatória sem as *strings* originais em texto claro.

---

## Além da aula

* **Ligação direta com o Capítulo 3 de [[00 AFD1|AFD1]]**:
  * O exemplo de `strings -o` (`433341` em octal) vs. `strings -t d` (`145121` em decimal) ilustra na prática a importância de dominar [[Sistemas de Numeração e Conversão entre Bases]] para localizar um *offset* num editor hexadecimal;
  * O corte das palavras `"acentuação"` ($\to$ `"acentua"`) e `"perspicácia"` ($\to$ `"perspic"` / `"cia."`) quando se omite `-e S` deve-se exatamente ao facto de o padrão ASCII clássico ser de **7 bits** (`0x00` a `0x7F`), enquanto os caracteres acentuados em **Latin-1 (`ISO-8859-1`)** ou **UTF-8** utilizam bytes $\ge \text{0x80}$ (8.º bit a `1`), conforme estudado em [[Codificação de Caracteres - ASCII, Latin-1 e Unicode]].

---

## Perguntas de revisão

1. **O que é uma *string*, qual é o comprimento mínimo considerado por omissão no Unix `strings` e que opção altera esse limiar?**

> [!success]- Ver Resposta
> Uma *string* é um conjunto de caracteres imprimíveis consecutivos. Por omissão, o comando Unix `strings` exige um comprimento mínimo de **`4` caracteres** (terminado por um carácter não imprimível), podendo este limite ser alterado através da opção **`-n`** (ou `--bytes=min-len`, ex.: `strings -n 6 /bin/ls`).

2. **Compare o comportamento das opções `-o`, `-t d/o/x`, `-d` e `-s` no comando `strings`.**

> [!success]- Ver Resposta
> * **`-o`**: exibe o deslocamento (*offset*) antes de cada string em **octal** (ex.: `433341 .rodata`).
> * **`-t base`**: exibe o *offset* na base escolhida (`d` decimal, `o` octal, `x` hexadecimal — ex.: `strings -t d /bin/ls` devolve `145121 .rodata`, equivalente a $433341_8$).
> * **`-d`**: restringe a análise apenas às secções de **dados inicializados** do binário.
> * **`-s sep`**: substitui a mudança de linha por um **separador** personalizado (ex.: `-s:` ou `-s|`).

3. **Porque é que `strings teste.txt` corta palavras portuguesas acentuadas (`acentuação`, `perspicácia`) e que parâmetro resolve o problema?**

> [!success]- Ver Resposta
> Porque, sem indicar codificação, o `strings` assume ASCII de **7 bits (`-e s`)**. Os caracteres acentuados (`é`, `ç`, `ã`, `á`) possuem o 8.º bit ativo ($\ge \text{0x80}$), sendo interpretados como bytes não imprimíveis (terminadores de *string*) e descartando fragmentos abaixo de 4 caracteres (como `"ção."`). Passar **`-e S`** (codificação de 8 bits) corrige a extração.

4. **Qual é o padrão de uso com `grep` na análise de binários e em que tipo de ficheiros o comando `strings` falha em produzir resultados úteis?**

> [!success]- Ver Resposta
> Canaliza-se a saída para o `grep` (`strings file | grep ...`) para filtrar padrões específicos dentro de ficheiros binários. Contudo, o `strings` **não produz resultados úteis com ficheiros cifrados** (nem com conteúdo comprimido/empacotado de alta entropia), pois os bytes tornam-se pseudo-aleatórios sem texto claro legível.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Exceções à MOTW (Ficheiros Compactados, 7-Zip, certutil LOLBin) e Microsoft Defender SmartScreen]] | `Bloco 02` |
| **Seguinte** | [[Extração de Strings no Windows - Sysinternals strings e Swiss File Knife (sfk)]] | `mesmo bloco` |
| **Índice** | [[Capítulo 3 - YARA - MOTW - Strings]] · [[00 ASSI]] | `Bloco 03` |

### Conceitos Relacionados

* [[Eric Zimmerman bstrings - Parâmetros, Expressões Regulares e Exercícios]] · `mesmo bloco`
* [[Codificação de Caracteres - ASCII, Latin-1 e Unicode]] · `AFD1 · Cap. 3`
* [[Sistemas de Numeração e Conversão entre Bases]] · `AFD1 · Cap. 3`
