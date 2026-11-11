---
title: Exercício de Projeto - Catalogação e Etiquetagem de Dispositivos e Serviços
tipo: exercicio
mestrado: Cibersegurança e Informática Forense
uc: Análise Forense Digital I
sigla_uc: AFD1
capitulo: 1
bloco: 4
fonte_aula: MCIF – Digital Forensic Analysis 1 - Investigation Method.pdf
tags:
  - afd1
  - forense
  - exercicio
  - catalogacao
  - etiquetagem
  - projeto
aliases:
  - Exercício de Catalogação
  - Team Project Catalog
atualizado: 2026-11-11
---

# Exercício de Projeto — Catalogação e Etiquetagem de Dispositivos e Serviços

Este exercício prepara o relatório do **Projeto em Equipa**, definindo atributos únicos para dispositivos físicos e serviços de rede, um sistema de etiquetagem hierárquica e tabelas com fotografia pericial.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Método / Sistema)**: Padroniza antes do trabalho laboratorial os campos mínimos de identificação, a notação hierárquica de etiquetas e os modelos de registo fotográfico aplicáveis a hardware e serviços lógicos.
> * **Porque importa (Forense / Tribunal)**: As tabelas, etiquetas e fotografias reais com escala construídas neste guião alimentam diretamente o relatório pericial do **Projeto em Equipa (*Team Project*)**, garantindo rastreabilidade e identificação inequívoca de cada evidência.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Três alvos obrigatórios**: armazenamento/computadores, dispositivos móveis/rede e serviços lógicos (`web`, `DNS`, `POP3`, `IMAP`, `SMTP`, `SSH`).
>   * **Hierarquia nas etiquetas**: deve ser fácil de memorizar e refletir contenção física (ex.: `PC01` $\to$ `PC01.1`, ou padrão LabCIF `A.PC01.HDD01`).
>   * **Regra fotográfica inegociável**: adicionar fotografias reais dos dispositivos **incluindo sempre a régua/escala métrica**.

---

## Especificação do Exercício

### 1. Levantamento de Informação de Registo Único
Elaborar uma lista de toda a informação que deve ser registada para identificar univocamente os seguintes **dispositivos** e **serviços**:

* **Armazenamento e Computadores**: cartões de memória, computadores, discos rígidos, unidades de estado sólido (SSD).
* **Dispositivos Móveis e de Rede**: telemóveis, *smartphones*, dispositivos GPS, *routers*, *switches*, *modems*.
* **Serviços Lógicos / Rede**: `web`, `DNS`, `POP3`, `IMAP`, `SMTP`, `SSH`.

### 2. Criação de um Sistema de Etiquetagem

* Deve ser **fácil de memorizar** e **refletir a hierarquia** sempre que necessário (ex.: 1 PC contendo vários discos rígidos internos).
* Exemplo de estrutura hierárquica: computador `PC01`, disco rígido dentro do computador `PC01.1` (ou seguindo a convenção LabCIF: `A.PC01.HDD01`).

### 3. Documentação, Tabelas e Registo Fotográfico

* Redigir as conclusões num documento formal.
* Criar um **modelo de tabela** para cada tipo de dispositivo ou serviço.
* Adicionar **fotografias reais** para os dispositivos (utilizando os próprios telemóveis, PCs do laboratório, etc.), **sem esquecer a inclusão da régua/escala métrica**.

> [!IMPORTANT] Aplicação no Projeto em Equipa
> Toda a informação, tabelas e regras definidas neste exercício serão diretamente utilizadas na elaboração do relatório pericial do **Projeto em Equipa (*Team Project*)**.

---

## Além da aula

### Guia de Referência de Atributos por Categoria (Apoio à Resolução)
Para apoiar o preenchimento consistente das tabelas de catalogação pedidas no ponto 1, em alinhamento com os modelos de catalogação de [[Registo, Etiquetagem e Fotografia Pericial (Regras LabCIF)]]:

| Categoria | Atributos Identificadores Recomendados |
| :--- | :--- |
| **Discos (`HDD` / `SSD`) e Cartões (`MC`)** | `Tag ID`, Tipo de Dispositivo, Marca, Modelo, Número de Série (`S/N`), Interface (`SATA`, `NVMe`, `USB`, `microSD`), Capacidade, Tipo de Intervenção (*Forensic copy* / aquisição física), Estado de funcionamento, Fotografias, Observações |
| **Computadores (`PC` / `LAP`)** | `Tag ID`, Tipo (Desktop / Portátil), Marca, Modelo, Número de Série / *Service Tag*, Dispositivos de armazenamento internos associados (ex.: `HDD01`, `SSD01`), Endereços MAC das interfaces de rede, Estado (ligado/desligado na apreensão), Tipo de Intervenção, Fotografias, Observações |
| **Telemóveis (`FPH` / `SPH`) e `GPS`** | `Tag ID`, Tipo, Marca, Modelo, Número de Série, `IMEI` (ou múltiplos IMEIs em Dual-SIM), Cartões SIM associados (`UICCID`/`IMSI`), Cartões de memória associados (`MC`), Estado da bateria/ecrã, Tipo de Intervenção (aquisição lógica/física), Fotografias, Observações |
| **Equipamentos de Rede (`Router` / `Switch` / `Modem`)** | `Tag ID`, Tipo, Marca, Modelo, Número de Série, Endereço(s) MAC, Versão de Firmware/OS, Portos ativos/ligações físicas fotografadas, Tipo de Intervenção (extração de configuração/RAM/logs), Fotografias, Observações |
| **Serviços (`Web`, `DNS`, `POP3`, `IMAP`, `SMTP`, `SSH`)** | `Tag ID` (ex.: `DNS01`, `WEB01`, `SSH01`), Nome de Domínio / Endereço IP, Porto e Protocolo (`TCP/UDP`), Tipo de Informação Recolhida (histórico DNS, certificados TLS, cabeçalhos/caixas de correio, chaves de host/logs), *Registrar* / Fornecedor (ISP/Hosting), Datas de Criação/Expiração ou janela temporal, Estado atual, Anexos |

---

## Perguntas de revisão

1. **Que três categorias de alvos têm de ser contempladas nas tabelas de catalogação do exercício para o Projeto em Equipa?**

> [!success]- Ver Resposta
> **1.** Armazenamento e computadores (cartões de memória, PCs, HDDs, SSDs); **2.** Dispositivos móveis e de rede (telemóveis, *smartphones*, GPS, *routers*, *switches*, *modems*); e **3.** Serviços lógicos/rede (`web`, `DNS`, `POP3`, `IMAP`, `SMTP`, `SSH`).

2. **Que requisitos deve cumprir o sistema de etiquetagem pedido no exercício e como se representa um disco interno de um computador?**

> [!success]- Ver Resposta
> Deve ser fácil de memorizar e refletir a hierarquia física sempre que necessário — por exemplo, `PC01` para o computador e `PC01.1` para o disco interno (ou seguindo a convenção LabCIF `A.PC01.HDD01`).

3. **Porque é indispensável incluir uma régua nas fotografias reais tiradas aos dispositivos do laboratório?**

> [!success]- Ver Resposta
> Para fornecer uma **escala métrica** objetiva na imagem, comprovando as dimensões reais do equipamento apreendido e dos detalhes fotografados em conformidade com as regras periciais do LabCIF.

4. **Que atributos distinguem a tabela de catalogação de um serviço lógico (`DNS` / `Web`) da tabela de um disco rígido (`HDD` / `SSD`)?**

> [!success]- Ver Resposta
> Enquanto um disco regista atributos físicos de hardware (marca, modelo, número de série, interface, capacidade e estado de funcionamento), um serviço lógico regista domínio/IP, porto e protocolo (`TCP/UDP`), tipo de informação recolhida (histórico DNS, certificados, logs), *registrar*/fornecedor, datas de criação/expiração, estado atual e anexos.

## Notas relacionadas

- [[Registo, Etiquetagem e Fotografia Pericial (Regras LabCIF)]]
- [[Princípios e Rota do Manuseamento de Evidência Digital]]
- [[Artefactos Forenses de Dispositivos USB]]
- [[Ficheiros LNK (Shell Links) - Metadados e Formato Binário]]
- [[Capítulo 1 - Método de Investigação]]
