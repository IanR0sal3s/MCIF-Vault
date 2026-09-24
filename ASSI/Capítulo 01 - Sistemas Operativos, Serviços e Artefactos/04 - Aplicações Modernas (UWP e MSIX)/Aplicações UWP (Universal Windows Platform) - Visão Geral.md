---
title: Aplicações UWP (Universal Windows Platform) - Visão Geral
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
tipo: conceito
tags:
  - windows
  - uwp
  - appx
aliases:
  - UWP
  - Universal Windows Platform
  - Metro Apps
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
atualizado: 2026-09-24
---

# Aplicações UWP (Universal Windows Platform)

A **Universal Windows Platform (UWP)** é uma plataforma de desenvolvimento introduzida pela Microsoft no Windows 10, sucedendo à arquitetura de *Metro Apps* (Windows 8) e *Modern Apps*. A designação *Universal* reflete a sua capacidade de permitir que o mesmo pacote e base de código sejam executados em múltiplos tipos de dispositivos do ecossistema Windows, incluindo PCs, tablets, smartphones e consolas Xbox.

As aplicações UWP são distribuídas primariamente através da Microsoft Store em pacotes no formato **APPX** (ou MSIX). Exemplos comuns incluem o Windows Terminal, WhatsApp para Windows e Messenger.

## Principais Propriedades da Plataforma
* **Compatibilidade multiplataforma**: execução uniforme em diferentes perfis de hardware Windows.
* **Design adaptado ao sistema operativo**: interfaces fluidas com suporte a temas e dimensões dinâmicas de ecrã.
* **Acesso controlado a recursos**: integração com serviços nativos do Windows (notificações, *live tiles* no Windows 10 e Windows Timeline).
* **Distribuição centralizada**: empacotamento assinado digitalmente e disponibilizado via Microsoft Store.

## Modelo de Execução e Sandbox

Para garantir a proteção do sistema operativo e a privacidade do utilizador, as aplicações UWP operam obrigatoriamente dentro de um ambiente de isolamento (*sandbox*):

* **Sem acesso direto ao Registry**: As aplicações não podem ler ou escrever livremente nas chaves do sistema; qualquer interação é restrita e intermediada pelo componente *Brokered Windows Runtime Component (BWC)*.
* **Acesso restrito ao sistema de ficheiros**: A aplicação está confinada à sua própria pasta de dados no perfil do utilizador, ficando impedida de aceder livremente a diretórios do sistema ou ficheiros de outros programas.
* **API Windows Runtime (WinRT)**: As aplicações são forçadas a utilizar a API moderna WinRT em vez das APIs Win32 tradicionais, assegurando a mediação de todas as chamadas de sistema.
* **Declaração explícita de permissões**: Recursos sensíveis de hardware (como microfone, câmara Web, localização e adaptadores de rede) têm de ser declarados previamente no manifesto da aplicação e explicitamente autorizados pelo utilizador.

## Auditoria de Processos UWP em Execução

Para identificar os processos em execução associados a pacotes UWP, o utilitário nativo `tasklist` disponibiliza o parâmetro `/APPS`:

```cmd
tasklist /APPS
```

Para contabilizar o número total de processos UWP atualmente ativos no sistema:

```cmd
tasklist /apps | find /c "."
```

## Inventário de Pacotes Instalados no Sistema

No PowerShell, o cmdlet `Get-AppxPackage` permite listar e auditar todas as aplicações UWP/APPX instaladas na máquina:

```powershell
# Listar nome e nome completo do pacote de forma legível
Get-AppxPackage | Select Name, PackageFullName | Format-Table -AutoSize

# Exportar inventário detalhado de metadados para ficheiro CSV
Get-AppxPackage | Select Name, Version, Status, ProviderName, Source, FromTrustedSource, FastPackageReference | Export-Csv -Encoding utf8 -Delimiter ";" -Path appx_instaladas.csv

# Listar os pacotes instalados para todos os utilizadores da máquina
Get-AppxPackage -AllUsers | Export-Csv -Path appx_todos_utilizadores.csv
```

## Diretórios de Binários e Instalação

Os ficheiros executáveis e binários das aplicações UWP residem em dois locais fundamentais consoante a sua origem:

| Categoria | Caminho no Disco | Descrição e Permissões |
| :--- | :--- | :--- |
| **Aplicações de Sistema** | `C:\Windows\SystemApps\` | Pacotes essenciais pré-integrados no sistema operativo (ex.: componentes de shell e pesquisa). |
| **Aplicações Instaladas (Store)** | `C:\Program Files\WindowsApps\` | Diretório protegido onde são instaladas as aplicações da Microsoft Store. |

> [!NOTE] Permissões em `WindowsApps` e o `TrustedInstaller`
> A pasta `C:\Program Files\WindowsApps` possui permissões estritas de controlo de acesso, estando bloqueada à navegação direta mesmo para utilizadores pertencentes ao grupo dos Administradores locais.
> * O proprietário (*owner*) da pasta é a conta de sistema interna **`TrustedInstaller`**.
> * Esta entidade de segurança está diretamente associada ao serviço do Windows **Windows Modules Installer** (`TrustedInstaller.exe`), garantindo que apenas os processos de atualização e instalação oficiais do sistema possam modificar os binários.

Para os artefactos forenses gerados durante a utilização das aplicações (histórico, definições e memória virtual), consulta: [[UWP - Artefactos Forenses e Estrutura de Dados]].

## Notas relacionadas

- [[UWP - Artefactos Forenses e Estrutura de Dados]]
- [[Processos e linha de comandos no Windows]]
- [[Registry em Aplicações Modernas (MSIX e Helium)]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
