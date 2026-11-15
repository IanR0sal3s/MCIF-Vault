---
title: PKI, Autoridades de Certificação (OpenSSL) e GnuPG
tipo: procedimento
mestrado: Cibersegurança e Informática Forense
uc: Segurança em Redes de Computadores
sigla_uc: SRC
capitulo: 2
bloco: 4
fonte_aula: aula_02_update.pdf (Slides 50–57)
tags:
  - src
  - pki
  - x509
  - openssl
  - gnupg
  - ca
aliases:
  - PKI
  - Autoridade de Certificação
  - OpenSSL CA
  - GnuPG
atualizado: 2026-11-15
---

# PKI, Autoridades de Certificação (`OpenSSL`) e `GnuPG`

A **Infraestrutura de Chave Pública (`PKI`)** e o ecossistema **`OpenPGP` / `GnuPG`** resolvem o problema da confiança na distribuição de chaves públicas, quer através de **Autoridades de Certificação (`CA`)** hierárquicas (`X.509`), quer através de troca e validação de *keyrings* entre pares.

> [!TIP] Lógica de Funcionamento e Valor de Segurança
> * **Porque existe (Confiança)**: Sem verificação de autenticidade da chave pública, um atacante pode substituir a chave divulgada (*Man-in-the-Middle*); certificados `X.509` assinados por uma `CA` vinculam uma identidade a uma chave pública.
> * **Porque importa (Operação)**: Os administradores usam `openssl` para operar CAs internas (TLS, VPNs) e emitir/revogar certificados, enquanto `gpg` protege mensagens e ficheiros fim-a-fim.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * Fluxo `OpenSSL` de emissão: gerar chave privada (`genrsa`) $\rightarrow$ criar pedido CSR (`req -new`) $\rightarrow$ assinar pela CA (`x509 -req` para a própria CA ou `ca -in ...` para utilizadores) $\rightarrow$ revogar quando comprometido (`ca -revoke`).
>   * No `GnuPG`, a falta de entropia durante a geração de chaves pode ser mitigada com `rngd -r /dev/urandom`.

---

## 1. Gestão e Distribuição de Chaves Públicas (`X.509` / `PKI`)

Os slides distinguem a evolução da distribuição de chaves públicas:
1. Publicação não controlada (vulnerável a falsificação);
2. Centralização de chaves públicas / Entidade de confiança;
3. **Uso de Certificados Digitais (`Framework X.509` / `PKI`)** emitidos por uma **Autoridade de Certificação (`CA`)**, evitando consultas constantes em tempo real a um diretório público.

**Aplicações principais:** autenticação de serviços `SSL/TLS` e autenticação de utilizadores (ex.: `VPN`).

---

## 2. Instalação e Operação de uma CA Privada com `OpenSSL` (Slides 56–57)

Diretoria padrão em Linux: `/etc/ssl` (`sudo apt-get install openssl`).

```bash
# 1. Inicializar a CA: gerar par de chaves da CA (protegido com 3DES)
openssl genrsa -des3 -out cakey.pem

# 2. Criar pedido de certificado da própria CA
openssl req -new -key cakey.pem -out ca.crt

# 3. Auto-assinar o certificado raiz da CA (validade 3650 dias)
openssl x509 -req -days 3650 -in ca.crt -out cacert.pem -signkey cakey.pem
```

**Emissão, inspeção e revogação de certificado de utilizador/serviço (ex.: `mantunes`):**

```bash
# 4. Gerar chave privada do utilizador
openssl genrsa -des3 -out mantunes.key

# 5. Gerar Certificate Signing Request (CSR)
openssl req -new -key mantunes.key -out mantunes.csr

# 6. Assinar o CSR com a CA privada
openssl ca -in mantunes.csr -cert cacert.pem -keyfile cakey.pem -out mantunes.crt

# 7. Visualizar detalhes do certificado emitido
openssl x509 -in mantunes.crt -text

# 8. Revogar o certificado do utilizador
openssl ca -revoke mantunes.crt -keyfile cakey.pem -cert cacert.pem
```

---

## 3. `GnuPG` (*The GNU Privacy Guard* / `OpenPGP`, `RFC 4880`)

* Implementação aberta do padrão `OpenPGP` (`RFC 4880`, Nov 2007) para cifragem e assinatura de ficheiros/email usando `RSA` ou `DSA`.
* Instalação e geração de entropia em Linux:

```bash
sudo apt-get install gnupg rng-tools
cd ~/.gnupg
rngd -r /dev/urandom
```

| Operação `gpg` | Parâmetro / Comando |
| :--- | :--- |
| Gerar par de chaves | `gpg --gen-key` |
| Listar chaves no *keyring* | `gpg --list-public-keys` / `gpg --list-secret-keys` |
| Importar chave pública externa | `gpg --import <ficheiro>` |
| Exportar chave pública em ASCII | `gpg --export -a` |

---

## Perguntas de revisão

1. **Qual a diferença entre os ficheiros `.key`, `.csr` e `.crt` no fluxo `OpenSSL`?**

> [!success]- Ver Resposta
> `.key` contém a chave privada gerada (`genrsa`); `.csr` é o pedido de assinatura de certificado (*Certificate Signing Request*, gerado com `req -new`) que inclui a chave pública e identidade; `.crt` é o certificado final assinado pela CA.

2. **Para que serve o comando `openssl ca -revoke`?**

> [!success]- Ver Resposta
> Serve para revogar um certificado antes do seu termo de validade (por exemplo, em caso de compromisso da chave privada ou saída do utilizador), atualizando a base de dados da CA para inclusão na CRL.

## Notas relacionadas

- [[Criptografia Assimétrica - Princípios, Diffie-Hellman, ECC e Algoritmo RSA]]
- [[SSH (Secure Shell), Port Forwarding e TLS 1.3]]
- [[Redes Privadas Virtuais (VPN) - IPSec e OpenVPN]]
