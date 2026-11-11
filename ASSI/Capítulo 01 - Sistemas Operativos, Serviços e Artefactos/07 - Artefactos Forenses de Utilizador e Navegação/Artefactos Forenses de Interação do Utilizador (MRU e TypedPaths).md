---
title: Artefactos Forenses de Interação do Utilizador (MRU e TypedPaths)
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
  - mru
  - typedpaths
  - runmru
  - comdlg32
  - recentdocs
  - forense
aliases:
  - Listas MRU
  - Most Recently Used
  - RunMRU
  - RecentDocs
  - ComDlg32
  - TypedPaths
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
fontes:
  - "http://www.nirsoft.net/utils/recent_files_view.html"
atualizado: 2026-09-23
---

# Artefactos Forenses de Interação do Utilizador (MRU e TypedPaths)

Listas **MRU** (*Most Recently Used*) e histórico de navegação no hive `NTUSER.DAT` (`RunMRU`, `RecentDocs`, `ComDlg32` e `TypedPaths`) para reconstituição pericial da atividade intencional do utilizador.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: Para melhorar a usabilidade e rapidez da interface gráfica, o Windows Explorer memoriza os últimos comandos digitados, ficheiros abertos, diretórios usados em caixas de diálogo *Abrir/Guardar* e caminhos escritos na barra de endereços, preenchendo automaticamente listas suspensas (*drop-down menus*).
> * **Porque importa (Forense)**: Como estas listas só são alimentadas por ações interativas diretas na interface, provam **intencionalidade e conhecimento do utilizador** sobre ficheiros, pastas ou comandos específicos — todos centralizados no ficheiro `NTUSER.DAT` (`HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\...`).
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **`MRUList` (Texto) vs. `MRUListEx` (Binário)**: `RunMRU` ordena entradas por letras num valor `REG_SZ` chamado **`MRUList`** (ex.: `"cba"` $\rightarrow$ `'c'` foi o mais recente). Já `RecentDocs` e `ComDlg32` usam números ordenados por blocos de **4 bytes Little-Endian** num valor `REG_BINARY` chamado **`MRUListEx`** (ex.: `02 00 00 00` indica que a entrada `"2"` é a mais recente).
>   * **Timestamp apenas no Topo da Lista**: Como as chaves do Registry só guardam um único *LastWriteTime* por chave, sabemos a data/hora exata em que o **item mais recente** (o 1.º da `MRUList`/`MRUListEx`) foi acedido, e sabemos a ordem relativa dos restantes, mas não o timestamp individual de cada item anterior.

---

## Mapa Rápido: "Ação do Utilizador / O que procuro?" $\rightarrow$ "Chave do Registry"

Todas as chaves abaixo residem no hive pessoal **`NTUSER.DAT`** sob `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\`:

| Ação do Utilizador / O que procuro? | Subchave em `...\Explorer\` | Nomes dos Valores | Valor de Ordenação Temporal | Limitação / Detalhe Pericial |
| :--- | :--- | :---: | :---: | :--- |
| Digitou um comando na caixa **Executar (`Win+R`)** | **`RunMRU`** | Letras (`a`, `b`, `c`...) com sufixo `\1` | **`MRUList`** (`REG_SZ`, string de letras) | Não regista comandos escritos dentro de uma janela `cmd.exe` já aberta, apenas na caixa `Win+R`. |
| Abriu um ficheiro ou pasta via **Windows Explorer** | **`RecentDocs`** (e subchaves `\.ext`) | Números (`0`, `1`, `2`...) em `REG_BINARY` | **`MRUListEx`** (`REG_BINARY`, inteiros de 4 bytes LE) | Organizado na raiz e em subchaves por extensão (`.pdf`, `.docx`, `.zip`). |
| Abriu ou guardou um ficheiro numa **caixa de diálogo padrão (*Open/Save*)** | **`ComDlg32\OpenSavePidlMRU`** | Números (`0`, `1`, `2`...) por extensão | **`MRUListEx`** (`REG_BINARY`, inteiros de 4 bytes LE) | Em apps modernas MSIX (ex.: Notepad no W11), fica no `User.dat` da pasta `Helium`. |
| Qual o **executável que invocou a caixa de diálogo** e em que pasta estava? | **`ComDlg32\LastVisitedPidlMRU`** | Números (`0`, `1`, `2`...) | **`MRUListEx`** (`REG_BINARY`, inteiros de 4 bytes LE) | Associa diretamente o nome do `.exe` ao último diretório navegado nessa janela. |
| Digitou um caminho ou comando na **barra de endereços do Explorer** | **`TypedPaths`** | `url1`, `url2`, `url3`... (`REG_SZ`) | Sequência `url1` (mais recente) a `urlN` | Prova digitação explícita (ex.: lançar `cmd` ou `powershell` a partir da barra de endereços). |

---

## 1. Comandos Executados na Caixa Executar (`Win+R`): `RunMRU`

Regista a lista de comandos, caminhos ou programas que o utilizador digitou explicitamente na caixa de diálogo **Executar** (`Win+R`):

```text
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU
```

### Estrutura dos Valores e Ordem de Execução (`MRUList`)

* **Entradas alfabéticas**: Cada comando digitado recebe uma letra minúscula como nome do valor (`a` a `z`), e o seu conteúdo termina com o sufixo interno `\1`:
  * `"a" = "notepad\1"`
  * `"b" = "cmd\1"`
  * `"c" = "calc\1"`
* **Valor `MRUList` (`REG_SZ`)**: Sequência textual de letras que define a ordem cronológica **do mais recente (à esquerda) para o mais antigo (à direita)**.
  * *Exemplo de Exame*: Se `MRUList = "cba"`, significa que o último comando executado foi **`'c'` (`calc`)**, antecedido por **`'b'` (`cmd`)** e, mais atrás no tempo, **`'a'` (`notepad`)**. O *LastWriteTime* da chave `RunMRU` corresponde ao instante exato em que `'c'` foi executado.

### Anatomia da Extração via CLI

```cmd
reg export HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU run_mru.txt
```

* **`reg export <Chave> <Ficheiro>`**: exporta todos os valores da chave `RunMRU` para o ficheiro de texto `run_mru.txt` sem alterar os dados originais.

---

## 2. Ficheiros Recentes no Explorer: `RecentDocs`

Regista ficheiros e pastas acedidos ou abertos através do Windows Explorer:

```text
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs
```

### Organização da Chave e Estrutura de `MRUListEx`

* **Raiz e Subchaves por Extensão**: A chave `RecentDocs` contém entradas gerais na raiz e subchaves divididas por extensão de ficheiro (ex.: `.docx`, `.pdf`, `.mp3`, `.zip`, mais a subchave `Folder` para diretórios).
* **Valores Numéricos (`0`, `1`, `2`...)**: Cada entrada é um valor `REG_BINARY` que armazena o nome do ficheiro em [[Codificação de Caracteres - ASCII, Latin-1 e Unicode|Unicode]] (UTF-16LE) seguido do nome do atalho `.lnk` correspondente.
* **Valor `MRUListEx` (`REG_BINARY`)**: Composto por uma sequência de blocos de **4 bytes (inteiros de 32 bits em [[Endianness e Ordem de Armazenamento|Little-Endian]])** que ditam a ordem temporal das entradas, terminando com o marcador `FF FF FF FF` (`-1`).
  * *Exemplo de Leitura Hexadecimal*: Se `MRUListEx` começar pelos bytes **`02 00 00 00` `00 00 00 00` `01 00 00 00`**, o primeiro inteiro de 4 bytes é `0x00000002` (decimal **2**), indicando que o ficheiro armazenado no valor **`"2"`** foi o último a ser aberto, seguido do valor `"0"` e depois `"1"`.

---

## 3. Caixas de Diálogo *Open/Save*: `ComDlg32`

Regista os ficheiros abertos ou gravados pelo utilizador através das caixas de diálogo comuns do Windows (*Common Dialogs* de *Abrir* e *Guardar Como*):

```text
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32
```

### Subchaves de Elevado Valor Pericial

1. **`OpenSavePidlMRU`**: Lista os ficheiros abertos ou guardados através de caixas de diálogo, organizados em subchaves por extensão (e `*` para todos) e ordenados pelo valor binário **`MRUListEx`**.
2. **`LastVisitedPidlMRU`**: Regista o **nome do executável de origem** (ex.: `winword.exe`, `chrome.exe`, `mspaint.exe`) que invocou a caixa de diálogo, juntamente com o **último diretório (PIDL)** navegado dentro dessa aplicação, também ordenado por `MRUListEx`.
3. **`CIDSizeMRU`**: Regista o executável juntamente com as dimensões e posições em píxeis das janelas de diálogo no ecrã.

---

## 4. Caminhos Digitados na Barra de Endereços: `TypedPaths`

Regista os caminhos de pastas locais, partilhas de rede (`\\servidor\partilha`) ou comandos que o utilizador **digitou diretamente na barra de endereços do Explorador de Ficheiros**:

```text
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths
```

### Anatomia da Extração via CLI

```cmd
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths\ /s
```

Exemplo de saídas típicas em investigação:

```text
url1    REG_SZ    cmd
url2    REG_SZ    C:\Users\User\OneDrive - IPLeiria\
url3    REG_SZ    C:\Windows\System32\cmd.exe
url4    REG_SZ    powershell
```

* **Valor Pericial**: Evidencia ação deliberada do utilizador para aceder a diretórios ocultos/não indexados ou para **invocar consolas de comandos (`cmd`, `powershell`) diretamente a partir da pasta aberta no Explorador** (técnica muito comum para abrir uma consola já posicionada num diretório específico).

---

## Ferramentas de Análise

* **RecentFilesView** (NirSoft): utilitário gráfico que cruza automaticamente as chaves `RecentDocs`, `RunMRU` e a pasta de atalhos `.lnk` (`Recent`), apresentando uma tabela cronológica dos últimos ficheiros abertos e pastas visitadas.
* **RegRipper** (`rip.exe`): plugins dedicados `runmru`, `recentdocs`, `typedpaths` e `comdlg32` executados sobre o ficheiro `NTUSER.DAT`.
* **RegistryExplorer** (Eric Zimmerman): descodifica automaticamente as estruturas binárias PIDL e ordena visualmente os valores segundo `MRUList` e `MRUListEx`.

---

## Perguntas de revisão

1. **Qual a diferença técnica entre o formato e a leitura dos valores `MRUList` (em `RunMRU`) e `MRUListEx` (em `RecentDocs` e `ComDlg32`)?**

> [!success]- Ver Resposta
> `MRUList` é um valor de texto (`REG_SZ`) onde cada carácter (letra `a` a `z`) identifica uma entrada da chave `RunMRU` da mais recente para a mais antiga (ex.: `"cba"` indica que `'c'` foi o último comando executado). Já `MRUListEx` é um valor binário (`REG_BINARY`) onde cada entrada é um número inteiro de **4 bytes (32 bits) em formato Little-Endian** (ex.: `02 00 00 00` indica que o valor com nome `"2"` é o mais recente), terminando a lista com `FF FF FF FF`.

2. **Ao analisar a subchave `RecentDocs\.pdf`, o perito observa que o valor `MRUListEx` contém a sequência hexadecimal `03 00 00 00 01 00 00 00 00 00 00 00 02 00 00 00 FF FF FF FF`. Qual foi o ficheiro PDF aberto mais recentemente e a que entrada corresponde o *LastWriteTime* da subchave `.pdf`?**

> [!success]- Ver Resposta
> Lendo os blocos de 4 bytes em Little-Endian, o primeiro bloco é `03 00 00 00` (`3`). Portanto, o ficheiro armazenado no valor **`"3"`** foi o PDF aberto mais recentemente, seguido de `"1"`, `"0"` e `"2"`. O carimbo temporal *LastWriteTime* da subchave `.pdf` regista o momento exato em que o ficheiro `"3"` foi acedido.

3. **Qual a diferença forense entre as subchaves `OpenSavePidlMRU` e `LastVisitedPidlMRU` dentro da chave `ComDlg32`?**

> [!success]- Ver Resposta
> `OpenSavePidlMRU` regista o caminho completo dos **ficheiros individuais** que foram abertos ou guardados numa caixa de diálogo padrão do Windows (agrupados por extensão). Por sua vez, `LastVisitedPidlMRU` regista qual foi o **executável da aplicação** (ex.: `notepad.exe`, `winword.exe`) que abriu a caixa de diálogo e qual foi o **último diretório (pasta)** visitado por essa aplicação.

4. **O que significa encontrar os valores `url1 = "powershell"` e `url2 = "cmd"` na chave `TypedPaths` de um utilizador?**

> [!success]- Ver Resposta
> Significa que o utilizador clicou na barra de endereços do Windows Explorer e digitou explicitamente `cmd` e, mais recentemente, `powershell` para lançar uma consola de comandos diretamente no diretório em que se encontrava a navegar.

## Notas relacionadas

- [[Estrutura e Hives do Windows Registry]]
- [[Ferramentas de Análise e Extração do Registry]]
- [[Artefacto Forense UserAssist]]
- [[Artefacto Forense ShellBags]]
- [[Pesquisa de Evidências e Reconstrução de Eventos]]
- [[Endianness e Ordem de Armazenamento]]
- [[Codificação de Caracteres - ASCII, Latin-1 e Unicode]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
