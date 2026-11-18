---
title: Scanner de IOCs LOKI (Versão Python) - Métodos de Deteção e Configuração
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
  - ioc
  - yara
  - incident-response
  - pe-sieve
aliases:
  - LOKI
  - Loki Scanner
  - Simple IOC and Incident Response Scanner
  - Loki Python
atualizado: 2026-11-11
---

# Scanner de IOCs LOKI (Versão Python) — Métodos de Deteção e Configuração

O **LOKI** é um scanner de IOCs de código aberto criado por Florian Roth que cruza regex de nomes, regras YARA, hashes criptográficos e ligações C2 sobre ficheiros em disco e processos em memória.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema / Deteção)**: Ferramentas isoladas obrigam a correr separadamente verificação de hashes, regras YARA e análise de ligações de rede; o LOKI agrega quatro vetores complementares de deteção num único scanner de resposta a incidentes.
> * **Porque importa (Forense / IR)**: Inspeciona simultaneamente o sistema de ficheiros e os processos em memória RAM (com apoio do `pe-sieve64.exe`), permitindo identificar persistência *fileless*, *process hollowing* e ligações a servidores C2 mesmo após eliminação do executável no disco.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Privilégios elevados**: deve ser executado como **Administrador** para conseguir inspecionar a memória de todos os processos e diretorias protegidas.
>   * **Limite padrão de tamanho (`-s`)**: por omissão ignora ficheiros superiores a **`5000` KB** ($\approx 5\text{ MB}$), salvo ajuste de `-s` ou uso de `--intense`.
>   * **`LOKI UPGRADER` (`signature-base`)**: quando `signature-base` não existe/está vazia (ou via `--update`), descarrega automaticamente os **7 conjuntos de assinaturas** do GitHub.

---

## 1. Características Gerais e Arquitetura do LOKI

* **Autor e Repositórios Oficiais**: o **LOKI (*Simple IOC and Incident Response Scanner*)** foi criado por **Florian Roth (`@cyb3rops`)** (Nextron Systems, autor também do `@thor_scanner`, Valhalla YARA rule feed, Sigma e yarGen), estando disponível no [Repositório Oficial do LOKI em Python](https://github.com/Neo23x0/Loki) (e na reescrita em Rust no [Repositório Oficial do Loki-RS](https://github.com/Neo23x0/Loki-RS), estudada em [[Loki-RS (Versão Rust) - Compilação, Atualização e Parâmetros CLI]]).
* **Deteção Proativa em Ficheiros e Memória**:
  * Empregue para deteção proativa de ameaças e *malware* em arquivos e em todo o sistema;
  * Verifica **ficheiros em disco** (assinaturas de *malware*, padrões conhecidos de comportamento malicioso);
  * Verifica também **processos em execução na memória RAM**.
* **Facilidade de Uso e Relatórios**:
  * Possui um ficheiro de configuração simples que permite especificar quais as regras [[YARA - Introdução, Estrutura de Regras, Metadados e Condições|YARA]] e diretorias a varrer;
  * Quando deteta potenciais ameaças, fornece um relatório detalhando exatamente quais os ficheiros ou processos que dispararam os alertas;
  * **Atualização automática**: atualiza as suas regras e base de assinaturas (`signature-base`) quando é lançado.

---

## 2. Os 4 Métodos de Deteção do LOKI

O motor de análise do LOKI combina **quatro métodos de deteção complementares** (Slide 28):

| # | Método de Deteção | Descrição e Funcionamento Técnico | Ficheiro na `signature-base` |
| :---: | :--- | :--- | :--- |
| **1** | **IOC com ficheiros (*File Name IOC*)** | Aplica **expressões regulares (Regex)** para detetar correspondências suspeitas em **nomes de ficheiros e caminhos completos** de diretorias. | `filename-iocs.txt` |
| **2** | **Yara Rule Check** | Procura correspondência de assinaturas YARA ([[YARA - Introdução, Estrutura de Regras, Metadados e Condições]]) tanto nos **dados de arquivos no disco** como na **memória dos processos em execução**. | `*.yar` (ex.: `airbnb_binaryalert.yar`) |
| **3** | **Hash Check** | Calcula e procura *hashes* criptográficos de software malicioso conhecido (**MD5, SHA1, SHA256** — ver [[Preservação do Sistema e Integridade de Dados]]) nos ficheiros do sistema. | `hash-iocs.txt`, `otx-hash-iocs.txt` |
| **4** | **C2 Back Connect Check** | Inspeciona as conexões de rede ativas dos processos e compara os **pontos de extremidade (*endpoints*: IPs/domínios)** com IOCs conhecidos de servidores **Command & Control (C2)**. | `c2-iocs.txt` |

---

## 3. Ficheiro de Configuração do LOKI (YAML)

No Slide 29 é apresentada a estrutura do ficheiro de configuração do LOKI, dividida em três secções (`rules`, `targets` e `verbosity`):

```yaml
# Loki Configuration File

rules:
# Specify the paths to YARA rules files
  yara_rules:
    - /path/to/yara/rules/file1.yar
    - /path/to/yara/rules/file2.yar

# Specify the paths to directories or files to scan
targets:
  files:
    - /path/to/scan/directory1
    - /path/to/scan/directory2
  processes: true

# Specify the verbosity level of the output (info, error, debug)
verbosity: info
```

---

## 4. Execução da Versão Python (`loki.py` / `loki.exe`), `PE-Sieve` e `LOKI UPGRADER`

* **Privilégios de Administrador**: o LOKI deve ser executado numa consola com privilégios de **Administrador** (`"loki" (administrador)`) para ter permissão de inspecionar a memória de todos os processos do sistema e pastas protegidas.
* **Fluxo de Arranque e Atualização Automática (Slide 30 — `Loki Scan VERSION: 0.51.0`, Python 3 release)**:
  1. **Integração com `PE-Sieve`**: no arranque, o LOKI inicializa o binário auxiliar **`pe-sieve64.exe`** (`tools\pe-sieve64.exe`, de *hasherezade* — [repositório oficial do PE-Sieve](https://github.com/hasherezade/pe-sieve)), utilizado para detetar injeção de código, *process hollowing* e DLLs maliciosas em memória;
  2. **Descarregamento automático de regras (`LOKI UPGRADER`)**: se a subdiretoria `signature-base` não existir ou estiver vazia (ou quando invocado com `--update`), o LOKI lança o processo `LOKI UPGRADER`, que descarrega o [arquivo `signature-base` no GitHub](https://github.com/Neo23x0/signature-base/archive/master.zip) e extrai os **7 conjuntos de ficheiros de assinaturas**:
     1. `c2-iocs.txt`
     2. `filename-iocs.txt`
     3. `hash-iocs.txt`
     4. `otx-hash-iocs.txt`
     5. `keywords.txt`
     6. `file-type-signatures.txt`
     7. Regras YARA (`*.yar`)

---

## 5. Sinopse e Parâmetros CLI do `loki.py` (Slide 28)

```text
usage: loki.py [-h] [-p path] [-s kilobyte] [-l log-file] [-r remote-loghost]
               [-t remote-syslog-port] [-a alert-level] [-w warning-level]
               [-n notice-level] [--allhds] [--alldrives] [--printall]
               [--allreasons] [--noprocscan] [--nofilescan] [--vulnchecks]
               [--nolevcheck] [--scriptanalysis] [--rootkit] [--noindicator]
               [--dontwait] [--intense] [--csv] [--onlyrelevant] [--nolog]
               [--update] [--debug] [--maxworkingset MAXWORKINGSET]
               [--syslogtcp] [--logfolder log-folder] [--nopesieve]
               [--pesieveshellc] [--nolisten]
               [--excludeprocess EXCLUDEPROCESS] [--force]
```

### A. Alvo & Limites

| Parâmetro (`loki.py`) | Função Técnica |
| :--- | :--- |
| **`-p path`** | Caminho inicial (diretoria) a analisar. |
| **`-s kilobyte`** | Tamanho máximo de ficheiro a verificar em KB (padrão = **`5000` KB** $\approx 5\text{ MB}$). |
| **`--allhds` / `--alldrives`** | Analisa todos os discos rígidos locais (`--allhds`) ou todas as unidades montadas (`--alldrives`). |
| **`--intense`** | Modo intensivo: analisa todos os ficheiros mesmo com extensões ou assinaturas não habituais. |
| **`--excludeprocess EXCLUDEPROCESS`** | Exclui um processo específico da análise de memória. |

### B. Controlo de Módulos & Memória

| Parâmetro (`loki.py`) | Função Técnica |
| :--- | :--- |
| **`--noprocscan` / `--nofilescan`** | Desativa a análise de processos em memória (`--noprocscan`) ou a análise do sistema de ficheiros (`--nofilescan`). |
| **`--vulnchecks` / `--rootkit` / `--scriptanalysis`** | Ativa verificações adicionais de vulnerabilidades, *rootkits* e análise heurística de scripts. |
| **`--nopesieve` / `--pesieveshellc`** | Desativa o uso do `pe-sieve` nos processos (`--nopesieve`) ou ativa a deteção adicional de *shellcode* no `pe-sieve` (`--pesieveshellc`). |
| **`--update`** | Atualiza a base de assinaturas `signature-base` a partir do GitHub. |

### C. Logs & Syslog

| Parâmetro (`loki.py`) | Função Técnica |
| :--- | :--- |
| **`-l log-file` / `--logfolder log-folder`** | Ficheiro ou pasta onde gravar o registo de execução (`.log`). |
| **`-r remote-loghost` / `-t port` / `--syslogtcp`** | Servidor e porta remotos para envio de eventos via Syslog (`--syslogtcp` força transporte TCP). |
| **`-a` / `-w` / `-n`** | Limiares de pontuação (*score*) para classificar alertas como `alert-level`, `warning-level` ou `notice-level`. |

---

## 6. Implicações Forenses

* **Correlação Disco + Memória + Rede num Único Varrimento**: enquanto ferramentas isoladas exigem correr um utilitário de hashes, outro de YARA e outro de conexões de rede (`netstat`), o LOKI cruza os 4 vetores numa única passagem. Mesmo que um atacante elimine o executável do disco após o lançar (*fileless / memory-only persistence*), o **Método 2 (Yara Rule Check em memória + PE-Sieve)** e o **Método 4 (C2 Back Connect Check)** detetam o processo comprometido em execução.

---

## Além da aula

* **Comparação entre a Hash Check do LOKI e a Base NSRL de [[00 AFD1|AFD1]]**: na nota [[Pesquisa de Evidências e Reconstrução de Eventos]] (Capítulo 1 de AFD1), estudou-se o uso de bases de *hashes* como a **NSRL (NIST)** para identificar ficheiros conhecidos (*known good* para redução de ruído, ou *known bad*). O **Método 3 (Hash Check)** do LOKI (`hash-iocs.txt` e `otx-hash-iocs.txt` da AlienVault OTX) implementa exatamente uma pesquisa *known bad* automatizada sobre os resumos [[Preservação do Sistema e Integridade de Dados|MD5, SHA-1 e SHA-256]] de cada ficheiro varrido.

---

## Perguntas de revisão

1. **Quem é o autor do scanner LOKI e que tipos de alvos no sistema operativo é capaz de inspecionar?**

> [!success]- Ver Resposta
> O autor é **Florian Roth (`@cyb3rops`)**, da Nextron Systems. O LOKI analisa tanto **ficheiros no sistema de ficheiros em disco** como **processos em execução na memória RAM** (além das ligações de rede ativas desses processos).

2. **Quais são os 4 métodos de deteção empregues pelo LOKI e a que ficheiros da `signature-base` correspondem?**

> [!success]- Ver Resposta
> (1) **File Name IOC** — aplica regex a nomes de ficheiros e caminhos completos (`filename-iocs.txt`); (2) **Yara Rule Check** — aplica regras YARA a ficheiros em disco e memória de processos (`*.yar`); (3) **Hash Check** — compara resumos MD5, SHA-1 e SHA-256 com *hashes* maliciosos conhecidos (`hash-iocs.txt`, `otx-hash-iocs.txt`); e (4) **C2 Back Connect Check** — compara *endpoints* (IPs/domínios) de ligações de rede ativas com servidores C2 conhecidos (`c2-iocs.txt`).

3. **Que secções compõem o ficheiro de configuração YAML do LOKI e qual o papel de cada uma?**

> [!success]- Ver Resposta
> Compõe-se de três secções: **`rules`** (caminhos para os ficheiros `.yar` em `yara_rules`), **`targets`** (lista de pastas/ficheiros a varrer em `files` e booleano `processes: true` para memória) e **`verbosity`** (nível de detalhe do output: `info`, `error` ou `debug`).

4. **O que ocorre no arranque se a pasta `signature-base` estiver vazia e qual o papel do binário `pe-sieve64.exe`?**

> [!success]- Ver Resposta
> Se `signature-base` não existir ou estiver vazia (ou com `--update`), o LOKI lança o **`LOKI UPGRADER`**, que descarrega o arquivo `master.zip` do repositório `Neo23x0/signature-base` e extrai os 7 conjuntos de assinaturas (`c2-iocs.txt`, `filename-iocs.txt`, `hash-iocs.txt`, `otx-hash-iocs.txt`, `keywords.txt`, `file-type-signatures.txt` e `*.yar`). No arranque, inicializa também **`pe-sieve64.exe`** (`tools\pe-sieve64.exe`) para detetar injeção de código, *process hollowing* e DLLs maliciosas em memória.

5. **Porque deve o LOKI ser corrido como Administrador e o que controla a flag `-s`?**

> [!success]- Ver Resposta
> Deve correr com privilégios de **Administrador** para obter permissão de leitura sobre a memória de todos os processos e diretorias protegidas do sistema. A flag **`-s kilobyte`** define o tamanho máximo dos ficheiros a analisar (por omissão **`5000` KB** $\approx 5\text{ MB}$).

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[YARA-X (Reimplementação em Rust) e Ferramenta CLI yr]] | `mesmo bloco` |
| **Seguinte** | [[Loki-RS (Versão Rust) - Compilação, Atualização e Parâmetros CLI]] | `mesmo bloco` |
| **Índice** | [[Capítulo 3 - YARA - MOTW - Strings]] · [[00 ASSI]] | `Bloco 01` |

### Conceitos Relacionados

* [[YARA - Introdução, Estrutura de Regras, Metadados e Condições]] · `mesmo bloco`
* [[Execução e Compilação no YARA (yara e yarac), Casos Reais (UPX, WannaCry) e LLMs]] · `mesmo bloco`
* [[Preservação do Sistema e Integridade de Dados]] · `AFD1 · Cap. 1`
* [[Pesquisa de Evidências e Reconstrução de Eventos]] · `AFD1 · Cap. 1`
