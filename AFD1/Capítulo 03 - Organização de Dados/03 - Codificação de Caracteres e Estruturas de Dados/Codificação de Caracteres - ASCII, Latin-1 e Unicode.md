---
title: Codificação de Caracteres - ASCII, Latin-1 e Unicode
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Análise Forense Digital I
sigla_uc: AFD1
capitulo: 3
bloco: 3
fonte_aula: MCIF – Digital Forensic Analysis 1 - Data Organization.pdf
tags:
  - afd1
  - forense
  - ascii
  - latin1
  - unicode
  - utf8
  - utf16
aliases:
  - Character Encoding
  - ASCII
  - Latin-1
  - ISO-8859-1
  - Unicode
  - UTF-8
  - UTF-16
atualizado: 2026-10-19
---

# Codificação de Caracteres — ASCII, Latin-1 e Unicode

A codificação de caracteres traduz símbolos de texto em valores binários/hexadecimais: o padrão **ASCII** (7 bits, 128 caracteres) e as suas extensões de 8 bits como o **Latin-1 (ISO-8859-1)** operam byte a byte (sem problemas de *endianness*), mas têm suporte multilingue limitado. O padrão **Unicode** (mais de 137.000 caracteres em 146 grafias) resolve esta limitação através de implementações como **UTF-8** (1 a 4 bytes, compatível com ASCII e imune a *endianness*), **UTF-16** (2 a 4 bytes, usado em Windows/macOS/Java/.NET) e **UTF-32** (4 bytes fixos).

---

## 1. Codificação de Caracteres — ASCII e Latin-1

### Vantagens do ASCII
* É a forma mais simples de codificar caracteres.
* **Não tem problemas de *endianness***, uma vez que utiliza **1 byte de cada vez** (*1 byte at a time*).
* A versão original utiliza apenas **7 bits**, permitindo **128 caracteres diferentes** (tabela de referência: `http://www.asciitable.com/`).
* Ocupa menos espaço de armazenamento do que o Unicode (para conjuntos de caracteres compatíveis com representações multi-byte fixas).

### Desvantagens do ASCII e Extensões de 8 bits
* Capacidade muito limitada para representar caracteres não ingleses (acentos, cedilhas, alfabetos não latinos).
* Existem várias **versões estendidas de 8 bits** (256 caracteres):
  * A mais conhecida é o **Latin-1** (**ISO-8859-1** — `http://cs.stanford.edu/people/miles/iso8859.html`).

### Exemplo em Memória (ASCII): `"2670-582 LOURES"`

| Endereço (*Address*) | `10` | `11` | `12` | `13` | `14` | `15` | `16` | `17` | `18` | `19` | `20` | `21` | `22` | `23` | `24` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Hexadecimal** | `32` | `36` | `37` | `30` | `2D` | `35` | `38` | `32` | `20` | `4C` | `4F` | `55` | `52` | `45` | `53` |
| **Texto (ASCII)** | `2` | `6` | `7` | `0` | `-` | `5` | `8` | `2` | ` ` | `L` | `O` | `U` | `R` | `E` | `S` |

*(Nota: `0x20` corresponde ao espaço em branco, `0x30`–`0x39` aos algarismos `0`–`9` e `0x41`–`0x5A` às letras maiúsculas `A`–`Z`).*

---

## 2. Codificação de Caracteres — Unicode

### Vantagens do Unicode
* Possui **mais de 137.000 caracteres**.
* Abrange **146 sistemas de escrita (*scripts*) modernos e históricos**, bem como múltiplos conjuntos de símbolos.

### Desvantagens e Implementações do Unicode
* Processamento computacional mais complexo.
* Existem **várias implementações** distintas:

| Implementação | Tamanho por Carácter | Características e Sistemas onde é Utilizado |
| :--- | :--- | :--- |
| **UTF-8** | Variável: **1 a 4 bytes** | Compatível com ASCII (caracteres ASCII ocupam 1 byte com o mesmo código); usado em sistemas **`*nix` (Unix/Linux), WWW, HTML**, etc. **Não está sujeito a problemas de *endianness*** porque é lido 1 byte de cada vez. |
| **UTF-16** | Variável: **2 a 4 bytes** | Utilizado internamente no **Windows, Mac OS, Java, .Net, KDE**, etc. (sujeito a *endianness*: UTF-16LE / UTF-16BE). |
| **UTF-32** | Fixo: **4 bytes** | Comprimento fixo de 32 bits por carácter. |

---

## Exemplo Comparativo: `"Olá"` em UTF-8 vs. Latin-1

Os caracteres ASCII puros (`'O'` = `0x4F` e `'l'` = `0x6C`) têm exatamente a mesma representação em ambos os padrões, mas o carácter acentuado **`'á'`** difere:
* Em **UTF-8**, `'á'` ocupa **2 bytes**: **`C3 A1`**.
* Em **Latin-1**, `'á'` ocupa **1 byte**: **`E1`**.

| Endereço (*Address*) | `10` | `11` | `12` | `13` | `14` | `15` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Hex. (UTF-8)** | `...` | `4F` | `6C` | **`C3`** | **`A1`** | `...` |
| **Texto (UTF-8)** | | `O` | `l` | **`á`** *(2 bytes)* | $\leftarrow$ | |
| **Hex. (Latin-1)** | `...` | `4F` | `6C` | **`E1`** | `...` | `...` |
| **Texto (Latin-1)** | | `O` | `l` | **`á`** *(1 byte)* | | |

---

## Implicações Forenses

* **Pesquisa de Palavras-Chave (*Keyword Search*) com Acentos e em Windows**: Se um perito pesquisar a palavra `"Olá"` apenas pela sequência de bytes UTF-8 (`4F 6C C3 A1`) ou Latin-1 (`4F 6C E1`), falhará a deteção de ficheiros ou estruturas do Windows gravadas em **UTF-16LE** (`4F 00 6C 00 E1 00`). As ferramentas forenses têm de ser configuradas para pesquisar simultaneamente em ASCII/Latin-1, UTF-8 e UTF-16LE.
* **Reconhecimento Visual de UTF-8**: Em *hex dumps* de textos em português codificados em UTF-8, a presença frequente do byte prefixo `0xC3` antes de vogais acentuadas ou `'ç'` (ex.: `C3 A1` = `á`, `C3 A3` = `ã`, `C3 A7` = `ç`) permite identificar imediatamente a codificação UTF-8.

---

## Perguntas de revisão

- Porque é que o ASCII e o UTF-8 não sofrem de problemas de *endianness*?
- Quais são as diferenças de comprimento em bytes e de utilização entre UTF-8, UTF-16 e UTF-32?
- Como é representada em hexadecimal a palavra `"Olá"` em UTF-8 e em Latin-1?

## Notas relacionadas

- [[Endianness e Ordem de Armazenamento]]
- [[Organização de Estruturas de Dados em Binário]]
- [[Codificação Binário-para-Texto (Base16, Base64 e Base58)]]
- [[Capítulo 3 - Organização de Dados]]
