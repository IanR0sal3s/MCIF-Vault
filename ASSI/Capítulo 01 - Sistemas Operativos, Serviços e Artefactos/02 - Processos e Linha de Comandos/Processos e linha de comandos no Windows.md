---
title: Processos e linha de comandos no Windows
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
tipo: procedimento
tags:
  - windows
  - processos
  - sysinternals
  - cli
aliases:
  - Processos Windows
  - Linha de Comandos
  - tasklist
  - pslist
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
atualizado: 2026-09-24
---

# Processos e Linha de Comandos no Windows

A interface de linha de comandos (CLI) constitui um mecanismo fundamental de interação, diagnóstico e administração em ambientes Windows, possibilitando automação avançada através de scripts (Batch, PowerShell, Python ou Perl).

O acesso à consola do sistema pode ser efetuado através de:
* Execução padrão: `Win+R` $\rightarrow$ `cmd`.
* Modo elevado: arranque do `cmd` como Administrador, indispensável para comandos de gestão de serviços e políticas de segurança (como `sc config`, `net stop` ou comandos de auditoria do sistema).

---

## Boas Práticas: Tratamento de Espaços em Nomes de Ficheiros

No interpretador de comandos (`cmd.exe`), o caracter de espaço atua como delimitador de argumentos. Quando nomes de pastas ou ficheiros contêm espaços, o interpretador divide o caminho em múltiplos parâmetros incorretos:
* *Exemplo*: O comando `dir Pasta 1` interpreta `Pasta` como primeiro argumento e `1` como segundo argumento.
* *Correção*: É fortemente recomendado utilizar o caracter de sublinhado (`_`) em vez de espaços. Caso existam espaços, o caminho deve ser obrigatoriamente delimitado por aspas: `dir "Pasta 1"`.

---

## Utilitários de Listagem e Auditoria de Processos

A monitorização de processos ativos é realizada através de ferramentas nativas e utilitários da suite Sysinternals:

| Ferramenta | Origem | Capacidades e Cenário de Uso |
| :--- | :--- | :--- |
| **`tasklist`** | Nativo (Windows) | Listagem de processos ativos; filtragem por critérios; mapeamento de serviços, DLLs e pacotes UWP. |
| **Gestor de Tarefas** | Nativo (`Ctrl+Shift+Esc`) | Monitorização visual de recursos (CPU, Memória, Disco, Rede); no Windows 11 inclui atalho direto para o Gestor de Serviços. |
| **Process Explorer** | Sysinternals | Visualização gráfica em árvore de processos pai/filho; localizador de *handles* e DLLs bloqueadas; deteção de processos ocultos. |
| **`pslist`** | Sysinternals | Utilitário CLI flexível; suporte para árvore (`-t`), memória detalhada (`-m`), threads (`-d`) e conexão remota a computadores da rede (`\\computador`). |
| **`pskill`, `psexec`, `psservice`** | Sysinternals | Terminação de processos, execução remota de comandos e gestão granular de serviços. |

### Sintaxe e Filtros Avançados do `tasklist`

O utilitário `tasklist` combina múltiplas valências de diagnóstico num único comando:

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

## A Suite Sysinternals e o Risco do `psexec`

A suite Sysinternals (originalmente criada por Mark Russinovich e integrada pela Microsoft) fornece utilitários avançados orientados para o administrador de sistemas e analistas de segurança.

> [!WARNING] Risco de Segurança do `psexec`
> Embora o `psexec` tenha sido concebido para administração remota legítima, é **frequentemente empregue por atacantes para efetuar movimento lateral** em redes Windows. O utilitário permite executar comandos e binários remotamente com privilégios de `SYSTEM` sem necessidade de software cliente instalado previamente na máquina de destino.

### Operações com o `pslist`
O `pslist` disponibiliza opções avançadas de depuração em linha de comandos:
* `-d`: Mostra o detalhe de todas as threads do processo.
* `-m`: Exibe o mapeamento detalhado de memória (Working Set, Virtual Memory, Peak).
* `-t`: Reconstrói a árvore genealógica de processos (relação pai-filho).
* `-s [n]`: Opera em modo interativo de monitorização em tempo real (análogo ao Gestor de Tarefas), atualizado a cada *n* segundos.
* `\\computador -u <user> -p <pass>`: Executa a auditoria de processos num computador remoto com credenciais autenticadas.

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

## Notas relacionadas

- [[Comando forfiles]]
- [[Serviços Windows]]
- [[svchost.exe]]
- [[Aplicações UWP (Universal Windows Platform) - Visão Geral]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
