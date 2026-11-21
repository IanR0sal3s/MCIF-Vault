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
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v4.pdf
atualizado: 2026-11-21
---

# O Comando `forfiles`

O **`forfiles`** é um comando nativo do Windows que seleciona um ficheiro (ou conjunto de ficheiros) segundo caminho, máscara e data, executando um comando em cada elemento encontrado.

## 1. Anatomia e Parâmetros Principais

```text
forfiles  /P C:\Users\  /S  /M *.txt  /D -30  /C "cmd /c echo @file"
          └───┬──────┘  └┬┘ └───┬───┘ └──┬──┘ └──────────┬─────────┘
         1. Diretório    │  3. Máscara 4. Data     5. Comando a executar
                    2. Recursivo
```

| Parâmetro / Variável | Função |
| :--- | :--- |
| **`/P`** | Diretório de partida (*path*). |
| **`/S`** | Percorre subdiretórios recursivamente. |
| **`/M`** | Máscara de pesquisa (ex.: `*.exe`, `*.txt`). |
| **`/D`** | Filtro de data de modificação: **`-n`** (modificados há mais de `n` dias) ou data absoluta (ex.: `01/01/2026` — posteriores à data). |
| **`/C`** | Comando a executar (ex.: `"cmd /c ..."`). |
| **`@file` / `@path` / `@isdir`** | Nome do ficheiro, caminho completo do ficheiro e booleano (`TRUE` se for diretório, `FALSE` se for ficheiro). |

---

## 2. Exemplos da Aula

```cmd
:: Procurar todos os .exe recursivamente em C:\Windows
forfiles /P C:\Windows /S /M *.exe

:: Listar .txt em C:\Users modificados há mais de 30 dias
forfiles.exe /P C:\Users\ /M *.txt /D -30 /C "cmd /c echo @file"

:: Listar apenas ficheiros (não diretórios) posteriores a 01/01/2026
forfiles /D 01/01/2026 /C "cmd /c if @isdir==FALSE echo '@path' +recente 2026.01.01"

:: Executar dir sobre ficheiros em C:\Temp com mais de 7 dias
forfiles /p "C:\Temp" /d -7 /c "cmd /c dir @file"
```

---

## Além da aula

Em segurança ofensiva e defensiva, o `forfiles` é também monitorizado como **LOLBIN** (*Living off the Land Binary*), pois o parâmetro `/C "cmd /c ..."` pode ser abusado para lançar comandos arbitrários em cascata.

---

## Perguntas de revisão

1. **No comando `forfiles`, que ficheiros seleciona `/D -30` face a `/D 01/01/2026`?**

> [!success]- Ver Resposta
> `/D -30` seleciona ficheiros modificados **há mais de 30 dias**; `/D 01/01/2026` seleciona ficheiros/diretórios **posteriores** a essa data.

2. **Como excluir diretórios da saída do `forfiles` imprimindo apenas o caminho completo dos ficheiros?**

> [!success]- Ver Resposta
> Usando `@isdir` e `@path` dentro de `/C`: `forfiles /D 01/01/2026 /C "cmd /c if @isdir==FALSE echo '@path'"`.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Processos e linha de comandos no Windows]] | `mesmo bloco` |
| **Seguinte** | [[Serviços Windows]] | `muda para Bloco 03` |
| **Índice** | [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]] · [[00 ASSI]] | `Bloco 02` |
