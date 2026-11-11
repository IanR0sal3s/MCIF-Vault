---
title: Eric Zimmerman bstrings - Parâmetros, Expressões Regulares e Exercícios
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
  - bstrings
  - zimmerman
  - strings
  - regex
  - exercicio
aliases:
  - bstrings
  - Eric Zimmerman bstrings
  - bstrings -p
  - Exercise with bstrings
atualizado: 2026-11-11
---

# Eric Zimmerman `bstrings` — Parâmetros, Expressões Regulares e Exercícios

O **`bstrings`**, de **Eric Zimmerman**, automatiza a extração de *strings* ASCII e Unicode no Windows com limites mínimo e máximo, processamento por blocos e **27 expressões regulares forenses integradas**.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: Utilitários básicos como o `strings.exe` devolvem todo o texto legível sem filtragem semântica; o `bstrings` (`version 1.5.1.0`) integra pesquisa de *strings* literais (`--ls`/`--fs`), expressões regulares personalizadas ou integradas (`--lr`/`--fr`), limites mínimo/máximo e leitura por *chunks*.
> * **Porque importa (Forense)**: Em ficheiros executáveis, `pagefile.sys` ou dumps de memória RAM, extrai diretamente indicadores acionáveis — chaves **BitLocker**, endereços **Bitcoin/Monero**, caminhos do **Registry (`reg_path`)**, **SIDs**, **IPs** e **URLs** — reduzindo drasticamente o ruído.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **ASCII e Unicode ativos por omissão**: `-a` e `-u` têm valor padrão `true` (para desativar um deles, usar `-a false` ou `-u false`), com comprimento mínimo `-m 3` e máximo `-x` ilimitado.
>   * **Sufixos `--ls`/`--fs` vs. `--lr`/`--fr`**: `s` = *string* literal (`--ls` única, `--fs` ficheiro); `r` = *regex* (`--lr` única ou *built-in*, `--fr` ficheiro).
>   * **Desempenho com `-s` + `-o`**: `-q` (*Quiet mode*) suprime cabeçalho e total de *hits*; **`-s` (*Really Quiet mode*)** omite a saída na consola e **acelera o processamento quando combinado com `-o`**.
>   * **Blocos de memória (`-b`)**: intervalo válido de `1` a `1024` MB (padrão `512` MB).

---

## 1. Arquitetura e Todos os 17 Parâmetros do `bstrings` (Slide 11)

O utilitário **[bstrings (GitHub — Eric Zimmerman)](https://github.com/EricZimmerman/bstrings)** (`version 1.5.1.0`) oferece maior capacidade analítica do que o [[Extração de Strings no Windows - Sysinternals strings e Swiss File Knife (sfk)|strings.exe da Sysinternals]], agrupando as suas **17 opções de linha de comandos** em quatro eixos funcionais:

### A. Alvo e Filtros de Comprimento (`-f`, `-d`, `-m`, `-x`)

| Opção (`bstrings`) | Valor Padrão | Descrição Técnica Oficial (Slide 11) |
| :--- | :---: | :--- |
| **`f`** (`-f`) | — | **Ficheiro** a pesquisar (obrigatório especificar `-f` ou `-d`). |
| **`d`** (`-d`) | — | **Diretoria** a processar de forma recursiva (obrigatório especificar `-d` ou `-f`). |
| **`m`** (`-m`) | `3` | Comprimento **mínimo** da *string*. |
| **`x`** (`-x`) | Ilimitado | Comprimento **máximo** da *string*. |

### B. Pesquisa por Texto e Expressões Regulares (`--ls`, `--fs`, `--lr`, `--fr`, `-p`)

| Opção (`bstrings`) | Valor Padrão | Descrição Técnica Oficial (Slide 11) |
| :--- | :---: | :--- |
| **`ls`** (`--ls`) | — | ***String* a procurar**. Quando definido, apenas devolve as *strings* que contenham esse texto. |
| **`fs`** (`--fs`) | — | **Ficheiro contendo *strings* a procurar** (uma por linha). |
| **`lr`** (`--lr`) | — | **Regex a procurar** (expressão regular personalizada ou nome de uma *built-in regex*). Quando definido, apenas devolve *strings* que correspondam ao padrão. |
| **`fr`** (`--fr`) | — | **Ficheiro contendo padrões regex a procurar**. |
| **`p`** (`-p`) | — | **Exibe a lista de expressões regulares integradas** (*built-in*). |

### C. Codificações e Intervalos (`-a`, `-u`, `--ar`, `--ur`)

| Opção (`bstrings`) | Valor Padrão | Descrição Técnica Oficial (Slide 11) |
| :--- | :---: | :--- |
| **`a`** (`-a`) | `true` | Se ativo, procura *strings* **ASCII**. Usar **`-a false`** para desativar. |
| **`u`** (`-u`) | `true` | Se ativo, procura *strings* **Unicode**. Usar **`-u false`** para desativar. |
| **`ar`** (`--ar`) | `[\x20 -\x7E]` | Intervalo de caracteres a procurar em *strings* *'Code page'* (especificado em formato hex entre aspas). |
| **`ur`** (`--ur`) | `[\u0020-\u007E]` | Intervalo de caracteres a procurar em *strings* Unicode (especificado em formato hex entre aspas). |

### D. Controlo de Output e Desempenho (`-o`, `-q`, `-s`, `-b`)

| Opção (`bstrings`) | Valor Padrão | Descrição Técnica Oficial (Slide 11) |
| :--- | :---: | :--- |
| **`o`** (`-o`) | — | Ficheiro onde gravar os resultados. |
| **`q`** (`-q`) | `false` | *Quiet mode*: não mostra o cabeçalho nem o número total de *hits*. |
| **`s`** (`-s`) | `false` | *Really Quiet mode*: não exibe os *hits* na consola; **acelera o processamento quando usado em conjunto com `-o`**. |
| **`b`** (`-b`) | `512` (MB) | Tamanho do bloco (*Chunk size*) em MB (intervalo válido: `1` a `1024`). |

---

## 2. Exemplos de Sintaxe com o `bstrings` (Slide 12)

**1. Restringir comprimento mínimo (`-m 10`) e máximo (`-x 15`) simultaneamente:**

```cmd
bstrings -m 10 -x 15 -f FILE
```

* Devolve apenas as *strings* cujo comprimento seja $\ge 10$ caracteres **E** $\le 15$ caracteres (`length >= 10 chars && length <= 15`).

**2. Procurar uma *string* específica (`--ls`) dentro das *strings* extraídas:**

```cmd
bstrings -f FILE --ls StringToSearch
```

**3. Procurar múltiplas *strings* guardadas num ficheiro (`--fs`) recursivamente numa diretoria (`-d`):**

```cmd
bstrings -d DIR --fs file_with_strings_to_search
```

* Procura todas as *strings* listadas em `file_with_strings_to_search` dentro de todos os ficheiros da diretoria `DIR` (e respetivas subdiretorias).

**4. Procurar usando uma expressão regular integrada (`--lr`):**

```cmd
bstrings -f FILE --lr guid
```

* `--lr`: pesquisa dada uma *built-in REGEX* (neste caso, a regex integrada para identificar um **`guid`**).

**5. Procurar usando um ficheiro de expressões regulares (`--fr`):**

```cmd
bstrings -f FILE --fr file_with_regexes
```

---

## 3. Catálogo Completo das 27 Expressões Regulares Integradas (`bstrings -p` — Slides 13 e 14)

Ao executar **`bstrings -p`**, a ferramenta lista os **27 padrões de expressões regulares integrados** (*built-in REGEXes*). Para utilizar qualquer um destes padrões, basta fornecer o seu **`Name`** ao parâmetro **`--lr`** (*To use a built in pattern, supply the Name to the `--lr` switch*).

### A. Identificadores e Rede (8 padrões)

| `Name` (`--lr <Name>`) | `Description` Oficial (`bstrings -p`) | Significado e Contexto Forense |
| :--- | :--- | :--- |
| **`email`** | `Finds embedded email addresses` | Endereços de **e-mail** embutidos no ficheiro. |
| **`guid`** | `Finds GUIDs` | *Globally Unique Identifiers* (**GUIDs**). |
| **`ipv4`** | `Finds IP version 4 addresses` | Endereços de rede **IPv4**. |
| **`ipv6`** | `Finds IP version 6 addresses` | Endereços de rede **IPv6**. |
| **`mac`** | `Finds MAC addresses` | Endereços físicos **MAC** de interfaces de rede. |
| **`unc`** | `Finds UNC paths` | Caminhos de partilhas de rede **UNC** (`\\servidor\partilha`). |
| **`url3986`** | `Finds URLs according to RFC 3986` | Endereços Web (**URLs**) conformes à norma RFC 3986. |
| **`urlUser`** | `Finds usernames in URLs` | Nomes de utilizador embutidos em URLs. |

### B. Artefactos Windows e Codificações (7 padrões)

| `Name` (`--lr <Name>`) | `Description` Oficial (`bstrings -p`) | Significado e Contexto Forense |
| :--- | :--- | :--- |
| **`b64`** | `Finds valid formatted base 64 strings` | Cadeias formatadas em Base64 ([[Codificação Binário-para-Texto (Base16, Base64 e Base58)]]). |
| **`bitlocker`** | `Finds Bitlocker recovery keys` | Chaves de recuperação **BitLocker** (8 blocos de 6 dígitos). |
| **`reg_path`** | `Finds paths related to Registry hives` | Caminhos relacionados com hives do Windows Registry ([[Estrutura e Hives do Windows Registry]]). |
| **`sid`** | `Finds Microsoft Security Identifiers (SID)` | *Security Identifiers* (**SID**) de contas Microsoft (`S-1-5-...`). |
| **`var_set`** | `Finds environment variables being set (OS=Windows_NT)` | Definições de **variáveis de ambiente** (ex.: `OS=Windows_NT`). |
| **`win_path`** | `Finds Windows style paths (C:\folder1\folder2\file.txt)` | Caminhos de ficheiros no estilo Windows (`C:\...`). |
| **`xml`** | `Finds XML/HTML tags` | Etiquetas **XML / HTML**. |

### C. Criptomoedas e Dados Pessoais (12 padrões)

| `Name` (`--lr <Name>`) | `Description` Oficial (`bstrings -p`) | Significado e Contexto Forense |
| :--- | :--- | :--- |
| **`aeon`** | `Finds Aeon wallet addresses` | Endereços de carteiras da criptomoeda Aeon. |
| **`bitcoin`** | `Finds BitCoin wallet addresses` | Endereços de carteiras **Bitcoin** em Base58 ([[Codificação Binário-para-Texto (Base16, Base64 e Base58)]]). |
| **`bytecoin`** | `Finds ByteCoin wallet addresses` | Endereços de carteiras da criptomoeda ByteCoin. |
| **`dashcoin`** | `Finds DashCoin wallet addresses (D*)` | Endereços de carteiras DashCoin iniciados por `D`. |
| **`dashcoin2`** | `Finds DashCoin wallet addresses (7\|X)*` | Endereços de carteiras DashCoin iniciados por `7` ou `X`. |
| **`fantomcoin`** | `Finds Fantomcoin wallet addresses` | Endereços de carteiras da criptomoeda Fantomcoin. |
| **`monero`** | `Finds Monero wallet addresses` | Endereços de carteiras da criptomoeda **Monero**. |
| **`sumokoin`** | `Finds SumoKoin wallet addresses` | Endereços de carteiras da criptomoeda SumoKoin. |
| **`cc`** | `Finds credit card numbers` | Números de **cartões de crédito**. |
| **`ssn`** | `Finds US Social Security Numbers` | Números de Segurança Social dos EUA. |
| **`usPhone`** | `Finds US phone numbers` | Números de telefone dos EUA. |
| **`zip`** | `Finds zip codes` | Códigos postais dos EUA (*zip codes*). |

---

## 4. Exercício Prático de Aula (`Exercise with bstrings` — Slide 15)

### Enunciado e Explicação Detalhada dos Comandos

**1. Comando 1:**

```cmd
bstrings -m 10 -f c:\windows\notepad.exe
```

* **Explicação do output**: analisa o ficheiro executável `c:\windows\notepad.exe` (`-f`) e extrai todas as *strings* (quer ASCII, quer Unicode, pois `-a` e `-u` são `true` por omissão) cujo comprimento seja de **pelo menos 10 caracteres** (`-m 10`), filtrando o ruído de sequências curtas de 3 a 9 caracteres.

**2. Comando 2:**

```cmd
bstrings -p
```

* **Explicação do output**: exibe no ecrã a tabela completa das **27 expressões regulares integradas (*built-in REGEXes*)** disponíveis no `bstrings` (listadas na secção anterior), com os respetivos identificadores (`Name`) e descrições (`Description`).

**3. Comando 3:**

```cmd
bstrings --lr reg_path -f c:\windows\notepad.exe
```

* **Explicação do output**: pesquisa no binário `c:\windows\notepad.exe` (`-f`) aplicando a expressão regular integrada **`reg_path`** (`--lr reg_path`), devolvendo exclusivamente as *strings* embutidas no Bloco de Notas que correspondem a **caminhos de chaves/hives do Windows Registry** (ex.: `Software\Microsoft\Notepad`).

**4. Questão: *"How to search for bitcoin addresses?"*:**

```cmd
bstrings --lr bitcoin -f c:\windows\notepad.exe
```

* **Explicação**: invoca o padrão integrado **`bitcoin`** através da opção **`--lr bitcoin`**, que procura no ficheiro alvo (`-f`) todas as *strings* que respeitem a estrutura de endereços de carteiras Bitcoin.

---

## Além da aula

* **Pontes com Codificações e Artefactos em [[00 AFD1|AFD1]] e [[00 ASSI|ASSI]]**:
  * Os padrões `b64` e `bitcoin` do `bstrings -p` articulam-se diretamente com o estudo de **[[Codificação Binário-para-Texto (Base16, Base64 e Base58)]]** no Capítulo 3 de AFD1.
  * Em análises de memória RAM ou ficheiros de paginação (`pagefile.sys` / `swapfile.sys`, ver [[UWP - Artefactos Forenses e Estrutura de Dados]]), o parâmetro `-b 512` (*chunk size* em MB) do `bstrings` permite processar dumps de dezenas de gigabytes sem esgotar a memória da estação forense, procurando chaves de recuperação BitLocker (`--lr bitlocker`), caminhos UNC (`--lr unc`) ou URLs (`--lr url3986`).

---

## Perguntas de revisão

1. **Qual é a diferença entre os parâmetros `--ls`, `--fs`, `--lr` e `--fr` no `bstrings`?**

> [!success]- Ver Resposta
> `--ls` e `--fs` procuram ***strings* literais** (uma *string* única passada na linha de comandos com `--ls`, ou várias listadas num ficheiro com `--fs`). Já `--lr` e `--fr` procuram **expressões regulares** (uma regex personalizada ou o nome de uma das 27 *built-in regexes* com `--lr`, ou um ficheiro de expressões regulares com `--fr`).

2. **Como se restringe a extração apenas a *strings* entre 10 e 15 caracteres num ficheiro e como se desativa a pesquisa Unicode?**

> [!success]- Ver Resposta
> Limita-se o comprimento mínimo e máximo em simultâneo com `bstrings -m 10 -x 15 -f FILE`. Como `-a` e `-u` têm valor padrão `true`, desativa-se a pesquisa Unicode passando explicitamente **`-u false`**.

3. **Como se listam as 27 expressões regulares integradas do `bstrings` e como se aplica uma delas para procurar caminhos do Registry ou endereços Bitcoin em `notepad.exe`?**

> [!success]- Ver Resposta
> Lista-se o catálogo com `bstrings -p`. Para aplicar uma expressão integrada passa-se o seu `Name` ao parâmetro `--lr`: **`bstrings --lr reg_path -f c:\windows\notepad.exe`** (para caminhos do Registry) e **`bstrings --lr bitcoin -f c:\windows\notepad.exe`** (para endereços Bitcoin).

4. **O que distingue o modo `-q` do modo `-s` no `bstrings`, e qual é o impacto de combinar `-s` com `-o`?**

> [!success]- Ver Resposta
> O parâmetro **`-q`** (*Quiet mode*) oculta apenas o cabeçalho e o total de *hits*, continuando a imprimir os resultados. Já **`-s`** (*Really Quiet mode*) suprime totalmente a impressão dos *hits* na consola — o que **acelera significativamente o processamento** quando combinado com **`-o`** para gravar diretamente para ficheiro.

---

## Notas relacionadas

- [[Conceito de Strings e Comando strings em Unix-Linux]]
- [[Extração de Strings no Windows - Sysinternals strings e Swiss File Knife (sfk)]]
- [[YARA - Tipos de Strings, Modificadores, Formato Hexadecimal, Base64 e Regex]]
- [[Codificação Binário-para-Texto (Base16, Base64 e Base58)]]
- [[Estrutura e Hives do Windows Registry]]
- [[Artefacto Forense do Bloco de Notas (Notepad Windows 11)]]
- [[Capítulo 3 - YARA - MOTW - Strings]]
