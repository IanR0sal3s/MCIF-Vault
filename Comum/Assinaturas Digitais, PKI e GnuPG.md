---
title: Assinaturas Digitais, PKI e GnuPG
tipo: procedimento
mestrado: Cibersegurança e Informática Forense
sigla_uc: COMUM
ucs_relacionadas:
  - SRC
  - AFD1
  - ASSI
tags:
  - comum
  - criptografia
  - pki
  - x509
  - openssl
  - gnupg
  - assinatura-digital
  - ca
aliases:
  - PKI, Autoridades de Certificação (OpenSSL) e GnuPG
  - PKI
  - Autoridade de Certificação
  - OpenSSL CA
  - GnuPG
atualizado: 2026-11-18
---

# Assinaturas Digitais, PKI e GnuPG

A **Infraestrutura de Chave Pública (`PKI`)** e o ecossistema **`OpenPGP` / `GnuPG`** resolvem o problema da confiança na distribuição de chaves públicas e na verificação de **assinaturas digitais**, quer através de **Autoridades de Certificação (`CA`)** hierárquicas (`X.509`), quer através de troca e validação de *keyrings* entre pares.

> [!TIP] Lógica de Funcionamento e Valor Transversal
> * **Porque existe (Confiança e Não-Repúdio)**: Sem verificação de autenticidade da chave pública, um atacante pode substituir a chave divulgada (*Man-in-the-Middle*); certificados `X.509` assinados por uma `CA` ou chaves validadas via `GnuPG` vinculam uma identidade a uma chave pública.
> * **Porque importa (Operação / Forense / Sistemas)**: Permite autenticar servidores e utilizadores (`TLS`, `VPN`), assinar manifestos forenses com valor probatório em tribunal e validar a autenticidade de *firmware* e binários (`Secure Boot`, `sigcheck`).
> * **Pontos Críticos e Armadilhas para Exame**:
>   * Fluxo `OpenSSL` de emissão: gerar chave privada (`genrsa`) $\rightarrow$ criar pedido CSR (`req -new`) $\rightarrow$ assinar pela CA (`x509 -req` para a própria CA ou `ca -in ...` para utilizadores) $\rightarrow$ revogar quando comprometido (`ca -revoke`).
>   * No `GnuPG`, a falta de entropia durante a geração de chaves pode ser mitigada com `rngd -r /dev/urandom`.
>   * Compromisso da chave privada de topo (ex.: `PKfail`) ou expiração de certificados em produção (ex.: caso Equifax) quebram a cadeia de confiança.

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

## Aplicação por UC

### Em SRC (Infraestrutura de Chave Pública, TLS e VPNs)

* **Assinaturas Digitais e Autenticação de Canal**: As assinaturas digitais cifram o resumo criptográfico da mensagem com a chave privada do emissor (ou combinam-se em esquemas como `RSA`/`DSA`/`ECDSA`), sendo a `PKI` (`X.509`) o mecanismo que garante ao cliente que a chave pública pertence legitimamente ao servidor ou utilizador remoto.
* **Protocolos Dependentes**: Essencial no *handshake* de [[SSH (Secure Shell), Port Forwarding e TLS 1.3]], na autenticação mútua e emissão de certificados de [[Redes Privadas Virtuais (VPN) - IPSec e OpenVPN]] e nos fundamentos de [[Autenticação de Mensagens (MAC, HMAC) e Assinaturas Digitais]].

### Em AFD1 (Assinatura de Hashes de Aquisição e Valor Probatório)

* **Assinatura de Manifestos de Hashes**: Como um valor de *hash* isolado não depende de segredo, os peritos assinam digitalmente o manifesto de *hashes* (`SHA-256`) gerado na aquisição com **`GnuPG`**, recorrendo idealmente a *timestamping* ou a dispositivos físicos seguros como o **Cartão de Cidadão** português.
* **Valor Probatório em Tribunal**: Esta assinatura comprova não só a integridade dos dados recolhidos, mas também a **autenticidade do perito** e o **não-repúdio** da recolha na cadeia de custódia. Ver [[Armazenamento da Aquisição - Clonagem vs Imagem, Formatos, Aquisição Remota e Assinatura de Hashes]] e [[Preservação do Sistema e Integridade de Dados]].

### Em ASSI (Validação de Firmware, Código e Certificados)

* **Cadeia de Confiança no Arranque (`UEFI Secure Boot`)**: O arranque seguro valida cada módulo (`bootmgr.efi`, `winload.efi`, `ntoskrnl.exe`) através de uma hierarquia de certificados (`PK` — *Platform Key*, `KEK` — *Key Exchange Key*, `db` — base de assinaturas permitidas, e `dbx` — lista de revogação) ([[UEFI Secure Boot]]). A exposição da chave privada de topo compromete toda a cadeia, como aconteceu no caso [[PKfail - Vulnerabilidade do UEFI Secure Boot]].
* **Verificação de Código e Gestão de Ciclo de Vida**: Em resposta a incidentes e administração de sistemas, verifica-se a assinatura digital de executáveis e ferramentas com `sigcheck`, enquanto a gestão de ativos obriga a monitorizar prazos de validade de certificados para evitar falhas críticas de visibilidade e segurança (como o incidente da **Equifax** por certificado expirado). Ver [[Gestão de Ativos (Asset Management) e Políticas de Armazenamento Amovível (VeraCrypt)]].

---

## Perguntas de revisão

1. **Qual a diferença entre os ficheiros `.key`, `.csr` e `.crt` no fluxo `OpenSSL`?**

> [!success]- Ver Resposta
> `.key` contém a chave privada gerada (`genrsa`); `.csr` é o pedido de assinatura de certificado (*Certificate Signing Request*, gerado com `req -new`) que inclui a chave pública e identidade; `.crt` é o certificado final assinado pela CA.

2. **Para que serve o comando `openssl ca -revoke`?**

> [!success]- Ver Resposta
> Serve para revogar um certificado antes do seu termo de validade (por exemplo, em caso de compromisso da chave privada ou saída do utilizador), atualizando a base de dados da CA para inclusão na CRL.

3. **Porque é que em `AFD1` se assina o manifesto de *hashes* da aquisição com `GnuPG` / Cartão de Cidadão e *timestamping* em vez de guardar apenas o ficheiro `.sha256`?**

> [!success]- Ver Resposta
> Porque um *hash* isolado pode ser recalculado por quem tenha acesso de escrita ao manifesto. A assinatura digital vincula o resumo à chave privada do perito (idealmente num dispositivo físico seguro como o Cartão de Cidadão) e, com *timestamping*, prova autenticidade, momento da recolha e não-repúdio em tribunal.

4. **De que forma a hierarquia `PK`/`KEK`/`db`/`dbx` no `UEFI Secure Boot` (`ASSI`) aplica os mesmos princípios de `PKI` estudados em `SRC`?**

> [!success]- Ver Resposta
> Tal como numa `PKI` `X.509` onde uma `CA` raiz assina certificados de entidades e mantém uma lista de revogação (`CRL`), no `UEFI Secure Boot` a `PK` autoriza a `KEK`, que por sua vez assina atualizações da base de confiança (`db`) e da lista de revogação (`dbx`); se a chave privada de topo for exposta (`PKfail`), o atacante consegue assinar *bootkits* aceites pelo *firmware*.

---

## Notas relacionadas

- [[Criptografia Assimétrica - Princípios, Diffie-Hellman, ECC e Algoritmo RSA]]
- [[Autenticação de Mensagens (MAC, HMAC) e Assinaturas Digitais]]
- [[SSH (Secure Shell), Port Forwarding e TLS 1.3]]
- [[Redes Privadas Virtuais (VPN) - IPSec e OpenVPN]]
- [[Armazenamento da Aquisição - Clonagem vs Imagem, Formatos, Aquisição Remota e Assinatura de Hashes]]
- [[Preservação do Sistema e Integridade de Dados]]
- [[UEFI Secure Boot]]
- [[PKfail - Vulnerabilidade do UEFI Secure Boot]]
- [[Gestão de Ativos (Asset Management) e Políticas de Armazenamento Amovível (VeraCrypt)]]
