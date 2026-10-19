---
title: Números em Vírgula Flutuante (IEEE 754)
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
  - ieee-754
  - floating-point
  - representacao-numerica
aliases:
  - Floating Point Numbers
  - IEEE 754
  - Vírgula Flutuante
atualizado: 2026-10-19
---

# Números em Vírgula Flutuante (IEEE 754)

A representação binária de números reais em vírgula flutuante rege-se pela norma **IEEE 754**, dividindo a palavra binária em três campos: **Sinal** (1 bit), **Expoente em excesso** (que viabiliza comparações diretas de grandeza) e **Mantissa normalizada** (na qual o dígito binário `1` à esquerda da vírgula é omitido). As duas variantes fundamentais são a **precisão simples (32 bits / `float`)** e a **precisão dupla (64 bits / `double`)**.

---

## Formato IEEE 754

* **Norma de referência**: **IEEE 754 standard**.
* **Expoente em excesso (*exponent in excess*)**: permite realizar comparações diretas entre números de vírgula flutuante.
* **Mantissa (ou *significand*)**:
  * **Normalizada (*normalized*)**: o dígito binário `1` imediatamente à esquerda da vírgula é **omitido** (implícito), maximizando os bits úteis de precisão.
  * Em operações de adição e subtração é **desnormalizada**, ocorrendo contudo uma perda gradual de precisão (*gradual loss of accuracy*).

---

## Precisão Simples (32 bits) vs. Precisão Dupla (64 bits)

| Formato | Tamanho Total | Bit de Sinal (*Signal*) | Expoente (*Exponent*) | Excesso e Intervalo do Expoente | Mantissa (*Significand*) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Precisão Simples** (*Single precision* / `float`) | **32 bits** (4 Bytes) | 1 bit | **8 bits** | Excesso de **127** $\rightarrow [2^{-126}, 2^{+127}]$ | **23 bits** |
| **Precisão Dupla** (*Double precision* / `double`) | **64 bits** (8 Bytes) | 1 bit | **11 bits** | Excesso de **1023** $\rightarrow [2^{-1022}, 2^{+1023}]$ | **52 bits** |

### Esquema de Bits — Precisão Simples (32 bits)
```text
+------------+------------------+------------------------------------+
|   Signal   |     Exponent     |      Mantissa (or significand)     |
|   1 bit    |      8 bits      |              23 bits               |
+------------+------------------+------------------------------------+
```

### Esquema de Bits — Precisão Dupla (64 bits)
```text
+------------+--------------------+--------------------------------------------------+
|   Signal   |      Exponent      |             Mantissa (or significand)            |
|   1 bit    |      11 bits       |                     52 bits                      |
+------------+--------------------+--------------------------------------------------+
```

* **Ferramenta de conversão**:
  * Conversor interativo IEEE 754: `http://www.h-schmidt.net/FloatConverter/IEEE754.html`

---

## Implicações Forenses

* **Identificação de `float` em Estruturas Binárias**: Ao analisar um *dump* hexadecimal de uma estrutura de dados (como no caso prático de [[Organização de Estruturas de Dados em Binário]]), valores em vírgula flutuante de 32 bits próximos de $1{,}0$ a $2{,}0$ apresentam frequentemente o byte mais significativo em torno de `0x3F` ou `0x40` (pois o sinal é `0` e o expoente em excesso de 127 situa-se perto de `01111111` = `127`). Se esse byte `3F` aparecer no endereço mais alto (à direita de um grupo de 4 bytes, ex.: `c9 76 9e 3f`), trata-se de um forte indicador visual de armazenamento **Little-endian**.

---

## Perguntas de revisão

- Quais são os três campos que compõem um número em vírgula flutuante segundo a norma IEEE 754?
- Porque se utiliza a representação de expoente em excesso e o que significa dizer que a mantissa está normalizada?
- Quantos bits são atribuídos ao sinal, ao expoente e à mantissa em precisão simples (32 bits) e em precisão dupla (64 bits)?

## Notas relacionadas

- [[Sistemas de Numeração e Conversão entre Bases]]
- [[Endianness e Ordem de Armazenamento]]
- [[Organização de Estruturas de Dados em Binário]]
- [[Capítulo 3 - Organização de Dados]]
