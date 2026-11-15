---
title: "Capítulo 5 - Enumeração"
uc: Cibersegurança Ofensiva e Defensiva I
sigla_uc: COD1
tipo: MOC
capitulo: 5
tags: [cod1, moc, enumeracao, netbios, smb, snmp, ldap, dns, smtp]
---
# Capítulo 5 - Enumeração

**Voltar a:** [[00 COD1]]

> [!ABSTRACT] Visão Geral do Capítulo
> Enquanto o scanning identifica portos abertos e versões de serviços, a **Enumeração** estabelece ligações ativas aos serviços descobertos e executa consultas diretas para extrair utilizadores, grupos, partilhas de rede, políticas de password, registos DNS completos e tabelas de rede.

## Estrutura do Capítulo

### 1. Conceitos, NetBIOS, SMB e LDAP
- [[Conceitos de Enumeração e Enumeração NetBIOS, SMB e LDAP]]
  - Conceito, informação enumerada e tabela de portos-chave (`53`, `135`, `137`, `139`, `445`, `161`, `162`, `389`, `3268`, `25`).
  - NetBIOS (nomes de 16 bytes, `nbtstat`, `nbtscan`, `nbstat`, `PsTools`, `net`/`net view`).
  - LDAP & SMB (`enum4linux`, `enum4linux-ng`, `ldapsearch`, `rpcclient`, `NetExec`/`nxc`, scripts NSE `smb-*`/`ldap-*`, `PowerView`).

### 2. Enumeração SNMP
- [[Enumeração SNMP (Community Strings, MIB e OIDs)]]
  - Arquitetura gestor/agente, community strings (`public` / `private`) e impacto de exposição.
  - MIB (*Management Information Base*), OIDs críticos (processos, software, utilizadores Windows, portos TCP) e ferramentas (`snmp-check`, `onesixtyone`, `snmpwalk`, scripts NSE `snmp-*`).

### 3. Enumeração SMTP, DNS, FTP, IPsec e VoIP
- [[Enumeração SMTP, DNS, FTP, IPsec e VoIP (SIP)]]
  - SMTP (`VRFY`, `EXPN`, `RCPT TO`, `smtp-user-enum`) e DNS Zone Transfer (`host -l`, `dig axfr`, `dnsrecon`, `dnsenum`, `dns-zone-transfer`).
  - FTP (acesso `anonymous`, scripts NSE), IPsec (`500/UDP`, `ISAKMP`, `ike-scan`), VoIP/SIP (`2000/2001/5050/5061`, `svmap`) e automação com `AutoRecon`.

### 4. Contramedidas e Metodologia Pentest
- [[Contramedidas de Enumeração e Metodologia Pentest]]
  - Hardening específico por protocolo (`SNMPv3`, `GPO`, Split-DNS, `SMTP`, `LDAPS`/`STARTTLS`, `RestrictNullSessAccess`).
  - Os 10 passos práticos de uma **Enumeração Pentest**.

### 5. Referência Rápida
- [[Cheat Sheet - Enumeração de Serviços e Portos]]

## Ligações Transversais
- **Anterior:** [[Capítulo 4 - Scanning de Redes]]
- **Seguinte:** [[Capítulo 6 - Análise de Vulnerabilidades]]
- **Playbook Prático:** [[Cheat Sheet - Playbook de Pentesting e Footprinting Organizacional]]
