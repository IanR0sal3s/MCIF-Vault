---
title: Criptografia Assimétrica - Princípios, Diffie-Hellman, ECC e Algoritmo RSA
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Segurança em Redes de Computadores
sigla_uc: SRC
capitulo: 2
bloco: 2
fonte_aula: aula_02_update.pdf (Slides 20–33); aula02_leituras_resumo.pdf (Stallings Cap. 9–10)
tags:
  - src
  - criptografia
  - criptografia-assimetrica
  - rsa
  - diffie-hellman
  - ecc
aliases:
  - Criptografia Assimétrica
  - Diffie-Hellman
  - RSA
  - Curvas Elípticas
atualizado: 2026-11-15
---

# Criptografia Assimétrica — Princípios, Diffie-Hellman, ECC e Algoritmo RSA

A criptografia assimétrica (ou de chave pública) utiliza pares de chaves matematicamente relacionados — uma **chave pública (`KU` / `PU`)** divulgada e uma **chave privada (`KR` / `PR`)** secreta — para resolver o problema da distribuição de chaves e viabilizar assinaturas digitais.

> [!TIP] Lógica de Funcionamento e Valor de Segurança
> * **Porque existe (Escala)**: Em criptografia simétrica, $n$ utilizadores exigem $Q_S = \frac{n(n-1)}{2}$ chaves secretas partilhadas; na assimétrica, bastam $Q_A = n$ pares de chaves, eliminando a dependência de um gestor central de chaves secretas.
> * **Porque importa (Segurança)**: Permite simultaneamente estabelecer segredos partilhados em canais inseguros (`Diffie-Hellman`), cifrar para confidencialidade (com a chave pública do destino) e assinar para autenticação/não-repúdio (com a chave privada da origem).
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Confidencialidade**: $Y = E(KU_B, X) \implies X = D(KR_B, Y)$ (cifra com pública do destino, decifra com privada do destino).
>   * **Autenticação (sem confidencialidade)**: $Y = E(KR_A, X) \implies X = D(KU_A, Y)$ (cifra com privada da origem; qualquer pessoa com $KU_A$ lê $X$).
>   * **Autenticação + Confidencialidade**: $Z = E(KU_B, E(KR_A, X)) \implies X = D(KU_A, D(KR_B, Z))$.
>   * **Curvas Elípticas (`ECC`)** oferecem a mesma segurança que `RSA` com **chaves mais curtas** e menor custo computacional (`ECDHE`, `ECDSA`, `ed25519`).

---

## 1. Acordo de Chaves `Diffie-Hellman` (1976)

Whitfield Diffie e Martin Hellman propuseram a troca segura de uma chave secreta sobre um canal público usando aritmética modular ($g$ gerador, $p$ primo grande):
1. $A$ escolhe aleatório privado $K$ e envia $X = g^K \bmod p$.
2. $B$ escolhe aleatório privado $K'$ e envia $Y = g^{K'} \bmod p$.
3. $A$ calcula $Z = Y^K \bmod p = g^{K \cdot K'} \bmod p$; $B$ calcula $Z' = X^{K'} \bmod p = g^{K \cdot K'} \bmod p$.
4. $Z = Z'$ é a chave secreta partilhada; um observador que conheça $g, p, X, Y$ enfrenta a dificuldade do **logaritmo discreto** para recuperar $K$ ou $K'$.

---

## 2. Modos de Utilização Assimétrica

| Objetivo | Operação no Emissor ($A$) | Operação no Recetor ($B$) | Propriedades Garantidas |
| :--- | :--- | :--- | :--- |
| **Confidencialidade** | $C = E(KU_B, M)$ | $M = D(KR_B, C)$ | Apenas $B$ decifra; não prova quem enviou |
| **Autenticação e Assinatura** | $C = E(KR_A, M)$ | $M = D(KU_A, C)$ | Autenticidade, integridade e não-repúdio; **sem confidencialidade** |
| **Autenticação + Confidencialidade** | $C = E(KU_B, E(KR_A, M))$ | $M = D(KU_A, D(KR_B, C))$ | Autenticidade + integridade + confidencialidade |

---

## 3. Algoritmo `RSA` (Rivest, Shamir, Adleman — 1978)

A segurança do `RSA` assenta na dificuldade computacional da **fatorização do produto de dois números primos grandes** ($n = p \cdot q$).

**Geração de Chaves:**
1. Escolher dois números primos inteiros grandes $p$ e $q$.
2. Calcular $n = p \cdot q$ e $\phi(n) = (p-1)(q-1)$.
3. Escolher $e$ tal que $1 < e < \phi(n)$ e $\gcd(\phi(n), e) = 1$.
4. Calcular $d$ tal que $d \cdot e \equiv 1 \pmod{\phi(n)}$ e $d < \phi(n)$.
5. **Chave Pública**: $PU = \{e, n\}$; **Chave Privada**: $PR = \{d, n\}$.

**Cifragem e Decifragem ($M < n$):**
* **Cifragem**: $C = M^e \bmod n$
* **Decifragem**: $M = C^d \bmod n = (M^e)^d \bmod n = M^{e \cdot d} \bmod n$

---

## 4. Criptografia de Curvas Elípticas (`ECC`)

* Grupo de algoritmos concorrente do `RSA`, matematicamente mais complexo;
* Atinge o **mesmo nível de segurança com chaves de menor tamanho**, exigindo menor poder computacional (adequado a ambientes com restrições de recursos e *handshakes* modernos);
* Exemplos referidos nos slides: **`ECDHE`** (*Elliptic Curve Diffie-Hellman Ephemeral*), **`ECDSA`** e **`ed25519`**.

---

## Perguntas de revisão

1. **Se $A$ enviar $Y = E(KR_A, X)$ para $B$, a mensagem $X$ está confidencial?**

> [!success]- Ver Resposta
> Não. A mensagem $X$ foi cifrada com a chave privada de $A$, pelo que qualquer entidade que possua a chave pública de $A$ ($KU_A$) consegue decifrar $Y$. A operação garante autenticação e integridade da origem, mas não confidencialidade.

2. **Em que problema matemático assenta a segurança do `RSA` face à do `Diffie-Hellman`?**

> [!success]- Ver Resposta
> O `RSA` baseia-se na dificuldade de fatorizar $n = p \cdot q$ (produto de dois primos grandes), enquanto o `Diffie-Hellman` clássico se baseia na dificuldade do problema do logaritmo discreto em aritmética modular.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Cifras de Blocos vs. Stream - Feistel, DES, 3DES, AES e RC4]] | `Bloco 01` |
| **Seguinte** | [[Funções de Hash Criptográficas e Integridade (MD5, SHA-1, SHA-2 e SHA-3)]] | `Comum/` · `muda para Bloco 03` |
| **Índice** | [[Capítulo 2 - Criptografia Aplicada]] · [[00 SRC]] | `Bloco 02` |

### Conceitos Relacionados

* [[Autenticação de Mensagens (MAC, HMAC) e Assinaturas Digitais]] · `Bloco 03`
* [[SSH (Secure Shell), Port Forwarding e TLS 1.3]] · `Bloco 04`
* [[TBL 2 - Fundamentos de Criptografia]] · `Bloco 05`
