---
title: Ferramentas Portáteis de Triagem, Pesquisa e FTK Imager Lite
tipo: ferramenta
mestrado: Cibersegurança e Informática Forense
uc: Análise Forense Digital I
sigla_uc: AFD1
capitulo: 2
bloco: 3
fonte_aula: MCIF – Digital Forensic Analysis 1 - Forensic Boot.pdf
tags:
  - afd1
  - forense
  - triagem
  - ransack
  - portable-tools
  - ftk-imager
  - ads
  - jumplists
aliases:
  - Agent Ransack
  - RanSack
  - Portable Forensic Tools
  - DataProtectionDecryptor
  - JumpListsView
  - FTK Imager Lite
  - Alternate Data Stream
atualizado: 2026-10-20
---

# Ferramentas Portáteis de Triagem, Pesquisa e FTK Imager Lite

Para além da análise focada no Windows Registry, a triagem forense em ambientes de arranque como o **WinFE** (ou em intervenções *live* controladas) recorre a ferramentas de pesquisa rápida de ficheiros (**Agent Ransack**), coleções de utilitários portáteis especializados (**Portable Forensic Tools**) e ferramentas multifunções portáteis de referência como o **FTK Imager Lite**, capaz de extrair ficheiros bloqueados pelo sistema operativo, detetar *Alternate Data Streams (ADS)*, montar imagens `.E01` e adquirir tanto dispositivos de armazenamento como memória RAM.

---

## 1. Ferramenta de Pesquisa de Ficheiros: *RanSack* (*Agent Ransack*)

* **Página oficial**: `https://www.mythicsoft.com/agentransack/`
* **Descrição**: Programa gratuito (*free software*) para localizar ficheiros no PC local ou em unidades de rede (*network drives*).
* **Características Técnicas para Triagem**:
  * **Pesquisa rápida** (*fast search* — menor tempo de espera face à pesquisa nativa do sistema).
  * **Capacidades avançadas de pesquisa**: Suporta **expressões booleanas (*Boolean expressions*)** e **expressões regulares Perl (*Perl regex*)**, bem como filtros por tamanho e intervalos de datas (*Modified / Created / Accessed*).
  * **Suporte a formatos de documentos**: Lê e pesquisa diretamente no interior de formatos de ficheiros do **Microsoft Office** e do **LibreOffice** (exibindo no painel inferior as linhas exatas onde o termo foi encontrado).

---

## 2. Aplicações Portáteis de Triagem (*Portable Forensic Tools*)

As aplicações portáteis (executáveis autónomos que não requerem instalação no sistema analisado) são ideais para transportar numa pen USB forense ou integrar no **WinFE**. O repositório de referência indicado na aula é `https://www.portablefreeware.com`.

| Ferramenta Portátil | Função Pericial na Triagem |
| :--- | :--- |
| **DataProtectionDecryptor** | Desencripta palavras-passe de contas do Microsoft Outlook, ficheiros de credenciais do Windows (*Windows Credentials*), chaves de redes sem fios (*wireless network keys*), palavras-passe em algumas versões do Internet Explorer, e palavras-passe e *cookies* do navegador Google Chrome. |
| **JumpListsView** | Exibe a informação armazenada pelas *Jump Lists* do Windows (histórico de ficheiros abertos por aplicação). |
| **Windows File Analyzer** | Descodifica e analisa artefactos do sistema para disponibilizar informação armazenada em *cache* (como ficheiros de Prefetch, atalhos LNK, Thumbs.db e Index.dat). |
| **BinText** | Extrai *strings* de texto (ASCII e Unicode) a partir de ficheiros binários (útil para triagem rápida de executáveis suspeitos ou *dumps*). |
| **Data Converter** | Converte números, valores hexadecimais ou datas/timestamps entre diferentes formatos de representação. |
| **EXIF Viewer** | Exibe metadados **EXIF** embutidos em imagens `JPEG` (modelo da câmara/telemóvel, data/hora do disparo, coordenadas GPS). |
| **eMule MET Viewer** | Apresenta informações diversas extraídas dos ficheiros `.met` do cliente de partilha *peer-to-peer* eMule (histórico de *downloads* e partilhas). |

---

## 3. Ferramenta Multifunções: *FTK Imager Lite*

* **Página de descarga referenciada**: `https://www.exterro.com/ftk-product-downloads/ftk-imager-4-7-3-81`
* **Perfil Geral**: Ferramenta extremamente poderosa e intuitiva (*user friendly*) que **corre como aplicação portátil (*portable application*)**, tornando-a **ideal para incluir no ambiente WinFE**.

### Capacidades de Triagem e Aquisição do FTK Imager Lite
1. **Pesquisar ficheiros** (*search files*) na árvore do sistema de ficheiros.
2. **Procurar ficheiros apagados** (*look for deleted files* — identificados com um ícone de cruz vermelha na árvore de evidências).
3. **Copiar ficheiros protegidos/bloqueados** (*copy files, e.g. cache and registry files*) — como lê diretamente a estrutura do sistema de ficheiros (MFT/FAT), permite exportar os hives `SAM`, `SYSTEM`, `SOFTWARE`, `NTUSER.DAT` ou bases de dados em uso mesmo num sistema *live*.
4. **Identificar ADS (*Alternate Data Stream*)** — fluxos de dados alternativos do sistema de ficheiros NTFS frequentemente usados para ocultar *payloads* ou guardar o `Zone.Identifier` de ficheiros descarregados da Internet.
5. **Adquirir dispositivos de armazenamento e memória RAM** (*acquire storage devices and RAM*).
6. **Montar ficheiros de imagem `E01`** (*mount E01 files*) para inspeção imediata.

---

## Implicações Forenses

* **Execução sem Instalação (Pegada Mínima)**: Na análise *live* ou num ambiente *WinFE*, instalar software altera o Registry e centenas de setores de disco. O uso de ferramentas portáteis (*FTK Imager Lite*, *JumpListsView*, *Agent Ransack*) a partir de um suporte externo garante que o perito obtém visibilidade imediata sem instalar pacotes no sistema.
* **Cópia de Artefactos Trancados pelo Kernel**: Quando não é possível desligar um servidor para aquisição *post-mortem* (ver [[Investigação Forense Digital - Análise Live vs Post-Mortem]]), o **FTK Imager Lite** permite realizar uma recolha cirúrgica (*logical/file triage*) copiando os ficheiros do Windows Registry, `$MFT`, `$UsnJrnl` e bases de dados de eventos/telemetria que o Windows Explorer recusa copiar por estarem abertos pelo sistema.

---

## Além da aula

* **Pontes Diretas com Artefactos e Ferramentas Estudados em [[00 ASSI|ASSI]] e [[00 AFD1|AFD1]]**:
  * **`JumpListsView` vs. `JLECmd`**: O utilitário portátil `JumpListsView` (da NirSoft) listado na aula analisa exatamente os ficheiros `*.automaticDestinations-ms` e `*.customDestinations-ms` estudados em [[Jump Lists - Arquitetura, AppIDs e Carving]] (Bloco 12 de ASSI). Enquanto o `JumpListsView` é excelente para uma visualização rápida em GUI das entradas ativas, a ferramenta `JLECmd` de Eric Zimmerman estudada em ASSI permite adicionalmente fazer *file carving* de entradas eliminadas no espaço livre dos contentores OLE/CFB.
  * **`BinText` e `Data Converter` vs. Capítulo 3 de AFD1**: O funcionamento do `BinText` baseia-se no reconhecimento de sequências de bytes válidas nas tabelas [[Codificação de Caracteres - ASCII, Latin-1 e Unicode|ASCII, Latin-1 e UTF-16]], enquanto o `Data Converter` automatiza as conversões estudadas em [[Sistemas de Numeração e Conversão entre Bases]], [[Endianness e Ordem de Armazenamento]] e [[Representação Forense de Data e Hora (Timestamps e SQLite)]].
  * **`Agent Ransack` vs. `Windows Search`**: Enquanto na nota [[Windows Search]] (ASSI) o perito analisa post-mortem a base de dados `Windows.edb` / `.db` para descobrir o que o sistema indexou no passado, o `Agent Ransack` realiza uma pesquisa ativa em tempo real sem depender do serviço `WSearch` do Windows (que até ignora pastas de sistema ou ficheiros não indexados) e suporta expressões regulares como referido em [[Pesquisa de Evidências e Reconstrução de Eventos]].
  * **Triagem Temporal Complementar**: Juntamente com estas ferramentas portáteis da NirSoft, recorde-se o utilitário [[LastActivityView e Reconstituição Temporal Live|LastActivityView]] estudado no Bloco 09 de ASSI para construir rapidamente uma cronologia em sistemas *live*.

---

## Perguntas de revisão

- Que vantagens oferece o *Agent Ransack* para a pesquisa forense de ficheiros em comparação com uma pesquisa simples por nome?
- Indique a finalidade pericial das ferramentas portáteis `DataProtectionDecryptor`, `JumpListsView`, `BinText` e `Data Converter`.
- Porque é que o *FTK Imager Lite* é considerado ideal para integrar num ambiente *WinFE* e que operações essenciais permite realizar durante a triagem?

## Notas relacionadas

- [[Ferramentas de Triagem Forense no Windows Registry (RegistryReport, ForensicUserInfo e WRR)]]
- [[Dispositivos de Arranque Forense - Disquetes DOS, Live CDs Linux, WinFE e USB]]
- [[Ferramentas Gráficas de Aquisição Forense (Guymager, Paladin Toolbox, Tableau Imager e FTK Imager)]]
- [[Pesquisa de Evidências e Reconstrução de Eventos]]
- [[Diretrizes de Manuseamento - Identificação, Preservação, Isolamento e Correlação]]
- [[Jump Lists - Arquitetura, AppIDs e Carving]]
- [[Ficheiros LNK (Shell Links) - Metadados e Formato Binário]]
- [[Caches de Ícones e Miniaturas (IconCache e Thumbcache)]]
- [[LastActivityView e Reconstituição Temporal Live]]
- [[Windows Search]]
- [[Codificação de Caracteres - ASCII, Latin-1 e Unicode]]
- [[Representação Forense de Data e Hora (Timestamps e SQLite)]]
- [[Capítulo 2 - Arranque e Aquisição Forense]]
