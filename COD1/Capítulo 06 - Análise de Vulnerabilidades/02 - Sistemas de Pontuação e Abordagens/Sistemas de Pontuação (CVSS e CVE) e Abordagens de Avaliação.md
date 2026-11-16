---
title: Sistemas de Pontuação (CVSS e CVE) e Abordagens de Avaliação
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Cibersegurança Ofensiva e Defensiva I
sigla_uc: COD1
capitulo: 6
bloco: 2
fonte_aula: 2026.27_MCIF_COD1_06_Analise_Vulnerabilidades.pdf (Slides 20–29)
tags: [cod1, cvss, cve, nvd, euvd, gestao-vulnerabilidades]
aliases: [CVSS v4.0, CVE, Abordagens de Avaliação]
criado: 2026-11-15
atualizado: 2026-11-16
---

# Sistemas de Pontuação (CVSS e CVE) e Abordagens de Avaliação

Os referenciais `CVE` (identificação padronizada) e `CVSS v4.0` (pontuação quantitativa de severidade) permitem classificar achados obtidos por diferentes abordagens e ferramentas de avaliação.

> [!TIP] Lógica de Funcionamento e Valor Operacional
> * **Porque existe (Sistema)**: Padroniza a comunicação técnica de vulnerabilidades entre fornecedores, scanners (`Nessus`/`OpenVAS`) e equipas de resposta.
> * **Porque importa (Pentesting / Segurança)**: Garante relatórios consistentes e permite priorizar a remediação com base em métricas auditáveis.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * Avaliação baseada em **árvore** (estratégia escolhida com info prévia do *sysadmin*) vs. **dedução** (inventaria protocolos/portos primeiro e deduz testes).
>   * Bases principais de CVE: **`MITRE` (`cve.org`)**, **`EUVD-ENISA`**, **`NVD-NIST`**, **`CVEdetails`** e **`MSRC`**.

## 1. Abordagens e Tipos de Ferramentas de Análise

O funcionamento base de um scanner de vulnerabilidades segue três etapas: **Localizar os nós** -> **Descobrir os serviços** -> **Verificar vulnerabilidades conhecidas**.

- **Modelo de Entrega:**
  - **Solução *product-based*:** Instalada na rede interna da organização com acesso aos espaços de endereçamento internos (se ficar apenas atrás da firewall, pode não detetar exposição externa).
  - **Solução *service-based*:** Fornecida por consultor externo, podendo combinar sensores externos e internos.
- **Estratégia de Análise:**
  - **Avaliação baseada em árvore:** O auditor seleciona estratégias/ferramentas diferentes por máquina ou componente (ex.: uma ferramenta para Windows e outra para Linux) com base em informação prévia do *sysadmin*.
  - **Avaliação baseada em dedução:** Começa por inventariar protocolos e portos associados aos serviços e, a partir dessa descoberta, seleciona automaticamente as verificações de vulnerabilidades por máquina.
- **Tipos de Ferramentas:** *Host-based* (SO, apps e serviços locais), *Profundidade* (procura falhas desconhecidas/0-day, ex.: **fuzzers**), *Application-layer* (web e bases de dados) e *Ativos/Passivos*.
- **Critérios de Seleção de Ferramentas:** tipos de vulnerabilidades suportados, quantidade/capacidade de testes, qualidade e precisão dos relatórios, eficiência/precisão de scanning, capacidade de criar novos testes (plugins/scripts) e agendamento de scans.

## 2. Sistemas de Identificação e Pontuação: `CVE` e `CVSS`

### Common Vulnerabilities and Exposures (`CVE`)
Fornece uma lista pública de identificadores únicos e descrições padronizadas para vulnerabilidades conhecidas (ex.: `CVE-YYYY-NNNNN`). Principais bases de consulta:
- **MITRE:** `cve.org`
- **EUVD (ENISA — União Europeia):** `euvd.enisa.europa.eu`
- **NVD (NIST):** `nvd.nist.gov`
- **CVEdetails:** `cvedetails.com`
- **Microsoft Security Response Center (MSRC):** `msrc.microsoft.com/update-guide`

### Common Vulnerability Scoring System (`CVSS v4.0`)
Framework aberta que fornece um modelo quantitativo para comunicar as características técnicas e o impacto de vulnerabilidades de TI (atualmente na versão **v4.0**), permitindo auditar exatamente os vetores usados no cálculo da pontuação:
- Calculadoras oficiais: `first.org/cvss/calculator` e `nvd.nist.gov/vuln-metrics/cvss/v4-calculator`
- Exemplos oficiais: `first.org/cvss/examples`

## Além da aula

> [!NOTE] Conteúdo Complementar (Além da aula)
> Como usar `CVSS` e `CVE` de forma realista num pentest organizacional:

- **CVSS Base Score não é Risco Final:** Uma vulnerabilidade com `CVSS 9.8` num servidor isolado sem dados sensíveis pode ter risco operacional menor do que uma falha `CVSS 6.5` num controlador de domínio ou portal exposto com credenciais fracas. Ajuste sempre a severidade no relatório considerando o **contexto ambiental** (*Environmental Metrics* do CVSS) e a existência de **exploits públicos ativos** (ex.: catálogo `KEV` da CISA / `EPSS`).

## Perguntas de revisão

1. **Qual a diferença entre uma avaliação baseada em *árvore* e uma baseada em *dedução*?**
   > [!success]- Ver Resposta
   > A avaliação baseada em **árvore** depende de informação prévia do administrador para escolher ferramentas/estratégias distintas por tipo de sistema (ex.: Windows vs. Linux), enquanto a baseada em **dedução** descobre primeiro os protocolos, portos e serviços em rede e só depois seleciona os testes aplicáveis a cada máquina.

2. **Para que servem os identificadores `CVE` em conjunto com o `CVSS`?**
   > [!success]- Ver Resposta
   > O `CVE` atribui um identificador único e padronizado a cada vulnerabilidade conhecida para facilitar a referência cruzada entre scanners, bases de dados (MITRE, NVD, EUVD) e patches, enquanto o `CVSS` quantifica a severidade técnica dessa vulnerabilidade de forma transparente.

## Notas relacionadas
- [[Análise e Gestão de Vulnerabilidades - Ciclo de Vida e Classificação]]
- [[Ferramentas de Análise - Nessus e OpenVAS (Instalação e Setup)]]
- [[Controlos de Segurança, Standards e Legislação (NIS 2, ISO 27001, NIST CSF)]]
