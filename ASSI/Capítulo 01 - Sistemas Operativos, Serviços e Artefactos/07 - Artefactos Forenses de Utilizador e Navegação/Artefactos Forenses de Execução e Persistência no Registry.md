---
title: Artefactos Forenses de Execução e Persistência no Registry
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
  - persistencia
  - execucao
  - autoruns
  - muicache
  - logonstats
  - forense
aliases:
  - Run Keys
  - RunOnce
  - Autoruns
  - MUICache
  - LogonStats
  - RecentApps
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
fontes:
  - "https://pastebin.com/kC702Y8A"
  - "http://www.nirsoft.net/utils/muicache_view.html"
atualizado: 2026-09-23
---

# Artefactos Forenses de Execução e Persistência no Registry

Chaves de persistência no arranque (`Run`, `RunOnce` e auditoria via `Autoruns`) e artefactos periciais de sessão e execução de aplicações no Registry (`LogonStats`, `MuiCache` e `RecentApps`).

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: O sistema operativo precisa de listas de arranque automático para iniciar serviços auxiliares no logon (`Run`/`RunOnce`), métricas de telemetria de sessão (`LogonStats`), uma cache de tradução de nomes de janelas para suporte multilingue (`MuiCache`) e um índice de aplicações e ficheiros recentes para a pesquisa do Windows 10 (`RecentApps`).
> * **Porque importa (Forense)**: Permite responder a três questões nucleares numa investigação: (1) *Que malware está configurado para arrancar sozinho?* (`Run`/`RunOnce` em `SOFTWARE` e `NTUSER.DAT`); (2) *Quando é que esta conta iniciou sessão pela primeira vez na máquina?* (`LogonStats` em `NTUSER.DAT`); e (3) *Que executáveis gráficos correram neste perfil, mesmo que já tenham sido apagados do disco?* (`MuiCache` em `USRCLASS.DAT` e `RecentApps` em `NTUSER.DAT`).
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **`MuiCache` reside no `USRCLASS.DAT`**: Regista o `.FriendlyAppName` e `.ApplicationCompany` do cabeçalho PE na 1.ª execução de uma aplicação com interface gráfica (GUI), mas **não guarda data/hora nem contador de execuções**.
>   * **Dupla Armadilha do `RecentApps`**: Primeiro, existe no **Windows 10**, mas **foi removido no Windows 11**. Segundo, a subchave `RecentItems` guarda até 10 ficheiros recentes por aplicação, mas ao atingir o 10.º item reordena as entradas **alfabeticamente** (e não por ordem cronológica FIFO).

---

## Mapa Rápido: "Pergunta do Investigador" $\rightarrow$ "Chave e Hive do Registry"

| O que procuro provar? | Chave do Registry | Ficheiro Físico (Hive) | Formato Temporal / Dados | Limitação / Armadilha Forense |
| :--- | :--- | :--- | :--- | :--- |
| **Persistência global** (arranca para todos os utilizadores) | `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run` (e `RunOnce`) | `SOFTWARE` | `REG_SZ` / `REG_EXPAND_SZ` (Comando) | Exige privilégios de Administrador; em 64 bits verificar também `WOW6432Node`. `RunOnce` apaga-se após correr. |
| **Persistência local** (arranca só para o utilizador atual) | `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` (e `RunOnce`) | `NTUSER.DAT` | `REG_SZ` (Comando) | Não requer privilégios de Administrador. |
| **Data do 1.º logon absoluto** do utilizador na máquina | `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\LogonStats` | `NTUSER.DAT` | `SYSTEMTIME` (16 bytes LE) | Diferenciar `FirstLogonTime` (absoluto) de `FirstLogonTimeOnCurrentInstallation` (pós-upgrade). |
| **Prova de que uma app GUI existiu e foi iniciada** pelo menos uma vez | `HKCU\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\MuiCache` | **`USRCLASS.DAT`** | `REG_SZ` (`FriendlyAppName` e `ApplicationCompany`) | Apenas aplicações **GUI**; não guarda contador nem timestamp individual de execução. |
| **Contador de execuções, última execução e últimos 10 ficheiros** abertos pela app | `HKCU\Software\Microsoft\Windows\CurrentVersion\Search\RecentApps` | `NTUSER.DAT` | `FILETIME64` (`LastAccessedTime`) + `LaunchCount` | **Exclusivo do Windows 10 (removido no Windows 11)**. Ao 10.º ficheiro em `RecentItems`, a lista ordena-se alfabeticamente (perde ordem cronológica). |

---

## 1. Chaves de Arranque Automático (*Run* e *RunOnce*)

Os pontos de extensão de inicialização automática (*Auto-Start Execution Points* — ASEPs) mais explorados por software malicioso residem sob o ramo `CurrentVersion`:

| Chave do Registry | Âmbito | Privilégio Exigido | Comportamento de Execução |
| :--- | :--- | :---: | :--- |
| `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run` | Máquina (Todos os utilizadores) | Administrador | Executado automaticamente sempre que qualquer utilizador inicia sessão no computador. |
| `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce` | Máquina (Todos os utilizadores) | Administrador | Executado uma única vez no arranque subsequente; a entrada é **eliminada** após o lançamento (comum em instaladores e atualizações). |
| `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` | Utilizador Atual | Utilizador Normal | Executado automaticamente apenas quando o utilizador específico inicia a sua sessão (muito usado por *malware* sem privilégios elevados). |
| `HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce` | Utilizador Atual | Utilizador Normal | Executado uma única vez na próxima sessão do utilizador atual e subsequentemente apagado. |

### Utilitário `Autoruns` (Sysinternals)

O utilitário de referência para auditoria de persistência e resposta a incidentes é o **Autoruns** (`autoruns.exe` / `autorunsc.exe`). Ao contrário de uma consulta manual apenas às chaves `Run`, o Autoruns inspeciona dezenas de vetores de arranque (ASEPs) em simultâneo:

* Chaves `Run` e `RunOnce` (tanto nativas de 64 bits como redirecionadas em `WOW6432Node`).
* Pastas de *Startup* do Menu Iniciar, Tarefas Agendadas (*Scheduled Tasks*), Serviços do Windows e Drivers de *kernel*.
* Notificações de *Winlogon*, extensões da *shell* do Explorer, *AppInit DLLs*, objetos WMI e sequestros de execução de imagem (*Image File Execution Options* — IFEO).

---

## 2. Chave `LogonStats` (Primeiro Início de Sessão)

Localizada no hive pessoal do utilizador (`NTUSER.DAT`):

```text
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\LogonStats
```

Armazena em formato binário [[Timestamps e Épocas Temporais (UNIX Epoch vs. Windows FILETIME)|SYSTEMTIME]] (128 bits / 16 bytes em Little-Endian):

* **`FirstLogonTime`**: data e hora em que o utilizador iniciou sessão pela primeira vez naquele computador.
* **`FirstLogonTimeOnCurrentInstallation`**: data e hora do primeiro início de sessão na versão/instalação atual do sistema operativo (atualizado após *feature updates* / atualizações de versão do Windows).
* **`LastLogonBuildNumber`** e **`LastLogonBuildRevision`**: versão exata da compilação (*build*) do Windows no último início de sessão.

### Descodificação em Lote via Python
A descodificação destes blocos de 16 bytes exportados do Registry pode ser automatizada com scripts em Python (como o script de aula disponível em `https://pastebin.com/kC702Y8A`):

```bash
python reg_systemtime_parser.py logon_from_reg.txt
```

---

## 3. Cache MUI (`MuiCache`)

O subsistema **MUI** (*Multilingual User Interface*) gere o suporte a múltiplos idiomas na interface do Windows:

* Sempre que uma aplicação com **interface gráfica (GUI)** é iniciada pela primeira vez por um utilizador, o sistema operativo extrai os metadados de versão do cabeçalho PE do executável e coloca-os em cache na chave:

```text
HKCU\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\MuiCache
```

* **Localização Física**: Gravado no ficheiro **`UsrClass.dat`** do utilizador (`C:\Users\<username>\AppData\Local\Microsoft\Windows\UsrClass.dat`).

### Dados Registados e Ferramenta de Análise
Para cada caminho completo de executável, o `MuiCache` cria tipicamente dois valores de texto (`REG_SZ`):

* `<Caminho_Executavel>.FriendlyAppName` (nome amigável da aplicação)
* `<Caminho_Executavel>.ApplicationCompany` (fabricante extraído dos recursos PE)
* *Exemplo real*:
  * `"C:\Program Files\Mozilla Firefox\firefox.exe.FriendlyAppName" = "Firefox"`
  * `"C:\Program Files\Mozilla Firefox\firefox.exe.ApplicationCompany" = "Mozilla Corporation"`

A ferramenta gráfica **MUICacheView** (NirSoft) lista todo este inventário. Constitui **evidência pericial direta de que uma determinada aplicação gráfica existiu naquele caminho e foi invocada pelo menos uma vez** na conta do utilizador (mesmo que o executável tenha sido posteriormente eliminado).

---

## 4. Chave `RecentApps` (Windows 10 vs. Windows 11)

```text
HKCU\Software\Microsoft\Windows\CurrentVersion\Search\RecentApps
```

| Característica | Detalhe Técnico e Comportamento Forense |
| :--- | :--- |
| **Disponibilidade por Versão** | Presente no **Windows 10** (especialmente edição Pro), mas **removido no Windows 11**. |
| **Valores por Subchave `{GUID}` de Aplicação** | `AppId`, `AppPath` (caminho completo do binário), **`LaunchCount`** (contador inteiro do número de execuções) e **`LastAccessedTime`** (timestamp `FILETIME64` em UTC / Little-Endian). |
| **Subchave `RecentItems`** | Debaixo de cada `{GUID}` de aplicação, regista até um **máximo de 10 ficheiros** abertos recentemente por esse programa. |
| **Armadilha Forense em `RecentItems`** | Ao atingir o **10.º ficheiro**, a substituição de entradas **não** segue uma fila cronológica estrita (FIFO); os itens remanescentes sofrem **ordenação alfabética**. Por conseguinte, os números das subchaves de `RecentItems` **não podem ser usados para inferir a ordem cronológica exata** dos últimos 10 ficheiros abertos (devendo consultar-se o timestamp individual de cada item). |

---

## Perguntas de revisão

1. **Qual a diferença prática entre configurar um binário na chave `HKLM\...\Run` versus `HKCU\...\Run`, e qual a diferença entre `Run` e `RunOnce`?**

> [!success]- Ver Resposta
> A chave `HKLM\...\Run` reside no hive global `SOFTWARE`, exige privilégios de **Administrador** para escrita e executa o programa sempre que **qualquer utilizador** inicia sessão na máquina. Já `HKCU\...\Run` reside no `NTUSER.DAT` do utilizador, **não requer privilégios de administrador** e dispara apenas no logon desse utilizador específico. Quanto a `RunOnce`, o comando é executado apenas uma única vez no arranque/logon seguinte e o valor é imediatamente eliminado pelo Windows.

2. **Em que ficheiro físico de hive reside a chave `MuiCache`, que tipo de aplicações regista e que metadados extrai do executável?**

> [!success]- Ver Resposta
> A chave `MuiCache` reside fisicamente no ficheiro **`UsrClass.dat`** do utilizador (`HKCU\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\MuiCache`). Regista apenas aplicações com **interface gráfica (GUI)** na sua primeira execução, extraindo do cabeçalho PE do binário o caminho completo e os valores `.FriendlyAppName` e `.ApplicationCompany`.

3. **Que tipo de marcador temporal é utilizado nos valores `FirstLogonTime` e `FirstLogonTimeOnCurrentInstallation` da chave `LogonStats` e qual a diferença entre ambos?**

> [!success]- Ver Resposta
> Ambos utilizam a estrutura binária **`SYSTEMTIME`** (128 bits / 16 bytes em Little-Endian). `FirstLogonTime` regista a data/hora absoluta em que o utilizador iniciou sessão pela primeira vez no computador, enquanto `FirstLogonTimeOnCurrentInstallation` regista o primeiro início de sessão após a última grande atualização de versão (*feature update*) do Windows.

4. **Quais são as duas limitações/armadilhas forenses associadas à chave `RecentApps` e à sua subchave `RecentItems`?**

> [!success]- Ver Resposta
> (1) A chave `RecentApps` existe no **Windows 10**, mas **foi descontinuada e removida no Windows 11**; (2) A subchave `RecentItems` guarda no máximo **10 ficheiros** recentes por aplicação, mas quando atinge o 10.º ficheiro, as entradas remanescentes são reordenadas **alfabeticamente** e não por ordem cronológica (FIFO), pelo que o número da subchave não reflete a sequência temporal de abertura.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Salvaguarda e Monitorização do Registry]] | `Bloco 06` |
| **Seguinte** | [[Artefactos Forenses de Interação do Utilizador (MRU e TypedPaths)]] | `mesmo bloco` |
| **Índice** | [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]] · [[00 ASSI]] | `Bloco 07` |

### Conceitos Relacionados

* [[Estrutura e Hives do Windows Registry]] · `Bloco 05`
* [[Timestamps e Épocas Temporais (UNIX Epoch vs. Windows FILETIME)]] · `Comum/`
* [[Artefacto Forense UserAssist]] · `mesmo bloco`
