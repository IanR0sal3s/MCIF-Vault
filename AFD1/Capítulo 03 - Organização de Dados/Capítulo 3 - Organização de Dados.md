---
title: Capítulo 3 - Organização de Dados
tipo: indice
mestrado: Cibersegurança e Informática Forense
uc: Análise Forense Digital I
sigla_uc: AFD1
capitulo: 3
fonte_aula: MCIF – Digital Forensic Analysis 1 - Data Organization.pdf
tags:
  - moc
  - afd1
  - forense
  - organizacao-dados
  - endianness
  - encoding
  - timestamps
aliases:
  - Capítulo 3 AFD1
  - Data Organization
  - Organização de Dados
atualizado: 2026-10-19
---

# Capítulo 3 — Organização de Dados (*Data Organization*)

Índice temático e encadeamento pedagógico do **Capítulo 3 (*Data Organization*)** da unidade curricular de [[00 AFD1|Análise Forense Digital I (AFD1)]], lecionada pelos docentes **Miguel Frade** e **Baltazar Rodrigues** (LabCIF).

As notas encontram-se organizadas em **4 blocos temáticos numerados** na pasta `AFD1/Capítulo 03 - Organização de Dados/`, cobrindo os 34 diapositivos da apresentação oficial.

---

## 1. Camadas de Organização e Análise de Sistemas de Ficheiros (`01 - Camadas de Organização e Análise de Sistemas de Ficheiros`)

| Nota | Descrição e Foco Técnico |
| :--- | :--- |
| [[Camadas de Organização de Dados e Análise de Sistemas de Ficheiros]] | As 4 camadas de organização e análise (Meios Físicos/Rede, Memória Volátil/Volumes, Sistemas de Ficheiros/Swap/Bases de Dados e SO/Aplicações); foco em **File System Analysis**; distinção entre **Dados Essenciais** (nome e cluster) e **Dados Não Essenciais** (*timestamps*); pipeline desde os setores do disco até à aplicação |

---

## 2. Representação Numérica, Vírgula Flutuante e Endianness (`02 - Representação Numérica, Vírgula Flutuante e Endianness`)

| Nota | Descrição e Foco Técnico |
| :--- | :--- |
| [[Sistemas de Numeração e Conversão entre Bases]] | Representação decimal, binária, hexadecimal e octal; notação posicional, *MSB* vs. *LSB*, fórmula polinomial genérica de conversão para decimal e conversão direta binário $\leftrightarrow$ hexadecimal ($1\text{ Byte} = 2\text{ dígitos hex}$) |
| [[Números em Vírgula Flutuante (IEEE 754)]] | Norma **IEEE 754**, bit de sinal, expoente em excesso (comparação direta) e mantissa normalizada (omissão do bit `1` inteiro); formatos de precisão simples (32 bits, excesso 127) e precisão dupla (64 bits, excesso 1023) |
| [[Endianness e Ordem de Armazenamento]] | Ordenação de valores multi-byte (16, 32, 64 bits): **Big-endian** vs. **Little-endian** (exemplo `0x12345678`), famílias de processadores (`SPARC`/`PowerPC`/`MIPS` vs. `x86`/`x86-64` vs. `ARM` bi-endian) e *network byte order* (IP) |

---

## 3. Codificação de Caracteres e Estruturas de Dados (`03 - Codificação de Caracteres e Estruturas de Dados`)

| Nota | Descrição e Foco Técnico |
| :--- | :--- |
| [[Codificação de Caracteres - ASCII, Latin-1 e Unicode]] | Codificação **ASCII** (7 bits, imune a *endianness*), extensões de 8 bits (**Latin-1 / ISO-8859-1**) e **Unicode** (**UTF-8** de 1–4 bytes imune a *endianness*, **UTF-16** de 2–4 bytes e **UTF-32** de 4 bytes); análise comparativa em hexadecimal da string `"Olá"` |
| [[Organização de Estruturas de Dados em Binário]] | Estruturas de dados como mapas interpretativos; caso de estudo de `typedef struct` em C (64 bytes com *padding*) e descodificação passo a passo de *hex dump* (`partner_num` e `quota` IEEE 754) em Big-endian vs. Little-endian |

---

## 4. Data, Hora e Codificação Binário-para-Texto (`04 - Data, Hora e Codificação Binário-para-Texto`)

| Nota | Descrição e Foco Técnico |
| :--- | :--- |
| [[Representação Forense de Data e Hora (Timestamps e SQLite)]] | Representação textual vs. binária/hexadecimal; contagem em **Unix Epoch** (`1970-01-01`, segundos) e **Ciclo Gregoriano de 400 anos** (`1601-01-01`, microssegundos); tabela de 14 formatos de software; ferramentas (`MFT Stampede`, `BrowsingHistoryView`) e queries SQLite forenses para **Firefox** e **Google Chrome** |
| [[Codificação Binário-para-Texto (Base16, Base64 e Base58)]] | Conceito de *binary-to-text encoding*, inflação de dados, reversibilidade e distinção face a **encriptação** (sem chave secreta); características e aplicações de **Hexadecimal (Base16)**, **Base64** (MIME, OpenPGP, *padding* `=`) e **Base58** (chaves Bitcoin) |

> [!NOTE] Exercícios Laboratoriais do Capítulo 3 (Slide 34)
> O diapositivo 34 referencia três exercícios práticos de laboratório (*Lab 1 – Endianness, read binary file*, *Lab 2 – Identify different character encodings* e *Lab 3 – Character encoding conversions*), cujos guiões detalhados serão integrados assim que disponibilizados.

---

## 🧭 Navegação

* [[00 AFD1|Voltar ao Índice de AFD1]]
* [[Capítulo 2 - Arranque e Aquisição Forense|Recuar para o Capítulo 2 — Arranque e Aquisição Forense]]
* [[Capítulo 1 - Método de Investigação|Recuar para o Capítulo 1 — Método de Investigação]]
* [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses|Pontes com ASSI — Capítulo 1 (Estruturas Binárias, Timestamps e SQLite no Windows)]]
* [[Home|Voltar ao Hub Central do MCIF]]
