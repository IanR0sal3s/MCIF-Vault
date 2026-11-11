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
atualizado: 2026-11-11
---

# Codificação de Caracteres — ASCII, Latin-1 e Unicode

As codificações traduzem texto em bytes: o ASCII de 7 bits e o Latin-1 de 8 bits operam byte a byte sem endianness, enquanto o Unicode usa UTF-8, UTF-16 e UTF-32 para suporte multilingue.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Representação)**: O ASCII original de 7 bits apenas codifica 128 símbolos ingleses; extensões regionais como o Latin-1 (8 bits) colidem entre idiomas, levando o Unicode a universalizar mais de 137 000 caracteres através das codificações UTF-8, UTF-16 e UTF-32.
> * **Porque importa (Forense)**: Um mesmo texto produz sequências hexadecimais distintas consoante a codificação (`"Olá"` termina em `C3 A1` em UTF-8, `E1` em Latin-1 e `E1 00` em UTF-16LE), obrigando a pesquisar palavras-chave em todas as variantes simultaneamente.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Imunidade a *endianness***: tanto o **ASCII** como o **UTF-8** são lidos 1 byte de cada vez, não sofrendo problemas de *endianness*; já o **UTF-16** existe em `UTF-16LE` (Windows) e `UTF-16BE`.
>   * **Compatibilidade ASCII**: nos caracteres `0x00`–`0x7F` (como `'O'` = `0x4F` e `'l'` = `0x6C`), ASCII, Latin-1 e UTF-8 são idênticos.
>   * **Assinatura visual em português**: o prefixo `0xC3` antes de vogais acentuadas ou `'ç'` denuncia texto em **UTF-8** (ex.: `C3 A1` = `'á'`).

---

## 1. Codificação de Caracteres — ASCII e Latin-1

### Vantagens do ASCII

* É a forma mais simples de codificar caracteres.
* **Não tem problemas de *endianness***, uma vez que utiliza **1 byte de cada vez**.
* A versão original utiliza apenas **7 bits**, permitindo **128 caracteres diferentes** ([Tabela ASCII](http://www.asciitable.com/)).
* Ocupa menos espaço de armazenamento do que o Unicode (para conjuntos de caracteres compatíveis com representações multi-byte fixas).

### Desvantagens do ASCII e Extensões de 8 bits

* Capacidade muito limitada para representar caracteres não ingleses (acentos, cedilhas, alfabetos não latinos).
* Existem várias **versões estendidas de 8 bits** (256 caracteres):
  * A mais conhecida é o **Latin-1** ([Tabela ISO-8859-1 / Latin-1](http://cs.stanford.edu/people/miles/iso8859.html)).

### Exemplo em Memória (ASCII): `"2670-582 LOURES"`

| Endereço | `10` | `11` | `12` | `13` | `14` | `15` | `16` | `17` | `18` | `19` | `20` | `21` | `22` | `23` | `24` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Hexadecimal** | `32` | `36` | `37` | `30` | `2D` | `35` | `38` | `32` | `20` | `4C` | `4F` | `55` | `52` | `45` | `53` |
| **Texto (ASCII)** | `2` | `6` | `7` | `0` | `-` | `5` | `8` | `2` | ` ` | `L` | `O` | `U` | `R` | `E` | `S` |

*(Nota: `0x20` corresponde ao espaço em branco, `0x30`–`0x39` aos algarismos `0`–`9` e `0x41`–`0x5A` às letras maiúsculas `A`–`Z`).*

---

## 2. Codificação de Caracteres — Unicode

### Vantagens do Unicode

* Possui **mais de 137.000 caracteres**.
* Abrange **146 sistemas de escrita modernos e históricos**, bem como múltiplos conjuntos de símbolos.

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

| Endereço | `10` | `11` | `12` | `13` | `14` | `15` |
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

## Além da aula

* **Presença Ubíqua de `UTF-16LE` e `ASCII` nos Artefactos do Windows ([[00 ASSI|ASSI]])**:
  * **Ficheiros `TabState` do Bloco de Notas ([[Artefacto Forense do Bloco de Notas (Notepad Windows 11)]])**: Combinam uma assinatura mágica em **ASCII** (`4E 50` = `"NP"`) com o caminho do ficheiro e o conteúdo integral do texto codificados em **UTF-16LE** (`43 00 3A 00 5C 00...` = `"C:\..."`, ocupando $2 \times \text{Length}$ bytes), guardando ainda um byte que identifica a codificação original do ficheiro em disco (ex.: `0x05` para **UTF-8**).
  * **Tabela de Mapeamento do SRUM (`SruDbIdMapTable`)**: Na análise da base `SRUDB.dat` ([[System Resource Usage Monitor (SRUM) - Arquitetura e Base ESE]] e [[Análise Forense do SRUM e Ferramentas Nativas (powercfg)]]), a coluna binária `IdBlob` armazena os caminhos das aplicações em **UTF-16LE** (ex.: `5C 00 44 00 65 00 76 00 69 00 63 00 65 00...` para `\Device\...`).
  * **Strings no Windows Registry e Prefetch**: Os valores `REG_SZ`, `REG_EXPAND_SZ` e `REG_MULTI_SZ` ([[Tipos de Dados e Associação de Ficheiros no Registry]]), os nomes de ficheiros em `RecentDocs` ([[Artefactos Forenses de Interação do Utilizador (MRU e TypedPaths)]]) e o campo `Actual_file_name` bem como o cálculo de hash Unicode em [[Estrutura Interna e Algoritmo de Hashing do Prefetch]] utilizam internamente **UTF-16LE**.
  * **Extração de Strings (`-e S`) e Modificadores `ascii` vs. `wide` em YARA ([[Capítulo 3 - YARA - MOTW - Strings]])**: A diferença entre codificações de 7 bits (ASCII), 8 bits (Latin-1, exigindo `-e S` no [[Conceito de Strings e Comando strings em Unix-Linux|comando strings em Unix]] para não cortar palavras acentuadas em português) e 16 bits (UTF-16LE) é determinante tanto na extração de strings no Windows ([[Extração de Strings no Windows - Sysinternals strings e Swiss File Knife (sfk)]] e [[Eric Zimmerman bstrings - Parâmetros, Expressões Regulares e Exercícios]]) como nos modificadores `ascii` e `wide` de [[YARA - Tipos de Strings, Modificadores, Formato Hexadecimal, Base64 e Regex]].

---

## Perguntas de revisão

1. **Porque é que o ASCII e o UTF-8 não sofrem de problemas de *endianness*, ao contrário do UTF-16?**

> [!success]- Ver Resposta
> Tanto o **ASCII** (7/8 bits) como o **UTF-8** são lidos sequencialmente **1 byte de cada vez**, não existindo ambiguidade sobre a ordem de múltiplos bytes por unidade de codificação. Pelo contrário, o **UTF-16** usa unidades mínimas de 2 bytes, variando entre `UTF-16LE` (Windows) e `UTF-16BE`.

2. **Quais são as diferenças de comprimento em bytes e de utilização entre UTF-8, UTF-16 e UTF-32?**

> [!success]- Ver Resposta
> * **UTF-8**: tamanho variável de **1 a 4 bytes**, compatível com ASCII no primeiro byte; padrão em sistemas `*nix` (Unix/Linux), WWW e HTML.
> * **UTF-16**: tamanho variável de **2 a 4 bytes**, sujeito a *endianness*; usado internamente em Windows, Mac OS, Java, .Net e KDE.
> * **UTF-32**: comprimento fixo de **4 bytes** (32 bits) por carácter.

3. **Como é representada em hexadecimal a palavra `"Olá"` em UTF-8 e em Latin-1, e porque diferem apenas no último carácter?**

> [!success]- Ver Resposta
> Em **UTF-8**, `"Olá"` corresponde a **`4F 6C C3 A1`** (4 bytes); em **Latin-1**, corresponde a **`4F 6C E1`** (3 bytes). Os caracteres `'O'` (`4F`) e `'l'` (`6C`) pertencem ao ASCII puro e mantêm o mesmo código, ao passo que `'á'` ocupa **2 bytes (`C3 A1`)** em UTF-8 e **1 byte (`E1`)** em Latin-1.

4. **Que falha ocorre numa pesquisa forense de palavras-chave por `"Olá"` em sistemas Windows se a ferramenta procurar apenas em UTF-8 ou Latin-1?**

> [!success]- Ver Resposta
> A pesquisa falhará estruturas e strings do Windows gravadas em **UTF-16LE** (`4F 00 6C 00 E1 00`). Uma pesquisa pericial completa exige configurar a ferramenta para testar simultaneamente ASCII/Latin-1, UTF-8 e UTF-16LE.

## Notas relacionadas

- [[Endianness e Ordem de Armazenamento]]
- [[Organização de Estruturas de Dados em Binário]]
- [[Codificação Binário-para-Texto (Base16, Base64 e Base58)]]
- [[Artefacto Forense do Bloco de Notas (Notepad Windows 11)]]
- [[Análise Forense do SRUM e Ferramentas Nativas (powercfg)]]
- [[System Resource Usage Monitor (SRUM) - Arquitetura e Base ESE]]
- [[Tipos de Dados e Associação de Ficheiros no Registry]]
- [[Estrutura Interna e Algoritmo de Hashing do Prefetch]]
- [[Capítulo 3 - Organização de Dados]]
