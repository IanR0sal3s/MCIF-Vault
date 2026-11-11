---
title: Diretrizes de Manuseamento - Identificação, Preservação, Isolamento e Correlação
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Análise Forense Digital I
sigla_uc: AFD1
capitulo: 1
bloco: 3
fonte_aula: MCIF – Digital Forensic Analysis 1 - Investigation Method.pdf
tags:
  - afd1
  - forense
  - handling
  - ordem-volatilidade
  - isolamento
  - correlacao
  - triagem
aliases:
  - Digital Evidence Handling Guidelines
  - Ordem de Volatilidade
  - Order of Volatility
  - Data Sorting
atualizado: 2026-11-11
---

# Diretrizes de Manuseamento — Identificação, Preservação, Isolamento e Correlação

As diretrizes operacionais de manuseamento organizam-se em cinco pilares — **Identificação**, **Preservação** (com a **Ordem de Volatilidade** de 7 níveis e **Data Sorting**), **Isolamento**, **Correlação** e **Registo**.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Método / Sistema)**: Os dados transitam por diferentes estados de persistência e artefactos suspeitos podem executar código destrutivo ou exibir *timestamps* falsificados; estas diretrizes ordenam a recolha do mais volátil para o mais persistente e isolam a estação forense.
> * **Porque importa (Forense / Tribunal)**: Recolher o disco antes da RAM destrói vestígios voláteis, criar ficheiros numa máquina ativa sobrescreve espaço não alocado e triar dados sem cobertura legal invalida a prova.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Ordem de Volatilidade (Níveis 1 a 7)**: recolher estritamente do mais volátil (**1. CPU/cache/registos** $\to$ **2. routing/ARP/processos/kernel** $\to$ **3. RAM**) até ao menos volátil (**7. suportes de arquivo/*backups***).
>   * **Triagem (*Data Sorting*) condicionada**: pré-analisar no local por limites de tempo, lei ou exequibilidade técnica **só é permitido com autorização legal**.
>   * **Perigo de ficheiros HTML suspeitos**: abrir um HTML fora de ambiente isolado pode disparar *scripts* no browser do perito e estabelecer ligações remotas.

---

## 1 — Identificação

### Estados e Principais Tipos de Dados

| Dimensão | Categorias e Exemplos |
| :--- | :--- |
| **Estados dos dados** | **Armazenados** (disco rígido); **Em trânsito** (rede local ou Internet); **Em receção** (a ser recebidos, ainda indisponíveis ao utilizador); **Em criação** (produzidos localmente, apenas parcialmente disponíveis) |
| **Tipos de dados** | **Simples e legíveis por humanos** (fotografias, documentos de texto, folhas de cálculo); **Complexos e/ou estruturados** (bases de dados, sistemas de ficheiros); **Dados em bruto / fluxos** |

### Fontes de Dados e Localização

* **Dispositivos de armazenamento**: discos rígidos (HDD), SSD, pen drives USB, fitas magnéticas, etc.
* **Localizações temporárias**: memória RAM, ficheiros de paginação, partições de *swap*, ficheiros de *cache*, etc.
* **Dispositivos periféricos**: impressoras, *plotters*, leitores de cartões de memória, etc.
* **Dispositivos de rede ativos**: *switches*, *routers*, *modems*, servidores de impressão, etc.
* **Localização lógica e física**: dispositivos locais ou remotos; sistemas de armazenamento dedicados (habitualmente em *data centers*); sistemas computacionais (ex.: PC, portátil) com pelo menos um dispositivo de armazenamento.

---

## 2 — Preservação

### Regras Fundamentais para Não Modificar Dados

* **Copiar dados importantes**, guardar o original num local seguro e **analisar sempre a cópia**, de modo a poder restaurar o original caso a cópia seja modificada.
* **Calcular valores de *hash*** dos dados importantes para provar posteriormente que não foram alterados — **melhor ainda se for realizada uma assinatura digital**.
* **Utilizar um *Write Blocker*** durante procedimentos que possam escrever nos dados suspeitos.
* **Minimizar o número de ficheiros criados durante uma análise *live***, pois novos ficheiros podem sobrescrever evidências residentes no **espaço não alocado** (*unallocated space*).
* **Ter extremo cuidado ao abrir ficheiros numa análise *live***, pois essa ação pode modificar metadados, tais como a data/hora do último acesso (*last access time*).

### Ordem de Volatilidade (*Order of Volatility*)

Na recolha de evidências, deve dar-se prioridade rigorosa dos dados **mais voláteis** para os **menos voláteis**:

| Prioridade | Nível de Volatilidade (Ordem Oficial) | Persistência / Risco de Perda | Exemplos Concretos |
| :---: | :--- | :--- | :--- |
| **1** | Conteúdo do **CPU, *cache* e registos** | Volatilidade extrema (ciclos de relógio) | Registos da CPU, linhas de *cache* L1/L2/L3 |
| **2** | **Tabela de encaminhamento, *cache* ARP, tabela de processos, estatísticas do *kernel*** | Estado dinâmico do SO em tempo real | Rotas ativas, mapeamentos MAC-IP, PIDs em curso |
| **3** | Memória **RAM** | Perde-se integralmente ao cortar a energia | Chaves de encriptação em claro, código injetado |
| **4** | **Sistema de ficheiros temporário e espaço de *swap*** | Sobrescrito continuamente em operação | `pagefile.sys`, `swapfile.sys`, `/tmp` |
| **5** | **Dados em suportes de armazenamento local** | Persistente, mas vulnerável a escritas locais | HDD, SSD, cartões de memória, pens USB |
| **6** | **Dados registados remotamente** | Dependente de políticas de retenção externas | Servidores de *syslog*, SIEM, *firewalls* remotas |
| **7** | **Dados contidos em suportes de arquivo (*backups*)** | Mais persistente e imutável a curto prazo | Fitas magnéticas, *snapshots* ou cópias *offline* |

### Triagem (*Data Sorting*)

* Por vezes não é possível transportar todos os dispositivos para o laboratório devido a várias restrições: **legais, de tempo, inexequibilidade técnica**, etc.

> [!WARNING] Condição Legal para Triagem (*Data Sorting*)
> Nestas situações é necessária uma **pré-análise**, mas esta **só pode ser realizada se for devidamente autorizada de acordo com as leis do país**.

---

## 3 — Isolamento

* **Isolar o sistema do investigador dos dados suspeitos**, uma vez que se desconhece o que esses dados podem fazer:
  * Um **executável** oriundo do sistema suspeito pode apagar todos os ficheiros do computador do perito ou comunicar com um sistema remoto.
  * Abrir um **ficheiro HTML** do sistema suspeito pode fazer com que o navegador Web do perito execute *scripts* e descarregue ficheiros de um servidor remoto.
* **Criar um ambiente isolado**:
  * Utilizar **máquinas virtuais** (*VMware*, *VirtualBox*, *Xen*, etc.).
  * Utilizar uma **rede de análise** desconectada do mundo exterior, ou protegida por uma *firewall* que permita apenas conectividade estritamente limitada.
  * O isolamento é muito difícil, ou mesmo impossível, durante uma análise *live*.

---

## 4 — Correlação

* **Correlacionar dados com outras fontes independentes**:
  * Ajuda a reduzir o risco de **dados forjados**.
  * Os marcadores temporais (*timestamps*) podem ser facilmente alterados na maioria dos sistemas.
  * Deve-se procurar entradas de registo, tráfego de rede ou outros eventos que confirmem os tempos de atividade dos ficheiros.

> [!NOTE] Esforço Computacional
> Esta tarefa é muito morosa, especialmente se for realizada sem o auxílio de software especializado.

---

## Implicações Forenses

* **Perigo de Visualização Direta de HTML**: Mesmo sem executar binários `.exe`, abrir um ficheiro `.html` apreendido numa estação de trabalho com acesso à Internet pode despoletar pedidos HTTP externos (imagens remotas, *JavaScript*), revelando o endereço IP do laboratório forense ao servidor do atacante e alterando o estado da prova.
* **Espaço Não Alocado em Análise *Live***: Guardar ferramentas de recolha ou o ficheiro de *dump* da RAM diretamente no disco rígido do sistema suspeito durante uma resposta *live* sobrescreve setores do espaço não alocado onde residiam ficheiros apagados cruciais.

---

## Além da aula

* **Mapeamento das Diretrizes de Manuseamento em Sistemas Windows ([[00 ASSI|ASSI]])**:
  * **1. Identificação e Fontes Temporárias/Estruturadas**: No Windows, os *dados complexos/estruturados* incluem os ficheiros de [[Estrutura e Hives do Windows Registry|Hives do Registry]] (`REGF`), bases de dados **ESE** (`Windows.edb` em [[Windows Search]], `SRUDB.dat` em [[System Resource Usage Monitor (SRUM) - Arquitetura e Base ESE]] e `qmgr.db` em [[Serviço BITS]]) e bases **SQLite** (`ActivitiesCache.db` em [[Windows Activity Timeline - Arquitetura e Base SQLite]]). Já as *localizações temporárias* abrangem o ficheiro de paginação de aplicações modernas `C:\swapfile.sys` ([[UWP - Artefactos Forenses e Estrutura de Dados]]), as caches gráficas ([[Caches de Ícones e Miniaturas (IconCache e Thumbcache)]]) e a área de transferência ([[Recuperação de Clipboard e Sincronização na Timeline]]).
  * **2. Preservação e Ordem de Volatilidade (Níveis 2 a 7)**:
    * **Nível 2 e 3 (Tabela de Processos e RAM)**: Processos ativos inspecionados via [[Processos e linha de comandos no Windows|`tasklist` / `pslist`]], hives voláteis (`HKLM\HARDWARE`) e a [[Application Compatibility e ShimCache (AppCompatCache)|ShimCache]] da sessão em curso.
    * **Nível 4 (Espaço de Swap)**: O ficheiro `swapfile.sys` das aplicações UWP ([[UWP - Artefactos Forenses e Estrutura de Dados]]).
    * **Nível 5 (Armazenamento Local)**: Artefactos persistidos em disco, cuja janela de gravação obedece à [[Matriz de Correlação Forense e Cronologia de Ativação dos Artefactos]] ($T_0 \to$ [[Artefacto Forense UserAssist|UserAssist]] $\approx 3\text{s} \to$ [[Serviço Prefetch e SysMain - Arquitetura e Funcionamento|Prefetch]] $\approx 10\text{s} \to$ [[System Resource Usage Monitor (SRUM) - Arquitetura e Base ESE|SRUM]] ao minuto 30).
    * **Nível 7 (Suportes de Arquivo / Backups)**: Cópias de sombra do [[Volume Shadow Service (VSS) - Arquitetura e Funcionamento|VSS]] e cópias de segurança do Registry em `RegBack` ([[Salvaguarda e Monitorização do Registry]]).
  * **4. Correlação Multi-Fonte**: Como os marcadores temporais padrão do sistema de ficheiros podem ser manipulados, a confirmação pericial num sistema Windows exige cruzar fontes independentes segundo a [[Matriz de Correlação Forense e Cronologia de Ativação dos Artefactos]] (por exemplo, cruzar a execução no [[Serviço Prefetch e SysMain - Arquitetura e Funcionamento|Prefetch]] com o consumo de rede/CPU no [[Análise Forense do SRUM e Ferramentas Nativas (powercfg)|SRUM]] e os metadados preservados em [[Ficheiros LNK (Shell Links) - Metadados e Formato Binário|atalhos LNK]] e [[Jump Lists - Arquitetura, AppIDs e Carving|Jump Lists]]).

---

## Perguntas de revisão

1. **Quais são os quatro estados possíveis dos dados na fase de Identificação?**

> [!success]- Ver Resposta
> **Armazenados** (guardados permanentemente num suporte), **Em trânsito** (em envio pela rede), **Em receção** (a ser recebidos, ainda indisponíveis ao utilizador) e **Em criação** (em produção local, apenas parcialmente disponíveis).

2. **Qual é a sequência exata dos 7 níveis da Ordem de Volatilidade?**

> [!success]- Ver Resposta
> Do mais volátil ao menos volátil: **1.** CPU, *cache* e registos; **2.** Tabela de encaminhamento, *cache* ARP, tabela de processos e estatísticas do *kernel*; **3.** Memória RAM; **4.** Sistema de ficheiros temporário e espaço de *swap*; **5.** Dados em suportes de armazenamento local; **6.** Dados registados remotamente; **7.** Dados contidos em suportes de arquivo (*backups*).

3. **Porque se deve minimizar a criação e abertura de ficheiros durante uma análise *live*?**

> [!success]- Ver Resposta
> Criar novos ficheiros pode sobrescrever evidências residentes no **espaço não alocado**, e abrir ficheiros pode alterar metadados como a data/hora do último acesso (*last access time*).

4. **Que riscos concretos existem ao inspecionar executáveis ou ficheiros HTML de um sistema suspeito fora de um ambiente isolado?**

> [!success]- Ver Resposta
> Um **executável** pode apagar ficheiros no computador do investigador ou comunicar com um servidor remoto; um **ficheiro HTML** pode executar *scripts* no navegador do perito e descarregar conteúdos externos, exigindo máquinas virtuais e redes isoladas.

## Notas relacionadas

- [[Princípios e Rota do Manuseamento de Evidência Digital]]
- [[Registo, Etiquetagem e Fotografia Pericial (Regras LabCIF)]]
- [[Preservação do Sistema e Integridade de Dados]]
- [[Matriz de Correlação Forense e Cronologia de Ativação dos Artefactos]]
- [[System Resource Usage Monitor (SRUM) - Arquitetura e Base ESE]]
- [[Análise Forense do SRUM e Ferramentas Nativas (powercfg)]]
- [[UWP - Artefactos Forenses e Estrutura de Dados]]
- [[Volume Shadow Service (VSS) - Arquitetura e Funcionamento]]
- [[Salvaguarda e Monitorização do Registry]]
- [[Capítulo 1 - Método de Investigação]]
