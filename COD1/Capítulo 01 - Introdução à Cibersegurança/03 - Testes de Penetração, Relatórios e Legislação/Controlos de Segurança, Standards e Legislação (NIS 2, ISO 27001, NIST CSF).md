---
title: Controlos de Segurança, Standards e Legislação (NIS 2, ISO 27001, NIST CSF)
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Segurança em Redes de Computadores
sigla_uc: COD1
capitulo: 1
bloco: 3
fonte_aula: 2026.27_MCIF_COD1_01_Introdução à Cibersegurança.pdf (Slides 49–57, 77–84)
tags:
  - cod1
  - nis2
  - iso27001
  - nist-csf
  - controlos-seguranca
aliases:
  - NIS 2
  - ISO 27001
  - NIST CSF
  - Segurança por Zonas
atualizado: 2026-11-15
---

# Controlos de Segurança, *Standards* e Legislação (`NIS 2`, `ISO 27001`, `NIST CSF`)

A postura defensiva de uma organização assenta em **políticas de segurança**, **segurança física**, **segmentação de rede por zonas** e **soluções técnicas** (`Firewall`, `IDS`/`IPS`, `EDR`/`XDR`, `SIEM`/`SOAR`), enquadradas por normas e legislação como `NIS 2` e `ISO/IEC 27001`.

> [!TIP] Lógica de Funcionamento e Valor Operacional
> * **Porque existe (Governação)**: Sem políticas formais e requisitos legais, os controlos técnicos são implementados de forma fragmentada; normas como `ISO 27001` e `NIS 2` estruturam a gestão contínua de risco.
> * **Porque importa (Pentesting)**: Conhecer a arquitetura por zonas (`Internet` $\rightarrow$ `DMZ` $\rightarrow$ `Produção`/`Intranet` $\rightarrow$ `Gestão`) e as soluções de deteção (`EDR`/`XDR`, `SIEM`) ajuda o *pentester* a compreender o que está a testar e a propor recomendações conformes com a regulação do cliente.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **`NIS 2`**: diretiva europeia que reforça a cibersegurança na UE, alarga setores abrangidos, exige gestão de riscos/incidentes e **responsabiliza diretamente a gestão de topo**.
>   * **`ISO/IEC 27001`**: norma para estabelecer, implementar, manter e melhorar um **ISMS** (*Information Security Management System*).

---

## 1. Controlos e Arquitetura Defensiva (Slides 49–57)

* ***Information Assurance***: garantia de integridade, disponibilidade, confidencialidade e autenticidade durante utilização, processamento, armazenamento e transmissão.
* **Políticas de Segurança**: base da infraestrutura de segurança (ex.: controlo de acessos, acesso remoto, gestão de firewall, *passwords*, contas de utilizador, segurança de e-mail).
* **Segurança Física**: primeira camada de proteção (contra ameaças ambientais — inundações, incêndios, sismos — e humanas — vandalismo, intrusão física).
* **Segurança da rede baseada em zonas**: separa a rede por níveis de confiança (**Internet, DMZ, Produção, Intranet, Gestão**).
* **Soluções de segurança**: *Firewall* / *vFirewall*, *Proxy* / filtro URL, `IDS`/`IPS`, `DLP`, `VPN`, `EDR`/`XDR`, `SIEM`/`SOAR`/análise de *logs*/`XSIAM`.

---

## 2. *Standards* e Legislação (Slides 78–84)

| Norma / Lei | Âmbito e Objetivo Principal |
| :--- | :--- |
| **`NIS 2`** | Diretiva da UE que alarga setores críticos, impõe medidas de gestão de risco, comunicação de incidentes e **responsabilidade da gestão de topo**. |
| **`ISO/IEC 27001`** | Requisitos para um **Sistema de Gestão da Segurança da Informação (`ISMS`)** adaptado ao contexto da organização. |
| **`NIST Cybersecurity Framework`** | Padrões e práticas flexíveis e prioritizadas para gestão de risco em infraestruturas críticas. |
| **`PCI-DSS`** | *Standard* proprietário obrigatório para entidades que processam, armazenam ou transmitem dados de **cartões de pagamento**. |
| **`HIPAA`** | Lei federal dos EUA para proteção de dados pessoais de **saúde** e seguros de saúde. |
| **Outros / Portugal** | `FISMA`, `COBIT`, `ITIL`, `CSIRT`; em Portugal: regime jurídico em `cncs.gov.pt/pt/regime-juridico/` e `cibercrime.net/legislacao`. |

---

## Perguntas de revisão

1. **Que zonas típicas compõem uma arquitetura de rede segmentada segundo os slides?**

> [!success]- Ver Resposta
> Zonas com diferentes níveis de confiança e controlo: **Internet**, **DMZ**, **Produção**, **Intranet** e **Gestão**.

2. **Qual a diferença de âmbito entre a `NIS 2` e o `PCI-DSS`?**

> [!success]- Ver Resposta
> A `NIS 2` é uma diretiva europeia transversal para reforço da cibersegurança, gestão de riscos e reporte de incidentes em setores essenciais/importantes da UE, enquanto o `PCI-DSS` é um *standard* setorial específico para organizações que lidam com cartões de pagamento.

## Notas relacionadas

- [[Testes de Penetração - Metodologia, Pentest Request e Relatórios]]
- [[Zero Trust Architecture (NIST SP 800-207) - Fundamentos, Componentes Lógicos e Planos]]
