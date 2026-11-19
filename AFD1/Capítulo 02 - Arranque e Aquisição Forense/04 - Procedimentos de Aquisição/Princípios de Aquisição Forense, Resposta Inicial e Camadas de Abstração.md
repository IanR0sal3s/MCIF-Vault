---
title: Princípios de Aquisição Forense, Resposta Inicial e Camadas de Abstração
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Análise Forense Digital I
sigla_uc: AFD1
capitulo: 2
bloco: 4
fonte_aula: MCIF – Digital Forensic Analysis 1 - Forensic Boot.pdf
tags:
  - afd1
  - forense
  - aquisicao
  - first-response
  - camadas-aquisicao
  - block-size
  - sector-size
  - hpa
  - dco
aliases:
  - Forensic Acquisition
  - Data Acquisition
  - Collecting Digital Evidence Flow Chart
  - Information Analysis Layers
  - Block Size vs Sector Size
atualizado: 2026-11-11
---

# Princípios de Aquisição Forense, Resposta Inicial e Camadas de Abstração

A aquisição forense preserva dados digitais segundo o protocolo de primeira intervenção, priorizando a camada física de ponta a ponta com blocos ajustados ao tamanho de setor do disco.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Método / Hardware)**: Erros na primeira intervenção (como reiniciar um servidor crítico ou copiar apenas ficheiros ativos) destroem provas voláteis e metadados de baixo nível, comprometendo a validade legal em tribunal.
> * **Porque importa (Forense)**: Seguir a árvore de decisão do DOJ garante o equilíbrio entre preservar a RAM e travar processos destrutivos; adquirir ao nível físico garante acesso a espaço não alocado, ficheiros apagados, tabela de partições e áreas ocultas **HPA/DCO**.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Árvore de Primeira Intervenção (U.S. DOJ)**: Desligado $\rightarrow$ não ligar e remover cabo; Ligado + rede empresarial $\rightarrow$ parar e chamar especialista; Ligado + processos destrutivos (`format`, `delete`, `remove`, `wipe`) $\rightarrow$ documentar/fotografar e cortar alimentação imediatamente.
>   * **4 Camadas de Abstração**: **Physical** > **Volume** > **File** > **Application** — *quanto mais elevada a camada de aquisição, menos informação pode ser recuperada*.
>   * **Tamanho de Bloco (`bs`)**: Blocos maiores aceleram a cópia, mas um único *bad sector* invalida o bloco inteiro; alinhar com o setor (`512 bytes` em HDD padrão, `4096 bytes` em *Advanced Format*; variável por marca/modelo/capacidade em SSD).

---

## 1. Enquadramento e Protocolo de Primeira Intervenção (*What to do if...*)

Na chegada à cena do crime digital, a atuação sobre o equipamento depende do seu estado elétrico e operacional (com base no guia *Electronic Crime Scene Investigation: A Guide for First Responders, Second Edition — U.S. Department of Justice*):

* **Se o computador estiver desligado** $\rightarrow$ **Remover o cabo de alimentação elétrica** e **NÃO ligar** o computador ou dispositivo.
* **Se o computador estiver ligado**:
  1. **Fotografar o ecrã** e documentar toda a informação visível com valor probatório.
  2. **Verificar se estão em execução processos destrutivos (*destructive processes*)**:
     * *Processos destrutivos*: quaisquer funções destinadas a obliterar dados no disco rígido ou dispositivo de armazenamento (termos visíveis no ecrã como `"format"`, `"delete"`, `"remove"` e `"wipe"` são indicadores de processos destrutivos e devem ser documentados no relatório).
     * **Se existirem processos destrutivos a correr** $\rightarrow$ **Remover imediatamente o cabo de alimentação elétrica**.
  3. **Realizar um *dump* da memória RAM e recolher o estado das ligações de rede**:
     * **Atenção**: esta operação **pode destruir ou contaminar evidências**, pelo que deve ser ponderada e executada por pessoal qualificado nas seguintes situações:
       * Quando **não é possível desligar um servidor** (ex.: ambiente empresarial em rede).
       * Para **obter palavras-passe ou chaves de cifragem armazenadas na RAM**.
       * Para **monitorizar atividades de rede de software malicioso**.

```mermaid
flowchart TD
    SCENE["Isolar a cena do crime e afastar pessoas<br/>dos computadores e dispositivos eletrónicos"] --> ON{"O computador<br/>está ligado?"}
    ON -->|NÃO| DONT["NÃO ligar o computador<br/>ou dispositivo"]
    DONT --> UNPLUG["Remover cabo de alimentação da traseira<br/>do computador e dispositivos ligados"]

    ON -->|SIM| TRAINED{"Há pessoal com formação<br/>específica em apreensão?"}
    TRAINED -->|NÃO| REQ["Solicitar assistência e seguir<br/>recomendações de pessoal qualificado"]
    TRAINED -->|SIM| NET{"É um ambiente empresarial<br/>em rede?"}
    NET -->|SIM| STOP["PARAR! NÃO desligar o computador.<br/>Contactar especialista em apreensão de rede"]
    NET -->|NÃO| DESTR{"Estão a correr processos<br/>destrutivos (format/delete/wipe)?"}
    DESTR -->|SIM| UNPLUG
    DESTR -->|NÃO| SCREEN{"Há informação com valor<br/>probatório visível no ecrã?"}
    SCREEN -->|SIM| PHOTO["Documentar exaustivamente e<br/>fotografar toda a informação no ecrã"]
    PHOTO --> UNPLUG
    SCREEN -->|NÃO| UNPLUG

    UNPLUG --> LABEL["Etiquetar todas as ligações nos computadores,<br/>dispositivos, cabos e fontes de alimentação"]
    LABEL --> DOC["Localizar, documentar, registar (log), fotografar<br/>e acondicionar todas as evidências para exame forense"]
```

---

## 2. Camadas de Análise e Aquisição em Suportes de Armazenamento

Os dados num suporte de armazenamento podem ser analisados e adquiridos em **quatro camadas de abstração**:

| Camada (do nível mais baixo ao mais alto) | Âmbito e Limitações Forenses |
| :--- | :--- |
| **1. Física (*Physical*)** | Abrange **desde o primeiro até ao último bit** do suporte de armazenamento. |
| **2. Volume (*Volume* / Lógica)** | Ao adquirir apenas ao nível do volume/partição, **não é possível obter setores não alocados (*unallocated sectors*), a tabela de partições (*partition table*) nem áreas ocultas (*hidden areas*)**. |
| **3. Ficheiro (*File*)** | Cópias de ficheiros individuais (ex.: ferramentas de *backup*), tornando **muito menos provável recuperar ficheiros apagados (*deleted files*)** ou espaço *slack*. |
| **4. Aplicação (*Application*)** | Cada aplicação possui a sua própria codificação ou formato de ficheiro interno. |

> [!IMPORTANT] Regra Fundamental da Camada de Aquisição
> **Quanto mais elevada for a camada de aquisição, menos informação poderá ser recuperada**.
> **Sempre que possível, a aquisição de dados deve ser realizada ao nível físico (*physical level*)**.
> *(Nota: Outros meios, como tráfego de rede e memória volátil RAM, possuem os seus próprios procedimentos recomendados específicos).*

---

## 3. Cópia de Suportes de Armazenamento: Tamanho de Bloco (*Block Size*) vs. Setor

Durante a cópia física de um suporte de armazenamento, a escolha do **tamanho de bloco de aquisição (*acquisition block size*)** envolve um compromisso direto entre velocidade e tolerância a erros de leitura:

* **Quanto maior for o tamanho do bloco (`bs`), mais rápida será a aquisição**.
* Contudo, **se existirem setores com erros (*bad sectors*), todo o bloco que contém o setor defeituoso ficará inválido**.

### Diretrizes de Configuração da Cópia Física

1. **Alinhamento do Tamanho de Bloco com o Tamanho do Setor**:
   * O tamanho de bloco de aquisição **deve coincidir com o tamanho do setor (*sector size*)** do dispositivo:
     * Para discos rígidos magnéticos (**HDD**), o tamanho padrão do setor é de **`512 bytes`** (ou `4096 bytes` em discos *Advanced Format* modernos).
     * Para unidades de estado sólido (**SSD**), o tamanho do setor/página **depende da marca, do modelo e da capacidade** da unidade.
2. **Abrangência Integral do Suporte**:
   * A aquisição de dados deve incluir a **totalidade do suporte de armazenamento (nível físico)**, abrangendo:
     * **Setores não alocados (*unallocated sectors*)**; e
     * **Áreas ocultas (*hidden areas*)**: **HPA (*Host Protected Area*)** ou **DCO (*Device Configuration Overlay*)** — caso existam, **recomendam-se 2 aquisições distintas**: uma primeira aquisição com a área oculta ativa (*in place*) e uma segunda aquisição com as áreas ocultas desativadas (*disabled*).

---

## Implicações Forenses

* **Consequência de um `bs` Excessivo em Discos Danificados**: Se um perito configurar `bs=1M` (1 Megabyte) num disco rígido antigo que tenha apenas 1 setor físico de `512 bytes` ilegível no meio desse megabyte, a ferramenta de aquisição descartará e preencherá com zeros a totalidade do bloco de `1 MB` (perdendo 2047 setores bons adjacentes!). Reduzir `bs=512` (ou usar ferramentas que reduzem automaticamente o bloco perante erros) limita a perda estritamente aos `512 bytes` defeituosos.
* **Articulação com as Regras LabCIF**: Os passos finais do fluxograma do DOJ (etiquetar todas as ligações, cabos e fontes de alimentação; documentar e fotografar) materializam-se diretamente nos procedimentos laboratoriais de etiquetagem e fotografia pericial ([[Registo, Etiquetagem e Fotografia Pericial (Regras LabCIF)]]).

---

## Além da aula

* **Correlação com as Camadas de Organização de Dados (Capítulo 3 de AFD1) e Artefactos de [[00 ASSI|ASSI]]**:
  * As 4 camadas de análise/aquisição (*Physical*, *Volume*, *File*, *Application*) espelham diretamente a arquitetura estudada em [[Camadas de Organização de Dados e Análise de Sistemas de Ficheiros]] no Capítulo 3 de AFD1.
  * Em **ASSI**, diversos procedimentos de recuperação forense dependem de dados que residem abaixo da camada de ficheiro ativo:
    * O acesso a snapshots anteriores através do [[Volume Shadow Service (VSS) - Arquitetura e Funcionamento|Volume Shadow Service (VSS)]] e [[Acesso Forense e Montagem de Shadow Copies]] opera ao nível de blocos de volume (*copy-on-write*), os quais se perdem numa simples cópia ao nível do ficheiro (*File layer*), mas são integralmente preservados numa aquisição física ou de volume.
    * O *carving* de registos eliminados em ficheiros [[Jump Lists - Arquitetura, AppIDs e Carving|Jump Lists]] ou de miniaturas órfãs em [[Caches de Ícones e Miniaturas (IconCache e Thumbcache)]] e a recuperação de ficheiros apagados no espaço não alocado exigem uma aquisição ao nível físico.
    * A recolha de processos e ligações num sistema *live* (quando o fluxograma indica não desligar a máquina) utiliza utilitários como `tasklist`, `pslist` e `netstat` estudados em [[Processos e linha de comandos no Windows]].

---

## Perguntas de revisão

1. **Perante um computador encontrado ligado na cena do crime, que verificação crítica deve ser feita no ecrã antes de decidir entre realizar um *memory dump* ou desligar imediatamente o cabo de alimentação?**

> [!success]- Ver Resposta
> Deve fotografar-se o ecrã, documentar a informação visível com valor probatório e verificar se existem **processos destrutivos** em execução (indicados por termos como `"format"`, `"delete"`, `"remove"` ou `"wipe"`). Se estiverem a correr processos destrutivos e não se tratar de um ambiente empresarial crítico que exija intervenção especializada de rede, deve **remover-se imediatamente o cabo de alimentação**.

2. **Em que três situações específicas se justifica realizar um *dump* de memória e recolha de estado de rede num sistema ligado, apesar do risco de contaminação?**

> [!success]- Ver Resposta
> 1. Quando **não é possível desligar um servidor** (ex.: ambiente empresarial em rede de alta disponibilidade).
> 2. Para **obter palavras-passe ou chaves de cifragem armazenadas na RAM**.
> 3. Para **monitorizar atividades de rede de software malicioso**.

3. **Quais são as quatro camadas de análise de informação num suporte de armazenamento e porque é que a aquisição deve ser feita, sempre que possível, ao nível físico?**

> [!success]- Ver Resposta
> De baixo para cima: **Physical** (Física), **Volume**, **File** (Ficheiro) e **Application** (Aplicação). Como **quanto mais elevada for a camada de aquisição, menos informação pode ser recuperada**, a aquisição deve ser realizada ao **nível físico** (do primeiro ao último bit), pois só assim se preservam a tabela de partições, os setores não alocados, o espaço *slack*, ficheiros eliminados e eventuais áreas ocultas (`HPA`/`DCO`).

4. **Qual é o compromisso entre velocidade e perda de dados na escolha do tamanho de bloco (`block size`) durante a aquisição de um disco com setores defeituosos?**

> [!success]- Ver Resposta
> Um tamanho de bloco maior acelera a aquisição, mas **um único setor defeituoso invalida o bloco inteiro** que o contém. Por isso, o tamanho de bloco deve coincidir com o tamanho do setor do dispositivo (`512 bytes` ou `4096 bytes` em HDDs; dependente de marca, modelo e capacidade em SSDs).

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Ferramentas Portáteis de Triagem, Pesquisa e FTK Imager Lite]] | `Bloco 03` |
| **Seguinte** | [[Procedimentos de Aquisição - Post-Mortem vs Live, Erros de Disco, HPA-DCO e Write Blockers]] | `mesmo bloco` |
| **Índice** | [[Capítulo 2 - Arranque e Aquisição Forense]] · [[00 AFD1]] | `Bloco 04` |

### Conceitos Relacionados

* [[Armazenamento da Aquisição - Clonagem vs Imagem, Formatos, Aquisição Remota e Assinatura de Hashes]] · `mesmo bloco`
* [[Investigação Forense Digital - Análise Live vs Post-Mortem]] · `Cap. 1`
* [[Fases da Investigação Forense Digital]] · `Cap. 1`
* [[Preservação do Sistema e Integridade de Dados]] · `Cap. 1`
* [[Princípios e Rota do Manuseamento de Evidência Digital]] · `Cap. 1`
* [[Diretrizes de Manuseamento - Identificação, Preservação, Isolamento e Correlação]] · `Cap. 1`
* [[Registo, Etiquetagem e Fotografia Pericial (Regras LabCIF)]] · `Cap. 1`
* [[Camadas de Organização de Dados e Análise de Sistemas de Ficheiros]] · `Cap. 3`
* [[Processos e linha de comandos no Windows]] · `ASSI · Cap. 1`
* [[Volume Shadow Service (VSS) - Arquitetura e Funcionamento]] · `ASSI · Cap. 1`
* [[Acesso Forense e Montagem de Shadow Copies]] · `ASSI · Cap. 1`
