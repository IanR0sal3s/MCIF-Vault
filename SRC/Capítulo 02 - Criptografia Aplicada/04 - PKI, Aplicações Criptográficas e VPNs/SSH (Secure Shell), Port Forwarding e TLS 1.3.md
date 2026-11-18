---
title: SSH (Secure Shell), Port Forwarding e TLS 1.3
tipo: procedimento
mestrado: Cibersegurança e Informática Forense
uc: Segurança em Redes de Computadores
sigla_uc: SRC
capitulo: 2
bloco: 4
fonte_aula: aula_02_update.pdf (Slides 58–63); 2_crypto_projectKickoff.pdf (Slides 2–4)
tags:
  - src
  - ssh
  - port-forwarding
  - tls
  - criptografia
aliases:
  - SSH
  - Secure Shell
  - SSH Port Forwarding
  - TLS 1.3
atualizado: 2026-11-15
---

# `SSH` (*Secure Shell*), *Port Forwarding* e `TLS 1.3`

O **`SSH`** é um protocolo de comunicação segura (não é uma *shell*) que garante **autenticação, confidencialidade e integridade**, combinando cifragem assimétrica na negociação/autenticação com cifragem simétrica na sessão; de forma análoga, o **`TLS 1.3`** combina três algoritmos distintos para proteger ligações Web.

> [!TIP] Lógica de Funcionamento e Valor de Segurança
> * **Porque existe (Hibridismo)**: A criptografia assimétrica é computacionalmente pesada para grandes volumes de dados; tanto o `SSH` como o `TLS` usam criptografia assimétrica para autenticar e acordar chaves, e cifragem simétrica (`AES` / `AES-GCM`) para cifrar o tráfego da sessão.
> * **Porque importa (Segurança)**: O `SSH` permite substituir autenticação por password por pares de chaves (`ssh-keygen`) e criar túneis TCP cifrados (`-L` local, `-R` remoto); no `TLS`, desativar a validação de certificados para restaurar disponibilidade abre a porta a ataques *Man-in-the-Middle*.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Túnel Local (`ssh -L`)**: abre um porto na máquina **local** (cliente) que encaminha através do servidor SSH até um serviço remoto.
>   * **Túnel Remoto (`ssh -R`)**: abre um porto no **servidor SSH** remoto que encaminha de volta através do cliente até um serviço destino.
>   * **Desativar validação de certificado TLS**: a ligação continua **cifrada**, mas perde a **autenticação do servidor**, permitindo interceção ativa (MITM).

---

## 1. Arquitetura e Utilização do `SSH` (Slides 58–60)

* **Ficheiros de configuração em Linux**: `/etc/ssh/sshd_config` (servidor) e `/etc/ssh/ssh_config` (cliente). Ferramentas Windows referidas: `PuTTY` (`plink`) e `WinSCP`.
* **Fases da ligação SSH (Slide 60):**
  1. **Negociar sessão cifrada**: troca de chaves públicas (números primos grandes) para estabelecer chave simétrica (**`AES`**) que cifra a sessão;
  2. **Autenticação**: dentro da sessão já cifrada, o cliente autentica-se por *password* (não recomendado) ou por **pares de chaves SSH** (recomendado).

```bash
# Acesso básico e execução remota
ssh user@10.1.1.1
ssh user@10.1.1.1 ls

# Cópia segura de ficheiros e montagem remota
scp user@10.1.1.1:fich.txt .
sshfs usr@10.1.1.1/local /remoto

# Autenticação por chaves públicas e agente (sem password)
ssh-keygen
ssh-copy-id user@x.y.z.w
ssh-agent
ssh-add .ssh/id_rsa
```

---

## 2. *SSH Port Forwarding* (Slides 61–63)

Pré-requisitos para encaminhamento de portos:
1. O serviço a reencaminhar tem de usar **TCP** e apenas um porto;
2. O servidor deve ter serviço SSH ativo com autenticação válida;
3. Criar o túnel SSH definindo o porto de redirecionamento;
4. Configurar o cliente aplicacional para ligar ao porto do túnel.

| Modo | Sintaxe (Slides 62–63) | Direção do Túnel |
| :--- | :--- | :--- |
| **Túnel Local (`-L`)** | `ssh -L 3000:www.dei.estg.ipleiria.pt:80 user@10.1.1.2`<br/>Cliente liga a `localhost:3000` | Cliente (`3000`) $\rightarrow$ Servidor SSH (`10.1.1.2:22`) $\rightarrow$ Destino (`:80`) |
| **Túnel Remoto (`-R`)** | `ssh -R 5000:www.google.com:80 user@10.1.1.2`<br/>Ligação a `localhost:5000` no servidor | Servidor SSH (`5000`) $\rightarrow$ Cliente SSH $\rightarrow$ Destino (`:80`) |

---

## 3. `TLS 1.3` e Validação de Certificados (*Project Kickoff*, Slides 2–4)

Na análise de uma ligação `TLS 1.3` válida (`www.ipleiria.pt`), surgem **3 algoritmos criptográficos distintos**:
* **`RSA 2048 bits`**: autenticação da identidade do servidor através de certificado/assinatura digital;
* **`X25519` (*Server Temp Key*)**: acordo de chaves efémero (*Elliptic Curve Diffie-Hellman*) garantindo sigilo futuro (*Forward Secrecy*);
* **`AES-GCM 128 bits`**: cifragem simétrica autenticada dos dados da sessão (confidencialidade + integridade).

> [!WARNING] Segurança vs. Disponibilidade (Slide 4 do Kickoff)
> Se um serviço crítico falhar por erro de validação de certificado TLS e um programador propuser *"desativar a verificação do certificado"*, a ligação continuará **cifrada**, mas qualquer atacante em posição MITM pode apresentar um certificado falso e ler/modificar todo o tráfego.

---

## Perguntas de revisão

1. **Porque é que o `TLS 1.3` utiliza simultaneamente `RSA 2048`, `X25519` e `AES-GCM 128` em vez de usar apenas `RSA`?**

> [!success]- Ver Resposta
> O `RSA` autentica o servidor (assinatura do certificado), o `X25519` realiza a troca efémera de chaves de sessão (eficiente e com *forward secrecy*) e o `AES-GCM` cifra e autentica os dados da sessão em massa a alta velocidade, o que seria impraticável diretamente com `RSA`.

2. **Qual a diferença prática entre `ssh -L` e `ssh -R`?**

> [!success]- Ver Resposta
> `ssh -L` (*Local Port Forwarding*) escuta num porto da máquina cliente e encaminha ligações através do servidor SSH para um serviço remoto; `ssh -R` (*Remote Port Forwarding*) escuta num porto do servidor SSH remoto e encaminha ligações de volta através do cliente SSH para um destino acessível a partir do cliente.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Assinaturas Digitais, PKI e GnuPG]] | `Comum/` · `mesmo bloco` |
| **Seguinte** | [[Redes Privadas Virtuais (VPN) - IPSec e OpenVPN]] | `mesmo bloco` |
| **Índice** | [[Capítulo 2 - Criptografia Aplicada]] · [[00 SRC]] | `Bloco 04` |

### Conceitos Relacionados

* [[Criptografia Assimétrica - Princípios, Diffie-Hellman, ECC e Algoritmo RSA]] · `Bloco 02`
