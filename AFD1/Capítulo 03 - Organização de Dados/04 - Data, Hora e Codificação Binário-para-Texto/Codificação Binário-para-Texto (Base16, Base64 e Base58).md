---
title: Codificação Binário-para-Texto (Base16, Base64 e Base58)
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Análise Forense Digital I
sigla_uc: AFD1
capitulo: 3
bloco: 4
fonte_aula: MCIF – Digital Forensic Analysis 1 - Data Organization.pdf
tags:
  - afd1
  - forense
  - encoding
  - base16
  - base64
  - base58
  - bitcoin
aliases:
  - Binary-to-text Encoding
  - Base16
  - Base64
  - Base58
atualizado: 2026-10-19
---

# Codificação Binário-para-Texto (Base16, Base64 e Base58)

A **codificação binário-para-texto (*binary-to-text encoding*)** transforma dados binários (ou texto) numa sequência de caracteres imprimíveis para permitir a sua transmissão segura através de canais que não suportam dados binários puros (como o correio eletrónico). Trata-se de uma operação **reversível** que inflaciona o tamanho original dos dados e que **não deve ser confundida com cifragem/encriptação**, pois não utiliza qualquer chave secreta. As técnicas mais comuns em análise forense são o **Hexadecimal (Base16)**, o **Base64** e o **Base58**.

---

## Conceito de Codificação Binário-para-Texto (*Binary-to-Text Encoding*)

* Consiste na codificação de dados em texto simples (*plain text*), isto é, na representação de dados binários através de uma **sequência de caracteres imprimíveis** (*printable characters*).
* É necessária para a transmissão de dados quando o canal de comunicação não permite o envio direto de dados binários (ex.: correio eletrónico / *email*).
* **Inflação de tamanho**: a codificação **aumenta (*inflates*) o tamanho dos dados originais**, dependendo a taxa de inflação da técnica utilizada.
* É uma **operação reversível** (qualquer pessoa que conheça o algoritmo reconstrói o dado original).
* Pode também ser aplicada sobre texto simples (*plain text*).

> [!IMPORTANT] Codificação (*Encoding*) NÃO é Encriptação (*Encryption*)
> * **Encriptação (*encryption*)**: requer uma **chave (*key*)**, habitualmente secreta, para proteger a confidencialidade dos dados.
> * **Codificação (*encoding*)**: **não depende de qualquer chave**; o seu objetivo é apenas a compatibilidade de representação e transporte.

---

## Técnicas Comuns de Codificação (*Common Encoding Techniques*)

| Técnica | Conjunto de Caracteres Usados (*Alphabet*) | Regras e Contextos de Utilização | Exemplo Prático |
| :--- | :--- | :--- | :--- |
| **Hexadecimal (Base16)** | `[0..9]` e `[A..F]` (ou `[a..f]`) | Valores de *hash* (`MD5`, `SHA-256`, etc.) são habitualmente exibidos em hexadecimal (duplica o tamanho face ao binário: 1 byte = 2 chars). | `"Hello World"` $\rightarrow$<br/>`48656c6c6f20776f726c64` |
| **Base64** | `[A..Z]`, `[a..z]`, `[0..9]` e `[+, /]` | O tamanho da string Base64 tem de ser **múltiplo de 4**, pelo que o carácter **`=`** é usado no final como preenchimento (*padding*). Usado em servidores de email (**MIME**), **OpenPGP**, etc. | `"Hello World"` $\rightarrow$<br/>`SGVsbG8gV29ybGQ=` |
| **Base58** | Semelhante ao Base64 (58 caracteres alfanuméricos) | Modificado para **evitar caracteres não alfanuméricos** (`+`, `/`) e **letras/dígitos visualmente ambíguos quando impressos** (`0`, `O`, `I`, `l`). Usado em **Bitcoin**. | **Chave pública Bitcoin**:<br/>`1ZNz2KDm8epACBA5bjgKQbRyaGcDt3XV2`<br/>**Chave privada Bitcoin**:<br/>`Ky1ZcCSMziFtdxfDEjANw3PZUZQQLjh6hKpX1CinVtJscnAFnvcn` |

---

## Implicações Forenses

* **Identificação Visual em Exames Periciais**:
  * Strings alfanuméricas compridas terminadas em `=` ou `==` (com caracteres `+` e `/`) indiciam quase sempre **Base64** (ex.: anexos de e-mail extraídos em bruto de ficheiros `.eml`/`.mbox` ou *payloads* de comandos PowerShell ofuscados).
  * Endereços e chaves privadas de criptomoedas (**Bitcoin**) começando por `1`, `3`, `5`, `K` ou `L` sem os caracteres `0`, `O`, `I`, `l` indicam codificação **Base58 / Base58Check**, sendo artefactos de elevado valor probatório em investigações de crimes económico-financeiros ou *ransomware*.

---

## Além da aula

* **Casos Práticos de Codificação (`Base64`, `Base16` e `ROT13`) em Artefactos do Windows ([[00 ASSI|ASSI]])**:
  * **Extração de Área de Transferência em Base64 ([[Recuperação de Clipboard e Sincronização na Timeline]])**: Quando o histórico do Clipboard (`Win+V`) e o *Cloud Sync* estão ativos, o serviço `CDPUserSvc` grava o texto copiado na coluna `ClipboardPayload` de `ActivitiesCache.db` dentro de um JSON cujo campo `"content"` está codificado em **Base64** (ex.: `"SXN0byDDqSB1bSB0ZXN0ZSE="` $\rightarrow$ `"Isto é um teste!"`).
  * **Identificador `PlatformDeviceId` em Base64 ([[Windows Activity Timeline - Arquitetura e Base SQLite]])**: Na mesma base `ActivitiesCache.db`, o identificador da máquina sincronizada é uma string **Base64** terminada no carácter de *padding* `=` (ex.: `0Yb2A9Xf+CNQxR57p1SOcH0DmUwpLCcqY/PUKTzth/Q=`), mapeada na chave `TaskFlow\DeviceCache`.
  * **Payloads PowerShell em Base64 Ocultos em Atalhos ([[Abuso e Vetores de Ataque com Ficheiros LNK]])**: Grupos APT (como o *APT10*) exploram o limite visual de 256 caracteres das propriedades do Windows Explorer para esconder, até aos 4096 caracteres do ficheiro `.lnk`, chamadas a `powershell -enc <Base64>`.
  * **Ofuscação por Substituição Reversível (`ROT13`) vs. Encriptação**: No [[Artefacto Forense UserAssist]], o Windows aplica a cifra de César **ROT13** aos nomes dos executáveis e atalhos (`.exe` $\rightarrow$ `.RKR`, `.lnk` $\rightarrow$ `.YAX`). Tal como o Base64, o ROT13 **não utiliza chave secreta**, funcionando apenas como ofuscação ligeira facilmente reversível por ferramentas como o `RegistryExplorer`.

---

## Perguntas de revisão

- Qual é a finalidade da codificação binário-para-texto e porque não pode ser considerada uma forma de encriptação?
- Porque é que algumas strings em Base64 terminam com o símbolo `=`? Em que protocolos/sistemas é utilizado o Base64?
- O que distingue o Base58 do Base64 e em que tecnologia é amplamente utilizado?

## Notas relacionadas

- [[Sistemas de Numeração e Conversão entre Bases]]
- [[Codificação de Caracteres - ASCII, Latin-1 e Unicode]]
- [[Preservação do Sistema e Integridade de Dados]]
- [[Recuperação de Clipboard e Sincronização na Timeline]]
- [[Windows Activity Timeline - Arquitetura e Base SQLite]]
- [[Abuso e Vetores de Ataque com Ficheiros LNK]]
- [[Artefacto Forense UserAssist]]
- [[Capítulo 3 - Organização de Dados]]
