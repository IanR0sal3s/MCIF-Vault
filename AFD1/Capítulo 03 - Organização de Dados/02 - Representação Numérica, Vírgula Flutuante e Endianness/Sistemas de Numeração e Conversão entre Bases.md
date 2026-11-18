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
atualizado: 2026-11-11
---

# Sistemas de Numeração e Conversão entre Bases

Enquanto os computadores operam em binário, a análise forense utiliza o sistema hexadecimal como notação compacta, onde cada dígito representa quatro bits e dois dígitos formam um Byte.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Representação)**: Circuitos digitais distinguem apenas dois níveis de tensão (`0` e `1`), mas sequências binárias extensas são ilegíveis para humanos; a base 16 agrupa exatamente 4 bits por símbolo (*nibble*), comprimindo 1 Byte em dois caracteres.
> * **Porque importa (Forense)**: Editores hexadecimais expõem discos, registos de memória e pacotes de rede em pares de dígitos hexadecimais, permitindo localizar *magic bytes*, calcular *offsets* e descodificar campos inteiros manualmente.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Regra de tamanho**: $\text{1 Byte} = \text{8 bits} = \text{2 dígitos hexadecimais}$ (intervalo `0x00` a `0xFF`, ou `0` a `255`).
>   * **Notação posicional**: na fórmula $\sum s_p \times b^p$, a posição $p$ começa em **`0` à direita** (*LSD/LSB*) e cresce para a esquerda (*MSD/MSB*).
>   * **Conversão direta**: para passar de binário para hexadecimal (e vice-versa) **não é necessário converter para decimal**; basta agrupar os bits em blocos de 4 da direita para a esquerda.

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

* **Símbolo mais significativo (*MSD / MSB*)**: o valor mais à **esquerda**.
* **Símbolo menos significativo (*LSD / LSB*)**: o valor mais à **direita**.

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

## Além da aula

* **Aplicações Diretas de Conversão Binário/Hexadecimal em Artefactos do Windows ([[00 ASSI|ASSI]])**:
  * **Codificação de Inteiros de Comprimento Variável ([[Codificação uLEB128 em Estruturas de Dados do Windows]])**: Utilizada nos ficheiros `TabState` do [[Artefacto Forense do Bloco de Notas (Notepad Windows 11)]], exige converter o número decimal para binário, agrupá-lo em blocos de 7 bits (usando o *MSB* — Bit 7 — como bit de continuação) e representar o resultado em hexadecimal (ex.: $301_d = 100101101_b \rightarrow \text{0xAD 0x02}$).
  * **Assinaturas Mágicas (*Magic Bytes*) e Trailers de Carving**: A leitura hexadecimal ao nível do byte permite validar cabeçalhos de executáveis e bases de dados no editor HxD, tais como `4D 5A` / `50 45 00 00` em cabeçalhos PE ([[Arquitetura 32 vs 64 bits no Registry e Executáveis (WOW6432Node)]]), `53 51 4C 69 74 65...` em [[Windows Search|SQLite 3]], `4D 41 4D 04` (`MAM`) ou `53 43 43 41` (`SCCA`) em [[Estrutura Interna e Algoritmo de Hashing do Prefetch|ficheiros Prefetch]], `4C 00 00 00` em [[Ficheiros LNK (Shell Links) - Metadados e Formato Binário|atalhos LNK]], `57 69 6E 34` (`Win4`) na [[Caches de Ícones e Miniaturas (IconCache e Thumbcache)|IconCache]], `4E 50` (`NP`) no Bloco de Notas e o trailer `AB FB BF BA` nas [[Jump Lists - Arquitetura, AppIDs e Carving|Jump Lists Customizadas]].

---

## Perguntas de revisão

1. **Qual é a fórmula genérica para converter um número de qualquer base $b$ para a base decimal e como se atribui o índice $p$?**

> [!success]- Ver Resposta
> A fórmula polinomial é $s_p \times b^p + \dots + s_1 \times b^1 + s_0 \times b^0$, onde $s$ é o valor numérico de cada símbolo, $b$ é a base original (ex.: $2$, $8$ ou $16$) e $p$ é a posição do dígito, começando em **`0` à direita** e aumentando para a esquerda.

2. **Converta o valor hexadecimal `0x8BE4` para decimal mostrando o cálculo posicional completo.**

> [!success]- Ver Resposta
> Substituindo $B = 11$ e $E = 14$: $8 \times 16^3 + 11 \times 16^2 + 14 \times 16^1 + 4 \times 16^0 = 32\,768 + 2\,816 + 224 + 4 = \mathbf{35\,812_d}$.

3. **Como se converte diretamente o byte binário `1001 0011` para hexadecimal sem passar pela base decimal?**

> [!success]- Ver Resposta
> Agrupam-se os bits em blocos de **4 bits** da direita para a esquerda: $1001_b = \text{0x9}$ e $0011_b = \text{0x3}$, resultando diretamente em **`0x93`**.

4. **Quantos bits e quantos dígitos hexadecimais compõem 1 Byte, e porque é o sistema hexadecimal preferido em editores forenses?**

> [!success]- Ver Resposta
> **1 Byte equivale a 8 bits e a exatamente 2 dígitos hexadecimais**. O sistema hexadecimal representa diretamente blocos de 4 bits (*nibbles*) sem o comprimento excessivo do binário nem a falta de alinhamento posicional da base 10.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Camadas de Organização de Dados e Análise de Sistemas de Ficheiros]] | `Bloco 01` |
| **Seguinte** | [[Números em Vírgula Flutuante (IEEE 754)]] | `mesmo bloco` |
| **Índice** | [[Capítulo 3 - Organização de Dados]] · [[00 AFD1]] | `Bloco 02` |

### Conceitos Relacionados

* [[Endianness e Ordem de Armazenamento]] · `mesmo bloco`
* [[Organização de Estruturas de Dados em Binário]] · `Bloco 03`
* [[Codificação uLEB128 em Estruturas de Dados do Windows]] · `ASSI · Cap. 1`
* [[Arquitetura 32 vs 64 bits no Registry e Executáveis (WOW6432Node)]] · `ASSI · Cap. 1`
* [[Estrutura Interna e Algoritmo de Hashing do Prefetch]] · `ASSI · Cap. 1`
* [[Jump Lists - Arquitetura, AppIDs e Carving]] · `ASSI · Cap. 1`
