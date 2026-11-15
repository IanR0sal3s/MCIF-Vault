---
title: "Técnicas de Port Scanning TCP, UDP e IDLE Scan"
uc: Cibersegurança Ofensiva e Defensiva I
sigla_uc: COD1
tipo: nota
capitulo: 4
topico: tecnicas-port-scanning
tags: [cod1, port-scanning, tcp, udp, idle-scan, nmap]
---
# Técnicas de Port Scanning TCP, UDP e IDLE Scan

**Capítulo:** [[Capítulo 4 - Scanning de Redes]]

> [!TIP] Lógica de Funcionamento e Valor Operacional
> Escolher a técnica certa de *port scanning* determina se o pentester precisa de privilégios `root`, se o scan será registado nos logs aplicacionais do alvo, se consegue inferir regras de firewall (*stateful* vs. *stateless*) ou até se consegue varrer um alvo de forma totalmente anónima através de um *zombie* (`IDLE Scan`).

## 1. Estados de Portos no `Nmap`

O `Nmap` classifica cada porto verificado num de seis estados:

- **`open`:** Existe uma aplicação/serviço à escuta a aceitar ligações.
- **`closed`:** O host está acessível e responde, mas não há nenhum serviço à escuta nesse porto.
- **`filtered`:** Uma firewall, filtro ou regra de rede bloqueia as sondas e impede determinar se o porto está aberto ou fechado.
- **`unfiltered`:** O porto é acessível às sondas (ex.: `ACK scan`), mas não é possível determinar se está aberto ou fechado.
- **`open|filtered`:** O `Nmap` não recebe resposta e não consegue distinguir se o porto está aberto (ex.: UDP/FIN/NULL/Xmas) ou filtrado por firewall.
- **`closed|filtered`:** Ocorre apenas em técnicas específicas (como `IP ID Idle Scan`) quando não é possível distinguir entre fechado e filtrado.

## 2. Técnicas de Port Scanning TCP, UDP e Protocolos

| Técnica (`Nmap`) | Flags / Mecanismo | Resposta: Aberto vs. Fechado | Notas Operacionais |
| :--- | :--- | :--- | :--- |
| **TCP Connect (`-sT`)** | Completa o *3-way handshake* (`SYN` -> `SYN/ACK` -> `ACK`) e envia `RST`. | `SYN/ACK` = aberto; `RST` = fechado. | Única opção sem privilégios `root`; mais lenta e facilmente registada em logs. |
| **TCP SYN / Stealth (`-sS`)** | Envia `SYN`; se receber `SYN/ACK`, envia `RST` sem completar handshake. | `SYN/ACK` = aberto; `RST` = fechado. | **Modo predefinido** (requer `root`); muito rápido e evita logs aplicacionais completos. |
| **TCP NULL (`-sN`)** | Nenhuma flag TCP ativa. | Sem resposta = aberto ou filtrado; `RST` = fechado. | Baseado na RFC 793; passa algumas firewalls *stateless*; não funciona em Windows. |
| **TCP FIN (`-sF`)** | Apenas flag `FIN` ativa. | Sem resposta = aberto ou filtrado; `RST` = fechado. | Mesmo comportamento do NULL scan. |
| **TCP Xmas (`-sX`)** | Flags `FIN`, `PSH`, `URG` ativas. | Sem resposta = aberto ou filtrado; `RST` = fechado. | Eficaz sobretudo em sistemas baseados em UNIX que seguem a RFC 793. |
| **TCP ACK (`-sA`)** | Flag `ACK` ativa. | `RST` = `unfiltered`; sem resposta / ICMP unreachable = `filtered`. | **Não distingue aberto de fechado**; serve para mapear regras de firewall (*stateful* vs. *stateless*). |
| **TCP Window (`-sW`)** | Igual ao `ACK`, mas inspeciona o campo `Window` do `RST`. | Em certos sistemas (ex.: BSD): `window > 0` = aberto; `window = 0` = fechado. | Útil apenas em stacks TCP específicas; comparar com outros scans. |
| **TCP Maimon (`-sM`)** | Flags `FIN` + `ACK` ativas. | RFC 793 dita `RST` sempre, mas alguns BSD não respondem se aberto. | Técnica clássica para sistemas BSD antigos. |
| **UDP Scan (`-sU`)** | Envia pacotes UDP (sem handshake). | Sem resposta = aberto ou filtrado; `ICMP port unreachable` = fechado. | Muito lento devido a rate-limiting de ICMP, mas essencial para DNS (53), SNMP (161), NTP (123). |
| **IP Protocol (`-sO`)** | Testa protocolos IP suportados (TCP, UDP, ICMP, IGMP, etc.). | Resposta do protocolo ou ausência de `protocol-unreachable` = suportado. | Não varre portos; lista protocolos IP aceites pelo host. |

## 3. Funcionamento Detalhado do `IDLE / IP Header Scan` (`-sI`)

O **IDLE Scan** (`nmap -Pn -p- -sI <zombie> <alvo>`) é o método mais furtivo do `Nmap`: o IP de origem visto pelo alvo e pelo seu IDS é o de um terceiro host (**zombie**), nunca o do atacante.

- **Princípio do IPID:** Cada pacote IP tem um identificador de fragmento (`IPID`) incrementado sequencialmente por cada pacote enviado pelo sistema operativo do *zombie* (que deve ter tráfego mínimo/previsível).
- **Sequência de Passos:**
  1. O atacante sonda o *zombie* (ex.: `SYN/ACK` não solicitado -> recebe `RST`) e lê o `IPID` atual ($N$).
  2. O atacante envia um `SYN` ao **alvo** com o **IP de origem falsificado como sendo o do *zombie***.
     - **Se o porto no alvo estiver aberto:** o alvo envia `SYN/ACK` para o *zombie*; como o *zombie* não iniciou a ligação, responde com `RST` ao alvo, incrementando o seu `IPID` para $N+1$.
     - **Se o porto no alvo estiver fechado/filtrado:** o alvo responde `RST` (que o *zombie* ignora) ou não responde; o *zombie* não envia nada e o seu `IPID` mantém-se em $N$.
  3. O atacante volta a sondar o *zombie* e lê o novo `IPID`:
     - Incremento de **2 unidades** ($N+2$) -> **porto aberto** no alvo.
     - Incremento de **1 unidade** ($N+1$) -> **porto fechado ou filtrado**.

## Além da aula

> [!NOTE] Conteúdo Complementar (Além da aula)
> Boas práticas operacionais ao escolher scans no terreno:

- **Combinar `-sS` (rápido) com `-sU --top-ports 100`:** Em pentests corporativos, falhar o varrimento UDP deixa passar serviços críticos como `SNMP` (161), `TFTP` (69), `IPsec/IKE` (500) e `DNS` (53). Corra um scan UDP focado nos portos mais comuns em paralelo ou após o scan TCP completo (`-p-`).
- **Limitações modernas do IDLE Scan:** Sistemas operativos modernos (Linux recente, Windows modernos, OpenBSD) geram `IPID` aleatórios ou por ligação em vez de um contador global previsível, tornando mais difícil encontrar *zombies* adequados (geralmente impressoras de rede antigas, dispositivos IoT ou routers antigos).

## Perguntas de revisão

1. **Porque é que um `TCP ACK scan` (`-sA`) não consegue distinguir entre um porto aberto e um porto fechado, e qual é então a sua utilidade?**
   > [!success]- Ver Resposta
   > Porque tanto os portos abertos como os fechados respondem com `RST` a um pacote `ACK` não solicitado (quando não há filtragem). A sua utilidade é mapear regras de firewall: saber quais os portos filtrados (*stateful*) e quais passam diretamente (*unfiltered*).

2. **No `IDLE Scan`, o que indica um incremento de 2 unidades no `IPID` do *zombie* entre as duas sondas do atacante?**
   > [!success]- Ver Resposta
   > Indica que o porto está **aberto** no alvo: +1 unidade deve-se ao `RST` que o *zombie* enviou ao alvo após receber o `SYN/ACK`, e +1 unidade deve-se à segunda sonda de leitura feita pelo atacante.

## Notas relacionadas
- [[Scanning de Redes - Conceitos, Flags TCP e Descoberta ICMP]]
- [[Nmap Avançado e Hping3 - Descoberta, Port Scanning e Evasão]]
- [[Evasão a IDS-Firewall, Banner Grabbing e Metodologia Pentest]]
