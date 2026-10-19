---
title: Sistemas de Numeração e Conversão entre Bases
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
  - binario
  - hexadecimal
  - representacao-numerica
aliases:
  - Numerical Representation
  - Binário e Hexadecimal
  - Conversão de Bases
atualizado: 2026-10-19
---

# Sistemas de Numeração e Conversão entre Bases

Enquanto os humanos utilizam o sistema **decimal** (10 símbolos) e os computadores operam internamente em **binário** (2 níveis de tensão: `0` e `1`), a análise forense de baixo nível recorre extensivamente ao sistema **hexadecimal** (16 símbolos, `0` a `F`) como representação compacta do binário, onde **1 dígito hexadecimal corresponde exatamente a 4 bits (*nibble*)** e **1 Byte (8 bits) é representado por 2 dígitos hexadecimais**.

---

## Sistemas de Representação Numérica

Os números podem ser representados em diferentes bases:
* **Decimal (base 10)**: sistema humano (10 dedos), composto por 10 símbolos: `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]`.
* **Binário (base 2)**: representação computacional (2 níveis de tensão elétrica), composto por 2 símbolos: `[0, 1]`.
* **Hexadecimal (base 16)**: representação compacta de números binários, composta por 16 símbolos: `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, A, B, C, D, E, F]`, onde:
  $$A = 10,\quad B = 11,\quad C = 12,\quad D = 13,\quad E = 14,\quad F = 15$$
* Existem outros sistemas numéricos utilizados em computação, como o **octal** (base 8).

---

## Notação Posicional e Fórmula Genérica de Conversão para Decimal

Cada símbolo possui um peso que depende da sua posição no número.

* **Símbolo mais significativo (*most significant symbol / digit*)**: o valor mais à **esquerda** (*leftmost value*).
* **Símbolo menos significativo (*less significant symbol / digit*)**: o valor mais à **direita** (*rightmost value*).

### Fórmula Genérica (Qualquer Base $b \rightarrow$ Decimal)
$$s_p \times b^p + \dots + s_1 \times b^1 + s_0 \times b^0$$
Onde:
* $s$ — valor numérico do símbolo.
* $b$ — base original (binária $2$, octal $8$, hexadecimal $16$, etc.).
* $p$ — posição do símbolo, que começa em zero ($0$) e aumenta da direita para a esquerda.

---

## Exemplos Práticos de Conversão

### 1. Decomposição Decimal ($35\,812_d$)
$$3 \times 10^4 + 5 \times 10^3 + 8 \times 10^2 + 1 \times 10^1 + 2 \times 10^0$$
$$= 3 \times 10\,000 + 5 \times 1\,000 + 8 \times 100 + 1 \times 10 + 2 \times 1 = 30\,000 + 5\,000 + 800 + 10 + 2 = 35\,812$$
* Símbolo mais significativo: `3` (esquerda); menos significativo: `2` (direita).

### 2. Binário para Decimal ($1001\,0011_b$)
$$1 \times 2^7 + 0 \times 2^6 + 0 \times 2^5 + 1 \times 2^4 + 0 \times 2^3 + 0 \times 2^2 + 1 \times 2^1 + 1 \times 2^0$$
$$= 128 + 0 + 0 + 16 + 0 + 0 + 2 + 1 = 147_d$$
* Dígito mais significativo: o `1` na posição $p=7$ (peso $128$); menos significativo: o `1` na posição $p=0$ (peso $1$).

### 3. Hexadecimal para Decimal ($8\text{BE}4_h$ ou `0x8BE4`)
$$8 \times 16^3 + 11 \times 16^2 + 14 \times 16^1 + 4 \times 16^0$$
$$= 8 \times 4\,096 + 11 \times 256 + 14 \times 16 + 4 \times 1 = 32\,768 + 2\,816 + 224 + 4 = 35\,812_d$$

---

## Conversão Direta entre Binário e Hexadecimal

| Decimal | Binário | Hexadecimal | Decimal | Binário | Hexadecimal |
| :---: | :---: | :---: | :---: | :---: | :---: |
| `0` | `0000` | `0x0` | `8` | `1000` | `0x8` |
| `1` | `0001` | `0x1` | `9` | `1001` | `0x9` |
| `2` | `0010` | `0x2` | `10` | `1010` | `0xA` |
| `3` | `0011` | `0x3` | `11` | `1011` | `0xB` |
| `4` | `0100` | `0x4` | `12` | `1100` | `0xC` |
| `5` | `0101` | `0x5` | `13` | `1101` | `0xD` |
| `6` | `0110` | `0x6` | `14` | `1110` | `0xE` |
| `7` | `0111` | `0x7` | `15` | `1111` | `0xF` |

### Exemplo de Conversão Direta ($1001\,0011_b \rightarrow \text{0x93}$)
Agrupando os bits de 4 em 4:
* $1001_b = \text{0x9}$
* $0011_b = \text{0x3}$
* Resultado: $1001\,0011_b = \text{0x93}$

> [!IMPORTANT] Relação Fundamental de Tamanho
> $$\text{1 Byte} = \text{8 bits} = \text{2 dígitos hexadecimais}$$

---

## Implicações Forenses

* **Leitura de Editores Hexadecimais (*Hex Dumps*)**: Quando um perito inspeciona setores de disco ou estruturas binárias num editor hexadecimal, cada par de caracteres (ex.: `4D`, `69`, `FF`) representa exatamente **1 Byte** de armazenamento físico.

---

## Perguntas de revisão

- Qual é a fórmula genérica para converter um número de qualquer base $b$ para a base decimal?
- Como se converte diretamente um byte em binário ($1001\,0011_b$) para hexadecimal sem passar pela base decimal?
- Quantos bits e quantos dígitos hexadecimais compõem 1 Byte?

## Notas relacionadas

- [[Números em Vírgula Flutuante (IEEE 754)]]
- [[Endianness e Ordem de Armazenamento]]
- [[Organização de Estruturas de Dados em Binário]]
- [[Capítulo 3 - Organização de Dados]]
