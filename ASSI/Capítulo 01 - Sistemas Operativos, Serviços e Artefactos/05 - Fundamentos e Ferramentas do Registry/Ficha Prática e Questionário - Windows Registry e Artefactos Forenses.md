---
title: Ficha Prática e Questionário - Windows Registry e Artefactos Forenses
tipo: exercicio
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 5
fonte_aula: 02---ficha_laboratorial_v1_Nirsoft_et_al---ULO.pdf
tags:
  - assi
  - windows
  - registry
  - nirsoft
  - uwp
  - usbstor
  - lab
aliases:
  - Ficha Prática 02
  - Lab 2 Windows Registry
  - Laboratório 2 ASSI
atualizado: 2026-11-21
---

# Guia do Laboratório 2 — NirSoft, UWP e Windows Registry

**Porque importa este laboratório**: instala o pacote completo da **NirSoft** (`NirLauncher`), ensina a automatizar a recolha de tarefas agendadas e apps UWP para ficheiros estruturados (CSV/HTML/JSON), e introduz a extração direta de chaves forenses do **Registry** pela linha de comandos (`reg query` e `reg export`).

---

## 1. Suite NirSoft (`NirLauncher`)

* **Objetivo**: disponibilizar dezenas de utilitários leves de triagem *live* no `PATH` (é preciso incluir a subpasta `NirSoft` no `PATH`, usar a senha indicada no site para extrair o ZIP e, se necessário, criar exclusão no antivírus devido a falsos positivos).
* **Ferramentas exploradas**:
  * **`USBDeview`**: lista todos os dispositivos USB ligados ao sistema (atuais e históricos);
  * **`awatch.exe` (*Adapter Watch*)**: mostra interfaces de rede, endereços IP e tráfego;
  * **`currports.exe` (*CurrPorts*)**: lista portas TCP/UDP abertas e os processos associados (útil para detetar ligações suspeitas).

---

## 2. Automação de Relatórios com `TaskSchedulerView` (NirSoft)

* **Objetivo**: em vez de inspecionar tarefas agendadas manualmente na GUI, usar as flags CLI da NirSoft para gerar relatórios ordenados e auditáveis (prestando especial atenção à coluna **`Executable Arguments`** para detetar scripts ou parâmetros suspeitos):

```cmd
taskSchedulerView /scomma %TEMP%\a.csv
taskSchedulerView /shtml %TEMP%\a.html /sort ~1
taskSchedulerView /sjson %TEMP%\a.json /sort ~1
```
*(`/scomma`, `/shtml` e `/sjson` exportam para CSV, HTML e JSON; `/sort ~1` ordena inversamente pela 1.ª coluna.)*

---

## 3. Inventário de Aplicações UWP/APPX

* **Objetivo**: obter em PowerShell (lançado em modo Administrador via `Win + R` → `powershell` → `Ctrl + Shift + Enter`) a lista completa de pacotes modernos instalados para todos os utilizadores, pronta para filtrar em Excel:

```powershell
Get-AppxPackage -AllUsers | Export-Csv -Path c:\temp\appx.csv
```

---

## 4. Extração de Chaves Forenses do Registry (GUI e CLI)

* **Objetivo**: praticar as três formas nativas de extrair chaves forenses reais do sistema:
  1. **`regedit` (exportação gráfica)** sobre `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU` (comandos digitados em `Win + R`);
  2. **`reg query` (consulta direta na consola)** sobre `HKCU\software\Microsoft\Internet Explorer\TypedURLs`;
  3. **`reg export` (exportação para texto via CLI)** sobre `HKLM\SYSTEM\ControlSet001\Enum\USBSTOR` *(nota: numa VM recém-instalada onde nunca foram ligadas pens USB, esta chave só aparece após a primeira interação USB)*.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Arquitetura 32 vs 64 bits no Registry e Executáveis (WOW6432Node)]] | `mesmo bloco` |
| **Seguinte** | [[Registry em Aplicações Modernas (MSIX e Helium)]] | `muda para Bloco 06` |
| **Índice** | [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]] · [[00 ASSI]] | `Bloco 05` |
