---
title: Funções de Hash Criptográficas e Integridade (MD5, SHA-1, SHA-2 e SHA-3)
tipo: conceito
mestrado: Cibersegurança e Informática Forense
sigla_uc: COMUM
ucs_relacionadas:
  - SRC
  - AFD1
  - ASSI
tags:
  - comum
  - criptografia
  - hash
  - integridade
  - md5
  - sha1
  - sha2
  - sha3
  - ripemd
aliases:
  - Funções de Hash Criptográficas (MD5, SHA-1, SHA-2, SHA-3 e RIPEMD)
  - Funções de Hash
  - MD5
  - SHA-1
  - SHA-2
  - SHA-3
atualizado: 2026-11-18
---

# Funções de Hash Criptográficas e Integridade (MD5, SHA-1, SHA-2 e SHA-3)

Uma função de *hash* criptográfica $h = H(M)$ transforma uma mensagem $M$ de **tamanho variável (arbitrário)** num resumo (*message digest*) de **tamanho fixo**, permitindo verificar a integridade dos dados.

> [!TIP] Lógica de Funcionamento e Valor Transversal
> * **Porque existe (Integridade)**: Permite detetar rapidamente se ficheiros, mensagens ou artefactos sofreram alterações bit-a-bit, comparando o resumo gerado com um valor de referência.
> * **Porque importa (Segurança / Forense / Sistemas)**: Serve de alicerce a assinaturas digitais, `HMAC`, manifestos de cadeia de custódia, deteção de malware por *IOCs* e armazenamento de credenciais (quando combinado com *salt* e *key stretching*); algoritmos legados como `MD5` e `SHA-1` apresentam colisões conhecidas.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Entrada variável $\rightarrow$ Saída fixa**: exige resistência à pré-imagem (unidirecionalidade), à segunda pré-imagem e a colisões.
>   * **Sem chave secreta**: uma função de *hash* isolada **não autentica a origem**, pois qualquer atacante pode alterar $M$ para $M'$ e recalcular $H(M')$; requer `HMAC` ou assinatura digital.
>   * **Rápidas por desenho**: em armazenamento de *passwords*, a rapidez do `MD5`/`SHA` facilita ataques de força bruta, exigindo *per-credential salt* e *key stretching* lento (`Argon2`/`PBKDF2`).

---

## 1. Estrutura Geral e Requisitos

O processamento típico de uma função de *hash* iterativa inclui:

1. **Padding**: preenchimento da mensagem até múltiplo de um tamanho de bloco fixo (ex.: `512` ou `1024` bits);
2. **Length**: adição do tamanho original da mensagem;
3. **Processamento iterativo**: atualização de um *hash buffer* inicializado, produzindo no final $h = H(M)$.

**Propriedades essenciais (Slides / TBL #2 / Stallings Cap. 11):**

* Entrada de tamanho variável $\rightarrow$ saída de tamanho fixo;
* Execução rápida e fácil de implementar;
* **Unidirecionalidade (*Pre-image resistance*)**: computacionalmente impraticável obter $M$ a partir de $H(M)$;
* **Resistência à segunda pré-imagem (*Second pre-image resistance*)**: dado $M_1$, é computacionalmente impraticável encontrar $M_2 \neq M_1$ tal que $H(M_1) = H(M_2)$;
* **Resistência a colisões (*Collision resistance*)**: computacionalmente impraticável encontrar quaisquer duas entradas distintas $M_1 \neq M_2$ tais que $H(M_1) = H(M_2)$.

---

## 2. Principais Algoritmos e Comandos Linux

| Algoritmo | Bloco de Entrada | Tamanho da Saída | Referência / Notas |
| :--- | :---: | :---: | :--- |
| **`MD5`** | `512` bits | **`128` bits** | `RFC 1321` (Abril 1992). Rápido; historicamente usado para *checksums*, **quebrado desde 2004** (vulnerável a colisões). |
| **`SHA-1`** | `512` bits | **`160` bits** | `FIPS 180` (NIST) / `RFC 6234`; funcionamento semelhante ao `MD4`, criado para corrigir falhas anteriores (tamanho máximo $2^{64}-1$ bits); obsoleto por colisões práticas. |
| **`SHA-2`** | `512` / `1024` bits | `224` / `256` / `384` / `512` bits | Ex.: `SHA-512` usa *buffer* de `512` bits, blocos de `1024` bits e **80 *rounds***. Padrão atual recomendado (`SHA-256`, `SHA-512`). |
| **`SHA-3`** | Variável (*Keccak*) | `224` / `256` / `384` / `512` bits | Padrão NIST mais recente (construção esponja / *sponge construction*). |
| **`RIPEMD`** | `512` bits | `160` bits (tipicamente) | Desenvolvido pelo **RIPE-NCC** (variantes de `160`, `256` e `320` bits). |

**Comandos práticos em Linux (`md5sum` / família `sha*sum`):**

```bash
# Gerar e verificar resumo MD5
md5sum /etc/passwd > /tmp/md5sum.txt
md5sum -c /tmp/md5sum.txt

# Calcular diretamente do STDIN (terminar com Ctrl+D)
md5sum -

# Família SHA
sha1sum /etc/passwd > /tmp/sha1sum.txt
sha1sum -c /tmp/sha1sum.txt
sha256sum /etc/passwd > /tmp/sha256sum.txt
sha256sum -c /tmp/sha256sum.txt
man sha256sum
man sha224sum
```

---

## Aplicação por UC

### Em SRC (Criptografia Aplicada, MAC e HMAC)

* **Integridade vs. Autenticidade**: Uma função de *hash* pública garante apenas deteção de erros acidentais quando o resumo está protegido; enviada em claro (`M || H(M)`), não autentica a origem porque qualquer atacante pode substituir `M` por `M'` e recalcular `H(M')`.
* **Autenticação com Chave**: Para autenticar integridade e origem em trânsito, combina-se uma chave secreta partilhada através de **`HMAC`** (ou cifra-se/assina-se o resumo com chave privada). Ver [[Autenticação de Mensagens (MAC, HMAC) e Assinaturas Digitais]] e [[TBL 2 - Fundamentos de Criptografia]].

### Em AFD1 (Integridade de Evidência Digital e Cadeia de Custódia)

* **Verificação Forense (`MD5` vs. `SHA-256`)**: Como o `MD5` está quebrado por colisões desde 2004, a prática pericial moderna exige `SHA-256` (ou `SHA-2`/`SHA-3`), calculado em tempo real durante a aquisição com ferramentas como o `dcfldd` ([[Aquisição em Linha de Comandos no Linux - dcfldd e Derivados do dd]]) e validado em lote com `sha256sum -c` ([[Exercícios Práticos - Integridade de Dados e Hashes]]).
* **Limite do *Hash* Isolado perante Adversário**: Se um atacante tiver acesso de escrita ao ficheiro onde o manifesto de *hashes* é armazenado, pode alterar a evidência e recalcular o respetivo resumo. Por isso, a preservação exige combinar *hashes* com **assinaturas digitais** (ex.: Cartão de Cidadão) para garantir integridade, autenticidade e não-repúdio em tribunal ([[Preservação do Sistema e Integridade de Dados]]).

### Em ASSI (Armazenamento de Passwords, Hashcat e IOCs)

* **Armazenamento Seguro de Passwords**: Funções de *hash* rápidas como `MD5` ou `SHA-256` sem proteção adicional são inseguras para *passwords*, pois permitem consultas instantâneas em *rainbow tables* e taxas elevadíssimas de tentativa em GPU. A defesa requer **salt único por credencial** (*per-credential salt*) e funções lentas de ***key stretching*** como `Argon2` ou `PBKDF2` ([[Armazenamento Seguro de Passwords (Salting e Key Stretching) e Casos RockYou e LastPass]]).
* **Auditoria e Deteção de IOCs**: Na auditoria ofensiva/defensiva, o `Hashcat` explora precisamente a velocidade destes algoritmos para testar milhões/milhares de milhões de candidatos por segundo ([[Cracking e Auditoria de Passwords com Hashcat (Hashcat 101 e Máscaras)]]); na resposta a incidentes, *scanners* como o LOKI usam bases de *hashes* (`MD5`/`SHA-1`/`SHA-256`) como Indicadores de Compromisso (IOCs) para identificar binários maliciosos conhecidos ([[Scanner de IOCs LOKI (Versão Python) - Métodos de Deteção e Configuração]]).

---

## Perguntas de revisão

1. **Quais são os tamanhos de bloco e de saída do `MD5` e do `SHA-1`, e porque não devem ser escolhidos para novas implementações de integridade?**

> [!success]- Ver Resposta
> Ambos processam blocos de `512` bits; o **`MD5`** gera resumos de **`128` bits** e o **`SHA-1`** gera resumos de **`160` bits**. Não devem ser usados em novas implementações porque ambos sofrem de vulnerabilidades práticas de **colisão** (`MD5` quebrado desde 2004), devendo privilegiar-se `SHA-2` (`SHA-256`/`SHA-512`) ou `SHA-3`.

2. **Porque é que uma função de *hash* simples (`M || H(M)`) enviada em claro não garante autenticidade da origem em `SRC` nem protege a evidência em `AFD1` contra um atacante com acesso de escrita ao manifesto?**

> [!success]- Ver Resposta
> Porque o algoritmo de *hash* é público e não depende de qualquer segredo: um atacante pode alterar `M` para `M'` e recalcular `H(M')`. Para garantir autenticidade e não adulteração é necessário um **`HMAC`** (chave secreta partilhada) ou uma **assinatura digital** (chave privada).

3. **Qual a diferença entre resistência à pré-imagem, resistência à segunda pré-imagem e resistência a colisões?**

> [!success]- Ver Resposta
> A **resistência à pré-imagem** (unidirecionalidade) impede recuperar $M$ a partir de $H(M)$; a **resistência à segunda pré-imagem** impede encontrar $M_2 \neq M_1$ com $H(M_2)=H(M_1)$ dado um $M_1$ fixo; a **resistência a colisões** impede encontrar qualquer par distinto $(M_1, M_2)$ tal que $H(M_1)=H(M_2)$.

4. **Porque é que funções de *hash* rápidas como `MD5` e `SHA-256` são adequadas para verificar integridade de imagens forenses, mas inadequadas para armazenar *passwords* diretamente?**

> [!success]- Ver Resposta
> Na verificação forense pretende-se velocidade para processar gigabytes de dados e detetar alterações acidentais/maliciosas; no armazenamento de *passwords*, essa mesma rapidez permite ao atacante (ex.: via `Hashcat` em GPU) testar milhares de milhões de candidatos por segundo e usar *lookup tables* se não houver *per-credential salt* e *key stretching* lento (`Argon2` ou `PBKDF2`).

---

## Notas relacionadas

- [[Autenticação de Mensagens (MAC, HMAC) e Assinaturas Digitais]]
- [[TBL 2 - Fundamentos de Criptografia]]
- [[Assinaturas Digitais, PKI e GnuPG]]
- [[Preservação do Sistema e Integridade de Dados]]
- [[Exercícios Práticos - Integridade de Dados e Hashes]]
- [[Aquisição em Linha de Comandos no Linux - dcfldd e Derivados do dd]]
- [[Armazenamento Seguro de Passwords (Salting e Key Stretching) e Casos RockYou e LastPass]]
- [[Cracking e Auditoria de Passwords com Hashcat (Hashcat 101 e Máscaras)]]
- [[Scanner de IOCs LOKI (Versão Python) - Métodos de Deteção e Configuração]]
