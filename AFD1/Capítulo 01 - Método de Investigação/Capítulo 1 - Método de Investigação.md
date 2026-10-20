---
title: Capítulo 1 - Método de Investigação
tipo: indice
mestrado: Cibersegurança e Informática Forense
uc: Análise Forense Digital I
sigla_uc: AFD1
capitulo: 1
fonte_aula: MCIF – Digital Forensic Analysis 1 - Investigation Method.pdf
tags:
  - moc
  - afd1
  - forense
  - metodologia
  - evidencia-digital
  - labcif
aliases:
  - Capítulo 1 AFD1
  - Investigation Method
  - Método de Investigação Forense
atualizado: 2026-10-19
---

# Capítulo 1 — Método de Investigação (*Investigation Method*)

Índice temático e encadeamento pedagógico do **Capítulo 1 (*Investigation Method*)** da unidade curricular de [[00 AFD1|Análise Forense Digital I (AFD1)]], lecionada pelos docentes **Miguel Frade** e **Baltazar Rodrigues** (LabCIF).

As notas encontram-se organizadas em **4 blocos temáticos numerados** na pasta `AFD1/Capítulo 01 - Método de Investigação/`, cobrindo a totalidade dos 50 diapositivos da apresentação oficial.

---

## 1. Introdução e Conceitos Forenses (`01 - Introdução e Conceitos Forenses`)

| Nota | Descrição e Foco Técnico |
| :--- | :--- |
| [[Investigação Digital e Evidência Digital]] | Foco da investigação (crimes físicos vs. eventos digitais), questões fundamentais (*what, who, when, how, where, why*), método científico (formulação e refutação de hipóteses), propriedades da evidência digital (*admissible, authentic, accurate, complete*) e desafios (*hard to control*, *diversity and complexity*) |
| [[Investigação Forense Digital - Análise Live vs Post-Mortem]] | Requisito legal de admissibilidade em tribunal, definições formais (Brian Carrier), comparação entre **Live Analysis** e **Post-Mortem Analysis** (vantagens, desvantagens e perda de dados na RAM) e caso prático de servidor comprometido |

---

## 2. Metodologia de Investigação da Cena de Crime Digital (`02 - Metodologia de Investigação da Cena de Crime Digital`)

| Nota | Descrição e Foco Técnico |
| :--- | :--- |
| [[Fases da Investigação Forense Digital]] | As 4 fases cíclicas baseadas na investigação criminal física: **Preparação / Identificação da fonte**, **Preservação do sistema**, **Pesquisa de evidências** e **Reconstrução de eventos e relatório** |
| [[Preservação do Sistema e Integridade de Dados]] | Objetivos e técnicas de preservação em *post-mortem* (*pull the plug*, cópias, *write blockers*) e *live analysis* (suspensão de processos, hub/switch vazio, filtros de rede); famílias de *hash* criptográfico (`SHA-1/2/3`, `MD5/6`, `RIPEMD`, `Whirlpool`), colisões no `MD5` (quebrado desde 2004), vulnerabilidade do *hash* isolado ($H(M)=h$) e **Assinaturas Digitais** (Cartão de Cidadão) |
| [[Pesquisa de Evidências e Reconstrução de Eventos]] | Pesquisa orientada ao incidente (hábitos web vs. intrusão Linux), técnicas de pesquisa por nome, conteúdo, metadados temporais, base de *hashes* **NSRL (NIST)** e tráfego de rede; reconstrução de eventos (defesa de malware vs. ação do utilizador e impacto da versão do SO/aplicação) |
| [[Exercícios Práticos - Integridade de Dados e Hashes]] | Exercícios práticos (Slide 24): verificação automatizada em lote com `sha256sum` no Linux (`-c`), `HashCalc` no Windows e teste de inversão de *hashes* de palavras comuns no *CrackStation* |

---

## 3. Manuseamento de Evidência Digital (`03 - Manuseamento de Evidência Digital`)

| Nota | Descrição e Foco Técnico |
| :--- | :--- |
| [[Princípios e Rota do Manuseamento de Evidência Digital]] | Os 4 princípios fundamentais de manuseamento (*first responders*, acesso excecional qualificado, cadeia de custódia/repetibilidade e responsabilidade legal) e fluxograma completo da **Rota da Evidência Digital** |
| [[Diretrizes de Manuseamento - Identificação, Preservação, Isolamento e Correlação]] | Diretrizes 1 a 4: estados dos dados (*stored, in transit, in reception, in creation*), fontes e tipos de dados; regras de preservação, **Ordem de Volatilidade** (7 níveis) e **Triagem (*Data Sorting*)**; isolamento laboratorial (VMs e redes isoladas) e correlação multi-fonte |
| [[Registo, Etiquetagem e Fotografia Pericial (Regras LabCIF)]] | Diretriz 5 (*Log*): documentação de ações, receção em processos de grande escala (30+ suspeitos, 200+ dispositivos), **regras de etiquetagem do LabCIF** (`ownerID.deviceID[.inside_deviceID]`), **regras de fotografia pericial** (escala/régua, caixa 3D `Top/Bottom/Left/Right/Front/Back`, nomenclatura de ficheiros, erros comuns) e **templates de catalogação** (`PC01.HD03`, `DNS01`, `A.SPH01`) |

---

## 4. Ética Forense e Exercícios (`04 - Ética Forense e Exercícios`)

| Nota | Descrição e Foco Técnico |
| :--- | :--- |
| [[Código de Ética na Investigação Forense Digital (ISFCE)]] | Propósito do código de ética na proteção da integridade pericial e diretrizes da *International Society of Forensic Computer Examiners (ISFCE)* (*will always* vs. *will never*) |
| [[Exercício de Projeto - Catalogação e Etiquetagem de Dispositivos e Serviços]] | Guião do exercício de preparação para o Relatório do Projeto em Equipa (Slide 48): matriz de atributos para dispositivos e serviços (`web`, `DNS`, `POP3`, `IMAP`, `SMTP`, `SSH`), sistema de etiquetagem hierárquica e tabelas com fotografia pericial |

---

## 🧭 Navegação

* [[00 AFD1|Voltar ao Índice de AFD1]]
* [[Capítulo 3 - Organização de Dados|Avançar para o Capítulo 3 — Organização de Dados]]
* [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses|Pontes com ASSI — Capítulo 1 (Artefactos Forenses no Windows)]]
* [[Home|Voltar ao Hub Central do MCIF]]
