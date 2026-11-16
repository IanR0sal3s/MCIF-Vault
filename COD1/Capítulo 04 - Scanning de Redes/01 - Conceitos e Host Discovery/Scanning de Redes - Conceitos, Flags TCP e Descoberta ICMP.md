---
title: Scanning de Redes - Conceitos, Flags TCP e Descoberta ICMP
tipo: tecnica
mestrado: Cibersegurança e Informática Forense
uc: Cibersegurança Ofensiva e Defensiva I
sigla_uc: COD1
capitulo: 4
bloco: 1
fonte_aula: 2026.27_MCIF_COD1_04_Scanning.pdf (Slides 3–15); nmap_avancado.pdf (Slides 1–16)
tags: [cod1, scanning, host-discovery, icmp, arp, ipv6, nmap]
aliases: [Host Discovery, ICMP Scanning, ARP Scan]
criado: 2026-11-15
atualizado: 2026-11-16
---

# Scanning de Redes - Conceitos, Flags TCP e Descoberta ICMP

O *scanning* de redes identifica hosts ativos, portos, serviços e sistemas operativos através de pacotes `ICMP`, `TCP` (`-PS`/`-PA`), `UDP` (`-PU`), `ARP` (`-PR`) e protocolos IP (`-PO`).

> [!TIP] Lógica de Funcionamento e Valor Operacional
> * **Porque existe (Sistema)**: O `Nmap` executa *Host Discovery* antes do *Port Scan* para não perder tempo a varrer milhares de IPs inativos.
> * **Porque importa (Pentesting / Segurança)**: Combinar múltiplos métodos de descoberta evita falsos negativos quando uma firewall bloqueia `ICMP Echo` (`ping`).
> * **Pontos Críticos e Armadilhas para Exame**:
>   * Na mesma LAN Ethernet, **`ARP Scan (-PR)`** é o método mais rápido e fiável (usado por omissão pelo Nmap).
>   * Combinar `-PS` (SYN) e `-PA` (ACK) maximiza a deteção atrás de firewalls *stateless*.
>   * Em **IPv6**, o varrimento completo é inviável (128 bits), mas dentro da sub-rede pode usar-se *link-local multicast*.

## 1. Conceito e Objetivos do Scanning de Redes

O **Scanning de Redes** compreende os procedimentos utilizados para identificar hosts, portos e serviços ativos numa rede, contribuindo para construir o perfil técnico da organização alvo:

- Descoberta de **hosts ligados** e respetivos endereços IP.
- Identificação de **portos** abertos/filtrados e **serviços** em operação.
- Deteção de **sistemas operativos** e arquiteturas.
- Identificação inicial de **vulnerabilidades** e topologia de filtragem.

### Ferramentas de Scanning e Pacotes Raw
- **Scanners principais:** `Ping`, `tracert`/`traceroute`, `Nmap` / `Zenmap` (GUI), `Hping2`/`Hping3`, `Netdiscover`, `Unicornscan`, `Masscan`, `JFScan`, `Angry IP Scanner`.
- **Criação de pacotes RAW (e fragmentação para evasão):** `packETH`, `Ostinato` (`ostinato.org`), `Hping`, `Scapy`, `Yersinia`.

### Particularidades de Scanning em Redes IPv6
- Como o **IPv6** passa de 32 bits para **128 bits**, o varrimento exaustivo tradicional de uma sub-rede IPv6 inteira é computacionalmente inviável.
- Contudo, se o atacante comprometer um host dentro da sub-rede IPv6, pode descobrir os restantes nós através do endereço **link-local multicast** (`ff02::1`).

## 2. Descoberta de Hosts (*Host Discovery*)

Por omissão, o `Nmap` não faz *port scan* a IPs que não respondam à fase de descoberta (alterável com `-Pn`, que força o scan assumindo que todos os hosts estão ativos, embora aumente muito o tempo de execução).

| Técnica / Opção `Nmap` | Mecanismo e Resposta Esperada | Quando Usar |
| :--- | :--- | :--- |
| **ICMP Echo (`-PE`) / Ping Sweep** | Envia `ICMP Echo Request`; host ativo responde com `ICMP Echo Reply`. | LANs internas onde ICMP não está bloqueado; verifica se ICMP atravessa firewall. |
| **ICMP Timestamp (`-PP`) e Netmask (`-PM`)** | Envia `timestamp-request` ou `address-mask-request`; resposta indica host ativo. | Alternativa quando o `ICMP Echo` (`ping`) está bloqueado. |
| **TCP SYN Discovery (`-PS<portos>`)** | Simula início de ligação TCP (ex.: `22,25,80`). Receber `SYN/ACK` ou `RST` prova que o host está ativo. | Redes com ICMP bloqueado mas com serviços TCP expostos. |
| **TCP ACK Discovery (`-PA<portos>`)** | Envia `ACK` para ligação inexistente; servidor responde com `RST`, revelando que existe. | Atravessar firewalls *stateless* mal configuradas que apenas bloqueiam `SYN` de entrada. |
| **UDP Discovery (`-PU<portos>`)** | Envia UDP para portos invulgares (omissão `40125`, ou `53`). Porto fechado devolve `ICMP port unreachable`. | Atravessar firewalls que apenas monitorizam tráfego TCP. |
| **ARP Scan (`-PR`)** | Usa pedidos ARP na LAN Ethernet; resposta ARP devolve logo IP + MAC. | **Mais rápido e fiável na mesma LAN** (usado automaticamente pelo Nmap em rede local). |
| **IP Protocol (`-PO<protocolos>`)** | Envia pacotes IP com protocolos (omissão: `1` ICMP, `2` IGMP, `4` IP-in-IP). | Descoberta alternativa quando filtros bloqueiam TCP/UDP padrão. |

### Exemplo Prático de Descoberta Combinada
```bash
# Descoberta intensiva sem port scan (-sn / -sP) combinando ICMP, SYN e ACK com porto de origem 53
sudo nmap -sn -PE -PP -PS21,22,23,25,80,113,21339 -PA80,113,443,10042 --source-port 53 -n -T4 192.168.226.0/24
```

## Além da aula

> [!NOTE] Conteúdo Complementar (Além da aula)
> Boas práticas de *Host Discovery* no início de um pentest organizacional:

- **Guardar sempre a lista de hosts ativos:** Exportar em formato greppable (`-oG hosts_up.gnmap`) e extrair os IPs com `awk '/Up$/{print $2}' hosts_up.gnmap > live_hosts.txt` para alimentar os scans de portos subsequentes sem repetir descoberta.
- **Cuidado com `-Pn` em gamas grandes:** Num `/16` ou `/20` externo, usar `-Pn` faz o `Nmap` testar todos os portos em milhares de IPs mortos; prefira primeiro uma combinação rápida de `-PS80,443,22,3389 -PA80,443 -PE` e só use `-Pn` em alvos específicos suspeitos de descartar sondas de descoberta.

## Perguntas de revisão

1. **Porque é que o `ARP Scan` (`-PR`) é mais rápido e fiável do que o `ICMP Scan` (`-PE`) numa LAN Ethernet?**
   > [!success]- Ver Resposta
   > Porque, numa LAN, mesmo antes de enviar um pacote ICMP o sistema operativo já precisa de resolver o endereço MAC via ARP. O `-PR` obtém diretamente a confirmação de presença e o MAC na resposta ARP sem depender de o host responder a ICMP.

2. **Qual a vantagem de combinar `-PS` e `-PA` na descoberta de hosts?**
   > [!success]- Ver Resposta
   > Firewalls *stateless* mal configuradas podem bloquear pacotes `SYN` de entrada (`-PS`) mas deixar passar pacotes `ACK` (`-PA`), aos quais o host responde com `RST`. Combinar ambos maximiza a taxa de deteção de máquinas ativas.

## Notas relacionadas
- [[Técnicas de Port Scanning TCP, UDP e IDLE Scan]]
- [[Nmap Avançado e Hping3 - Descoberta, Port Scanning e Evasão]]
- [[WHOIS, DNS, Networking Footprinting e Engenharia Social]]
