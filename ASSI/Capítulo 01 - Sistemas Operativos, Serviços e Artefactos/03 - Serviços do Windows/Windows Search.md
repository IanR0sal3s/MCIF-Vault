---
title: Windows Search
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
tipo: procedimento
tags:
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

O **Windows Search** é o serviço responsável pela **indexação de conteúdos e metadados de ficheiros** no sistema operativo, tornando instantânea a pesquisa do utilizador no menu Iniciar (`Win+Q`), no Explorador de Ficheiros (`F3`), na barra de endereços do Microsoft Edge e no cliente Microsoft Outlook para desktop.

Como o índice cataloga nomes de ficheiros, diretórios, caminhos completos e propriedades de ficheiros acedidos pelo utilizador, constitui um **artefacto forense de elevado valor pericial**, permitindo comprovar a existência prévia de ficheiros que foram entretanto apagados do sistema de ficheiros.

---

## Localização Central da Base de Dados

Tanto no Windows 10 como no Windows 11, o repositório de indexação reside no mesmo caminho protegido de sistema:

```text
%AllUsersProfile%\Microsoft\Search\Data\Applications\Windows\
```

(Equivalente a `C:\ProgramData\Microsoft\Search\Data\Applications\Windows\`).

* **Âmbito de Indexação Padrão (Windows 11)**: Por omissão, o serviço indexa as pastas pessoais `C:\Users\*` (**com exceção explícita da subpasta `AppData`**) e o Menu Iniciar (`Start Menu`).
* **Anomalia de Tamanho**: Em certas condições operacionais (por exemplo, na indexação extensiva de ficheiros PST do Outlook), o ficheiro de índice pode atingir dimensões gigantescas.
* **Opções de Gestão**: A janela de configuração pode ser invocada via `Win+Q` $\rightarrow$ `indexing` ou executando diretamente o comando:
  ```cmd
  control srchadmin.dll
  ```

---

## Controlo do Serviço na Linha de Comandos

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

## Windows 10: Motor ESE (`Windows.edb`)

No Windows 10, o índice é armazenado num ficheiro de base de dados gerido pelo motor **ESE (*Extended Storage Engine*)**:

```text
Windows.edb
```

*(O mesmo motor de base de dados relacional incorporado pelo Active Directory, Microsoft Edge, SRUM e pela base `qmgr.db` do [[Serviço BITS]]). Além do `.edb`, a pasta inclui ficheiros de log e controlo de transações como `MSS.log` e `edb.chk`.*

### Principais Tabelas Forenses no `Windows.edb`:
* **`SystemIndex_Gthr`**: Regista os nomes dos ficheiros e diretórios recolhidos (*gather*).
* **`SystemIndex_GthrPth`**: Regista os caminhos das pastas indexadas associadas às entradas da tabela `Gthr`.
* **`SystemIndex_PropertyStore`**: Armazena os metadados e propriedades estendidas dos ficheiros indexados (data de modificação, autor, dimensões), constituindo a tabela mais rica para análise pericial.

### Ferramenta Especializada: `WinSearchDBAnalyzer`
Utilitário desenhado para análise direta de ficheiros `Windows.edb`:
* Permite pesquisar registos ativos e recuperar **registos apagados (*deleted records*)** da base de dados.
* Suporta a extração e inspeção de ficheiros `Windows.edb` mesmo a partir de sistemas ativos em execução.

---

## Windows 11: Transição para SQLite3

No Windows 11, o serviço mantém o mesmo caminho em `ProgramData`, mas substituiu o motor ESE por **bases de dados relacionais em formato SQLite3**:

| Ficheiro no Disco | Descrição e Função |
| :--- | :--- |
| **`Windows.db`** | Base de dados principal do índice de pesquisa. |
| **`Windows-gather.db`** | Base de dados de recolha (*gather*) de ficheiros e pastas. |
| **`Windows-usn.db`** | Registo associado a atualizações e alterações provenientes do USN Journal de volumes NTFS. |
| **`*.db-shm` e `*.db-wal`** | Ficheiros de controlo de concorrência (*shared memory*) e registo de transações (*Write-Ahead Logging*). Devem ser sempre recolhidos conjuntamente na aquisição forense. |

### Diferença Estrutural W10 vs. W11
* No Windows 10 (EDB), cada entrada consolida todas as propriedades do ficheiro num único registo.
* No Windows 11 (SQLite3), a arquitetura foi normalizada: **um registo do Windows 10 distribui-se por múltiplos registos no Windows 11** (armazenando um campo/propriedade por linha, utilizando identificadores como `ColumnId` correspondentes a propriedades como `System_IsFolder` ou `System_FilePlaceHolderStatus`).

### Validação de Formato SQLite3
Para verificar que se trata de uma base de dados SQLite3 legítima num editor hexadecimal (como o HxD):
* **Sequência Hexadecimal Inicial (Magic Number)**:
  `53 51 4C 69 74 65 20 66 6F 72 6D 61 74 20 33`
* **Texto ASCII Decodificado**:
  `SQLite format 3`

Os ficheiros podem ser visualizados e interrogados via SQL através do **DB Browser for SQLite**.

---

## Ferramenta Forense: `sidr` (Search Index DB Reporter)

O **sidr** (Stroz Friedberg) é uma ferramenta *open-source* multiplataforma concebida especificamente para extração pericial automatizada de artefactos do Windows Search:
* **Compatibilidade**: Suporta bases de dados do Windows 10 (EDB) e do Windows 11 (SQLite3).
* **Formatos de Exportação**: Permite extrair relatórios estruturados em **CSV** ou **JSON**.

```cmd
REM Extração para ficheiros JSON
sidr.exe -f json C:\Caminho\Onde\Estao\Ficheiros_WSearch

REM Extração para ficheiros CSV direcionados para uma pasta de saída
sidr.exe -f csv C:\ProgramData\Microsoft\Search\Data\Applications\Windows -o C:\Relatorio_WSearch
```

### Relatórios Gerados pelo `sidr`:
1. **`File_Report`**: Lista exaustiva de ficheiros indexados e respetivos metadados.
2. **`Activity_History_Report`**: Histórico de atividades do sistema e do utilizador.
3. **`Internet_History_Report`**: Histórico de pesquisas efetuadas diretamente na barra de endereços do navegador Microsoft Edge.

---

## Laboratório 1 — Ferramentas & Windows Search

O programa da unidade curricular integra a aplicação prática destes conceitos (Slide 57), focando-se na auditoria do serviço `WSearch`, preservação dos ficheiros de índice (`Windows.edb` ou `Windows.db`), execução de analisadores especializados (`sidr` e `WinSearchDBAnalyzer`) e interpretação pericial dos dados de histórico extraídos em CSV/JSON.

## Notas relacionadas

- [[Serviços Windows]]
- [[Serviço BITS]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
