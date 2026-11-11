---
title: Artefacto Forense ShellBags
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 7
tipo: conceito
tags:
  - assi
  - windows
  - registry
  - shellbags
  - usrclass
  - zimmerman
  - forense
aliases:
  - ShellBags
  - BagMRU
  - Bags
  - SBECmd
  - ShellBags Explorer
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
fontes:
  - "https://www.bleepingcomputer.com/news/microsoft/windows-11-adds-support-for-11-file-archives-including-7-zip-and-rar/"
atualizado: 2026-09-23
---

# Artefacto Forense ShellBags

Estruturas de preferências visuais de pastas (`BagMRU` e `Bags`) armazenadas no hive `USRCLASS.DAT` que documentam o histórico de navegação de diretórios e arquivos comprimidos pelo utilizador.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: O Windows Explorer precisa de memorizar as preferências de visualização de cada pasta (tamanho e posição da janela, modo de ícones/detalhes/miniaturas e coluna de ordenação) para restaurar exatamente o mesmo aspeto gráfico da próxima vez que o utilizador abrir essa pasta.
> * **Porque importa (Forense)**: Como o Windows não apaga o registo `ShellBag` quando uma pasta é eliminada ou uma pen USB é removida, as chaves `BagMRU` e `Bags` (no ficheiro **`USRCLASS.DAT`**) funcionam como um **mapa histórico persistente de todas as pastas locais, partilhas de rede, pens USB e arquivos compactados (`.zip`, e no W11 22H2+ também `.7z`/`.rar`) navegados pelo utilizador**.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **O que PROVA vs. O que NÃO PROVA**: Os ShellBags provam conclusivamente a **navegação/abertura do contentor (a pasta ou o arquivo comprimido)** na interface gráfica, mas **não provam que os ficheiros individuais dentro dessa pasta foram abertos ou lidos** (para isso é necessário correlacionar com `RecentDocs`, ficheiros `.lnk` ou `UserAssist`).
>   * **Expansão no Windows 11 22H2 (Setembro de 2023)**: Além dos `.zip` (suportados desde o Windows Me), o Explorador do Windows 11 passou a abrir nativamente **11 novos formatos de arquivo** (incluindo **`.7z`**, **`.rar`**, `.tar.gz` e formatos **ZStandard / ZST**), gerando entradas completas no `ShellBags` quando o utilizador navega dentro deles.

---

## Localização no Registry e Evolução por Versão do Windows

A localização dos ShellBags e a cobertura de ficheiros compactados evoluíram ao longo das versões do Windows:

| Versão do Sistema Operativo | Ficheiro Físico de Hive | Caminho das Chaves (`BagMRU` e `Bags`) | Arquivos Compactados Registados como Pastas |
| :--- | :---: | :--- | :--- |
| **Windows XP** | `NTUSER.DAT` | `HKCU\Software\Microsoft\Windows\ShellNoRoam\BagMRU` (e `\Bags`) | Ficheiros `.zip` (suporte nativo introduzido desde o Windows Me) |
| **Windows 7, 8 e 10** | **`USRCLASS.DAT`** | `HKCU\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\BagMRU` (e `\Bags`) | Ficheiros `.zip` (e `.cab` / `.iso` montados ou abertos no Explorer) |
| **Windows 11 (22H2 — Set. 2023+)** | **`USRCLASS.DAT`** | `HKCU\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\BagMRU` (e `\Bags`) | `.zip` + **11 novos formatos nativos**: **`.7z`**, **`.rar`**, `.tar`, `.tar.gz`, `.tar.bz2`, `.tar.xz`, `.tgz`, `.tbz2`, `.tzst`, `.txz` e algoritmos **ZStandard (ZST)** da Meta |

**Caminho Físico do `USRCLASS.DAT` (Windows 7 a 11):**

```text
C:\Users\<username>\AppData\Local\Microsoft\Windows\UsrClass.dat
```

---

## Arquitetura Interna: `BagMRU` vs. `Bags`

Os ShellBags dividem-se em duas árvores complementares debaixo de `...\Windows\Shell\`:

1. **`BagMRU` (A Árvore de Diretórios)**:
   * Estrutura hierárquica de subchaves indexadas por números inteiros (`0`, `1`, `2`...) que espelha exatamente a árvore de pastas do sistema de ficheiros navegada pelo utilizador.
   * Cada subchave contém valores binários (estruturas `Shell Item ID List` / **`SHITEMID`**), o valor `MRUListEx` (ordem de acesso às subpastas) e o valor **`NodeSlot`**, que funciona como o ponteiro numérico para a subchave correspondente em `Bags`.
2. **`Bags` (As Propriedades Visuais de Renderização)**:
   * Subchaves indexadas pelo número de `NodeSlot` atribuído na `BagMRU`.
   * Armazena os parâmetros gráficos da janela daquela pasta específica: modo de visualização (ícones grandes, lista, detalhes), coluna de ordenação, resolução e coordenadas no ecrã.

---

## ShellBags e Ficheiros Compactados (Arquivos)

Como o Windows Explorer trata arquivos comprimidos suportados nativamente como **pastas virtuais (*Compressed Folders*)**, quando o utilizador faz duplo clique num arquivo para ver o seu conteúdo sem o extrair com programas externos, o Explorer renderiza a vista e **grava entradas `BagMRU`/`Bags` para o arquivo e para as subpastas internas navegadas**:

* **Ficheiros `.zip`**: suporte nativo desde o Windows Me.
* **Novidade de Exame — Windows 11 22H2 (Setembro de 2023)**: A integração da biblioteca `libarchive` no Windows Explorer adicionou suporte nativo de leitura para **11 novos formatos**:
  * Família TAR: `.tar`, `.tar.gz`, `.tar.bz2`, `.tar.xz`, `.tgz`, `.tbz2`, `.tzst`, `.txz`
  * Formatos populares: **`.rar`** e **`.7z`**
  * Compressão **ZStandard (ZST)** desenvolvida pela Meta.
* **Impacto Pericial**: Se um suspeito abrir um arquivo `.7z` ou `.rar` diretamente no Explorador do Windows 11, os nomes das subpastas internas do arquivo ficam perpetuados no `UsrClass.dat`, mesmo que o ficheiro `.7z`/`.rar` seja posteriormente eliminado ou esteja numa pen USB removida.

---

## Anatomia das Ferramentas Forenses de Extração (Eric Zimmerman)

Devido à codificação binária das estruturas `SHITEMID` em hexadecimal, a leitura direta no `regedit.exe` é inviável. Utilizam-se duas ferramentas de referência de **Eric Zimmerman**:

### 1. `SBECmd.exe` (Extração em Linha de Comandos para CSV)
Processa ficheiros `UsrClass.dat` (e `NTUSER.DAT`) extraídos de imagens forenses ou do sistema vivo:

```cmd
sbecmd.exe -d C:\Caminho\Onde\Esta\UsrClass.dat --csv C:\Caminho\Relatorio_CSV
```

* **`sbecmd.exe`**: (*ShellBags Explorer Command Line*) executável CLI de processamento em lote.
* **`-d <Diretório>`**: especifica o diretório que contém os hives de utilizador (`UsrClass.dat` / `NTUSER.DAT`) a analisar.
* **`--csv <Diretório_Saída>`**: gera o relatório tabulado em formato CSV no diretório indicado, contendo caminhos absolutos reconstruídos (`Absolute Path`), tipo de contentor (`Directory`, `Zip file contents`), datas de criação/modificação/acesso embutidas nas estruturas `SHITEMID` e o *LastWriteTime* da chave (`First Interacted` / `Last Interacted`).

### 2. `ShellBags Explorer` (`ShellBagsExplorer.exe` — Interface Gráfica)

* Reconstrói visualmente a árvore exata de pastas que o suspeito viu no Windows Explorer, destacando com ícones e cores distintas as pastas locais, pastas já eliminadas, partilhas de rede, dispositivos USB e o interior de ficheiros compactados.

---

## Conclusão e Limitações Forenses

> [!IMPORTANT] Valor Probatório dos ShellBags (O que Provam vs. O que NÃO Provam)
> * **O que PROVAM**: Provam de forma inequívoca que a conta daquele utilizador solicitou à *shell* do Windows a **abertura e renderização visual de uma determinada pasta (ou arquivo comprimido)** numa determinada janela temporal. Provam que a pasta existiu (mesmo que hoje esteja apagada ou numa pen USB desaparecida) e que o utilizador navegou até ela.
> * **O que NÃO PROVAM**: Os ShellBags documentam apenas a **interação com o contentor (diretório)**. **Não constituem prova pericial de que os ficheiros individuais contidos dentro dessa pasta foram abertos, lidos ou executados**. Para provar a abertura de um ficheiro individual, o perito tem obrigatoriamente de cruzar os ShellBags com artefactos de ficheiro/execução, tais como [[Artefactos Forenses de Interação do Utilizador (MRU e TypedPaths)|RecentDocs]], `ComDlg32`, atalhos `.lnk` ou [[Artefacto Forense UserAssist|UserAssist]].

---

## Perguntas de revisão

1. **Em que ficheiro físico de hive residem os ShellBags no Windows 10 e 11 e qual a função distinta das subchaves `BagMRU` e `Bags`?**

> [!success]- Ver Resposta
> No Windows 7, 8, 10 e 11, os ShellBags residem no ficheiro **`USRCLASS.DAT`** (`C:\Users\<username>\AppData\Local\Microsoft\Windows\UsrClass.dat`), sob `HKCU\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\`. A subchave **`BagMRU`** armazena a estrutura em árvore dos diretórios navegados (através de blocos binários `SHITEMID` e ponteiros `NodeSlot`), enquanto a subchave **`Bags`** armazena as definições visuais de apresentação de cada pasta (modo de ícones, ordenação e posição da janela).

2. **Um suspeito apaga uma pasta comprometedora chamada `D:\Contabilidade_Secreta` que estava numa pen USB e deita a pen fora. Como podem os ShellBags ajudar a investigação e qual o limite probatório deste artefacto em tribunal?**

> [!success]- Ver Resposta
> Como o Windows não remove as entradas de `BagMRU`/`Bags` quando uma pasta é eliminada ou o suporte USB é desconectado, os ShellBags no `USRCLASS.DAT` provam que a pasta `D:\Contabilidade_Secreta` existiu e foi aberta/visualizada no Windows Explorer por aquele utilizador numa data/hora específica. Contudo, o limite probatório é que os ShellBags provam apenas a **navegação na pasta (contentor)**, não provando por si sós que os ficheiros individuais dentro dela foram abertos (o que exige correlação com `RecentDocs`, `.lnk`, etc.).

3. **Que alteração introduzida no Windows 11 versão 22H2 (setembro de 2023) aumentou significativamente o valor forense dos ShellBags na análise de ficheiros comprimidos?**

> [!success]- Ver Resposta
> Até ao Windows 10, o Windows Explorer abria nativamente como pastas virtuais sobretudo ficheiros `.zip`. A partir da atualização de setembro de 2023 do Windows 11 22H2, a Microsoft adicionou suporte nativo no Explorer para **11 novos formatos de arquivos compactados** — incluindo **`.7z`**, **`.rar`**, `.tar.gz` e formatos **ZStandard (ZST)**. Assim, quando um utilizador navega dentro de um `.7z` ou `.rar` no Explorer do Windows 11, são gerados registos completos nos ShellBags.

4. **Qual é a sintaxe do comando de Eric Zimmerman para extrair os ShellBags de uma pasta contendo o ficheiro `UsrClass.dat` para um relatório em formato CSV?**

> [!success]- Ver Resposta
> `sbecmd.exe -d C:\Caminho\Onde\Esta\UsrClass.dat --csv C:\Caminho\Relatorio_CSV` (onde `-d` aponta para o diretório com o hive e `--csv` define o diretório de destino do ficheiro CSV).

## Notas relacionadas

- [[Estrutura e Hives do Windows Registry]]
- [[Ferramentas de Análise e Extração do Registry]]
- [[Artefactos Forenses de Interação do Utilizador (MRU e TypedPaths)]]
- [[Artefactos Forenses de Dispositivos USB]]
- [[Pesquisa de Evidências e Reconstrução de Eventos]]
- [[Investigação Digital e Evidência Digital]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
