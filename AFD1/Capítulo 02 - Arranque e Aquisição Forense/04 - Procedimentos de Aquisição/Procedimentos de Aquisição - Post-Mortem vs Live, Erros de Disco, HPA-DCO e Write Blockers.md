---
title: Procedimentos de Aquisição - Post-Mortem vs Live, Erros de Disco, HPA-DCO e Write Blockers
tipo: procedimento
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
  - post-mortem
  - live-analysis
  - bad-sectors
  - hpa
  - dco
  - hdparm
  - write-blocker
  - cftt
aliases:
  - Dealing with media errors
  - Bad Sectors
  - Host Protected Area
  - HPA
  - Device Configuration Overlay
  - DCO
  - Hardware vs Software Write Blockers
atualizado: 2026-11-11
---

# Procedimentos de Aquisição — Post-Mortem vs Live, Erros de Disco, HPA-DCO e Write Blockers

A aquisição segura exige leitura em acesso direto, tratamento de *bad sectors* com preenchimento a zeros (`000000`), dupla cópia para áreas **HPA/DCO** e isolamento via *write blockers*.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Hardware / Método)**: Chamadas antigas à BIOS truncam discos grandes, setores físicos avariados desalinhariam partições se fossem omitidos, e comandos ATA permitem esconder dados em áreas **HPA** e **DCO** invisíveis ao sistema operativo.
> * **Porque importa (Forense)**: Sem preenchimento a zeros (`000000`) nos *bad sectors*, os *offsets* do sistema de ficheiros colapsam; remover uma **DCO** antes da primeira cópia altera permanentemente o disco original antes de o preservar; e sem *write blocker* validado (**CFTT**), o próprio SO de análise pode escrever no disco suspeito.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Leitura**: **Direct Access** (comunica diretamente com o controlador, melhor escolha) vs. leitura via BIOS (pode reportar capacidade incorreta).
>   * **3 Regras em *Bad Sectors***: (1) preencher com `000000` para manter o alinhamento; (2) registar em ficheiro de *log*; (3) reduzir automaticamente o bloco para o tamanho do setor.
>   * **HPA vs. DCO**: **`hdparm`** destranca a **HPA temporariamente** (reinício restaura); remoção da **DCO é permanente** — realizar **sempre 2 aquisições** (1.ª com área oculta intacta, 2.ª após desativação). **Tableau Imager** lê ambas.
>   * **Write Blockers**: Hardware (melhor velocidade, independente do SO, mais caro) vs. Software (mais económico, sujeito a *bypass* de baixo nível).

---

## 1. Leitura dos Dados e Aquisição *Post-Mortem* vs. *Alive*

### Requisitos de Espaço e Modo de Leitura do Disco

* Realizar uma cópia forense de um suporte de armazenamento exige **outro suporte de armazenamento de capacidade igual ou superior** (embora muitas ferramentas consigam criar ficheiros de imagem comprimidos).
* **Métodos de leitura dos dados**:
  * **Através da BIOS**: As BIOS antigas não suportam discos de grande capacidade $\rightarrow$ **podem reportar um tamanho de disco incorreto** (truncando a aquisição).
  * **Acesso Direto (*direct access*)**: Consiste em comunicar diretamente com o controlador de armazenamento ignorando a BIOS; **é a melhor escolha**, embora não seja suportada por todas as ferramentas.

### Aquisição *Post-Mortem* vs. Aquisição *Alive* (*Online*)

| Modalidade | Características, Riscos e Recomendações Periciais |
| :--- | :--- |
| **Aquisição *Post-Mortem*** | • O sistema operativo suspeito encontra-se **desligado**.<br/>• O próprio hardware suspeito pode ser utilizado recorrendo a um **sistema operativo de confiança (*trusted OS*)** para o arrancar (arranque forense).<br/>• **Cuidado**: Os PCs modernos arrancam demasiado depressa, pelo que o perito pode não ir a tempo de alterar a ordem de arranque antes de o disco interno iniciar.<br/>• **Confiança no Hardware**: O escândalo da NSA demonstrou que **nem sempre podemos confiar no hardware** (existência de *spyware* alojado dentro do próprio *firmware* dos discos rígidos HDD), embora tal seja muito menos provável de acontecer do que a adulteração de software. |
| **Aquisição *Alive* (*Online*)** | • O sistema operativo suspeito **está em execução** e é utilizado para realizar a própria aquisição.<br/>• Existe o **risco de o sistema operativo ter sido adulterado e devolver dados falsos/incorretos** — por exemplo, **rootkits** que ocultam processos e ficheiros para evitar a deteção.<br/>• **Regra**: A aquisição *online* deve ser realizada **apenas em situações especiais** (ex.: servidores críticos que não podem ser desligados ou discos cifrados em aberto). |

---

## 2. Tratamento de Erros de Leitura (*Media Errors / Bad Sectors*)

O que acontece se o disco tiver setores defeituosos (*bad sectors*)?

* A aquisição continua a ser possível, desde que a percentagem de setores defeituosos seja reduzida.
* A ferramenta de aquisição forense **tem obrigatoriamente de lidar com os erros cumprindo 3 requisitos**:
  1. **Colocar zeros (`000000`) nos setores defeituosos** para que os dados subsequentes **mantenham o seu alinhamento** — caso contrário, a cópia forense ficaria mais pequena do que o disco original (deslocando os offsets de todas as partições e estruturas seguintes) e a ferramenta de análise desencadearia erros.
  2. **Registar num ficheiro de *log*** todos os setores defeituosos identificados.
  3. **Diminuir automaticamente o tamanho do bloco de aquisição para o tamanho do setor** na zona do erro, minimizando a perda de dados válidos adjacentes.

```text
Original:  | 342622 | xxxxxx | xxxxxx | 826193 | xxxxxx | 648633 |
               │                          │                 │
               ▼                          ▼                 ▼
Cópia:     | 342622 | 000000 | 000000 | 826193 | 000000 | 648633 |
```

*(Os setores ilegíveis `xxxxxx` são substituídos por blocos de zeros `000000` de igual dimensão na cópia, preservando os offsets exatos dos blocos válidos `826193` e `648633`).*

---

## 3. Áreas Ocultas do Disco: HPA e DCO (*Hidden Areas*)

Os discos rígidos suportam comandos de controlador (ATA) que permitem ocultar parte da capacidade real do disco ao sistema operativo e à BIOS, criando áreas onde um utilizador ou malware pode esconder dados:

| Área Oculta | Comportamento Técnico, Ferramentas e Procedimento Pericial |
| :--- | :--- |
| **HPA (*Host Protected Area*)** | • Esta área **deve também ser copiada**, pois pode conter dados ocultos.<br/>• Poucas ferramentas suportam a leitura direta da HPA.<br/>• Podemos utilizar a ferramenta Linux **`hdparm`** para aceder temporariamente à HPA (**um reinício do sistema restaurará a HPA** para o seu estado oculto original).<br/>• **Medida de precaução**: Deve efetuar-se **primeiro uma cópia forense com a HPA ativa (*in place*)** e só depois destrancar e adquirir o disco completo. |
| **DCO (*Device Configuration Overlay*)** | • Ao contrário da HPA, **a remoção da DCO é permanente** — altera definitivamente a configuração do disco.<br/>• **Medida de precaução crítica**: Como a remoção é irreversível, deve obrigatoriamente fazer-se **primeiro uma cópia forense com a DCO ativa (*in place*)** antes de a remover para a segunda aquisição.<br/>• Poucas ferramentas suportam a leitura de áreas DCO (lista mantida em `forensicswiki.org`). |

> [!TIP] Ferramenta Recomendada para HPA e DCO
> O **Tableau Imager** é capaz de **identificar e ler tanto áreas HPA como áreas DCO**.

---

## 4. Bloqueadores de Escrita (*Write Blockers*)

Os **bloqueadores de escrita (*write blockers*)** impedem qualquer operação de escrita no suporte de armazenamento sob investigação, dividindo-se em duas categorias:

### 1. Bloqueadores de Escrita de Hardware (*Hardware Write Blockers*)

* São **específicos para cada interface de suporte**: `ATA`, `SATA`, `SCSI`, `Firewire (IEEE 1394)` ou `USB`.
* **Impedem operações de escrita independentemente do sistema operativo utilizado**.
* O hardware especializado proporciona **melhor desempenho (velocidade) de aquisição**.
* Alguns equipamentos de hardware funcionam como um *proxy* entre o computador e o disco, monitorizando e filtrando todas as operações/comandos enviados ao controlador.
* **É a melhor opção técnica**, mas também **a mais dispendiosa**.
* Os relatórios públicos de testes de conformidade encontram-se no catálogo **CFTT hardware write blockers** (NIST).

### 2. Bloqueadores de Escrita de Software (*Software Write Blockers*)

* Constituem a **solução mais económica** (ex.: configurações de registo no WinFE ou montagem read-only no kernel Linux).
* Contudo, **podem ser menos eficazes**: algumas aplicações conseguem contornar (*bypass*) o bloqueio de escrita por software se comunicarem diretamente com o hardware a baixo nível.
* Os relatórios de validação encontram-se no catálogo **CFTT software write blockers** (NIST).

---

## Implicações Forenses

* **Porquê Duas Aquisições em Discos com HPA/DCO?**: Desativar uma HPA ou remover uma DCO (especialmente a DCO, cuja remoção é permanente!) exige enviar comandos de escrita/configuração ao controlador do disco original. Se o perito o fizesse antes de criar uma primeira imagem, um advogado de defesa poderia alegar que o perito alterou o estado original do disco antes de o preservar. Fazendo **primeiro a aquisição com HPA/DCO intacta** (e calculando o respetivo hash) e **depois uma segunda aquisição com HPA/DCO desativada**, o perito preserva a integridade da prova original e obtém também os setores ocultos.
* **Importância do Alinhamento Binário nos *Bad Sectors***: No Capítulo 3 de AFD1 ([[Organização de Estruturas de Dados em Binário]]) e nos artefactos de [[00 ASSI|ASSI]] (como a MFT, hives do Registry ou ficheiros `.pf`), todas as estruturas são localizadas por deslocamentos (*offsets*) exatos em bytes desde o início do disco/partição. Se um setor defeituoso fosse simplesmente omitido em vez de preenchido com `512 bytes` de zeros (`0x00`), todos os *offsets* seguintes ficariam deslocados em `-512 bytes`, corrompendo a leitura de todo o sistema de ficheiros.

---

## Além da aula

* **Ameaças ao Firmware e Cadeia de Arranque em [[00 ASSI|ASSI]]**:
  * O alerta da aula sobre *spyware* no firmware de discos rígidos (revelações da NSA, como o módulo *IRATEMONK* do catálogo ANT) e sobre a impossibilidade de confiar num SO em execução devido a *rootkits* articula-se diretamente com o estudo de *bootkits* UEFI em [[PKfail - Vulnerabilidade do UEFI Secure Boot]] e [[PKfail - Vulnerabilidade do UEFI Secure Boot]]: quando o próprio firmware ou kernel está comprometido, a análise *live* pode sofrer manipulação ativa (*API hooking*), tornando a aquisição *offline* com *hardware write-blocker* a única fonte totalmente imune a ocultação por software.

---

## Perguntas de revisão

1. **Porque é que o acesso direto (*direct access*) ao disco é preferível à leitura através da BIOS durante a aquisição forense?**

> [!success]- Ver Resposta
> Porque as BIOS antigas não suportam discos de grande capacidade e podem **reportar um tamanho de disco incorreto**, truncando a aquisição. O **acesso direto** comunica diretamente com o controlador de armazenamento, garantindo a leitura integral da unidade.

2. **Que riscos específicos apresenta a aquisição *post-mortem* através de um arranque forense no computador suspeito e que risco principal apresenta a aquisição *alive*?**

> [!success]- Ver Resposta
> Na aquisição *post-mortem* por arranque forense, os PCs modernos **arrancam demasiado depressa** (risco de não intercetar o *boot* a tempo) e o próprio **hardware/firmware do disco** pode estar comprometido (embora menos provável do que adulteração de software). Na aquisição *alive*, o sistema operativo em execução pode estar **adulterado por *rootkits*** que ocultam processos e ficheiros e devolvem dados falsos.

3. **Como deve uma ferramenta forense proceder quando encontra setores defeituosos (*bad sectors*) e porque é indispensável preencher esses setores com zeros?**

> [!success]- Ver Resposta
> Deve: (1) **preencher os setores defeituosos com zeros (`000000`)**; (2) **registar todos os setores defeituosos num ficheiro de *log***; e (3) **diminuir automaticamente o tamanho do bloco de aquisição para o tamanho do setor** na zona afetada. O preenchimento com zeros é indispensável para **manter o alinhamento** dos dados subsequentes — sem ele, a imagem ficaria mais pequena e todos os *offsets* seguintes seriam deslocados, gerando erros nas ferramentas de análise.

4. **Qual é a diferença fundamental entre a remoção de uma *Host Protected Area (HPA)* com `hdparm` e a remoção de uma *Device Configuration Overlay (DCO)*? Porque se recomendam duas aquisições em ambos os casos?**

> [!success]- Ver Resposta
> A remoção de uma **HPA** com `hdparm` é **temporária** (um reinício do sistema restaura a HPA ao estado oculto original), enquanto a remoção de uma **DCO** é **permanente** (altera definitivamente a configuração do disco). Recomendam-se **duas aquisições** — a primeira com a área oculta ativa (*in place*) e a segunda após desativação — para garantir a preservação e o *hash* do estado original antes de enviar comandos de alteração ao controlador do disco.

5. **Compare os bloqueadores de escrita (*write blockers*) de hardware e de software quanto ao custo, desempenho e segurança.**

> [!success]- Ver Resposta
> Os **hardware write blockers** são específicos por interface (`ATA`, `SATA`, `SCSI`, `Firewire`, `USB`), oferecem **melhor velocidade de aquisição** e impedem escritas **independentemente do sistema operativo**, sendo a melhor opção técnica embora **mais dispendiosa**. Os **software write blockers** são **mais económicos**, mas podem ser **contornados (*bypass*)** por aplicações que comuniquem diretamente com o hardware a baixo nível. Ambos são testados pelo projeto **CFTT** do NIST.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Princípios de Aquisição Forense, Resposta Inicial e Camadas de Abstração]] | `mesmo bloco` |
| **Seguinte** | [[Armazenamento da Aquisição - Clonagem vs Imagem, Formatos, Aquisição Remota e Assinatura de Hashes]] | `mesmo bloco` |
| **Índice** | [[Capítulo 2 - Arranque e Aquisição Forense]] · [[00 AFD1]] | `Bloco 04` |

### Conceitos Relacionados

* [[Aquisição em Linha de Comandos no Linux - dcfldd e Derivados do dd]] · `Bloco 05`
* [[Ferramentas Gráficas de Aquisição Forense (Guymager, Paladin Toolbox, Tableau Imager e FTK Imager)]] · `Bloco 05`
* [[Investigação Forense Digital - Análise Live vs Post-Mortem]] · `Cap. 1`
* [[Preservação do Sistema e Integridade de Dados]] · `Cap. 1`
* [[Organização de Estruturas de Dados em Binário]] · `Cap. 3`
* [[PKfail - Vulnerabilidade do UEFI Secure Boot]] · `ASSI · Cap. 1`
