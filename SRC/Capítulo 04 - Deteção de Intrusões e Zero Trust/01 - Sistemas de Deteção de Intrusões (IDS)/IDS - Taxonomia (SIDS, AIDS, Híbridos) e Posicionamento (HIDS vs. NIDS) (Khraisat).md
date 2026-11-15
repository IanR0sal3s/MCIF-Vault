---
title: IDS - Taxonomia (SIDS, AIDS, Híbridos) e Posicionamento (HIDS vs. NIDS) (Khraisat)
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Segurança em Redes de Computadores
sigla_uc: SRC
capitulo: 4
bloco: 1
fonte_aula: s42400-019-0038-7.pdf (Abstract, Intrusion Detection Systems, SIDS, Intrusion Data Sources, Hybrid, Tabelas 2 e 4)
tags:
  - src
  - ids
  - sids
  - aids
  - hids
  - nids
aliases:
  - Intrusion Detection System
  - SIDS vs AIDS
  - HIDS vs NIDS
atualizado: 2026-11-15
---

# `IDS` — Taxonomia (`SIDS`, `AIDS`, Híbridos) e Posicionamento (`HIDS` vs. `NIDS`) (*Khraisat*)

Um **Sistema de Deteção de Intrusões (`IDS`)** é um sistema de software ou hardware que identifica atividades maliciosas em redes ou sistemas informáticos — algo que uma *firewall* tradicional não consegue detetar — para proteger a **confidencialidade, integridade e disponibilidade**.

> [!TIP] Lógica de Funcionamento e Valor de Segurança
> * **Porque existe (Deteção)**: *Firewalls* filtram tráfego por regras estáticas de porto/IP, mas não inspecionam padrões de ataque em carga útil ou anomalias comportamentais; o `IDS` monitoriza continuamente eventos de rede ou de *host*.
> * **Porque importa (Segurança)**: Combinar **`SIDS`** (assinaturas conhecidas, baixos falsos positivos) com **`AIDS`** (desvios do normal, deteção de *zero-days*) em **`Hybrid IDS`**, e cruzar **`HIDS`** + **`NIDS`**, oferece defesa em profundidade contra ameaças externas e internas.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **`SIDS`** (*Signature-based* / *Knowledge-based* / *Misuse Detection*): excelente precisão e **mínimos falsos alarmes** em ataques conhecidos (ex.: `Snort`), mas **incapaz de detetar *zero-day attacks*** ou variantes polimórficas sem assinatura prévia.
>   * **`AIDS`** (*Anomaly-based*): deteta ***zero-day attacks*** e atividades internas anómalas, mas sofre de **elevada taxa de falsos positivos (`FP`)** e **não consegue inspecionar pacotes cifrados**.
>   * **`HIDS` vs. `NIDS`**: o `HIDS` consegue analisar **comportamento em comunicações cifradas fim-a-fim** (no *endpoint*) e ataques *insider* locais, enquanto o `NIDS` monitoriza múltiplos *hosts* na rede sem instalação individual, mas tem dificuldade em tráfego cifrado e redes de alta velocidade.

---

## 1. Metodologias de Deteção: `SIDS`, `AIDS` e Híbridos (Tabela 2 e p. 11)

| Metodologia | Funcionamento | Vantagens | Desvantagens |
| :--- | :--- | :--- | :--- |
| **`SIDS`** (*Signature-based*) | Compara atividades/pacotes com uma base de dados de assinaturas conhecidas (ex.: regras `if antecedent then consequent`, `Snort`, `NetSTAT`). | Mínimos falsos alarmes; identificação rápida; superior em ataques conhecidos; desenho simples. | Exige atualização constante de assinaturas; falha perante pequenas variações; **não deteta *zero-day*** nem ataques multi-passo facilmente. |
| **`AIDS`** (*Anomaly-based*) | Constrói um modelo de comportamento normal (estatístico, conhecimento ou `ML`) e sinaliza desvios significativos como anomalias. | **Deteta ataques *zero-day*** e internos; útil para criar novas assinaturas; perfil personalizado dificulta evasão silenciosa. | **Elevados falsos positivos**; difícil definir perfil normal em sistemas dinâmicos; alertas não classificados; exige treino inicial; **não trata pacotes cifrados**. |
| **Técnicas Híbridas** | Combina **`SIDS` + `AIDS`** (ex.: *Naïve Bayes* + *Decision Tree*). | Supera as limitações individuais de `SIDS` (zero-days) e `AIDS` (falsos positivos). | Maior complexidade de integração e manutenção. |

---

## 2. Posicionamento e Fontes de Dados: `HIDS` vs. `NIDS` (Tabela 4)

| Tecnologia | Vantagens | Desvantagens | Fontes de Dados (*Data Sources*) |
| :--- | :--- | :--- | :--- |
| **`HIDS`** (*Host-based*) | Analisa comportamento de **comunicações cifradas fim-a-fim**; sem hardware extra; deteta ataques no sistema de ficheiros/chamadas de sistema e *insiders* sem tráfego de rede; remonta pacotes e analisa o item completo. | Atrasos no reporte; **consome recursos do *host***; exige instalação em cada *host*; monitoriza apenas a máquina local. | Registos de auditoria, ficheiros de *log* (SO, firewall, BD, aplicações), APIs, padrões de regras, **chamadas de sistema (*system calls*)**. |
| **`NIDS`** (*Network-based*) | Monitoriza vários *hosts* em simultâneo; **não exige instalação em cada *host***; deteta ataques externos precocemente antes de se propagarem; cobre vasta gama de protocolos. | **Dificuldade em identificar ataques em tráfego cifrado**; exige hardware dedicado; só deteta ataques de rede; difícil em redes de alta velocidade; vulnerável a ataques internos (*insiders*). | Pacotes de rede (`TCP`/`UDP`/`ICMP`), `SNMP`, `MIB`, registos **`NetFlow`** de *routers*. |

---

## Perguntas de revisão

1. **Porque é que um `HIDS` consegue detetar ataques envolvendo comunicações cifradas fim-a-fim quando um `NIDS` falha?**

> [!success]- Ver Resposta
> Porque o `NIDS` observa apenas pacotes em trânsito na rede (onde o *payload* está cifrado), enquanto o `HIDS` reside no próprio *host* e inspeciona eventos locais após a decifragem, incluindo *logs* de sistema/aplicação, APIs e chamadas de sistema (*system calls*).

2. **Qual a principal razão para utilizar um *Hybrid IDS*?**

> [!success]- Ver Resposta
> Um *Hybrid IDS* combina `SIDS` e `AIDS` para aliar a baixa taxa de falsos alarmes e precisão do `SIDS` em ataques conhecidos à capacidade do `AIDS` de detetar ataques *zero-day* desconhecidos.

## Notas relacionadas

- [[IDS - Métricas de Desempenho, Técnicas de Evasão e Desafios (Khraisat)]]
- [[Zero Trust Architecture (NIST SP 800-207) - Fundamentos, Componentes Lógicos e Planos]]
- [[Ataques e Contramedidas por Camada em IoT (Sharma)]]
