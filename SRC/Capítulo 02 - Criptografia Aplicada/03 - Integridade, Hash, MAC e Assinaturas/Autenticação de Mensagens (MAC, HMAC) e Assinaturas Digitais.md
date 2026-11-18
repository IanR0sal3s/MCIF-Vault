---
title: Autenticação de Mensagens (MAC, HMAC) e Assinaturas Digitais
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Segurança em Redes de Computadores
sigla_uc: SRC
capitulo: 2
bloco: 3
fonte_aula: aula_02_update.pdf (Slides 36–39, 46–49); aula02_leituras_resumo.pdf (Stallings Cap. 11–12)
tags:
  - src
  - criptografia
  - mac
  - hmac
  - assinatura-digital
aliases:
  - MAC
  - HMAC
  - Assinatura Digital
  - Autenticação de Mensagens
atualizado: 2026-11-15
---

# Autenticação de Mensagens (`MAC`, `HMAC`) e Assinaturas Digitais

A autenticação de mensagens garante ao recetor que a mensagem provém da origem alegada e não foi alterada em trânsito, recorrendo a esquemas combinados com *hash*, a **Códigos de Autenticação de Mensagem (`MAC` / `HMAC`)** ou a **assinaturas digitais**.

> [!TIP] Lógica de Funcionamento e Valor de Segurança
> * **Porque existe (Protocolos)**: Como funções de *hash* simples não possuem chave secreta, é necessário vincular um segredo partilhado (`MAC`/`HMAC` ou segredo $S$) ou uma chave privada (assinatura digital) ao cálculo do autenticador.
> * **Porque importa (Segurança)**: Permite autenticar mensagens de forma muito rápida com primitivas simétricas (`HMAC` sobre `SHA-256`) ou garantir **não-repúdio** perante terceiros com assinaturas digitais assimétricas.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Apenas autenticação (sem cifrar a mensagem)**: `M + H(M || S)` (partilha de segredo $S$) ou `M + C(K, M)` (`MAC`).
>   * **Confidencialidade + Autenticação com MAC**: `E(K2, [M || C(K1, M)])` ou `E(K2, M) + C(K1, E(K2, M))` (*Encrypt-then-MAC*), usando chaves distintas `K1` e `K2`.
>   * **`MAC` NÃO garante não-repúdio**: como `A` e `B` partilham a mesma chave secreta `K`, `B` também poderia gerar o mesmo `MAC`.

---

## 1. Esquemas de Autenticação Baseados em *Hash*

Nos slides 37–38 (e Stallings Fig. 11.3 / 12.1), distinguem-se quatro formas de autenticar uma mensagem com $H(M)$:

| Esquema | Expressão | Confidencialidade? | Mecanismo |
| :--- | :--- | :---: | :--- |
| **1. Cifrar mensagem e *hash*** | $E(K, [M \parallel H(M)])$ | **Sim** | Cifra simétrica sobre $M$ concatenada com $H(M)$ |
| **2. Cifrar apenas o *hash*** | $M \parallel E(K, H(M))$ | **Não** | $M$ segue em claro; apenas $H(M)$ é cifrado com $K$ |
| **3. Segredo partilhado $S$ sem cifragem** | $M \parallel H(M \parallel S)$ | **Não** | $A$ e $B$ partilham $S$; só quem conhece $S$ calcula $H(M \parallel S)$ |
| **4. Segredo $S$ + cifragem** | $E(K, [M \parallel H(M \parallel S)])$ | **Sim** | Combina proteção de segredo $S$ no *hash* e cifragem simétrica |

---

## 2. Assinatura Digital de Mensagens

* Semelhante à autenticação de mensagens, mas recorre a **criptografia assimétrica**:
  1. O emissor calcula o *hash* $H(M)$ e cifra-o com a sua **chave privada** ($E(PR_A, H(M))$).
  2. O recetor decifra o bloco assinado usando a **chave pública** do emissor ($PU_A$) e compara com o $H(M)$ recalculado localmente.
* **Propriedades**: Autenticidade da origem, integridade e **não-repúdio** (apenas $A$ possui $PR_A$).
* Para adicionar **confidencialidade**, cifra-se o conjunto (mensagem + assinatura) com uma chave simétrica de sessão ou com $PU_B$.

---

## 3. `MAC` (*Message Authentication Code*) e `HMAC` (`RFC 2104`)

* **`MAC`**: utiliza uma **chave secreta partilhada $K$** para gerar um *checksum* criptográfico de tamanho fixo anexado à mensagem:
  $$\text{MAC} = C(K, M)$$
* **`HMAC`** (*Keyed-Hash Message Authentication Code*, `RFC 2104`):
  * **Motivação**: funções de *hash* (`MD5`, `SHA`) são rápidas e amplamente disponíveis, mas não aceitam chave nativamente.
  * **Objetivos**: reutilizar funções de *hash* criptográficas **sem modificações** internas, integrando a chave secreta $K$ de forma segura e simples.
* **Outras funções MAC**: baseadas em cifras de blocos (ex.: modo *Cipher Block Chaining* — CBC-MAC).

---

## Perguntas de revisão

1. **Qual a principal vantagem do `HMAC` face a um `MAC` construído de raiz?**

> [!success]- Ver Resposta
> O `HMAC` (`RFC 2104`) permite reutilizar funções de *hash* já existentes, rápidas e testadas (como `SHA-256`) sem modificar o algoritmo de *hash* subjacente, bastando gerir a chave secreta partilhada.

2. **Porque é que uma assinatura digital oferece não-repúdio, ao contrário de um `HMAC`?**

> [!success]- Ver Resposta
> Porque no `HMAC` tanto o emissor como o recetor partilham a mesma chave secreta $K$ (qualquer um pode produzir a etiqueta), enquanto na assinatura digital apenas o emissor detém a chave privada $PR_A$ usada para assinar.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Funções de Hash Criptográficas e Integridade (MD5, SHA-1, SHA-2 e SHA-3)]] | `Comum/` · `mesmo bloco` |
| **Seguinte** | [[Assinaturas Digitais, PKI e GnuPG]] | `Comum/` · `muda para Bloco 04` |
| **Índice** | [[Capítulo 2 - Criptografia Aplicada]] · [[00 SRC]] | `Bloco 03` |

### Conceitos Relacionados

* [[Criptografia Assimétrica - Princípios, Diffie-Hellman, ECC e Algoritmo RSA]] · `Bloco 02`
* [[TBL 2 - Fundamentos de Criptografia]] · `Bloco 05`
