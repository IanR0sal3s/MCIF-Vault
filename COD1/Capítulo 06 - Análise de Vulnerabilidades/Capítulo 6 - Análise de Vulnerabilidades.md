---
title: "Capítulo 6 - Análise de Vulnerabilidades"
uc: Cibersegurança Ofensiva e Defensiva I
sigla_uc: COD1
tipo: MOC
capitulo: 6
tags: [cod1, moc, vulnerabilidades, cvss, cve, nessus, openvas]
---
# Capítulo 6 - Análise de Vulnerabilidades

**Voltar a:** [[00 COD1]]

> [!ABSTRACT] Visão Geral do Capítulo
> Depois de mapear a organização ([[Capítulo 3 - Rastreamento e Reconhecimento]]), descobrir hosts/portos/banners ([[Capítulo 4 - Scanning de Redes]]) e enumerar utilizadores/serviços ([[Capítulo 5 - Enumeração]]), a **Análise de Vulnerabilidades** identifica, classifica e prioriza falhas de configuração, software desatualizado e vulnerabilidades conhecidas antes da fase de exploração ou remediação.

## Estrutura do Capítulo

### 1. Conceitos, Classificação e Ciclo de Vida
- [[Análise e Gestão de Vulnerabilidades - Ciclo de Vida e Classificação]]
  - Conceito, utilidade para sysadmins e as 9 categorias de vulnerabilidades.
  - Tipos de avaliação (ativa/passiva, externa/interna, host/rede, aplicacional/wireless).
  - Ciclo de vida completo: Pré-avaliação (*baseline*), Avaliação e Pós-avaliação (risco, remediação, verificação e monitorização `SIEM`/`SOAR`).

### 2. Sistemas de Pontuação (`CVSS` / `CVE`) e Abordagens
- [[Sistemas de Pontuação (CVSS e CVE) e Abordagens de Avaliação]]
  - Abordagens `product-based` vs. `service-based`; avaliação baseada em árvore vs. dedução; tipos de ferramentas e critérios de seleção.
  - `CVSS v4.0` e `CVE` (Mitre, EUVD-ENISA, NVD-NIST, CVEdetails, MSRC).

### 3. Ferramentas: Nessus, OpenVAS, Nikto e Nmap NSE
- [[Ferramentas de Análise - Nessus e OpenVAS (Instalação e Setup)]]
  - Scanners de rede (`Nessus`, `OpenVAS`, `Nexpose`, `Qualys`, `GFI LanGuard`, `SAINT`, `beSECURE/Fortra`).
  - Scanners web (`Nikto`, `Burp Suite`/`Dastardly`, `Acunetix`, `Vega`, `Uniscan`/`RapidScan`) e scripts NSE (`vulners`, `vulscan`, `vuln`/`exploit`).
  - Guias práticos de instalação e troubleshooting para **Nessus** (`8834`) e **OpenVAS / GVM** (`9392`, PostgreSQL 14->15, `greenbone-feed-sync`).
  - Papel dos relatórios de análise de vulnerabilidades.

## Ligações Transversais
- **Anterior:** [[Capítulo 5 - Enumeração]]
- **Playbook Prático:** [[Cheat Sheet - Playbook de Pentesting e Footprinting Organizacional]]
