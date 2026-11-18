---
title: Timestamps e Épocas Temporais (UNIX Epoch vs. Windows FILETIME)
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Transversal (AFD1 e ASSI)
sigla_uc: COMUM
ucs_relacionadas:
  - AFD1
  - ASSI
tags:
  - comum
  - timestamps
  - unix-epoch
  - filetime
  - systemtime
  - sqlite
  - forense
aliases:
  - Representação Forense de Data e Hora (Timestamps e SQLite)
  - Marcadores Temporais no Windows (Timestamps)
  - FILETIME
  - SYSTEMTIME
  - Unix Epoch
atualizado: 2026-11-18
---

# Timestamps e Épocas Temporais (UNIX Epoch vs. Windows FILETIME)

Sistemas operativos e aplicações armazenam data e hora como contadores numéricos indexados a uma época fixa (`1970-01-01` no Unix ou `1601-01-01` no Windows/Chrome) ou como estruturas binárias de campos fixos (`SYSTEMTIME`), exigindo conversão rigorosa para `UTC`.

> [!TIP] Lógica de Funcionamento e Valor Transversal
> * **Porque existe (Sistema)**: Strings legíveis por humanos ocupam demasiado espaço, variam entre idiomas e tornam lentas as operações de comparação e ordenação. Por isso, o software guarda o tempo como contadores inteiros desde uma origem (**EPOCH**) ou como estruturas C de campos de 16 bits (`SYSTEMTIME`).
> * **Porque importa (Forense)**: A construção de uma linha temporal (*timeline*) fiável exige converter inteiros em [[Endianness e Ordem de Armazenamento|Little-Endian]] extraídos de bases SQLite de navegadores (**AFD1**) e de artefactos do Windows Registry ou NTFS (**ASSI**) para datas exatas normalizadas em **UTC**. Um erro de época ou *endianness* desloca eventos em décadas ou séculos.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Época vs. Unidade**: `UNIX` parte de **`1970-01-01`** (segundos no POSIX; microssegundos no Firefox `places.sqlite`); `Microsoft FILETIME64` parte de **`1601-01-01`** em intervalos de **100 nanossegundos** ($10^{-7}\text{ s}$); `WebKit / Google Chrome` parte de **`1601-01-01`** em **microssegundos** ($10^{-6}\text{ s}$).
>   * **Constante mágica `11644473600`**: representa os segundos exatos entre `1601-01-01` e `1970-01-01` ($369\text{ anos} = 134\,774\text{ dias}$).
>   * **Estrutura `SYSTEMTIME` (16 bytes)**: 8 campos `WORD` (2 bytes cada, Little-Endian) onde o 3.º campo é `wDayOfWeek` (`0` = Domingo) e o 4.º campo é `wDay` (dia do mês).
>   * **Ambiguidade textual**: datas com dia $\le 12$ (ex.: `04-05-2019`) não distinguem `DD-MM` (PT) de `MM-DD` (US) sem contexto adicional.

---

## 1. Representação Textual vs. Binária e Épocas Temporais (Epochs)

### String de Texto vs. Binário / Numérico

* **Como String de Texto**:
  * **Vantagem**: fácil de ler diretamente por humanos.
  * **Desvantagens**: lenta para comparar ou ordenar em bases de dados e sujeita a variações de idioma ou convenção nacional:
    * `Wednesday, January 9, 11:13:48 UTC 2019`
    * `2018-12-23 08:23:55` (ISO 8601)
    * `23-12-2018 08:23:55` (formato PT — `DD-MM-YYYY`)
    * `12-23-2018 08:23:55` (formato US — `MM-DD-YYYY`)
  * **Ambiguidade de Datas em Strings**: Em logs onde o dia é $\le 12$ (ex.: `04-05-2019`), é impossível distinguir entre 4 de maio (PT) e 5 de abril (US) sem inspecionar entradas adjacentes onde um dos campos ultrapasse `12` ou verificar o *locale* do serviço.
* **Como Binário / Numérico (ou Hexadecimal)**:
  * **Vantagem**: compacto e eficiente para operações computacionais.
  * **Desvantagem**: ilegível diretamente por humanos e dependente da **Época (EPOCH)**, da **Unidade de Contagem** e da [[Endianness e Ordem de Armazenamento|ordem de bytes (*endianness*)]].

### Épocas Temporais Principais e Constante de Conversão

| Sistema de Contagem | Origem (*Epoch* — UTC) | Unidade de Contagem | Sistemas Operativos, Linguagens e Aplicações |
| :--- | :--- | :--- | :--- |
| **Unix time** = **POSIX time** = **UNIX Epoch time** | `1970-01-01 00:00:00` | **Segundos** (ou ms / µs em variantes) | Unix, Linux, **Firefox**, Java, JavaScript, Perl, PHP, Python, Ruby, Tcl, cabeçalhos PE |
| **Ciclo do Calendário Gregoriano de 400 anos** (*400-year Gregorian calendar cycle*) | `1601-01-01 00:00:00` | **Microssegundos** ($10^{-6}\text{ s}$) ou **intervalos de 100 ns** ($10^{-7}\text{ s}$) | **Google Chrome / WebKit** (µs); **Windows 32/64 bits (`FILETIME64`)**, **NTFS**, Cobol (100 ns) |

Entre `1601-01-01 00:00:00 UTC` e `1970-01-01 00:00:00 UTC` decorreram exatamente $369\text{ anos}$ ($134\,774\text{ dias}$), equivalentes a **`11644473600` segundos** (ou `116444736000000000` intervalos de $100\text{ ns}$).

* **De Chrome / WebKit (microssegundos desde 1601) para UNIX (segundos desde 1970)**:

$$\text{UNIX (s)} = \frac{\text{WebKit}_{\mu\text{s}}}{1\,000\,000} - 11\,644\,473\,600$$

* **De Microsoft `FILETIME64` (intervalos de 100 ns desde 1601) para UNIX (segundos desde 1970)**:

$$\text{UNIX (s)} = \frac{\text{FILETIME64} - 116\,444\,736\,000\,000\,000}{10\,000\,000}$$

---

## 2. Tabela Comparativa Unificada de Formatos Temporais

| Formato Temporal | Origem (*EPOCH* — UTC) | Unidade de Contagem | Tamanho Binário | Onde surge na Forense / Windows? |
| :--- | :---: | :---: | :---: | :--- |
| **UNIX Epoch** | `01/01/1970 00:00:00` | Segundos ($1\text{ s}$) | 32 bits (`int32`) ou 64 bits (`int64`) | Cabeçalhos PE (`TimeDateStamp`), logs multiplataforma, sistemas Unix/Linux. |
| **UNIX Milliseconds (JavaTime)** | `01/01/1970 00:00:00` | Milissegundos ($10^{-3}\text{ s}$) | 64 bits (`int64`) | Aplicações Java, Android, artefactos web e JSON. |
| **UNIX Microseconds** | `01/01/1970 00:00:00` | Microssegundos ($10^{-6}\text{ s}$) | 64 bits (`int64`) | **Mozilla Firefox** (`places.sqlite`), sistemas de ficheiros e bases de alta precisão. |
| **Microsoft `FILETIME64`** | **`01/01/1601 00:00:00`** | **100 nanossegundos** ($10^{-7}\text{ s}$) | 64 bits (`QWORD` / 8 bytes LE) | NTFS (`$STANDARD_INFORMATION`, `$FILE_NAME`), *LastWriteTime* do Registry, `UserAssist`, `RecentApps`, `TelemetryController`, `AmCache`. |
| **WebKit / Google Chrome** | **`01/01/1601 00:00:00`** | **Microssegundos** ($10^{-6}\text{ s}$) | 64 bits (`int64`) | Histórico (`History`) e cookies em browsers Chromium (Chrome, Edge, Brave). |
| **Estrutura `SYSTEMTIME`** | *Não usa EPOCH* (campos diretos) | Até ao Milissegundo | **128 bits (16 bytes)** — 8 $\times$ `WORD` (2 bytes LE) | `LogonStats` (`FirstLogonTime`), perfis de rede (`NetworkList\Profiles\...\DateCreated`/`DateLastConnected`). |

### Ferramentas de Conversão Transversais

* **DCODE** (*Digital Detective*): ferramenta gráfica pericial de referência capaz de detetar e converter simultaneamente dezenas de formatos temporais (`UNIX`, `FILETIME64`, `SYSTEMTIME`, `HFS+`, `Chrome/WebKit`, `OLE Automation`) em Little-Endian e Big-Endian.
* **CyberChef**: operações `From UNIX Timestamp`, `Windows Filetime to UNIX Timestamp` e `Swap endianness`.
* **MFT Stampede**: ferramenta GUI para Windows para converter múltiplos formatos temporais.
* **NirSoft `BrowsingHistoryView`**: extrai e converte automaticamente o histórico do *Internet Explorer*, *Mozilla Firefox*, *Google Chrome* e *Safari*.
* **EpochConverter / SiliSoftware Date/Time Converter**: conversores rápidos entre diferentes *EPOCHs*.

---

## Aplicação por UC

### Em AFD1 (Organização de Dados e Bases SQLite de Browsers)

#### Formatos de Armazenamento de Data e Hora por Software

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

#### Queries SQL para Automação em Bases SQLite de Navegadores

**Mozilla Firefox (`places.sqlite` — época `1970-01-01` em microssegundos):**

```sql
SELECT datetime(moz_historyvisits.visit_date/1000000, 'unixepoch', 'localtime'), moz_places.url
FROM moz_places, moz_historyvisits
WHERE moz_places.id = moz_historyvisits.place_id;
```

**Google Chrome (`History` — época `1601-01-01` em microssegundos):**

```sql
SELECT datetime(((visits.visit_time/1000000)-11644473600), 'unixepoch'), urls.url, urls.title
FROM urls, visits
WHERE urls.id = visits.url;
```

#### Anatomia das Queries SQLite (Firefox e Chrome)

| Elemento da Query | Função na Conversão Forense | Firefox (`places.sqlite`) | Google Chrome (`History`) |
| :--- | :--- | :--- | :--- |
| **`/ 1000000`** | Converte o timestamp armazenado em **microssegundos** ($10^{-6}\text{ s}$) para **segundos inteiros**, preparando o argumento numérico esperado por `datetime()`. | Aplicado a `visit_date` (16 dígitos). | Aplicado a `visit_time` (17 dígitos). |
| **`- 11644473600`** | Subtrai os exatos $369\text{ anos}$ ($134\,774\text{ dias}$) que separam `1601-01-01` de `1970-01-01`, alinhando a contagem com a época Unix. | **Não necessário** (já usa `1970-01-01`). | **Obrigatório** após `/ 1000000`. |
| **`'unixepoch'`** | Instrui a função `datetime()` do SQLite a interpretar o número como segundos desde `1970-01-01 00:00:00 UTC` (em vez do padrão de dia juliano). | Presente. | Presente. |
| **`'localtime'`** | Modificador opcional que converte a hora resultante em UTC para o fuso horário local da máquina onde a query corre. | Incluído na query. | Omitido (devolve data/hora em **UTC**). |
| **Junção `WHERE`** | Relaciona cada visita temporal à respetiva página web através das chaves estrangeiras. | `moz_places.id = moz_historyvisits.place_id` | `urls.id = visits.url` |

* **Extensão a Bases SQLite e Artefactos do Windows 11**: A mesma técnica `datetime(..., 'unixepoch')` aplica-se à [[AmCache - Arquitetura, Hives e Evolução para SQLite|AmCache em SQLite (`DeviceCensus.db`)]] (`datetime((LastModified - 116444736000000000) / 10000000, 'unixepoch')`), `ActivitiesCache.db` ([[Windows Activity Timeline - Arquitetura e Base SQLite]]), `Windows.db` ([[Windows Search]]) e `StateRepository-*.srd` ([[UWP - Artefactos Forenses e Estrutura de Dados]]). O formato `FILETIME64` surge também no offset `60` do [[Artefacto Forense UserAssist]], no array `Time01`–`Time08` do [[Estrutura Interna e Algoritmo de Hashing do Prefetch|Prefetch]], nos metadados MAC dos [[Ficheiros LNK (Shell Links) - Metadados e Formato Binário|atalhos LNK]] e comprimido em `uLEB128` no campo `LastWriteTimestamp` do [[Artefacto Forense do Bloco de Notas (Notepad Windows 11)]].

---

### Em ASSI (Windows Registry, SYSTEMTIME e Linha de Comandos)

#### Estrutura `SYSTEMTIME` (128 bits / 16 bytes) e Descodificação Passo a Passo

Ao contrário do `FILETIME64` (um inteiro único de 8 bytes), a estrutura `SYSTEMTIME` da API Win32 ocupa **16 bytes** divididos em **8 palavras de 16 bits (`WORD`, 2 bytes cada em Little-Endian)**:

```c
typedef struct _SYSTEMTIME {
    WORD wYear;          // Bytes 0-1:  Ano (ex: 0x07E4 = 2020)
    WORD wMonth;         // Bytes 2-3:  Mês (1 = Janeiro ... 12 = Dezembro)
    WORD wDayOfWeek;     // Bytes 4-5:  Dia da semana (0 = Domingo, 1 = 2ª feira, ...)
    WORD wDay;           // Bytes 6-7:  Dia do mês (1-31)
    WORD wHour;          // Bytes 8-9:  Hora (0-23)
    WORD wMinute;        // Bytes 10-11: Minutos (0-59)
    WORD wSecond;        // Bytes 12-13: Segundos (0-59)
    WORD wMilliseconds;  // Bytes 14-15: Milissegundos (0-999)
} SYSTEMTIME;
```

**Exemplo Prático de Descodificação (`REG_BINARY`):**

`E4 07 08 00 01 00 1F 00 0B 00 15 00 1C 00 FF 00`

| Offset | Par de Bytes (LE) | Inversão para Hex (BE) | Valor Decimal | Campo da Estrutura `SYSTEMTIME` |
| :---: | :---: | :---: | :---: | :--- |
| `0–1` | `E4 07` | `0x07E4` | **2020** | `wYear` (Ano) |
| `2–3` | `08 00` | `0x0008` | **8** | `wMonth` (Agosto) |
| `4–5` | `01 00` | `0x0001` | **1** | `wDayOfWeek` (Segunda-feira — `0` é Domingo) |
| `6–7` | `1F 00` | `0x001F` | **31** | `wDay` (Dia do mês) |
| `8–9` | `0B 00` | `0x000B` | **11** | `wHour` (Horas) |
| `10–11` | `15 00` | `0x0015` | **21** | `wMinute` (Minutos) |
| `12–13` | `1C 00` | `0x001C` | **28** | `wSecond` (Segundos) |
| `14–15` | `FF 00` | `0x00FF` | **255** | `wMilliseconds` (Milissegundos) |

* **Resultado Final**: **`2020-08-31 11:21:28.255 UTC`** (Segunda-feira).

#### Exemplos Reais de Timestamps no Windows Registry

1. **Perfis de Rede Conectada (`SYSTEMTIME` — 16 bytes)**:
   * **Chave**: `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Profiles\<GUID>`
   * **Valores `DateCreated` e `DateLastConnected`**: armazenam os 16 bytes de `SYSTEMTIME` indicando a data/hora exata da primeira e última ligação a essa rede Wi-Fi ou cablada.
2. **Telemetria e Execução (`FILETIME64` — 8 bytes `REG_QWORD`)**:
   * **Chave**: `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\TelemetryController`
   * **Valor `LastRunTime`**: valor `REG_QWORD` numérico em intervalos de 100 ns desde 1601 (ex.: `132817350018518822` decimal $\rightarrow$ `18/11/2021 18:50:01 UTC`).

#### Utilitário Nativo `w32tm.exe`

```cmd
w32tm.exe /ntte 132487968980000000
REM Saída: 153240 17:46:40.0000000 - 2020-07-23 5:46:40 PM
```

* **`w32tm.exe`**: utilitário de diagnóstico e configuração do serviço *Windows Time*.
* **`/ntte <valor_decimal>`**: (*NT Time Epoch*) converte um carimbo temporal do sistema NT (inteiro de 64 bits em intervalos de 100 ns desde `01/01/1601 00:00:00 UTC`) para data e hora legíveis.

#### Exercícios Clássicos de Exame: Year 2038 Problem e Conversão `FILETIME64`

**1. Limite de 32 bits do UNIX Timestamp (*Year 2038 Problem*):**

Um inteiro de 32 bits com sinal (`int32`) reserva 1 bit para o sinal e 31 bits para a magnitude, atingindo o máximo positivo em:

$$2^{31} - 1 = 2\,147\,483\,647\text{ segundos}\quad (\text{em hexadecimal: }\mathtt{0x7FFFFFFF})$$

* **Data limite exata**: **`19/01/2038 03:14:07 UTC`** (terça-feira).
* **1 segundo depois (`0x80000000`)**: ocorre *integer overflow* para `-2147483648`, recuando o relógio para **`13/12/1901 20:45:52 UTC`**.

**2. Conversão Matemática de `FILETIME64` (`140000000000000000`):**

Sabendo que entre `01/01/1601` e `01/01/1970` existem `116444736000000000` intervalos de 100 ns e que $1\text{ s} = 10^7$ intervalos de 100 ns:

$$\text{UNIX (s)} = \frac{140\,000\,000\,000\,000\,000 - 116\,444\,736\,000\,000\,000}{10\,000\,000} = 2\,355\,526\,400\text{ s}$$

* **Data correspondente** (validável via `w32tm.exe /ntte 140000000000000000`): **`13/09/2044 02:53:20 UTC`**.

* **Implicações Forenses no Windows**: Normalizar sempre todos os marcadores para **UTC** na *timeline* (evitando desvios de fuso horário ou *DST*) e validar a inversão [[Endianness e Ordem de Armazenamento|Little-Endian]] (nos 8 bytes de `FILETIME64` ou nos pares de 2 bytes de cada `WORD` de `SYSTEMTIME` — ver [[Organização de Estruturas de Dados em Binário]]).

---

## Perguntas de revisão

1. **Nas queries SQLite do Firefox (`places.sqlite`) e do Google Chrome (`History`), qual é a função de `/ 1000000`, `- 11644473600`, `'unixepoch'` e `'localtime'`?**

> [!success]- Ver Resposta
> * **`/ 1000000`**: converte os timestamps de microssegundos para segundos inteiros.
> * **`- 11644473600`**: aplicado apenas no Chrome para deslocar a origem de `1601-01-01` para `1970-01-01` ($134\,774\text{ dias} = 11\,644\,473\,600\text{ segundos}$).
> * **`'unixepoch'`**: indica ao `datetime()` do SQLite que o valor numérico representa segundos desde `1970-01-01 00:00:00 UTC`.
> * **`'localtime'`**: modificador opcional (usado na query do Firefox) que ajusta o resultado UTC para o fuso horário local do sistema de análise; sem ele, a saída permanece em UTC.

2. **Qual a diferença entre os formatos `Microsoft FILETIME64` e `WebKit / Google Chrome` em termos de época (EPOCH) e unidade de contagem?**

> [!success]- Ver Resposta
> Ambos partilham exatamente a mesma origem: **`1601-01-01 00:00:00 UTC`**. A diferença reside na unidade de contagem: o `Microsoft FILETIME64` conta intervalos de **100 nanossegundos** ($10^{-7}\text{ s}$), enquanto o `WebKit / Google Chrome` conta **microssegundos** ($10^{-6}\text{ s}$, um valor 10 vezes menor para o mesmo instante).

3. **Descodifique os primeiros 8 bytes de uma estrutura `SYSTEMTIME` extraída do Registry: `E5 07 0B 00 03 00 18 00`. Que ano, mês, dia da semana e dia do mês representam?**

> [!success]- Ver Resposta
> Cada campo da estrutura `SYSTEMTIME` tem 2 bytes (`WORD`) em Little-Endian:
> * `E5 07` $\rightarrow$ `0x07E5` = **2021** (`wYear`, Ano)
> * `0B 00` $\rightarrow$ `0x000B` = **11** (`wMonth`, Novembro)
> * `03 00` $\rightarrow$ `0x0003` = **3** (`wDayOfWeek`, Quarta-feira, pois `0` = Domingo)
> * `18 00` $\rightarrow$ `0x0018` = **24** (`wDay`, Dia 24 do mês).
>
> Corresponde a Quarta-feira, 24 de novembro de 2021.

4. **Em que consiste o *Year 2038 Problem* nos marcadores `UNIX Epoch`, qual a data/hora limite exata em UTC e qual o comando nativo Windows para converter `FILETIME64` (`140000000000000000`)?**

> [!success]- Ver Resposta
> Ocorre quando o timestamp UNIX é armazenado num inteiro de 32 bits com sinal (`int32`), cujo máximo positivo é $2^{31} - 1 = 2\,147\,483\,647\text{ s}$ (`0x7FFFFFFF`), correspondendo a **`19/01/2038 03:14:07 UTC`**; no segundo seguinte ocorre *overflow* para `-2147483648` (`13/12/1901 20:45:52 UTC`). Para converter o `FILETIME64` na consola Windows usa-se `w32tm.exe /ntte 140000000000000000` (que devolve `13/09/2044 02:53:20 UTC`).

5. **Como se resolve pericialmente a ambiguidade de uma data textual como `04-05-2019` num registo de log?**

> [!success]- Ver Resposta
> Quando o dia é $\le 12$, não é possível distinguir isoladamente entre 4 de maio (PT `DD-MM`) e 5 de abril (US `MM-DD`). É necessário inspecionar entradas adjacentes no mesmo log onde um dos campos ultrapasse `12` ou verificar a configuração regional (*locale*) do serviço ou sistema operativo.

---

## Notas relacionadas

- [[Endianness e Ordem de Armazenamento]]
- [[Organização de Estruturas de Dados em Binário]]
- [[Camadas de Organização de Dados e Análise de Sistemas de Ficheiros]]
- [[Capítulo 3 - Organização de Dados]]
- [[AmCache - Arquitetura, Hives e Evolução para SQLite]]
- [[Windows Activity Timeline - Arquitetura e Base SQLite]]
- [[Windows Search]]
- [[UWP - Artefactos Forenses e Estrutura de Dados]]
- [[Estrutura e Hives do Windows Registry]]
- [[Artefacto Forense UserAssist]]
- [[Estrutura Interna e Algoritmo de Hashing do Prefetch]]
- [[Ficheiros LNK (Shell Links) - Metadados e Formato Binário]]
- [[Artefacto Forense do Bloco de Notas (Notepad Windows 11)]]
- [[Artefactos Forenses de Execução e Persistência no Registry]]
- [[Artefactos Forenses de Dispositivos USB]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
