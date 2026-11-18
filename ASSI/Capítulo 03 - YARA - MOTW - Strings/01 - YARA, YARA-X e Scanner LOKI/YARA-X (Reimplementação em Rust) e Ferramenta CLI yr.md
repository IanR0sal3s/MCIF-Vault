---
title: YARA-X (Reimplementação em Rust) e Ferramenta CLI yr
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
  - yara
  - yara-x
  - rust
  - yr
  - virustotal
aliases:
  - YARA-X
  - yr
  - Ferramenta CLI yr
  - YARA Clássico vs YARA-X
atualizado: 2026-11-11
---

# YARA-X (Reimplementação em Rust) e Ferramenta CLI `yr`

O **YARA-X** é a reimplementação oficial do YARA em Rust desenvolvida pela VirusTotal para substituir o motor clássico em C, oferecendo maior desempenho, segurança de memória e a ferramenta CLI unificada `yr`.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema / Deteção)**: O motor clássico em C sofria de riscos de corrupção de memória durante o *parsing* de binários malformados, lentidão em expressões regulares complexas e erros de compilação pouco descritivos; o Rust elimina essa classe de vulnerabilidades e acelera a análise.
> * **Porque importa (Forense / IR)**: Usado diariamente em produção pela VirusTotal, o `yr` produz saída estruturada JSON (`--output-format json`) pronta para pipelines SIEM e inspeciona metadados estruturais de ficheiros (`yr dump`) para construir regras de alta precisão.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **CLI unificada (`yr`)**: substitui os dois binários separados do YARA clássico (`yara` e `yarac`) por um único executável com subcomandos (`yr scan`, `yr compile`, `yr fmt`, `yr dump`, `yr deps`, `yr fix`).
>   * **`yr dump` vs. `yr deps`**: `yr dump` extrai os dados dos módulos internos (`pe`, `elf`, `dotnet`) de um ficheiro alvo; `yr deps` exibe as dependências de módulos declaradas nas regras.
>   * **Bindings suportados**: APIs nativas para **Python, Go, C/C++ e JavaScript/TypeScript**.

---

## 1. Objetivos e Arquitetura do YARA-X

O [projeto oficial do YARA-X](https://virustotal.github.io/yara-x/) constitui a reimplementação oficial do [[YARA - Introdução, Estrutura de Regras, Metadados e Condições|YARA]] em **Rust**, desenvolvida pela **VirusTotal** após o motor clássico em C ter entrado em *maintenance mode* em 2025.

* **Objetivos centrais do YARA-X face ao YARA clássico**:
  1. **Melhor desempenho**: execução mais rápida e otimizada, especialmente em expressões regulares complexas sobre ficheiros de grandes dimensões;
  2. **Mais segurança de memória**: ao ser escrito em **Rust**, garante proteção nativa contra vulnerabilidades de corrupção de memória (*buffer overflows*, *use-after-free*) durante o *parsing* de ficheiros binários maliciosos;
  3. **Mais usabilidade**: melhores ferramentas de diagnóstico, formatação automática de código e mensagens de erro detalhadas.
* **Adoção em Produção e Ecossistema**:
  * É **empregue diariamente pela VirusTotal** nos seus sistemas de produção para detetar conteúdo malicioso em ficheiros submetidos globalmente;
  * Disponibiliza **suporte nativo (APIs/bindings)** para várias linguagens de programação: **Python, Go, C/C++ e JavaScript/TypeScript**.

---

## 2. Comparação: YARA Clássico (v4.x) vs. YARA-X (`yara` vs. `yr`)

| Funcionalidade | YARA Clássico (v4.x) | YARA-X |
| :--- | :--- | :--- |
| **Linguagem Base** | Linguagem **C** (gestão manual de memória) | **Rust** (segurança de memória) |
| **Interface CLI** | Comando **`yara`** (e `yarac` separado) | Comando **`yr`** com formatador nativo |
| **Desempenho Regex** | Lento em expressões complexas | **Otimizado** (sub-segundo em grandes ficheiros) |
| **Mensagens de Erro** | Erros genéricos de compilação | **Apontadores exatos de linha, coluna e sugestões** |
| **Estado do Projeto** | ***Maintenance mode*** (desde 2025) | **Desenvolvimento ativo e foco principal** |

---

## 3. A Ferramenta de Linha de Comandos `yr`

No YARA-X, todas as operações de varrimento, compilação, inspeção de módulos e formatação de regras são unificadas no executável **`yr`**:

```text
Usage: yr [COMMAND]
```

### Principais Comandos Destacados na Aula (Slide 24)

**1. `yr scan`** — análise de amostras com suporte nativo a exportação em **JSON**:

```bash
yr scan --output-format json regras.yar amostras/
```

**2. `yr fmt`** — formatador automático para padronizar a indentação e o estilo do código das regras:

```bash
yr fmt regras_malware.yar
```

**3. `yr compile`** — compilação prévia de conjuntos de regras para formato binário reutilizável.

### Tabela Completa de Subcomandos e Opções do `yr help` (Slide 25)

| Comando / Opção | Função Técnica (`yr help`) |
| :--- | :--- |
| **`scan`** | Analisa um ficheiro ou diretoria face às regras especificadas. |
| **`compile`** | Compila regras YARA para formato binário reutilizável. |
| **`dump`** | Mostra os dados extraídos pelos módulos internos do YARA (ex.: `pe`, `elf`, `dotnet`) para um ficheiro. |
| **`deps`** | Mostra as dependências de módulos exigidas pelas regras. |
| **`fmt`** | Formata automaticamente ficheiros de código-fonte YARA. |
| **`fix`** | Utilitários para corrigir problemas e incompatibilidades em código-fonte de regras YARA. |
| **`completion`** | Gera o código de preenchimento automático (*shell completion*) para a shell especificada. |
| **`help`** | Imprime a mensagem de ajuda geral ou a ajuda do subcomando indicado. |
| **`-h, --help`** | Apresenta a ajuda da linha de comandos. |
| **`-V, --version`** | Mostra a versão instalada do `yr`. |

---

## 4. Implicações Forenses

* **Inspeção Estrutural com `yr dump`**: quando um analista forense pretende escrever uma regra YARA baseada em atributos específicos do cabeçalho de um executável Windows (módulo `pe`, como *timestamps* de compilação, secções, *imports* ou certificados Authenticode), o subcomando `yr dump amostra.exe` despeja toda a árvore de propriedades extraída pelos módulos do YARA-X, permitindo copiar diretamente os campos e valores para a secção `condition:`.
* **Integração Direta com SIEM/Pipelines Forenses (`--output-format json`)**: ao contrário do `yara` clássico (cuja saída em texto plano exigia *parsing* externo), o `yr scan --output-format json` produz saída estruturada pronta a ingerir em ferramentas de análise ou bases de dados de resposta a incidentes.

---

## Além da aula

* **Convergência Tecnológica para Rust (YARA-X e Loki-RS)**: tal como a VirusTotal reescreveu o YARA em Rust dando origem ao **YARA-X**, também Florian Roth reescreveu o scanner LOKI em Rust dando origem ao **[[Loki-RS (Versão Rust) - Compilação, Atualização e Parâmetros CLI|Loki-RS]]**, que utiliza internamente o ecossistema Rust para avaliar regras YARA com máxima performance e segurança de memória.

---

## Perguntas de revisão

1. **Quais são os três principais objetivos do YARA-X face ao YARA clássico e que linguagens possuem suporte de APIs/bindings?**

> [!success]- Ver Resposta
> Os três objetivos são: (1) **melhor desempenho** (especialmente em expressões regulares complexas sobre ficheiros grandes); (2) **mais segurança de memória** (proteção nativa do Rust contra *buffer overflows* e *use-after-free*); e (3) **mais usabilidade** (formatação automática e diagnóstico preciso de erros). Possui APIs/bindings para **Python, Go, C/C++ e JavaScript/TypeScript**.

2. **Compare o YARA Clássico (v4.x) e o YARA-X quanto à linguagem base, interface CLI, desempenho em regex, mensagens de erro e estado atual do projeto.**

> [!success]- Ver Resposta
> O **YARA Clássico (v4.x)** é escrito em **C**, utiliza os binários separados `yara` e `yarac`, é lento em expressões regulares complexas, apresenta erros genéricos de compilação e está em ***maintenance mode* desde 2025**. O **YARA-X** é escrito em **Rust**, unifica as operações na CLI **`yr`** (com formatador nativo), oferece execução **sub-segundo em regex**, apresenta apontadores exatos de linha/coluna com sugestões e encontra-se em **desenvolvimento ativo** (usado em produção pela VirusTotal).

3. **Distinga a finalidade dos subcomandos `yr scan`, `yr fmt`, `yr compile`, `yr dump`, `yr deps` e `yr fix`.**

> [!success]- Ver Resposta
> **`yr scan`** analisa ficheiros ou diretorias (suportando `--output-format json`); **`yr fmt`** formata automaticamente o estilo das regras; **`yr compile`** compila regras para formato binário; **`yr dump`** exibe os dados extraídos pelos módulos (`pe`, `elf`, `dotnet`) sobre um ficheiro; **`yr deps`** lista as dependências de módulos das regras; e **`yr fix`** fornece utilitários para corrigir código-fonte de regras.

4. **Como ajudam `yr dump` e `yr scan --output-format json` num fluxo real de resposta a incidentes?**

> [!success]- Ver Resposta
> O **`yr dump`** despeja todos os atributos estruturais extraídos pelos módulos do YARA-X sobre uma amostra suspeita (como *timestamps*, secções e *imports* PE), facilitando a redação exata da secção `condition:`. Já o **`yr scan --output-format json`** gera resultados estruturados diretamente ingeríveis por SIEMs e pipelines de triagem sem necessidade de *parsing* artesanal de texto.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Execução e Compilação no YARA (yara e yarac), Casos Reais (UPX, WannaCry) e LLMs]] | `mesmo bloco` |
| **Seguinte** | [[Scanner de IOCs LOKI (Versão Python) - Métodos de Deteção e Configuração]] | `mesmo bloco` |
| **Índice** | [[Capítulo 3 - YARA - MOTW - Strings]] · [[00 ASSI]] | `Bloco 01` |

### Conceitos Relacionados

* [[YARA - Introdução, Estrutura de Regras, Metadados e Condições]] · `mesmo bloco`
* [[YARA - Tipos de Strings, Modificadores, Formato Hexadecimal, Base64 e Regex]] · `mesmo bloco`
* [[Loki-RS (Versão Rust) - Compilação, Atualização e Parâmetros CLI]] · `mesmo bloco`
