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
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v4.pdf
fontes:
  - "https://technet.microsoft.com/en-us/library/cc742028.aspx"
  - "http://www.nirsoft.net/utils/regscanner.html"
  - "https://ericzimmerman.github.io/#!index.md"
  - "https://github.com/keydet89/RegRipper4.0"
atualizado: 2026-11-21
---

# Ferramentas de Análise e Extração do Registry

O Windows inclui ferramentas nativas (`reg.exe`, `regedit.exe`) úteis para administração *live*, mas a análise forense exige utilitários especializados (`RegScanner`, `RegistryExplorer`, `RegRipper`) capazes de analisar hives *offline* sem alterar timestamps e descodificar estruturas binárias automaticamente.

## 1. Comparativo das Ferramentas

| Ferramenta | Origem | Modo | Filtro por Data (*LastWriteTime*) | Ponto Forte |
| :--- | :--- | :---: | :---: | :--- |
| **`reg.exe`** | Nativo (CLI) | *Live* | Não | Triagem rápida por scripts (`reg query`, `reg export`). |
| **`regedit.exe`** | Nativo (GUI) | *Live* | Não | Navegação básica; pesquisa sequencial lenta e sem descodificação binária. |
| **`RegScanner`** | NirSoft (GUI) | *Live* | **Sim** | Pesquisa avançada muito mais rápida que o `regedit`, com filtro por intervalo de datas e tipo de dados. |
| **`RegistryExplorer`** | Eric Zimmerman | *Offline* e *Live* (Admin/VSS) | **Sim** | Referência DFIR: *bookmarks*, *replay* de `.LOG1`/`.LOG2` e descodificação automática (ex.: ROT13 em [[Artefacto Forense UserAssist\|UserAssist]]). |
| **`RegRipper` (`rip.exe`)** | Open-source (Perl) | *Offline* (CLI/GUI) | **Sim** (plugins) | Extração automatizada via plugins Perl; usado internamente pelo **Autopsy** (GUI sofrível, ideal em CLI). |

---

## 2. Comandos Essenciais

### Utilitário Nativo `reg.exe`
```cmd
:: Ler valores de uma chave (/s = recursivo; /v <Nome> = valor específico)
reg query HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\hivelist

:: Exportar chave em formato texto (Windows Registry Editor Version 5.00)
reg export HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\hivelist out.txt
```

### `RegRipper` (`rip.exe` — Análise Offline)
```bash
./rip.exe -l                                # Listar todos os plugins disponíveis
./rip.exe -r NTUSER.DAT -p userassist       # Executar 1 plugin específico (-p) sobre um hive (-r)
./rip.exe -r SYSTEM -f system               # Executar um perfil completo de plugins (-f)
```

> [!IMPORTANT] Integridade Forense
> Usar o `regedit.exe` para editar chaves num sistema vivo altera o *LastWriteTime* e contamina a evidência. Em perícia digital, extraem-se os ficheiros de hive (com `.LOG1`/`.LOG2`) para análise *offline* em `RegistryExplorer` ou `RegRipper`.

---

## Perguntas de revisão

1. **Quais as principais limitações do `regedit.exe` face ao `RegScanner` e ao `RegistryExplorer`?**

> [!success]- Ver Resposta
> O `regedit.exe` tem pesquisa sequencial limitada (não filtra por data de modificação *LastWriteTime*) e não descodifica automaticamente estruturas binárias, timestamps `FILETIME64` ou cifras como o ROT13.

2. **No `RegRipper` (`rip.exe`), qual a diferença entre `-l`, `-p` e `-f`?**

> [!success]- Ver Resposta
> `-l` lista os plugins disponíveis; `-p <plugin>` corre um único plugin sobre o hive indicado por `-r`; `-f <perfil>` corre um conjunto completo de plugins para esse tipo de hive (ex.: `system`, `ntuser`).

3. **Como consegue o `RegistryExplorer` abrir hives bloqueados pelo Windows numa máquina *live*?**

> [!success]- Ver Resposta
> Em modo Administrador, acede aos hives bloqueados através de leitura de baixo nível / *Volume Shadow Copy* (VSS), aplicando também o *replay* dos logs transacionais (`.LOG1`/`.LOG2`).

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
