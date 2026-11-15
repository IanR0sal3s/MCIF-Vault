---
title: Conceitos de Cibersegurança, Terminologia e Vetores de Ataque
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Cibersegurança Ofensiva e Defensiva I
sigla_uc: COD1
capitulo: 1
bloco: 1
fonte_aula: 2026.27_MCIF_COD1_01_Introdução à Cibersegurança.pdf (Slides 4–32)
tags:
  - cod1
  - ciberseguranca
  - vetores-de-ataque
  - terminologia
aliases:
  - Terminologia Hacking
  - Pivoting
  - Daisy Chaining
  - Vetores de Ataque COD1
atualizado: 2026-11-15
---

# Conceitos de Cibersegurança, Terminologia e Vetores de Ataque

Um ataque informático resulta da conjunção de três fatores — **Objetivo (motivo) + Método + Vulnerabilidade** — visando explorar ativos com *hack value* através de vetores de rede, máquina ou aplicação.

> [!TIP] Lógica de Funcionamento e Valor Operacional
> * **Porque existe (Pentesting)**: Durante um *pentest* organizacional, o auditor deve classificar corretamente o que encontra (vulnerabilidade vs. *exploit* vs. *payload*) e mapear a superfície de ataque nas três camadas técnicas (Rede, Máquina, Aplicação).
> * **Porque importa (Defesa e Ataque)**: Compreender *daisy chaining / pivoting* explica porque comprometer um servidor aparentemente secundário na DMZ pode dar acesso à rede interna crítica.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Vulnerabilidade** (falha/erro de implementação) $\neq$ ***Exploit*** (forma/código para ganhar acesso através da vulnerabilidade) $\neq$ ***Payload*** (código malicioso executado após a exploração, ex.: criar *backdoor*).
>   * ***Zero-day***: ataque que explora uma vulnerabilidade **antes** de ser publicada ou existir *patch* de correção.
>   * **Ataques *shrink-wrap code***: exploração de configurações por omissão ou mal concebidas em bibliotecas/código de software colocado em produção.

---

## 1. Terminologia Fundamental (Slide 21)

| Termo | Definição da UC |
| :--- | :--- |
| ***Hack value*** | Noção do valor/interesse que um sistema ou informação tem para um atacante. |
| **Vulnerabilidade** | Falha ou erro de implementação que pode levar a um evento inesperado que comprometa a segurança. |
| ***Threat*** | Exploração potencial ou efetiva de uma vulnerabilidade. |
| ***Exploit*** | Forma de ganhar acesso a um sistema explorando uma quebra de segurança através de uma vulnerabilidade. |
| ***Payload*** | Parte do código malicioso que executa a ação desejada após o acesso (ex.: criação de uma *backdoor*). |
| **Ataque *zero-day*** | Ataque que explora uma vulnerabilidade antes da publicação de um *patch* de correção. |
| ***Daisy chaining / Pivoting*** | Uso da informação/acesso obtido numa rede ou sistema para ganhar acesso a múltiplas redes/sistemas subsequentes. |
| ***Bot*** | Aplicação controlável remotamente para executar ou automatizar determinadas tarefas. |

---

## 2. Objetivos e Vetores de Ataque (Slides 25–32)

* **Objetivos típicos**: disrupção do negócio, roubo de informação, manipulação de dados, pânico por interrupção de infraestruturas críticas, propaganda política/religiosa, dano reputacional e vingança.
* **Principais vetores**: *cloud computing*, *APTs* (*Advanced Persistent Threats*), *malware*/vírus/*worms*, *ransomware*, dispositivos móveis, *botnets*, ataques *insider* e *phishing*, sistemas IoT e aplicações web.

| Camada | Categorias de Ameaças (Slides 28–30) |
| :--- | :--- |
| **Rede** | Recolha de informação, escuta/espionagem, falsificação, roubo de sessão e `MITM`, `DNS`/`ARP poisoning`, ataques a *passwords*, `DoS`/`DDoS`, ataques a *Firewall* e `IDS`. |
| **Máquina** | Software malicioso e *backdoors*, *footprinting*, ataques a *passwords*, `DoS`/`DDoS`, execução de código, acessos não autorizados, escalonamento de privilégios, ameaças físicas. |
| **Aplicação** | *Injection*, má validação de *input*, falhas de autenticação/autorização, má configuração, divulgação de informação, *buffer overflow*, ataques à gestão de sessões, falhas criptográficas. |

**Quatro tipos de ataques a um sistema (Slides 31–32):**
1. **Sistema Operativo (SO)**: exploração de vulnerabilidades do próprio SO.
2. **Falhas de configuração**: má configuração em servidores web, aplicações, bases de dados ou redes.
3. **Nível aplicacional**: exploração de falhas no código da aplicação para roubo/modificação de dados.
4. ***Shrink-wrap code***: exploração de configurações por omissão em bibliotecas ou código de terceiros em produção.

---

## Perguntas de revisão

1. **Qual a diferença entre *Exploit*, *Payload* e *Pivoting* num teste de penetração?**

> [!success]- Ver Resposta
> O ***exploit*** é o mecanismo que aproveita a vulnerabilidade para obter acesso; o ***payload*** é o código executado após o acesso (ex.: abrir uma *backdoor* ou *reverse shell*); o ***pivoting*** (*daisy chaining*) consiste em usar esse sistema comprometido como ponto de salto para aceder a outras redes/sistemas internos.

2. **O que caracteriza um ataque *shrink-wrap code*?**

> [!success]- Ver Resposta
> A exploração de configurações por omissão ou mal concebidas em bibliotecas, *frameworks* ou código-fonte de software de terceiros colocado em produção sem *hardening*.

## Notas relacionadas

- [[Fases do Hacking e Âmbito do Ethical Hacking]]
- [[Testes de Penetração - Metodologia, Pentest Request e Relatórios]]
- [[Conceitos de Segurança - CIA, Vulnerabilidade, Ameaça, Ataque e RFC 4949]]
