---
title: Representação Forense de Data e Hora (Timestamps e SQLite)
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Análise Forense Digital I
sigla_uc: AFD1
capitulo: 3
bloco: 4
fonte_aula: MCIF – Digital Forensic Analysis 1 - Data Organization.pdf
tags:
  - afd1
  - forense
  - timestamps
  - unix-epoch
  - sqlite
  - firefox
  - chrome
aliases:
  - Date and Time
  - Unix Epoch Time
  - 400-year Gregorian calendar cycle
  - Histórico SQLite Firefox e Chrome
atualizado: 2026-10-19
---

# Representação Forense de Data e Hora (Timestamps e SQLite)

As datas e horas podem ser armazenadas como **strings de texto** (fáceis de ler por humanos, mas ambíguas quanto ao idioma/região e ineficientes para operações computacionais) ou em **binário/hexadecimal** (eficientes para o computador, mas dependentes da época de referência e resolução de cada software). Na análise forense destacam-se duas contagens fundamentais: o **Unix Epoch Time** (segundos desde `1970-01-01 00:00:00`) e o **Ciclo do Calendário Gregoriano de 400 anos** (microssegundos ou intervalos de 100ns desde `1601-01-01 00:00:00`).

---

## Formas de Armazenamento de Data e Hora

### 1. Como String de Texto (*as a string*)
* **Vantagem**: fácil de ler diretamente por humanos.
* **Desvantagens**:
  * Difícil para as operações do computador (por exemplo, para comparar ou ordenar datas numa base de dados).
  * Existem muitas representações diferentes e por vezes dependentes do idioma ou convenção nacional:
    * `Wednesday, January 9, 11:13:48 UTC 2019`
    * `2018-12-23 08:23:55` (ISO)
    * `23-12-2018 08:23:55` (formato PT — `DD-MM-YYYY`)
    * `12-23-2018 08:23:55` (formato US — `MM-DD-YYYY`)

### 2. Como Binário Representado com Números ou Hexadecimal
* **Vantagem**: mais fácil e eficiente para as operações do computador.
* **Desvantagem**: difícil de ler diretamente por humanos e, infelizmente, **nem todo o software utiliza a mesma representação**.

---

## Como o Tempo é Contado (*Epochs*)

| Sistema de Contagem | Origem (*Epoch*) | Unidade de Contagem | Sistemas Operativos, Linguagens e Aplicações |
| :--- | :--- | :--- | :--- |
| **Unix time** = **POSIX time** = **UNIX Epoch time** | `1970-01-01 00:00:00` | Número de **segundos** decorridos | Unix, Linux, **Firefox**, Java, JavaScript, Perl, PHP, Python, Ruby, Tcl, etc. |
| **Ciclo do Calendário Gregoriano de 400 anos** (*400-year Gregorian calendar cycle*) | `1601-01-01 00:00:00` | Número de **microssegundos** decorridos *(ou intervalos de 100ns no Win64/NTFS)* | **Google Chrome**, Windows 32 e 64 bits, NTFS, Cobol, etc. |

---

## Formatos de Armazenamento de Data e Hora por Software

Tabela comparativa de representações equivalentes em diferentes sistemas e aplicações:

| Software | Representação | Exemplo | Software | Representação | Exemplo |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Win 64 bits BE** | 16 Hex chars | `01 CC A6 3C 91 B9 72 00` | **Firefox SQLite** | 16 dígitos | `1 321 653 236 000 000` |
| **Win 64 bits LE** | 16 Hex chars | `00 72 B9 91 3C A6 CC 01` | **Chrome SQLite** | 17 dígitos | `12 966 126 836 000 000` |
| **Unix numeric** | 10 dígitos | `1 321 653 236` | **Cookie hi:low** | 18:19 dígitos | `3 923 586 186:30 188 999` |
| **Unix numeric m. seconds** | 13/16 dígitos | `1 321 653 236 000 000` | **DOS wFAT** | 8 Hex chars | `F0 48 64 40` |
| **Unix 32 bits BE** | 8 Hex chars | `4E C6 D3 F4` | **GSM** | 14 dígitos | `99 309 251 619 580` |
| **Unix 32 bits LE** | 8 Hex chars | `F4 D3 C6 4E` | **Samsung Swift** | 8 Hex chars | `E7 8C 94 7D` |
| **HFS+ 32 bits BE** | 8 Hex chars | `CA EC 84 74` | **Nokia Series 40** | 14 Hex chars | `07 D9 04 11 13 27 09` |
| **HFS+ 32 bits LE** | 8 Hex chars | `74 84 EC CA` | | | |
| **Mac Absolute time** | 9 dígitos | `343 346 036` | | | |

---

## Ferramentas de Conversão e Automação com SQL

### 1. Ferramentas Gráficas
* **MFT Stampede**: ferramenta GUI para Windows, muito simples de utilizar para converter múltiplos formatos temporais.
* **NirSoft `BrowsingHistoryView`**: extrai e converte automaticamente o histórico de navegação do *Internet Explorer*, *Mozilla Firefox*, *Google Chrome* e *Safari*.

### 2. Queries SQL para Automação de Tarefas em Bases SQLite de Navegadores

#### Mozilla Firefox (`places.sqlite` — época `1970-01-01` em microssegundos)
Como o Firefox guarda `visit_date` em microssegundos desde a época Unix (`1970-01-01`), divide-se por `1000000` para obter segundos Unix Epoch:

```sql
SELECT datetime(moz_historyvisits.visit_date/1000000, 'unixepoch', 'localtime'), moz_places.url
FROM moz_places, moz_historyvisits
WHERE moz_places.id = moz_historyvisits.place_id;
```

#### Google Chrome (`History` — época `1601-01-01` em microssegundos)
Como o Google Chrome guarda `visit_time` em microssegundos desde `1601-01-01`, divide-se primeiro por `1000000` (convertendo para segundos desde 1601) e subtrai-se **`11644473600`** (o número exato de segundos entre `1601-01-01` e `1970-01-01`) para normalizar para `unixepoch`:

```sql
SELECT datetime(((visits.visit_time/1000000)-11644473600), 'unixepoch'), urls.url, urls.title
FROM urls, visits
WHERE urls.id = visits.url;
```

---

## Implicações Forenses

* **Constante de Conversão `11644473600`**: Entre `1601-01-01 00:00:00 UTC` e `1970-01-01 00:00:00 UTC` decorreram exatamente $369\text{ anos}$ ($134\,774\text{ dias}$, equivalentes a $11\,644\,473\,600\text{ segundos}$). Conhecer este deslocamento permite converter qualquer timestamp WebKit/Chrome ou Windows FILETIME para Unix Epoch diretamente em queries SQL ou scripts Python.
* **Ambiguidade de Datas em Strings (`DD-MM` vs. `MM-DD`)**: Em logs textuais onde o dia é $\le 12$ (ex.: `04-05-2019`), é impossível distinguir entre 4 de maio (PT) e 5 de abril (US) sem analisar entradas adjacentes onde o dia ultrapasse `12` ou verificar a configuração regional (*locale*) do serviço.

---

## Além da aula

* **Convergência com os Marcadores Temporais e Bases SQLite do Windows ([[00 ASSI|ASSI]])**:
  * **FILETIME64, SYSTEMTIME e Utilitários (`w32tm`, `DCODE`)**: Na nota [[Marcadores Temporais no Windows (Timestamps)]], aprofunda-se a conversão de Microsoft `FILETIME64` (intervalos de 100 nanossegundos desde `1601-01-01`, onde se subtrai `116444736000000000` e se divide por `10000000`), o problema do ano 2038 (`int32`) e a estrutura de 128 bits `SYSTEMTIME`.
  * **Queries SQL sobre Bases SQLite do Windows 11**: Exatamente a mesma técnica SQLite `datetime(..., 'unixepoch')` estudada para o Chrome é aplicada na nova geração da [[AmCache - Arquitetura, Hives e Evolução para SQLite|AmCache em SQLite (`DeviceCensus.db`)]] no Windows 11 (`datetime((LastModified - 116444736000000000) / 10000000, 'unixepoch')`), bem como na exploração de `ActivitiesCache.db` ([[Windows Activity Timeline - Arquitetura e Base SQLite]]), `Windows.db` ([[Windows Search]]) e `StateRepository-*.srd` ([[UWP - Artefactos Forenses e Estrutura de Dados]]).
  * **Artefactos com Timestamps FILETIME64**: O formato de 64 bits da época de 1601 está presente no offset `60` do [[Artefacto Forense UserAssist]], no array das últimas 8 execuções (`Time01`–`Time08`) do [[Estrutura Interna e Algoritmo de Hashing do Prefetch|Prefetch]], nos metadados MAC dos [[Ficheiros LNK (Shell Links) - Metadados e Formato Binário|atalhos LNK]] e comprimido em `uLEB128` no campo `LastWriteTimestamp` do [[Artefacto Forense do Bloco de Notas (Notepad Windows 11)]].

---

## Perguntas de revisão

- Quais são as desvantagens de armazenar datas como strings de texto face à representação binária?
- Qual é a época inicial (*Epoch*) utilizada pelo Unix/Firefox e qual é a época inicial utilizada pelo Google Chrome/Windows/NTFS?
- Nas queries SQLite do Firefox e do Google Chrome, porque se divide o timestamp por `1000000` e porque é que no Chrome se subtrai adicionalmente `11644473600`?

## Notas relacionadas

- [[Marcadores Temporais no Windows (Timestamps)]]
- [[AmCache - Arquitetura, Hives e Evolução para SQLite]]
- [[Windows Activity Timeline - Arquitetura e Base SQLite]]
- [[Windows Search]]
- [[UWP - Artefactos Forenses e Estrutura de Dados]]
- [[Artefacto Forense UserAssist]]
- [[Estrutura Interna e Algoritmo de Hashing do Prefetch]]
- [[Endianness e Ordem de Armazenamento]]
- [[Camadas de Organização de Dados e Análise de Sistemas de Ficheiros]]
- [[Capítulo 3 - Organização de Dados]]
