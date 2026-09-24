---
title: Artefactos Forenses de Execução e Persistência no Registry
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
tipo: conceito
tags:
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

O Registry mantém múltiplos registos que documentam tanto os programas configurados para arrancar automaticamente com o sistema operativo como o histórico de programas e ficheiros acedidos pelo utilizador.

---

## Chaves de Arranque Automático (*Run* e *RunOnce*)

Os pontos de extensão de inicialização automática (*Auto-Start Execution Points* - ASEPs) mais explorados por software malicioso residem sob o ramo `CurrentVersion`:

| Chave do Registry | Âmbito | Comportamento de Execução |
| :--- | :--- | :--- |
| `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run` | Máquina (Todos os utilizadores) | Executado automaticamente sempre que qualquer utilizador inicia sessão no computador. |
| `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce` | Máquina (Todos os utilizadores) | Executado uma única vez no arranque subsequente; a entrada é **eliminada** após o lançamento (comum em instaladores e atualizações). |
| `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` | Utilizador Atual | Executado automaticamente apenas quando o utilizador específico inicia a sua sessão (não requer privilégios de administrador para ser configurado). |
| `HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce` | Utilizador Atual | Executado uma única vez na próxima sessão do utilizador atual e subsequentemente apagado. |

### Utilitário `autoruns` (Sysinternals)

O utilitário de referência para auditoria e resposta a incidentes é o **Autoruns**. Ao contrário de ferramentas nativas simples, o Autoruns analisa dezenas de vetores de arranque em simultâneo:
* Chaves `Run` e `RunOnce` (em 32 bits, 64 bits e WOW64).
* Tarefas Agendadas (*Scheduled Tasks*).
* Serviços do Windows e Drivers de kernel.
* Notificações de Winlogon, extensões do Explorer, *AppInit DLLs* e sequestros de imagem (*Image Hijacks / IFEO*).

---

## Chave `LogonStats` (Primeiro Início de Sessão)

Localizada no hive de utilizador (`NTUSER.DAT`):

```text
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\LogonStats
```

Armazena em formato binário [[Marcadores Temporais no Windows (Timestamps)|SYSTEMTIME]] (128 bits / 16 bytes em Little-Endian):
* **`FirstLogonTime`**: data e hora em que o utilizador iniciou sessão pela primeira vez no computador.
* **`FirstLogonTimeOnCurrentInstallation`**: data e hora do primeiro início de sessão na versão/instalação atual do SO (após atualizações de versão do Windows).
* **`LastLogonBuildNumber`** e **`LastLogonBuildRevision`**: versão exata da compilação do Windows.

A descodificação destes campos em lote é efetuada através de scripts em Python (como o script de parsing de referências, disponível em `https://pastebin.com/kC702Y8A`):

```bash
python reg_systemtime_parser.py logon_from_reg.txt
```

---

## Cache MUI (`MuiCache`)

O subsistema **MUI** (*Multilingual User Interface*) gere a internacionalização de aplicações no Windows:
* Sempre que uma aplicação com **interface gráfica (GUI)** é iniciada pela primeira vez, o sistema operativo extrai os metadados do cabeçalho do executável e regista-os em:

```text
HKCU\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\MuiCache
```

(Fisicamente gravado no ficheiro `UsrClass.dat` do utilizador).

### Dados Registados:
* Caminho completo do executável (`.FriendlyAppName` e `.ApplicationCompany`).
* *Exemplo*:
  * `"C:\Program Files\Mozilla Firefox\firefox.exe.FriendlyAppName" = "Firefox"`
  * `"C:\Program Files\Mozilla Firefox\firefox.exe.ApplicationCompany" = "Mozilla Corporation"`

A ferramenta **MUICacheView** (NirSoft) lista todo este inventário graficamente. Constitui evidência pericial direta de que uma determinada aplicação gráfica existiu e foi invocada pelo menos uma vez pelo utilizador.

---

## Chave `RecentApps` (Windows 10)

```text
HKCU\Software\Microsoft\Windows\CurrentVersion\Search\RecentApps
```

> [!NOTE] Limitação de Versão
> Este artefacto está presente no **Windows 10** (especialmente Pro), mas **foi removido no Windows 11**.

Regista para cada aplicação:
* `AppId` e `AppPath` (caminho completo do binário).
* `LaunchCount`: contador de vezes que a app foi executada.
* `LastAccessedTime`: marca temporal FILETIME64 em UTC/Little-Endian.

### Subchave `RecentItems` e Armadilha Forense:
* Lista até um **máximo de 10 ficheiros** recentemente abertos pela aplicação.
* **Armadilha forense**: Ao atingir o 10.º ficheiro, a substituição de entradas não é efetuada por ordem cronológica (FIFO estrito); os itens remanescentes sofrem ordenação alfabética. **Não pode ser usado para inferir a ordem cronológica exata dos últimos 10 ficheiros abertos**.

## Notas relacionadas

- [[Estrutura e Hives do Windows Registry]]
- [[Marcadores Temporais no Windows (Timestamps)]]
- [[Salvaguarda e Monitorização do Registry]]
- [[Artefactos Forenses de Interação do Utilizador (MRU e TypedPaths)]]
- [[Artefacto Forense UserAssist]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
