---
title: YARA - Introdução, Estrutura de Regras, Metadados e Condições
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
  - malware
  - ioc
  - virustotal
aliases:
  - YARA
  - Introdução ao YARA
  - Estrutura de Regras YARA
  - Metadados YARA
atualizado: 2026-11-11
---

# YARA — Introdução, Estrutura de Regras, Metadados e Condições

O **YARA** (*"The pattern Swiss knife (for malware)"*) é uma ferramenta de deteção baseada em assinaturas que avalia ficheiros e processos segundo regras formais com resultado binário (positivo ou negativo).

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema / Deteção)**: Hashes criptográficos identificam apenas ficheiros idênticos bit-a-bit e falham perante qualquer reempacotamento ou alteração mínima; o YARA descreve famílias de *malware*, comportamentos e IOCs através de padrões combinados por lógica booleana.
> * **Porque importa (Forense / IR)**: Permite executar triagem automatizada em disco e memória para localizar variantes maliciosas, caminhos de compilação (`.pdb`), domínios C2 e assinaturas estruturais, servindo de motor base a ferramentas como o `LOKI`.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Ordem de bytes (`$mz = { 4D 5A }` vs. `uint16(0) == 0x5a4d`)**: na secção `strings:`, os bytes são declarados sequencialmente (`4D 5A`); na secção `condition:`, `uint16(0)` lê um inteiro de 16 bits em **Little-Endian**, invertendo para **`0x5a4d`**.
>   * **Avaliação por curto-circuito**: validar `uint16(0) == 0x5a4d and filesize < 300KB` no início da `condition:` evita pesquisar strings em ficheiros não-PE ou demasiado grandes.
>   * **Ciclo de vida e licença**: lançado em **2013** pela **VirusTotal** (Victor M. Alvarez) sob licença **BSD-3**; entrou em *maintenance mode* em **2025**, dando lugar ao `YARA-X` (em Rust).

---

## 1. Conceitos, Arquitetura e Ciclo de Vida

### 1.1. Princípio de Funcionamento e Deteção Binária

* **Deteção baseada em assinatura (*signature-based*)**: o YARA avalia cada ficheiro, diretoria ou processo em execução face a descrições formais (regras).
* **Resultado estritamente binário**: a avaliação de uma regra YARA produz sempre uma resposta **positiva** (a amostra satisfaz a condição definida) ou **negativa** (não satisfaz).
* **Exemplo elementar de marcador binário (`4D 5A` / `MZ`)**:
  * Todos os executáveis DOS/Windows (*Portable Executable* — PE) iniciam no *offset* `00000000` pela sequência hexadecimal **`4D 5A`**, que em [[Codificação de Caracteres - ASCII, Latin-1 e Unicode|ASCII]] corresponde aos caracteres **`MZ`** (iniciais de Mark Zbikowski).
  * No exemplo ilustrado nos diapositivos com o ficheiro `EraserPortable.exe`, a inspeção hexadecimal mostra nos dois primeiros bytes (`Offset 00000000`, colunas `00` e `01`) exatamente `4D 5A` (`MZ`).

### 1.2. Disponibilidade, Histórico e Obtenção

* **Código aberto e Licença**: disponível no [Repositório Oficial do YARA no GitHub](https://github.com/VirusTotal/yara) sob [licença BSD-3](https://github.com/VirusTotal/yara/blob/master/COPYING).
* **Ciclo de Vida**:
  * Desenvolvido pela **VirusTotal** (criado originalmente por Victor M. Alvarez);
  * Lançado pela primeira vez em **2013**;
  * Passou para ***maintenance mode* em 2025**, dando lugar à nova implementação em Rust: o [[YARA-X (Reimplementação em Rust) e Ferramenta CLI yr|YARA-X]].
* **Multiplataforma**: suporta nativamente **Windows, macOS e Linux**.

**Formas de Obtenção:**

* **Windows**: executáveis pré-compilados de 32 e 64 bits disponibilizados na [secção de Releases do YARA](https://github.com/VirusTotal/yara/releases) (ex.: `yara-4.5.5-2368-win32.zip` e `yara-4.5.5-2368-win64.zip`).

**Linux / Outras plataformas:**

**1.** Através do gestor de pacotes nativo da distribuição:

```bash
sudo apt install yara yarac
```

**2.** Ou descarregando (`Source code (zip)` / `(tar.gz)`) e compilando diretamente o código-fonte.

---

## 2. Finalidade e Anatomia das Regras YARA

As regras YARA são **ficheiros de texto com sintaxe própria** concebidos para automatizar a identificação de ficheiros maliciosos ou trechos de código:

* Descrevem características de ficheiros combinando **strings específicas, expressões regulares e sequências binárias**;
* Identificam **famílias de *malware***, **comportamentos específicos** ou **Indicadores de Comprometimento (*Indicators of Compromise* — IOCs)** conhecidos;
* São portáveis entre plataformas e ferramentas de segurança (como o [[Scanner de IOCs LOKI (Versão Python) - Métodos de Deteção e Configuração|scanner LOKI]]) ou criadas à medida para incidentes específicos;
* **Inspiração Sintática**: combina elementos da linguagem **C** (blocos `{ ... }`, comentários de linha `//` e multi-linha `/* ... */`) e de **PERL** (expressões regulares delimitadas por `/.../`).

### Comparação das Três Secções de uma Regra YARA

| Secção | Obrigatoriedade e Papel | Elementos Suportados | Interfere na Deteção? |
| :--- | :--- | :--- | :---: |
| **`meta:`** | Opcional (boa prática de documentação e rastreabilidade) | Pares chave-valor com strings (`"..."`), inteiros e booleanos (`true`/`false`) | **Não** |
| **`strings:`** | Declaração dos padrões a pesquisar (opcional se a condição usar apenas módulos/offsets/tamanho) | Variáveis `$nome` com texto (`"..."`), sequências hex (`{ ... }`) ou regex (`/.../`) | **Sim** (define os alvos) |
| **`condition:`** | **Obrigatória** — define a lógica de disparo da regra | Expressões booleanas (`and`, `or`, `not`), quantificadores (`any of`, `N of`), `filesize`, offsets (`at`, `in`) e funções inteiras (`uint16`) | **Sim** (decide o resultado binário) |

### Modelo Geral de um Ficheiro de Regras YARA

Cada regra inicia pela palavra reservada `rule`, seguida do nome identificador (e opcionalmente de uma ou mais *tags* separadas por `:`, como `rule silent_banker : banker`), organizando-se nas três secções:

```yara
rule specific_name // e.g. APT_xpto, ...
{
    meta: // suggested
        author = ""
        date_created = ""
        date_last_modified = ""
        description = ""
        filetype = ""
        hash = ""
        source = ""
        TLP = ""
        license = ""
        min_yara_version = ""

    strings:
        $a1 = "string type 1-1" ascii wide fullword nocase
        $a2 = "string type 1-2"
        $a3 = "string type 1-3"

        $b1 = "string type 2-1"
        $b2 = "string type 2-2"
        $b3 = "string type 2-3"

        $c1 = "string type 3-1"
        $c2 = "string type 3-2"
        $c3 = "string type 3-3"

    condition:
        any of $a* or (2 of $b*) or (1 of $c*)
}
```

---

## 3. A Secção `meta:` (Metadados da Regra)

A secção `meta:` **identifica e documenta a regra**, não interferindo na lógica de avaliação da `condition:`. Suporta valores de texto (entre aspas), inteiros e booleanos (`true`/`false`):

| Atributo de Metadados | Significado e Exemplos nos Diapositivos |
| :--- | :--- |
| **`author`** | Criador da regra (ex.: `author = "Florian Roth"`, `author = "someone"`). |
| **`date` / `date_created`** | Data de criação da regra (ex.: `date = "2025.08.30"` ou formato ISO `"2016-12-29"`). |
| **`date_last_modified`** | Data da última modificação da regra. |
| **`description`** | Descrição sumária do alvo da regra (ex.: `"Auto-generated rule - file HRDG022184_certclint.dll"`). |
| **`filetype`** | Tipo de ficheiro visado pela regra. |
| **`hash` / `hash1`** | Resumo criptográfico ([[Preservação do Sistema e Integridade de Dados\|MD5, SHA-1 ou SHA-256]]) da amostra maliciosa de referência (ex.: `hash1 = "9f918fb741e951a10e68ce6874b839aef5a26d60486db31e509f8dcaa13acec5"`). |
| **`source` / `reference`** | URL ou referência externa sobre a ameaça (ex.: `reference = "https://goo.gl/WVflzO"`). |
| **`TLP`** | Classificação *Traffic Light Protocol* (ex.: `TLP = "WHITE"`). |
| **`license`** | Licença aplicável à regra. |
| **`min_yara_version`** | Versão mínima do YARA necessária para interpretar a regra. |
| **`threat_level`** | Nível numérico de ameaça (ex.: `threat_level = 3`). |
| **`in_the_wild`** | Booleano indicando se o *malware* foi detetado ativamente (ex.: `in_the_wild = true`). |

---

## 4. A Secção `condition:` e Análise das Regras de Exemplo da Aula

A secção `condition:` define os **critérios booleanos** requeridos para que um ficheiro ou processo produza uma avaliação positiva. Os padrões declarados na secção `strings:` (detalhados em [[YARA - Tipos de Strings, Modificadores, Formato Hexadecimal, Base64 e Regex]]) são referenciados pelo seu prefixo `$`.

### Exemplo 0 — Agrupamento por Comodins (`$a*`) e Quantificadores (`any of`, `N of`)
Na regra modelo:

```yara
condition:
    any of $a* or (2 of $b*) or (1 of $c*)
```

* **`$a*`**: agrupa todas as variáveis cujo nome começa por `$a` (`$a1`, `$a2`, `$a3`); `any of $a*` exige pelo menos uma delas.
* **`2 of $b*`**: exige que pelo menos **duas** das strings do grupo `$b` (`$b1`, `$b2`, `$b3`) estejam presentes.
* **`1 of $c*`**: exige pelo menos uma string do grupo `$c`.

### Exemplo 1 — `silent_banker` (Combinação de Tuplo de Strings, Regex e `filesize`)

```yara
rule silent_banker : banker
{
    meta:
        author = "someone"
        date = "2025.08.30"

    strings:
        $domain1 = "evilsite1.com" nocase
        $domain2 = "evilsite2.com"
        $domain3 = "evilsite3.com"
        $ip = /([0-9]{1,3}\.){3}[0-9]{1,3}/ wide ascii

    condition:
        2 of ($domain1, $domain2, $domain3) or
        ($ip and filesize < 1 KB)
}
```

* **Critério de disparo**: o ficheiro é avaliado positivamente se contiver pelo menos **2 dos 3 domínios** listados (`$domain1`, `$domain2`, `$domain3`) **OU** se contiver simultaneamente um endereço IPv4 (`$ip` em formato Unicode ou ASCII) **e** o tamanho total do ficheiro for inferior a 1 Kilobyte (`filesize < 1 KB`).

### Exemplo 2 — `silent_banker2` (Restrição Posicional `in (0..100)` e Sequência Hex DOS)

```yara
rule silent_banker2 : banker
{ /* This is a comment */
    meta:
        description = "This is just an example"
        threat_level = 3
        in_the_wild = true

    strings:
        $a = {6A 40 68 00 30 00 00 6A 14 8D 91}
        $b = {8D 4D B0 2B C1 83 C0 27 99 6A 4E 59 F7 F9}
        $c = "UVODFRYSIHLNWPEJXQZAKCBGMT"
        $d = {54 68 69 73 20 70 72 6F 67 72 61 6D 20 63 61 6E 6E 6F 74
              20 62 65 20 72 75 6E 20 69 6E 20 44 4F 53}

    condition:
        $a in (0..100) or $b or $c or $d
}
```

* **`$a in (0..100)`**: exige que a sequência hexadecimal `$a` seja encontrada dentro dos **primeiros 100 octetos (bytes)** do ficheiro.
* **`$d`**: a sequência hexadecimal `{54 68 69 73 ... 44 4F 53}` traduz-se em ASCII para a clássica mensagem do cabeçalho DOS de executáveis PE: **`"This program cannot be run in DOS"`**.
* Basta que `$a` (nos primeiros 100 bytes), `$b`, `$c` ou `$d` exista para identificar o ficheiro.

### Exemplo 3 — `GRIZZLY_STEPPE_Malware_1` (`uint16(0) == 0x5a4d` e `4 of them`)
Regra real do repositório `Yara-Rules` (`APT_APT29_Grizzly_Steppe.yar`), da autoria de **Florian Roth**:

```yara
rule GRIZZLY_STEPPE_Malware_1
{
    meta:
        description = "Auto-generated rule - file HRDG022184_certclint.dll"
        author = "Florian Roth"
        reference = "https://goo.gl/WVflzO"
        date = "2016-12-29"
        hash1 = "9f918fb741e951a10e68ce6874b839aef5a26d60486db31e509f8dcaa13acec5"

    strings:
        $s1 = "S:\\Lidstone\\renewing\\HA\\disable\\In.pdb" fullword ascii
        $s2 = "Repeat last find command)Replace specific text with different text" fullword wide
        $s3 = "l\\Processor(0)\\% Processor Time" fullword wide
        $s6 = "Self Process" fullword wide
        $s7 = "Default Process" fullword wide
        $s8 = "Star Polk.exe" fullword wide

    condition:
        ( uint16(0) == 0x5a4d and filesize < 300KB and 4 of them )
}
```

* **`uint16(0) == 0x5a4d`**: lê um inteiro sem sinal de 16 bits (2 bytes) no *offset* `0` do ficheiro para confirmar a assinatura `MZ` de executável PE.
* **`filesize < 300KB`**: restringe a pesquisa a ficheiros com menos de 300 KB.
* **`4 of them`**: exige que pelo menos **4 de todas as strings declaradas** (`$s1` a `$s8`) estejam presentes no ficheiro.

> [!IMPORTANT] Armadilha Clássica de Exame: `$mz = { 4D 5A }` vs. `uint16(0) == 0x5a4d`
> * Na secção **`strings:`**, `$mz = { 4D 5A }` (ou `$mz = "MZ"`) descreve uma **sequência literal de bytes no ficheiro** lida da esquerda para a direita: byte `0` = `0x4D` (`M`), byte `1` = `0x5A` (`Z`).
> * Na secção **`condition:`**, **`uint16(0)`** interpreta os dois bytes nos offsets `0` e `1` como um **inteiro numérico de 16 bits em [[Endianness e Ordem de Armazenamento|Little-Endian]]**: o byte menos significativo (`0x4D`) ocupa o offset `0` e o mais significativo (`0x5A`) ocupa o offset `1`, resultando no valor hexadecimal invertido **`0x5a4d`** (e não `0x4d5a`).

---

## 5. Implicações Forenses

* **Desempenho por Curto-Circuito (`uint16(0) == 0x5a4d` e `filesize`)**: colocar `uint16(0) == 0x5a4d and filesize < 300KB` no início da `condition:` permite ao motor YARA descartar quase instantaneamente ficheiros que não sejam executáveis PE ou que excedam 300 KB, evitando varrer inutilmente gigabytes de ficheiros multimédia ou bases de dados.
* **Caminho PDB (`$s1 = "S:\...\In.pdb"`)**: na regra `GRIZZLY_STEPPE_Malware_1`, o primeiro indicador `$s1` é o caminho do ficheiro *Program Database* (`.pdb`) gerado pelo compilador Visual Studio na máquina do autor do *malware*, constituindo uma assinatura forense de altíssima especificidade.

---

## Além da aula

* **Ponte com Endianness e Integridade em [[00 AFD1|AFD1]]**:
  * A distinção entre `$mz = { 4D 5A }` e `uint16(0) == 0x5a4d` é uma aplicação prática direta do capítulo [[Endianness e Ordem de Armazenamento]] de AFD1.
  * Já o atributo `hash1` na secção `meta:` (com um resumo `SHA-256` de 64 caracteres hexadecimais) liga-se a [[Preservação do Sistema e Integridade de Dados]] e [[Pesquisa de Evidências e Reconstrução de Eventos]]: enquanto o hash SHA-256 identifica apenas uma amostra estática exata (que falha se o atacante alterar 1 único bit), a regra YARA permite detetar toda a família de variantes que partilhem pelo menos 4 das strings (`4 of them`).

---

## Perguntas de revisão

1. **Qual é a finalidade do YARA e porque se diz que a sua deteção é binária?**

> [!success]- Ver Resposta
> O YARA é uma ferramenta *signature-based* destinada a pesquisar padrões de *malware* e IOCs em ficheiros, diretorias e processos através de regras descritivas. A sua deteção é estritamente binária porque cada regra devolve apenas um resultado **positivo** (a amostra satisfaz a `condition:`) ou **negativo** (não satisfaz).

2. **Quando foi lançado o YARA pela VirusTotal, sob que licença é disponibilizado e qual é o seu estado atual desde 2025?**

> [!success]- Ver Resposta
> Foi lançado em **2013** pela VirusTotal (criado originalmente por Victor M. Alvarez) sob licença de código aberto **BSD-3**. Desde **2025** encontra-se em ***maintenance mode***, sendo sucedido pela reimplementação oficial em Rust designada **YARA-X** (`yr`).

3. **Quais são as três secções que compõem uma regra YARA e em que difere o papel da `meta:` face às secções `strings:` e `condition:`?**

> [!success]- Ver Resposta
> As três secções são **`meta:`** (documentação da regra com `author`, `date`, `hash`, `TLP`, etc.), **`strings:`** (definição dos padrões em texto, hexadecimal ou regex) e **`condition:`** (lógica booleana que determina o disparo). Ao contrário de `strings:` e `condition:`, a secção **`meta:` não interfere na avaliação nem no resultado da deteção**.

4. **Na condição `( uint16(0) == 0x5a4d and filesize < 300KB and 4 of them )`, o que verifica `uint16(0) == 0x5a4d` e porque surge `0x5a4d` em vez de `0x4d5a`?**

> [!success]- Ver Resposta
> Verifica se o ficheiro começa pela assinatura `MZ` (`4D 5A` em ASCII), identificando um executável DOS/Windows (PE). Surge como **`0x5a4d`** porque `uint16(0)` lê um inteiro sem sinal de 16 bits no *offset* `0` usando ordenação **Little-Endian** (x86), na qual o primeiro byte (`4D`) é o menos significativo e o segundo (`5A`) o mais significativo — ao contrário de `$mz = { 4D 5A }` em `strings:`, que lê bytes sequencialmente.

5. **Porque é vantajoso colocar condições como `uint16(0) == 0x5a4d and filesize < 300KB` antes de `4 of them` na `condition:`?**

> [!success]- Ver Resposta
> Permite a avaliação por **curto-circuito**: o motor YARA valida primeiro dois bytes no offset `0` e o tamanho do ficheiro, descartando de imediato ficheiros não-PE ou superiores a 300 KB sem despender tempo a pesquisar strings em grandes volumes de dados.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Capítulo 3 - YARA - MOTW - Strings]] | Início do capítulo |
| **Seguinte** | [[YARA - Tipos de Strings, Modificadores, Formato Hexadecimal, Base64 e Regex]] | `mesmo bloco` |
| **Índice** | [[Capítulo 3 - YARA - MOTW - Strings]] · [[00 ASSI]] | `Bloco 01` |

### Conceitos Relacionados

* [[Execução e Compilação no YARA (yara e yarac), Casos Reais (UPX, WannaCry) e LLMs]] · `mesmo bloco`
* [[YARA-X (Reimplementação em Rust) e Ferramenta CLI yr]] · `mesmo bloco`
* [[Scanner de IOCs LOKI (Versão Python) - Métodos de Deteção e Configuração]] · `mesmo bloco`
* [[Endianness e Ordem de Armazenamento]] · `AFD1 · Cap. 3`
* [[Preservação do Sistema e Integridade de Dados]] · `AFD1 · Cap. 1`
* [[Pesquisa de Evidências e Reconstrução de Eventos]] · `AFD1 · Cap. 1`
