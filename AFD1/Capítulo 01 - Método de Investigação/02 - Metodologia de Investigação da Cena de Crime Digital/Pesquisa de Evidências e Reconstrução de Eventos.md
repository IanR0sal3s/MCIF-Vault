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
atualizado: 2026-10-19
---

# Pesquisa de Evidências e Reconstrução de Eventos

A **Fase 3 (Pesquisa de Evidências)** procura dados que suportem **ou refutem** hipóteses sobre o incidente, combinando pesquisas em sistemas de ficheiros (nomes, conteúdo, datas e comparação de *hashes* com bases como a **NSRL**) e análise de tráfego de rede. Já a **Fase 4 (Reconstrução de Eventos e Relatório)** vai além da simples localização de ficheiros ilícitos: procura determinar **como** os eventos digitais ocorreram (ex.: ação deliberada num navegador web vs. descarga automática por *malware*) e correlacioná-los com eventos físicos, exigindo conhecimento profundo sobre o comportamento de cada versão do sistema operativo e das aplicações.

---

## Fase 3 — Pesquisa de Evidências (*Evidence Searching*)

* **Objetivo**: Encontrar dados que suportem ou refutem hipóteses acerca de um incidente.
* Tipicamente inicia-se com uma **inspeção aos locais comuns** (*survey of common locations*) de acordo com a natureza do incidente:
  * **Hábitos de navegação Web (*Web-browsing habits*)**: analisar a *cache* do navegador Web, o ficheiro de histórico (*history file*) e os marcadores/favoritos (*bookmarks*).
  * **Intrusão em Linux (*Linux intrusion*)**: procurar sinais de um *rootkit* ou a criação de novas contas de utilizador.

> [!IMPORTANT] Regra Científica na Pesquisa
> É fundamental procurar também evidências que **refutem** a nossa hipótese, em vez de procurar apenas evidências que a suportem.

---

## O Processo e as Técnicas de Pesquisa

O processo de pesquisa divide-se em:
1. Definir as **características gerais do objeto** que estamos a procurar.
2. Procurar esse objeto numa **coleção de dados**.
3. Executar dois passos-chave:
   * Determinar **o que** estamos a procurar (*what we are looking for* — ex.: procurar todos os ficheiros com fotografias).
   * Determinar **onde** esperamos encontrá-lo (*where we expect to find it*).

### Técnicas de Pesquisa em Sistemas de Ficheiros e Ficheiros
A maior parte da pesquisa de evidências é realizada num sistema de ficheiros e no interior dos ficheiros, baseando-se em:
1. **Nomes de ficheiros** ou padrões nos seus nomes (*patterns*).
2. **Palavras-chave (*keywords*)** no interior do seu conteúdo.
3. **Dados temporais (*temporal data*)**, tais como a data/hora do último acesso (*last accessed*) ou da última escrita (*last written*).
4. **Valores de *hash*** e respetiva comparação contra uma base de dados de referência:
   * Permite encontrar todos os ficheiros de um determinado tipo ou origem, **mesmo que alguém tenha alterado o seu nome ou extensão**.
   * Base de dados de referência: **National Software Reference Library (NSRL)** do NIST (`http://www.nsrl.nist.gov`).

### Técnicas de Pesquisa em Dados de Rede
* **Cabeçalhos de pacotes (*packet headers*)**: endereços IP, números de porto, protocolo, etc.
* **Palavras-chave (*keywords*)** no conteúdo (*payload*) dos pacotes.

---

## Fase 4 — Reconstrução de Eventos e Relatório (*Event Reconstruction and Report*)

* **Objetivo**: Tentar responder a questões sobre os **eventos digitais** ocorridos no sistema.
* **Limitação da simples presença de ficheiros**:
  * Durante a fase de Pesquisa de Evidências, podemos encontrar vários ficheiros que violam uma lei.
  * Contudo, a mera existência do ficheiro **não responde a questões sobre os eventos** que lhe deram origem.
  * O ficheiro pode ter sido o *efeito* de um evento, mas **qual foi a aplicação que o descarregou?**
    * Foi um navegador Web (*web browser*) operado pelo utilizador?
    * Foi **software malicioso (*malware*)**? — *Vários processos judiciais têm utilizado a presença de malware como argumento de defesa* (*Trojan defense*).
* **Correlação físico-digital**: Pode ser possível correlacionar os eventos digitais com **eventos físicos** (ex.: registos de controlo de acessos físicos ao edifício, câmaras de vigilância, utilização de cartões).

> [!NOTE] Conhecimento do Sistema Operativo e Aplicações
> A reconstrução de eventos exige conhecimento técnico sobre as **aplicações e o Sistema Operativo** instalados no sistema, para que se possam formular hipóteses baseadas nas suas reais capacidades:
> * Diferentes versões do sistema operativo **Windows (XP, 7, 8, 10)** podem originar eventos e artefactos distintos.
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
  * **Diferenças entre Versões do Windows (XP, 7, 8, 10, 11)**: O impacto da versão do SO na reconstrução de eventos é exemplificado pela evolução da [[Application Compatibility e ShimCache (AppCompatCache)|ShimCache]] (que provava execução no Windows XP, tinha `InsertFlag` no Vista–8.1 e deixou de provar execução no Windows 10/11), pela migração do [[Windows Search]] e da [[AmCache - Arquitetura, Hives e Evolução para SQLite|AmCache]] para SQLite no Windows 11, pela perda de relevância da [[Windows Activity Timeline - Arquitetura e Base SQLite|Windows Activity Timeline]] no Windows 11 e pelo novo formato `TabState` do [[Artefacto Forense do Bloco de Notas (Notepad Windows 11)]].

---

## Perguntas de revisão

- Que artefactos devem ser prioritariamente inspecionados num caso de análise de hábitos de navegação Web versus uma intrusão em Linux?
- Quais são os quatro critérios de pesquisa de ficheiros num sistema de ficheiros e qual a utilidade da base de dados NSRL?
- Porque é que encontrar um ficheiro ilegal no disco não basta para concluir a Fase 4 (Reconstrução de Eventos)?
- Porque é que a versão exata do Windows ou do navegador Web influencia a reconstrução de eventos?

## Notas relacionadas

- [[Fases da Investigação Forense Digital]]
- [[Preservação do Sistema e Integridade de Dados]]
- [[Diretrizes de Manuseamento - Identificação, Preservação, Isolamento e Correlação]]
- [[Taxonomia dos Artefactos de Execução no Windows]]
- [[Extração da AmCache e Comparação Forense com a ShimCache]]
- [[Application Compatibility e ShimCache (AppCompatCache)]]
- [[Windows Search]]
- [[Artefacto Forense UserAssist]]
- [[Artefactos Forenses de Interação do Utilizador (MRU e TypedPaths)]]
- [[Artefacto Forense ShellBags]]
- [[Caches de Ícones e Miniaturas (IconCache e Thumbcache)]]
- [[Abuso e Vetores de Ataque com Ficheiros LNK]]
- [[Matriz de Correlação Forense e Cronologia de Ativação dos Artefactos]]
- [[Capítulo 1 - Método de Investigação]]
