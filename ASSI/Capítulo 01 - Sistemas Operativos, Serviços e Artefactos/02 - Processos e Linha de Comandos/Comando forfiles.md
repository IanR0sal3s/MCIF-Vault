---
title: Comando forfiles
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
tipo: procedimento
tags:
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

O **`forfiles`** é um utilitário nativo de linha de comandos do Windows concebido para selecionar ficheiros ou diretórios com base em critérios de filtragem (como máscaras de extensão e datas de modificação) e **executar automaticamente um comando arbitrário em cada elemento selecionado**.

Em administração de sistemas e triagem forense inicial, o `forfiles` é amplamente utilizado para identificar ficheiros modificados recentemente, localizar artefactos criados em datas suspeitas ou realizar tarefas de manutenção em lote sem necessidade de scripts complexos de PowerShell ou Python.

---

## Sintaxe e Parâmetros Principais

A estrutura geral do comando é:

```cmd
forfiles [/P <Caminho>] [/S] [/M <Mascara>] [/D <Data>] [/C <Comando>]
```

| Parâmetro | Função | Descrição |
| :---: | :--- | :--- |
| **`/P`** | *Path* | Diretório de partida a partir do qual é efetuada a pesquisa (por omissão é a pasta atual). |
| **`/S`** | *Subdirectories* | Instrui o comando a percorrer recursivamente todas as subpastas. |
| **`/M`** | *Mask* | Máscara de pesquisa para correspondência de nomes de ficheiros (ex.: `*.exe`, `*.txt`, `*.*`). O padrão é `*`. |
| **`/D`** | *Date* | Filtro de data de última modificação. Suporta datas absolutas (`DD/MM/YYYY`) ou valores relativos (`-n` para ficheiros com mais de *n* dias; `+n` para ficheiros com menos de *n* dias). |
| **`/C`** | *Command* | Comando a executar para cada elemento correspondente. A string do comando deve estar delimitada por aspas duplas. Tipicamente invoca-se `cmd /c <instrução>`. |

### Variáveis Especiais de Substituição no Parâmetro `/C`

Ao definir a instrução a executar em cada ficheiro, podem utilizar-se as seguintes variáveis internas:
* **`@file`**: Nome do ficheiro ou pasta atual com a respetiva extensão.
* **`@fname`**: Nome do ficheiro sem a extensão.
* **`@ext`**: Apenas a extensão do ficheiro.
* **`@path`**: Caminho absoluto completo do elemento (ex.: `"C:\Windows\System32\cmd.exe"`).
* **`@isdir`**: Retorna `TRUE` se o elemento atual for um diretório e `FALSE` se for um ficheiro.
* **`@fdate`** / **`@ftime`**: Data e hora da última modificação do ficheiro.

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

## Implicações Forenses

* **Identificação Rápida de *Timestomping* e Alterações Recentes**: O `forfiles` permite a um analista pericial listar imediatamente ficheiros executáveis ou scripts (`.ps1`, `.bat`, `.vbs`) modificados nas últimas 24 ou 48 horas numa máquina sem necessitar de instalar ferramentas externas.
* **Uso Legítimo vs. Abuso por Malware**: A capacidade do `forfiles` de executar comandos arbitrários em cascata através de `cmd /c` é por vezes abusada por atores maliciosos como técnica de *Living off the Land* (LOLBIN) para evadir deteção baseada em linhas de comando convencionais.

## Notas relacionadas

- [[Processos e linha de comandos no Windows]]
- [[Serviços Windows]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
