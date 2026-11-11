---
title: Endianness e Ordem de Armazenamento
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Análise Forense Digital I
sigla_uc: AFD1
capitulo: 3
bloco: 2
fonte_aula: MCIF – Digital Forensic Analysis 1 - Data Organization.pdf
tags:
  - afd1
  - forense
  - endianness
  - big-endian
  - little-endian
  - x86
aliases:
  - Endianness
  - Big-endian
  - Little-endian
  - Storage Order
  - Network Byte Order
atualizado: 2026-11-11
---

# Endianness e Ordem de Armazenamento

Valores multi-byte exigem uma convenção de ordenação em memória: sistemas Big-endian gravam o byte mais significativo primeiro, enquanto sistemas Little-endian gravam o menos significativo primeiro.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: Um único byte codifica apenas $256$ valores (`0x00`–`0xFF`); armazenar inteiros de 16, 32 ou 64 bits requer distribuir vários bytes por endereços consecutivos, variando a ordem consoante a arquitetura de hardware ou o protocolo de rede.
> * **Porque importa (Forense)**: Arquiteturas `x86`/`x86-64` armazenam inteiros multi-byte em Little-endian no disco, na RAM e no Registry, ao passo que capturas de rede IP usam Big-endian; falhar a inversão dos bytes corrompe cálculos de tamanhos, identificadores e datas.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Inversão ao nível do byte, nunca dos dígitos hex individuais**: `0x12345678` em Little-endian grava-se `78 56 34 12` (não `87 65 43 21`).
>   * **Strings ASCII/UTF-8 não sofrem inversão**: apenas valores numéricos multi-byte (`uint16`, `uint32`, `uint64`, `float`) e caracteres multi-byte (`UTF-16`) dependem do *endianness*.
>   * **Network Byte Order**: os cabeçalhos IP utilizam **Big-endian** para garantir interoperabilidade entre arquiteturas distintas.

---

## Unidade de Dados Binários e Agrupamento Multi-Byte

* $1\text{ Byte (B)} = 8\text{ bits (b)}$: permite $2^8 = 256$ valores possíveis (`0` a `255` ou `0x00` a `0xFF`).
* Para armazenar números de maior dimensão é necessário agrupar bytes:
  * Tipicamente **2, 4 ou 8 bytes** (**16, 32 ou 64 bits**).

---

## O Problema do Endianness: Big-Endian vs. Little-Endian

Os sistemas informáticos diferem na ordem pela qual armazenam valores compostos por múltiplos bytes:

* **Big-endian**: coloca o **byte mais significativo (*MSB*)** no **1.º endereço de armazenamento** (ou endereço mais baixo).
* **Little-endian**: coloca o **byte menos significativo (*LSB*)** no **1.º endereço de armazenamento** (ou endereço mais baixo).

### Exemplo Clássico: Armazenamento do Valor de 4 Bytes `0x12 34 56 78`

* Byte mais significativo (*MSB*): `12`
* Byte menos significativo (*LSB*): `78`

| Endereço de Armazenamento | `...` | `91` | `92` | `93` | `94` | `...` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Valor em Big-endian** | `...` | **`12`** | **`34`** | **`56`** | **`78`** | `...` |
| **Valor em Little-endian** | `...` | **`78`** | **`56`** | **`34`** | **`12`** | `...` |

---

## Arquiteturas de Processadores e Redes de Dados

| Ordem de Armazenamento | Arquiteturas / Contextos | Características Técnicas |
| :--- | :--- | :--- |
| **Processadores Big-endian** | `SPARC`, `PowerPC`, `MIPS`, `Motorola 68k`, `Alpha`, ... | Ordem natural de leitura humana (esquerda para a direita) |
| **Processadores Little-endian** | `z80`, `VAX`, `x86`, `x86-64`, `amd64`, ... | Apresenta vantagens de otimização em arquiteturas *pipelined* |
| **Programáveis (Big/Little-endian)** | `ARM`, ... | Suportam configuração em ambos os modos (*bi-endian*) |
| **Redes de Dados (*Network Order*)** | Protocolo **IP**: **Big-endian** (com algumas exceções) | Essencial para garantir a interoperabilidade entre sistemas heterogéneos |

---

## Implicações Forenses

* **Inversão Obrigatória na Leitura Manual de *Hex Dumps***: Na análise forense de sistemas Windows e Linux em arquiteturas `x86`/`x86-64` (como a tabela MFT do NTFS, o Windows Registry ou estruturas C compiladas para PC), todos os inteiros de 16, 32 e 64 bits estão gravados em **Little-endian**. Ler `b3 00 0d 00` diretamente como `0xB3000D00` em vez de inverter os bytes para `0x000D00B3` conduz a erros grosseiros de interpretação pericial.
* **Tráfego de Rede vs. Disco**: Num ficheiro de captura de pacotes (`.pcap`), os cabeçalhos IP/TCP encontram-se em *Network Byte Order* (**Big-endian**), mesmo que a máquina que capturou o tráfego seja `x86-64` (**Little-endian**).

---

## Além da aula

* **O Papel do *Endianness* nos Artefactos Forenses do Windows ([[00 ASSI|ASSI]])**:
  * **Tipos de Dados no Windows Registry**: Na especificação de [[Tipos de Dados e Associação de Ficheiros no Registry]], o tipo padrão `REG_DWORD` (ID `4`) armazena inteiros de 32 bits em **Little-endian**, existindo um tipo separado `REG_DWORD_BIG_ENDIAN` (ID `5`) para **Big-endian**, enquanto `REG_QWORD` (ID `11`) armazena inteiros de 64 bits em **Little-endian**. De igual forma, na [[Artefactos Forenses de Interação do Utilizador (MRU e TypedPaths)|chave RecentDocs]], o valor `MRUListEx` guarda a ordem de abertura em blocos de 4 bytes Little-endian (ex.: `02 00 00 00` $= 2$).
  * **Marcadores Temporais (`FILETIME64` e `SYSTEMTIME`)**: Conforme detalhado em [[Marcadores Temporais no Windows (Timestamps)]], tanto os inteiros de 64 bits `FILETIME` (ex.: no offset `60` do [[Artefacto Forense UserAssist]]) como cada palavra `WORD` de 2 bytes da estrutura `SYSTEMTIME` (ex.: `E4 07` $\rightarrow$ `0x07E4` $= 2020$) estão guardados em **Little-endian**.
  * **Identificação de Arquiteturas de Processador em Cabeçalhos PE**: Em [[Arquitetura 32 vs 64 bits no Registry e Executáveis (WOW6432Node)]], os *magic bytes* do campo `Machine` no cabeçalho PE estão gravados em Little-endian no disco: `4C 01` (`0x014C` para `x86`), `64 86` (`0x8664` para `x86-64`/`AMD64`) e `64 AA` (`0xAA64` para `ARM64` Little-endian).
  * **Compressão de Inteiros em `uLEB128`, Checksums e Condições YARA (`uint16(0) == 0x5a4d`)**: O algoritmo [[Codificação uLEB128 em Estruturas de Dados do Windows]] (*Unsigned Little Endian Base 128*) dispõe os grupos de 7 bits em ordem **Little-endian**, ao passo que o checksum `CRC32` no final dos ficheiros `TabState` do [[Artefacto Forense do Bloco de Notas (Notepad Windows 11)]] é gravado em **Big-endian**. Já nas regras [[YARA - Introdução, Estrutura de Regras, Metadados e Condições|YARA]] e casos reais como o WannaCry em [[Execução e Compilação no YARA (yara e yarac), Casos Reais (UPX, WannaCry) e LLMs]], a condição `uint16(0) == 0x5a4d` lê os primeiros 2 bytes do cabeçalho PE (`4D 5A` = `"MZ"`) como um inteiro de 16 bits em **Little-endian** (`0x5A4D`).

---

## Perguntas de revisão

1. **Qual é a diferença entre Big-endian e Little-endian na disposição em memória do número hexadecimal `0x12345678` nos endereços `91` a `94`?**

> [!success]- Ver Resposta
> Em **Big-endian**, o byte mais significativo (`12`) ocupa o endereço mais baixo, ficando gravado como **`12 | 34 | 56 | 78`**. Em **Little-endian**, o byte menos significativo (`78`) ocupa o endereço mais baixo, invertendo a ordem dos bytes para **`78 | 56 | 34 | 12`**.

2. **Porque é que a conversão para Little-endian altera os pares de dígitos (`78 56 34 12`) e nunca os nibbles internos (`87 65 43 21`)?**

> [!success]- Ver Resposta
> Porque o *endianness* define a ordem de endereçamento **byte a byte** (cada byte corresponde a 2 dígitos hexadecimais), mantendo intacta a ordem dos bits dentro de cada byte individual.

3. **Que famílias de processadores utilizam Big-endian, Little-endian e modo programável (*bi-endian*)?**

> [!success]- Ver Resposta
> * **Big-endian**: `SPARC`, `PowerPC`, `MIPS`, `Motorola 68k`, `Alpha`.
> * **Little-endian**: `z80`, `VAX`, `x86`, `x86-64`, `amd64`.
> * **Programáveis (*bi-endian*)**: `ARM`.

4. **Qual é a ordem de bytes padrão nas redes IP (*Network Byte Order*) e que erro pericial ocorre num sistema Windows/Linux `x86-64` ao ler `b3 00 0d 00` sem inverter os bytes?**

> [!success]- Ver Resposta
> As redes IP utilizam **Big-endian** (*Network Byte Order*) para garantir interoperabilidade entre arquiteturas heterogéneas. Num sistema `x86-64` (Little-endian), ler `b3 00 0d 00` diretamente como `0xB3000D00` produz o valor errado `3 003 124 992` em vez de inverter para `0x000D00B3` (`852 147`).

## Notas relacionadas

- [[Sistemas de Numeração e Conversão entre Bases]]
- [[Números em Vírgula Flutuante (IEEE 754)]]
- [[Organização de Estruturas de Dados em Binário]]
- [[Codificação de Caracteres - ASCII, Latin-1 e Unicode]]
- [[Marcadores Temporais no Windows (Timestamps)]]
- [[Tipos de Dados e Associação de Ficheiros no Registry]]
- [[Arquitetura 32 vs 64 bits no Registry e Executáveis (WOW6432Node)]]
- [[Artefacto Forense UserAssist]]
- [[Codificação uLEB128 em Estruturas de Dados do Windows]]
- [[Capítulo 3 - Organização de Dados]]
