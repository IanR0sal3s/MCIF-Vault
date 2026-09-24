---
title: Artefactos Forenses de Interação do Utilizador (MRU e TypedPaths)
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
tipo: conceito
tags:
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

As listas **MRU** (*Most Recently Used*) são mecanismos do sistema operativo desenhados para melhorar a usabilidade, apresentando ao utilizador menus com ficheiros, diretórios e comandos acedidos recentemente. Em informática forense, constituem artefactos primários para reconstituir a interação intencional de um utilizador com o sistema.

Estes artefactos residem no hive pessoal do utilizador (`NTUSER.DAT` $\rightarrow$ `HKCU`).

---

## 1. Comandos Executados: `RunMRU`

Regista a lista de comandos e programas que o utilizador digitou explicitamente na caixa de diálogo **Executar** (`Win+R`):

```text
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU
```

### Estrutura dos Valores:
* As entradas recebem nomes alfabéticos: `"a" = "notepad\\1"`, `"b" = "cmd\\1"`, `"c" = "calc\\1"`. O sufixo `\1` indica terminação interna.
* **Ordem de Execução (`MRUList`)**: valor em texto (`REG_SZ`) cuja sequência de letras dita a ordem do mais recente para o mais antigo.
  * *Exemplo*: se `MRUList = "cba"`, significa que o comando `'c'` foi o mais recente, seguido de `'b'` e depois `'a'`.

```cmd
REM Exportar a chave RunMRU
reg export HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU run_mru.txt
```

---

## 2. Ficheiros Recentes: `RecentDocs`

Regista ficheiros acedidos ou abertos através do Windows Explorer:

```text
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs
```

### Organização da Chave:
* A raiz contém entradas gerais e o valor `MRUListEx`.
* Subchaves divididas por extensão de ficheiro (ex.: `.docx`, `.pdf`, `.mp3`, `.zip`).
* **Valor `MRUListEx`**: valor binário (`REG_BINARY`) composto por blocos de 4 bytes (inteiros Little-Endian) que especificam a ordem temporal das entradas.
  * Se o primeiro bloco de 4 bytes for `02 00 00 00`, a entrada designada `"2"` é a mais recente.
* Cada valor individual armazena o nome do ficheiro em Unicode e dados do atalho LNK correspondente.

---

## 3. Caixas de Diálogo: `ComDlg32`

Regista os ficheiros abertos ou gravados pelo utilizador através de caixas de diálogo padrão do Windows (*Open/Save Dialogs*):

```text
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32
```

### Subchaves de Elevado Valor Pericial:
* **`OpenSavePidlMRU`**: lista ficheiros abertos ou guardados em caixas de diálogo, estruturados por extensão e ordenados por `MRUListEx`.
* **`LastVisitedPidlMRU`**: regista o executável de origem que abriu a caixa de diálogo e o último diretório navegado dentro dessa aplicação.
* **`CIDSizeMRU`**: dimensões e posições das janelas de diálogo.

---

## 4. Caminhos Digitados: `TypedPaths`

Regista os caminhos de pastas ou comandos que o utilizador digitou diretamente na **barra de endereços do Explorador de Ficheiros**:

```text
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths
```

### Extração via CLI:

```cmd
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths\ /s
```

Exemplo de saídas típicas:
```text
url1    REG_SZ    cmd
url2    REG_SZ    C:\Users\User\OneDrive - IPLeiria\
url3    REG_SZ    C:\Windows\System32\cmd.exe
url4    REG_SZ    powershell
```

* *Valor pericial*: evidencia tentativa ativa do utilizador em navegar para caminhos ocultos, partilhas de rede ou invocar shells (`cmd`, `powershell`) a partir do Explorador.

---

## Ferramentas de Análise

* **RecentFilesView** (NirSoft): utilitário que lê automaticamente as chaves `RecentDocs`, `RunMRU` e atalhos LNK, apresentando uma tabela cronológica dos últimos ficheiros abertos e pastas visitadas.
* **RegRipper**: plugins `runmru`, `recentdocs`, `typedpaths` e `comdlg32`.
* **RegistryExplorer**: navegação com ordenação automática de `MRUList` e `MRUListEx`.

## Notas relacionadas

- [[Estrutura e Hives do Windows Registry]]
- [[Ferramentas de Análise e Extração do Registry]]
- [[Artefacto Forense UserAssist]]
- [[Artefacto Forense ShellBags]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
