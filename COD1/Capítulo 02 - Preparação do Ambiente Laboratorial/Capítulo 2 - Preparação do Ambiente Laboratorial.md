---
title: "Capítulo 2 - Preparação do Ambiente Laboratorial"
uc: Cibersegurança Ofensiva e Defensiva I
sigla_uc: COD1
tipo: MOC
capitulo: 2
tags: [cod1, moc, ambiente-laboratorial, kali-linux, anonimizacao]
---
# Capítulo 2 - Preparação do Ambiente Laboratorial

**Voltar a:** [[00 COD1]]

> [!ABSTRACT] Visão Geral do Capítulo
> Antes de executar qualquer fase de footprinting, scanning ou enumeração, um pentester precisa de um laboratório isolado, reprodutível e operacionalmente seguro (OpSec). Este capítulo cobre a preparação de máquinas virtuais, distribuições especializadas (Linux e Windows) e mecanismos de anonimização de tráfego e identidade.

## Estrutura do Capítulo

### 1. Ambiente de Hacking e Virtualização
- [[Ambiente de Hacking - Kali Linux, Commando VM e Virtualização]]
  - Requisitos de hardware, virtualização (`VMware`, `VirtualBox`, `Hyper-V`) e contentores (`Docker`).
  - Distribuições Linux especializadas (`Kali Linux`, `Parrot OS`, `BackBox`, `SamuraiWTF`, `Wifislax`, `ArchStrike`, `NST`, `Attify OS`) e suítes Windows (`Commando-VM`, `Pentestbox`).
  - Ferramentas essenciais pré-instaladas e linguagens de scripting (`Python`, `Bash`, `PowerShell`).

### 2. Anonimização e Segurança Operacional (OpSec)
- [[Anonimização - MAC, Proxy, VPN, kali-anonsurf e Whonix]]
  - Spoofing de endereço MAC com `macchanger`.
  - Encaminhamento via Proxies, `ProxyChains`, `Tor` e VPNs.
  - `kali-anonsurf`, serviços de e-mail temporário/privado (`temp-mail`, `tuta.com`) e arquitetura de duas VMs do `Whonix`.

## Ligações Transversais
- **Anterior:** [[Capítulo 1 - Introdução à Cibersegurança]]
- **Seguinte:** [[Capítulo 3 - Rastreamento e Reconhecimento]]
- **Playbook Prático:** [[Cheat Sheet - Playbook de Pentesting e Footprinting Organizacional]]
