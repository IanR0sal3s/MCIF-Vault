---
title: Threat Hunting em EVTX - Regras SIGMA, APT-Hunter, Chainsaw e Hayabusa
tipo: ferramenta
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 4
bloco: 3
fonte_aula: EI_ASSI_1S2026-27_cap04_v01_LOGs_parte01_v1---ULO.pdf
tags:
  - assi
  - logs
  - evtx
  - sigma
  - apt-hunter
  - chainsaw
  - hayabusa
  - threat-hunting
  - timeline-explorer
aliases:
  - Regras SIGMA
  - APT-Hunter
  - Chainsaw
  - Hayabusa
atualizado: 2026-11-21
---

# Threat Hunting em EVTX - Regras SIGMA, `APT-Hunter`, `Chainsaw` e `Hayabusa`

Dado o elevado volume de ficheiros e eventos `.evtx`, a deteção de atividades suspeitas ou *Advanced Persistent Threats* (APT) apoia-se em regras padronizadas (**SIGMA**) e ferramentas automatizadas de triagem e geração de timelines.

## 1. Formato `SIGMA`

* **Definição**: formato genérico em **YAML** para descrever assinaturas e condições de deteção sobre registos de log (repositório oficial: `SigmaHQ/sigma`).
* **Analogia fundamental**: ***SIGMA* está para os logs como o [[YARA - Introdução, Estrutura de Regras, Metadados e Condições|YARA]] está para os ficheiros**.
* **Portabilidade**: permite partilhar regras de deteção (por exemplo, deteção de remoção de ficheiros *Prefetch*) e convertê-las para queries de diferentes SIEMs ou SQL.

---

## 2. Comparativo das Ferramentas de Threat Hunting

| Ferramenta | Linguagem | Base de Deteção | Formatos de Saída | Caso de Uso Principal |
| :--- | :--- | :--- | :--- | :--- |
| **`APT-Hunter`** | Python | Regras internas para EVTX tradicionais | `CSV`, `XLSX` (múltiplas folhas) | Triagem focada em padrões de APTs e exportação para timeline (`Timeline Explorer`, `Timesketch`). |
| **`Chainsaw`** | Rust | Pesquisa direta (ID/string/regex) + modo `hunt` (regras **SIGMA** + heurística interna) | `ASCII`, `CSV`, `JSON` | *First-response* muito rápido e multiplataforma (Windows, Linux, macOS). |
| **`Hayabusa`** | Rust (GPL v3.0, *Yamato-Security*) | Regras **SIGMA** atualizáveis | `CSV` em formato `log2timeline` | Construção rápida de timelines forenses prontas a abrir no `Timeline Explorer`. |

---

## 3. Comandos Essenciais

### `APT-Hunter`
```cmd
apt-hunter -p Dir_LOGS -o Results
```
(`-p` indica a pasta com os `.evtx`; `-o` define o prefixo dos ficheiros CSV/XLSX gerados.)

### `Chainsaw`
Subcomandos principais: `search`, `hunt`, `check` e `help`.

```cmd
:: Pesquisa por Event ID (ex.: 4624 login) numa pasta de logs
chainsaw search PATH_EVT_LOGS -e 4624

:: Pesquisa case-insensitive (-i) por string com saída JSON (-j)
chainsaw search stringA -i PATH_EVT_LOGS -j > a.json

:: Pesquisa com expressão regular (-r) e gravação em ficheiro (-o)
chainsaw search -r "string[a-zA-Z]" PATH_EVT_LOGS -o output.txt

:: Modo hunt com regras SIGMA, mapeamento e intervalo temporal
chainsaw hunt evtx_attack_samples/ -s sigma/ --mapping mappings/sigma-event-logs-all.yml --from "2023-03-17T19:09:39" --to "2023-03-17T19:09:50" --json

:: Modo hunt com saída em múltiplos CSV (um por classe de evento suspeito)
chainsaw hunt evtx_attack_samples/ -s sigma/ --mapping mappings/sigma-event-logs-all.yml --from "2023-03-17T19:09:39" --csv --output CSVDir
```

### `Hayabusa`
```cmd
:: Atualizar regras SIGMA embutidas
hayabusa.exe update-rules

:: Gerar timeline CSV (formato log2timeline) a partir de uma pasta de EVTX
hayabusa.exe csv-timeline -d logsDir -o hayabusa.csv

:: Modo super-verbose (maior detalhe por evento)
hayabusa.exe csv-timeline -d logsDir -o hayabusa-super-verbose.csv -p super-verbose
```

Os ficheiros CSV gerados pelo `APT-Hunter`, `Chainsaw` ou `Hayabusa` podem ser analisados diretamente no **`Timeline Explorer`** (Eric Zimmerman). Para treino e testes, destacam-se repositórios públicos como **`EVTX-ATTACK-SAMPLES`** (*sbousseaden*) e amostras do `LogonTracer`.

---

## Perguntas de revisão

1. **Qual é a analogia entre `SIGMA` e `YARA`, e em que formato são escritas as regras `SIGMA`?**

> [!success]- Ver Resposta
> O `SIGMA` está para os logs como o `YARA` está para os ficheiros: define assinaturas genéricas em **YAML** para detetar comportamentos maliciosos em logs, convertíveis para vários SIEMs e ferramentas.

2. **Qual a diferença entre os subcomandos `search` e `hunt` no `Chainsaw`?**

> [!success]- Ver Resposta
> `search` procura diretamente eventos por Event ID (`-e`), string (`-i`) ou regex (`-r`); `hunt` aplica regras **SIGMA** (`-s` e `--mapping`) e heurísticas internas para identificar ameaças automaticamente, suportando filtros temporais (`--from`/`--to`).

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Análise Forense de USB e Crashes nos Logs EVTX]] | `muda do Bloco 02` |
| **Seguinte** | [[Monitorização Avançada com Sysmon (Sysinternals)]] | `mesmo bloco` |
| **Índice** | [[Capítulo 4 - Logs]] · [[00 ASSI]] | `Bloco 03` |

### Conceitos Relacionados

* [[YARA - Introdução, Estrutura de Regras, Metadados e Condições]] · `ASSI · Cap. 3`
* [[Extração e Análise Offline de EVTX (evtx_dump, jq, FullEventLogView e EvtxECmd)]] · `ASSI · Cap. 4`
