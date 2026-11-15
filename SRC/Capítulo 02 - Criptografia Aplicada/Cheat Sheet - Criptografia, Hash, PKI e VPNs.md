---
title: Cheat Sheet - Criptografia, Hash, PKI e VPNs
tipo: cheatsheet
mestrado: Cibersegurança e Informática Forense
uc: Segurança em Redes de Computadores
sigla_uc: SRC
capitulo: 2
fonte_aula: aula_02_update.pdf; 2_crypto_projectKickoff.pdf; TBL_Cryptography_EN_202627.pdf
tags:
  - cheatsheet
  - src
  - criptografia
  - openssl
  - ssh
  - vpn
aliases:
  - Cheat Sheet Capítulo 2 SRC
  - Cheat Sheet Criptografia SRC
atualizado: 2026-11-15
---

# Cheat Sheet — Criptografia, Hash, PKI e VPNs

Guia de consulta rápida do **[[Capítulo 2 - Criptografia Aplicada]]** de [[00 SRC|SRC]].

---

## 1. Simétrica vs. Assimétrica e Notação

| Conceito | Regra / Fórmula | Armadilha Comum |
| :--- | :--- | :--- |
| **Chaves em $n$ utilizadores** | Simétrica: $\frac{n(n-1)}{2}$ \| Assimétrica: $n$ pares | Assimétrica **não substitui** simétrica; complementa-a (acordo de chaves + assinaturas) |
| **Stream vs. Blocos** | Stream: bit/byte (`RC4`, Vernam) \| Blocos: `Feistel`, `DES`, `AES`, `RC5` | **`RC4` é cifra *stream*** (não é de blocos) |
| **`DES`** | Bloco `64` bits, chave `56` bits efetivos, `16` *rounds* | $2^{56}$ chaves é quebrável por força bruta $\rightarrow$ `3DES` / `AES` (`256` bits) |
| **Confidencialidade** | $Y = E(PU_B, X) \implies X = D(PR_B, Y)$ | Só $B$ lê; não prova origem |
| **Autenticação (sem sigilo)** | $Y = E(PR_A, X) \implies X = D(PU_A, Y)$ | Todos com $PU_A$ leem $X$ |
| **Autenticação + Sigilo** | $Z = E(PU_B, E(PR_A, X))$ | Ordem inversa na decifragem: $D(PU_A, D(PR_B, Z))$ |
| **`RSA`** | $n = p \cdot q$, $\phi(n)=(p-1)(q-1)$, $d \cdot e \equiv 1 \pmod{\phi(n)}$ | $C = M^e \bmod n$; $M = C^d \bmod n$ ($M < n$) |
| **`TLS 1.3`** | `RSA 2048` (auth) + `X25519` (troca chaves) + `AES-GCM 128` (dados) | Desativar validação de certificado mantém cifragem mas abre porta a MITM |

---

## 2. Hash, `MAC` e `HMAC`

| Primitiva | Entrada $\rightarrow$ Saída | Chave? | Não-Repúdio? | Comandos / Notas |
| :--- | :--- | :---: | :---: | :--- |
| **`MD5`** | Variável $\rightarrow$ `128` bits (blocos `512`) | Não | Não | `md5sum ficheiro` / `md5sum -c` (`RFC 1321`) |
| **`SHA-1`** | Variável $\rightarrow$ `160` bits (blocos `512`) | Não | Não | `sha1sum ficheiro` (`FIPS 180` / `RFC 6234`) |
| **`SHA-2` / `SHA-3`** | Variável $\rightarrow$ `224`–`512` bits | Não | Não | `sha256sum`; `SHA-512` usa blocos `1024` bits, `80` *rounds* |
| **`MAC` / `HMAC`** | $\text{MAC} = C(K, M)$ | **Sim ($K$)** | **Não** | `HMAC` (`RFC 2104`) reutiliza `MD5`/`SHA` sem alterar o algoritmo |
| **Assinatura Digital** | $E(PR_A, H(M))$ | **Sim ($PR_A$)** | **Sim** | Verificada com $PU_A$ |

---

## 3. Comandos Essenciais (`OpenSSL`, `GnuPG`, `SSH`, `OpenVPN`)

```bash
# --- OpenSSL CA Privada ---
openssl genrsa -des3 -out cakey.pem
openssl req -new -key cakey.pem -out ca.crt
openssl x509 -req -days 3650 -in ca.crt -out cacert.pem -signkey cakey.pem
openssl ca -in user.csr -cert cacert.pem -keyfile cakey.pem -out user.crt
openssl ca -revoke user.crt -keyfile cakey.pem -cert cacert.pem

# --- GnuPG ---
gpg --gen-key | gpg --list-public-keys | gpg --import <pub> | gpg --export -a

# --- SSH e Port Forwarding ---
ssh-keygen && ssh-copy-id user@host
ssh -L 3000:destino_interno:80 user@ssh_server   # Túnel Local (cliente:3000 -> remoto:80)
ssh -R 5000:destino:80 user@ssh_server           # Túnel Remoto (servidor:5000 -> cliente -> destino:80)
```

* **`IPSec`** (camada de rede, interligação de redes remotas) vs. **`OpenVPN`** (camada de transporte sobre `SSL/TLS`, *road warriors*, interface `tun`).

---

## Navegação

- [[Capítulo 2 - Criptografia Aplicada|Voltar ao MOC do Capítulo 2]]
- [[00 SRC|Voltar ao MOC Geral de SRC]]
