---
title: Análise Forense de Logs do OneDrive (ODL, SQLite e OneDriveExplorer)
tipo: analise
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 4
bloco: 4
fonte_aula: EI_ASSI_1S2026-27_cap04_v01_LOGs_parte02_v1.pdf
tags:
  - assi
  - logs
  - onedrive
  - odl
  - sqlite
  - onedriveexplorer
  - privacidade
  - forense
aliases:
  - Logs OneDrive
  - OneDriveExplorer
  - Ficheiros ODL
atualizado: 2026-11-21
---

# Análise Forense de Logs do OneDrive (ODL, SQLite e `OneDriveExplorer`)

O cliente Microsoft OneDrive mantém localmente logs de sincronização, ficheiros de estado e bases de dados SQLite que permitem reconstruir a estrutura de pastas e atividade de ficheiros na nuvem.

## 1. Localização e Estrutura dos Artefactos do OneDrive

### Logs de Sincronização (`.odl`)
* **Pasta**: `%LOCALAPPDATA%\Microsoft\OneDrive\logs\`
  * Contas empresariais/escolares: `\logs\Business1`
  * Contas pessoais: `\logs\Personal`
* **Extensões**: `.odl`, `.odlgz`, `.odlsent` e `.aold`.
* **Cifragem (desde abril de 2022)**: os ficheiros de log passaram a ser cifrados com **AES-ECB 128 bits**, ficando a chave armazenada localmente no ficheiro **`general.keystore`**.
* **Ficheiros de estado**: `<UserCid>.dat` e `<UserCid>.dat.previous` (onde `UserCid` identifica a conta do utilizador).

### Bases de Dados SQLite 3
Nas versões recentes, o OneDrive armazena diversas bases SQLite em `%LOCALAPPDATA%\Microsoft\OneDrive\settings\`, incluindo `SafeDelete.db`, `SettingsDatabase.db`, `SyncEngineDatabase.db`, `UXDatabase.db` e caches de telemetria (`.otc`).

É possível localizar todas as bases SQLite numa diretoria (independentemente da extensão) procurando o cabeçalho mágico com `sfk`:
```cmd
sfk hexfind -text "/SQLite format 3/" -dir %LOCALAPPDATA%\Microsoft\OneDrive\ -stat
```

---

## 2. Análise com `OneDriveExplorer`

Ferramenta open source (*Beercow/OneDriveExplorer*) com versão **GUI** e **CLI** que reconstrói a estrutura de pastas do OneDrive a partir de `<UserCid>.dat`/`.previous` e decifra/analisa os logs `.odl`, `.odlgz`, `.odlsent` e `.aold`.

```cmd
:: Extrair e exportar logs OneDrive da máquina live para CSV
OneDriveExplorer.exe --LIVE LIVE --csv --output-dir c:\temp\OneDriveCSV
```
*(Gera ficheiros CSV no diretório indicado, como `USER_Business1_OneDrive.csv`.)*

---

## 3. Nota de Encerramento: Telemetria e Privacidade em Veículos

Os diapositivos encerram o capítulo destacando a expansão da recolha de logs/telemetria para além de computadores — citando o estudo da Mozilla (*"Cars Are the Worst Product Category We Have Ever Reviewed for Privacy"*): fabricantes automóveis recolhem continuamente dados do condutor e do ambiente através da conetividade do veículo e da aplicação móvel da marca, chegando algumas marcas a vendê-los a terceiros (*data hubs*).

---

## Perguntas de revisão

1. **O que mudou nos logs `.odl` do OneDrive a partir de abril de 2022 e onde se encontra a chave necessária para os decifrar?**

> [!success]- Ver Resposta
> Passaram a estar cifrados com **ECB 128 bits**, encontrando-se a chave localmente no ficheiro **`general.keystore`**.

2. **Como se podem identificar rapidamente todas as bases de dados SQLite na pasta do OneDrive mesmo quando não têm extensão `.db` ou `.sqlite`?**

> [!success]- Ver Resposta
> Procurando a assinatura de cabeçalho `SQLite format 3` com `sfk hexfind -text "/SQLite format 3/" -dir %LOCALAPPDATA%\Microsoft\OneDrive\ -stat`.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Logs ETL e Caso de Estudo Delivery Optimization (IP Externo)]] | `mesmo bloco` |
| **Seguinte** | [[Cheat Sheet - Logs no Windows e Threat Hunting]] | Revisão rápida |
| **Índice** | [[Capítulo 4 - Logs]] · [[00 ASSI]] | `Bloco 04` |

### Conceitos Relacionados

* [[Extração de Strings no Windows - Sysinternals strings e Swiss File Knife (sfk)]] · `ASSI · Cap. 3`
* [[Windows Activity Timeline - Arquitetura e Base SQLite]] · `ASSI · Cap. 1`
