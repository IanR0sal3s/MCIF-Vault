---
title: WHOIS, DNS, Networking Footprinting e Engenharia Social
tipo: tecnica
mestrado: Cibersegurança e Informática Forense
uc: Cibersegurança Ofensiva e Defensiva I
sigla_uc: COD1
capitulo: 3
bloco: 3
fonte_aula: 2026.27_MCIF_COD1_03_Reconhecimento_Footprinting.pdf (Slides 41–53)
tags: [cod1, whois, dns, traceroute, engenharia-social, maltego, amass, recon-ng]
aliases: [WHOIS Footprinting, DNS Footprinting, Networking Footprinting]
criado: 2026-11-15
atualizado: 2026-11-16
---

# WHOIS, DNS, Networking Footprinting e Engenharia Social

O reconhecimento técnico de infraestrutura combina consultas `WHOIS` (RIRs), registos `DNS`, mapeamento de caminho (`traceroute`), engenharia social e suítes agregadoras (`Maltego`, `Amass`, `theHarvester`, `Recon-ng`).

> [!TIP] Lógica de Funcionamento e Valor Operacional
> * **Porque existe (Sistema)**: O registo público de blocos IP/domínios nos RIRs e a resolução DNS são necessários para o encaminhamento global na Internet.
> * **Porque importa (Pentesting / Segurança)**: Traduz nomes comerciais em blocos CIDR reais, servidores de correio (`MX`), registos `TXT` (SaaS/SPF) e topologia de firewalls intermédias antes do scanning.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * Os 5 RIRs são **`RIPE NCC`**, **`ARIN`**, **`APNIC`**, **`AFRINIC`** e **`LACNIC`**.
>   * `traceroute -T` (TCP SYN) atravessa firewalls que bloqueiam `traceroute -I` (ICMP).
>   * Transferência de zona `AXFR` mal restringida expõe todos os registos da zona DNS.

## 1. WHOIS Footprinting e Regional Internet Registries (RIR)

As bases de dados **WHOIS** são mantidas pelos **5 RIRs** mundiais e guardam informações sobre proprietários de domínios e atribuições de blocos IP/AS:

1. **RIPE NCC** — Europa, Médio Oriente e partes da Ásia Central (`ripe.net`)
2. **ARIN** — América do Norte
3. **APNIC** — Ásia-Pacífico
4. **AFRINIC** — África
5. **LACNIC** — América Latina e Caraíbas

**Dados obtidos via WHOIS:** Nome do domínio, contactos e detalhes do proprietário/entidade, servidores de nomes (`NS`), intervalo de endereços IP (*IP Range*), e datas de criação/atualização/expiração (úteis inclusive para engenharia social direcionada).

- **Soluções Web e CLI:** `lookup.icann.org`, `centralops.net`, `research.domaintools.com`, `dns.pt/pt/ferramentas/whois`, `viewdns.info`, `whois.com` e comando `whois <dominio|IP>`.

## 2. DNS Footprinting

As consultas DNS revelam servidores expostos, serviços de e-mail, subdomínios, registos de validação cloud e, em configurações inseguras, a zona inteira (`AXFR`).

| Registo DNS | Significado / Utilidade no Reconhecimento |
| :--- | :--- |
| **`A` / `AAAA`** | Mapeia hostname para endereço IPv4 / IPv6. |
| **`MX`** | Servidores de correio eletrónico (*Mail Exchange*). |
| **`NS`** | Servidores de nomes autoritativos para o domínio. |
| **`CNAME`** | Alias (*Canonical Name*) apontando para outro domínio/serviço (ex.: SaaS/CDN). |
| **`SOA`** | *Start of Authority* (servidor primário, contacto administrativo, timers da zona). |
| **`PTR`** | Resolução inversa (IP para hostname). |
| **`TXT`** | Texto arbitrário; expõe registos `SPF`, `DMARC`, verificações de domínio (Microsoft 365, Google, Atlassian, etc.). |
| **`AXFR`** | Pedido de transferência de zona DNS completa (se permitido a IPs não autorizados, expõe toda a zona). |

- **Ferramentas Web:** `dnsdumpster.com`, `securitytrails.com`, `centralops.net`, `viewdns.info`, `dnsinspect.com`, `mydnstools.info`, `netlas.io`, `digwebinterface.com`, `robtex.com`, `network-tools.com`.
- **Ferramentas CLI:**
  ```bash
  host <dominio>
  nslookup -type=mx <dominio>
  dig @<servidor_dns> <dominio> -t AXFR
  fierce -dns <dominio>
  dnsrecon -d <dominio>
  ```

## 3. Networking Footprinting e Engenharia Social

- **Descoberta do Network Range:** Através da base de dados `WHOIS` da `RIPE` (ou RIR correspondente) identifica-se o bloco CIDR e o Sistema Autónomo (`AS`) da organização.
- **Mapeamento de Caminho (`Traceroute`):** Utiliza mensagens ICMP e incremento progressivo de `TTL` para descobrir routers, firewalls e saltos intermédios até ao alvo:
  ```bash
  traceroute -I <alvo>   # Usando ICMP Echo
  traceroute -T <alvo>   # Usando TCP SYN (útil para atravessar firewalls)
  ```
  Alternativas visuais/Windows: `tracert`, `traceroute-online.com`, `Path Analyzer`, `VisualRoute`.
- **Redes Wi-Fi:** `wigle.net` indexa localizações geográficas de redes sem fios (SSID/BSSID).
- **Engenharia Social no Footprinting:** Explora comportamentos humanos para obter credenciais, IPs, versões de software, layout de rede ou dados financeiros, através de técnicas como:
  - **Eavesdropping (Espionagem):** Escuta ou interceção não autorizada de conversas/comunicações.
  - **Shoulder surfing:** Observação direta e discreta de ecrãs ou teclados para captar usernames e passwords.
  - **Dumpster Diving:** Procura de informação crítica no lixo físico (post-its, impressões descartadas, documentos da sala de impressão).

## 4. Ferramentas Integradas de Footprinting

- **Suites gerais / OSINT:** `Maltego` (grafo visual de relações), `Recon-ng` (framework modular estilo Metasploit), `AMASS` (mapeamento de superfície de ataque e subdomínios), `theHarvester` (e-mails, subdomínios, hosts), `Spiderfoot` (automação OSINT geral por domínio).
- **Especializadas:** `Sublist3r` (enumeração de subdomínios), `DIRB` (força bruta de diretórios web), `Iky` (OSINT por e-mail), `FOCA` (extração de metadados de documentos web).

## Além da aula

> [!NOTE] Conteúdo Complementar (Além da aula)
> Fluxo prático para correlacionar `WHOIS`, `ASN` e `DNS` numa auditoria organizacional:

1. Identificar o **ASN** da organização via `whois -h whois.radb.net <IP>` ou `bgp.he.net`.
2. Listar todos os prefixos IP anunciados por esse ASN — frequentemente revela gamas de IP secundárias ou de filiais que não estão associadas ao domínio principal.
3. Analisar registos `TXT` (`dig +short TXT alvo.pt`) para mapear rapidamente os fornecedores SaaS da empresa (`v=spf1`, `google-site-verification`, `MS=`, `atlassian-domain-verification`), o que orienta tanto a análise de superfície externa como cenários de phishing autorizado.

## Perguntas de revisão

1. **Qual a diferença entre o comando `traceroute -I` e `traceroute -T` durante o *networking footprinting*?**
   > [!success]- Ver Resposta
   > `traceroute -I` envia sondas ICMP Echo Request, que são frequentemente bloqueadas por firewalls de perímetro; `traceroute -T` envia pacotes TCP SYN, aumentando a probabilidade de atravessar firewalls até ao porto do serviço alvo (ex.: 80 ou 443).

2. **Que informação crítica revela um registo DNS `TXT` e porque se testa o pedido `AXFR`?**
   > [!success]- Ver Resposta
   > O registo `TXT` expõe políticas de e-mail (`SPF`, `DMARC`) e tokens de verificação de serviços externos/cloud utilizados pela organização. O pedido `AXFR` testa se o servidor DNS permite indevidamente transferência de zona a qualquer cliente, o que exporia todos os registos e hostnames internos/externos do domínio.

## Notas relacionadas
- [[Footprinting - Conceitos, Objetivos e Motores de Pesquisa (Google Hacking)]]
- [[OSINT - Plataformas (GitHub, Trello), Redes Sociais, Website e E-mail]]
- [[Footprinting Pentest e Contramedidas (Metodologia Prática)]]
- [[Scanning de Redes - Conceitos, Flags TCP e Descoberta ICMP]]
