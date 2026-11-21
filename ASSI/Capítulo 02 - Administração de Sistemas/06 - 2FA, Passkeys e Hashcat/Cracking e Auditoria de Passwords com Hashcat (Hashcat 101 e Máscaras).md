---
title: Cracking e Auditoria de Passwords com Hashcat (Hashcat 101 e Máscaras)
tipo: procedimento
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 2
bloco: 6
fonte_aula: System Administration - Access Control.pdf
tags:
  - assi
  - administracao-sistemas
  - controlo-acessos
  - hashcat
  - password-cracking
  - mascaras
  - wordlists
  - ntlm
  - auditoria
aliases:
  - Hashcat 101
  - Cracking com Hashcat
  - Máscaras Hashcat
  - Charsets Hashcat
  - Auditoria de Passwords Hashcat
atualizado: 2026-11-11
---

# Cracking e Auditoria de Passwords com Hashcat (Hashcat 101 e Máscaras)

O hashcat é a ferramenta padrão de auditoria e recuperação offline de passwords, suportando mais de 100 algoritmos de hash, aceleração por CPU/GPU, ataques de dicionário (-a 0) e máscaras (-a 3).

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema / Segurança)**: Equipas de auditoria, resposta a incidentes e peritos forenses necessitam de avaliar a resistência real de credenciais armazenadas e recuperar acesso a ficheiros ou contas cifradas através de ataques offline de alto débito.
> * **Porque importa (Segurança / Forense)**: A execução paralela em GPU (`cudaHashcat` e `oclHashcat`) combinada com *wordlists* reais (`rockyou.txt`) e máscaras estruturadas (`-a 3`) permite auditar em minutos hashes fracos extraídos de bases de dados ou hives `SAM` do Windows (`-m 1000`).
> * **Pontos Críticos e Armadilhas para Exame**:
>   * Os **4 argumentos base**: **`-m`** (algoritmo de hash, ex.: `0` = MD5, `1000` = NTLM), **`-a`** (modo: `0` = dicionário, `3` = máscara/força bruta), `<Filename>` e `<Dictionary or mask>`.
>   * Dominar os **8 *built-in charsets***: `?l`, `?u`, `?d`, `?h`, `?H`, `?s`, `?a` (`?l?u?d?s`, 95 caracteres) e `?b` (`0x00–0xff`).
>   * A máscara `?a?a?a?a?a?a?a` (7 vezes `?a`) gera um espaço de busca de $95^7$ combinações.

---

## 1. Arquitetura e Capacidades do `hashcat` (Slide 113)

* **Definição**: o **[hashcat](http://hashcat.net/oclhashcat/)** ([código-fonte no GitHub](https://github.com/hashcat/hashcat)) é uma ferramenta de alto desempenho para recuperação e auditoria de palavras-passe por força bruta offline.
* **Modos e Algoritmos Suportados**:
  * Executa ataques de **dicionário (*dictionary attack*)**, **padrões/máscaras (*patterns/masks*)**, híbridos e baseados em regras (*rule-based*);
  * Suporta **mais de 100 tipos de algoritmos de hash**, incluindo documentos Microsoft Office, bases Oracle, sistemas Unix/Linux, Windows NTLM, `MD5`, `SHA-1`, `bcrypt` e redes `WPA2`.
* **Aceleração por CPU e GPU**:
  * **CPU *multithreading***: distribui o cálculo por todos os núcleos do processador;
  * **Variantes dedicadas para GPU**: **`cudaHashcat`** (otimizada para placas **NVIDIA**) e **`oclHashcat`** (otimizada para placas **AMD** via OpenCL).
* **Repositórios de Dicionários**: além do `rockyou.txt` incluído no Kali Linux (`/usr/share/wordlists/rockyou.txt.gz`), os diapositivos recomendam o [repositório de dicionários SkullSecurity](https://wiki.skullsecurity.org/Passwords/).

---

## 2. `Hashcat 101`: Anatomia dos 4 Argumentos Básicos (Slide 114)

A sintaxe essencial do `hashcat` organiza-se em torno de **quatro parâmetros principais**:

| Argumento | Flag / Parâmetro | Função e Valores Principais |
| :---: | :--- | :--- |
| **#1** | **`-m` / `--hashtype <num>`** | Define o identificador numérico do algoritmo de hash alvo:<br>• **`-m 0`**: **`MD5`**<br>• **`-m 1`** (ou `100` nas versões modernas): **`SHA1`**<br>• **`-m 1000`**: **`NTLM`** (hashes de contas locais Windows extraídos do hive `SAM`). |
| **#2** | **`-a` / `--attack-mode <num>`** | Seleciona o modo de ataque:<br>• **`-a 0`**: **Ataque de dicionário ou *wordlist*** (*dictionary or word list*)<br>• **`-a 3`**: **Ataque de força bruta por máscara** (*brute-force / mask attack*). |
| **#3** | **`<Filename>`** | Ficheiro de entrada contendo os hashes a quebrar (ex.: `FileWithHashesToCrack`). |
| **#4** | **`<Dictionary or mask>`** | Caminho do ficheiro de dicionário (no modo `-a 0`) **ou** a **máscara de caracteres** (no modo `-a 3`, ex.: `?l?l?l` para testar todas as combinações de 3 letras minúsculas). |

---

## 3. Tabela Completa dos 8 *Built-in Charsets* de Máscara (Slide 114)

No modo **`-a 3`**, cada posição da palavra-passe candidata é especificada por um marcador de conjunto de caracteres (*charset*):

| Símbolo na Máscara | Conjunto de Caracteres Equivalente | Descrição Técnica |
| :---: | :--- | :--- |
| **`?l`** | `abcdefghijklmnopqrstuvwxyz` (`[a-z]`) | 26 letras minúsculas ASCII |
| **`?u`** | `ABCDEFGHIJKLMNOPQRSTUVWXYZ` (`[A-Z]`) | 26 letras maiúsculas ASCII |
| **`?d`** | `0123456789` (`[0-9]`) | 10 dígitos decimais |
| **`?h`** | `0123456789abcdef` (`[0-9a-f]`) | 16 caracteres hexadecimais em minúsculas |
| **`?H`** | `0123456789ABCDEF` (`[0-9A-F]`) | 16 caracteres hexadecimais em maiúsculas |
| **`?s`** | ``!"#$%&'()*+,-./:;<=>?@[\]^_`{\|}~`` (e espaço) | 33 símbolos especiais imprimíveis ASCII |
| **`?a`** | **`?l?u?d?s`** | Todos os **95** caracteres ASCII imprimíveis (minúsculas, maiúsculas, dígitos e símbolos) |
| **`?b`** | `0x00 - 0xff` | Qualquer valor de byte binário completo (0 a 255) |

---

## 4. Dissecação do Comando de Exemplo e Cenários Práticos (Slide 114)

### 4.1. Dissecação Flag-a-Flag do Comando da Aula

```bash
hashcat -m 0 -a 3 -o results.txt FileWithHashesToCrack ?a?a?a?a?a?a?a
```

* **`-m 0`**: especifica que os hashes contidos no ficheiro alvo correspondem ao algoritmo **`MD5`**.
* **`-a 3`**: ativa o modo de **força bruta com máscara**.
* **`-o results.txt`**: grava automaticamente todas as palavras-passe recuperadas no ficheiro de saída `results.txt`.
* **`FileWithHashesToCrack`**: ficheiro de texto de entrada com os hashes alvo.
* **`?a?a?a?a?a?a?a`** (`7` ocorrências de `?a`): testa sistematicamente todas as combinações de uma **palavra-passe com `7` caracteres** sobre os 95 caracteres ASCII imprimíveis (`?l?u?d?s`), totalizando **$95^7$ combinações**.

### 4.2. Custom Charset (`-1`), Dicionário (`-a 0`) e Auditoria Windows `NTLM` (`-m 1000`)

```bash
# Custom charset (Ficha 13 Extra-Aula): 7 letras misturando maiúsculas e minúsculas (-1 ?u?l)
hashcat -m 0 -a 3 -1 ?u?l -o cracked.txt hashes_md5.txt ?1?1?1?1?1?1?1

# Auditoria de hashes MD5 contra o dicionário RockYou no Kali Linux
hashcat -m 0 -a 0 -o cracked.txt hashes_md5.txt /usr/share/wordlists/rockyou.txt

# Auditoria de hashes NTLM extraídos de hives SAM do Windows
hashcat -m 1000 -a 0 -o cracked_ntlm.txt sam_hashes.txt /usr/share/wordlists/rockyou.txt
```

---

## Além da aula

* **Triagem de Hashes `SAM` e `CrackStation` em `AFD1` (Caps. 1 e 2)**: Na triagem forense de sistemas Windows descrita em [[Ferramentas de Triagem Forense no Windows Registry (RegistryReport, ForensicUserInfo e WRR)]], o utilitário `ForensicUserInfo` extrai os hashes `NTLM` das contas locais a partir dos hives `SAM` e `SYSTEM`, permitindo posteriormente auditá-los offline com **`hashcat -m 1000`**. Para hashes simples não salgados (`MD5`/`SHA-256`), ferramentas online baseadas em *lookup tables* como o `CrackStation` ([[Exercícios Práticos - Integridade de Dados e Hashes]] e [[Preservação do Sistema e Integridade de Dados]]) oferecem verificação imediata por dicionário pré-computado.
* **Impacto do Armazenamento Defensivo na Taxa do `hashcat` (`ASSI` Cap. 2 Bloco 06)**: A origem da wordlist `rockyou.txt` e o motivo pelo qual funções lentas com `per-credential salt` e `Key Stretching` (`Argon2`, `PBKDF2`, `scrypt`, `bcrypt`) reduzem drasticamente a velocidade de ataque do `hashcat` encontram-se detalhados em [[Armazenamento Seguro de Passwords (Salting e Key Stretching) e Casos RockYou e LastPass]].

---

## Perguntas de revisão

1. **Que arquiteturas de hardware e tipos de ataque são suportados pelo `hashcat` (incluindo os nomes das variantes otimizadas para GPUs NVIDIA e AMD)?**

> [!success]- Ver Resposta
> O `hashcat` suporta ataques de dicionário, máscaras/padrões, híbridos e baseados em regras para mais de 100 algoritmos de hash (Office, Oracle, Unix/Linux, NTLM, MD5, SHA-1, bcrypt, WPA2). Executa com *multithreading* em todos os núcleos de CPU e dispõe das variantes aceleradas por GPU **`cudaHashcat`** (NVIDIA) e **`oclHashcat`** (AMD).

2. **Indique os quatro argumentos básicos do `hashcat` e distinga o modo `-a 0` do modo `-a 3`.**

> [!success]- Ver Resposta
> Os quatro argumentos são: (1) **`-m`** (código numérico do tipo de hash, ex.: `0` para MD5); (2) **`-a`** (modo de ataque); (3) **`<Filename>`** (ficheiro com os hashes); e (4) **`<Dictionary or mask>`**. O modo **`-a 0`** executa um ataque de **dicionário (*wordlist*)**, enquanto o modo **`-a 3`** executa um ataque de **força bruta por máscara**.

3. **Qual é o significado exato dos oito *built-in charsets* de máscara do `hashcat` (`?l`, `?u`, `?d`, `?h`, `?H`, `?s`, `?a`, `?b`)?**

> [!success]- Ver Resposta
> **`?l`**: minúsculas `[a-z]` (26); **`?u`**: maiúsculas `[A-Z]` (26); **`?d`**: dígitos `[0-9]` (10); **`?h`**: hexadecimal minúsculas `[0-9a-f]` (16); **`?H`**: hexadecimal maiúsculas `[0-9A-F]` (16); **`?s`**: 33 símbolos especiais imprimíveis + espaço; **`?a`**: `?l?u?d?s` (95 caracteres ASCII imprimíveis); **`?b`**: todos os valores de byte `0x00–0xff`.

4. **Explique cada elemento do comando `hashcat -m 0 -a 3 -o results.txt FileWithHashesToCrack ?a?a?a?a?a?a?a` e quantas combinações testa.**

> [!success]- Ver Resposta
> **`-m 0`** seleciona hashes `MD5`; **`-a 3`** ativa o ataque de força bruta por máscara; **`-o results.txt`** guarda os resultados recuperados em `results.txt`; **`FileWithHashesToCrack`** fornece os hashes alvo; e **`?a?a?a?a?a?a?a`** testa todas as palavras-passe de 7 caracteres sobre os 95 caracteres ASCII imprimíveis, totalizando **$95^7$ combinações**.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Armazenamento Seguro de Passwords (Salting e Key Stretching) e Casos RockYou e LastPass]] | `mesmo bloco` |
| **Seguinte** | [[Capítulo 2 - Administração de Sistemas]] · [[00 ASSI]] | Fim do capítulo |
| **Índice** | [[Capítulo 2 - Administração de Sistemas]] · [[00 ASSI]] | `Bloco 06` |

### Conceitos Relacionados

* [[Entropia de Passwords e Entropia de Ficheiros (ent e Detect It Easy)]] · `Bloco 05`
* [[Ferramentas de Triagem Forense no Windows Registry (RegistryReport, ForensicUserInfo e WRR)]] · `AFD1 · Cap. 2`
* [[Exercícios Práticos - Integridade de Dados e Hashes]] · `AFD1 · Cap. 1`
* [[Preservação do Sistema e Integridade de Dados]] · `AFD1 · Cap. 1`
* [[Cheat Sheet - Administração de Sistemas e Controlo de Acessos]] · `mesmo cap.`
