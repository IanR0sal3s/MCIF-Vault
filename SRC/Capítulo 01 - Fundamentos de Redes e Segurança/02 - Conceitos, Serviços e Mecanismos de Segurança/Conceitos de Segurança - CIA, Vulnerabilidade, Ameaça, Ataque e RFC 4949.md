---
title: Conceitos de Segurança - CIA, Vulnerabilidade, Ameaça, Ataque e RFC 4949
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Segurança em Redes de Computadores
sigla_uc: SRC
capitulo: 1
bloco: 2
fonte_aula: 1_fundamentals.pdf (Slides 14–20); ch1_Computer_Network_Security_Concepts.pdf (Secções 1.1–1.3)
tags:
  - src
  - seguranca
  - cia
  - rfc4949
  - nist
aliases:
  - Tríade CIA
  - Vulnerabilidade Ameaça Ataque
  - Ataques Passivos e Ativos
atualizado: 2026-11-15
---

# Conceitos de Segurança — CIA, Vulnerabilidade, Ameaça, Ataque e RFC 4949

A segurança em redes visa preservar a **confidencialidade, integridade e disponibilidade (CIA)** dos recursos de um sistema de informação através da identificação rigorosa de ativos, vulnerabilidades, ameaças e ataques.

> [!TIP] Lógica de Funcionamento e Valor de Segurança
> * **Porque existe (Norma)**: Distinções imprecisas entre falha técnica, risco potencial e ação hostil dificultam a análise de risco e a resposta a incidentes; normas como o NIST e a `RFC 4949` uniformizam o vocabulário.
> * **Porque importa (Segurança)**: Permite mapear cenários concretos (ex.: câmara de rede exposta com password por omissão) em controlos técnicos adequados e distinguir ataques detetáveis por alteração de dados (ativos) de ataques silenciosos (passivos).
> * **Pontos Críticos e Armadilhas para Exame**:
>   * Uma **vulnerabilidade** pode existir antes de qualquer exploração; um **ataque** é uma tentativa deliberada e **pode falhar**.
>   * **Ataques passivos** (ex.: *sniffing*, análise de tráfego, *taps*) **não alteram os dados** e são difíceis de detetar (prevenção via cifragem); **ataques ativos** (ex.: *spoofing*, `DoS`, alteração de mensagens) **modificam ou perturbam dados/fluxos** (foco em deteção e recuperação).

---

## 1. Definição NIST e Objetivos de Segurança (CIA+)

Segundo o **NIST**, *Computer Security* é a proteção conferida a um sistema de informação automatizado para atingir os objetivos aplicáveis de preservar a **integridade**, **disponibilidade** e **confidencialidade** dos recursos do sistema (hardware, software, firmware, informação/dados e telecomunicações).

| Propriedade | Definição |
| :--- | :--- |
| **Confidencialidade (*Confidentiality*)** | Prevenir a divulgação não autorizada de informação (inclui privacidade de dados e de fluxos). |
| **Integridade (*Integrity*)** | Proteger informação e sistemas contra modificação ou destruição imprópria (integridade de dados e de sistema). |
| **Disponibilidade (*Availability*)** | Garantir acesso atempado e fiável à informação e aos serviços. |
| **Autenticidade (*Authenticity*)** | Confiança de que uma entidade ou a origem da informação é genuína. |
| **Responsabilização (*Accountability*)** | Capacidade de rastrear ações até à entidade responsável. |

---

## 2. Vulnerabilidade, Ameaça e Ataque (Cenário Prático)

| Conceito | Definição | Exemplo na Aula (Câmara de Rede no Laboratório) |
| :--- | :--- | :--- |
| **Ativo (*Asset*)** | Recurso com valor a proteger | A câmara de rede, o *feed* de vídeo e a sua configuração |
| **Vulnerabilidade (*Vulnerability*)** | Fraqueza num sistema, configuração ou procedimento que pode ser explorada ou acionada | A interface de administração está acessível a partir da Internet e mantém a password por omissão |
| **Ameaça (*Threat*)** | Potencial de dano — circunstância ou evento que pode comprometer o sistema ou informação | Um agente externo pode assumir o controlo da conta de administração |
| **Ataque (*Attack*)** | Tentativa deliberada e intencional de comprometer a segurança (pode falhar) | Alguém submete as credenciais por omissão para obter acesso não autorizado |
| **Impacto possível** | Consequência da materialização da ameaça | Exposição de vídeo, alterações não autorizadas de configuração ou interrupção da gravação |

---

## 3. Ataques Passivos vs. Ataques Ativos (`RFC 4949` / Stallings)

| Tipo de Ataque | Característica Central | Exemplos | Estratégia Principal |
| :--- | :--- | :--- | :--- |
| **Passivo** | **Sem alteração de dados**; o atacante observa ou monitoriza transmissões | Análise de tráfego (*traffic analysis*), *sniffing*, *taps* | **Prevenção** (ex.: cifragem), pois é difícil de detetar |
| **Ativo** | **Com alteração de dados** ou perturbação do fluxo normal | *Spoofing* (mascaramento), `DoS` (negação de serviço), alteração/repetição de mensagens | **Deteção e recuperação**, complementadas por prevenção |

---

## Perguntas de revisão

1. **Qual a diferença prática entre vulnerabilidade, ameaça e ataque no cenário de uma câmara de rede com password por omissão exposta à Internet?**

> [!success]- Ver Resposta
> A **vulnerabilidade** é a fraqueza técnica/de configuração (interface exposta com password por omissão); a **ameaça** é o potencial dano (tomada de controlo não autorizada da câmara); o **ataque** é a ação deliberada de alguém tentar iniciar sessão com essas credenciais (que pode ter sucesso ou falhar).

2. **Porque é que os ataques passivos exigem sobretudo prevenção enquanto os ativos exigem deteção e recuperação?**

> [!success]- Ver Resposta
> Como os ataques passivos (*sniffing*, análise de tráfego) não alteram os dados nem deixam vestígios óbvios na transmissão, são difíceis de detetar, tornando a prevenção (cifragem) prioritária; já os ataques ativos alteram mensagens ou degradam serviços, podendo ser detetados e mitigados com mecanismos de deteção e recuperação.

## Notas relacionadas

- [[Modelo TCP-IP, Encapsulamento e Visibilidade de Tráfego HTTPS]]
- [[Serviços e Mecanismos de Segurança (ITU-T X.800)]]
- [[Princípios Fundamentais de Desenho Seguro, Attack Surfaces e Attack Trees]]
