---
title: Sanitização e Destruição de Discos Magnéticos (HDDs) - Wiping, Degaussing e Destruição Física
tipo: procedimento
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 2
bloco: 1
fonte_aula: System Administration - System and Data Management.pdf
tags:
  - assi
  - administracao-sistemas
  - data-disposal
  - sanitizacao
  - wiping
  - degaussing
  - eraser
  - dban
  - killdisk
  - diskmantler
aliases:
  - Sanitização de HDDs
  - Wiping e Degaussing
  - Eraser
  - Boot&Nuke
  - DBAN
  - Active KillDisk
  - DiskMantler
atualizado: 2026-11-11
---

# Sanitização e Destruição de Discos Magnéticos (HDDs) — Wiping, Degaussing e Destruição Física

A sanitização de **HDDs** abrange os níveis **Discarding**, **Clearing/Purging** e **Destroying**, combinando *wiping* por software (reutilizável), *degaussing* (1 min) e trituração física (`6–30 mm`).

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: Num disco magnético, eliminar ficheiros ou formatar apenas remove referências na tabela de alocação do sistema de ficheiros, mantendo os domínios magnéticos dos setores intactos nos pratos. A eliminação definitiva requer sobrescrever cada setor endereçável (*wiping*), colapsar o alinhamento magnético (*degaussing*) ou fragmentar mecanicamente os pratos.
> * **Porque importa (Segurança / Forense)**: A escolha do método define simultaneamente a recuperabilidade pericial residual e a viabilidade económica do hardware. Ferramentas como o `Eraser` visam especificamente apagar *Cluster Tip Area* (*slack space*) e *Alternate Data Streams*, enquanto um abate mal conduzido — como confiar na desmontagem pelo `DiskMantler` sem sanitização prévia — deixa os pratos magnéticos íntegros e recuperáveis em laboratório.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Reutilização após *Degaussing***: um **HDD nunca pode ser reutilizado** após *degaussing* porque o campo magnético destrói as pistas de servo-alinhamento de fábrica (`tracks`), exigindo formatação de baixo nível indisponível fora da fábrica; porém, **algumas fitas magnéticas (*tapes*) e disquetes** podem voltar a ser usadas;
>   * **Granulometria física**: trituração padrão de **`15–30 mm`** vs. **`6 mm`** para ativos críticos de categoria **`IL4`, `IL5` ou `IL6`**;
>   * **Armadilha do `DiskMantler`**: separa mecanicamente os componentes do HDD em cerca de **60 segundos** por vibração para reciclagem, mas **NÃO destrói os dados** nos pratos.

---

## 1. Os Três Níveis de Sanitização (Jones & Afrifa, 2020 — Slide 15)

Segundo a taxonomia de Jones & Afrifa (2020 — [JDFSL, Vol. 15, No. 1, Art. 2](https://doi.org/10.15394/jdfsl.2020.1615)), distinguem-se três níveis no tratamento de suportes de armazenamento:

| Nível | Designação | Descrição e Mecanismos Técnicos | Reutilização do HDD |
| :---: | :--- | :--- | :---: |
| **1** | **Discarding** | Nada é feito aos dados (o HDD é vendido, doado ou abandonado no estado atual). | Sim (**totalmente inseguro**) |
| **2** | **Clearing / Purging** | Destruição lógica ou magnética dos dados por **sobreposição (*overwriting*)**, *Secure Erase* ou *degaussing*. | **Sim** no *overwriting* / *Secure Erase*;<br>**Não** em HDDs após *degaussing* |
| **3** | **Destroying** | Destruição física do suporte (*shredding*, *melting*, *disintegration*, *crushing*). | **Não** (impossível reutilizar) |

---

## 2. Limpeza por Software (*Single / Multiple Pass Wipe* — Slide 16)

### 2.1. Princípio e Vantagem Económica
O *wiping* por software sobrescreve todos os setores endereçáveis do disco através de uma passagem única (*single pass wipe*) ou múltiplas passagens (*multiple pass wipe*). A sua principal vantagem é permitir que **as unidades de disco sejam reutilizadas ou revendidas** em segurança.

### 2.2. Ferramentas de Software para *Wiping*

1. **`Eraser`**:
   * Permite agendar tarefas (*Erase Schedule*) para ficheiros, pastas ou espaço livre, disponibilizando **seis métodos de limpeza (*Erasure methods*)**:
     * `Gutmann (35 passes)`
     * `US DoD 5220.22-M (8-306./E, C and E) (7 passes)`
     * `US DoD 5220.22-M (8-306./E) (3 passes)`
     * `Schneier's 7 pass`
     * `Pseudorandom Data (1 pass)`
     * `First and last 2KB of the file`
   * Suporta ainda opções dedicadas para limpeza da **`Cluster Tip Area`** (*slack space* no final do cluster) e de **`Alternate Data Streams`** (fluxos alternativos do sistema de ficheiros NTFS).
2. **`Boot&Nuke` (`DBAN` — *Darik's Boot and Nuke*)**: ambiente de arranque autónomo para sanitização integral de discos magnéticos.
3. **`CCleaner`**: integra o módulo *Drive Wiper* para limpeza do espaço livre ou do disco completo (1, 3, 7 ou 35 passagens).
4. **`KillDisk` (`Active@ KillDisk`)**: solução *freemium* com suporte para limpeza verificada e emissão formal de certificados de destruição.

---

## 3. Destruição da Drive: *Degaussing*, Trituração Física e `DiskMantler` (Slides 17–19)

### 3.1. Desmagnetização (*Degaussing* — Slide 17)

* **Funcionamento**: aplica um **campo magnético extremamente forte** ao disco rígido ou suporte magnético ([Data Security Inc. — Degausser](http://www.datasecurityinc.com/security/degausser.html)).
* **Desempenho e Conformidade**:
  * Rápido: **`1 ciclo = 1 minuto`**;
  * Cumpre as normas **NIST**, **PIPEDA**, **HIPAA** e **PCI DSS**;
  * **Mais eficiente energeticamente** do que a limpeza prolongada por software (*disk erasure*).
* **Impacto na Reutilização**:
  * **Após o *degaussing*, os HDDs NÃO podem voltar a ser utilizados**: as pistas de controlo e servo-alinhamento (**`tracks`**) gravadas na fábrica são destruídas, exigindo uma formatação a baixo nível com equipamento especial de fábrica indisponível ao utilizador;
  * **Exceção**: após o *degaussing*, **algumas fitas magnéticas (*tapes*) e disquetes (*floppy disks*) podem ser reutilizadas**;
  * *(Em suportes sólidos baseados em NAND Flash/SSDs, o degaussing não tem qualquer efeito).*

### 3.2. Destruição Física (*Disk Crusher* e *Super Shredder* — Slide 18)

* **Equipamentos**:
  * **Esmiuçador de discos (*Disk crusher*)**: perfura e dobra mecanicamente os pratos e o chassi;
  * **Super trituradora (*Super shredder*, ex.: `JBF 54-60`)**: tritura integralmente o disco em fragmentos metálicos ([DataRaze — Secure Data Disposal](https://dataraze.com/secure-data-disposal-destruction/)).
* **Tamanho das Partículas**:
  * **Norma padrão**: tamanho de partícula de **`15–30 mm`**;
  * **Ativos sensíveis `IL4`, `IL5` ou `IL6` (*Impact Level 4, 5, 6 — Confidential, Secret and Top Secret*)**: triturados até **`6 mm`**, impedindo qualquer reutilização ou reconstrução.
* **Desperdício evitável**: triturar sistematicamente discos funcionais que poderiam ser sanitizados (*wiped out*) e reutilizados/revendidos gera desperdício económico e ambiental desnecessário ([Artigo sobre Desperdício na Trituração](https://tinyurl.com/5n83e2j3)).

### 3.3. Desmontagem por Vibração — `DiskMantler` (Slide 19)

* O **`DiskMantler`** é um equipamento que utiliza **vibração** durante cerca de **`60 segundos`** para desmontar discos rígidos e separar os seus componentes internos (placa lógica, motor, pratos, ímanes e tampa) para reciclagem ([DiskMantler](https://tinyurl.com/y2xdkdzr)).

> [!WARNING] Armadilha Crítica: O `DiskMantler` NÃO Destrói os Dados
> O **`DiskMantler` apenas separa mecanicamente as peças do HDD para reciclagem — NÃO apaga nem desmagnetiza os dados**. Se os pratos magnéticos não tiverem sido previamente limpos (*wiped*) ou desmagnetizados (*degaussed*), saem fisicamente intactos e legíveis da máquina.

---

## 4. Matriz Comparativa de Métodos para HDDs

| Método | Mecanismo Técnico | Duração / Eficiência | Reutilização do HDD | Efeito nos Dados | Conformidade / Notas |
| :--- | :--- | :--- | :---: | :--- | :--- |
| ***Wiping* por Software** (`Eraser`, `DBAN`, `CCleaner`, `KillDisk`) | Sobreposição lógica de setores (1 a 35 passagens) | Lento; maior consumo energético em discos grandes | **Sim** (revenda/reuso) | Destrói dados em setores endereçáveis (+ *slack* / `ADS` no `Eraser`) | Permite certificação por dispositivo (`Active@ KillDisk`) |
| ***Degaussing*** | Campo magnético intenso | **`1 ciclo = 1 min`**; mais eficiente energeticamente | **Não** (destrói `tracks` de fábrica; exceção: *tapes*/disquetes) | Destrói magnetização integral dos pratos | Cumpre **NIST**, **PIPEDA**, **HIPAA** e **PCI DSS** |
| ***Disk Crusher* / *Super Shredder*** (`JBF 54-60`) | Perfuração/dobra ou trituração mecânica | Rápido | **Não** | Destruição física irreversível | Padrão **`15–30 mm`**; **`6 mm`** para **`IL4`/`IL5`/`IL6`** |
| **`DiskMantler`** | Vibração mecânica (~`60 s`) | ~1 minuto | Apenas reciclagem de peças | **NÃO destrói dados** | Exige *wiping* ou *degaussing* prévio |

---

## Além da aula

* **Limpeza da `Cluster Tip Area` e `Alternate Data Streams` vs. Análise Forense (`AFD1` Cap. 2 e `ASSI` Cap. 3)**: A opção do `Eraser` para limpar especificamente a *Cluster Tip Area* (*file slack*) e os *Alternate Data Streams* visa eliminar precisamente os locais onde as ferramentas forenses procuram vestígios ocultos — nomeadamente o *slack space* inspecionado pelo *FTK Imager* em [[Ferramentas Gráficas de Aquisição Forense (Guymager, Paladin Toolbox, Tableau Imager e FTK Imager)]] e os fluxos alternativos NTFS estudados em [[Alternate Data Streams (ADS) no NTFS - Arquitetura, Manipulação em CMD e PowerShell]] e [[Ferramentas Gráficas de Análise de ADS e Caso de Estudo WastedLocker]].
* **Certificação e Cadeia de Auditoria no Abate (`ASSI` Cap. 2 Bloco 01)**: Os requisitos de certificação por dispositivo, *audit trail* (*When, what, who, where, how?*), arquivo com fotografias e diretrizes do NCSC para dispositivos usados encontram-se detalhados em [[Certificação de Sanitização, Audit Trail e Guia NCSC para Dispositivos Usados]].

---

## Perguntas de revisão

1. **Quais são os três níveis de sanitização de suportes definidos por Jones & Afrifa (2020) e em quais é possível reutilizar o HDD?**

> [!success]- Ver Resposta
> Os três níveis são: (1) **Discarding** (descarte simples sem apagar dados — reutilizável mas inseguro), (2) **Clearing / Purging** (sobreposição por software/*Secure Erase* permite reutilizar o HDD; *degaussing* impede a reutilização do HDD), e (3) **Destroying** (destruição física por trituração/esmagamento — impossibilita qualquer reutilização).

2. **Que seis métodos de sobreposição e que duas opções específicas de limpeza NTFS são disponibilizados pelo software `Eraser`?**

> [!success]- Ver Resposta
> Os seis métodos são: `Gutmann (35 passes)`, `US DoD 5220.22-M (8-306./E, C and E) (7 passes)`, `US DoD 5220.22-M (8-306./E) (3 passes)`, `Schneier's 7 pass`, `Pseudorandom Data (1 pass)` e `First and last 2KB of the file`. Adicionalmente, permite limpar a **`Cluster Tip Area`** (*slack space* no fim do cluster) e os **`Alternate Data Streams`** (fluxos alternativos do NTFS).

3. **Porque é que um HDD fica inutilizável após o *degaussing*, ao contrário de algumas fitas magnéticas (*tapes*) e disquetes (*floppy disks*)?**

> [!success]- Ver Resposta
> O campo magnético intenso do *degaussing* destrói não apenas os dados do utilizador, mas também as pistas de servo-alinhamento e controlo (`tracks`) gravadas na fábrica. O disco exigiria uma formatação de baixo nível com equipamento especializado de fábrica inacessível ao utilizador. Em contraste, certas fitas magnéticas e disquetes não dependem dessas pistas permanentes de fábrica e podem voltar a ser formatadas e reutilizadas.

4. **Qual é a granulometria padrão na trituração física de discos e qual é a exigida para ativos classificados nos níveis `IL4`, `IL5` ou `IL6`?**

> [!success]- Ver Resposta
> A norma padrão produz partículas de **`15–30 mm`**, enquanto ativos contendo dados sensíveis classificados em **`IL4`, `IL5` ou `IL6`** (*Confidential, Secret and Top Secret*) têm de ser triturados até partículas de **`6 mm`**.

5. **O que faz a máquina `DiskMantler` em ~60 segundos e qual é o erro crítico ao usá-la isoladamente?**

> [!success]- Ver Resposta
> O `DiskMantler` aplica vibração durante ~60 segundos para desmontar um HDD e separar os seus componentes físicos (placa lógica, motor, pratos, ímanes e tampa) para reciclagem. O erro crítico é presumir que substitui a sanitização: **o `DiskMantler` NÃO destrói os dados**, deixando os pratos magnéticos legíveis caso não tenham sido previamente submetidos a *wiping* ou *degaussing*.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Ataques Físicos em Viagens - Evil Maid (FlowCloud) e Burner Phones]] | `mesmo bloco` |
| **Seguinte** | [[Certificação de Sanitização, Audit Trail e Guia NCSC para Dispositivos Usados]] | `mesmo bloco` |
| **Índice** | [[Capítulo 2 - Administração de Sistemas]] · [[00 ASSI]] | `Bloco 01` |

### Conceitos Relacionados

* [[Decommissioning de Equipamentos, Destruição de Papel (P-1 a P-7) e Enquadramento Legal UE]] · `mesmo bloco`
* [[Arquitetura SSD e Memória NAND (Wear Leveling e Garbage Collection)]] · `Comum/`
* [[Alternate Data Streams (ADS) no NTFS - Arquitetura, Manipulação em CMD e PowerShell]] · `Cap. 3`
* [[Ferramentas Gráficas de Análise de ADS e Caso de Estudo WastedLocker]] · `Cap. 3`
* [[Ferramentas Gráficas de Aquisição Forense (Guymager, Paladin Toolbox, Tableau Imager e FTK Imager)]] · `AFD1 · Cap. 2`
