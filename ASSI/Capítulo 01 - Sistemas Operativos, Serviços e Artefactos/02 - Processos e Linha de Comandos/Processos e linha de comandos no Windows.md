---
title: Processos e linha de comandos no Windows
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 2
tipo: procedimento
tags:
  - assi
  - windows
  - processos
  - sysinternals
  - cli
aliases:
  - Processos Windows
  - Linha de Comandos
  - tasklist
  - pslist
  - btop4win
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
fontes:
  - "https://github.com/aristocratos/btop4win"
atualizado: 2026-10-16
---

# Processos e Linha de Comandos no Windows

A interface de linha de comandos (CLI) do Windows e os utilitários de inspeção de processos (`tasklist`, suite Sysinternals e `btop4win`) permitem auditar processos ativos, módulos DLL, serviços alojados e árvores de execução.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: O sistema operativo organiza a execução de programas em processos isolados (identificados por um PID) que carregam bibliotecas DLL e criam *threads*; as ferramentas de CLI expõem estas estruturas internas para administração e automação via scripts.
> * **Porque importa (Forense / Segurança)**: Na resposta a incidentes e triagem *live*, correlacionar processos com serviços (`tasklist /SVC`), DLLs carregadas (`tasklist /M`) e relações pai-filho (`pslist -t`) permite detetar injeção de código, processos anómalos e movimentos laterais via `psexec`.
> * **Pontos Críticos para Exame**:
>   * Espaços em caminhos no `cmd.exe` atuam como separadores de argumentos — usar sempre aspas duplas (ex.: `dir "Pasta 1"`) ou sublinhados (`_`).
>   * Dominar os parâmetros de `tasklist` (`/SVC`, `/M`, `/APPS`, `/V`, `/FI`) e de `pslist` (`-t`, `-m`, `-d`, `-x`, `-e`, `-s`).

---

## Acesso à Consola e Tratamento de Espaços em Argumentos

A interface de linha de comandos (CLI) constitui um mecanismo fundamental de interação, diagnóstico e administração em ambientes Windows, possibilitando automação avançada através de scripts (Batch, PowerShell, Python ou Perl).

O acesso à consola do sistema pode ser efetuado através de:

* **Execução padrão**: `Win+R` $\rightarrow$ `cmd`.
* **Modo elevado**: arranque do `cmd` como Administrador, indispensável para comandos de gestão de serviços e políticas de segurança (como `sc config`, `net stop` ou comandos de auditoria do sistema).

### Boas Práticas: Tratamento de Espaços em Nomes de Ficheiros
No interpretador de comandos (`cmd.exe`), o caracter de espaço atua como delimitador de argumentos. Quando nomes de pastas ou ficheiros contêm espaços, o interpretador divide o caminho em múltiplos parâmetros incorretos:

* *Exemplo de Erro*: O comando `dir Pasta 1` interpreta `Pasta` como primeiro argumento e `1` como segundo argumento.
* *Correção*: É fortemente recomendado utilizar o caracter de sublinhado (`_`) em vez de espaços. Caso existam espaços, o caminho deve ser obrigatoriamente delimitado por aspas: `dir "Pasta 1"`.

---

## Utilitários de Listagem e Auditoria de Processos

A monitorização de processos ativos é realizada através de ferramentas nativas, utilitários da suite Sysinternals e monitores de terminal:

| Ferramenta | Origem | Capacidades e Cenário de Uso |
| :--- | :--- | :--- |
| **`tasklist`** | Nativo (Windows) | Listagem de processos ativos; filtragem por critérios; mapeamento de serviços, DLLs e pacotes UWP. |
| **Gestor de Tarefas** | Nativo (`Ctrl+Shift+Esc`) | Monitorização visual de recursos (CPU, Memória, Disco, Rede); no Windows 11 inclui atalho direto para o Gestor de Serviços. |
| **Process Explorer** | Sysinternals | Visualização gráfica em árvore de processos pai/filho; localizador de *handles* e DLLs bloqueadas; deteção de processos ocultos. |
| **`pslist`** | Sysinternals | Utilitário CLI flexível; suporte para árvore (`-t`), memória (`-m`), threads (`-d`), vista combinada (`-x`) e conexão remota (`\\computador`). |
| **`pskill`, `psexec`, `psservice`** | Sysinternals | Terminação de processos, execução remota de comandos e gestão granular de serviços. |
| **`btop++` (`btop4win`)** | Open-source (`aristocratos/btop4win`) | Monitor interativo de recursos em modo texto (TUI) para Windows, exibindo utilização de CPU, RAM, discos, rede e árvore/filtragem de processos. |

---

## Anatomia e Filtros Avançados do `tasklist`

O utilitário nativo `tasklist` combina múltiplas valências de diagnóstico num único comando:

```cmd
tasklist [/V | /SVC | /M | /APPS] [/FI "<Filtro>"]
```

| Parâmetro | Função Principal | Utilidade Prática e Forense |
| :---: | :--- | :--- |
| **`/V`** | Modo Verboso (*Verbose*) | Exibe informações estendidas: estado, conta de utilizador que executa o processo, tempo de CPU e título da janela. |
| **`/SVC`** | Mapeamento de Serviços | Lista os serviços de sistema alojados em cada processo (indispensável para auditar instâncias de [[svchost.exe]]). |
| **`/M`** | Módulos e Bibliotecas DLL | Lista todas as bibliotecas DLL carregadas em memória por cada processo ativo. |
| **`/APPS`** | Aplicações Modernas UWP | Filtra e exibe os processos associados a pacotes [[Aplicações UWP (Universal Windows Platform) - Visão Geral\|UWP]]. |
| **`/FI "..."`** | Filtro Condicional (*Filter*) | Restringe a saída com operadores (`eq`, `ne`, `gt`, `lt`, `ge`, `le`) sobre propriedades como `MEMUSAGE` (em KB) ou `IMAGENAME`. |

### Exemplos Práticos do `tasklist`

```cmd
REM Listagem básica de processos
tasklist

REM Modo detalhado e verboso (/V)
tasklist /V

REM Listar os serviços hospedados por cada processo (essencial para svchost.exe)
tasklist /SVC

REM Listar todos os módulos e bibliotecas DLL carregados pelos processos
tasklist /M

REM Listar processos associados a aplicações modernas UWP
tasklist /APPS

REM Filtrar processos com consumo de memória física superior a 45 MB (45000 KB)
tasklist /FI "MEMUSAGE ge 45000"

REM Combinar filtros: aplicações UWP com consumo de memória superior a 45 MB
tasklist /APPS /FI "MEMUSAGE ge 45000"

REM Filtrar por nome específico de executável
tasklist /FI "IMAGENAME eq notepad.exe"

REM Contabilizar o número de instâncias de processos svchost em execução
tasklist /svc | find /c "svchost.exe"
```

---

## A Suite Sysinternals: `pslist` e o Risco do `psexec`

A suite Sysinternals (originalmente criada por Mark Russinovich e integrada pela Microsoft) fornece utilitários avançados orientados para o administrador de sistemas e analistas de segurança.

> [!WARNING] Risco de Segurança do `psexec`
> Embora o `psexec` tenha sido concebido para administração remota legítima, é **frequentemente empregue por atacantes para efetuar movimento lateral** em redes Windows. O utilitário permite executar comandos e binários remotamente com privilégios de `SYSTEM` sem necessidade de software cliente instalado previamente na máquina de destino.

### Anatomia do Comando `pslist`

```cmd
pslist [-d] [-m] [-x] [-t] [-e] [-s [n]] [\\computador [-u <user>] [-p <pass>]] [<nome_ou_pid>]
```

| Parâmetro | Função Operacional |
| :---: | :--- |
| **`-d`** | Mostra o detalhe de todas as *threads* do processo. |
| **`-m`** | Exibe o mapeamento detalhado de memória (*Working Set*, *Virtual Memory*, *Peak*). |
| **`-x`** | Mostra simultaneamente processos, informação de memória e *threads* (combina `-d` e `-m`). |
| **`-t`** | Reconstrói a árvore genealógica de processos (relação pai-filho). |
| **`-e`** | Exige correspondência exata (*exact match*) do nome do processo pesquisado. |
| **`-s [n]`** | Opera em modo interativo de monitorização em tempo real (*task-manager mode*), atualizado a cada *n* segundos. |
| **`\\computador -u <user> -p <pass>`** | Executa a auditoria de processos num computador remoto com credenciais autenticadas. |

---

## Atalhos de Teclado Úteis para Diagnóstico

| Atalho | Função e Utilidade |
| :--- | :--- |
| `Win + V` | Histórico avançado do Clipboard (área de transferência multinível). |
| `Win + .` | Seletor de caracteres especiais e emojis. |
| `Win + E` | Abertura do Explorador de Ficheiros. |
| `Win + Q` | Pesquisa global do Windows (interage diretamente com o [[Windows Search]]). |
| `Win + Shift + S` | Captura de ecrã seletiva com opções de recorte e OCR. |
| `Win + N` | Painel de notificações e calendário. |

---

## Perguntas de revisão

1. **Qual é o comando exato do `tasklist` para listar todas as aplicações UWP em execução cujo consumo de memória seja igual ou superior a 45 MB?**

> [!success]- Ver Resposta
> `tasklist /APPS /FI "MEMUSAGE ge 45000"` (o filtro `MEMUSAGE` do `tasklist` é expresso em kilobytes, pelo que 45 MB correspondem a 45000 KB, combinando o operador `ge` — *greater than or equal* — com a flag `/APPS`).

2. **Na ferramenta `pslist` (Sysinternals), qual é a diferença entre os parâmetros `-t`, `-x` e `-e`?**

> [!success]- Ver Resposta
> * **`-t`**: apresenta a árvore hierárquica de processos (relação pai-filho).
> * **`-x`**: exibe em simultâneo a informação de processos, detalhes de memória (`-m`) e *threads* (`-d`).
> * **`-e`**: força a correspondência exata (*exact match*) do nome do processo pesquisado.

3. **Por que razão a ferramenta legítima `psexec` (Sysinternals) é um indicador crítico em investigações de resposta a incidentes?**

> [!success]- Ver Resposta
> Porque é amplamente abusada por atacantes para realizar **movimento lateral** em redes Windows, permitindo executar comandos e binários remotamente com privilégios máximos (`SYSTEM`) sem exigir instalação prévia de agentes na máquina alvo.

4. **Como se contabiliza na linha de comandos o número exato de processos `svchost.exe` em execução num sistema Windows?**

> [!success]- Ver Resposta
> Através do encadeamento (*pipe*) do `tasklist` com o comando `find /c`:
> `tasklist /svc | find /c "svchost.exe"`

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[PKfail - Cadeia de Ataque e Deteção Forense]] | `Bloco 01` |
| **Seguinte** | [[Comando forfiles]] | `mesmo bloco` |
| **Índice** | [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]] · [[00 ASSI]] | `Bloco 02` |

### Conceitos Relacionados

* [[Serviços Windows]] · `Bloco 03`
* [[svchost.exe]] · `Bloco 03`
* [[Aplicações UWP (Universal Windows Platform) - Visão Geral]] · `Bloco 04`
* [[Investigação Forense Digital - Análise Live vs Post-Mortem]] · `AFD1 · Cap. 1`
* [[Diretrizes de Manuseamento - Identificação, Preservação, Isolamento e Correlação]] · `AFD1 · Cap. 1`
