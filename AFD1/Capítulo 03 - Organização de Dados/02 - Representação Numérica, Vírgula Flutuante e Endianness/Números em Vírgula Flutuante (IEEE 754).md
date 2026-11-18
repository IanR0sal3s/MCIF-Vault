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
atualizado: 2026-11-11
---

# Números em Vírgula Flutuante (IEEE 754)

A norma IEEE 754 codifica números reais em binário usando sinal, expoente em excesso e mantissa normalizada nos formatos de precisão simples de 32 bits e precisão dupla de 64 bits.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Representação)**: Representar números reais muito grandes ou fracionários em largura fixa exige notação científica binária; o expoente em excesso simplifica comparações de grandeza e a omissão do `1` implícito na mantissa normalizada ganha 1 bit extra de precisão.
> * **Porque importa (Forense)**: Campos `float` e `double` surgem frequentemente em bases de dados, telemetria, coordenadas GPS e estruturas C; saber reconhecer o padrão de bits e combinar com *endianness* evita interpretar valores decimais como lixo ou inteiros absurdos.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Precisão simples (`float`, 32 bits)**: `1` bit de sinal + `8` bits de expoente (excesso **`127`**, intervalo $[2^{-126}, 2^{+127}]$) + `23` bits de mantissa.
>   * **Precisão dupla (`double`, 64 bits)**: `1` bit de sinal + `11` bits de expoente (excesso **`1023`**, intervalo $[2^{-1022}, 2^{+1023}]$) + `52` bits de mantissa.
>   * **Indicador visual de `float` próximo de $1{,}0$–$2{,}0$**: o byte mais significativo situa-se em `0x3F` ou `0x40`; em Little-endian surge à direita (ex.: `c9 76 9e 3f` $\rightarrow$ `0x3F9E76C9` $\approx 1{,}238$).

---

## Formato IEEE 754

* **Norma de referência**: **IEEE 754**.
* **Expoente em excesso**: permite realizar comparações diretas entre números de vírgula flutuante.
* **Mantissa (ou *significand*)**:
  * **Normalizada**: o dígito binário `1` imediatamente à esquerda da vírgula é **omitido** (implícito), maximizando os bits úteis de precisão.
  * Em operações de adição e subtração é **desnormalizada**, ocorrendo contudo uma perda gradual de precisão.

---

## Precisão Simples (32 bits) vs. Precisão Dupla (64 bits)

| Formato | Tamanho Total | Bit de Sinal | Expoente | Excesso e Intervalo do Expoente | Mantissa (*Significand*) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Precisão Simples** (`float`) | **32 bits** (4 Bytes) | 1 bit | **8 bits** | Excesso de **127** $\rightarrow [2^{-126}, 2^{+127}]$ | **23 bits** |
| **Precisão Dupla** (`double`) | **64 bits** (8 Bytes) | 1 bit | **11 bits** | Excesso de **1023** $\rightarrow [2^{-1022}, 2^{+1023}]$ | **52 bits** |

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

* **Ferramenta de conversão**: [Conversor IEEE 754](http://www.h-schmidt.net/FloatConverter/IEEE754.html)

---

## Exemplo Passo a Passo: Descodificação de `0x3F9E76C9` (Precisão Simples)

No caso de estudo de [[Organização de Estruturas de Dados em Binário]], o campo `float quota` surge no *hex dump* como `c9 76 9e 3f` (em Little-endian, correspondendo à palavra **`0x3F9E76C9`**):

**1. Conversão para binário (32 bits):**

$$0\text{x3F9E76C9} = \underbrace{0}_{\text{Sinal}} \;\; \underbrace{01111111}_{\text{Expoente (8 bits)}} \;\; \underbrace{00111100111011011001001}_{\text{Mantissa (23 bits)}}$$

**2. Sinal:** `0` $\rightarrow (-1)^0 = +1$ (valor positivo).

**3. Expoente:** `01111111`$_2 = 127_{10}$; subtraindo o excesso `127`, obtém-se $127 - 127 = 0 \implies 2^0 = 1$.

**4. Mantissa normalizada:** repõe-se o bit `1` implícito à esquerda da vírgula (`1.00111100111011011001001`$_2$), somando as potências negativas de base 2:

$$1 + 2^{-3} + 2^{-4} + 2^{-5} + 2^{-6} + 2^{-9} + 2^{-10} + 2^{-11} + 2^{-13} + 2^{-14} + 2^{-16} + 2^{-17} + 2^{-20} + 2^{-23} \approx 1{,}238000035$$

**5. Resultado final:** $+1 \times 2^0 \times 1{,}238000035 \approx \mathbf{1{,}238}$.

---

## Implicações Forenses

* **Identificação de `float` em Estruturas Binárias**: Ao analisar um *hex dump* de uma estrutura de dados (como no caso prático de [[Organização de Estruturas de Dados em Binário]]), valores em vírgula flutuante de 32 bits próximos de $1{,}0$ a $2{,}0$ apresentam frequentemente o byte mais significativo em torno de `0x3F` ou `0x40` (pois o sinal é `0` e o expoente em excesso de 127 situa-se perto de `01111111` = `127`). Se esse byte `3F` aparecer no endereço mais alto (à direita de um grupo de 4 bytes, ex.: `c9 76 9e 3f`), trata-se de um forte indicador visual de armazenamento **Little-endian**.

---

## Perguntas de revisão

1. **Quais são os três campos que compõem um número em vírgula flutuante segundo a norma IEEE 754?**

> [!success]- Ver Resposta
> Um número IEEE 754 divide-se em **Bit de Sinal** (indica se o número é positivo `0` ou negativo `1`), **Expoente em excesso** (define a ordem de grandeza em potência de 2) e **Mantissa ou *significand*** (armazena os bits fracionários significativos após o `1` implícito).

2. **Porque se utiliza expoente em excesso e o que significa dizer que a mantissa está normalizada (bem como o risco da desnormalização)?**

> [!success]- Ver Resposta
> O **expoente em excesso** permite realizar comparações diretas de grandeza entre números em vírgula flutuante sem tratamento separado de sinal do expoente. Dizer que a mantissa está **normalizada** significa que o dígito binário `1` à esquerda da vírgula é **omitido** (implícito), ganhando precisão; durante adições e subtrações, a mantissa é **desnormalizada**, podendo ocorrer perda gradual de precisão.

3. **Quantos bits são atribuídos ao sinal, ao expoente e à mantissa em precisão simples (32 bits) e em precisão dupla (64 bits), e quais os respetivos excessos?**

> [!success]- Ver Resposta
> * **Precisão simples (32 bits / `float`)**: `1` bit de sinal, **`8` bits** de expoente com **excesso `127`** (intervalo $[2^{-126}, 2^{+127}]$) e **`23` bits** de mantissa.
> * **Precisão dupla (64 bits / `double`)**: `1` bit de sinal, **`11` bits** de expoente com **excesso `1023`** (intervalo $[2^{-1022}, 2^{+1023}]$) e **`52` bits** de mantissa.

4. **Como se verifica manualmente que `0x3F9E76C9` representa o valor positivo $\approx 1{,}238$ em precisão simples?**

> [!success]- Ver Resposta
> Em binário (`0 01111111 00111100111011011001001`), o bit de sinal é `0` (positivo), o expoente `01111111` vale $127 - 127 = 0$ ($2^0 = 1$) e a mantissa com o `1` implícito reposto vale `1.00111100111011011001001`$_2 \approx 1{,}238000035$, resultando em **`1,238`**.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Sistemas de Numeração e Conversão entre Bases]] | `mesmo bloco` |
| **Seguinte** | [[Endianness e Ordem de Armazenamento]] | `mesmo bloco` |
| **Índice** | [[Capítulo 3 - Organização de Dados]] · [[00 AFD1]] | `Bloco 02` |

### Conceitos Relacionados

* [[Organização de Estruturas de Dados em Binário]] · `Bloco 03`
