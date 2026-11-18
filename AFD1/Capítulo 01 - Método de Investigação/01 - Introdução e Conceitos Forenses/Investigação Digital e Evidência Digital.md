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
atualizado: 2026-11-11
---

# Investigação Digital e Evidência Digital

A **investigação digital** aplica o método científico à formulação e refutação de hipóteses sobre incidentes, apoiando-se em **evidência digital** fidedigna, admissível, autêntica, precisa e completa.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Método / Sistema)**: Os sistemas informáticos registam vestígios de atividade humana e automática facilmente alteráveis; o método científico disciplina a análise impondo hipóteses testáveis e refutáveis em vez de suposições.
> * **Porque importa (Forense / Tribunal)**: Um artefacto digital só ganha valor probatório se satisfizer simultaneamente os quatro requisitos de qualidade da evidência (admissível, autêntica, precisa e completa) e resistir a tentativas ativas de refutação.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Princípio da refutabilidade**: testar uma hipótese implica procurar evidências adicionais que provem que ela é **impossível**, combatendo o viés de confirmação.
>   * **Quatro propriedades obrigatórias**: admissível, autêntica, precisa/exata e completa.
>   * **Natureza frágil e complexa**: dados criam-se, modificam-se ou apagam-se rapidamente, exigindo um perito certificado e atuação legal.

---

## Foco da Investigação Digital

Uma investigação digital incide sobre dispositivos digitais envolvidos num incidente ou crime, nomeadamente quando o dispositivo foi utilizado para:

1. **Cometer um crime físico**: por exemplo, um suspeito que utiliza a Internet para realizar pesquisas preparatórias sobre um crime físico.
2. **Executar um evento digital que viola uma política ou lei**: por exemplo, um atacante que obtém acesso não autorizado a um computador, um utilizador que descarrega material de contrabando ou que envia mensagens de correio eletrónico ameaçadoras.

Quando a violação é detetada, inicia-se a investigação para responder às questões fundamentais:

* **O quê**, **quem**, **quando** e **como**.
* Em alguns casos, também **onde** e **porquê**.

---

## A Investigação Digital como Método Científico

Uma investigação digital consiste num processo estruturado de desenvolvimento e teste de hipóteses para responder a questões sobre eventos digitais:

* Baseia-se no **método científico**.
* O investigador desenvolve uma **hipótese** utilizando as evidências inicialmente encontradas.
* De seguida, **testa a hipótese** procurando evidências adicionais que demonstrem que a hipótese é **impossível** (princípio da refutabilidade).

---

## Conceito e Requisitos da Evidência Digital

> [!IMPORTANT] Definição de Evidência Digital
> É um objeto digital que contém informação **fidedigna** que suporta ou refuta uma hipótese. Para ter valor probatório, a evidência digital tem obrigatoriamente de ser:
> * **Admissível**
> * **Autêntica**
> * **Precisa / Exata**
> * **Completa**

Complementarmente, a evidência digital define-se como:

* Informação armazenada ou transmitida em formatos ou suportes digitais, cujo conteúdo constitui prova — quer **material**, quer meramente **indicativa** — de um determinado incidente ou evento.
* Por ser intrinsecamente **frágil e volátil**, exige a intervenção de um **perito certificado** para assegurar que os dados com valor probatório são eficazmente isolados e extraídos de forma correta e legal.

---

## Desafios da Evidência Digital

| Desafio | Caracterização Técnica e Operacional |
| :--- | :--- |
| **Difícil de controlar** | É extremamente fácil criar, modificar, transmitir ou apagar dados num curto espaço de tempo. |
| **Diversidade e complexidade** | Torna-se difícil identificar evidências digitais devido à rápida evolução e heterogeneidade dos sistemas de informação. |

---

## Implicações Forenses

* **Evitar o Viés de Confirmação**: O rigor científico exige que o perito não procure apenas artefactos que confirmem a sua teoria inicial, mas tente refutá-la através de fontes independentes (como registos de firewall, logs de rede ou a [[Matriz de Correlação Forense e Cronologia de Ativação dos Artefactos|correlação cruzada de artefactos do sistema operativo]]).
* **Fragilidade Probatória**: Qualquer manuseamento incorreto sem isolamento e preservação adequados pode invalidar a autenticidade ou a admissibilidade da prova em sede judicial.

---

## Além da aula

* **Materialização das Questões Fundamentais em Sistemas Windows ([[00 ASSI|ASSI]])**: Na análise prática de um posto de trabalho Windows, as questões científicas desta fase mapeiam-se diretamente na [[Taxonomia dos Artefactos de Execução no Windows]]:
  * **O quê e Quando**: comprovados por artefactos de sistema como [[Serviço Prefetch e SysMain - Arquitetura e Funcionamento|Prefetch]] (últimas 8 execuções) e [[System Resource Usage Monitor (SRUM) - Arquitetura e Base ESE|SRUM]].
  * **Quem e Como**: apurados através de artefactos do perfil do utilizador (hive `NTUSER.DAT`/`USRCLASS.DAT`), tais como [[Artefacto Forense UserAssist|UserAssist]], [[Artefacto Forense ShellBags|ShellBags]], [[Jump Lists - Arquitetura, AppIDs e Carving|Jump Lists]] e [[Ficheiros LNK (Shell Links) - Metadados e Formato Binário|atalhos LNK]].
  * **Refutação de Hipóteses de Execução**: encontrar um executável registado na [[Application Compatibility e ShimCache (AppCompatCache)|ShimCache]] ou na [[AmCache - Arquitetura, Hives e Evolução para SQLite|AmCache]] prova apenas a *existência* do ficheiro no sistema, sendo insuficiente para sustentar a hipótese de que o programa foi *executado* (ver [[Extração da AmCache e Comparação Forense com a ShimCache]]).

---

## Perguntas de revisão

1. **Quais são as duas grandes categorias de utilização de um dispositivo digital num incidente ou crime?**

> [!success]- Ver Resposta
> Um dispositivo digital pode ser usado para **cometer um crime físico** (ex.: pesquisas preparatórias na Internet) ou para **executar um evento digital que viola uma política ou lei** (ex.: acesso não autorizado, descarga de material ilícito ou envio de emails ameaçadores).

2. **Porque se afirma que a investigação digital segue o método científico no teste de hipóteses?**

> [!success]- Ver Resposta
> Porque o investigador formula uma hipótese a partir dos vestígios iniciais e testa-a procurando ativamente evidências adicionais capazes de **demonstrar que essa hipótese é impossível** (princípio da refutabilidade), evitando confirmar apenas a teoria inicial.

3. **Quais são as quatro propriedades obrigatórias que a evidência digital deve cumprir?**

> [!success]- Ver Resposta
> A evidência digital deve ser **admissível**, **autêntica**, **precisa / exata** e **completa**, contendo informação fidedigna que suporte ou refute uma hipótese.

4. **Quais são os dois principais desafios associados à natureza da evidência digital?**

> [!success]- Ver Resposta
> É **difícil de controlar** (dados criam-se, modificam-se, transmitem-se ou apagam-se muito depressa) e apresenta grande **diversidade e complexidade** devido à rápida evolução dos sistemas de informação.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Capítulo 1 - Método de Investigação]] | Início do capítulo |
| **Seguinte** | [[Investigação Forense Digital - Análise Live vs Post-Mortem]] | `mesmo bloco` |
| **Índice** | [[Capítulo 1 - Método de Investigação]] · [[00 AFD1]] | `Bloco 01` |

### Conceitos Relacionados

* [[Fases da Investigação Forense Digital]] · `Bloco 02`
* [[Princípios e Rota do Manuseamento de Evidência Digital]] · `Bloco 03`
* [[Taxonomia dos Artefactos de Execução no Windows]] · `ASSI · Cap. 1`
* [[Matriz de Correlação Forense e Cronologia de Ativação dos Artefactos]] · `ASSI · Cap. 1`
* [[Extração da AmCache e Comparação Forense com a ShimCache]] · `ASSI · Cap. 1`
