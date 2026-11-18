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
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
atualizado: 2026-09-24
---

# Aplicações UWP (Universal Windows Platform)

A **Universal Windows Platform (UWP)** é a plataforma de aplicações modernas do Windows (sucessora das *Metro Apps* do Windows 8), distribuída em pacotes **APPX/MSIX** que correm isolados em *sandbox* sob a API WinRT.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: Aplicações Win32 clássicas têm acesso amplo ao sistema de ficheiros e ao Registry global, permitindo que software malicioso comprometa o sistema ou deixe resíduos permanentes; a plataforma UWP isola cada aplicação num contentor (*sandbox*) mediado pela API **WinRT** e pelo *Brokered Windows Runtime Component (BWC)*.
> * **Porque importa (Forense / Segurança)**: Os binários das aplicações da Store ficam protegidos em `C:\Program Files\WindowsApps\` sob posse exclusiva da conta **`TrustedInstaller`**, exigindo comandos específicos (`tasklist /APPS` e `Get-AppxPackage`) para inventariação e auditoria.
> * **Pontos Críticos para Exame**:
>   * Quatro restrições da *sandbox* UWP: sem acesso direto ao Registry (mediado por **BWC**), acesso restrito ao sistema de ficheiros, uso forçado da API **WinRT** (em vez de Win32) e declaração explícita de permissões no manifesto.
>   * Diferença entre `C:\Windows\SystemApps\` (apps nativas de sistema) e `C:\Program Files\WindowsApps\` (apps instaladas via Store, propriedade do **`TrustedInstaller`** / serviço *Windows Modules Installer*).

---

## Principais Propriedades e Evolução da Plataforma

Introduzida pela Microsoft no Windows 10 (sucedendo às *Metro Apps* do Windows 8 e *Modern Apps*), a designação *Universal* reflete a capacidade de permitir que o mesmo pacote e base de código sejam executados em múltiplos dispositivos do ecossistema Windows (PCs, tablets, smartphones e consolas Xbox). As aplicações UWP são distribuídas primariamente através da Microsoft Store em pacotes **APPX** (ou MSIX), incluindo exemplos como o Windows Terminal, WhatsApp para Windows e Messenger.

* **Compatibilidade multiplataforma**: execução uniforme em diferentes perfis de hardware Windows.
* **Design adaptado ao sistema operativo**: interfaces fluidas com suporte a temas e dimensões dinâmicas de ecrã.
* **Acesso controlado a recursos**: integração com serviços nativos do Windows (notificações, *live tiles* no Windows 10 e Windows Timeline).
* **Distribuição centralizada**: empacotamento assinado digitalmente e disponibilizado via Microsoft Store.

---

## Modelo de Execução e Isolamento em *Sandbox*

Para garantir a proteção do sistema operativo e a privacidade do utilizador, as aplicações UWP operam obrigatoriamente dentro de um ambiente de isolamento (*sandbox*):

| Domínio de Isolamento | Comportamento na *Sandbox* UWP | Mecanismo Mediador |
| :--- | :--- | :--- |
| **1. Acesso ao Registry** | Sem leitura ou escrita direta nas chaves globais do sistema. | Mediado pelo *Brokered Windows Runtime Component (**BWC**)* e isolado em ficheiro próprio (`settings.dat`). |
| **2. Sistema de Ficheiros** | Confinada à sua pasta de dados no perfil do utilizador; impedida de ler pastas de sistema ou de outros programas. | Contentor de perfil (`%LocalAppData%\Packages\<APP>`). |
| **3. Chamadas de Sistema (API)** | Impedida de invocar livremente APIs Win32 tradicionais. | Forçada a utilizar a API moderna **Windows Runtime (WinRT)**. |
| **4. Hardware e Recursos Sensíveis** | Acesso bloqueado por omissão a câmara, microfone, localização e rede. | Exige **declaração explícita no manifesto** da aplicação e autorização do utilizador. |

---

## Auditoria de Processos e Inventário de Pacotes via CLI

### 1. Processos UWP em Execução (`tasklist /APPS`)
Para identificar os processos em execução associados a pacotes UWP, o utilitário nativo `tasklist` disponibiliza o parâmetro `/APPS`:

```cmd
REM Listar todos os processos UWP ativos e respetivos nomes de pacote
tasklist /APPS

REM Contabilizar o número total de processos UWP atualmente ativos no sistema
tasklist /apps | find /c "."
```

### 2. Inventário de Pacotes Instalados (`Get-AppxPackage`)
No PowerShell, o cmdlet `Get-AppxPackage` permite listar e auditar todas as aplicações UWP/APPX instaladas na máquina:

#### Anatomia do Pipeline PowerShell (`Get-AppxPackage`)

* **`Get-AppxPackage`**: enumera os pacotes instalados no perfil do utilizador atual (ou de toda a máquina se usado **`-AllUsers`**).
* **`Select Name, Version, ...`**: filtra as propriedades relevantes de cada pacote (como `FromTrustedSource` e `PackageFullName`).
* **`Export-Csv -Encoding utf8 -Delimiter ";"`**: exporta o inventário forense para ficheiro CSV estruturado.

```powershell
# Listar nome e nome completo do pacote de forma legível
Get-AppxPackage | Select Name, PackageFullName | Format-Table -AutoSize

# Exportar inventário detalhado de metadados para ficheiro CSV
Get-AppxPackage | Select Name, Version, Status, ProviderName, Source, FromTrustedSource, FastPackageReference | Export-Csv -Encoding utf8 -Delimiter ";" -Path appx_instaladas.csv

# Listar os pacotes instalados para todos os utilizadores da máquina
Get-AppxPackage -AllUsers | Export-Csv -Path appx_todos_utilizadores.csv
```

---

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

---

## Perguntas de revisão

1. **Quais são as quatro restrições fundamentais impostas pela *sandbox* de execução das aplicações UWP?**

> [!success]- Ver Resposta
> 1. **Sem acesso direto ao Registry**: mediado pelo *Brokered Windows Runtime Component (BWC)*.
> 2. **Acesso restrito ao sistema de ficheiros**: confinada à sua própria pasta de dados no perfil do utilizador.
> 3. **Uso forçado da API WinRT** (*Windows Runtime*) em vez das APIs Win32 tradicionais.
> 4. **Declaração explícita de permissões**: o acesso a microfone, câmara, localização ou rede tem de constar no manifesto e ser autorizado pelo utilizador.

2. **Qual é a diferença entre os diretórios `C:\Windows\SystemApps\` e `C:\Program Files\WindowsApps\`, e qual é a conta proprietária (*owner*) deste último?**

> [!success]- Ver Resposta
> * `C:\Windows\SystemApps\` armazena pacotes UWP nativos pré-integrados no próprio sistema operativo.
> * `C:\Program Files\WindowsApps\` armazena as aplicações UWP instaladas a partir da Microsoft Store. O seu proprietário (*owner*) é a conta interna **`TrustedInstaller`** (associada ao serviço *Windows Modules Installer* / `TrustedInstaller.exe`), que bloqueia o acesso direto mesmo a Administradores locais.

3. **Que comandos permitem, respetivamente, (a) contabilizar os processos UWP em execução no `cmd.exe` e (b) exportar para CSV os pacotes APPX instalados para todos os utilizadores no PowerShell?**

> [!success]- Ver Resposta
> * **(a) No `cmd.exe`**: `tasklist /apps | find /c "."`
> * **(b) No PowerShell**: `Get-AppxPackage -AllUsers | Export-Csv -Path appx_todos_utilizadores.csv`

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
