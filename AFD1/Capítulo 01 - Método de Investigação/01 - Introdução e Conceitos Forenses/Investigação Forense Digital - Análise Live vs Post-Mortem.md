---
title: Investigação Forense Digital - Análise Live vs Post-Mortem
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
  - live-analysis
  - post-mortem
  - brian-carrier
aliases:
  - Investigação Forense Digital
  - Live Analysis
  - Post-Mortem Analysis
  - Análise Live vs Post-Mortem
atualizado: 2026-10-19
---

# Investigação Forense Digital — Análise Live vs. Post-Mortem

O termo **forense** implica o cumprimento de requisitos legais para que os resultados possam ser aceites num tribunal (*court of law*), tornando a **investigação forense digital** uma forma mais restrita de investigação digital. Na recolha e exame de vestígios, distinguem-se duas abordagens: a **análise *live*** (executada sobre o sistema em funcionamento para aceder a dados voláteis na RAM, mas vulnerável a manipulação por software malicioso) e a **análise *post-mortem*** (realizada em ambiente laboratorial controlado com ferramentas fidedignas, sendo o método ideal sempre que exequível).

---

## Definição de Investigação Forense Digital

* **Significado de *Forensic***: possui requisitos legais específicos para ser aceite num tribunal de justiça.
* **Relação com a Investigação Digital**: Uma investigação forense digital é uma forma mais restrita de [[Investigação Digital e Evidência Digital|investigação digital]].

> [!IMPORTANT] Definições Clássicas
> * **Definição de Brian Carrier (2005)**: *"Processo que utiliza a ciência e a tecnologia para analisar objetos digitais e que desenvolve e testa teorias, as quais **podem ser apresentadas num tribunal de justiça**, para responder a questões sobre eventos que ocorreram."*
> * **Definição complementar**: *"A inspeção sistemática e tecnológica de um sistema informático e do seu conteúdo com o objetivo de obter evidências de um crime ou de qualquer outra utilização sob investigação."*

---

## Tipos de Análise para Encontrar Evidências

| Tipo de Análise | Definição | Vantagens | Desvantagens |
| :--- | :--- | :--- | :--- |
| **Análise *Live*** (*Live analysis*) | Utiliza o próprio sistema operativo ou outros recursos do sistema sob investigação para procurar evidências | Permite obter dados da memória **RAM** de processos em execução | Risco de obter **informação falsa**, pois o software no sistema pode ocultar ou falsificar dados maliciosamente (ex.: *rootkits*) |
| **Análise *Post-Mortem*** (*Post-mortem analysis*) | Utiliza aplicações de confiança (*trusted applications*) num sistema operativo de confiança em **ambiente de laboratório** | Ambiente **totalmente controlado** e isolado de interferências do sistema suspeito | A informação contida na **RAM é perdida** (ex.: chaves criptográficas necessárias para desencriptar um ficheiro ou volume) |

> [!NOTE] Regra Geral de Escolha
> Uma análise *post-mortem* é mais ideal do ponto de vista pericial, mas nem sempre é possível na prática (por exemplo, em servidores críticos de alta disponibilidade ou perante volumes cifrados cujas chaves residem apenas em RAM).

---

## Caso de Estudo: Servidor Comprometido

Cenário: **Um servidor foi comprometido — como ocorreu o incidente e quem foi o autor?**

1. **Recolha de vestígios iniciais no servidor**:
   * Encontrar dados criados por eventos relacionados com o incidente.
   * Recuperar entradas de registos (*log entries*) apagadas do servidor.
   * Localizar ferramentas de ataque (*attack tools*) deixadas no sistema.
   * Identificar as vulnerabilidades que existiam no servidor.
2. **Desenvolvimento de hipóteses**:
   * Com base nestes dados, formulam-se hipóteses sobre **qual a vulnerabilidade explorada** pelo atacante para ganhar acesso e **o que fez posteriormente**.
3. **Teste e refutação pela correlação de rede**:
   * Mais tarde, examinam-se a configuração e os registos da *firewall*.
   * Determina-se que alguns dos cenários das hipóteses iniciais são **impossíveis**, porque esse tipo de tráfego de rede não poderia ter existido através da *firewall*.
   * **Conclusão**: Foi encontrada evidência que **refuta** uma ou mais hipóteses iniciais.

---

## Implicações Forenses

* **Dilema da Volatilidade vs. Confiança**: Desligar imediatamente uma máquina preserva o disco contra alterações subsequentes (favorecendo a análise *post-mortem*), mas destrói irremediavelmente o estado da memória RAM (processos, ligações de rede ativas e chaves de cifra em claro).
* **Desconfiança do Sistema Operativo Comprometido**: Numa análise *live*, utilitários nativos do sistema suspeito (como `ps`, `ls`, `netstat` ou o Gestor de Tarefas) podem estar comprometidos por *rootkits* ao nível do utilizador ou do *kernel*, ocultando processos e ficheiros do atacante.

---

## Perguntas de revisão

- O que distingue uma investigação forense digital de uma investigação digital genérica?
- Segundo Brian Carrier, qual é a definição de investigação forense digital?
- Quais são as principais vantagens e desvantagens da análise *live* face à análise *post-mortem*?
- No exemplo do servidor comprometido, de que forma a análise da *firewall* ilustra o método científico?

## Notas relacionadas

- [[Investigação Digital e Evidência Digital]]
- [[Fases da Investigação Forense Digital]]
- [[Preservação do Sistema e Integridade de Dados]]
- [[Diretrizes de Manuseamento - Identificação, Preservação, Isolamento e Correlação]]
- [[Capítulo 1 - Método de Investigação]]
