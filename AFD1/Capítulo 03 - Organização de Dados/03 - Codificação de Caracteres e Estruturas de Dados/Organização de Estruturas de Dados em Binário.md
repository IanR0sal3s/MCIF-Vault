---
title: Organização de Estruturas de Dados em Binário
tipo: analise
mestrado: Cibersegurança e Informática Forense
uc: Análise Forense Digital I
sigla_uc: AFD1
capitulo: 3
bloco: 3
fonte_aula: MCIF – Digital Forensic Analysis 1 - Data Organization.pdf
tags:
  - afd1
  - forense
  - estruturas-dados
  - struct
  - hex-dump
  - endianness
aliases:
  - Data Structures Organization
  - Análise de Struct em Hexadecimal
atualizado: 2026-10-19
---

# Organização de Estruturas de Dados em Binário

Uma **estrutura de dados (*data structure*)** especifica como os diferentes campos são dispostos em memória ou em disco, funcionando como um **mapa interpretativo**: a definição da estrutura em si (nomes de campos e tipos de dados) **não é gravada** no ficheiro binário. Através de um caso de estudo de uma `struct` em linguagem C de 64 bytes, demonstra-se como mapear *offsets* hexadecimais, identificar bytes de alinhamento (*padding*) e determinar o *endianness* do sistema analisando inteiros de 32 bits (`uint32_t`) e números em vírgula flutuante (`float` IEEE 754).

---

## Conceito de Estrutura de Dados (*Data Structures*)

* Especifica a forma como os dados são posicionados (*placed*) em memória ou armazenamento.
* Funciona exatamente como um **mapa**.
* **A estrutura de dados em si não é gravada** no suporte — apenas os bytes brutos dos valores são armazenados sequencialmente.

---

## Caso de Estudo: `struct` em Linguagem C e Análise em Hexadecimal

### 1. Definição da Estrutura (64 Bytes)
```c
typedef struct {
    char name[32];         // 32 bytes (Offsets 0x00 a 0x1F)
    char postalcode[16];   // 16 bytes (Offsets 0x20 a 0x2F)
    uint32_t partner_num;  // 4 bytes  (Offsets 0x30 a 0x33)
    float quota;           // 4 bytes  (Offsets 0x34 a 0x37)
    char empty[8];         // 8 bytes to lineup the structure to multiples of 16 bytes (0x38 a 0x3F)
};                         // Total = 64 bytes (0x40 bytes)
```

### 2. Dados Registados em Hexadecimal (*Hex Dump*)
```text
0000000: 4d69 6775 656c 2046 7261 6465 0000 0000  Miguel Frade....
0000010: 0000 0000 0000 0000 0000 0000 0000 0000  ................
0000020: 3234 3131 2d39 3031 0000 0000 0000 0000  2411-901........
0000030: b300 0d00 c976 9e3f 0000 0000 0000 0000  .....v.?........
```

---

## Resolução e Mapeamento Campo a Campo

| Campo da `struct` | Offset Hexadecimal | Tamanho | Bytes Extraídos do *Hex Dump* | Interpretação |
| :--- | :---: | :---: | :--- | :--- |
| `char name[32]` | `0x00` – `0x1F` | 32 B | `4d 69 67 75 65 6c 20 46 72 61 64 65 00...` | String ASCII terminada em nulo: `"Miguel Frade"` |
| `char postalcode[16]` | `0x20` – `0x2F` | 16 B | `32 34 31 31 2d 39 30 31 00...` | String ASCII terminada em nulo: `"2411-901"` |
| `uint32_t partner_num` | `0x30` – `0x33` | 4 B | `b3 00 0d 00` | Inteiro sem sinal de 32 bits (depende do *endianness*) |
| `float quota` | `0x34` – `0x37` | 4 B | `c9 76 9e 3f` | Vírgula flutuante IEEE 754 de 32 bits (depende do *endianness*) |
| `char empty[8]` | `0x38` – `0x3F` | 8 B | `00 00 00 00 00 00 00 00` | *Padding* para alinhar a estrutura a múltiplos de 16 bytes |

### Questões de Análise Forense
1. **Qual é o número de sócio (`partner_num`) em hexadecimal?** É `0xb300 0d00` ou `0x000d 00b3`?
2. **Qual é o valor da quota (`quota`) em hexadecimal?** É `0xc976 9e3f` ou `0x3f9e 76c9`?
3. **Este sistema é *Little-endian* ou *Big-endian*?**

### Comparação das Duas Hipóteses de Endianness
* **Hipótese 1 — Se o sistema fosse *Big-endian***:
  * `partner_num`: `0xb3000d00` $= 3\,003\,124\,992_d$
  * `quota`: `0xc9769e3f` $= -1\,010\,147{,}94_d$ (valor negativo absurdo para uma quota de sócio)
* **Hipótese 2 — Se o sistema for *Little-endian*** (invertendo a ordem dos 4 bytes de cada campo numérico):
  * `partner_num`: `b3 00 0d 00` $\rightarrow$ **`0x000d00b3`** $= 852\,147_d$
  * `quota`: `c9 76 9e 3f` $\rightarrow$ **`0x3f9e76c9`** $= 1{,}238_d$

### Confirmação pelo Código-Fonte Original
```c
strcpy(partners[0].name, "Miguel Frade");
strcpy(partners[0].postalcode, "2411-901");
partners[0].partner_num=852147;
partners[0].quota=1.238;
```
* **Conclusão**: O sistema onde a estrutura foi gravada é **Little-endian**. Note-se que os arrays de caracteres (`name` e `postalcode`) mantêm sempre a ordem normal de leitura byte a byte (`4d 69...` = `'M'`, `'i'`, ...), enquanto os campos numéricos multi-byte (`uint32_t` e `float` de 4 bytes) têm os seus bytes invertidos em memória.

---

## Implicações Forenses

* **Engenharia Reversa de Formatos Proprietários**: Mesmo sem acesso ao código-fonte original, um perito forense consegue deduzir o *endianness* de um ficheiro binário observando a plausibilidade semântica dos valores descodificados (por exemplo, um número de sócio de 6 dígitos versus 3 mil milhões, ou uma quota positiva pequena `1,238` versus um número negativo na ordem do milhão).

---

## Perguntas de revisão

- Porque é que na análise do *hex dump* as strings `"Miguel Frade"` e `"2411-901"` se leem da esquerda para a direita sem inversão, mas os campos `partner_num` e `quota` têm os bytes invertidos?
- Qual é a finalidade do campo `char empty[8]` na estrutura apresentada?
- Como é que a análise do valor `float quota` (`c9 76 9e 3f`) permite concluir se o sistema é Little-endian ou Big-endian mesmo sem conhecer o código-fonte?

## Notas relacionadas

- [[Endianness e Ordem de Armazenamento]]
- [[Números em Vírgula Flutuante (IEEE 754)]]
- [[Codificação de Caracteres - ASCII, Latin-1 e Unicode]]
- [[Camadas de Organização de Dados e Análise de Sistemas de Ficheiros]]
- [[Capítulo 3 - Organização de Dados]]
