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
atualizado: 2026-11-11
---

# Codificação Binário-para-Texto (Base16, Base64 e Base58)

A codificação binário-para-texto converte bytes em caracteres imprimíveis para transporte seguro em canais textuais, sendo reversível e sem chave secreta ao contrário da encriptação.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: Protocolos textuais antigos (como SMTP/email) interpretam certos bytes binários de controlo como delimitadores de mensagem ou fim de linha; codificações como Base16, Base64 e Base58 garantem integridade no transporte usando apenas texto imprimível.
> * **Porque importa (Forense)**: Anexos de email MIME, payloads ofuscados em PowerShell (`-enc`), dados em JSON/SQLite e carteiras Bitcoin surgem codificados em Base64 ou Base58; identificá-los pelo alfabeto e *padding* permite reverter imediatamente o conteúdo sem qualquer chave.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Codificação não é encriptação**: é totalmente reversível por qualquer pessoa sem chave secreta, não oferecendo confidencialidade.
>   * **Inflação de dados**: toda a codificação binário-para-texto aumenta o tamanho original (ex.: Base16 duplica o tamanho: `1` byte $\rightarrow$ `2` caracteres).
>   * **Base64 vs. Base58**: o **Base64** exige comprimento múltiplo de 4 usando **`=`** como *padding* (e inclui `+`, `/`); o **Base58** (usado em Bitcoin) remove `+`, `/` e os caracteres visualmente ambíguos **`0`, `O`, `I`, `l`**.

---

## Conceito de Codificação Binário-para-Texto (*Binary-to-Text Encoding*)

* Consiste na codificação de dados em texto simples, isto é, na representação de dados binários através de uma **sequência de caracteres imprimíveis**.
* É necessária para a transmissão de dados quando o canal de comunicação não permite o envio direto de dados binários (ex.: correio eletrónico / email).
* **Inflação de tamanho**: a codificação **aumenta o tamanho dos dados originais**, dependendo a taxa de inflação da técnica utilizada.
* É uma **operação reversível** (qualquer pessoa que conheça o algoritmo reconstrói o dado original).
* Pode também ser aplicada sobre texto simples.

> [!IMPORTANT] Codificação NÃO é Encriptação
> * **Encriptação**: requer uma **chave**, habitualmente secreta, para proteger a confidencialidade dos dados.
> * **Codificação**: **não depende de qualquer chave**; o seu objetivo é apenas a compatibilidade de representação e transporte.

---

## Técnicas Comuns de Codificação

| Técnica | Conjunto de Caracteres Usados | Regras e Contextos de Utilização | Exemplo Prático |
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
  * **Pesquisa Forense de Base64 e Endereços Bitcoin (Base58) em Binários ([[Capítulo 3 - YARA - MOTW - Strings]])**: Na ferramenta [[Eric Zimmerman bstrings - Parâmetros, Expressões Regulares e Exercícios|bstrings]], os padrões de expressões regulares integrados `--lr b64` e `--lr bitcoin` aplicam diretamente os alfabetos Base64 e Base58 para extrair cadeias codificadas e carteiras de criptomoedas, enquanto em [[YARA - Tipos de Strings, Modificadores, Formato Hexadecimal, Base64 e Regex]] o modificador `base64` calcula e procura automaticamente as 3 permutações de alinhamento Base64 de uma *string*.

---

## Perguntas de revisão

1. **Qual é a finalidade da codificação binário-para-texto e porque não pode ser considerada uma forma de encriptação?**

> [!success]- Ver Resposta
> Destina-se a converter dados binários (ou texto) em caracteres imprimíveis compatíveis com canais textuais como o email. **Não é encriptação** porque não utiliza qualquer chave secreta: trata-se de uma operação puramente reversível por qualquer pessoa que conheça o algoritmo.

2. **Qual é o impacto da codificação binário-para-texto no tamanho dos dados e qual a taxa de expansão do Base16?**

> [!success]- Ver Resposta
> Todas as codificações binário-para-texto **inflacionam o tamanho original dos dados**. No caso do **Hexadecimal (Base16)**, cada byte é representado por dois caracteres hexadecimais, **duplicando** exatamente o tamanho face aos dados binários originais.

3. **Porque é que algumas strings Base64 terminam em `=` ou `==` e em que protocolos/contextos forenses é utilizado?**

> [!success]- Ver Resposta
> Como o comprimento total de uma string Base64 tem de ser **múltiplo de 4**, o carácter **`=`** (uma ou duas vezes no final) serve como preenchimento (*padding*). É amplamente usado em anexos de email (**MIME**), chaves/mensagens **OpenPGP**, JSON e *payloads* PowerShell (`-enc`).

4. **O que distingue o Base58 do Base64 e em que tecnologia é amplamente utilizado?**

> [!success]- Ver Resposta
> O **Base58** elimina os caracteres não alfanuméricos (`+` e `/`) e os quatro caracteres visualmente ambíguos quando impressos (**`0`**, **`O`**, **`I`** e **`l`**), reduzindo o alfabeto para 58 símbolos alfanuméricos. É utilizado nas chaves públicas e privadas de **Bitcoin**.

## Notas relacionadas

- [[Sistemas de Numeração e Conversão entre Bases]]
- [[Codificação de Caracteres - ASCII, Latin-1 e Unicode]]
- [[Preservação do Sistema e Integridade de Dados]]
- [[Recuperação de Clipboard e Sincronização na Timeline]]
- [[Windows Activity Timeline - Arquitetura e Base SQLite]]
- [[Abuso e Vetores de Ataque com Ficheiros LNK]]
- [[Artefacto Forense UserAssist]]
- [[Capítulo 3 - Organização de Dados]]
