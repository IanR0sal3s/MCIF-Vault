---
title: Ferramentas de Análise e Extração do Registry
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 5
tipo: procedimento
tags:
  - assi
  - windows
  - registry
  - ferramentas
  - forense
  - zimmerman
  - nirsoft
aliases:
  - Registry Tools
  - reg query
  - reg export
  - RegistryExplorer
  - RegRipper
  - RegScanner
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
fontes:
  - "https://technet.microsoft.com/en-us/library/cc742028.aspx"
  - "https://technet.microsoft.com/en-us/library/cc742017.aspx"
  - "http://www.nirsoft.net/utils/regscanner.html"
  - "https://ericzimmerman.github.io/#!index.md"
  - "https://github.com/keydet89/RegRipper4.0"
atualizado: 2026-09-23
---

# Ferramentas de Análise e Extração do Registry

Instrumentos nativos (`reg.exe`, `regedit.exe`) e ferramentas periciais especializadas (`RegScanner`, `RegistryExplorer`, `RegRipper`) para interrogação *live* e análise *offline* de hives do Registry.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: O Windows disponibiliza utilitários nativos (`reg.exe` em consola e `regedit.exe` em GUI) desenhados para administração quotidiana e manutenção do sistema ativo, mas que não expõem metadados forenses nem descodificam estruturas binárias complexas.
> * **Porque importa (Forense)**: Em investigação digital é imperativo analisar ficheiros de hive extraídos (*offline*) sem alterar o carimbo temporal (*LastWriteTime*) das chaves, filtrar chaves por intervalos temporais do incidente e automatizar a descodificação de *blobs* binários, cifras ROT13 e ficheiros de transação (`.LOG1`/`.LOG2`).
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Limitações Críticas do `regedit.exe`**: Não permite filtrar pesquisas por data de modificação (*LastWriteTime*), realiza pesquisas sequenciais lentas e, se usado para editar/carregar hives sem precaução num sistema vivo, altera marcas temporais.
>   * **Escolha da Ferramenta Certa**: `RegScanner` destaca-se na filtragem por intervalo de datas em sistema vivo; `RegistryExplorer` na inspeção visual *offline* com descodificação automática e *replay* de logs; `RegRipper` (`rip.exe`) na extração automatizada em linha de comandos via plugins.

---

## Comparação de Ferramentas de Análise do Registry

| Ferramenta | Autor / Origem | Modo de Operação | Filtro por *LastWriteTime* | Principais Vantagens e Casos de Uso Pericial |
| :--- | :--- | :---: | :---: | :--- |
| **`reg.exe`** | Microsoft (Nativo CLI) | *Live* (e carga manual) | Não | Triagem rápida por scripts (`reg query`, `reg export`) sem abrir GUI. |
| **`regedit.exe`** | Microsoft (Nativo GUI) | *Live* / *Load Hive* | Não | Navegação básica. Pesquisa sequencial lenta; não descodifica estruturas binárias. |
| **`RegScanner`** | NirSoft | *Live* (Principal) | **Sim** | Utilitário gráfico leve para pesquisas avançadas por tipo de valor, tamanho, Unicode/ASCII e **intervalo de datas de modificação de chaves**. |
| **`RegistryExplorer`** | Eric Zimmerman | *Offline* e *Live* (via VSS) | **Sim** | Referência em DFIR. Suporta *bookmarks*, *replay* de transações (`.LOG1`/`.LOG2`) e **descodificação transparente de campos binários e cifras (ex.: ROT13 em [[Artefacto Forense UserAssist\|UserAssist]])**. |
| **`RegRipper`** (`rip.exe`) | Harlan Carvey / Mark Woan | *Offline* (CLI / GUI) | **Sim** (via plugins) | Ferramenta em Perl orientada à extração rápida e direcionada de artefactos através de plugins ou perfis. Integrada nativamente no **Autopsy**. |

---

## Anatomia dos Comandos Nativos (`reg.exe`)

O executável nativo `reg.exe` permite interrogar e exportar ramos do Registry diretamente na linha de comandos.

### 1. `reg query` (Leitura e Pesquisa em Consola)
Lista chaves, subchaves e os respetivos valores de um caminho especificado:

```cmd
reg query HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\hivelist
```

* **Parâmetros fundamentais para exame**:
  * `/s`: executa a consulta de forma **recursiva** em todas as subchaves abaixo do caminho indicado.
  * `/v <Nome>`: filtra a saída para exibir apenas um **valor específico** dentro da chave.

### 2. `reg export` (Exportação Textual Estruturada)
Exporta uma chave, respetivas subchaves e valores para um ficheiro de texto estruturado compatível com o formato `Windows Registry Editor Version 5.00`:

```cmd
reg export HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\hivelist out.txt
```

* **Comportamento de saída**: O ficheiro resultante (`out.txt`) é gravado em codificação Unicode e representa valores de texto em claro, enquanto valores binários (`REG_BINARY`) ou multilinhas (`REG_MULTI_SZ`) são serializados em notação hexadecimal (ex.: `hex:` ou `hex(7):`).

---

## Anatomia do RegRipper na Linha de Comandos (`rip.exe`)

O executável de linha de comandos do **RegRipper** (`rip.exe`) processa ficheiros de hive brutos extraídos de uma imagem forense, aplicando plugins individuais ou perfis completos de auditoria:

```bash
# 1. Listar todos os plugins disponíveis na instalação
./rip.exe -l

# 2. Extrair artefactos de execução do utilizador a partir de um NTUSER.DAT offline
./rip.exe -r NTUSER.DAT -p userassist

# 3. Executar o perfil completo de auditoria sobre um hive SYSTEM
./rip.exe -r SYSTEM -f system
```

### Explicação dos Parâmetros do `rip.exe`

* **`-l`**: (*list*) lista no ecrã todos os plugins instalados, a versão, o hive a que se destinam e uma breve descrição.
* **`-r <Ficheiro_Hive>`**: (*registry hive*) especifica o caminho para o ficheiro físico de hive a analisar (ex.: `NTUSER.DAT`, `SYSTEM`, `SOFTWARE`, `SAM`, `USRCLASS.DAT`).
* **`-p <Nome_Plugin>`**: (*plugin*) executa apenas um plugin específico sobre o hive indicado (ex.: `-p userassist`, `-p runmru`, `-p typedpaths`, `-p compname`).
* **`-f <Perfil>`**: (*profile file*) executa sequencialmente uma lista pré-definida de plugins adequados àquele tipo de hive (ex.: `-f system`, `-f software`, `-f ntuser`, `-f sam`).

---

## Implicações Forenses

1. **Integridade da Prova (*Live* vs. *Offline*)**:
   * A manipulação descuidada do Registry num sistema vivo através do `regedit.exe` atualiza o *LastWriteTime* de qualquer chave modificada e gera registos voláteis indesejados.
   * Em perícia digital, prioriza-se a extração dos ficheiros brutos do hive (juntamente com os ficheiros de log transacional `.LOG1` e `.LOG2`, ou leitura direta via *Volume Shadow Copies*) e a posterior análise *offline* com `RegistryExplorer` ou `RegRipper`.
2. **Automação e Normalização Temporal**:
   * Ferramentas periciais como o `RegRipper` e o `RegistryExplorer` automatizam a correlação pericial, convertendo timestamps binários (`FILETIME64` e `SYSTEMTIME`) diretamente para formato legível em **UTC** e traduzindo chaves crípticas em relatórios estruturados.

---

## Perguntas de revisão

1. **Quais são as três principais limitações do utilitário nativo `regedit.exe` quando comparado com o `RegScanner` e o `RegistryExplorer` numa investigação forense?**

> [!success]- Ver Resposta
> (1) O `regedit.exe` não permite pesquisar nem filtrar chaves pelo seu carimbo temporal de última modificação (*LastWriteTime*); (2) a sua pesquisa textual é sequencial e muito lenta; e (3) não descodifica automaticamente estruturas binárias complexas, timestamps `FILETIME64`/`SYSTEMTIME` nem ofuscações como o ROT13 do `UserAssist`.

2. **Qual a diferença entre os parâmetros `-p` e `-f` na execução do comando `rip.exe` (RegRipper)?**

> [!success]- Ver Resposta
> O parâmetro `-p <plugin>` executa apenas um **único plugin** específico (ex.: `./rip.exe -r NTUSER.DAT -p userassist`), enquanto o parâmetro `-f <perfil>` executa um **perfil completo** contendo dezenas de plugins agrupados para um determinado hive (ex.: `./rip.exe -r SYSTEM -f system`). Em ambos os casos, `-r` especifica o ficheiro de hive bruto de entrada.

3. **Como é que um perito pode consultar recursivamente todos os valores de uma chave do Registry na linha de comandos nativa do Windows e como pode filtrar apenas um valor específico?**

> [!success]- Ver Resposta
> Utilizando o comando `reg query <Caminho_da_Chave> /s` para realizar uma busca recursiva em todas as subchaves, ou `reg query <Caminho_da_Chave> /v <Nome_do_Valor>` para filtrar apenas o valor pretendido.

4. **De que forma o `RegistryExplorer` consegue analisar hives bloqueados pelo sistema operativo numa máquina Windows em execução?**

> [!success]- Ver Resposta
> Quando executado com privilégios de Administrador num sistema vivo, o `RegistryExplorer` contorna o bloqueio exclusivo do Configuration Manager recorrendo ao serviço *Volume Shadow Copy* (VSS) ou leitura direta de baixo nível, permitindo abrir os hives ativos e aplicar o *replay* dos ficheiros de transação (`.LOG1` e `.LOG2`).

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Tipos de Dados e Associação de Ficheiros no Registry]] | `mesmo bloco` |
| **Seguinte** | [[Arquitetura 32 vs 64 bits no Registry e Executáveis (WOW6432Node)]] | `mesmo bloco` |
| **Índice** | [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]] · [[00 ASSI]] | `Bloco 05` |

### Conceitos Relacionados

* [[Estrutura e Hives do Windows Registry]] · `mesmo bloco`
* [[Artefacto Forense UserAssist]] · `Bloco 07`
* [[Artefactos Forenses de Execução e Persistência no Registry]] · `Bloco 07`
* [[Ferramentas de Triagem Forense no Windows Registry (RegistryReport, ForensicUserInfo e WRR)]] · `AFD1 · Cap. 2`
* [[Dispositivos de Arranque Forense - Disquetes DOS, Live CDs Linux, WinFE e USB]] · `AFD1 · Cap. 2`
* [[Investigação Forense Digital - Análise Live vs Post-Mortem]] · `AFD1 · Cap. 1`
