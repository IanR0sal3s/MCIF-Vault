---
title: UWP - Artefactos Forenses e Estrutura de Dados
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
tipo: procedimento
tags:
  - forense
  - windows
  - uwp
  - appx
  - sqlite
aliases:
  - UWP Forensics
  - Artefactos UWP
  - StateRepository
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
fontes:
  - "Yogesh Khatri, Appx-Analysis (Magnet Summit 2019), https://github.com/ydkhatri/Appx-Analysis"
atualizado: 2026-09-24
---

# Artefactos Forenses em Aplicações UWP

O modelo de execução em sandbox das [[Aplicações UWP (Universal Windows Platform) - Visão Geral|Aplicações UWP]] condiciona a localização dos dados de utilizador, das configurações persistentes e dos registos de instalação. Para recolher evidências relativas a estas aplicações, a investigação pericial orienta-se para três locais principais: o diretório de dados do utilizador, a base de dados central de registo de pacotes e o ficheiro de memória virtual.

---

## 1. Dados e Configurações por Utilizador (`Packages`)

Os dados de sessão, ficheiros descarregados e definições de cada aplicação UWP residem na pasta local de dados do respetivo utilizador:

```text
C:\Users\%username%\AppData\Local\Packages\
```

Cada aplicação instalada possui um subdiretório próprio nomeado através do seu identificador de pacote (ex.: `27879SnkeKhn.NotepadX_xq0nh4s6cn4qe`).

### Estrutura Típica da Pasta da Aplicação
Dentro da pasta de cada pacote, os dados organizam-se na seguinte hierarquia:

```text
<APP_PACKAGE_NAME>\
├── Settings\
│   └── settings.dat       <- Hive de Registry privado da aplicação
├── LocalState\            <- Ficheiros locais persistentes da aplicação
├── LocalCache\            <- Ficheiros temporários e recriáveis pela aplicação
├── RoamingState\          <- Definições sincronizadas entre dispositivos da mesma conta
├── AC\                    <- AppContainer: caches in-app, cookies e histórico web
│   ├── INetCache\
│   ├── INetCookies\
│   └── INetHistory\
├── SystemAppData\         <- Dados de sistema do pacote (inclui subpasta Helium em MSIX)
└── TempState\             <- Ficheiros temporários locais
```

### O Ficheiro de Registry `settings.dat`
As configurações internas da aplicação UWP são mantidas num ficheiro binário dedicado:

```text
%LocalAppData%\Packages\<APP>\Settings\settings.dat
```

* **Formato**: Embora muitas componentes modernas usem SQLite, o `settings.dat` é estruturado internamente como um **ficheiro de Registry** do Windows.
* **Análise**: Não pode ser aberto com visualizadores SQLite. Deve ser analisado através de ferramentas de Registry (como o `RegistryExplorer` ou através do comando nativo `reg.exe load`).

---

## 2. Inventário Global do Sistema: State Repository

Para auditar o histórico de todas as aplicações UWP instaladas no sistema operativo (incluindo utilizadores associados, versões e data de instalação), o Windows utiliza o **State Repository**:

```text
C:\ProgramData\Microsoft\Windows\AppRepository\Packages\
```

Este repositório assenta em duas bases de dados relacionais em formato **SQLite3**:

| Ficheiro de Base de Dados | Função Pericial |
| :--- | :--- |
| **`StateRepository-Machine.srd`** | Registo global de aplicações, extensões, protocolos, nós e permissões associadas à máquina. |
| **`StateRepository-Deployment.srd`** | Histórico de operações de instalação, pacotes fontes, utilizadores de destino e estado de implementação (*deployment*). |

> [!NOTE] Localização dos Ficheiros `.srd`
> Dependendo da compilação e versão específica do Windows 10 ou Windows 11, os ficheiros `.srd` podem encontrar-se diretamente na raiz de `C:\ProgramData\Microsoft\Windows\AppRepository\` ou sob a subpasta `Packages\` e `Downlevel\`. O perito deve verificar a existência dos ficheiros em ambos os caminhos.

### Ferramentas de Extração
Para além de consultas SQL diretas através do *DB Browser for SQLite*, destaca-se a suite de scripts e ferramentas desenvolvida por **Yogesh Khatri** (*Appx-Analysis*, Magnet User Summit), que correlaciona tabelas como `Application`, `AppInstaller` e `Package` para reconstruir o inventário de software instalado.

---

## 3. Análise de Memória Virtual: `swapfile.sys`

As aplicações UWP e os processos em contentor utilizam o ficheiro de paginação específico **`swapfile.sys`** (localizado na raiz do volume do sistema, ex.: `C:\swapfile.sys`) para descarregar páginas de memória quando as aplicações são suspensas em segundo plano.

* **Relevância pericial**: Permite a recuperação de fragmentos de texto, mensagens em claro, URLs ou chaves de sessão de aplicações suspensas através de técnicas de pesquisa de cadeias de caracteres (*strings*) e *carving* de ficheiros.
* É um artefacto complementar aos ficheiros de perfil e ao State Repository quando se investigam processos e mensagens voláteis.

---

## Metodologia de Recolha Pericial

Numa análise a aplicações UWP, a recolha deve seguir uma sequência lógica e metódica:
1. **Inventário**: Extração das bases de dados `.srd` do `AppRepository` para mapear que aplicações existem e quando foram instaladas.
2. **Dados de Utilizador**: Preservação da pasta `%LocalAppData%\Packages\<APP>` do utilizador visado (com especial atenção às subpastas `LocalState`, `AC` e `SystemAppData`).
3. **Definições**: Carregamento pericial do `settings.dat` para inspecionar preferências da app.
4. **Memória de Troca**: Análise de *strings* ao `swapfile.sys` se a investigação exigir recuperar conteúdo em trânsito de apps suspensas.

## Notas relacionadas

- [[Aplicações UWP (Universal Windows Platform) - Visão Geral]]
- [[Registry em Aplicações Modernas (MSIX e Helium)]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
