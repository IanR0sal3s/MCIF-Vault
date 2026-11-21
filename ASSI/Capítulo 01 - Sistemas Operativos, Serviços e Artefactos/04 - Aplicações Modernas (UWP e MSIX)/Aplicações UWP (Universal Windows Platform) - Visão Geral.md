---
title: Aplicações UWP (Universal Windows Platform) - Visão Geral
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 4
tipo: conceito
tags:
  - assi
  - windows
  - uwp
  - appx
aliases:
  - UWP
  - Universal Windows Platform
  - Metro Apps
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v4.pdf
atualizado: 2026-11-21
---

# Aplicações UWP (Universal Windows Platform)

A **Universal Windows Platform (UWP)** — sucessora das *Metro Apps* (W8) e *Modern Apps* — é a plataforma de aplicações modernas da Microsoft (desde o W10), distribuída via Microsoft Store no formato **APPX** para múltiplos dispositivos Windows (PC, tablet, Xbox; ex.: Windows Terminal, WhatsApp, Messenger).

## 1. Isolamento em *Sandbox*

As aplicações UWP correm numa ***sandbox*** para proteção da app e do sistema operativo:
* **Sem acesso direto ao Registry**: apenas via ***Brokered Windows Runtime Component (BWC)***;
* **Sistema de ficheiros restrito**: sem acesso fora da pasta da própria aplicação;
* **API obrigatória**: forçadas a usar **Windows Runtime (`WinRT`)**;
* **Permissões explícitas**: devem declarar recursos sensíveis (microfone, câmara, etc.); integram com notificações, *live tiles* (W10) e Windows Timeline.

---

## 2. Auditoria CLI e Diretórios de Instalação

```cmd
:: Listar processos de apps UWP ativos / contar nº de APPX em execução
tasklist /APPS
tasklist /apps | find /c "."
```

```powershell
# Listar aplicações UWP instaladas (live box)
Get-AppxPackage | Select Name, PackageFullName | Format-Table -AutoSize
Get-AppxPackage -AllUsers | Export-Csv -Path appx_all.csv
```

| Diretório | Conteúdo e Permissões |
| :--- | :--- |
| **`C:\Windows\SystemApps`** | Aplicações UWP integradas no sistema operativo. |
| **`C:\Program Files\WindowsApps`** | Aplicações instaladas via Store — **sem acesso direto mesmo para Administrador**; proprietário (*owner*) é a conta interna **`TrustedInstaller`** (serviço *Windows Module Installer*). |

Para os artefactos forenses deixados por estas aplicações, ver [[UWP - Artefactos Forenses e Estrutura de Dados]].

---

## Perguntas de revisão

1. **Que quatro restrições principais impõe a *sandbox* às aplicações UWP?**

> [!success]- Ver Resposta
> Sem acesso direto ao Registry (mediado por **BWC**), sem acesso ao sistema de ficheiros fora da sua pasta, uso obrigatório da API **WinRT** e declaração explícita de recursos (microfone, câmara, etc.).

2. **Qual a diferença entre `C:\Windows\SystemApps` e `C:\Program Files\WindowsApps`, e quem é o proprietário desta última?**

> [!success]- Ver Resposta
> `SystemApps` contém apps de sistema; `WindowsApps` contém apps instaladas via Store e pertence à conta interna **`TrustedInstaller`** (serviço *Windows Module Installer*), bloqueando o acesso direto mesmo a Administradores.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Ficha Prática e Questionário - Serviços e Windows Search]] | `Bloco 03` |
| **Seguinte** | [[UWP - Artefactos Forenses e Estrutura de Dados]] | `mesmo bloco` |
| **Índice** | [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]] · [[00 ASSI]] | `Bloco 04` |

### Conceitos Relacionados

* [[Processos e linha de comandos no Windows]] · `Bloco 02`
* [[Registry em Aplicações Modernas (MSIX e Helium)]] · `Bloco 06`
