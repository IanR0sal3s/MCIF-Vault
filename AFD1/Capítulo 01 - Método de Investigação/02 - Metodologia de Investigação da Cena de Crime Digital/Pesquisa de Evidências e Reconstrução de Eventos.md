---
title: Pesquisa de Evidências e Reconstrução de Eventos
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Análise Forense Digital I
sigla_uc: AFD1
capitulo: 1
bloco: 2
fonte_aula: MCIF – Digital Forensic Analysis 1 - Investigation Method.pdf
tags:
  - afd1
  - forense
  - pesquisa-evidencias
  - reconstrucao-eventos
  - nsrl
  - nist
aliases:
  - Evidence Searching
  - Event Reconstruction
  - NSRL
  - National Software Reference Library
atualizado: 2026-11-11
---

# Pesquisa de Evidências e Reconstrução de Eventos

A **pesquisa de evidências** localiza ficheiros e tráfego de rede com apoio de bases como a **NSRL**, enquanto a **reconstrução de eventos** apura que aplicação ou ação originou cada vestígio.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Método / Sistema)**: Localizar um ficheiro proibido num sistema de ficheiros apenas revela um efeito; só a combinação de pesquisas orientadas com conhecimento sobre o comportamento das aplicações e do sistema operativo explica o evento causal.
> * **Porque importa (Forense / Tribunal)**: Permite filtrar rapidamente centenas de milhares de ficheiros legítimos com conjuntos de *hashes* (**NSRL**) e sustentar ou refutar argumentos de defesa como a *Trojan Defense* perante um tribunal.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Pesquisa para refutação**: procurar também evidências que **refutem** a hipótese inicial, nunca apenas vestígios que a confirmem.
>   * **Valor dos *hashes* com a NSRL**: identifica ficheiros conhecidos **mesmo que o nome ou extensão tenham sido alterados**.
>   * **Impacto das versões de SO e software**: versões distintas do Windows (`XP`, `7`, `8`, `10`) e de navegadores (`Firefox`, `Chrome`) geram artefactos diferentes.

---

## Fase 3 — Pesquisa de Evidências

* **Objetivo**: Encontrar dados que suportem ou refutem hipóteses acerca de um incidente.
* Tipicamente inicia-se com uma **inspeção aos locais comuns** de acordo com a natureza do incidente:

| Natureza do Incidente | Locais Comuns e Artefactos Prioritários |
| :--- | :--- |
| **Hábitos de navegação Web** | *Cache* do navegador Web, ficheiro de histórico e marcadores/favoritos |
| **Intrusão em Linux** | Sinais de um *rootkit* e criação de novas contas de utilizador |

> [!IMPORTANT] Regra Científica na Pesquisa
> É fundamental procurar também evidências que **refutem** a nossa hipótese, em vez de procurar apenas evidências que a suportem.

---

## O Processo e as Técnicas de Pesquisa

O processo de pesquisa divide-se em:

1. Definir as **características gerais do objeto** procurado.
2. Procurar esse objeto numa **coleção de dados**.
3. Executar dois passos-chave:
   * Determinar **o que** estamos a procurar (ex.: procurar todos os ficheiros com fotografias).
   * Determinar **onde** esperamos encontrá-lo.

| Domínio de Pesquisa | Critérios e Técnicas Operacionais | Finalidade / Notas Técnicas |
| :--- | :--- | :--- |
| **Sistemas de Ficheiros e Ficheiros** | **Nomes de ficheiros** ou padrões nos nomes | Filtragem direta por designação ou extensão |
| **Sistemas de Ficheiros e Ficheiros** | **Palavras-chave** no conteúdo interno | Descoberta de strings relevantes dentro dos ficheiros |
| **Sistemas de Ficheiros e Ficheiros** | **Dados temporais** (último acesso, última escrita) | Delimitação de atividade numa janela horária |
| **Sistemas de Ficheiros e Ficheiros** | **Valores de *hash*** comparados com base de referência | Identifica ficheiros mesmo após mudança de nome/extensão; referência: [National Software Reference Library (NSRL) — NIST](http://www.nsrl.nist.gov) |
| **Dados de Rede** | **Cabeçalhos de pacotes** | Endereços IP, números de porto e protocolo |
| **Dados de Rede** | **Palavras-chave** no conteúdo (*payload*) | Identificação de comandos, transferências ou termos nos pacotes |

---

## Fase 4 — Reconstrução de Eventos e Relatório

* **Objetivo**: Tentar responder a questões sobre os **eventos digitais** ocorridos no sistema.
* **Limitação da simples presença de ficheiros**:
  * Durante a Pesquisa de Evidências, podem encontrar-se vários ficheiros que violam uma lei.
  * Contudo, a mera existência do ficheiro **não responde a questões sobre os eventos** que lhe deram origem.
  * O ficheiro pode ter sido o *efeito* de um evento, mas **qual foi a aplicação que o descarregou?**
    * Foi um navegador Web operado pelo utilizador?
    * Foi *malware*? — *Vários processos judiciais têm utilizado a presença de malware como argumento de defesa* (***Trojan Defense***).
* **Correlação físico-digital**: Pode ser possível correlacionar os eventos digitais com **eventos físicos** (ex.: registos de controlo de acessos físicos ao edifício, câmaras de vigilância, utilização de cartões).

> [!NOTE] Conhecimento do Sistema Operativo e Aplicações
> A reconstrução de eventos exige conhecimento técnico sobre as **aplicações e o Sistema Operativo** instalados no sistema, para formular hipóteses baseadas nas suas reais capacidades:
> * Diferentes versões do sistema operativo **Windows (`XP`, `7`, `8`, `10`)** podem originar eventos e artefactos distintos.
> * Diferentes versões dos navegadores **Firefox** ou **Chrome** podem produzir comportamentos e registos diferentes.

---

## Implicações Forenses

* **Redução de Ruído com NSRL (*Hash Sets*)**: Na análise de um disco com centenas de milhares de ficheiros, comparar os *hashes* contra a base NSRL permite filtrar imediatamente ficheiros legítimos conhecidos do sistema operativo e de aplicações comerciais (*known good*), reduzindo drasticamente o volume de ficheiros a inspecionar manualmente, ou detetar imediatamente ficheiros ilícitos conhecidos (*known bad*).
* **Refutação da Defesa por Malware (*Trojan Defense*)**: Para provar se um ficheiro ilícito foi descarregado intencionalmente pelo utilizador ou por um *trojan*, o perito tem de reconstruir a cadeia de eventos (histórico do browser, *Referer*, cliques, ausência de processos maliciosos ativos na época e correlação com sessões interativas de teclado/rato).

---

## Além da aula

* **Articulação com os Artefactos do Windows Estudados em [[00 ASSI|ASSI]]**:
  * **Pesquisa por Palavras-Chave e Metadados (Fase 3)**: Além da pesquisa bruta no sistema de ficheiros, o índice do [[Windows Search]] (`Windows.edb` em ESE no W10 ou `Windows.db` em SQLite3 no W11) preserva nomes, caminhos, conteúdos indexados e metadados temporais mesmo após a eliminação dos ficheiros originais. De igual modo, os hashes `SHA-1` guardados na [[AmCache - Arquitetura, Hives e Evolução para SQLite|AmCache]] permitem cruzar executáveis apagados ou renomeados contra bases de reputação ([[Extração da AmCache e Comparação Forense com a ShimCache]]).
  * **Existência vs. Execução e Interação Consciente (Fase 4 — Reconstrução de Eventos)**: A advertência de que *"a mera existência do ficheiro não responde a questões sobre os eventos que lhe deram origem"* corresponde exatamente à **Regra de Ouro** estudada na [[Taxonomia dos Artefactos de Execução no Windows]]:
    * **Mera Presença/Existência**: Entradas na [[Application Compatibility e ShimCache (AppCompatCache)|ShimCache]] ou na [[AmCache - Arquitetura, Hives e Evolução para SQLite|AmCache]] provam apenas que o ficheiro existiu no disco, e miniaturas na [[Caches de Ícones e Miniaturas (IconCache e Thumbcache)|Thumbcache]] provam apenas que a pasta foi enumerada pelo Explorer (não provando visualização consciente).
    * **Prova de Ação Deliberada do Utilizador (*Refutação de Trojan Defense*)**: Para demonstrar interação humana direta na interface gráfica (em oposição a uma descarga/execução automática em segundo plano por *malware*), o perito correlaciona o [[Artefacto Forense UserAssist]] (contadores de execução GUI e tempo de foco da janela), [[Artefactos Forenses de Interação do Utilizador (MRU e TypedPaths)|RunMRU, RecentDocs, ComDlg32 e TypedPaths]], [[Artefacto Forense ShellBags|ShellBags]] (navegação interativa em pastas e arquivos comprimidos), [[Jump Lists - Arquitetura, AppIDs e Carving|Jump Lists]] e [[Ficheiros LNK (Shell Links) - Metadados e Formato Binário|atalhos LNK na pasta Recent]].
    * **Análise de Vetores de Engenharia Social**: Quando a defesa alega ação de *malware*, a inspeção de [[Abuso e Vetores de Ataque com Ficheiros LNK|atalhos LNK maliciosos]] (ex.: campanhas *Emotet* com ícones forjados e comandos truncados a 256 caracteres na GUI) permite esclarecer exatamente como a infeção foi despoletada.
  * **Diferenças entre Versões do Windows (`XP`, `7`, `8`, `10`, `11`) e Proveniência Web (MOTW)**: O impacto da versão do SO e do navegador Web na reconstrução de eventos é exemplificado pela evolução da [[Application Compatibility e ShimCache (AppCompatCache)|ShimCache]] (que provava execução no Windows XP, tinha `InsertFlag` no Vista–8.1 e deixou de provar execução no Windows 10/11), pela migração do [[Windows Search]] e da [[AmCache - Arquitetura, Hives e Evolução para SQLite|AmCache]] para SQLite no Windows 11, pela perda de relevância da [[Windows Activity Timeline - Arquitetura e Base SQLite|Windows Activity Timeline]] no Windows 11, pelo novo formato `TabState` do [[Artefacto Forense do Bloco de Notas (Notepad Windows 11)]] e pela diferença de verbosidade na ADS `Zone.Identifier` ([[Mark of the Web (MOTW) e Zone.Identifier - Formato, Zonas URLZONE e Verbosidade dos Browsers]] e [[Exceções à MOTW (Ficheiros Compactados, 7-Zip, certutil LOLBin) e Microsoft Defender SmartScreen]]).
  * **Pesquisa Automatizada de Padrões, Strings e IOCs ([[Capítulo 3 - YARA - MOTW - Strings]])**: Na Fase 3 (Pesquisa de Evidências), a pesquisa por expressões regulares, assinaturas binárias e hashes é operacionalizada com [[Eric Zimmerman bstrings - Parâmetros, Expressões Regulares e Exercícios|bstrings]], regras [[YARA - Introdução, Estrutura de Regras, Metadados e Condições|YARA]], [[YARA-X (Reimplementação em Rust) e Ferramenta CLI yr|YARA-X]] e os scanners [[Scanner de IOCs LOKI (Versão Python) - Métodos de Deteção e Configuração|LOKI]] e [[Loki-RS (Versão Rust) - Compilação, Atualização e Parâmetros CLI|Loki-RS]].

---

## Perguntas de revisão

1. **Que artefactos devem ser prioritariamente inspecionados num caso de análise de hábitos de navegação Web versus uma intrusão em Linux?**

> [!success]- Ver Resposta
> Nos **hábitos de navegação Web**, inspeciona-se a *cache* do navegador, o ficheiro de histórico e os marcadores/favoritos. Numa **intrusão em Linux**, procuram-se sinais de *rootkits* e a criação de novas contas de utilizador.

2. **Quais são os quatro critérios de pesquisa de ficheiros num sistema de ficheiros e qual a utilidade da base de dados NSRL?**

> [!success]- Ver Resposta
> Os quatro critérios são: **nomes de ficheiros** (ou padrões), **palavras-chave** no conteúdo, **dados temporais** (último acesso/escrita) e **valores de *hash***. A base **NSRL (NIST)** permite identificar ficheiros conhecidos mesmo que o seu nome ou extensão tenham sido alterados, filtrando ficheiros legítimos conhecidos (*known good*).

3. **Porque é que encontrar um ficheiro ilegal no disco não basta para concluir a Fase 4 (Reconstrução de Eventos)?**

> [!success]- Ver Resposta
> Porque a simples presença do ficheiro é apenas o *efeito* e não explica **como** surgiu (ex.: navegador operado pelo utilizador vs. descarga automática por *malware*, argumento típico da *Trojan Defense*), sendo necessário reconstruir os eventos digitais e correlacioná-los com eventos físicos.

4. **Porque é que a versão exata do Windows ou do navegador Web influencia a reconstrução de eventos?**

> [!success]- Ver Resposta
> Porque diferentes versões de sistemas operativos (ex.: Windows `XP`, `7`, `8`, `10`) e de navegadores (`Firefox`, `Chrome`) têm capacidades distintas e geram artefactos, registos e comportamentos diferentes, exigindo hipóteses ajustadas à versão concreta instalada.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Preservação do Sistema e Integridade de Dados]] | `mesmo bloco` |
| **Seguinte** | [[Exercícios Práticos - Integridade de Dados e Hashes]] | `mesmo bloco` |
| **Índice** | [[Capítulo 1 - Método de Investigação]] · [[00 AFD1]] | `Bloco 02` |

### Conceitos Relacionados

* [[Fases da Investigação Forense Digital]] · `mesmo bloco`
* [[Diretrizes de Manuseamento - Identificação, Preservação, Isolamento e Correlação]] · `Bloco 03`
* [[Taxonomia dos Artefactos de Execução no Windows]] · `ASSI · Cap. 1`
* [[Extração da AmCache e Comparação Forense com a ShimCache]] · `ASSI · Cap. 1`
* [[Application Compatibility e ShimCache (AppCompatCache)]] · `ASSI · Cap. 1`
* [[Windows Search]] · `ASSI · Cap. 1`
* [[Artefacto Forense UserAssist]] · `ASSI · Cap. 1`
* [[Artefactos Forenses de Interação do Utilizador (MRU e TypedPaths)]] · `ASSI · Cap. 1`
* [[Artefacto Forense ShellBags]] · `ASSI · Cap. 1`
* [[Caches de Ícones e Miniaturas (IconCache e Thumbcache)]] · `ASSI · Cap. 1`
* [[Abuso e Vetores de Ataque com Ficheiros LNK]] · `ASSI · Cap. 1`
* [[Matriz de Correlação Forense e Cronologia de Ativação dos Artefactos]] · `ASSI · Cap. 1`
