---
title: "Capítulo 3 - Rastreamento e Reconhecimento"
uc: Cibersegurança Ofensiva e Defensiva I
sigla_uc: COD1
tipo: MOC
capitulo: 3
tags: [cod1, moc, footprinting, osint, reconhecimento]
---
# Capítulo 3 - Rastreamento e Reconhecimento

**Voltar a:** [[00 COD1]]

> [!ABSTRACT] Visão Geral do Capítulo
> O **Footprinting** (Rastreamento e Reconhecimento) é a primeira fase operacional de um pentest ou ataque. O objetivo é recolher o máximo de informação pública ou semi-pública sobre a rede, os sistemas e a organização alvo para desenhar o mapa da infraestrutura, reduzir áreas de foco e identificar vetores de entrada antes de qualquer interação intrusiva.

## Estrutura do Capítulo

### 1. Conceitos, Objetivos e Motores de Pesquisa
- [[Footprinting - Conceitos, Objetivos e Motores de Pesquisa (Google Hacking)]]
  - Definição, objetivos (rede, sistemas, organização) e postura de segurança.
  - Motores de pesquisa generalistas, `Netcraft`, `Shodan`, `Censys`, `Fullhunt`, `FOFA`, geolocalização e pesquisa de pessoas.
  - **Google Hacking** (operadores avançados, `GHDB`, `Pagodo`).

### 2. OSINT em Plataformas, Redes Sociais, Websites e E-mail
- [[OSINT - Plataformas (GitHub, Trello), Redes Sociais, Website e E-mail]]
  - Partilha de código e fugas de segredos (`GitHub` dorks, `gitleaks`, `gitrob`, `keyhacks`, `Trello`, `Pastebin`).
  - Redes sociais (comportamentos de utilizadores e organizações).
  - Website footprinting (headers HTTP, `Wappalyzer`, `BuiltWith`, crawlers, mirroring com `HTTrack`/`wget`, `archive.org`).
  - E-mail footprinting (cabeçalhos e tracking) e informação competitiva.

### 3. WHOIS, DNS, Rede e Engenharia Social
- [[WHOIS, DNS, Networking Footprinting e Engenharia Social]]
  - RIRs (`RIPE NCC`, `ARIN`, `APNIC`, `AFRINIC`, `LACNIC`) e consultas `WHOIS`.
  - Registos DNS (`A`, `AAAA`, `MX`, `NS`, `CNAME`, `SOA`, `PTR`, `TXT`, `AXFR`) e ferramentas (`dig`, `host`, `nslookup`, `dnsrecon`, `fierce`, `dnsdumpster`).
  - Networking footprinting (`traceroute`, descoberta de blocos IP, `wigle.net`) e Engenharia Social (eavesdropping, shoulder surfing, dumpster diving).
  - Suítes agregadoras (`Maltego`, `Recon-ng`, `AMASS`, `theHarvester`, `Spiderfoot`, `Sublist3r`, `FOCA`, `DIRB`, `Iky`).

### 4. Metodologia Prática de Footprinting Pentest e Contramedidas
- [[Footprinting Pentest e Contramedidas (Metodologia Prática)]]
  - Os 11 passos práticos de um *Footprinting Pentest* e estrutura completa do modelo de relatório.
  - Contramedidas técnicas e organizacionais contra recolha passiva/ativa.

## Ligações Transversais
- **Anterior:** [[Capítulo 2 - Preparação do Ambiente Laboratorial]]
- **Seguinte:** [[Capítulo 4 - Scanning de Redes]]
- **Playbook Prático:** [[Cheat Sheet - Playbook de Pentesting e Footprinting Organizacional]]
