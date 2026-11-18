---
title: Conceitos Fundamentais de Segurança (CIA, Ameaça, Vulnerabilidade e Ataque)
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Transversal (COD1 e SRC)
sigla_uc: COMUM
ucs_relacionadas:
  - COD1
  - SRC
tags:
  - comum
  - cia
  - rfc-4949
  - ameaca
  - vulnerabilidade
  - vetores-ataque
aliases:
  - Conceitos de Cibersegurança, Terminologia e Vetores de Ataque
  - Conceitos de Segurança - CIA, Vulnerabilidade, Ameaça, Ataque e RFC 4949
  - Tríade CIA
  - Vulnerabilidade Ameaça Ataque
  - Ataques Passivos e Ativos
  - Terminologia Hacking
  - Pivoting
  - Daisy Chaining
  - Vetores de Ataque COD1
atualizado: 2026-11-18
---

# Conceitos Fundamentais de Segurança (CIA, Ameaça, Vulnerabilidade e Ataque)

A segurança da informação e de redes visa preservar a **confidencialidade, integridade e disponibilidade (CIA)** dos recursos de um sistema através da identificação rigorosa de ativos, vulnerabilidades, ameaças e vetores de ataque. Um ataque informático resulta da conjunção de três fatores — **Objetivo (motivo) + Método + Vulnerabilidade** — visando explorar ativos com *hack value* através de vetores de rede, máquina ou aplicação.

> [!TIP] Lógica de Funcionamento e Valor Transversal
> * **Porque existe (Norma e Operação)**: Distinções imprecisas entre falha técnica, risco potencial e ação hostil dificultam a análise de risco, a resposta a incidentes e a execução de *pentests*; normas como o NIST e a `RFC 4949` uniformizam o vocabulário entre redes (`SRC`) e segurança ofensiva/defensiva (`COD1`).
> * **Porque importa (Segurança e Pentesting)**: Permite mapear cenários concretos (ex.: câmara de rede exposta com *password* por omissão) em controlos técnicos adequados, distinguir ataques silenciosos (passivos) de ataques que alteram dados ou serviços (ativos) e compreender porque o *daisy chaining / pivoting* permite que um servidor comprometido na DMZ dê acesso à rede interna crítica.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * Uma **vulnerabilidade** pode existir antes de qualquer exploração; um **ataque** é uma tentativa deliberada e **pode falhar**.
>   * **Vulnerabilidade** (falha/erro de implementação) $\neq$ ***Exploit*** (forma/código para ganhar acesso através da vulnerabilidade) $\neq$ ***Payload*** (código malicioso executado após a exploração, ex.: criar *backdoor*).
>   * ***Zero-day***: ataque que explora uma vulnerabilidade **antes** de ser publicada ou existir *patch* de correção.
>   * **Ataques *shrink-wrap code***: exploração de configurações por omissão ou mal concebidas em bibliotecas/código de software colocado em produção.
>   * **Ataques passivos** (*sniffing*, análise de tráfego, *taps*) **não alteram os dados** (prevenção via cifragem); **ataques ativos** (*spoofing*, `DoS`, alteração/repetição de mensagens) **modificam ou perturbam dados/fluxos** (deteção e recuperação).

---

## 1. Objetivos de Segurança: Tríade CIA e Extensões NIST

Segundo o **NIST**, *Computer Security* é a proteção conferida a um sistema de informação automatizado para atingir os objetivos aplicáveis de preservar a **integridade**, **disponibilidade** e **confidencialidade** dos recursos do sistema (*hardware*, *software*, *firmware*, informação/dados e telecomunicações).

| Propriedade | Definição |
| :--- | :--- |
| **Confidencialidade (*Confidentiality*)** | Prevenir a divulgação não autorizada de informação (inclui privacidade de dados e de fluxos). |
| **Integridade (*Integrity*)** | Proteger informação e sistemas contra modificação ou destruição imprópria (integridade de dados e de sistema). |
| **Disponibilidade (*Availability*)** | Garantir acesso atempado e fiável à informação e aos serviços. |
| **Autenticidade (*Authenticity*)** | Confiança de que uma entidade ou a origem da informação é genuína. |
| **Responsabilização (*Accountability*)** | Capacidade de rastrear ações até à entidade responsável. |

---

## 2. Terminologia Fundamental e Cadeia de Risco

A cadeia de risco articula os elementos técnicos e operacionais desde o recurso a proteger até às consequências de um incidente e respetivas defesas:

| Conceito | Definição | Exemplo Prático (Câmara de Rede no Laboratório) |
| :--- | :--- | :--- |
| **Ativo (*Asset*)** | Recurso com valor a proteger. | A câmara de rede, o *feed* de vídeo e a sua configuração. |
| **Vulnerabilidade (*Vulnerability*)** | Fraqueza ou erro de implementação num sistema, configuração ou procedimento que pode ser explorada ou acionada. | A interface de administração está acessível a partir da Internet e mantém a *password* por omissão. |
| **Ameaça (*Threat*)** | Potencial de dano — circunstância ou evento (exploração potencial ou efetiva de uma vulnerabilidade) que pode comprometer o sistema ou informação. | Um agente externo pode assumir o controlo da conta de administração. |
| **Risco (*Risk*)** | Probabilidade e impacto potencial de uma ameaça explorar uma vulnerabilidade e causar dano a um ativo. | Elevado, dada a exposição direta à Internet e credenciais previsíveis. |
| **Ataque (*Attack*)** | Tentativa deliberada e intencional de comprometer a segurança (pode falhar). | Alguém submete as credenciais por omissão para obter acesso não autorizado. |
| **Contramedida (*Countermeasure*)** | Controlo técnico, físico ou procedimental aplicado para eliminar ou mitigar vulnerabilidades, ameaças ou impactos. | Alterar a *password* por omissão, restringir a interface por VPN/*firewall* e atualizar o *firmware*. |
| **Impacto possível** | Consequência da materialização da ameaça. | Exposição de vídeo, alterações não autorizadas de configuração ou interrupção da gravação. |

---

## Aplicação por UC

### Em SRC (Taxonomia RFC 4949 e Stallings)

Na unidade curricular **Segurança em Redes de Computadores** (`1_fundamentals.pdf`, Slides 14–20; `ch1_Computer_Network_Security_Concepts.pdf`, Secções 1.1–1.3), a `RFC 4949` e William Stallings classificam os ataques em **passivos** e **ativos** consoante alterem ou não os dados ou o funcionamento do sistema:

| Tipo de Ataque | Característica Central | Subtipos e Exemplos | Estratégia Principal |
| :--- | :--- | :--- | :--- |
| **Passivo** | **Sem alteração de dados**; o atacante observa ou monitoriza transmissões de forma silenciosa. | Escuta/*eavesdropping* (*sniffing*, *taps*), análise de tráfego (*traffic analysis*). | **Prevenção** (ex.: cifragem), pois é difícil de detetar. |
| **Ativo** | **Com alteração de dados** ou perturbação do fluxo normal de comunicação/serviço. | Mascaramento (*masquerade* / *spoofing*), repetição de mensagens (*replay*), alteração de mensagens (*modification*), negação de serviço (`DoS`). | **Deteção e recuperação**, complementadas por prevenção. |

Para o mapeamento entre estes ataques e os respetivos controlos normativos, ver [[Serviços e Mecanismos de Segurança (ITU-T X.800)]].

### Em COD1 (Ethical Hacking e Vetores de Ataque)

Na unidade curricular **Cibersegurança Ofensiva e Defensiva I** (`2026.27_MCIF_COD1_01_Introdução à Cibersegurança.pdf`, Slides 4–32), a terminologia foca a execução prática de ataques e o trabalho de *pentesting*.

#### Terminologia Fundamental (Slide 21)

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

#### Objetivos e Vetores de Ataque (Slides 25–32)

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

Para enquadramento nas etapas operacionais do auditor, ver [[Fases do Hacking e Âmbito do Ethical Hacking]].

---

## Perguntas de revisão

1. **Qual a diferença prática entre vulnerabilidade, ameaça e ataque no cenário de uma câmara de rede com *password* por omissão exposta à Internet?**

> [!success]- Ver Resposta
> A **vulnerabilidade** é a fraqueza técnica/de configuração (interface exposta com *password* por omissão); a **ameaça** é o potencial dano (tomada de controlo não autorizada da câmara); o **ataque** é a ação deliberada de alguém tentar iniciar sessão com essas credenciais (que pode ter sucesso ou falhar).

2. **Porque é que os ataques passivos exigem sobretudo prevenção enquanto os ativos exigem deteção e recuperação?**

> [!success]- Ver Resposta
> Como os ataques passivos (*eavesdropping*/*sniffing*, análise de tráfego) não alteram os dados nem deixam vestígios óbvios na transmissão, são difíceis de detetar, tornando a prevenção (cifragem) prioritária; já os ataques ativos (*masquerade*, *replay*, *modification*, `DoS`) alteram mensagens ou degradam serviços, podendo ser detetados e mitigados com mecanismos de deteção e recuperação.

3. **Qual a diferença entre *Exploit*, *Payload* e *Pivoting* num teste de penetração?**

> [!success]- Ver Resposta
> O ***exploit*** é o mecanismo que aproveita a vulnerabilidade para obter acesso; o ***payload*** é o código executado após o acesso (ex.: abrir uma *backdoor* ou *reverse shell*); o ***pivoting*** (*daisy chaining*) consiste em usar esse sistema comprometido como ponto de salto para aceder a outras redes/sistemas internos.

4. **O que caracteriza um ataque *shrink-wrap code*?**

> [!success]- Ver Resposta
> A exploração de configurações por omissão ou mal concebidas em bibliotecas, *frameworks* ou código-fonte de software de terceiros colocado em produção sem *hardening*.

---

## Notas relacionadas

- [[Fases do Hacking e Âmbito do Ethical Hacking]]
- [[Testes de Penetração - Metodologia, Pentest Request e Relatórios]]
- [[Modelo TCP-IP, Encapsulamento e Visibilidade de Tráfego HTTPS]]
- [[Serviços e Mecanismos de Segurança (ITU-T X.800)]]
- [[Princípios Fundamentais de Desenho Seguro, Attack Surfaces e Attack Trees]]
