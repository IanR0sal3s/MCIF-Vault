---
title: Loki-RS (Versão Rust) - Compilação, Atualização e Parâmetros CLI
tipo: ferramenta
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 3
bloco: 1
fonte_aula: YARA & LOKI (Prof. Patrício Domingues)
tags:
  - assi
  - forense
  - loki
  - loki-rs
  - rust
  - yara
  - ioc
aliases:
  - Loki-RS
  - Loki versão Rust
  - loki-util.exe
  - Ficha de trabalho 14
atualizado: 2026-11-11
---

# Loki-RS (Versão Rust) — Compilação, Atualização e Parâmetros CLI

O **Loki-RS** é a reimplementação multi-thread em Rust do scanner de IOCs LOKI, combinando o motor YARA em Rust, atualização separada via `loki-util.exe` e envio remoto de logs para triagem forense.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema / Deteção)**: O LOKI original em Python apresentava menor velocidade em discos volumosos; a reescrita em Rust tira partido de paralelismo *multi-thread* nativo e do motor `YARA-X`, mantendo segurança de memória.
> * **Porque importa (Forense / IR)**: Separa o utilitário de atualização (`loki-util.exe --update`) do binário de varrimento (`loki.exe`) para suportar kits portáteis offline (`WinFE`/USB) e permite suprimir toda a escrita em disco local enviando alertas remotamente via rede.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Comportamento por omissão de `-f`**: omitir `-f` / `--folder` faz o `loki.exe` varrer **todo o sistema** (*entire system*).
>   * **Zero-write em triagem *live***: por omissão o `Loki-RS` grava `.log`, `.jsonl` e `.html` localmente; para não poluir o suporte suspeito deve combinar **`--no-log --no-jsonl --no-html -r host:port`**.
>   * **`--scan-hard-drives` vs. `--scan-all-drives` vs. `--scan-all-files`**: o primeiro restringe-se a discos locais fixos, o segundo inclui USB/cloud/partilhas de rede, e o terceiro analisa todos os ficheiros independentemente do tipo ou extensão.

---

## 1. Vantagens, Compilação e Fluxo de Operação do `Loki-RS`

O **`Loki-RS`** ([repositório oficial no GitHub](https://github.com/Neo23x0/Loki-RS)) é a **reimplementação do [[Scanner de IOCs LOKI (Versão Python) - Métodos de Deteção e Configuração|scanner de IOCs LOKI]] na linguagem de programação Rust**, concebida como um scanner *multi-thread* de alto desempenho (*High-Performance, Multi-threaded YARA & IOC Scanner*).

* **Desempenho Superior**: a versão em Rust é **muito mais rápida que a versão original em Python**, tirando partido de paralelismo *multi-thread* nativo e do motor [[YARA-X (Reimplementação em Rust) e Ferramenta CLI yr|YARA em Rust]].

**Compilação a partir do Código-Fonte:**

Utilizando o gestor de pacotes e compilador do ecossistema Rust (`cargo`), o código-fonte do `Loki-RS` pode ser compilado em modo otimizado (*release*) com o comando:

```bash
cargo b --release
```

**Fluxo de Trabalho em 2 Comandos (Slide 32):**

**1. Descarregar e atualizar as regras YARA e IOCs para o Loki-RS** (através do utilitário auxiliar `loki-util.exe`):

```cmd
loki-util.exe --update
```

**2. Executar o varrimento com o Loki-RS numa pasta específica** (através do binário principal `loki.exe`):

```cmd
loki.exe -f c:\PASTA
```

---

## 2. Parâmetros de Linha de Comandos do `loki.exe` (`Loki-RS`)

A interface de linha de comandos do `loki.exe` organiza as suas opções em três categorias (**Scan Target**, **Scan Control** e **Output Options**), conforme apresentado no Slide 33:

```text
Loki-RS - High-Performance, Multi-threaded YARA & IOC Scanner
Usage: loki.exe [OPTIONS]
```

### A. Opções Gerais e Alvo do Varrimento (*Scan Target*)

| Opção | Descrição Técnica (`loki.exe --help`) |
| :--- | :--- |
| **`-h, --help`** | Imprime a mensagem de ajuda. |
| **`-f, --folder <FOLDER>`** | Pasta raiz a analisar. **Por omissão, se omitida, analisa o sistema inteiro (*entire system*)**. |

### B. Controlo do Varrimento (*Scan Control*)

| Opção | Descrição Técnica (`loki.exe --help`) |
| :--- | :--- |
| **`--no-procs`** | **Não analisa processos** em execução na memória RAM. |
| **`--no-fs`** | **Não analisa o sistema de ficheiros** (restringe o varrimento apenas aos processos em memória). |
| **`--no-archive`** | **Não analisa o interior de ficheiros de arquivo comprimidos** (ex.: `.zip`). |
| **`--scan-hard-drives`** | Analisa todos os discos rígidos locais (Windows: unidades fixas; Linux/macOS: sistemas de ficheiros locais). |
| **`--scan-all-drives`** | Analisa **todas as unidades**, incluindo unidades montadas, drives USB, drives na cloud e partilhas de rede. |
| **`--scan-all-files`** | Analisa **todos os ficheiros independentemente do seu tipo ou extensão**. |

### C. Opções de Saída e Relatórios (*Output Options*)

| Opção | Descrição Técnica (`loki.exe --help`) |
| :--- | :--- |
| **`-l, --log <LOG>`** | Especifica o ficheiro de saída de log em texto simples (por omissão: `loki_<hostname>_<date>.log`). |
| **`--no-log`** | Desativa a geração do ficheiro de log em texto simples. |
| **`-j, --jsonl <JSONL>`** | Especifica o ficheiro de saída em formato **JSON Lines** (por omissão: `loki_<hostname>_<date>.jsonl`). |
| **`--no-jsonl`** | Desativa a geração do ficheiro de saída JSONL. |
| **`--no-html`** | Desativa a geração automática do relatório em **HTML**. |
| **`-r, --remote <REMOTE>`** | Ativa o envio remoto de logs indicando o destino no formato **`host:port`**. |
| **`-p, --remote-proto <REMOTE_PROTO>`** | Protocolo de transporte para o envio remoto de logs: **`udp`** ou **`tcp`** (por omissão: `udp`). |
| **`--remote-format <REMOTE_FORMAT>`** | Formato dos logs enviados remotamente: **`syslog`** ou **`json`** (por omissão: `syslog`). |
| **`--no-tui`** | Desativa a interface gráfica de terminal (*TUI*) e utiliza o registo padrão em linha de comandos. |

---

## 3. Referência Laboratorial: Ficha de Trabalho 14 (`YARA & LOKI`)

A **Ficha 14** consolida em laboratório os três componentes deste bloco:
1. **`yara` clássico**: aplicação de `suspicious_strings.yar` sobre `sysmon.exe` usando `-L` (comprimento/offset) e `-m` (metadados);
2. **`YARA-X` (`yr`)**: geração (com validação crítica) de uma regra para detetar bases **SQLite 3** (`"SQLite format"`) e **SQLite WAL**, compilação via `yr compile sqlite.yr -o sqlite.yrc` e varrimento em `%LocalAppData%` com `yr scan -r -C sqlite.yrc %LocalAppData%`;
3. **Extra-Aula (`Loki-RS` e `yarac`)**: compilação com `cargo b --release`, atualização via `loki-util.exe update`, execução com `loki.exe -f c:\PASTA` e compilação/execução de uma regra de IPv4 (`yarac ip.yar ip.yarac` $\to$ `yara -C ip.yarac FICHEIRO_ALVO`).

---

## 4. Implicações Forenses e Anatomia da Triagem Live Remota

Durante uma intervenção *live* num sistema comprometido (ver [[Diretrizes de Manuseamento - Identificação, Preservação, Isolamento e Correlação]] em AFD1), gravar ficheiros `.log`, `.jsonl` e `.html` no disco suspeito pode sobrescrever setores no espaço não alocado. As opções do `Loki-RS` permitem desativar todos os ficheiros locais e transmitir os resultados diretamente pela rede para o servidor do perito:

```text
loki.exe --no-log --no-jsonl --no-html -r <IP:PORT> -p tcp --remote-format json
│        │        │          │         │            │      └─ Formato remoto: json (padrão: syslog)
│        │        │          │         │            └──────── Transporte TCP fiável (padrão: udp)
│        │        │          │         └───────────────────── Servidor recetor remoto no formato host:port
│        │        │          └─────────────────────────────── Suprime geração local de relatório .html
│        │        └────────────────────────────────────────── Suprime geração local de ficheiro .jsonl
│        └─────────────────────────────────────────────────── Suprime geração local de ficheiro .log
└──────────────────────────────────────────────────────────── Scanner principal Loki-RS (sem escrita local)
```

---

## Além da aula

* **Integração em Pen USB de Triagem e WinFE ([[00 AFD1|AFD1]])**: no Capítulo 2 de AFD1 ([[Dispositivos de Arranque Forense - Disquetes DOS, Live CDs Linux, WinFE e USB]] e [[Ferramentas Portáteis de Triagem, Pesquisa e FTK Imager Lite]]), viu-se a importância de dispor de ferramentas portáteis pré-atualizadas. O `Loki-RS` separa explicitamente o binário de atualização (`loki-util.exe --update`, executado previamente na estação de trabalho do perito com acesso à Internet) do binário de varrimento (`loki.exe`), permitindo transportar a pasta com as assinaturas já atualizadas para correr offline numa máquina isolada da rede.

---

## Perguntas de revisão

1. **Como se compila o código-fonte do `Loki-RS` em modo otimizado e quais são os dois comandos do fluxo operacional padrão?**

> [!success]- Ver Resposta
> Compila-se com **`cargo b --release`**. O fluxo de trabalho em dois passos consiste em: (1) atualizar regras YARA e IOCs via **`loki-util.exe --update`**; e (2) executar o varrimento com **`loki.exe -f c:\PASTA`** (ou omitir `-f` para analisar todo o sistema).

2. **No `loki.exe` (`Loki-RS`), qual a diferença entre `--scan-hard-drives`, `--scan-all-drives` e `--scan-all-files`, e o que acontece se omitir `-f`?**

> [!success]- Ver Resposta
> Se omitir `-f` (`--folder`), o `loki.exe` analisa **o sistema inteiro** por omissão. **`--scan-hard-drives`** analisa apenas discos rígidos locais fixos; **`--scan-all-drives`** abrange todas as unidades, incluindo USB, cloud e partilhas de rede; e **`--scan-all-files`** analisa todos os ficheiros independentemente do seu tipo ou extensão.

3. **Que ficheiros de relatório gera o `Loki-RS` localmente por omissão e que combinação de parâmetros permite executar triagem *live* sem escrita em disco?**

> [!success]- Ver Resposta
> Por omissão gera três ficheiros locais: texto simples (`loki_<hostname>_<date>.log`), JSON Lines (`loki_<hostname>_<date>.jsonl`) e um relatório **HTML**. Em triagem *live*, deve suprimir-se toda a escrita local e enviar os eventos pela rede com **`--no-log --no-jsonl --no-html -r host:port`** (opcionalmente com `-p tcp --remote-format json`).

4. **Porque é que a separação entre `loki-util.exe` e `loki.exe` favorece ambientes de triagem offline e WinFE?**

> [!success]- Ver Resposta
> Porque o perito pode executar `loki-util.exe --update` previamente numa estação conectada à Internet, copiar o conjunto já atualizado para uma pen USB forense ou ambiente **WinFE**, e correr apenas o `loki.exe` offline no sistema alvo isolado da rede.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Scanner de IOCs LOKI (Versão Python) - Métodos de Deteção e Configuração]] | `mesmo bloco` |
| **Seguinte** | [[Alternate Data Streams (ADS) no NTFS - Arquitetura, Manipulação em CMD e PowerShell]] | `muda para Bloco 02` |
| **Índice** | [[Capítulo 3 - YARA - MOTW - Strings]] · [[00 ASSI]] | `Bloco 01` |

### Conceitos Relacionados

* [[YARA-X (Reimplementação em Rust) e Ferramenta CLI yr]] · `mesmo bloco`
* [[YARA - Introdução, Estrutura de Regras, Metadados e Condições]] · `mesmo bloco`
* [[Execução e Compilação no YARA (yara e yarac), Casos Reais (UPX, WannaCry) e LLMs]] · `mesmo bloco`
* [[Ferramentas Portáteis de Triagem, Pesquisa e FTK Imager Lite]] · `AFD1 · Cap. 2`
* [[Diretrizes de Manuseamento - Identificação, Preservação, Isolamento e Correlação]] · `AFD1 · Cap. 1`
