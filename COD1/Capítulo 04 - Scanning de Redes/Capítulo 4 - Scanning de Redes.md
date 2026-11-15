---
title: "Capítulo 4 - Scanning de Redes"
uc: Cibersegurança Ofensiva e Defensiva I
sigla_uc: COD1
tipo: MOC
capitulo: 4
tags: [cod1, moc, scanning, nmap, hping3]
---
# Capítulo 4 - Scanning de Redes

**Voltar a:** [[00 COD1]]

> [!ABSTRACT] Visão Geral do Capítulo
> Após mapear domínios e blocos de rede no [[Capítulo 3 - Rastreamento e Reconhecimento]], a fase de **Scanning** interage ativamente com os alvos para descobrir hosts ativos, portos abertos/filtrados, serviços em execução, sistemas operativos e regras de filtragem de firewalls/IDS.

## Estrutura do Capítulo

### 1. Conceitos, Flags TCP e Host Discovery
- [[Scanning de Redes - Conceitos, Flags TCP e Descoberta ICMP]]
  - Objetivos do scanning, construção de pacotes raw (`packETH`, `Ostinato`, `Hping`, `Scapy`, `Yersinia`) e desafios em redes IPv6.
  - Descoberta de hosts (`ICMP Echo`, `Ping Sweep`, `TCP SYN -PS`, `TCP ACK -PA`, `UDP -PU`, `ICMP Timestamp/Netmask -PP/-PM`, `ARP -PR`, `Protocol -PO`).

### 2. Técnicas de Port Scanning
- [[Técnicas de Port Scanning TCP, UDP e IDLE Scan]]
  - Estados de portos no `Nmap` (`open`, `closed`, `filtered`, `unfiltered`, `open|filtered`, `closed|filtered`).
  - `TCP Connect (-sT)`, `SYN Stealth (-sS)`, `NULL/FIN/Xmas (-sN/-sF/-sX)`, `ACK (-sA)`, `Window (-sW)`, `Maimon (-sM)`, `UDP (-sU)`, `IDLE Scan (-sI)` e `IP Protocol (-sO)`.

### 3. Nmap Avançado e Hping3
- [[Nmap Avançado e Hping3 - Descoberta, Port Scanning e Evasão]]
  - Temporização (`-T0` a `-T5`, `--max-rtt-timeout`, `--initial-rtt-timeout`), scripts NSE (`/usr/share/nmap/scripts`, `-sC`, `--script`), formatos de output (`-oN`, `-oX`, `-oG`, `-oA`) e comparação com `ndiff`.
  - Interseção de scans (`-sS` + `-sF` + `-sA`) para distinguir portos abertos de filtrados atrás de firewalls.
  - Sintaxe prática de `Hping3`, `Netcat`, `Netdiscover`, `Unicornscan`, `Masscan` e `JFScan`.

### 4. Evasão a IDS/Firewall, Banner Grabbing e Metodologia Pentest
- [[Evasão a IDS-Firewall, Banner Grabbing e Metodologia Pentest]]
  - Fragmentação (`-f`), decoys (`-D`), spoofing de IP/porto (`-S`, `--source-port`), temporização lenta (`-T0`/`-T1`) e `ProxyChains`.
  - Banner grabbing ativo (`telnet`, `nc`, `nmap -sV --script=banner`) e passivo (mensagens de erro, sniffing TTL, extensões web).
  - Contramedidas, passos do **Scanning Pentest** e recomendações defensivas.

### 5. Referência Rápida
- [[Cheat Sheet - Scanning de Redes e Nmap]]

## Ligações Transversais
- **Anterior:** [[Capítulo 3 - Rastreamento e Reconhecimento]]
- **Seguinte:** [[Capítulo 5 - Enumeração]]
- **Playbook Prático:** [[Cheat Sheet - Playbook de Pentesting e Footprinting Organizacional]]
