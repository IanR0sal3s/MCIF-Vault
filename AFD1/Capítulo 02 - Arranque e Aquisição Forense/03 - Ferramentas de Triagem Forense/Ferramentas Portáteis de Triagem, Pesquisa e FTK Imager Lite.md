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
atualizado: 2026-11-11
---

# Ferramentas Portáteis de Triagem, Pesquisa e FTK Imager Lite

Na triagem forense em **WinFE** ou sistemas *live*, utilitários portáteis como **Agent Ransack**, ferramentas da **PortableFreeware** e o **FTK Imager Lite** pesquisam e extraem artefactos sem instalação.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema / Método)**: Instalar software num equipamento sob investigação altera o Registry e sobrescreve setores livres; aplicações portáteis executam diretamente a partir de uma pen USB ou imagem WinFE sem deixar rasto de instalação.
> * **Porque importa (Forense)**: Permite realizar pesquisa rápida com *regex* dentro de documentos (**Agent Ransack**), extrair credenciais e artefactos específicos (**Portable Forensic Tools**) e copiar ficheiros trancados pelo kernel, detetar fluxos **ADS** e adquirir disco/RAM (**FTK Imager Lite**).
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **`Agent Ransack`**: Suporta expressões booleanas, *Perl regex*, filtros por tamanho/datas (*Modified/Created/Accessed*) e pesquisa no interior de ficheiros **MS Office** e **LibreOffice**.
>   * **`FTK Imager Lite`**: Corre como aplicação portátil ideal para **WinFE**; lê diretamente ao nível dos setores para exportar hives bloqueados (`SAM`, `SYSTEM`, `SOFTWARE`, `NTUSER.DAT`), detetar ficheiros eliminados (cruz vermelha), identificar **ADS**, montar `.E01` e adquirir disco e RAM.
>   * **7 Ferramentas Portáteis da Aula**: `DataProtectionDecryptor`, `JumpListsView`, `Windows File Analyzer`, `BinText`, `Data Converter`, `EXIF Viewer` e `eMule MET Viewer`.

---

## 1. Ferramenta de Pesquisa de Ficheiros: *Agent Ransack*

* **Página oficial**: [Agent Ransack (Mythicsoft)](https://www.mythicsoft.com/agentransack/)
* **Descrição**: Programa gratuito para localizar ficheiros no PC local ou em unidades de rede.
* **Características Técnicas para Triagem**:
  * **Pesquisa rápida** com menor tempo de espera face à pesquisa nativa do sistema.
  * **Capacidades avançadas de pesquisa**: Suporta **expressões booleanas (*Boolean expressions*)** e **expressões regulares Perl (*Perl regex*)**, bem como filtros por tamanho e intervalos de datas (*Modified / Created / Accessed*).
  * **Suporte a formatos de documentos**: Lê e pesquisa diretamente no interior de formatos de ficheiros do **Microsoft Office** e do **LibreOffice** (exibindo no painel inferior as linhas exatas onde o termo foi encontrado).

---

## 2. Aplicações Portáteis de Triagem (*Portable Forensic Tools*)

As aplicações portáteis (executáveis autónomos que não requerem instalação no sistema analisado) são ideais para transportar numa pen USB forense ou integrar no **WinFE**. O repositório de referência indicado na aula é [PortableFreeware](https://www.portablefreeware.com).

| Ferramenta Portátil | Função Pericial na Triagem |
| :--- | :--- |
| **DataProtectionDecryptor** | Desencripta palavras-passe de contas do Microsoft Outlook, ficheiros de credenciais do Windows (*Windows Credentials*), chaves de redes sem fios, palavras-passe em algumas versões do Internet Explorer, e palavras-passe e *cookies* do navegador Google Chrome. |
| **JumpListsView** | Exibe a informação armazenada pelas *Jump Lists* do Windows (histórico de ficheiros abertos por aplicação). |
| **Windows File Analyzer** | Descodifica e analisa artefactos do sistema para disponibilizar informação armazenada em *cache* (como ficheiros de Prefetch, atalhos LNK, `Thumbs.db` e `Index.dat`). |
| **BinText** | Extrai *strings* de texto (ASCII e Unicode) a partir de ficheiros binários (útil para triagem rápida de executáveis suspeitos ou *dumps*). |
| **Data Converter** | Converte números, valores hexadecimais ou datas/timestamps entre diferentes formatos de representação. |
| **EXIF Viewer** | Exibe metadados **EXIF** embutidos em imagens `JPEG` (modelo da câmara/telemóvel, data/hora do disparo, coordenadas GPS). |
| **eMule MET Viewer** | Apresenta informações diversas extraídas dos ficheiros `.met` do cliente de partilha *peer-to-peer* eMule (histórico de *downloads* e partilhas). |

---

## 3. Ferramenta Multifunções: *FTK Imager Lite*

* **Página oficial**: [FTK Imager (Exterro)](https://www.exterro.com/ftk-product-downloads/ftk-imager-4-7-3-81)
* **Perfil Geral**: Ferramenta extremamente poderosa e intuitiva que **corre como aplicação portátil**, tornando-a **ideal para incluir no ambiente WinFE**.

### Capacidades de Triagem e Aquisição do FTK Imager Lite

1. **Pesquisar ficheiros** na árvore do sistema de ficheiros.
2. **Procurar ficheiros apagados** (identificados com um ícone de cruz vermelha na árvore de evidências).
3. **Copiar ficheiros protegidos/bloqueados** (ex.: ficheiros de *cache* e *hives* do Registry) — como lê diretamente a estrutura do sistema de ficheiros (MFT/FAT), permite exportar `SAM`, `SYSTEM`, `SOFTWARE`, `NTUSER.DAT` ou bases de dados em uso mesmo num sistema *live*.
4. **Identificar ADS (*Alternate Data Stream*)** — fluxos de dados alternativos do sistema de ficheiros NTFS frequentemente usados para ocultar *payloads* ou guardar o `Zone.Identifier` de ficheiros descarregados da Internet.
5. **Adquirir dispositivos de armazenamento e memória RAM**.
6. **Montar ficheiros de imagem `E01`** para inspeção imediata.

---

## Implicações Forenses

* **Execução sem Instalação (Pegada Mínima)**: Na análise *live* ou num ambiente *WinFE*, instalar software altera o Registry e centenas de setores de disco. O uso de ferramentas portáteis (*FTK Imager Lite*, *JumpListsView*, *Agent Ransack*) a partir de um suporte externo garante que o perito obtém visibilidade imediata sem instalar pacotes no sistema.
* **Cópia de Artefactos Trancados pelo Kernel**: Quando não é possível desligar um servidor para aquisição *post-mortem* (ver [[Investigação Forense Digital - Análise Live vs Post-Mortem]]), o **FTK Imager Lite** permite realizar uma recolha cirúrgica (*logical/file triage*) copiando os ficheiros do Windows Registry, `$MFT`, `$UsnJrnl` e bases de dados de eventos/telemetria que o Windows Explorer recusa copiar por estarem abertos pelo sistema.

---

## Além da aula

* **Pontes Diretas com Artefactos e Ferramentas Estudados em [[00 ASSI|ASSI]] e [[00 AFD1|AFD1]]**:
  * **`JumpListsView` vs. `JLECmd`**: O utilitário portátil `JumpListsView` (da NirSoft) listado na aula analisa exatamente os ficheiros `*.automaticDestinations-ms` e `*.customDestinations-ms` estudados em [[Jump Lists - Arquitetura, AppIDs e Carving]] (Bloco 12 de ASSI). Enquanto o `JumpListsView` é excelente para uma visualização rápida em GUI das entradas ativas, a ferramenta `JLECmd` de Eric Zimmerman estudada em ASSI permite adicionalmente fazer *file carving* de entradas eliminadas no espaço livre dos contentores OLE/CFB.
  * **`BinText` e `Data Converter` vs. Capítulo 3 de AFD1 e Capítulo 3 de ASSI**: O funcionamento do `BinText` baseia-se no reconhecimento de sequências de bytes válidas nas tabelas [[Codificação de Caracteres - ASCII, Latin-1 e Unicode|ASCII, Latin-1 e UTF-16]], articulando-se diretamente com os utilitários de linha de comandos estudados no [[Capítulo 3 - YARA - MOTW - Strings]] de ASSI ([[Conceito de Strings e Comando strings em Unix-Linux]], [[Extração de Strings no Windows - Sysinternals strings e Swiss File Knife (sfk)]] e [[Eric Zimmerman bstrings - Parâmetros, Expressões Regulares e Exercícios]]), enquanto o `Data Converter` automatiza as conversões estudadas em [[Sistemas de Numeração e Conversão entre Bases]], [[Endianness e Ordem de Armazenamento]] e [[Timestamps e Épocas Temporais (UNIX Epoch vs. Windows FILETIME)]].
  * **Inspeção de Alternate Data Streams (ADS) e Triagem de IOCs**: A capacidade do *FTK Imager Lite* de enumerar fluxos alternativos no NTFS complementa a análise de [[Alternate Data Streams (ADS) no NTFS - Arquitetura, Manipulação em CMD e PowerShell]], [[Ferramentas Gráficas de Análise de ADS e Caso de Estudo WastedLocker]] e [[Mark of the Web (MOTW) e Zone.Identifier - Formato, Zonas URLZONE e Verbosidade dos Browsers]], enquanto a triagem portátil de *malware* e IOCs é potenciada pelo [[Scanner de IOCs LOKI (Versão Python) - Métodos de Deteção e Configuração]], [[Loki-RS (Versão Rust) - Compilação, Atualização e Parâmetros CLI]] e regras [[YARA - Introdução, Estrutura de Regras, Metadados e Condições|YARA]].
  * **`Agent Ransack` vs. `Windows Search`**: Enquanto na nota [[Windows Search]] (ASSI) o perito analisa post-mortem a base de dados `Windows.edb` / `.db` para descobrir o que o sistema indexou no passado, o `Agent Ransack` realiza uma pesquisa ativa em tempo real sem depender do serviço `WSearch` do Windows (que até ignora pastas de sistema ou ficheiros não indexados) e suporta expressões regulares como referido em [[Pesquisa de Evidências e Reconstrução de Eventos]].
  * **Triagem Temporal Complementar**: Juntamente com estas ferramentas portáteis da NirSoft, recorde-se o utilitário [[LastActivityView e Reconstituição Temporal Live|LastActivityView]] estudado no Bloco 09 de ASSI para construir rapidamente uma cronologia em sistemas *live*.

---

## Perguntas de revisão

1. **Que vantagens oferece o *Agent Ransack* para a pesquisa forense de ficheiros em comparação com uma pesquisa simples por nome?**

> [!success]- Ver Resposta
> É mais rápido do que a pesquisa nativa do sistema, pesquisa em unidades locais e de rede utilizando **expressões booleanas**, **expressões regulares Perl (*Perl regex*)** e filtros por tamanho/datas (*Modified / Created / Accessed*), e consegue ler e pesquisar diretamente no interior de documentos **Microsoft Office** e **LibreOffice**, exibindo as linhas exatas de correspondência.

2. **Indique a finalidade pericial das ferramentas portáteis `DataProtectionDecryptor`, `JumpListsView`, `BinText` e `Data Converter`.**

> [!success]- Ver Resposta
> * **`DataProtectionDecryptor`**: Desencripta palavras-passe do Outlook, *Windows Credentials*, chaves Wi-Fi e palavras-passe/cookies do Chrome e de versões do Internet Explorer.
> * **`JumpListsView`**: Apresenta o histórico de ficheiros abertos por aplicação armazenado nas *Jump Lists* do Windows.
> * **`BinText`**: Extrai *strings* ASCII e Unicode de ficheiros binários.
> * **`Data Converter`**: Converte números, valores hexadecimais e datas/timestamps entre diferentes formatos de representação.

3. **Porque é que o *FTK Imager Lite* é considerado ideal para integrar num ambiente *WinFE* e que operações essenciais permite realizar durante a triagem?**

> [!success]- Ver Resposta
> Porque funciona como **aplicação portátil** sem necessitar de instalação. Permite pesquisar ficheiros, identificar ficheiros eliminados (cruz vermelha), **copiar ficheiros protegidos/bloqueados pelo sistema** (como *hives* do Registry e caches), identificar **Alternate Data Streams (ADS)**, adquirir dispositivos de armazenamento e **memória RAM**, e montar ficheiros de imagem **`.E01`**.

4. **Por que razão as ferramentas portáteis são preferíveis a instaladores tradicionais numa análise *live* ou em ambiente *WinFE*?**

> [!success]- Ver Resposta
> Porque executam diretamente a partir do suporte externo sem escrever entradas de instalação no Windows Registry nem sobrescrever setores livres no disco suspeito, mantendo a pegada forense mínima e preservando a integridade da evidência.

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
- [[Timestamps e Épocas Temporais (UNIX Epoch vs. Windows FILETIME)]]
- [[Capítulo 2 - Arranque e Aquisição Forense]]
