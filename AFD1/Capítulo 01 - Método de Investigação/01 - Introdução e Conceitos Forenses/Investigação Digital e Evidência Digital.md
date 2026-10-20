---
title: Investigação Digital e Evidência Digital
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Análise Forense Digital I
sigla_uc: AFD1
capitulo: 1
bloco: 1
fonte_aula: MCIF – Digital Forensic Analysis 1 - Investigation Method.pdf
tags:
  - afd1
  - forense
  - investigacao-digital
  - evidencia-digital
  - metodo-cientifico
aliases:
  - Investigação Digital
  - Evidência Digital
  - Digital Investigation
  - Digital Evidence
atualizado: 2026-10-19
---

# Investigação Digital e Evidência Digital

A **investigação digital** aplica o **método científico** à análise de dispositivos digitais envolvidos num incidente ou crime, formulando hipóteses a partir dos vestígios recolhidos e procurando ativamente evidências adicionais capazes de **refutar** (mostrar como impossíveis) essas hipóteses. A **evidência digital** é qualquer objeto digital que contenha informação fidedigna que suporte ou refute uma hipótese, devendo ser **admissível, autêntica, precisa e completa**.

---

## Foco da Investigação Digital

Uma investigação digital incide sobre dispositivos digitais envolvidos num incidente ou crime, nomeadamente quando o dispositivo foi utilizado para:
1. **Cometer um crime físico**: por exemplo, um suspeito que utiliza a Internet para realizar pesquisas preparatórias sobre um crime físico.
2. **Executar um evento digital que viola uma política ou lei**: por exemplo, um atacante que obtém acesso não autorizado a um computador, um utilizador que descarrega material de contrabando ou que envia mensagens de correio eletrónico ameaçadoras.

Quando a violação é detetada, inicia-se a investigação para responder às questões fundamentais:
* **O quê** (*what*), **quem** (*who*), **quando** (*when*) e **como** (*how*).
* Em alguns casos, também **onde** (*where*) e **porquê** (*why*).

---

## A Investigação Digital como Método Científico

Uma investigação digital consiste num processo estruturado de desenvolvimento e teste de hipóteses para responder a questões sobre eventos digitais:
* Baseia-se no **método científico**.
* O investigador desenvolve uma **hipótese** utilizando as evidências inicialmente encontradas.
* De seguida, **testa a hipótese** procurando evidências adicionais que demonstrem que a hipótese é **impossível** (princípio da refutabilidade).

---

## Conceito e Requisitos da Evidência Digital

> [!IMPORTANT] Definição de Evidência Digital (*Digital Evidence*)
> É um objeto digital que contém informação **fidedigna** (*reliable*) que suporta ou refuta uma hipótese. Para ter valor probatório, a evidência digital tem obrigatoriamente de ser:
> * **Admissível** (*admissible*)
> * **Autêntica** (*authentic*)
> * **Precisa / Exata** (*accurate*)
> * **Completa** (*complete*)

Complementarmente, a evidência digital define-se como:
* Informação armazenada ou transmitida em formatos ou suportes digitais, cujo conteúdo constitui prova — quer **material**, quer meramente **indicativa** — de um determinado incidente ou evento.
* Por ser intrinsecamente **frágil e volátil**, exige a intervenção de um **perito certificado** (*certified expert*) para assegurar que os dados com valor probatório são eficazmente isolados e extraídos de forma correta e legal (*lawfully*).

---

## Desafios da Evidência Digital

1. **Difícil de controlar (*Hard to control*)**: é extremamente fácil criar, modificar, transmitir ou apagar dados num curto espaço de tempo.
2. **Diversidade e complexidade (*Diversity and complexity*)**: por vezes é difícil identificar as evidências digitais devido à rápida evolução dos sistemas de informação.

---

## Implicações Forenses

* **Evitar o Viés de Confirmação**: O rigor científico exige que o perito não procure apenas artefactos que confirmem a sua teoria inicial, mas tente refutá-la através de fontes independentes (como registos de firewall, logs de rede ou a [[Matriz de Correlação Forense e Cronologia de Ativação dos Artefactos|correlação cruzada de artefactos do sistema operativo]]).
* **Fragilidade Probatória**: Qualquer manuseamento incorreto sem isolamento e preservação adequados pode invalidar a autenticidade ou a admissibilidade da prova em sede judicial.

---

## Além da aula

* **Materialização das Questões Fundamentais em Sistemas Windows ([[00 ASSI|ASSI]])**: Na análise prática de um posto de trabalho Windows, as questões científicas desta fase mapeiam-se diretamente na [[Taxonomia dos Artefactos de Execução no Windows]]:
  * **O quê (*what*) e Quando (*when*)**: comprovados por artefactos de sistema como [[Serviço Prefetch e SysMain - Arquitetura e Funcionamento|Prefetch]] (últimas 8 execuções) e [[System Resource Usage Monitor (SRUM) - Arquitetura e Base ESE|SRUM]].
  * **Quem (*who*) e Como (*how*)**: apurados através de artefactos do perfil do utilizador (hive `NTUSER.DAT`/`USRCLASS.DAT`), tais como [[Artefacto Forense UserAssist|UserAssist]], [[Artefacto Forense ShellBags|ShellBags]], [[Jump Lists - Arquitetura, AppIDs e Carving|Jump Lists]] e [[Ficheiros LNK (Shell Links) - Metadados e Formato Binário|atalhos LNK]].
  * **Refutação de Hipóteses de Execução**: encontrar um executável registado na [[Application Compatibility e ShimCache (AppCompatCache)|ShimCache]] ou na [[AmCache - Arquitetura, Hives e Evolução para SQLite|AmCache]] prova apenas a *existência* do ficheiro no sistema, sendo insuficiente para sustentar a hipótese de que o programa foi *executado* (ver [[Extração da AmCache e Comparação Forense com a ShimCache]]).

---

## Perguntas de revisão

- Quais são as duas grandes categorias de utilização de um dispositivo digital num incidente ou crime?
- Porque se afirma que a investigação digital segue o método científico no teste de hipóteses?
- Quais são as quatro propriedades obrigatórias que a evidência digital deve cumprir?
- Quais são os dois principais desafios associados à natureza da evidência digital?

## Notas relacionadas

- [[Investigação Forense Digital - Análise Live vs Post-Mortem]]
- [[Fases da Investigação Forense Digital]]
- [[Princípios e Rota do Manuseamento de Evidência Digital]]
- [[Taxonomia dos Artefactos de Execução no Windows]]
- [[Matriz de Correlação Forense e Cronologia de Ativação dos Artefactos]]
- [[Extração da AmCache e Comparação Forense com a ShimCache]]
- [[Capítulo 1 - Método de Investigação]]
