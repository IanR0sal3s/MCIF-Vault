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
atualizado: 2026-10-19
---

# Exercício de Projeto — Catalogação e Etiquetagem de Dispositivos e Serviços

Exercício prático estruturante do final do Capítulo 1, cujo resultado serve de base direta para o **relatório do Projeto em Equipa (*Team Project*)** da unidade curricular: consiste em definir os atributos de identificação obrigatórios para uma lista abrangente de dispositivos físicos e serviços de rede, desenhar um sistema de etiquetagem hierárquica e produzir modelos de tabelas (*templates*) acompanhados de fotografias reais com escala.

---

## Especificação do Exercício

### 1. Levantamento de Informação de Registo Único
Elaborar uma lista de toda a informação que deve ser registada para identificar univocamente os seguintes **dispositivos** e **serviços**:
* **Armazenamento e Computadores**: cartões de memória (*memory cards*), computadores (*computers*), discos rígidos (*hard drives*), unidades de estado sólido (*solid state drives* — SSD).
* **Dispositivos Móveis e de Rede**: telemóveis (*phones*), *smartphones*, dispositivos GPS, *routers*, *switches*, *modems*.
* **Serviços Lógicos / Rede**: `web`, `DNS`, `POP3`, `IMAP`, `SMTP`, `SSH`.

### 2. Criação de um Sistema de Etiquetagem (*Tagging System*)
* Deve ser **fácil de memorizar** e **refletir a hierarquia** sempre que necessário (ex.: 1 PC contendo vários discos rígidos internos).
* Exemplo de estrutura hierárquica: computador `PC01`, disco rígido dentro do computador `PC01.1` (ou seguindo a convenção LabCIF: `A.PC01.HDD01`).

### 3. Documentação, Tabelas e Registo Fotográfico
* Redigir as conclusões num documento formal.
* Criar um **modelo de tabela (*table template*)** para cada tipo de dispositivo ou serviço.
* Adicionar **fotografias reais** para os dispositivos (utilizando os próprios telemóveis, PCs do laboratório, etc.), **sem esquecer a inclusão da régua/escala métrica** (*don't forget the ruler*).

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

- Que três categorias de alvos têm de ser contempladas nas tabelas de catalogação do exercício para o Projeto em Equipa?
- Porque é indispensável incluir uma régua nas fotografias reais tiradas aos dispositivos do laboratório?

## Notas relacionadas

- [[Registo, Etiquetagem e Fotografia Pericial (Regras LabCIF)]]
- [[Princípios e Rota do Manuseamento de Evidência Digital]]
- [[Artefactos Forenses de Dispositivos USB]]
- [[Ficheiros LNK (Shell Links) - Metadados e Formato Binário]]
- [[Capítulo 1 - Método de Investigação]]
