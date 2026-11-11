---
title: Extração de Strings no Windows - Sysinternals strings e Swiss File Knife (sfk)
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
  - windows
  - sysinternals
  - sfk
aliases:
  - Strings in Windows
  - Sysinternals strings
  - strings.exe
  - sfk strings
  - Swiss File Knife
atualizado: 2026-11-11
---

# Extração de Strings no Windows — Sysinternals `strings` e Swiss File Knife (`sfk`)

Como o Windows não inclui um comando **`strings`** nativo, recorre-se ao **`strings.exe`** da Sysinternals, ao **Swiss File Knife (`sfk`)** ou ao **`bstrings`** para extrair texto ASCII e Unicode em binários.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: Binários e artefactos do Windows armazenam texto tanto em ANSI/ASCII como em **Unicode (UTF-16)**; utilitários dedicados para Windows automatizam a deteção simultânea de ambas as codificações e a travessia recursiva de diretorias.
> * **Porque importa (Forense)**: Em triagem *live* ou análise de *malware* no Windows, `strings.exe` e `sfk strings` permitem extrair e filtrar indicadores rapidamente em linha de comandos, evitando omissão de cadeias UTF-16LE típicas da API Win32.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Ausência de ferramenta nativa**: o Windows não traz `strings` de fábrica (alternativas da aula: **Sysinternals `strings`**, **Eric Zimmerman `bstrings`** e **`sfk strings`**).
>   * **Unix `strings` vs. Sysinternals `strings.exe`**: o Unix procura apenas **ASCII 7 bits** com mínimo de **`4`** caracteres; o Sysinternals procura **ANSI + Unicode** por omissão com mínimo de **`3`** caracteres.
>   * **Flag `-nobanner`**: indispensável ao redirecionar ou encadear saída do `strings.exe` em scripts para omitir o cabeçalho de copyright.
>   * **`sfk filter -ls+WORD`**: `ls` significa ***line start*** (filtra apenas linhas iniciadas por `WORD`).

---

## 1. Comparação Lado a Lado: Unix `strings` vs. `strings.exe` vs. `sfk strings` vs. `bstrings`

Antes de escolher a ferramenta para um exame pericial ou script de triagem, importa comparar os padrões de cada utilitário (Slides 3–11):

| Ferramenta | Codificação Padrão | Comprimento Mínimo Padrão | Suporte Recursivo | Filtros / Pesquisa Nativa |
| :--- | :--- | :---: | :--- | :--- |
| **Unix `strings`** | ASCII 7 bits (`-e s`; suporta `S`, `b`/`l`, `B`/`L` com `-e`) | **`4`** caracteres (`-n`) | Não nativo | Não (requer *pipe* para `\| grep`) |
| **Sysinternals `strings.exe`** | **ANSI (ASCII) + Unicode** (`-a` ou `-u` para restringir) | **`3`** caracteres (`-n`) | Sim (**`-s`**) | Não (requer *pipe* externo) |
| **Swiss File Knife (`sfk strings`)** | Extração de texto legível em ficheiros | *Conforme sintaxe `sfk strings FILE`* | — *(não abordado em aula)* | **Sim**: filtro interno `+filter -+WORD` ou *pipe* `\| sfk filter -ls+WORD` |
| **Eric Zimmerman `bstrings`** | **ASCII + Unicode** (`-a` e `-u` ativos por omissão; intervalos `--ar`/`--ur`) | **`3`** caracteres (`-m`, e máximo `-x` ilimitado) | Sim (**`-d DIR`**) | **Sim**: *strings* (`--ls`, `--fs`), *regex* (`--lr`, `--fr`) e **27 padrões integrados (`-p`)** |

---

## 2. Alternativas de Extração no Windows (Slide 8)

Ao contrário dos sistemas Unix/Linux (que incluem nativamente o [[Conceito de Strings e Comando strings em Unix-Linux|comando strings]]), **o sistema operativo Windows não possui um comando `strings` nativo**. Para extrair *strings* na linha de comandos do Windows, recorre-se a três opções principais apresentadas em aula:

1. **[Sysinternals `strings`](https://docs.microsoft.com/en-us/sysinternals/downloads/strings)**;
2. **[Eric Zimmerman `bstrings`](https://github.com/EricZimmerman/bstrings)** (estudado em detalhe em [[Eric Zimmerman bstrings - Parâmetros, Expressões Regulares e Exercícios]]);
3. **Swiss File Knife (`sfk strings FILE`)**.

---

## 3. Sysinternals `strings` (`strings.exe` — Slide 9)

O utilitário **`strings`** da Microsoft Sysinternals (`Strings v2.54`, da autoria de **Mark Russinovich**) é uma ferramenta simples e direta que **procura por omissão tanto *strings* ANSI (ASCII) como Unicode (UTF-16)** em imagens binárias, adotando um comprimento mínimo predefinido de **3 caracteres** (em vez dos 4 caracteres do Unix `strings`).

### Sinopse Oficial (`Strings v2.54`)

```text
Strings v2.54 - Search for ANSI and Unicode strings in binary images.
Copyright (C) 1999-2021 Mark Russinovich
Sysinternals - www.sysinternals.com

usage: strings [-a] [-f offset] [-b bytes] [-n length] [-o] [-s] [-u] [-nobanner] <file or directory>
```

### Tabela Completa de Parâmetros do Sysinternals `strings`

| Parâmetro | Descrição Técnica (`strings.exe`) |
| :--- | :--- |
| **`-a`** | Pesquisa **apenas *strings* ASCII** (por omissão pesquisa Unicode e ASCII). |
| **`-b <bytes>`** | Número de **bytes do ficheiro a varrer**. |
| **`-f <offset>`** | **Deslocamento (*file offset*) em bytes** a partir do qual deve iniciar o varrimento. |
| **`-o`** | Imprime o **offset no ficheiro** onde cada *string* foi localizada. |
| **`-n <length>`** | **Comprimento mínimo** da *string* em caracteres (**por omissão é `3`**). |
| **`-s`** | Percorre **subdiretorias de forma recursiva**. |
| **`-u`** | Pesquisa **apenas *strings* Unicode** (por omissão pesquisa Unicode e ASCII). |
| **`-nobanner`** | **Não exibe o banner de arranque** e a mensagem de copyright. |

---

## 4. Swiss File Knife (`sfk strings` — Slide 8)

O utilitário **`sfk` (*Swiss File Knife*)** disponibiliza o subcomando `sfk strings FILE`, permitindo extrair *strings* e filtrá-las diretamente sem depender do comando `grep`:

### Exemplos da Aula

**1. Extração com filtro interno encadeado (`+filter -+WORD`):**

```cmd
sfk strings FILE +filter -+WORD
```

* Extrai as *strings* de `FILE` e filtra internamente apenas as linhas que contêm `WORD`.

**2. Extração com *pipe* e filtro de início de linha (`| sfk filter -ls+WORD`):**

```cmd
sfk strings FILE | sfk filter -ls+WORD
```

* **`ls = line start`**: o modificador `-ls+WORD` filtra apenas as linhas extraídas que **começam** exatamente pela palavra `WORD`.

---

## Implicações Forenses

* **Diferença Crítica de Comportamento Padrão (Unix `strings` vs. Sysinternals `strings.exe`)**:
  1. **Codificação padrão**: enquanto o `strings` do Linux procura apenas ASCII de 7 bits por omissão (ignorando *strings* UTF-16LE a menos que se passe `-e l`), o `strings.exe` da Sysinternals procura **simultaneamente ASCII e Unicode (UTF-16)** por omissão (podendo restringir-se com `-a` ou `-u`).
  2. **Tamanho mínimo padrão**: no Unix `strings` o mínimo por omissão é **`4`**, enquanto no Sysinternals `strings.exe` (e no `bstrings`) o mínimo por omissão é **`3`**.
* **Uso de `-nobanner` em Scripts de Triagem**: ao redirecionar a saída do `strings.exe` para um ficheiro de relatório ou para outro comando através de *pipe*, deve incluir-se `-nobanner` para evitar que as 3 linhas de cabeçalho da Sysinternals contaminem os resultados.

---

## Além da aula

* **Relação com o `BinText` estudado em [[00 AFD1|AFD1]]**: Na nota [[Ferramentas Portáteis de Triagem, Pesquisa e FTK Imager Lite]] (Capítulo 2 de AFD1), foi apresentada a ferramenta gráfica portátil **`BinText`**. Enquanto o `BinText` oferece uma interface visual para inspecionar um ficheiro executável individualmente, o `strings.exe -s` da Sysinternals, o `sfk strings` e o [[Eric Zimmerman bstrings - Parâmetros, Expressões Regulares e Exercícios|bstrings]] permitem varrer diretorias inteiras e filtrar resultados em linha de comandos.

---

## Perguntas de revisão

1. **O Windows inclui nativamente o comando `strings`? Que três alternativas principais foram apresentadas na aula?**

> [!success]- Ver Resposta
> Não — o Windows não possui um comando `strings` nativo. As três alternativas de linha de comandos apresentadas na aula são: **Sysinternals `strings`** (`strings.exe`), **Eric Zimmerman `bstrings`** e **Swiss File Knife (`sfk strings`)**.

2. **Indique duas diferenças críticas de comportamento por omissão entre o `strings` do Unix/Linux e o `strings.exe` da Sysinternals.**

> [!success]- Ver Resposta
> (1) **Codificação**: o Unix `strings` pesquisa apenas ASCII de 7 bits por omissão, ao passo que o `strings.exe` pesquisa simultaneamente **ANSI (ASCII) e Unicode (UTF-16)** (podendo restringir-se com `-a` ou `-u`). (2) **Comprimento mínimo**: o Unix usa **`4`** caracteres por omissão, enquanto o Sysinternals `strings.exe` (tal como o `bstrings`) usa **`3`** caracteres.

3. **No Sysinternals `strings.exe`, o que fazem os parâmetros `-b`, `-f`, `-o`, `-s` e `-nobanner`?**

> [!success]- Ver Resposta
> * **`-b <bytes>`**: limita o número de bytes do ficheiro a varrer;
> * **`-f <offset>`**: define o *file offset* em bytes onde iniciar o varrimento;
> * **`-o`**: imprime o *offset* no ficheiro de cada *string* encontrada;
> * **`-s`**: percorre subdiretorias de forma recursiva;
> * **`-nobanner`**: suprime o cabeçalho inicial de arranque e copyright (essencial em scripts e *pipes*).

4. **Qual é a diferença entre `sfk strings FILE +filter -+WORD` e `sfk strings FILE | sfk filter -ls+WORD`?**

> [!success]- Ver Resposta
> O primeiro utiliza encadeamento interno (`+filter -+WORD`) para devolver qualquer linha extraída que contenha `WORD`; no segundo, o modificador **`-ls+WORD`** (*`ls` = line start*) restringe os resultados exclusivamente às linhas que **começam** por `WORD`.

---

## Notas relacionadas

- [[Conceito de Strings e Comando strings em Unix-Linux]]
- [[Eric Zimmerman bstrings - Parâmetros, Expressões Regulares e Exercícios]]
- [[Processos e linha de comandos no Windows]]
- [[Ferramentas Portáteis de Triagem, Pesquisa e FTK Imager Lite]]
- [[Capítulo 3 - YARA - MOTW - Strings]]
