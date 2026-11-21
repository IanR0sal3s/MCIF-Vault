---
title: Registry em Aplicações Modernas (MSIX e Helium)
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 6
tipo: conceito
tags:
  - assi
  - windows
  - msix
  - helium
  - registry
  - uwp
  - forense
aliases:
  - MSIX Registry
  - Pasta Helium
  - Virtualized Registry
  - Helium User.dat
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v4.pdf
fontes:
  - "https://tinyurl.com/MSIXregistryHelium"
atualizado: 2026-11-21
---

# Registry em Aplicações Modernas (MSIX e `Helium`)

As aplicações modernas empacotadas em **MSIX** (ex.: Notepad no W11, Windows Terminal, Teams, Paint, Dropbox) correm num contentor isolado com assinatura digital obrigatória e manifesto `AppManifest.xml`. Em vez de escreverem no Registry global do Windows, mantêm ficheiros de **Registry virtualizado privado** na subpasta **`Helium`**.

## 1. Win32 Clássico vs. Pacote MSIX (`Helium`)

| Critério | Aplicação Win32 Clássica | Aplicação Empacotada **MSIX** |
| :--- | :--- | :--- |
| **Escrita em `HKCU`** | `C:\Users\<user>\NTUSER.DAT` | `%LocalAppData%\Packages\<APPID>\SystemAppData\Helium\User.dat` |
| **Escrita em `HKLM`** | `%SystemRoot%\System32\config\SOFTWARE` | `...\SystemAppData\Helium\Registry.dat` |
| **Classes / COM** | `USRCLASS.DAT` | `...\SystemAppData\Helium\UsrClasses.dat` |
| **Assinatura digital** | Opcional | **Obrigatória** + manifesto `AppManifest.xml` |

*(Na extração forense da pasta `Helium`, recolher sempre também os logs de transação `*.dat.LOG1` e `*.dat.LOG2` para abrir no `RegistryExplorer`.)*

---

## 2. Caso de Estudo Forense: Bloco de Notas (Notepad) no Windows 11

No Windows 11, o Notepad é uma aplicação MSIX cujo Registry virtualizado reside em:
`%LocalAppData%\Packages\Microsoft.WindowsNotepad_8wekyb3d8bbwe\SystemAppData\Helium\User.dat`

Ao carregar este `User.dat` no **`RegistryExplorer`**, encontra-se a chave **`OpenSavePIDMru`** (ficheiros abertos/guardados recentemente no Notepad), que **não aparece no `NTUSER.DAT` global do utilizador**.

> [!IMPORTANT] Risco de Falso Negativo
> Em perícias ao Windows 10/11, analisar apenas `NTUSER.DAT` leva a falsos negativos sobre ficheiros abertos em aplicações MSIX. É necessário recolher também `%LocalAppData%\Packages\*\SystemAppData\Helium\`.

---

## Perguntas de revisão

1. **Onde guarda uma aplicação MSIX (como o Notepad no Windows 11) as suas chaves de Registry privadas e que ficheiros existem nessa pasta?**

> [!success]- Ver Resposta
> Na pasta `%LocalAppData%\Packages\<APPID>\SystemAppData\Helium\`, contendo os hives virtualizados **`User.dat`**, **`Registry.dat`** e **`UsrClasses.dat`** (mais os respetivos `.LOG1`/`.LOG2`).

2. **Porque é que um perito que analise apenas `NTUSER.DAT` no Windows 11 pode não encontrar os ficheiros recentemente abertos no Notepad?**

> [!success]- Ver Resposta
> Porque o Notepad do Windows 11 é empacotado em MSIX e grava a chave `OpenSavePIDMru` exclusivamente no seu hive privado `Helium\User.dat`, sem escrever no `NTUSER.DAT` global.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Ficha Prática e Questionário - Windows Registry e Artefactos Forenses]] | `Bloco 05` |
| **Seguinte** | [[Timestamps e Épocas Temporais (UNIX Epoch vs. Windows FILETIME)]] | `Comum/` · `mesmo bloco` |
| **Índice** | [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]] · [[00 ASSI]] | `Bloco 06` |

### Conceitos Relacionados

* [[Estrutura e Hives do Windows Registry]] · `Bloco 05`
* [[Ferramentas de Análise e Extração do Registry]] · `Bloco 05`
* [[Aplicações UWP (Universal Windows Platform) - Visão Geral]] · `Bloco 04`
* [[UWP - Artefactos Forenses e Estrutura de Dados]] · `Bloco 04`
