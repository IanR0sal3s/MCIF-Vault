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
atualizado: 2026-11-11
---

# Armazenamento da Aquisição — Clonagem vs Imagem, Formatos, Aquisição Remota e Assinatura de Hashes

Os dados adquiridos são armazenados por clonagem disco-a-disco ou em ficheiros de imagem (`RAW`, `RAW + metadados`, `Embedded`), exigindo *hashes* por blocos assinados com GnuPG.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema / Método)**: A clonagem replica um disco para outro suporte físico, enquanto a criação de imagem encapsula a cópia num ou mais ficheiros só de leitura (com metadados, compressão e segmentação) imunes ao *auto-mount* do sistema operativo.
> * **Porque importa (Forense)**: Um disco clone sem limpeza prévia com zeros (`zero out`) contamina a investigação com vestígios de casos antigos; já uma imagem permite simular escritas numa *cache* separada sem tocar no original, e *hashes* por blocos impedem que um único bit corrompido invalide a prova inteira.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Clonagem vs. Imagem**: A clonagem é vulnerável ao *auto-mount* do Windows (exige *write blocker* ao analisar o clone) e pode alterar a geometria; a imagem é montada *read-only*, permite armazenar várias aquisições num só disco e dividir ficheiros (*split*).
>   * **3 Formatos**: **RAW** (`.dd`, `.raw`, `.img` — mais flexível e universal), **RAW + metadados externos** e **Embedded** (`.E01`, `AFF` — metadados e *hashes* embutidos).
>   * **Compressão e Aquisição Remota**: Compressão poupa espaço para arquivo de longo prazo, mas aumenta o tempo de CPU e nem todas as ferramentas a suportam; na aquisição remota usar **compressão** (rede lenta) e **cifragem** (sem controlo total da rede).
>   * **Hashes por Blocos + GnuPG + Timestamping**: Hashes por janelas evitam invalidação global; assinar o ficheiro `.txt` de *hashes* com **GnuPG** e servidor de *timestamping* prova integridade, autenticidade e data.

---

## 1. Como Armazenar os Dados Adquiridos: Clonagem vs. Imagem Forense

Existem duas abordagens principais para guardar os dados recolhidos durante a aquisição:

| Critério | 1. Clonagem (*Cloning* — Disco para Disco) | 2. Criação de Imagem (*Imaging the Drive* — Disco para Ficheiro) |
| :--- | :--- | :--- |
| **Popularidade** | Menos comum (usada quando é necessário arrancar fisicamente uma réplica do disco). | **Abordagem mais comum** em laboratório. |
| **Tamanho e Preparação do Destino** | • Recomenda-se usar discos **exatamente do mesmo tamanho**.<br/>• Se o disco clone for maior, surge a questão: *onde terminam os dados clonados?*<br/>• É **altamente recomendado preencher previamente o disco de destino com zeros (*zero out first*)** antes de clonar.<br/>• A geometria do disco do clone pode ser diferente da original. | • **Um único disco de destino pode armazenar ficheiros de imagem de vários suportes diferentes**.<br/>• O ficheiro de imagem pode ser **dividido (*split*) em ficheiros mais pequenos** para caber num DVD ou sistema de ficheiros limitado (como FAT32). |
| **Vulnerabilidade ao *Auto-Mount* e Proteção de Escrita** | • Alguns sistemas operativos, nomeadamente o **Windows, montam automaticamente (*auto-mount*) os discos por omissão**.<br/>• Consequentemente, **é necessário continuar a usar bloqueadores de escrita (*write blockers*) para analisar os próprios clones**. | • **Não é vulnerável ao *auto-mount*** pelo sistema operativo.<br/>• Uma imagem será sempre montada em modo só de leitura (*read-only*), **não necessitando de bloqueador de escrita** durante a análise.<br/>• É possível **simular operações de leitura/escrita (*simulate read/write*)**: as alterações são guardadas num **ficheiro de *cache*** separado, deixando a imagem original intacta. |

---

## 2. Formatos de Ficheiro de Imagem Forense

Existem diversos formatos de ficheiro para armazenar os dados adquiridos:

1. **Imagem Bruta (*Raw image* — ex.: `.dd`, `.raw`, `.img`)**:
   * É o formato **mais flexível**, sendo suportado por **todo o software de análise forense** (cópia fiel bit-a-bit sem cabeçalhos proprietários).
2. **Imagem Bruta + Metadados Externos (*Raw image + external metadata*)**:
   * Idêntico à imagem *raw*, mas adiciona **um ficheiro externo complementar** contendo dados descritivos do caso, valores de *hash* e carimbos temporais.
3. **Imagem Embutida (*Embedded image* — ex.: `EWF / .E01`, `AFF`)**:
   * Formato proprietário ou estruturado no qual **os metadados ficam embutidos dentro do próprio ficheiro de imagem** (juntamente com *hashes* e controlos de erro).

### Compromissos do Uso de Compressão em Imagens Forenses
Alguns formatos de ficheiro de imagem (como o formato *embedded* `.E01`) suportam **compressão**:

* **Vantagens**:
  * **Poupa espaço de armazenamento**.
  * Constitui uma **excelente solução para armazenamento de longo prazo** dos ficheiros de imagem.
* **Desvantagens**:
  * O processo de aquisição **demora mais tempo a concluir** devido ao processamento de CPU.
  * **Nem todas as ferramentas de análise suportam ficheiros de imagem comprimidos** — podendo ser necessário descomprimir ou converter primeiro a imagem para formato *RAW*.

---

## 3. Aquisição Local vs. Aquisição Remota

| Modalidade | Condições de Utilização e Requisitos Técnicos |
| :--- | :--- |
| **Aquisição Local (*Local Acquisition*)** | Implica **acesso físico direto** à unidade de armazenamento. |
| **Aquisição Remota (*Remote Acquisition*)** | Realizada através da rede nos seguintes cenários:<br/>• Quando **não é possível ter acesso físico** à unidade de armazenamento (ex.: servidor remoto ou na *cloud*).<br/>• Quando **não existem adaptadores adequados** para o suporte de armazenamento do equipamento suspeito.<br/>• **Recomendações técnicas**: Como este processo é **mais lento** (limitado pela largura de banda da rede), **recomenda-se o uso de compressão**; adicionalmente, se não existir controlo total sobre a rede atravessada, **deve ser utilizada cifragem** do canal de transmissão. |

---

## 4. Valores de Hash por Blocos e Assinaturas Digitais

Para garantir a integridade dos dados adquiridos ao longo do tempo:

* **Hashes por blocos de pequena dimensão**:
  * Além do *hash* global do disco inteiro, devem ser calculados e guardados *hashes* de blocos mais pequenos (por exemplo, do mesmo tamanho do bloco de aquisição ou janelas de `1 MB` / `1 GB`) **para evitar que um único erro futuro invalide a imagem inteira do disco**.
* **Armazenamento em ficheiros RAW**:
  * Numa aquisição em formato `RAW`, os valores de *hash* são guardados num **ficheiro de texto separado** (ex.: `md5.txt`, `sha256.txt`).

> [!IMPORTANT] Assinatura Digital do Ficheiro de Hashes (GnuPG + Timestamping)
> * **Boa Prática Recomendada pelo Docente**: Realizar uma **assinatura digital sobre os ficheiros que contêm os valores de *hash***.
> * **Porquê esta prática?** (Revisão do Capítulo 1 — [[Preservação do Sistema e Integridade de Dados]]): Porque o cálculo de um *hash* $H(M) = h$ não envolve qualquer chave secreta; sem assinatura digital, alguém com acesso ao repositório poderia modificar a imagem `RAW` para $M'$, recalcular o novo hash $H(M')$ e substituir o ficheiro `.txt` de hashes. A assinatura digital com a chave privada do perito garante a **autenticidade, integridade e não-repúdio** do manifesto de *hashes*.
> * **Ferramentas recomendadas**:
>   * A melhor ferramenta para assinar o ficheiro de *hashes* é o [GnuPG](https://gnupg.org/) (*GNU Privacy Guard*).
>   * Sempre que possível, deve também recorrer-se a um **servidor de selos temporais (*time stamping server*)** para provar criptograficamente a data e hora exatas em que a aquisição e o manifesto de *hashes* existiam.

---

## Implicações Forenses

* **Porquê preencher um disco de destino com zeros (*zero out*) antes de Clonar?**: Se um perito clonar um disco suspeito de `250 GB` para um disco de destino de `500 GB` que já tinha sido utilizado noutra investigação sem o limpar previamente com zeros (`0x00`), os segundos `250 GB` do disco de destino continuarão a conter restos de ficheiros de outro caso! Durante o *file carving* no espaço não alocado, ocorreria **contaminação cruzada de evidências** entre processos judiciais distintos.
* **Resiliência Pericial com *Hash Windows***: Se uma imagem forense de `2 TB` sofrer a corrupção de 1 bit no meio de armazenamento meses mais tarde, um único hash global `SHA-256` falhará, inutilizando toda a imagem. Com *hashes* calculados por janelas (ex.: a cada `1 GB` com `dcfldd`), o perito consegue provar matematicamente ao tribunal que `1999 GB` da imagem permanecem 100% íntegros e isolar o único bloco afetado.

---

## Além da aula

* **Simulação de Escrita com Ficheiro de Cache na Prática**:
  * A funcionalidade destacada nesta aula — emular operações de leitura/escrita gravando as alterações num ficheiro de *cache* e mantendo a evidência original intacta — é implementada na prática pela ferramenta Linux **`xmount --cache`** (estudada em [[Aquisição e Montagem em Linux - Formato EWF (ewf-tools, ewfmount e xmount)]]) e é igualmente indispensável quando montamos imagens ou cópias de sombra em [[Acesso Forense e Montagem de Shadow Copies]] (ASSI) ou quando precisamos que motores de bases de dados como o **SQLite** ([[Timestamps e Épocas Temporais (UNIX Epoch vs. Windows FILETIME)]], [[Windows Activity Timeline - Arquitetura e Base SQLite]]) ou o **ESE** ([[System Resource Usage Monitor (SRUM) - Arquitetura e Base ESE]], [[Windows Search]]) façam *replay* de *transaction logs* sujos (*dirty shutdown*) sem tocar na imagem original.

---

## Perguntas de revisão

1. **Enumere quatro vantagens de adquirir um disco para um ficheiro de imagem (*imaging*) em vez de realizar a clonagem direta disco-a-disco (*cloning*).**

> [!success]- Ver Resposta
> 1. **Não é vulnerável ao *auto-mount*** do sistema operativo e é montada em modo *read-only*, dispensando *write blockers* durante a análise.
> 2. Permite armazenar **múltiplas imagens** de diferentes suportes num único disco de destino.
> 3. Pode ser **dividida (*split*)** em segmentos mais pequenos (ex.: para DVD ou FAT32).
> 4. Permite **simular operações de leitura/escrita** gravando as alterações num ficheiro de *cache* separado e mantendo a imagem original intocada.

2. **Porque é altamente recomendado preencher previamente com zeros (*zero out*) o disco de destino antes de realizar uma clonagem forense?**

> [!success]- Ver Resposta
> Para evitar **contaminação cruzada de evidências**: se o disco de destino tiver maior capacidade ou contiver resíduos de investigações anteriores nos setores além do final da cópia, esses dados residuais misturar-se-iam com o espaço não alocado durante análises de *file carving*.

3. **Quais são os três formatos gerais de ficheiros de imagem forense e que vantagens/desvantagens apresenta o uso de compressão?**

> [!success]- Ver Resposta
> Os três formatos são **Imagem Bruta (*Raw* — `.dd`, `.raw`, `.img`)**, **Imagem Bruta + Metadados Externos** e **Imagem Embutida (*Embedded* — `.E01`, `AFF`)**. A **compressão** poupa espaço e é excelente para armazenamento a longo prazo, mas torna a aquisição mais lenta (CPU) e **nem todas as ferramentas de análise suportam imagens comprimidas** diretamente.

4. **Em que situações se recorre à aquisição remota (*remote acquisition*) e que duas medidas técnicas (desempenho e segurança) devem ser aplicadas nesse processo?**

> [!success]- Ver Resposta
> Recorre-se quando **não há acesso físico** ao suporte (ex.: servidor remoto ou *cloud*) ou quando **não existem adaptadores adequados**. Como é mais lenta, recomenda-se usar **compressão** para poupar largura de banda e **cifragem** do canal sempre que não exista controlo total sobre a rede atravessada.

5. **Porque se recomenda calcular *hashes* por blocos pequenos e assinar digitalmente o ficheiro de *hashes* com o GnuPG e um servidor de *timestamping*?**

> [!success]- Ver Resposta
> Calcular *hashes* por blocos pequenos impede que um único erro futuro num setor ou ficheiro invalide toda a imagem do disco. Assinar o ficheiro de *hashes* com **GnuPG** (chave privada) e um servidor de ***timestamping*** impede que terceiros adulterem simultaneamente a imagem e o respetivo ficheiro de *hashes* (já que o hash $H(M)$ não tem segredo), provando autenticidade, integridade e existência numa data exata.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Procedimentos de Aquisição - Post-Mortem vs Live, Erros de Disco, HPA-DCO e Write Blockers]] | `mesmo bloco` |
| **Seguinte** | [[Aquisição e Montagem em Linux - Formato EWF (ewf-tools, ewfmount e xmount)]] | `muda para Bloco 05` |
| **Índice** | [[Capítulo 2 - Arranque e Aquisição Forense]] · [[00 AFD1]] | `Bloco 04` |

### Conceitos Relacionados

* [[Princípios de Aquisição Forense, Resposta Inicial e Camadas de Abstração]] · `mesmo bloco`
* [[Aquisição em Linha de Comandos no Linux - dcfldd e Derivados do dd]] · `Bloco 05`
* [[Preservação do Sistema e Integridade de Dados]] · `Cap. 1`
* [[Exercícios Práticos - Integridade de Dados e Hashes]] · `Cap. 1`
* [[Acesso Forense e Montagem de Shadow Copies]] · `ASSI · Cap. 1`
* [[System Resource Usage Monitor (SRUM) - Arquitetura e Base ESE]] · `ASSI · Cap. 1`
* [[Windows Activity Timeline - Arquitetura e Base SQLite]] · `ASSI · Cap. 1`
