---
title: Armazenamento da Aquisição - Clonagem vs Imagem, Formatos, Aquisição Remota e Assinatura de Hashes
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
  - cloning
  - imaging
  - raw
  - ewf
  - gnupg
  - assinatura-digital
  - hash
aliases:
  - Cloning vs Imaging
  - Clonagem vs Imagem Forense
  - Image File Formats
  - RAW Image
  - Embedded Image
  - Local vs Remote Acquisition
  - GnuPG Hash Signature
atualizado: 2026-10-20
---

# Armazenamento da Aquisição — Clonagem vs Imagem, Formatos, Aquisição Remota e Assinatura de Hashes

Os dados adquiridos de um suporte suspeito podem ser guardados através de duas abordagens: a **clonagem (*cloning*)** direta para outro disco físico ou a **criação de um ficheiro de imagem (*imaging the drive*)** — sendo a criação de imagem a abordagem mais comum e segura por não ser vulnerável ao *auto-mount* do sistema operativo, permitir armazenar várias imagens num único disco e emular escritas através de ficheiros de *cache*. Para garantir a integridade e a autenticidade pericial, os resumos criptográficos devem ser calculados por blocos de pequena dimensão e o ficheiro de *hashes* resultante deve ser **assinado digitalmente** (por exemplo, com **GnuPG** e um servidor de *timestamping*).

---

## 1. Como Armazenar os Dados Adquiridos: Clonagem vs. Imagem Forense

Existem duas abordagens principais para guardar os dados recolhidos durante a aquisição:

| Critério | 1. Clonagem (*Cloning* — Disco para Disco) | 2. Criação de Imagem (*Imaging the Drive* — Disco para Ficheiro) |
| :--- | :--- | :--- |
| **Popularidade** | Menos comum (usada quando é necessário arrancar fisicamente uma réplica do disco). | **Abordagem mais comum (*the most common approach*)** em laboratório. |
| **Tamanho e Preparação do Destino** | • Recomenda-se usar discos **exatamente do mesmo tamanho**.<br/>• Se o disco clone for maior, surge a questão: *onde terminam os dados clonados?*<br/>• É **altamente recomendado preencher previamente o disco de destino com zeros (*zero out first*)** antes de clonar.<br/>• A geometria do disco (*drive geometry*) do clone pode ser diferente da original. | • **Um único disco de destino pode armazenar ficheiros de imagem de vários suportes diferentes**.<br/>• O ficheiro de imagem pode ser **dividido (*split*) em ficheiros mais pequenos** para caber num DVD ou sistema de ficheiros limitado (como FAT32). |
| **Vulnerabilidade ao *Auto-Mount* e Proteção de Escrita** | • Alguns sistemas operativos, nomeadamente o **Windows, montam automaticamente (*auto mount*) os discos por omissão**.<br/>• Consequentemente, **é necessário continuar a usar bloqueadores de escrita (*write blockers*) para analisar os próprios clones**. | • **Não é vulnerável ao *auto mount*** pelo sistema operativo.<br/>• Uma imagem será sempre montada em modo só de leitura (*read-only*), **não necessitando de bloqueador de escrita** durante a análise.<br/>• É possível **simular operações de leitura/escrita (*simulate read/write*)**: as alterações são guardadas num **ficheiro de *cache*** separado, deixando a imagem original intacta. |

---

## 2. Formatos de Ficheiro de Imagem Forense (*Image File Formats*)

Existem diversos formatos de ficheiro para armazenar os dados adquiridos:

1. **Imagem Bruta (*Raw image* — ex.: `.dd`, `.raw`, `.img`)**:
   * É o formato **mais flexível (*most flexible format*)**, sendo suportado por **todo o software de análise forense** (cópia fiel bit-a-bit sem cabeçalhos proprietários).
2. **Imagem Bruta + Metadados Externos (*Raw image + external metadata*)**:
   * Idêntico à imagem *raw*, mas adiciona **um ficheiro externo complementar** contendo dados descritivos do caso, valores de *hash* e carimbos temporais (*time*).
3. **Imagem Embutida (*Embedded image* — ex.: `EWF / .E01`, `AFF`)**:
   * Formato proprietário ou estruturado no qual **os metadados ficam embutidos dentro do próprio ficheiro de imagem** (juntamente com *hashes* e controlos de erro).

### Compromissos do Uso de Compressão em Imagens Forenses
Alguns formatos de ficheiro de imagem (como o formato *embedded* `.E01`) suportam **compressão**:
* **Vantagens**:
  * **Poupa espaço de armazenamento** (*saves storage space*).
  * Constitui uma **excelente solução para armazenamento de longo prazo (*long term storage*)** dos ficheiros de imagem.
* **Desvantagens**:
  * O processo de aquisição **demora mais tempo a concluir** (*takes longer to complete*) devido ao processamento de CPU.
  * **Nem todas as ferramentas de análise suportam ficheiros de imagem comprimidos** — podendo ser necessário descomprimir ou converter primeiro a imagem para formato *RAW*.

---

## 3. Aquisição Local vs. Aquisição Remota

| Modalidade | Condições de Utilização e Requisitos Técnicos |
| :--- | :--- |
| **Aquisição Local (*Local Acquisition*)** | Implica **acesso físico direto** à unidade de armazenamento (*physical access to the storage drive*). |
| **Aquisição Remota (*Remote Acquisition*)** | Realizada através da rede nos seguintes cenários:<br/>• Quando **não é possível ter acesso físico** à unidade de armazenamento (ex.: servidor remoto ou na *cloud*).<br/>• Quando **não existem adaptadores adequados** para o suporte de armazenamento do equipamento suspeito.<br/>• **Recomendações técnicas**: Como este processo é **mais lento** (limitado pela largura de banda da rede), **recomenda-se o uso de compressão**; adicionalmente, se não existir controlo total sobre a rede atravessada, **deve ser utilizada cifragem (*encryption*)** do canal de transmissão. |

---

## 4. Valores de Hash por Blocos e Assinaturas Digitais

Para garantir a integridade dos dados adquiridos ao longo do tempo:
* **Hashes por blocos de pequena dimensão (*hash blocks of small size*)**:
  * Além do *hash* global do disco inteiro, devem ser calculados e guardados *hashes* de blocos mais pequenos (por exemplo, do mesmo tamanho do bloco de aquisição ou janelas de `1 MB` / `1 GB`) **para evitar que um único erro futuro invalide a imagem inteira do disco** (*to prevent a single error to invalidate the all drive image*).
* **Armazenamento em ficheiros RAW**:
  * Numa aquisição em formato `RAW`, os valores de *hash* são guardados num **ficheiro de texto separado** (ex.: `md5.txt`, `sha256.txt`).

> [!IMPORTANT] Assinatura Digital do Ficheiro de Hashes (GnuPG + Timestamping)
> * **Boa Prática Recomendada pelo Docente**: Realizar uma **assinatura digital sobre os ficheiros que contêm os valores de *hash*** (*do a digital signature on the hash values files*).
> * **Porquê esta prática?** (Revisão do Capítulo 1 — [[Preservação do Sistema e Integridade de Dados]]): Porque o cálculo de um *hash* $H(M) = h$ não envolve qualquer chave secreta; sem assinatura digital, alguém com acesso ao repositório poderia modificar a imagem `RAW` para $M'$, recalcular o novo hash $H(M')$ e substituir o ficheiro `.txt` de hashes. A assinatura digital com a chave privada do perito garante a **autenticidade, integridade e não-repúdio** do manifesto de *hashes*.
> * **Ferramentas recomendadas**:
>   * A melhor ferramenta para assinar o ficheiro de *hashes* é o **GnuPG** (*GNU Privacy Guard* — `https://gnupg.org/`).
>   * Sempre que possível, deve também recorrer-se a um **servidor de selos temporais (*time stamping server*)** para provar criptograficamente a data e hora exatas em que a aquisição e o manifesto de *hashes* existiam.

---

## Implicações Forenses

* **Porquê preencher um disco de destino com zeros (*zero out*) antes de Clonar?**: Se um perito clonar um disco suspeito de `250 GB` para um disco de destino de `500 GB` que já tinha sido utilizado noutra investigação sem o limpar previamente com zeros (`0x00`), os segundos `250 GB` do disco de destino continuarão a conter restos de ficheiros de outro caso! Durante o *file carving* no espaço não alocado, ocorreria **contaminação cruzada de evidências** entre processos judiciais distintos.
* **Resiliência Pericial com *Hash Windows***: Se uma imagem forense de `2 TB` sofrer a corrupção de 1 bit no meio de armazenamento meses mais tarde, um único hash global `SHA-256` falhará, inutilizando toda a imagem. Com *hashes* calculados por janelas (ex.: a cada `1 GB` com `dcfldd`), o perito consegue provar matematicamente ao tribunal que `1999 GB` da imagem permanecem 100% íntegros e isolar o único bloco afetado.

---

## Além da aula

* **Simulação de Escrita com Ficheiro de Cache na Prática**:
  * A funcionalidade destacada nesta aula (*"it is possible to simulate read/write operation — the changes will be stored in a cache file, leaving the original intact"*) é implementada na prática pela ferramenta Linux **`xmount --cache`** (estudada em [[Aquisição e Montagem em Linux - Formato EWF (ewf-tools, ewfmount e xmount)]]) e é igualmente indispensável quando montamos imagens ou cópias de sombra em [[Acesso Forense e Montagem de Shadow Copies]] (ASSI) ou quando precisamos que motores de bases de dados como o **SQLite** ([[Representação Forense de Data e Hora (Timestamps e SQLite)]], [[Windows Activity Timeline - Arquitetura e Base SQLite]]) ou o **ESE** ([[System Resource Usage Monitor (SRUM) - Arquitetura e Base ESE]], [[Windows Search]]) façam *replay* de *transaction logs* sujos (*dirty shutdown*) sem tocar na imagem original.

---

## Perguntas de revisão

- Enumere quatro vantagens de adquirir um disco para um ficheiro de imagem (*imaging*) em vez de realizar a clonagem direta disco-a-disco (*cloning*).
- Porque é altamente recomendado preencher previamente com zeros (*zero out*) o disco de destino antes de realizar uma clonagem forense?
- Quais são os três formatos gerais de ficheiros de imagem forense e que vantagens/desvantagens apresenta o uso de compressão?
- Em que situações se recorre à aquisição remota (*remote acquisition*) e que duas medidas técnicas (desempenho e segurança) devem ser aplicadas nesse processo?
- Porque se recomenda calcular *hashes* por blocos pequenos e assinar digitalmente o ficheiro de *hashes* com o GnuPG e um servidor de *timestamping*?

## Notas relacionadas

- [[Princípios de Aquisição Forense, Resposta Inicial e Camadas de Abstração]]
- [[Procedimentos de Aquisição - Post-Mortem vs Live, Erros de Disco, HPA-DCO e Write Blockers]]
- [[Aquisição e Montagem em Linux - Formato EWF (ewf-tools, ewfmount e xmount)]]
- [[Aquisição em Linha de Comandos no Linux - dcfldd e Derivados do dd]]
- [[Preservação do Sistema e Integridade de Dados]]
- [[Exercícios Práticos - Integridade de Dados e Hashes]]
- [[Acesso Forense e Montagem de Shadow Copies]]
- [[System Resource Usage Monitor (SRUM) - Arquitetura e Base ESE]]
- [[Windows Activity Timeline - Arquitetura e Base SQLite]]
- [[Capítulo 2 - Arranque e Aquisição Forense]]
