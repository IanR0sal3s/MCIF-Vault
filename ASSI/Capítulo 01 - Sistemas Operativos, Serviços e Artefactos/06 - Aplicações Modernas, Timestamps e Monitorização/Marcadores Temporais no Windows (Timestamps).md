---
title: Marcadores Temporais no Windows (Timestamps)
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 6
tipo: conceito
tags:
  - assi
  - windows
  - timestamps
  - filetime
  - systemtime
  - epoch
  - forense
aliases:
  - Timestamps
  - FILETIME
  - SYSTEMTIME
  - Unix Epoch
  - w32tm
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
fontes:
  - "https://www.digital-detective.net/dcode/"
  - "https://www.silisoftware.com/tools/date.php"
atualizado: 2026-10-16
---

# Marcadores Temporais no Windows (Timestamps)

Representação binária de data e hora em sistemas operativos e artefactos do Registry (`UNIX Epoch`, `Microsoft FILETIME64`, `WebKit` e estrutura `SYSTEMTIME`) e respetiva descodificação pericial.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: Armazenar datas como texto (`"2020-11-02 13:21:38"`) ocupa demasiado espaço e torna lentas as operações aritméticas de comparação e ordenação. Por isso, o sistema operativo armazena o tempo como um inteiro que conta quantas unidades de tempo decorreram desde uma data zero de referência (**EPOCH**), ou como uma estrutura C de campos de 16 bits (`SYSTEMTIME`).
> * **Porque importa (Forense)**: A construção de uma linha temporal (*timeline*) rigorosa exige converter bytes em [[Endianness e Ordem de Armazenamento|Little-Endian]] extraídos do Registry (`UserAssist`, `LogonStats`, `NetworkList\Profiles`, `TelemetryController`) e do NTFS (`$MFT`) para datas exatas normalizadas em **UTC**.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Distinguir a EPOCH e a Unidade**: `UNIX` parte de **01/01/1970** (em segundos); `Microsoft FILETIME64` parte de **01/01/1601** (em intervalos de **100 nanossegundos**, $10^{-7}\text{ s}$); `WebKit/Chrome` parte de **01/01/1601** (em **microssegundos**, $10^{-6}\text{ s}$).
>   * **Descodificação Manual de `SYSTEMTIME` (16 bytes)**: Composta por 8 campos `WORD` (2 bytes cada, Little-Endian) na ordem exata: **Ano, Mês, Dia da Semana, Dia do Mês, Hora, Minuto, Segundo, Milissegundo**. Cuidado para não confundir o 3.º campo (`wDayOfWeek`) com o dia do mês (`wDay`, que é o 4.º campo!).

---

## Tabela Comparativa de Formatos Temporais em Exame

Qualquer marcador temporal numérico define-se por dois parâmetros: a **Origem (Tempo Zero / EPOCH)** e a **Unidade de Contagem**:

| Formato Temporal | Origem (EPOCH — UTC) | Unidade de Contagem | Tamanho Binário | Onde surge no Windows / Forense? |
| :--- | :---: | :---: | :---: | :--- |
| **UNIX Epoch** | `01/01/1970 00:00:00` | Segundos ($1\text{ s}$) | 32 bits (`int32`) ou 64 bits (`int64`) | Cabeçalhos PE (`TimeDateStamp`), logs multiplataforma, bases SQLite. |
| **UNIX Milliseconds (JavaTime)** | `01/01/1970 00:00:00` | Milissegundos ($10^{-3}\text{ s}$) | 64 bits (`int64`) | Aplicações Java, Android, artefactos web e JSON. |
| **UNIX Microseconds** | `01/01/1970 00:00:00` | Microssegundos ($10^{-6}\text{ s}$) | 64 bits (`int64`) | Sistemas de ficheiros e bases de dados de alta precisão. |
| **Microsoft FILETIME64** | **`01/01/1601 00:00:00`** | **100 nanossegundos** ($10^{-7}\text{ s}$) | 64 bits (`QWORD` / 8 bytes Little-Endian) | NTFS (`$STANDARD_INFORMATION`, `$FILE_NAME`), *LastWriteTime* de chaves do Registry, `UserAssist`, `RecentApps`, `TelemetryController`. |
| **WebKit / Google Chrome** | **`01/01/1601 00:00:00`** | **Microssegundos** ($10^{-6}\text{ s}$) | 64 bits (`int64`) | Histórico de navegação e cookies em browsers baseados em Chromium (Chrome, Edge, Brave). |
| **Estrutura `SYSTEMTIME`** | *Não usa EPOCH* (campos diretos) | Até ao Milissegundo | **128 bits (16 bytes)** — 8 $\times$ `WORD` (2 bytes LE) | `LogonStats` (`FirstLogonTime`), perfis de rede (`NetworkList\Profiles\...\DateCreated`/`DateLastConnected`). |

---

## Estrutura `SYSTEMTIME` (128 bits / 16 bytes) e Descodificação Passo a Passo

Ao contrário do `FILETIME64` (que é um único inteiro de 8 bytes), a estrutura `SYSTEMTIME` da API Win32 ocupa **16 bytes** divididos em **8 palavras de 16 bits (`WORD`, 2 bytes cada em Little-Endian)**:

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

### Exemplo Prático de Descodificação de `SYSTEMTIME`
Considere a sequência de 16 bytes extraída de um valor `REG_BINARY` do Registry:

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

---

## Exemplos Reais de Timestamps no Windows Registry

1. **Perfis de Rede Conectada (`SYSTEMTIME` — 16 bytes)**:
   * **Chave**: `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Profiles\<GUID>`
   * **Valor `DateCreated`** (e `DateLastConnected`): armazena os 16 bytes de `SYSTEMTIME` indicando a data/hora exata em que o computador se ligou pela primeira (e última) vez a essa rede Wi-Fi ou cablada.
2. **Telemetria e Execução (`FILETIME64` — 8 bytes `REG_QWORD`)**:
   * **Chave**: `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\TelemetryController`
   * **Valor `LastRunTime`**: valor `REG_QWORD` numérico em intervalos de 100 ns desde 1601 (ex.: `132817350018518822` decimal $\rightarrow$ `18/11/2021 18:50:01 UTC`).

---

## Ferramentas de Conversão e Descodificação

### 1. Anatomia do Utilitário Nativo: `w32tm.exe`
O Windows inclui a ferramenta nativa de serviço de tempo (`w32tm.exe`) capaz de converter um inteiro decimal `FILETIME64` diretamente na linha de comandos:

```cmd
w32tm.exe /ntte 132487968980000000
REM Saída: 153240 17:46:40.0000000 - 2020-07-23 5:46:40 PM
```

* **`w32tm.exe`**: utilitário de diagnóstico e configuração do serviço *Windows Time*.
* **`/ntte <valor_decimal>`**: (*NT Time Epoch*) parâmetro que converte um carimbo temporal do sistema NT (inteiro de 64 bits em intervalos de 100 nanossegundos desde `01/01/1601 00:00:00 UTC`) para uma data e hora legíveis.

### 2. Ferramentas Forenses Dedicadas

* **DCODE** (*Digital Detective*): ferramenta gráfica pericial de referência capaz de detetar e converter simultaneamente dezenas de formatos temporais (UNIX, FILETIME64, SYSTEMTIME, HFS+, Google Chrome/WebKit, OLE Automation) em Little-Endian e Big-Endian.
* **CyberChef**: operações `From UNIX Timestamp`, `Windows Filetime to UNIX Timestamp` e inversão de endianness (`Swap endianness`).
* **SiliSoftware Date/Time Converter**: conversor online rápido entre diferentes EPOCHs.

---

## Exercícios Clássicos de Aula e Exame: Limites e Conversões

### 1. Limite de 32 bits do UNIX Timestamp (*Year 2038 Problem*)

**Cálculo do Valor Limite:** Um inteiro de 32 bits com sinal (`int32`) reserva 1 bit para o sinal e 31 bits para a magnitude, atingindo o valor máximo positivo em:

$$2^{31} - 1 = 2\,147\,483\,647\text{ segundos}\quad (\text{em hexadecimal: }\mathtt{0x7FFFFFFF})$$

* **Data correspondente**: **`19/01/2038 03:14:07 UTC`** (terça-feira).
* **O que acontece 1 segundo depois?**: Ao somar 1 segundo (`0x80000000`), os contadores `int32` sofrem *integer overflow* para o valor negativo máximo (`-2147483648`), recuando a data para **`13/12/1901 20:45:52 UTC`**.

### 2. Conversão Matemática de Microsoft FILETIME64 (`140000000000000000`)
Como converter manualmente um `FILETIME64` para `UNIX Epoch`?

**1.** Sabendo que entre `01/01/1601` e `01/01/1970` existem `11644473600` segundos (ou `116444736000000000` intervalos de 100 ns) e que $1\text{ s} = 10^7\text{ intervalos de 100 ns}$:

$$\text{UNIX (s)} = \frac{140\,000\,000\,000\,000\,000 - 116\,444\,736\,000\,000\,000}{10\,000\,000} = 2\,355\,526\,400\text{ s}$$

**2. Data correspondente** (validável via `w32tm.exe /ntte 140000000000000000`): **`13/09/2044 02:53:20 UTC`**.

---

## Implicações Forenses

* **Normalização para UTC na Linha Temporal (*Timeline*)**: A reconstrução fidedigna de um incidente depende de correlacionar artefactos em múltiplos formatos temporais sem desvios de fuso horário ou horário de verão (*DST*). Todos os timestamps internos de baixo nível do Windows (`FILETIME64`) são armazenados em **UTC** e devem ser reportados de forma normalizada (ver [[Representação Forense de Data e Hora (Timestamps e SQLite)]]).
* **Armadilha de Endianness**: A inversão incorreta dos bytes de um valor [[Endianness e Ordem de Armazenamento|Little-Endian]] (ex.: esquecer de inverter os 8 bytes de um `FILETIME64` ou os pares de 2 bytes de cada campo `WORD` da estrutura C `SYSTEMTIME` — ver [[Organização de Estruturas de Dados em Binário]]) produz datas totalmente corrompidas ou séculos no passado/futuro.

---

## Perguntas de revisão

1. **Qual a diferença entre os formatos temporais `Microsoft FILETIME64` e `WebKit / Google Chrome` em termos de origem (EPOCH) e unidade de contagem?**

> [!success]- Ver Resposta
> Ambos partilham exatamente a mesma origem (EPOCH): **1 de janeiro de 1601 às 00:00:00 UTC**. A diferença reside na unidade de contagem: o `Microsoft FILETIME64` conta intervalos de **100 nanossegundos** ($10^{-7}\text{ s}$), enquanto o formato `WebKit / Google Chrome` conta **microssegundos** ($10^{-6}\text{ s}$, ou seja, um valor 10 vezes menor para o mesmo instante).

2. **Descodifique os primeiros 8 bytes de uma estrutura `SYSTEMTIME` extraída do Registry: `E5 07 0B 00 03 00 18 00`. Que ano, mês, dia da semana e dia do mês representam?**

> [!success]- Ver Resposta
> Cada campo da estrutura `SYSTEMTIME` tem 2 bytes (`WORD`) em formato Little-Endian:
> * `E5 07` $\rightarrow$ `0x07E5` = **2021** (`wYear`, Ano)
> * `0B 00` $\rightarrow$ `0x000B` = **11** (`wMonth`, Novembro)
> * `03 00` $\rightarrow$ `0x0003` = **3** (`wDayOfWeek`, Quarta-feira, pois `0` = Domingo)
> * `18 00` $\rightarrow$ `0x0018` = **24** (`wDay`, Dia 24 do mês).
>
> Corresponde a Quarta-feira, 24 de novembro de 2021.

3. **Em que consiste o "Problema do Ano 2038" (*Year 2038 Problem*) nos marcadores `UNIX Epoch` e qual é a data/hora limite exata em UTC?**

> [!success]- Ver Resposta
> Ocorre em sistemas que armazenam o timestamp UNIX num inteiro de 32 bits com sinal (`int32`). O valor máximo positivo é $2^{31} - 1 = 2\,147\,483\,647$ segundos após `01/01/1970 00:00:00 UTC`, o que corresponde exatamente a **`19/01/2038 03:14:07 UTC`**. No segundo seguinte ocorre *integer overflow* para um número negativo, fazendo o relógio saltar para dezembro de 1901.

4. **Qual o comando nativo do Windows que permite converter na consola o valor `FILETIME64` decimal `140000000000000000` para uma data legível?**

> [!success]- Ver Resposta
> O comando é `w32tm.exe /ntte 140000000000000000` (que devolve a data `13/09/2044 02:53:20 UTC`).

## Notas relacionadas

- [[Representação Forense de Data e Hora (Timestamps e SQLite)]]
- [[Endianness e Ordem de Armazenamento]]
- [[Organização de Estruturas de Dados em Binário]]
- [[Estrutura e Hives do Windows Registry]]
- [[Artefacto Forense UserAssist]]
- [[Artefactos Forenses de Execução e Persistência no Registry]]
- [[Artefactos Forenses de Dispositivos USB]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
