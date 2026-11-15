---
title: Funções de Hash Criptográficas (MD5, SHA-1, SHA-2, SHA-3 e RIPEMD)
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Segurança em Redes de Computadores
sigla_uc: SRC
capitulo: 2
bloco: 3
fonte_aula: aula_02_update.pdf (Slides 34–35, 40–45); aula02_leituras_resumo.pdf (Stallings Cap. 11)
tags:
  - src
  - criptografia
  - hash
  - md5
  - sha
aliases:
  - Funções de Hash
  - MD5
  - SHA-1
  - SHA-2
  - SHA-3
atualizado: 2026-11-15
---

# Funções de Hash Criptográficas (`MD5`, `SHA-1`, `SHA-2`, `SHA-3` e `RIPEMD`)

Uma função de *hash* criptográfica $h = H(M)$ transforma uma mensagem $M$ de **tamanho variável (arbitrário)** num resumo (*message digest*) de **tamanho fixo**, garantindo integridade dos dados.

> [!TIP] Lógica de Funcionamento e Valor de Segurança
> * **Porque existe (Integridade)**: Permite verificar rapidamente se ficheiros, mensagens ou artefactos foram alterados, comparando o resumo gerado com o valor de referência.
> * **Porque importa (Segurança / Forense)**: Serve de base a assinaturas digitais, `HMAC` e validação de integridade forense; porém, algoritmos legados como `MD5` e `SHA-1` sofrem de colisões conhecidas.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Entrada variável $\rightarrow$ Saída fixa**: deve ser computacionalmente impraticável encontrar duas entradas distintas com o mesmo *hash* (resistência a colisões) ou reverter o *hash* (unidirecionalidade).
>   * **Uma função de *hash* por si só NÃO usa chave secreta**: logo, não autentica a origem nem substitui um `MAC` sem proteção adicional.

---

## 1. Estrutura Geral e Requisitos

O processamento típico de uma função de *hash* iterativa inclui:
1. **Padding**: preenchimento da mensagem até múltiplo de um tamanho de bloco fixo (ex.: `512` ou `1024` bits);
2. **Length**: adição do tamanho original da mensagem;
3. **Processamento iterativo**: atualização de um *hash buffer* inicializado, produzindo no final $h = H(M)$.

**Propriedades essenciais (Slides / TBL #2 / Stallings Cap. 11):**
* Entrada de tamanho variável $\rightarrow$ saída de tamanho fixo;
* Execução rápida e fácil de implementar;
* **Unidirecionalidade (*Preimage resistance*)**: impraticável obter $M$ a partir de $H(M)$;
* **Resistência a colisões**: computacionalmente impraticável encontrar $M_1 \neq M_2$ tal que $H(M_1) = H(M_2)$.

---

## 2. Principais Algoritmos e Comandos Linux

| Algoritmo | Bloco de Entrada | Tamanho da Saída | Referência / Notas |
| :--- | :---: | :---: | :--- |
| **`MD5`** | `512` bits | **`128` bits** | `RFC 1321` (Abril 1992). Rápido; historicamente usado para *checksums*, hoje vulnerável a colisões. |
| **`SHA-1`** | `512` bits | **`160` bits** | `FIPS 180` (NIST) / `RFC 6234`; funcionamento semelhante ao `MD4`, criado para corrigir falhas anteriores (tamanho máximo $2^{64}-1$ bits). |
| **`SHA-2`** | `512` / `1024` bits | `224` / `256` / `384` / `512` bits | Ex.: `SHA-512` usa *buffer* de `512` bits, blocos de `1024` bits e **80 *rounds***. |
| **`SHA-3`** | Variável (*Keccak*) | `224` / `256` / `384` / `512` bits | Padrão NIST mais recente (construção esponja). |
| **`RIPEMD`** | `512` bits | `160` bits (tipicamente) | Desenvolvido pelo **RIPE-NCC**. |

**Comandos práticos demonstrados nos slides (Slides 41–42):**

```bash
# Gerar e verificar resumo MD5
md5sum /etc/passwd > /tmp/md5sum.txt
md5sum -c /tmp/md5sum.txt

# Calcular diretamente do STDIN (terminar com Ctrl+D)
md5sum -

# Família SHA
sha1sum /etc/passwd > /tmp/sha1sum.txt
sha1sum -c /tmp/sha1sum.txt
man sha256sum
man sha224sum
```

---

## Perguntas de revisão

1. **Quais são os tamanhos de bloco e de saída do `MD5` e do `SHA-1`?**

> [!success]- Ver Resposta
> Ambos processam blocos de `512` bits; o **`MD5`** produz um *hash* de **`128` bits**, enquanto o **`SHA-1`** produz um *hash* de **`160` bits**.

2. **Porque é que uma função de *hash* simples (`M || H(M)`) enviada em claro não garante autenticidade da origem?**

> [!success]- Ver Resposta
> Porque o algoritmo de *hash* é público e não utiliza qualquer segredo partilhado ou chave privada: um atacante pode alterar `M` para `M'` e recalcular `H(M')` sem que o recetor detete a adulteração.

## Notas relacionadas

- [[Autenticação de Mensagens (MAC, HMAC) e Assinaturas Digitais]]
- [[TBL 2 - Fundamentos de Criptografia]]
- [[Exercícios Práticos - Integridade de Dados e Hashes]]
