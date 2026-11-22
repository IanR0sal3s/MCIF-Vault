---
title: Cheat Sheet - Scanning de Redes e Nmap
tipo: cheatsheet
mestrado: Cibersegurança e Informática Forense
uc: Cibersegurança Ofensiva e Defensiva I
sigla_uc: COD1
capitulo: 4
tags: [cod1, cheatsheet, nmap, hping3, scanning]
aliases: [Cheat Sheet Nmap, Scanning Cheat Sheet]
atualizado: 2026-11-16
---
# Cheat Sheet - Scanning de Redes e Nmap

**Capítulo:** [[Capítulo 4 - Scanning de Redes]] | **UC:** [[00 COD1]]

> [!ABSTRACT] Referência Rápida Operacional
> Comandos essenciais de *Host Discovery*, *Port Scanning*, deteção de versões/SO, scripts `NSE`, evasão e comparação de resultados (`ndiff`) para uso direto durante auditorias e laboratório.

## 1. Host Discovery (Sem Port Scan: `-sn` / `-sP`)

```bash
# LAN local (ARP automático e mais fiável)
sudo nmap -sn -PR 192.168.1.0/24

# Ping Sweep ICMP clássico
sudo nmap -sn -PE 10.1.1.0/24

# Descoberta intensiva quando ICMP Echo está bloqueado
sudo nmap -sn -PE -PP -PS21,22,23,25,80,443,3389 -PA80,443 --source-port 53 -n -T4 -oG hosts_up.gnmap 10.1.1.0/24

# Extrair lista limpa de IPs ativos
awk '/Up$/{print $2}' hosts_up.gnmap > live_hosts.txt
```

## 2. Port Scanning TCP & UDP

```bash
# Scan padrão (SYN Stealth - requer root, top 1000 portos)
sudo nmap -sS -n -T4 -iL live_hosts.txt -oA scan_tcp_top1000

# Todos os 65535 portos TCP
sudo nmap -sS -Pn -n -p- -T4 <IP> -oA scan_tcp_full

# TCP Connect (quando não há privilégios root ou via ProxyChains)
nmap -sT -Pn -n <IP>

# UDP Scan nos portos mais relevantes (DNS, SNMP, NTP, TFTP, IKE)
sudo nmap -sU -Pn -n -p 53,67,68,69,123,161,162,500 <IP>
```

## 3. Deteção de Versões, SO, Banners e NSE

```bash
# Deteção de serviços (-sV), sistema operativo (-O) e scripts padrão (-sC)
sudo nmap -sS -sV -O -sC -T4 <IP> -oA scan_detalhado

# Banner grabbing rápido com NSE
sudo nmap -sV --script=banner <IP>

# Pesquisa e execução de scripts NSE
nmap --script-help "*http* and safe"
sudo nmap -p 80,443 --script http-title,http-headers <IP>
```

## 4. Análise de Firewall e Evasão a IDS

```bash
# Mapear firewall stateless vs stateful (ACK scan)
sudo nmap -sA -T4 <IP>

# FIN / NULL / Xmas scans (comparar com -sS e -sA)
sudo nmap -sF -T4 <IP>
sudo nmap -sN -T4 <IP>
sudo nmap -sX -T4 <IP>

# Evasão: fragmentação (-f), decoys (-D), porto origem 53 (-g 53) e scan lento (-T1)
sudo nmap -sS -f -D RND:10 -g 53 -T1 <IP>

# IDLE Scan anónimo via zombie
sudo nmap -Pn -p- -sI <IP_zombie> <IP_alvo>
```

## 5. Comparação e Ferramentas Complementares

```bash
# Comparar dois scans XML com ndiff
ndiff scan1.xml scan2.xml

# Banner grabbing manual com Netcat / Telnet
nc -nv <IP> 80
# Escrever: GET / HTTP/1.0 [Enter][Enter]

# Hping3, Netdiscover e Masscan
sudo hping3 <IP> --scan 80,443 -S
sudo netdiscover -r 192.168.1.0/24
sudo masscan -p80,443 10.1.1.0/24 --rate 1000 -e eth0
```
