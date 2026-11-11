---
title: YARA - Tipos de Strings, Modificadores, Formato Hexadecimal, Base64 e Regex
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 3
bloco: 1
fonte_aula: YARA & LOKI (Prof. Patrício Domingues)
tags:
  - assi
  - forense
  - yara
  - regex
  - base64
  - hex
  - unicode
aliases:
  - Modificadores YARA
  - Strings YARA
  - YARA Base64
  - YARA Regex
  - YARA Hexadecimal
atualizado: 2026-11-11
---

# YARA — Tipos de Strings, Modificadores, Formato Hexadecimal, Base64 e Regex

Na secção `strings:` de uma regra YARA, os indicadores podem ser definidos como texto com modificadores (`ascii`, `wide`, `nocase`, `fullword`, `base64`), sequências hexadecimais ou expressões regulares.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema / Deteção)**: Os artefactos em disco e memória codificam texto em múltiplos formatos (ASCII de 1 byte, UTF-16 de 2 bytes, Base64) e sofrem variações entre compilações; os modificadores, *wildcards* hexadecimais e regex do YARA generalizam a deteção numa única regra.
> * **Porque importa (Forense / IR)**: Garante a captura de chamadas Win32 em Unicode (`wide`), comandos ofuscados em Base64 independentemente do alinhamento e assinaturas de código máquina com endereços variáveis (`??`, `[min-max]`).
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Omissão de `wide`**: por omissão, o YARA procura apenas strings `ascii` (1 byte). Em binários Windows compilados com UTF-16, omitir `wide` (ou `wide ascii`) provoca falsos negativos silenciosos.
>   * **As 3 permutações do `base64`**: como cada 3 octetos (`24` bits) geram 4 caracteres Base64, uma string pode iniciar no deslocamento `0`, `1` ou `2` bytes dentro do bloco de 3 octetos, exigindo 3 pesquisas distintas.
>   * **Custo de Regex**: expressões abertas como `.*` degradam gravemente o desempenho no YARA clássico (v4.x).

---

## 1. Cadeias de Texto e Modificadores (`nocase`, `wide`, `ascii`, `fullword`, `base64`)

As strings de texto são declaradas entre aspas duplas (`"..."`). Por omissão, o YARA pesquisa em formato **ASCII** (1 byte por carácter) com distinção entre maiúsculas e minúsculas (*case-sensitive*), comportamento ajustável através de **modificadores**:

| Modificador | Exemplo em YARA | Funcionamento Técnico Detalhado |
| :--- | :--- | :--- |
| **`nocase`** | `$domain1 = "evilsite1.com" nocase` | **Desativa a diferenciação entre maiúsculas e minúsculas** (*case-insensitive*), fazendo corresponder `"EVILSITE1.COM"`, `"EvilSite1.com"`, etc. |
| **`wide`** | `$s2 = "Self Process" fullword wide` | Procura a string codificada a **dois bytes por carácter** (formato **UTF-16 / Unicode** usado nativamente pelo Windows, onde os caracteres ASCII são intercalados com um byte nulo `0x00`, ex.: `"M.i.c.r.o.s.o.f.t."`). |
| **`ascii`** | `$s1 = "In.pdb" fullword ascii` | Procura exclusivamente strings em formato **ASCII** de 1 byte por carácter (comportamento predefinido quando `wide` não é especificado). |
| **`wide ascii`** | `$a1 = "string" ascii wide fullword nocase` | Combina ambos os formatos: instrui o YARA a procurar simultaneamente a representação **UNICODE (2 bytes)** e **ASCII (1 byte)** da string. |
| **`fullword`** | `$x2 = "taskdl.exe" fullword ascii` | Exige **correspondência de palavra inteira**: a string só dispara se estiver delimitada antes e depois por caracteres **não alfanuméricos** (ex.: início/fim do ficheiro, espaços, barras `\` ou pontuação). |
| **`base64`** | `$a = "This program cannot" base64` | Pesquisa automaticamente as **3 permutações de alinhamento** da string codificada em Base64 (detalhado na secção seguinte). |

---

## 2. O Modificador `base64` e as 3 Permutações de Alinhamento

O modificador **`base64`** instrui o YARA a procurar uma string de texto codificada em **[[Codificação Binário-para-Texto (Base16, Base64 e Base58)|Base64]]** dentro do ficheiro analisado.

### Exemplo da Aula (`rule Base64Example1`)

```yara
rule Base64Example1 {
    strings:
        $a = "This program cannot" base64
    condition:
        $a
}
```

### Porque é que o YARA procura 3 sequências Base64 distintas?
Na codificação Base64, cada bloco de **3 octetos (24 bits)** do texto original (8 bits por carácter ASCII) é dividido em **4 grupos de 6 bits**, originando **4 caracteres Base64** (alfabeto `A-Za-z0-9+/=`):

| Campo | 1.º Carácter | 2.º Carácter | 3.º Carácter |
| :--- | :---: | :---: | :---: |
| **Source ASCII** | `M` | `a` | `n` |
| **Source octets (Decimal / Hex)** | `77` (`0x4d`) | `97` (`0x61`) | `110` (`0x6e`) |
| **Bit pattern (24 bits)** | `01001101` | `01100001` | `01101110` |
| **Grupos de 6 bits (Index)** | `010011` (`19`) | `010110` (`22`) | `000101` (`5`) / `101110` (`46`) |
| **Base64-encoded** | **`T`** (`84` / `0x54`) | **`W`** (`87` / `0x57`) | **`F`** (`70` / `0x46`) e **`u`** (`117` / `0x75`) |

Como a string `"This program cannot"` pode surgir em qualquer posição dentro de um fluxo de dados maior antes de ser codificada em Base64 (alinhada ao byte `0`, deslocada de `1` espaço/byte ou deslocada de `2` espaços/bytes no grupo de 3 octetos), o modificador `base64` gera e **procura automaticamente as três permutações de alinhamento** (omitindo os caracteres das extremidades que dependem dos bytes vizinhos):

1. **`VGhpcyBwcm9ncmFtIGNhbm5vd`** — correspondente a `"This program cannot"` (sem deslocamento);
2. **`RoaXMgcHJvZ3JhbSBjYW5ub3`** — correspondente a `" This program cannot"` (deslocado 1 byte — no exemplo CyberChef dos diapositivos, `"  This program cannot"` de 22 bytes gera `ICBUaGlzIHByb2dyYW0gY2Fubm90IA==`);
3. **`UaGlzIHByb2dyYW0gY2Fubm90`** — correspondente a `"  This program cannot"` (deslocado 2 bytes).

---

## 3. Formato Hexadecimal: *Wildcards* (`??`) e *Jumps* (`[min-max]`)

As sequências hexadecimais são definidas entre chavetas `{ ... }` e permitem procurar padrões de bytes brutos (*magic bytes* ou sequências de *opcodes*), admitindo dois mecanismos de flexibilidade demonstrados nos diapositivos:

### A. *Wildcards* (`?` e `??`) — `rule WildcardExample`

```yara
rule WildcardExample {
    strings:
        $hex_string = { E2 34 ?? C8 A? FB }
    condition:
        $hex_string
}
```

* **`??` (Wildcard de byte completo)**: substitui **quaisquer dois dígitos hexadecimais** (`1` octeto completo, de `00` a `FF`).
* **`A?` (Wildcard de meio byte / *nibble*)**: exige que o primeiro *nibble* seja `A`, aceitando qualquer valor hexadecimal (`0` a `F`) no segundo *nibble* (`A0` a `AF`).

### B. *Jumps* (`[min-max]`) — `rule JumpExample`

```yara
rule JumpExample
{
    strings:
        $hex_string = { F4 23 [4-6] 62 B4 }
    condition:
        $hex_string
}
```

* **`[4-6]` (Salto variável de octetos)**: aceita **quaisquer quatro a seis octetos** (bytes arbitrários) entre a sequência inicial `F4 23` e a sequência final `62 B4`.

---

## 4. Expressões Regulares (*REGEXes*) no YARA

O YARA suporta expressões regulares delimitadas entre barras **`/.../`** (podendo ser seguidas de modificadores como `nocase`, `wide`, `ascii`, `fullword`).

### Exemplos nos Diapositivos

**1. Regra `RegExpExample1`:**

```yara
rule RegExpExample1
{
    strings:
        $re1 = /md5: [0-9a-zA-Z]{32}/
        $re2 = /state: (on|off)/
        $hex = { E2 34 A1 C8 23 FB }
    condition:
        $re1 and $re2
}
```

* `$re1` procura o prefixo literal `"md5: "` seguido de exatamente **32 caracteres alfanuméricos** (`[0-9a-zA-Z]{32}`);
* `$re2` procura `"state: "` seguido de `"on"` ou `"off"` (`(on|off)`).

**2. Pesquisa de Endereços IPv4 (na regra `silent_banker`):**

```yara
$ip = /([0-9]{1,3}\.){3}[0-9]{1,3}/ wide ascii
```

* Procura 3 grupos compostos por 1 a 3 dígitos seguidos de um ponto literal (`\.`), terminando num quarto grupo de 1 a 3 dígitos, quer em UTF-16 (`wide`), quer em ASCII (`ascii`).

### Construções Regex no YARA Agrupadas por Função

#### A. Âncoras e Escape

| Símbolo | Descrição Técnica |
| :---: | :--- |
| **`\`** | Escapa o metacaracter seguinte para correspondência literal (ex.: `\.` corresponde ao ponto literal). |
| **`^`** | Corresponde ao **início** do ficheiro ou string. |
| **`$`** | Corresponde ao **fim** do ficheiro ou string. |

#### B. Agrupamento, Alternância e Classes de Caracteres

| Símbolo | Descrição Técnica |
| :---: | :--- |
| **`\|`** | Operador de **alternância** (OU lógico entre alternativas, ex.: `(on\|off)`). |
| **`()`** | Agrupa sub-expressões para aplicar quantificadores ou alternância. |
| **`[]`** | Classe de caracteres entre parênteses retos (ex.: `[0-9a-zA-Z]`). |

#### C. Quantificadores

| Símbolo | Descrição Técnica |
| :---: | :--- |
| **`*`** | Corresponde **0 ou mais** vezes. |
| **`+`** | Corresponde **1 ou mais** vezes. |
| **`?`** | Corresponde **0 ou 1** vez. |
| **`{n}`** | Corresponde **exatamente $n$** vezes. |
| **`{n,}`** | Corresponde **pelo menos $n$** vezes. |
| **`{,m}`** | Corresponde **de 0 até $m$** vezes. |
| **`{n,m}`** | Corresponde **entre $n$ e $m$** vezes. |

#### D. Classes Rápidas (*Shorthand Classes*)

| Símbolo | Descrição Técnica |
| :---: | :--- |
| **`\w`** | Carácter de palavra (alfanumérico mais `_`). |
| **`\W`** | Carácter **não** pertencente a palavra. |
| **`\s`** | Carácter de espaço em branco (*whitespace*: espaço, tabulação, etc.). |
| **`\S`** | Carácter que **não** é espaço em branco. |
| **`\d`** | Dígito decimal (`[0-9]`). |
| **`\D`** | Carácter que **não** é dígito decimal. |

---

## 5. Implicações Forenses

* **A Omissão de `wide` no Windows Causa Falsos Negativos**: como o compilador Visual C++ e a API Win32 armazenam grande parte das strings internas de executáveis Windows em **UTF-16 Little-Endian** (2 bytes por carácter), escrever uma regra YARA apenas com `"CreateRemoteThread"` sem os modificadores `wide ascii` falhará a deteção se a string estiver em Unicode no binário.
* **Custo Computacional das Expressões Regulares**: como alertado na bibliografia da aula (*Enhancing YARA Rule Performance*), expressões regulares demasiado abertas (como `.*`) degradam severamente o desempenho no YARA clássico (v4.x), devendo preferir-se strings literais, sequências hexadecimais com *jumps* limitados `[4-6]` ou o motor otimizado do [[YARA-X (Reimplementação em Rust) e Ferramenta CLI yr|YARA-X]].

---

## Além da aula

* **Pontes Diretas com o Capítulo 3 de [[00 AFD1|AFD1]]**:
  * A tabela de conversão de `"Man"` (`0x4d`, `0x61`, `0x6e` $\to$ `TWFu`) no Slide 11 desta aula de ASSI aplica diretamente o algoritmo de agrupamento de $3 \times 8\text{ bits} = 4 \times 6\text{ bits}$ estudado em [[Codificação Binário-para-Texto (Base16, Base64 e Base58)]].
  * A distinção entre os modificadores `ascii` (1 byte) e `wide` (UTF-16 de 2 bytes) reflete diretamente os conceitos de [[Codificação de Caracteres - ASCII, Latin-1 e Unicode]] e [[Extração de Strings no Windows - Sysinternals strings e Swiss File Knife (sfk)]].

---

## Perguntas de revisão

1. **Qual é a diferença prática entre usar `ascii`, `wide` e `wide ascii` numa regra YARA, e o que garante o modificador `fullword`?**

> [!success]- Ver Resposta
> Por omissão (`ascii`), o YARA pesquisa strings de **1 byte por carácter**; `wide` pesquisa em **UTF-16 / Unicode (2 bytes por carácter, intercalado com `0x00`)**, usado nativamente pela API Win32; `wide ascii` instrui o motor a procurar simultaneamente ambas as codificações. O modificador **`fullword`** garante que a string só dispara se estiver delimitada antes e depois por caracteres **não alfanuméricos** (ex.: início/fim do ficheiro, espaços, barras ou pontuação).

2. **Na sequência hexadecimal `{ E2 34 ?? C8 A? FB }` e em `{ F4 23 [4-6] 62 B4 }`, o que significam `??`, `A?` e `[4-6]`?**

> [!success]- Ver Resposta
> **`??`** é um *wildcard* de byte completo (aceita qualquer octeto de `00` a `FF`); **`A?`** é um *wildcard* de *nibble* (meio byte) que fixa o primeiro dígito em `A` e aceita qualquer dígito `0–F` no segundo (`A0` a `AF`); **`[4-6]`** é um *jump* que aceita **4 a 6 octetos arbitrários** entre `F4 23` e `62 B4`.

3. **Porque é que `$a = "This program cannot" base64` pesquisa três sequências Base64 diferentes em vez de apenas uma?**

> [!success]- Ver Resposta
> Porque o Base64 codifica blocos de **3 octetos (24 bits)** em **4 caracteres de 6 bits**. Dependendo da posição onde a string começa dentro do fluxo original antes da codificação (deslocamento `0`, `1` ou `2` bytes), os bits alinham-se de três formas distintas, gerando as permutações `VGhpcyBwcm9ncmFtIGNhbm5vd`, `RoaXMgcHJvZ3JhbSBjYW5ub3` e `UaGlzIHByb2dyYW0gY2Fubm90`.

4. **O que procuram as expressões regulares `/md5: [0-9a-zA-Z]{32}/` e `/([0-9]{1,3}\.){3}[0-9]{1,3}/`?**

> [!success]- Ver Resposta
> `/md5: [0-9a-zA-Z]{32}/` procura o prefixo literal `"md5: "` seguido de exatamente **32 caracteres alfanuméricos** (formato típico de hash MD5). `/([0-9]{1,3}\.){3}[0-9]{1,3}/` procura **endereços IPv4**: 3 grupos de 1 a 3 dígitos seguidos de ponto literal (`\.`), terminando num quarto grupo de 1 a 3 dígitos.

5. **Porque se devem evitar expressões regulares abertas (como `.*`) no YARA clássico (v4.x)?**

> [!success]- Ver Resposta
> Expressões regulares demasiado permissivas aumentam drasticamente o custo de avaliação do motor clássico em C, degradando o desempenho do varrimento; deve dar-se preferência a strings literais, sequências hexadecimais com *jumps* limitados (ex.: `[4-6]`) ou recorrer ao motor otimizado do **YARA-X**.

## Notas relacionadas

- [[YARA - Introdução, Estrutura de Regras, Metadados e Condições]]
- [[Execução e Compilação no YARA (yara e yarac), Casos Reais (UPX, WannaCry) e LLMs]]
- [[YARA-X (Reimplementação em Rust) e Ferramenta CLI yr]]
- [[Codificação de Caracteres - ASCII, Latin-1 e Unicode]]
- [[Codificação Binário-para-Texto (Base16, Base64 e Base58)]]
- [[Eric Zimmerman bstrings - Parâmetros, Expressões Regulares e Exercícios]]
- [[Capítulo 3 - YARA - MOTW - Strings]]
