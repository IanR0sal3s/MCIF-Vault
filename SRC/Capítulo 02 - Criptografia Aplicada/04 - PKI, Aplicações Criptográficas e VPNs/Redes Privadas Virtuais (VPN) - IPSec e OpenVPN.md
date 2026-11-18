---
title: Redes Privadas Virtuais (VPN) - IPSec e OpenVPN
tipo: procedimento
mestrado: Cibersegurança e Informática Forense
uc: Segurança em Redes de Computadores
sigla_uc: SRC
capitulo: 2
bloco: 4
fonte_aula: aula_02_update.pdf (Slides 64–67)
tags:
  - src
  - vpn
  - ipsec
  - openvpn
  - tls
aliases:
  - VPN
  - IPSec
  - OpenVPN
atualizado: 2026-11-15
---

# Redes Privadas Virtuais (`VPN`) — `IPSec` e `OpenVPN`

As **VPNs** estendem redes privadas através de infraestruturas públicas (Internet) usando túneis cifrados e autenticados, destacando-se na UC duas abordagens complementares: **`IPSec`** e **`OpenVPN`**.

> [!TIP] Lógica de Funcionamento e Valor de Segurança
> * **Porque existe (Redes)**: Permite interligar filiais remotas de forma transparente (*site-to-site*) ou dar acesso seguro a utilizadores móveis (*road warriors*) sem expor serviços internos diretamente à Internet.
> * **Porque importa (Segurança)**: Garante confidencialidade, integridade e autenticação mútua (por certificados PKI e chaves pré-partilhadas `ta.key`) sobre redes não confiáveis.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **`IPSec`**: atua na **camada de rede** (ou encapsulamento rede/transporte), orientado à **interligação de redes remotas**.
>   * **`OpenVPN`**: enquadra-se na **camada de transporte** aplicando segurança via **`SSL/TLS`**, orientado ao **acesso remoto seguro por utilizadores (*road warriors*)** através de interfaces virtuais `tun`.

---

## 1. Comparação `IPSec` vs. `OpenVPN` (Slide 65)

| Característica | `IPSec` | `OpenVPN` |
| :--- | :--- | :--- |
| **Camada de atuação** | Camada de Rede (IP) | Camada de Transporte (TCP/UDP) com segurança via **`SSL/TLS`** |
| **Caso de uso típico** | Interligação de **redes remotas** através de túnel na Internet (*site-to-site*) | Acesso remoto seguro por **utilizadores (*road warriors*)** |
| **Gestão de confiança** | Chaves pré-partilhadas ou PKI (`IKE`) | PKI (`easy-rsa` / `OpenSSL`) + chave HMAC `ta.key` |

---

## 2. Configuração Base de `OpenVPN` (Slides 66–67)

**No Servidor:**

```bash
# 1. Instalar pacotes
sudo apt-get install openvpn easy-rsa

# 2. Inicializar a CA com easy-rsa
make-cadir ~/openvpn-ca
# Editar ~/openvpn-ca/vars
source vars
./clean-all
./build-ca

# 3. Gerar chaves do servidor, parâmetros Diffie-Hellman e ta.key
./build-key-server server
./build-dh
openvpn --genkey --secret keys/ta.key

# 4. Configurar /etc/openvpn/server.conf e regras de firewall (ufw)
# 5. Iniciar e validar serviço e interface virtual tun
sudo service openvpn start
tail /var/log/syslog
ifconfig   # verificar interface virtual tun
```

**Nos Clientes:**

```bash
# 1. Gerar certificado do cliente na CA
source vars
./build-key client1

# 2. Copiar exemplo /usr/share/doc/openvpn/examples/sample-config-files/client.conf
#    para /etc/openvpn e ajustar parâmetros do servidor
# 3. Iniciar serviço e validar interface tun ativa
sudo service openvpn start
tail /var/log/syslog
ifconfig
```

---

## Perguntas de revisão

1. **Qual a principal diferença arquitetural e de caso de uso entre `IPSec` e `OpenVPN` segundo os slides?**

> [!success]- Ver Resposta
> O `IPSec` opera ao nível da camada de rede para interligar redes remotas através de túneis na Internet, enquanto o `OpenVPN` opera na camada de transporte aplicando segurança via `SSL/TLS`, sendo particularmente vocacionado para acesso remoto de utilizadores (*road warriors*).

2. **Que interface de rede virtual é criada no sistema operativo após o arranque bem-sucedido do `OpenVPN` nos passos da aula?**

> [!success]- Ver Resposta
> É criada uma interface virtual **`tun`** (verificada com `ifconfig`), responsável por encaminhar o tráfego IP encapsulado pelo túnel TLS.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[SSH (Secure Shell), Port Forwarding e TLS 1.3]] | `mesmo bloco` |
| **Seguinte** | [[TBL 2 - Fundamentos de Criptografia]] | `muda para Bloco 05` |
| **Índice** | [[Capítulo 2 - Criptografia Aplicada]] · [[00 SRC]] | `Bloco 04` |

### Conceitos Relacionados

* [[Assinaturas Digitais, PKI e GnuPG]] · `Comum/`
