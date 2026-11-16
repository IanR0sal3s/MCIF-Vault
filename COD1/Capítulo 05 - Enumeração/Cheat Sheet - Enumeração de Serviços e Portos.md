---
title: Cheat Sheet - Enumeração de Serviços e Portos
tipo: cheat-sheet
mestrado: Cibersegurança e Informática Forense
uc: Cibersegurança Ofensiva e Defensiva I
sigla_uc: COD1
capitulo: 5
tags: [cod1, cheat-sheet, enumeracao, smb, snmp, ldap, dns, smtp]
aliases: [Cheat Sheet Enumeração]
atualizado: 2026-11-16
---
# Cheat Sheet - Enumeração de Serviços e Portos

**Capítulo:** [[Capítulo 5 - Enumeração]] | **UC:** [[00 COD1]]

> [!ABSTRACT] Referência Rápida por Porto e Serviço
> Comandos prontos a copiar para enumerar rapidamente os serviços descobertos durante o scanning.

## 1. NetBIOS (`137/UDP`, `139/TCP`) & SMB (`445/TCP`)

```bash
# NetBIOS na sub-rede (Kali)
nbtscan -r 192.168.1.0/24
nmap -sV --script nbstat -v <IP>

# Enumeração completa SMB / AD
enum4linux -a <IP>
enum4linux-ng -A <IP>
nxc smb <IP> -u '' -p '' --shares --users
rpcclient -U "" -N <IP>   # querydominfo | enumdomusers | netshareenum | srvinfo

# Scripts Nmap NSE SMB
nmap -sS -p 445 <IP> --script smb-enum-users,smb-enum-groups,smb-enum-shares,smb-enum-domains
```

## 2. LDAP (`389/TCP`, `3268/TCP`)

```bash
# Descobrir Base DN (namingContexts) anonimamente
ldapsearch -x -H ldap://<IP> -s base
ldapsearch -x -H ldap://<IP> -b "" -s base namingContexts
nmap --script-help "ldap-*"
```

## 3. SNMP (`161/UDP`)

```bash
# Descobrir community strings e enumerar
onesixtyone <IP> public
snmp-check -c public -v 1 <IP>
snmpwalk -c public -v1 -t 10 <IP>
snmpwalk -c public -v2c <IP> 1.3.6.1.4.1.77.1.2.25   # Utilizadores Windows
sudo nmap -sU -p 161 <IP> --script="snmp*"
```

## 4. DNS (`53/TCP/UDP`) & SMTP (`25/TCP`)

```bash
# DNS Zone Transfer (AXFR)
host -t ns <dominio>
host -l <dominio> <DNS_server>
dig @<DNS_server> <dominio> axfr
dnsrecon -d <dominio> -t axfr
nmap --script=dns-zone-transfer -p 53 <DNS_server>

# SMTP User Enumeration
smtp-user-enum -M VRFY -D <dominio> -u <lista_users.txt> -t <IP>
telnet <IP> 25
```

## 5. FTP (`21/TCP`), IPsec (`500/UDP`) & VoIP/SIP (`5060/5061`)

```bash
# FTP (anonymous + scripts seguros)
sudo nmap -p 21 --script "*ftp* and safe" <IP>
ftp <IP>   # user: anonymous

# IPsec / IKE
sudo nmap -sU -p 500 <IP>
sudo ike-scan -M <IP>

# VoIP / SIP
svmap <IP>
```
