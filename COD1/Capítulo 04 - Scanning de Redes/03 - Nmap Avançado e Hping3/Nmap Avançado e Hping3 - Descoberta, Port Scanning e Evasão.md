---
title: Nmap Avançado e Hping3 - Descoberta, Port Scanning e Evasão
tipo: ferramenta
mestrado: Cibersegurança e Informática Forense
uc: Cibersegurança Ofensiva e Defensiva I
sigla_uc: COD1
capitulo: 4
bloco: 3
fonte_aula: 2026.27_MCIF_COD1_04_Scanning.pdf (Slides 26–29); nmap_avancado.pdf (Slides 17, 29–36)
tags: [cod1, nmap, nse, ndiff, hping3, masscan, unicornscan]
aliases: [Nmap Avançado, NSE, ndiff, Hping3]
criado: 2026-11-15
atualizado: 2026-11-16
---

# Nmap Avançado e Hping3 - Descoberta, Port Scanning e Evasão

O uso avançado do `Nmap` combina temporização (`-T0`–`-T5`, RTT timeouts), scripts `NSE`, interseção de scans (`-sS` + `-sF` + `-sA`), comparação com `ndiff` e ferramentas de alto débito (`Masscan`, `Unicornscan`, `Hping3`).

> [!TIP] Lógica de Funcionamento e Valor Operacional
> * **Porque existe (Sistema)**: Firewalls e redes congestionadas mascaram o estado real dos portos se o auditor usar apenas o scan padrão.
> * **Porque importa (Pentesting / Segurança)**: Cruzar `-sS`, `-sF` e `-sA` separa portos realmente fechados de portos abertos atrás de filtros, enquanto `-sV` e `NSE` detetam serviços anómalos e backdoors.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **`open|filtered`** no `-sF` + **`unfiltered`** no `-sA` = porto **aberto**; **`open|filtered`** + **`filtered`** = porto **filtrado**.
>   * `-oA` grava simultaneamente `.nmap`, `.xml` (para `ndiff`) e `.gnmap` (para `grep`/`awk`).

## 1. Controlo de Alvos, Portos, Temporização e Output no `Nmap`

- **Especificação de alvos:** IP único (`192.168.10.123`), intervalo (`192.168.10.0-200`), CIDR (`192.168.10.0/24`) ou ficheiro (`-iL alvos.txt`).
- **Portos:** `-p22`, `-p1-1024`, `-p U:53,111,137,T:21-25,80,139,8080`, `-p-` (todos os 65 535 portos) ou `--top-ports=100`.
- **Resolução DNS e Deteção:**
  - `-n`: desativa resolução DNS inversa (acelera muito o scan).
  - `-O`: deteção de sistema operativo.
  - `-sV`: deteção de versões de serviços (mais de 1000 assinaturas; ajuda também a detetar backdoors ou máquinas infetadas, ex.: MyDoom, embora possa gerar alarmes em IDS).
  - `-A`: modo agressivo (`-O` + `-sV` + `-sC` + `--traceroute`).
- **Perfis de Temporização (`-T0` a `-T5`):**
  - `-T0` (*Paranoid*, ~5 min entre sondas) e `-T1` (*Sneaky*, ~15 s): evasão a IDS e proteção contra crashes/saturação de largura de banda.
  - `-T2` (0,4 s) e `-T3` (predefinido).
  - `-T4` (~10 ms, paralelização): recomendado pelo autor do Nmap para redes estáveis.
  - `-T5` (~5 ms, paralelização agressiva): muito rápido, mas pode perder pacotes.
  - **Ajuste fino de RTT:** `--initial-rtt-timeout 150 --max-rtt-timeout 200` (útil na Internet onde muitos pacotes são filtrados; estimar RTT previamente com `ping`/`hping`).
- **Formatos de Output:** `-oN` (normal), `-oX` (XML), `-oG` (*greppable*), `-oS` (script kiddie), `-oA <prefixo>` (gera `.nmap`, `.xml` e `.gnmap` em simultâneo).

## 2. Nmap Scripting Engine (NSE) e `ndiff`

- **Localização dos scripts:** `/usr/share/nmap/scripts/`
- **Pesquisa e atualização:**
  ```bash
  nmap --script-updatedb
  cat /usr/share/nmap/scripts/scripts.db | grep -E "safe|version"
  nmap --script-help "*http* and safe"
  ```
- **Execução:** `-sC` (equivalente a `--script default`), `--script <nome|categoria>` (ex.: `nmap -sSV --script version <IP>`).
- **Comparação temporal/entre scans (`ndiff`):** Compara dois ficheiros XML (`-oX`) e mostra alterações em hosts, estados de portos, versões de serviços e SO:
  ```bash
  sudo nmap -n -Pn -sS -oX sS.xml 192.168.226.3
  sudo nmap -n -Pn -sF -oX sF.xml 192.168.226.3
  ndiff sS.xml sF.xml
  ```

## 3. Interseção de Scans para Mapear Firewalls (`-sS` + `-sF` + `-sA`)

Quando um `SYN scan` (`-sS`) reporta a maioria dos portos como `filtered`, cruzar diferentes técnicas revela a verdade:

1. **Passo 1 (`-sS`):** Encontra 2 portos `open` e 998 `filtered`.
2. **Passo 2 (`-sF` — FIN scan):** Reporta 997 `closed` e 3 `open|filtered` -> logo, **997 dos 998 portos filtrados no `-sS` estão efetivamente fechados** (e a firewall não é *stateful* para pacotes FIN).
3. **Passo 3 (`-sA` — ACK scan):**
   - Se um porto aparece `filtered` no `-sA` e `open|filtered` no `-sF` -> o porto está **filtrado**.
   - Se aparece `unfiltered` no `-sA` e `open|filtered` no `-sF` -> o porto está **aberto**.

## 4. Outras Ferramentas de Scanning de Alta Velocidade / Pacotes Customizados

- **`Hping3`:** `hping3 <host/IP> --scan <porto> -S` (também excelente para testar regras de firewall, latência e fragmentação manual).
- **`Netcat` (`nc`):** `nc -z <host/IP> 1-1000` (varrimento simples TCP sem ICMP).
- **`Netdiscover`:** `netdiscover -r <IP/sub-rede>` (descoberta ARP passiva/ativa em LAN).
- **`Unicornscan`:** `us -r200 -mT -I <host/IP>:80,443` (scanning assíncrono de alto débito).
- **`Masscan`:** `masscan -p80 <IP/gama> --rate 1000 -e <interface>` (varrimento em larga escala extremamente rápido).

## Além da aula

> [!NOTE] Conteúdo Complementar (Além da aula)
> Fluxo de duas etapas para scans grandes sem perder portos:

- **Estratégia Masscan/Nmap rápido -> Nmap cirúrgico:** Em redes corporativas grandes (`/16` ou múltiplos `/24`), varra primeiro todos os portos TCP rapidamente (`sudo nmap -n -Pn -p- --min-rate 3000 -T4 -oG fast.gnmap <alvo>`) e, em seguida, passe **apenas os portos descobertos** para o scan detalhado (`sudo nmap -n -Pn -sC -sV -O -p <portos_descobertos> -oA detailed <alvo>`). Isto evita correr `-sV` e scripts NSE em 65 535 portos, poupando horas e reduzindo ruído.

## Perguntas de revisão

1. **Que vantagem oferece a opção `-oA` em relação a `-oN` durante um pentest?**
   > [!success]- Ver Resposta
   > A opção `-oA` guarda simultaneamente o resultado em três formatos: texto legível (`.nmap`), formato pesquisável por `grep`/`awk` (`.gnmap`) e XML (`.xml`) para importação em ferramentas de relatório, `ndiff` ou plataformas como o Metasploit.

2. **Se um porto surge como `open|filtered` num `FIN scan` (`-sF`) e como `unfiltered` num `ACK scan` (`-sA`), qual é o estado real desse porto?**
   > [!success]- Ver Resposta
   > O porto está **aberto**, pois o `ACK scan` provou que o tráfego atravessa o filtro sem ser bloqueado (`unfiltered`) e o `FIN scan` não recebeu `RST` de volta.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Técnicas de Port Scanning TCP, UDP e IDLE Scan]] | `Bloco 02` |
| **Seguinte** | [[Evasão a IDS-Firewall, Banner Grabbing e Metodologia Pentest]] | `muda para Bloco 04` |
| **Índice** | [[Capítulo 4 - Scanning de Redes]] · [[00 COD1]] | `Bloco 03` |

### Conceitos Relacionados

* [[Scanning de Redes - Conceitos, Flags TCP e Descoberta ICMP]] · `Bloco 01`
* [[Cheat Sheet - Scanning de Redes e Nmap]] · `mesmo cap.`
