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
atualizado: 2026-11-11
---

# Investigação Forense Digital — Análise Live vs. Post-Mortem

A **investigação forense digital** impõe requisitos legais para aceitação em tribunal, dividindo-se entre **análise live** (sobre o sistema ativo e a RAM) e **análise post-mortem** (em laboratório isolado).

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Método / Sistema)**: Desligar um equipamento preserva o disco mas destrói o conteúdo volátil da memória RAM; manter a máquina ligada permite aceder a processos e chaves em claro, mas submete a recolha à mediação de um sistema potencialmente comprometido.
> * **Porque importa (Forense / Tribunal)**: Define quando se deve capturar primeiro o estado volátil ou avançar para aquisição estática controlada em laboratório, garantindo que as teorias construídas cumprem os critérios legais de prova judicial.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Regra geral de preferência**: a **análise *post-mortem*** é a mais ideal do ponto de vista pericial por usar ferramentas e sistema operativo de confiança em ambiente isolado, mas nem sempre é exequível.
>   * **Risco da *Live Analysis***: *rootkits* ou software malicioso no sistema investigado podem ocultar ou falsificar os dados devolvidos pelas ferramentas.
>   * **Perda na RAM em *Post-Mortem***: chaves criptográficas residentes apenas em memória perdem-se ao desligar o sistema.

---

## Definição de Investigação Forense Digital

* **Significado de *Forensic***: possui requisitos legais específicos para ser aceite num tribunal de justiça.
* **Relação com a Investigação Digital**: Uma investigação forense digital é uma forma mais restrita de [[Investigação Digital e Evidência Digital|investigação digital]].

> [!IMPORTANT] Definições Clássicas
> * **Definição de Brian Carrier (2005)**: *"Processo que utiliza a ciência e a tecnologia para analisar objetos digitais e que desenvolve e testa teorias, as quais **podem ser apresentadas num tribunal de justiça**, para responder a questões sobre eventos que ocorreram."*
> * **Definição complementar**: *"A inspeção sistemática e tecnológica de um sistema informático e do seu conteúdo com o objetivo de obter evidências de um crime ou de qualquer outra utilização sob investigação."*

---

## Comparação: Análise *Live* vs. Análise *Post-Mortem*

| Critério Técnico e Forense | Análise *Live* (*Live Analysis*) | Análise *Post-Mortem* (*Post-Mortem Analysis*) |
| :--- | :--- | :--- |
| **Ambiente e Ferramentas** | Utiliza o próprio sistema operativo e recursos do sistema sob investigação para procurar evidências | Utiliza aplicações de confiança num sistema operativo de confiança em **ambiente de laboratório** |
| **Acesso à Memória RAM** | **Vantagem**: permite obter dados da memória **RAM** de processos em execução | **Desvantagem**: a informação contida na **RAM é perdida** (ex.: chaves criptográficas necessárias para desencriptar ficheiros ou volumes) |
| **Controlo e Fiabilidade** | **Desvantagem**: risco de obter **informação falsa**, pois o software no sistema pode ocultar ou falsificar dados maliciosamente (ex.: *rootkits*) | **Vantagem**: ambiente **totalmente controlado** e isolado de interferências do sistema suspeito |
| **Invasividade sobre o Sistema** | A execução de utilitários altera o estado do sistema ativo (*Prefetch*, registos, *timestamps*) | Preserva os discos originais sem interferência da execução local do sistema suspeito |
| **Aplicabilidade Prática** | Necessária em servidores críticos de alta disponibilidade ou perante volumes cifrados abertos em RAM | Abordagem pericial ideal sempre que seja exequível desligar e examinar em laboratório |

> [!NOTE] Regra Geral de Escolha
> Uma análise *post-mortem* é mais ideal do ponto de vista pericial, mas nem sempre é possível na prática (por exemplo, em servidores críticos de alta disponibilidade ou perante volumes cifrados cujas chaves residem apenas em RAM).

---

## Caso de Estudo: Servidor Comprometido

Cenário: **Um servidor foi comprometido — como ocorreu o incidente e quem foi o autor?**

1. **Recolha de vestígios iniciais no servidor**:
   * Encontrar dados criados por eventos relacionados com o incidente.
   * Recuperar entradas de registos apagadas do servidor.
   * Localizar ferramentas de ataque deixadas no sistema.
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

## Além da aula

* **Impacto Prático de *Live* vs. *Post-Mortem* nos Artefactos do Windows ([[00 ASSI|ASSI]])**:
  * **Triagem *Live* e Invasividade**: Ferramentas como o [[LastActivityView e Reconstituição Temporal Live|LastActivityView]] ou utilitários de inspeção de [[Processos e linha de comandos no Windows|processos na linha de comandos]] (`tasklist`, `pslist`) permitem reconstruir rapidamente a atividade num sistema ligado, mas a sua própria execução altera o estado da máquina (gera entradas no [[Serviço Prefetch e SysMain - Arquitetura e Funcionamento|Prefetch]] e modifica timestamps).
  * **Artefactos Exclusivos da RAM ou de Persistência Diferida**: Na [[Estrutura e Hives do Windows Registry]], o hive `HKLM\HARDWARE` existe apenas em memória RAM volátil, e vistas como `HKCU` são pontes dinâmicas que, em análise *post-mortem*, obrigam a carregar manualmente os ficheiros brutos `NTUSER.DAT` e `USRCLASS.DAT` em analisadores como o [[Ferramentas de Análise e Extração do Registry|RegistryExplorer]].
  * **Perda de Dados no Corte Abrupto de Energia (*Pull the Plug*)**: Conforme documentado na [[Matriz de Correlação Forense e Cronologia de Ativação dos Artefactos]], desligar um computador da tomada para análise *post-mortem* impede a gravação das entradas da sessão corrente da [[Application Compatibility e ShimCache (AppCompatCache)|ShimCache]] (que reside em RAM até ao *shutdown* ordenado) e deixa a base ESE do [[System Resource Usage Monitor (SRUM) - Arquitetura e Base ESE|SRUM]] sem a descarga da última hora e em estado *Dirty Shutdown*.
  * **Ficheiros Bloqueados em Análise *Live***: Enquanto numa análise *post-mortem* os ficheiros `SYSTEM`, `SAM` ou `Amcache.hve` são lidos diretamente da imagem forense, numa análise *live* encontram-se bloqueados pelo *kernel*, exigindo o recurso a [[Acesso Forense e Montagem de Shadow Copies|Shadow Copies (VSS)]] ou acesso bruto ao volume.

---

## Perguntas de revisão

1. **O que distingue uma investigação forense digital de uma investigação digital genérica?**

> [!success]- Ver Resposta
> O termo **forense** implica requisitos legais específicos para que os resultados obtidos possam ser aceites num **tribunal de justiça**, tornando a investigação forense digital uma forma mais restrita da investigação digital.

2. **Segundo Brian Carrier, qual é a definição de investigação forense digital?**

> [!success]- Ver Resposta
> É o processo que utiliza a ciência e a tecnologia para analisar objetos digitais e que desenvolve e testa teorias, as quais podem ser apresentadas num tribunal de justiça, para responder a questões sobre eventos que ocorreram.

3. **Quais são as principais vantagens e desvantagens da análise *live* face à análise *post-mortem*?**

> [!success]- Ver Resposta
> A **análise *live*** permite aceder a dados voláteis na memória **RAM** de processos em execução (ex.: chaves de cifra), mas corre o risco de obter informação falsa ou ocultada por *rootkits* no sistema comprometido. A **análise *post-mortem*** oferece um ambiente totalmente controlado com ferramentas fidedignas em laboratório, mas perde toda a informação residente em **RAM**.

4. **No exemplo do servidor comprometido, de que forma a análise da *firewall* ilustra o método científico?**

> [!success]- Ver Resposta
> Ao verificar nos registos e na configuração da *firewall* que determinado tráfego de rede não poderia ter existido, o perito obtém evidência objetiva que **refuta** hipóteses iniciais impossíveis, aplicando o princípio científico da falsificabilidade.

## Notas relacionadas

- [[Investigação Digital e Evidência Digital]]
- [[Fases da Investigação Forense Digital]]
- [[Preservação do Sistema e Integridade de Dados]]
- [[Diretrizes de Manuseamento - Identificação, Preservação, Isolamento e Correlação]]
- [[LastActivityView e Reconstituição Temporal Live]]
- [[Estrutura e Hives do Windows Registry]]
- [[Application Compatibility e ShimCache (AppCompatCache)]]
- [[Matriz de Correlação Forense e Cronologia de Ativação dos Artefactos]]
- [[Acesso Forense e Montagem de Shadow Copies]]
- [[Processos e linha de comandos no Windows]]
- [[Capítulo 1 - Método de Investigação]]
