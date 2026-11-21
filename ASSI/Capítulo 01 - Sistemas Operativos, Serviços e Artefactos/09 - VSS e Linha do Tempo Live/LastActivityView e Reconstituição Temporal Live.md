---
title: LastActivityView e Reconstituição Temporal Live
tipo: ferramenta
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 9
fonte_aula: 02_ArtefactosWindows---2026-27_ULO_v2.pdf
tags:
  - assi
  - windows
  - forense
  - nirsoft
  - timeline
  - triagem
aliases:
  - LastActivityView
  - Reconstituição Temporal Live com LastActivityView
  - NirSoft LastActivityView
atualizado: 2026-11-21
---

# `LastActivityView` e Reconstituição Temporal *Live*

O **`LastActivityView`** (NirSoft) é um utilitário de triagem rápida que recolhe dados de múltiplas fontes num sistema Windows ativo (*live*) para construir uma linha do tempo unificada de atividade do utilizador e do sistema.

## 1. Fontes Agregadas e Requisitos

* **Fontes recolhidas**: [[Serviço Prefetch e SysMain - Arquitetura e Funcionamento|Prefetch]], Registry (`UserAssist`, MRU, ShellBags), ficheiros *minidump* (crashes/BSOD) e eventos de sistema (ligar/desligar, execução de `.exe`, abertura de pastas).
* **Privilégios obrigatórios**: requer execução como **Administrador** para aceder a `%WINDIR%\Prefetch`, hives `HKLM` e minidumps.
* **Exportação CLI** (suporta TXT, CSV, HTML e XML):
  ```cmd
  lastactivityview.exe /stab c:\temp\info.csv
  ```
  *(O ficheiro gerado pode ser analisado diretamente em Excel ou LibreOffice Calc.)*

> [!WARNING] Limitações Periciais
> Por correr em sistema *live*, a própria execução do `lastactivityview.exe` altera o sistema (cria o seu próprio ficheiro `.pf` e chaves de Registry). Além disso, serve para triagem inicial e não substitui a análise profunda individual de artefactos como VSS, Prefetch ou AmCache.

---

## Perguntas de revisão

1. **Para que serve o `LastActivityView` e que privilégio exige para recolher todas as fontes?**

> [!success]- Ver Resposta
> Agrega múltiplas fontes de um sistema Windows *live* (`Prefetch`, `Registry`, `Minidumps`, eventos do SO) numa linha do tempo cronológica de atividade. Exige privilégios de **Administrador**.

2. **Qual a principal limitação forense de executar o `LastActivityView` diretamente numa máquina suspeita?**

> [!success]- Ver Resposta
> É invasivo em sistema *live* (gera artefactos da sua própria execução, como o seu `.pf`) e fornece apenas uma visão agregada de triagem, sem substituir a análise profunda dos artefactos individuais.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Artefactos Forenses de Dispositivos USB]] | `Bloco 08` |
| **Seguinte** | [[Volume Shadow Service (VSS) - Arquitetura e Funcionamento]] | `mesmo bloco` |
| **Índice** | [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]] · [[00 ASSI]] | `Bloco 09` |

### Conceitos Relacionados

* [[Gestão e Manipulação de VSS (CLI, PowerShell e Permissões)]] · `mesmo bloco`
* [[Serviço Prefetch e SysMain - Arquitetura e Funcionamento]] · `Bloco 10`
* [[Investigação Forense Digital - Análise Live vs Post-Mortem]] · `AFD1 · Cap. 1`
* [[Princípios e Rota do Manuseamento de Evidência Digital]] · `AFD1 · Cap. 1`
* [[Diretrizes de Manuseamento - Identificação, Preservação, Isolamento e Correlação]] · `AFD1 · Cap. 1`
