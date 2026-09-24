---
title: Marcadores Temporais no Windows (Timestamps)
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
tipo: conceito
tags:
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
atualizado: 2026-09-23
---

# Marcadores Temporais no Windows (Timestamps)

A representação textual de data/hora (ex.: `"2020-11-02 13:21:38"`) é computacionalmente ineficiente para indexação, pesquisa e armazenamento. Nos sistemas operativos e em bases de dados como o Registry, os marcadores temporais são armazenados sob a forma de **números inteiros** ou **estruturas binárias compactas**.

Qualquer marcador temporal numérico assenta em dois elementos fundamentais:
1. **Origem (Tempo Zero / EPOCH)**: a data e hora de referência a partir da qual a contagem tem início.
2. **Unidade de Contagem**: a fração de tempo contabilizada a cada incremento (segundos, milissegundos, microssegundos ou intervalos de 100 nanossegundos).

---

## Principais Formatos Encontrados no Windows

### 1. UNIX Epoch (Seconds)
* **Origem**: 1 de janeiro de 1970 às 00:00:00 GMT/UTC.
* **Unidade**: segundos.
* **Tamanho**: inteiro de 32 bits com sinal (`int32`) ou 64 bits (`int64`).
* *Variações*: UNIX Milliseconds (JavaTime, `int64`) e UNIX Microseconds (`int64`).

### 2. Microsoft FILETIME64
* **Origem**: 1 de janeiro de 1601 às 00:00:00 GMT/UTC.
* **Unidade**: intervalos de **100 nanossegundos** ($10^{-7}\text{ s}$).
* **Tamanho**: inteiro de 64 bits (`int64` / `QWORD`) em formato Little-Endian.
* *Uso no Windows*: marcas temporais NTFS (MFT: $STANDARD_INFORMATION e $FILE_NAME), chaves de execução do Registry e telemetria.

### 3. WebKit / Google Chrome
* **Origem**: 1 de janeiro de 1601 às 00:00:00 GMT/UTC (idêntico à EPOCH da Microsoft).
* **Unidade**: **microssegundos** ($10^{-6}\text{ s}$).

### 4. Estrutura `SYSTEMTIME` (128 bits / 16 bytes)
Estrutura binária definida na API Win32 que armazena os campos de data e hora em palavras de 16 bits (`WORD`, inteiros de 2 bytes em Little-Endian):

```c
typedef struct _SYSTEMTIME {
    WORD wYear;          // Ano (ex: 0x07E4 = 2020)
    WORD wMonth;         // Mês (1-12)
    WORD wDayOfWeek;     // Dia da semana (0 = Domingo, 1 = 2ª feira, ...)
    WORD wDay;           // Dia do mês (1-31)
    WORD wHour;          // Hora (0-23)
    WORD wMinute;        // Minutos (0-59)
    WORD wSecond;        // Segundos (0-59)
    WORD wMilliseconds;  // Milissegundos (0-999)
} SYSTEMTIME;
```

#### Exemplo Prático de Descodificação de `SYSTEMTIME`
Sequência de 16 bytes extraída de um valor do Registry:
`E4 07 08 00 01 00 1F 00 0B 00 15 00 1C 00 FF 00`

* `E4 07` $\rightarrow$ Little-Endian: `0x07E4` = **2020**
* `08 00` $\rightarrow$ `0x0008` = **Mês 8 (Agosto)**
* `01 00` $\rightarrow$ `0x0001` = **1 (2ª feira)**
* `1F 00` $\rightarrow$ `0x001F` = **Dia 31**
* `0B 00` $\rightarrow$ `0x000B` = **11 horas**
* `15 00` $\rightarrow$ `0x0015` = **21 minutos**
* `1C 00` $\rightarrow$ `0x001C` = **28 segundos**
* `FF 00` $\rightarrow$ `0x00FF` = **255 milissegundos**
* **Resultado**: `2020-08-31 11:21:28.255 UTC`.

---

## Exemplos Reais no Registry

1. **Perfis de Rede Conectada** (`SYSTEMTIME`):
   * Chave: `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Profiles\<GUID>`
   * Valor `DateCreated`: armazena os 16 bytes de `SYSTEMTIME` indicando a data em que o computador se ligou pela primeira vez à rede.
2. **Telemetria e Execução** (FILETIME64):
   * Chave: `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\TelemetryController`
   * Valor `LastRunTime`: valor `REG_QWORD` numérico (ex.: `132817350018518822` decimal $\rightarrow$ `18/11/2021 18:50:01 UTC`).

---

## Ferramentas de Conversão e Descodificação

### 1. Utilitário Nativo: `w32tm`
O Windows inclui a ferramenta nativa de sincronização temporal capaz de converter FILETIME64 na linha de comandos:

```cmd
w32tm.exe /ntte 132487968980000000
REM Saída: 153240 17:46:40.0000000 - 2020-07-23 5:46:40 PM
```

### 2. Ferramentas Forenses Dedicadas
* **DCODE** (Digital Detective): ferramenta gráfica pericial capaz de detetar e converter automaticamente dezenas de formatos temporais (UNIX, FILETIME, SYSTEMTIME, HFS+, Google Chrome, OLE Automation).
* **CyberChef**: operações `From UNIX Timestamp` e conversões hexadecimais.
* **SiliSoftware Date/Time Converter**: conversão online rápida entre EPOCHs.

## Implicações Forenses

* **Linha Temporal (*Timeline*)**: A reconstrução fidedigna de um incidente depende de correlacionar artefactos em múltiplos formatos temporais sem desvios de fuso horário. Todos os timestamps internos de baixo nível do Windows devem ser convertidos e normalizados para **UTC**.
* **Endianness**: A inversão incorreta dos bytes de um valor Little-Endian (ex.: inverter bytes num FILETIME64 ou nos campos individuais de um `SYSTEMTIME`) produz datas totalmente corrompidas ou séculos no passado/futuro.

## Notas relacionadas

- [[Estrutura e Hives do Windows Registry]]
- [[Artefacto Forense UserAssist]]
- [[Artefactos Forenses de Execução e Persistência no Registry]]
- [[Artefactos Forenses de Dispositivos USB]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
