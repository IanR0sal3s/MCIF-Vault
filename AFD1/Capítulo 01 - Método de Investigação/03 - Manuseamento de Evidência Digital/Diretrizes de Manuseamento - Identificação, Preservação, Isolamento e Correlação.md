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
atualizado: 2026-10-19
---

# Diretrizes de Manuseamento — Identificação, Preservação, Isolamento e Correlação

As diretrizes práticas de manuseamento de evidência digital desdobram-se em cinco pilares: **1. Identificação** (compreender estados, fontes, localizações e tipos de dados), **2. Preservação** (proteger os originais, respeitar a **Ordem de Volatilidade** de 7 níveis e realizar triagem apenas sob autorização legal), **3. Isolamento** (analisar dados suspeitos em máquinas virtuais e redes isoladas), **4. Correlação** (cruzar artefactos com fontes independentes para detetar manipulações temporais) e **5. Registo (*Log*)**.

---

## 1 — Identificação (*Identification*)

### Estados dos Dados (*Data States*)
* **Armazenados (*stored*)**: dados guardados permanentemente num dispositivo de armazenamento (ex.: disco rígido).
* **Em trânsito (*in transit*)**: dados a serem enviados através de uma rede local ou da Internet para um dispositivo recetor.
* **Em receção (*in reception*)**: dados a serem recebidos num dispositivo, mas ainda não disponíveis para o utilizador.
* **Em criação (*in creation*)**: dados a serem produzidos localmente e apenas parcialmente disponíveis para o utilizador.

### Fontes de Dados (*Data Sources*)
* **Dispositivos de armazenamento (*storage devices*)**: discos rígidos (HDD), SSD, pen drives USB, fitas magnéticas (*tapes*), etc.
* **Localizações temporárias (*temporary location*)**: memória RAM, ficheiros de paginação (*page files*), partições de *swap*, ficheiros de *cache*, etc.
* **Dispositivos periféricos (*peripheral devices*)**: impressoras, *plotters*, leitores de cartões de memória, etc.
* **Dispositivos de rede ativos (*active network devices*)**: *switches*, *routers*, *modems*, servidores de impressão (*print servers*), etc.

### Localização Lógica e Física e Principais Tipos de Dados
* **Localização lógica e física**:
  * Dispositivos locais ou remotos.
  * Sistemas de armazenamento dedicados (habitualmente em centros de dados / *data centers*).
  * Sistemas computacionais (ex.: PC, portátil), que possuem pelo menos um dispositivo de armazenamento.
* **Principais tipos de dados (*main data types*)**:
  * **Simples e legíveis por humanos (*simple and human readable*)**: ex.: fotografias, documentos de texto, folhas de cálculo (*spreadsheets*).
  * **Complexos e/ou estruturados (*complex and/or structured data*)**: ex.: bases de dados, sistemas de ficheiros.
  * **Dados em bruto / fluxos (*raw data, streams of data*)**.

---

## 2 — Preservação (*Preservation*)

### Regras Fundamentais para Não Modificar Dados
* **Copiar dados importantes**, guardar o original num local seguro e **analisar sempre a cópia**, de modo a poder restaurar o original caso a cópia seja modificada.
* **Calcular valores de *hash*** dos dados importantes para provar posteriormente que não foram alterados — **melhor ainda se for realizada uma assinatura digital**.
* **Utilizar um dispositivo bloqueador de escrita (*write-blocking device*)** durante procedimentos que possam escrever nos dados suspeitos.
* **Minimizar o número de ficheiros criados durante uma análise *live***, pois novos ficheiros podem sobrescrever evidências residentes no espaço não alocado (*unallocated space*).
* **Ter extremo cuidado ao abrir ficheiros numa análise *live***, pois essa ação pode modificar metadados, tais como a data/hora do último acesso (*last access time*).

### Ordem de Volatilidade (*Order of Volatility*)
Na recolha de evidências, deve dar-se prioridade aos dados mais voláteis para os menos voláteis:

| Prioridade | Nível de Volatilidade (do mais volátil ao menos volátil) |
| :---: | :--- |
| **1** | Conteúdo do **CPU, *cache* e registos (*registers*)** |
| **2** | **Tabela de encaminhamento (*routing table*), *cache* ARP, tabela de processos, estatísticas do *kernel*** |
| **3** | Memória **RAM** |
| **4** | **Sistema de ficheiros temporário, espaço de *swap*** |
| **5** | **Dados em suportes de armazenamento local** (*local storage media*) |
| **6** | **Dados registados remotamente** (*remotely logged data*) |
| **7** | **Dados contidos em suportes de arquivo (*archival media / backups*)** |

### Triagem (*Sorting / Data Sorting*)
* Por vezes não é possível transportar todos os dispositivos para o laboratório devido a várias restrições: **legais, de tempo, inexequibilidade técnica**, etc.
* > [!WARNING] Condição Legal para Triagem (*Data Sorting*)
  > Nestas situações é necessária uma **pré-análise (*pre-analysis*)**, mas esta **só pode ser realizada se for devidamente autorizada de acordo com as leis do país**.

---

## 3 — Isolamento (*Isolate*)

* **Isolar o sistema do investigador dos dados suspeitos**, uma vez que se desconhece o que esses dados podem fazer:
  * Um **executável** oriundo do sistema suspeito pode apagar todos os ficheiros do computador do perito ou comunicar com um sistema remoto.
  * Abrir um **ficheiro HTML** do sistema suspeito pode fazer com que o navegador Web do perito execute *scripts* e descarregue ficheiros de um servidor remoto.
* **Criar um ambiente isolado**:
  * Utilizar **máquinas virtuais** (*VMware*, *VirtualBox*, *Xen*, etc.).
  * Utilizar uma **rede de análise** desconectada do mundo exterior, ou protegida por uma *firewall* que permita apenas conectividade estritamente limitada.
  * O isolamento é muito difícil, ou mesmo impossível, durante uma análise *live*.

---

## 4 — Correlação (*Correlate*)

* **Correlacionar dados com outras fontes independentes**:
  * Ajuda a reduzir o risco de **dados forjados (*forged data*)**.
  * Os marcadores temporais (*timestamps*) podem ser facilmente alterados na maioria dos sistemas.
  * Deve-se procurar entradas de registo (*log entries*), tráfego de rede ou outros eventos que confirmem os tempos de atividade dos ficheiros.
* > [!NOTE] Esforço Computacional
  > Esta tarefa é muito morosa (*time consuming*), especialmente se for realizada sem o auxílio de software especializado.

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

- Quais são os quatro estados possíveis dos dados na fase de Identificação?
- Qual é a sequência exata dos 7 níveis da Ordem de Volatilidade?
- Porque se deve minimizar a criação e abertura de ficheiros durante uma análise *live*?
- Que riscos concretos existem ao inspecionar executáveis ou ficheiros HTML de um sistema suspeito fora de um ambiente isolado?

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
