---
title: Comando forfiles
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 2
tipo: procedimento
tags:
  - assi
  - windows
  - cli
  - automacao
  - forense
aliases:
  - forfiles
  - forfiles.exe
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
atualizado: 2026-09-24
---

# O Comando `forfiles`

O **`forfiles`** é um utilitário nativo de linha de comandos do Windows que seleciona ficheiros ou pastas segundo critérios de caminho, máscara e data de modificação, executando automaticamente um comando em cada item.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: Comandos simples como `dir` apenas listam ficheiros; o `forfiles` funciona como um motor de iteração nativo em lote (*batch*) que filtra elementos na árvore de diretórios e invoca uma ação (`cmd /c ...`) sobre cada resultado sem exigir scripts PowerShell.
> * **Porque importa (Forense / Segurança)**: Na triagem forense *live*, permite localizar rapidamente binários ou scripts modificados num intervalo temporal suspeito (`/D`). Em segurança ofensiva/defensiva, é monitorizado como **LOLBIN**, pois permite invocar comandos arbitrários em cascata através de `/C`.
> * **Pontos Críticos para Exame**:
>   * Filtro `/D`: **`-n`** seleciona ficheiros com **mais de *n* dias** (mais antigos); **`+n`** ou `+DD/MM/YYYY` seleciona ficheiros modificados **há menos de *n* dias / após a data** (mais recentes).
>   * Para filtrar apenas ficheiros (excluindo diretórios), usa-se a condição `if @isdir==FALSE` dentro do bloco `/C "cmd /c ..."`.

---

## Anatomia do Comando e Parâmetros Principais

Em administração de sistemas e triagem forense inicial, o `forfiles` é amplamente utilizado para identificar ficheiros modificados recentemente, localizar artefactos criados em datas suspeitas ou realizar tarefas de manutenção em lote sem necessidade de scripts complexos de PowerShell ou Python.

```cmd
forfiles [/P <Caminho>] [/S] [/M <Mascara>] [/D <Data>] [/C "<Comando>"]
```

```text
forfiles  /P C:\Users\  /S  /M *.txt  /D -30  /C "cmd /c echo @file"
          └───┬──────┘  └┬┘ └───┬───┘ └──┬──┘ └──────────┬─────────┘
        1. Onde procurar │  3. O quê  4. Quando    5. O que executar
                   2. Recursivo                    em cada resultado
```

| Parâmetro | Função | Descrição Detalhada e Comportamento |
| :---: | :--- | :--- |
| **`/P`** | *Path* | Diretório de partida a partir do qual é efetuada a pesquisa (por omissão é a pasta atual). |
| **`/S`** | *Subdirectories* | Instrui o comando a percorrer recursivamente todas as subpastas. |
| **`/M`** | *Mask* | Máscara de pesquisa para correspondência de nomes de ficheiros (ex.: `*.exe`, `*.txt`, `*.*`). O padrão é `*`. |
| **`/D`** | *Date* | Filtro de data de última modificação. Suporta datas absolutas (`DD/MM/YYYY`) ou valores relativos (`-n` para ficheiros com mais de *n* dias; `+n` para ficheiros com menos de *n* dias). |
| **`/C`** | *Command* | Comando a executar para cada elemento correspondente. A string do comando deve estar delimitada por aspas duplas. Tipicamente invoca-se `cmd /c <instrução>`. |

### Variáveis Especiais de Substituição no Parâmetro `/C`

Ao definir a instrução a executar em cada ficheiro, podem utilizar-se as seguintes variáveis internas:

| Variável | Valor Retornado | Exemplo de Saída |
| :--- | :--- | :--- |
| **`@file`** | Nome do ficheiro ou pasta atual com a respetiva extensão (entre aspas). | `"cmd.exe"` |
| **`@fname`** | Nome do ficheiro sem a extensão. | `"cmd"` |
| **`@ext`** | Apenas a extensão do ficheiro. | `"exe"` |
| **`@path`** | Caminho absoluto completo do elemento. | `"C:\Windows\System32\cmd.exe"` |
| **`@isdir`** | Retorna `TRUE` se o elemento atual for um diretório e `FALSE` se for um ficheiro. | `FALSE` |
| **`@fdate`** / **`@ftime`** | Data e hora da última modificação do ficheiro. | `24/09/2026` / `14:30:00` |

---

## Exemplos Práticos de Aplicação

### 1. Pesquisa Recursiva de Executáveis
Localizar todos os ficheiros executáveis presentes na pasta de sistema do Windows e respetivas subpastas:

```cmd
forfiles /P C:\Windows /S /M *.exe
```

### 2. Localização de Ficheiros Modificados há mais de 30 Dias
Identificar ficheiros de texto na pasta de utilizadores que foram modificados há mais de 30 dias:

```cmd
forfiles.exe /P C:\Users\ /M *.txt /D -30 /C "cmd /c echo @file"
```

### 3. Filtro Temporal Posterior a uma Data Específica
Listar exclusivamente ficheiros (excluindo diretórios através de validação lógica com `@isdir`) cuja data de modificação seja posterior a 01/01/2026:

```cmd
forfiles /D 01/01/2026 /C "cmd /c if @isdir==FALSE echo '@path' - +recente 2026.01.01"
```

### 4. Triagem de Ficheiros com mais de 7 Dias em Pastas Temporárias
Inspecionar o conteúdo de pastas de ficheiros temporários filtrando por ficheiros com mais de 7 dias de antiguidade (recorrendo a aspas no caminho para prevenir erros de parsing com espaços):

```cmd
forfiles /p "C:\Temp" /d -7 /c "cmd /c dir @file"
```

---

## Implicações Forenses

* **Identificação Rápida de *Timestomping* e Alterações Recentes**: O `forfiles` permite a um analista pericial listar imediatamente ficheiros executáveis ou scripts (`.ps1`, `.bat`, `.vbs`) modificados nas últimas 24 ou 48 horas numa máquina sem necessitar de instalar ferramentas externas.
* **Uso Legítimo vs. Abuso por Malware**: A capacidade do `forfiles` de executar comandos arbitrários em cascata através de `cmd /c` é por vezes abusada por atores maliciosos como técnica de *Living off the Land* (LOLBIN) para evadir deteção baseada em linhas de comando convencionais.

---

## Perguntas de revisão

1. **No comando `forfiles`, qual é a diferença entre usar o filtro `/D -30` e `/D +30` (ou `/D 01/01/2026`)?**

> [!success]- Ver Resposta
> * **`/D -30`**: seleciona ficheiros cuja data de última modificação é anterior ou igual a hoje menos 30 dias (ou seja, ficheiros com **mais de 30 dias** de antiguidade).
> * **`/D +30`** (ou `/D 01/01/2026`): seleciona ficheiros modificados recentemente (nos últimos 30 dias ou em data posterior/igual a `01/01/2026`).

2. **Como se constrói um comando `forfiles` que ignore pastas e imprima apenas o caminho completo (`@path`) dos ficheiros modificados após `01/01/2026`?**

> [!success]- Ver Resposta
> Utilizando a variável booleana `@isdir` numa condição `if` dentro do parâmetro `/C`:
> `forfiles /D 01/01/2026 /C "cmd /c if @isdir==FALSE echo '@path' - +recente 2026.01.01"`

3. **Qual é a diferença entre as variáveis internas `@file`, `@fname` e `@path` no parâmetro `/C` do `forfiles`?**

> [!success]- Ver Resposta
> * **`@file`**: devolve o nome do ficheiro com a extensão.
> * **`@fname`**: devolve apenas o nome do ficheiro sem a extensão.
> * **`@path`**: devolve o caminho absoluto completo do ficheiro no disco (incluindo diretório, nome e extensão).

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Processos e linha de comandos no Windows]] | `mesmo bloco` |
| **Seguinte** | [[Serviços Windows]] | `muda para Bloco 03` |
| **Índice** | [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]] · [[00 ASSI]] | `Bloco 02` |
