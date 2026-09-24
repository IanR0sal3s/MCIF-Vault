---
title: Ferramentas de Análise e Extração do Registry
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
tipo: procedimento
tags:
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

A investigação e administração do Windows Registry requer instrumentos capazes de atuar tanto em sistemas em execução (*live analysis*) como em ficheiros brutos de hive extraídos de imagens de disco (*offline analysis*).

## Utilitários Nativos de Linha de Comandos

O executável nativo `reg.exe` permite interrogar e manipular o Registry sem recurso à interface gráfica.

### 1. `reg query` (Leitura)
Permite listar chaves, subchaves e os respetivos valores.

```cmd
reg query HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\hivelist
```

* Parâmetro `/s`: consulta recursiva de todas as subchaves.
* Parâmetro `/v <Nome>`: filtra por um valor específico dentro da chave.

### 2. `reg export` (Exportação Textual)
Exporta uma chave e respetivas subchaves para um ficheiro de texto compatível com o formato do Registry Editor (`Windows Registry Editor Version 5.00`):

```cmd
reg export HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\hivelist out.txt
```

O ficheiro resultante preserva a codificação Unicode e apresenta os valores binários ou multilinhas sob formato hexadecimal (ex.: `hex:` ou `hex(7):`).

## Utilitários Gráficos Nativos

* **`regedit.exe`**: aplicação padrão do Windows para navegar, pesquisar e editar chaves.
  * *Limitações*: a funcionalidade de pesquisa é sequencial e lenta; não filtra por datas de última modificação de chave (*LastWriteTime*); exige carregar hives offline manualmente através de `Ficheiro -> Carregar Hive (Load Hive)`.

## Ferramentas Forenses Especializadas

Para ultrapassar as limitações nativas e analisar hives sem alterar marcas temporais, destacam-se três ferramentas fundamentais:

| Ferramenta | Autor / Origem | Características e Cenário de Uso |
| :--- | :--- | :--- |
| **RegScanner** | NirSoft | Utilitário gráfico leve para pesquisas avançadas no Registry ativo. Permite filtrar por tipo de valor, comprimento, texto/Unicode, e de forma crítica por **intervalo de datas de modificação** de chaves. |
| **RegistryExplorer** | Eric Zimmerman | Aplicação de referência em DFIR. Permite análise de hives em sistemas ativos (com privilégios de administrador via VSS) e análise *offline* de ficheiros copiados (`SYSTEM`, `SOFTWARE`, `NTUSER.DAT`, etc.). Inclui marcadores (*bookmarks*), plugins automáticos de interpretação e **descodificação transparente de campos binários e cifras (ex.: ROT13 em [[Artefacto Forense UserAssist|UserAssist]])**. |
| **RegRipper** | Harlan Carvey / Mark Woan | Ferramenta em Perl desenhada para extração rápida e direcionada de artefactos forenses através de plugins especializados. É amplamente empregue de forma automatizada por plataformas periciais como o **Autopsy**. |

### Utilização do RegRipper na Linha de Comandos

O executável de linha de comandos (`rip.exe`) recebe o ficheiro de hive bruto e o plugin (ou perfil) a executar:

```bash
# Listar todos os plugins disponíveis
./rip.exe -l

# Extrair artefactos de execução do utilizador a partir de um NTUSER.DAT offline
./rip.exe -r NTUSER.DAT -p userassist

# Executar perfil completo de auditoria a um hive SYSTEM
./rip.exe -r SYSTEM -f system
```

## Implicações Forenses

1. **Integridade da Prova (*Live* vs. *Offline*)**:
   * O uso do `regedit` num sistema vivo atualiza o *LastWriteTime* de qualquer chave modificada e cria registos voláteis indesejados.
   * Em perícia digital, prioriza-se a extração dos ficheiros brutos do hive (ou leitura direta de *shadow copies*) e a posterior análise offline com `RegistryExplorer` ou `RegRipper`.
2. **Plugins Forenses**:
   * Ferramentas como o `RegRipper` automatizam a correlação pericial, convertendo timestamps complexos em formato legível (UTC) e traduzindo chaves crípticas em relatos estruturados de atividade maliciosa.

## Notas relacionadas

- [[Estrutura e Hives do Windows Registry]]
- [[Artefacto Forense UserAssist]]
- [[Artefactos Forenses de Execução e Persistência no Registry]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
