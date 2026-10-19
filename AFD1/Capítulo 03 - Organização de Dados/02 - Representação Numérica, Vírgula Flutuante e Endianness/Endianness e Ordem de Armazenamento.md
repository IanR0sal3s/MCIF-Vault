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
atualizado: 2026-10-19
---

# Endianness e Ordem de Armazenamento

Como um único Byte (8 bits) apenas permite representar $2^8 = 256$ valores distintos, o armazenamento de números maiores exige o agrupamento de múltiplos bytes (tipicamente 2, 4 ou 8 bytes). A ordem pela qual esses bytes são colocados em endereços sucessivos de memória ou disco designa-se por **Endianness**: sistemas **Big-endian** colocam o byte mais significativo (*MSB*) no primeiro endereço (mais baixo), enquanto sistemas **Little-endian** colocam o byte menos significativo (*LSB*) no primeiro endereço.

---

## Unidade de Dados Binários e Agrupamento Multi-Byte

* $1\text{ Byte (B)} = 8\text{ bits (b)}$: permite $2^8 = 256$ valores possíveis (`0` a `255` ou `0x00` a `0xFF`).
* Para armazenar números de maior dimensão é necessário agrupar bytes:
  * Tipicamente **2, 4 ou 8 bytes** (**16, 32 ou 64 bits**).

---

## O Problema do Endianness: Big-Endian vs. Little-Endian

Os sistemas informáticos diferem na ordem pela qual armazenam valores compostos por múltiplos bytes:
* **Big-endian**: coloca o **byte mais significativo (*most significant byte*)** no **1.º endereço de armazenamento** (ou endereço mais baixo).
* **Little-endian**: coloca o **byte menos significativo (*less significant byte*)** no **1.º endereço de armazenamento** (ou endereço mais baixo).

### Exemplo Clássico: Armazenamento do Valor de 4 Bytes `0x12 34 56 78`
* Byte mais significativo (*MSB*): `12`
* Byte menos significativo (*LSB*): `78`

| Endereço de Armazenamento (*Storage address*) | `...` | `91` | `92` | `93` | `94` | `...` |
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

## Perguntas de revisão

- Qual é a diferença entre Big-endian e Little-endian na disposição em memória do número hexadecimal `0x12345678` nos endereços `91` a `94`?
- Que famílias de processadores utilizam Little-endian, Big-endian e modo programável?
- Qual é a ordem de bytes padrão nas redes IP (*network byte order*) e qual a sua importância?

## Notas relacionadas

- [[Sistemas de Numeração e Conversão entre Bases]]
- [[Números em Vírgula Flutuante (IEEE 754)]]
- [[Organização de Estruturas de Dados em Binário]]
- [[Codificação de Caracteres - ASCII, Latin-1 e Unicode]]
- [[Capítulo 3 - Organização de Dados]]
