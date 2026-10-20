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
atualizado: 2026-10-20
---

# Procedimentos de Aquisição — Post-Mortem vs Live, Erros de Disco, HPA-DCO e Write Blockers

A execução técnica de uma cópia forense exige controlar como a ferramenta lê o dispositivo (**acesso direto** em vez de chamadas à BIOS antiga), decidir entre aquisição **post-mortem** (com um sistema operativo de confiança, acautelando o arranque rápido e potenciais compromissos de firmware) ou **alive** (sujeita à ocultação de dados por *rootkits*), garantir o alinhamento binário perante **setores defeituosos (*bad sectors*)** através do preenchimento com zeros (`000000`), extrair áreas ocultas de disco (**HPA** e **DCO**) respeitando a regra da dupla aquisição, e isolar o suporte com **bloqueadores de escrita (*write blockers*)** de hardware ou software testados pelo projeto **CFTT**.

---

## 1. Leitura dos Dados e Aquisição *Post-Mortem* vs. *Alive*

### Requisitos de Espaço e Modo de Leitura do Disco
* Realizar uma cópia forense de um suporte de armazenamento exige **outro suporte de armazenamento de capacidade igual ou superior** (embora muitas ferramentas consigam criar ficheiros de imagem comprimidos).
* **Métodos de leitura dos dados (*reading the data*)**:
  * **Através da BIOS (*through the BIOS*)**: As BIOS antigas não suportam discos de grande capacidade $\rightarrow$ **podem reportar um tamanho de disco incorreto** (truncando a aquisição).
  * **Acesso Direto (*direct access*)**: Consiste em comunicar diretamente com o controlador de armazenamento ignorando a BIOS; **é a melhor escolha**, embora não seja suportada por todas as ferramentas.

### Aquisição *Post-Mortem* vs. Aquisição *Alive* (*Online*)

| Modalidade | Características, Riscos e Recomendações Periciais |
| :--- | :--- |
| **Aquisição *Post-Mortem*** | • O sistema operativo suspeito encontra-se **desligado (*shutdown*)**.<br/>• O próprio hardware suspeito pode ser utilizado recorrendo a um **sistema operativo de confiança (*trusted OS*)** para o arrancar (arranque forense).<br/>• **Cuidado (*Caution*)**: Os PCs modernos arrancam demasiado depressa (*boot too fast*), pelo que o perito pode não ir a tempo de alterar a ordem de arranque antes de o disco interno iniciar.<br/>• **Confiança no Hardware**: O escândalo da NSA demonstrou que **nem sempre podemos confiar no hardware** (existência de *spyware* alojado dentro do próprio *firmware* dos discos rígidos HDD), embora tal seja muito menos provável de acontecer do que a adulteração de software (*software tampering*). |
| **Aquisição *Alive* (*Online*)** | • O sistema operativo suspeito **está em execução** e é utilizado para realizar a própria aquisição.<br/>• Existe o **risco de o sistema operativo ter sido adulterado (*tampered*) e devolver dados falsos/incorretos** — por exemplo, **rootkits** que ocultam processos e ficheiros para evitar a deteção.<br/>• **Regra**: A aquisição *online* deve ser realizada **apenas em situações especiais** (ex.: servidores críticos que não podem ser desligados ou discos cifrados em aberto). |

---

## 2. Tratamento de Erros de Leitura (*Dealing with Media Errors / Bad Sectors*)

O que acontece se o disco tiver setores defeituosos (*bad sectors*)?
* A aquisição continua a ser possível, desde que a percentagem de setores defeituosos seja reduzida.
* A ferramenta de aquisição forense **tem obrigatoriamente de lidar com os erros cumprindo 3 requisitos**:
  1. **Colocar zeros (`000000`) nos setores defeituosos** para que os dados subsequentes **mantenham o seu alinhamento (*keep its alignment*)** — caso contrário, a cópia forense ficaria mais pequena do que o disco original (deslocando os offsets de todas as partições e estruturas seguintes) e a ferramenta de análise desencadearia erros.
  2. **Registar num ficheiro de *log* (*log file*)** todos os setores defeituosos identificados.
  3. **Diminuir automaticamente o tamanho do bloco de aquisição para o tamanho do setor** (*automatically decrease the acquisition block size to the sector size*) na zona do erro, minimizando a perda de dados válidos adjacentes.

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
| **DCO (*Device Configuration Overlay*)** | • Ao contrário da HPA, **a remoção da DCO é permanente (*permanent*)** — altera definitivamente a configuração do disco.<br/>• **Medida de precaução crítica**: Como a remoção é irreversível, deve obrigatoriamente fazer-se **primeiro uma cópia forense com a DCO ativa (*in place*)** antes de a remover para a segunda aquisição.<br/>• Poucas ferramentas suportam a leitura de áreas DCO (lista mantida em `forensicswiki.org`). |

> [!TIP] Ferramenta Recomendada para HPA e DCO
> O **Tableau Imager** é capaz de **identificar e ler tanto áreas HPA como áreas DCO**.

---

## 4. Bloqueadores de Escrita (*Write Blockers*)

Os **bloqueadores de escrita (*write blockers*)** impedem qualquer operação de escrita no suporte de armazenamento sob investigação, dividindo-se em duas categorias:

### 1. Bloqueadores de Escrita de Hardware (*Hardware Write Blockers*)
* São **específicos para cada interface de suporte**: `ATA`, `SATA`, `SCSI`, `Firewire (IEEE 1394)` ou `USB`.
* **Impedem operações de escrita independentemente do sistema operativo utilizado** (*regardless of the used OS*).
* O hardware especializado proporciona **melhor desempenho (velocidade) de aquisição**.
* Alguns equipamentos de hardware funcionam como um *proxy* entre o computador e o disco, monitorizando e filtrando todas as operações/comandos enviados ao controlador.
* **É a melhor opção técnica**, mas também **a mais dispendiosa (*most expensive*)**.
* Os relatórios públicos de testes de conformidade encontram-se no catálogo **CFTT hardware write blockers** (NIST).

### 2. Bloqueadores de Escrita de Software (*Software Write Blockers*)
* Constituem a **solução mais económica (*less expensive*)** (ex.: configurações de registo no WinFE ou montagem read-only no kernel Linux).
* Contudo, **podem ser menos eficazes**: algumas aplicações conseguem contornar (*bypass*) o bloqueio de escrita por software se comunicarem diretamente com o hardware a baixo nível.
* Os relatórios de validação encontram-se no catálogo **CFTT software write blockers** (NIST).

---

## Implicações Forenses

* **Porquê Duas Aquisições em Discos com HPA/DCO?**: Desativar uma HPA ou remover uma DCO (especialmente a DCO, cuja remoção é permanente!) exige enviar comandos de escrita/configuração ao controlador do disco original. Se o perito o fizesse antes de criar uma primeira imagem, um advogado de defesa poderia alegar que o perito alterou o estado original do disco antes de o preservar. Fazendo **primeiro a aquisição com HPA/DCO intacta** (e calculando o respetivo hash) e **depois uma segunda aquisição com HPA/DCO desativada**, o perito preserva a integridade da prova original e obtém também os setores ocultos.
* **Importância do Alinhamento Binário nos *Bad Sectors***: No Capítulo 3 de AFD1 ([[Organização de Estruturas de Dados em Binário]]) e nos artefactos de [[00 ASSI|ASSI]] (como a MFT, hives do Registry ou ficheiros `.pf`), todas as estruturas são localizadas por deslocamentos (*offsets*) exatos em bytes desde o início do disco/partição. Se um setor defeituoso fosse simplesmente omitido em vez de preenchido com `512 bytes` de zeros (`0x00`), todos os *offsets* seguintes ficariam deslocados em `-512 bytes`, corrompendo a leitura de todo o sistema de ficheiros.

---

## Além da aula

* **Ameaças ao Firmware e Cadeia de Arranque em [[00 ASSI|ASSI]]**:
  * O alerta da aula sobre *spyware* no firmware de discos rígidos (revelações da NSA, como o módulo *IRATEMONK* do catálogo ANT) e sobre a impossibilidade de confiar num SO em execução devido a *rootkits* articula-se diretamente com o estudo de *bootkits* UEFI em [[PKfail - Vulnerabilidade do UEFI Secure Boot]] e [[PKfail - Cadeia de Ataque e Deteção Forense]]: quando o próprio firmware ou kernel está comprometido, a análise *live* pode sofrer manipulação ativa (*API hooking*), tornando a aquisição *offline* com *hardware write-blocker* a única fonte totalmente imune a ocultação por software.

---

## Perguntas de revisão

- Porque é que o acesso direto (*direct access*) ao disco é preferível à leitura através da BIOS durante a aquisição forense?
- Que riscos específicos apresenta a aquisição *post-mortem* através de um arranque forense no computador suspeito e que risco principal apresenta a aquisição *alive*?
- Como deve uma ferramenta forense proceder quando encontra setores defeituosos (*bad sectors*) e porque é indispensável preencher esses setores com zeros?
- Qual é a diferença fundamental entre a remoção de uma *Host Protected Area (HPA)* com `hdparm` e a remoção de uma *Device Configuration Overlay (DCO)*? Porque se recomendam duas aquisições em ambos os casos?
- Compare os bloqueadores de escrita (*write blockers*) de hardware e de software quanto ao custo, desempenho e segurança.

## Notas relacionadas

- [[Princípios de Aquisição Forense, Resposta Inicial e Camadas de Abstração]]
- [[Armazenamento da Aquisição - Clonagem vs Imagem, Formatos, Aquisição Remota e Assinatura de Hashes]]
- [[Aquisição em Linha de Comandos no Linux - dcfldd e Derivados do dd]]
- [[Ferramentas Gráficas de Aquisição Forense (Guymager, Paladin Toolbox, Tableau Imager e FTK Imager)]]
- [[Investigação Forense Digital - Análise Live vs Post-Mortem]]
- [[Preservação do Sistema e Integridade de Dados]]
- [[Organização de Estruturas de Dados em Binário]]
- [[PKfail - Vulnerabilidade do UEFI Secure Boot]]
- [[PKfail - Cadeia de Ataque e Deteção Forense]]
- [[Capítulo 2 - Arranque e Aquisição Forense]]
