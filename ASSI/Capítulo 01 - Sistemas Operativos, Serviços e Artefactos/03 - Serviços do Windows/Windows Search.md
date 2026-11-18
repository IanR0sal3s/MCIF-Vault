---
title: Windows Search
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 3
tipo: procedimento
tags:
  - assi
  - windows
  - wsearch
  - ese
  - sqlite
  - forense
aliases:
  - WSearch
  - Windows Search Service
  - sidr
  - WinSearchDBAnalyzer
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
fontes:
  - "Chivers, H. and Hargreaves, C. Forensic data recovery from the Windows Search database. Digital Investigation 7.3 (2011): 114–126"
  - "https://github.com/strozfriedberg/sidr"
  - "https://moaistory.blogspot.com/2018/10/winsearchdbanalyzer.html"
atualizado: 2026-09-24
---

# Windows Search (WSearch)

O **Windows Search (`WSearch`)** é o serviço do Windows responsável pela indexação contínua de conteúdos e metadados de ficheiros, alimentando a pesquisa no Menu Iniciar (`Win+Q`), Explorador (`F3`), Microsoft Edge e Outlook.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: Pesquisar ficheiros varrendo todo o disco em tempo real seria demasiado lento; o `WSearch` mantém uma base de dados indexada em `%AllUsersProfile%\Microsoft\Search\Data\Applications\Windows\` com caminhos, propriedades e fragmentos de texto.
> * **Porque importa (Forense / Segurança)**: Mesmo quando um utilizador apaga um ficheiro do disco, os seus metadados, caminho original e carimbos temporais permanecem frequentemente retidos na base de dados do Windows Search, comprovando a existência prévia do artefacto.
> * **Pontos Críticos para Exame**:
>   * **Transição de motor (W10 vs. W11)**: O Windows 10 usa uma base de dados **ESE (`Windows.edb`)** onde 1 ficheiro = 1 registo consolidado; o Windows 11 usa **SQLite3 (`Windows.db`, `Windows-gather.db`, `Windows-usn.db`)** onde 1 ficheiro do W10 se desdobra em **múltiplos registos** normalizados.
>   * Por omissão no Windows 11, o serviço indexa `C:\Users\*` **com exceção explícita da pasta `AppData`**.

---

## Localização Central e Controlo do Serviço

Tanto no Windows 10 como no Windows 11, o repositório de indexação reside no mesmo caminho protegido de sistema:

```text
%AllUsersProfile%\Microsoft\Search\Data\Applications\Windows\
```

*(Equivalente a `C:\ProgramData\Microsoft\Search\Data\Applications\Windows\`).*

* **Âmbito de Indexação Padrão (Windows 11)**: Por omissão, o serviço indexa as pastas pessoais `C:\Users\*` (**com exceção explícita da subpasta `AppData`**) e o Menu Iniciar (`Start Menu`).
* **Anomalia de Tamanho**: Em certas condições operacionais (por exemplo, na indexação extensiva de ficheiros PST do Outlook), o ficheiro de índice pode atingir dimensões gigantescas.

**Opções de Gestão Gráfica:** A janela de configuração pode ser invocada via `Win+Q` $\rightarrow$ `indexing` ou executando diretamente o comando:

```cmd
control srchadmin.dll
```

### Controlo do Serviço na Linha de Comandos (`sc.exe`)
O serviço `WSearch` pode ser auditado e desativado através do utilitário `sc`:

```cmd
REM Consultar estado do serviço de indexação
sc query wsearch

REM Desativar arranque automático (espaço obrigatório após start=)
sc config WSearch start= disabled

REM Parar a execução imediata do serviço
sc stop WSearch
```

---

## Comparação Arquitetural: Windows 10 (ESE) vs. Windows 11 (SQLite3)

| Critério Técnico / Forense | Windows 10 (`Windows.edb`) | Windows 11 (`Windows.db`) |
| :--- | :--- | :--- |
| **Motor de Base de Dados** | **ESE** (*Extended Storage Engine* — o mesmo do Active Directory, Edge, SRUM e `qmgr.db` do [[Serviço BITS]]). | **SQLite3** (Magic Number ASCII: `SQLite format 3` / Hex: `53 51 4C 69 74 65 20 66 6F 72 6D 61 74 20 33`). |
| **Caminho no Disco** | `C:\ProgramData\Microsoft\Search\Data\Applications\Windows\` | `C:\ProgramData\Microsoft\Search\Data\Applications\Windows\` (mesmo diretório). |
| **Ficheiros Principais** | **`Windows.edb`** (acompanhado por logs de transações `MSS.log` e `edb.chk`). | **`Windows.db`** (índice), **`Windows-gather.db`** (recolha) e **`Windows-usn.db`** (USN Journal NTFS). |
| **Ficheiros de Transação Auxiliares** | `MSS.log`, `edb.chk` | **`*.db-shm`** (*shared memory*) e **`*.db-wal`** (*Write-Ahead Logging* — recolha forense obrigatória). |
| **Estrutura de Registos** | **Consolidada**: cada entrada concentra todas as propriedades do ficheiro num único registo. | **Normalizada**: um registo do W10 distribui-se por **múltiplos registos** no W11 (1 propriedade por linha via `ColumnId`). |
| **Ferramentas de Análise** | **`WinSearchDBAnalyzer`** (suporta *deleted records* e extração *live*) e **`sidr`**. | **`DB Browser for SQLite`** (interrogação SQL direta) e **`sidr`**. |

---

## Detalhe por Versão do Sistema Operativo

### 1. Windows 10: Motor ESE (`Windows.edb`)

No Windows 10, o índice é armazenado no ficheiro **`Windows.edb`** gerido pelo motor **ESE (*Extended Storage Engine*)** — o mesmo motor de base de dados relacional incorporado pelo Active Directory, Microsoft Edge, SRUM e pela base `qmgr.db` do [[Serviço BITS]]. Além do `.edb`, a pasta inclui ficheiros de log e controlo de transações como `MSS.log` e `edb.chk`.

#### Principais Tabelas Forenses no `Windows.edb`

* **`SystemIndex_Gthr`**: Regista os nomes dos ficheiros e diretórios recolhidos (*gather*).
* **`SystemIndex_GthrPth`**: Regista os caminhos das pastas indexadas associadas às entradas da tabela `Gthr`.
* **`SystemIndex_PropertyStore`**: Armazena os metadados e propriedades estendidas dos ficheiros indexados (data de modificação, autor, dimensões), constituindo a tabela mais rica para análise pericial.

#### Ferramenta Especializada: `WinSearchDBAnalyzer`
Utilitário desenhado para análise direta de ficheiros `Windows.edb`:

* Permite pesquisar registos ativos e recuperar **registos apagados (*deleted records*)** da base de dados.
* Suporta a extração e inspeção de ficheiros `Windows.edb` mesmo a partir de sistemas ativos em execução.

---

### 2. Windows 11: Transição para SQLite3

No Windows 11, o serviço mantém o mesmo caminho em `ProgramData`, mas substituiu o motor ESE por **bases de dados relacionais em formato SQLite3**:

| Ficheiro no Disco | Descrição e Função |
| :--- | :--- |
| **`Windows.db`** | Base de dados principal do índice de pesquisa. |
| **`Windows-gather.db`** | Base de dados de recolha (*gather*) de ficheiros e pastas. |
| **`Windows-usn.db`** | Registo associado a atualizações e alterações provenientes do USN Journal de volumes NTFS. |
| **`*.db-shm` e `*.db-wal`** | Ficheiros de controlo de concorrência (*shared memory*) e registo de transações (*Write-Ahead Logging*). Devem ser sempre recolhidos conjuntamente na aquisição forense. |

#### Diferença Estrutural W10 vs. W11

* No Windows 10 (EDB), cada entrada consolida todas as propriedades do ficheiro num único registo.
* No Windows 11 (SQLite3), a arquitetura foi normalizada: **um registo do Windows 10 distribui-se por múltiplos registos no Windows 11** (armazenando um campo/propriedade por linha, utilizando identificadores como `ColumnId` correspondentes a propriedades como `System_IsFolder` ou `System_FilePlaceHolderStatus`).

#### Validação de Formato SQLite3 (Magic Number)
Para verificar que se trata de uma base de dados SQLite3 legítima num editor hexadecimal (como o HxD):

* **Sequência Hexadecimal Inicial (Magic Number)**: `53 51 4C 69 74 65 20 66 6F 72 6D 61 74 20 33`
* **Texto ASCII Decodificado**: `SQLite format 3`

Os ficheiros podem ser visualizados e interrogados via SQL através do **DB Browser for SQLite**.

---

## Ferramenta Forense: `sidr` (Search Index DB Reporter)

O **sidr** (Stroz Friedberg) é uma ferramenta *open-source* multiplataforma concebida especificamente para extração pericial automatizada de artefactos do Windows Search, compatível tanto com bases do Windows 10 (EDB) como do Windows 11 (SQLite3).

### Anatomia do Comando `sidr`

```cmd
sidr.exe -f <formato_csv_ou_json> <Caminho_Pasta_Input> [-o <Caminho_Pasta_Output>]
```

* **`-f <formato>`**: define o formato de exportação estruturada (**`json`** ou **`csv`**).
* **`<Caminho_Pasta_Input>`**: diretório onde residem os ficheiros de base de dados (`Windows.edb` ou `Windows.db`).
* **`-o <Caminho_Pasta_Output>`**: diretório de destino onde serão gravados os três relatórios gerados.

```cmd
REM Extração para ficheiros JSON
sidr.exe -f json C:\Caminho\Onde\Estao\Ficheiros_WSearch

REM Extração para ficheiros CSV direcionados para uma pasta de saída
sidr.exe -f csv C:\ProgramData\Microsoft\Search\Data\Applications\Windows -o C:\Relatorio_WSearch
```

### Relatórios Gerados pelo `sidr`

1. **`File_Report`**: Lista exaustiva de ficheiros indexados e respetivos metadados.
2. **`Activity_History_Report`**: Histórico de atividades do sistema e do utilizador.
3. **`Internet_History_Report`**: Histórico de pesquisas efetuadas diretamente na barra de endereços do navegador Microsoft Edge.

---

## Laboratório 1 — Ferramentas & Windows Search

O programa da unidade curricular integra a aplicação prática destes conceitos (Slide 57), focando-se na auditoria do serviço `WSearch`, preservação dos ficheiros de índice (`Windows.edb` ou `Windows.db`), execução de analisadores especializados (`sidr` e `WinSearchDBAnalyzer`) e interpretação pericial dos dados de histórico extraídos em CSV/JSON.

---

## Perguntas de revisão

1. **Quais são as principais diferenças entre o armazenamento do Windows Search no Windows 10 e no Windows 11 (motor de base de dados, nome dos ficheiros e organização dos registos)?**

> [!success]- Ver Resposta
> * **Windows 10**: utiliza o motor **ESE** num único ficheiro principal **`Windows.edb`** (com `MSS.log` e `edb.chk`), onde cada ficheiro indexado corresponde a um único registo consolidado (nas tabelas `SystemIndex_Gthr`, `SystemIndex_GthrPth` e `SystemIndex_PropertyStore`).
> * **Windows 11**: utiliza **SQLite3** dividido em **`Windows.db`**, **`Windows-gather.db`** e **`Windows-usn.db`** (mais ficheiros `.db-shm` e `.db-wal`), com estrutura normalizada onde um registo do W10 se distribui por múltiplos registos (uma propriedade/`ColumnId` por linha).

2. **Que pastas são indexadas por omissão pelo Windows Search no Windows 11 e qual é a subpasta crítica que fica excluída por padrão?**

> [!success]- Ver Resposta
> O Windows Search indexa por omissão o Menu Iniciar (`Start Menu`) e as pastas de perfil dos utilizadores em `C:\Users\*`, mas **exclui explicitamente a subpasta `AppData`**.

3. **Como se valida num editor hexadecimal que o ficheiro `Windows.db` é uma base SQLite3 e porque é obrigatório preservar também os ficheiros `.db-wal` e `.db-shm`?**

> [!success]- Ver Resposta
> Verifica-se o cabeçalho (*Magic Number*) hexadecimal `53 51 4C 69 74 65 20 66 6F 72 6D 61 74 20 33`, correspondente à string ASCII `SQLite format 3`. Os ficheiros `.db-wal` (*Write-Ahead Logging*) e `.db-shm` (*shared memory*) têm de ser recolhidos conjuntamente porque contêm transações recentes que ainda não foram consolidadas no ficheiro `.db` principal.

4. **Que ferramenta de linha de comandos analisa simultaneamente bases de dados do Windows 10 e Windows 11 e quais são os três relatórios que produz?**

> [!success]- Ver Resposta
> A ferramenta **`sidr`** (*Search Index DB Reporter*, p. ex. `sidr.exe -f csv <input> -o <output>`), que gera os relatórios:
> 1. `File_Report` (ficheiros indexados e metadados)
> 2. `Activity_History_Report` (histórico de atividades)
> 3. `Internet_History_Report` (pesquisas e histórico do Microsoft Edge).

## Notas relacionadas

- [[Serviços Windows]]
- [[Serviço BITS]]
- [[Caches de Ícones e Miniaturas (IconCache e Thumbcache)]]
- [[Pesquisa de Evidências e Reconstrução de Eventos]]
- [[Camadas de Organização de Dados e Análise de Sistemas de Ficheiros]]
- [[Timestamps e Épocas Temporais (UNIX Epoch vs. Windows FILETIME)]]
- [[Sistemas de Numeração e Conversão entre Bases]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
