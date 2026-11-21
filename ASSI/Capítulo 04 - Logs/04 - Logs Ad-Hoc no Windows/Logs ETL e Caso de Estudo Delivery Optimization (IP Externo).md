---
title: Logs ETL e Caso de Estudo Delivery Optimization (IP Externo)
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
  - etl
  - delivery-optimization
  - tracerpt
  - ip-externo
  - forense
aliases:
  - Event Trace Log
  - Logs ETL
  - Delivery Optimization ETL
  - tracerpt
atualizado: 2026-11-21
---

# Logs ETL e Caso de Estudo Delivery Optimization (IP Externo)

Os ficheiros **ETL (*Event Trace Log*)** são um formato binário da Microsoft desenhado para registar execuções (*traces*) de eventos de elevada frequência (ex.: acessos a disco, *page faults*). No serviço **Delivery Optimization**, estes logs constituem um artefacto forense valioso para recuperar o histórico de endereços IP externos da máquina.

## 1. Formato `ETL` e Ferramenta `tracerpt`

* **Ferramentas nativas**: **`tracerpt`** (linha de comandos) e **Event Viewer**.
* **Ferramentas externas / descontinuadas**: *Microsoft Tracelog*, *Microsoft Message Analyzer* (retirado em 2020) e *Microsoft Network Monitor* (*deprecated*).
* **Uso básico do `tracerpt`**:
  ```cmd
  tracerpt dosvc.etl -o -report
  ```

---

## 2. Caso de Estudo: Delivery Optimization (DO) e IP Externo

O [[Serviço Delivery Optimization]] distribui atualizações do Windows em modo *peer-to-peer* na rede local ou via Internet. Os seus logs `.etl` residem em:

`C:\Windows\ServiceProfiles\NetworkService\AppData\Local\Microsoft\Windows\DeliveryOptimization\Logs`

Existem **dois tipos de ficheiros ETL** nesta pasta:

| Prefixo | Características e Janela Temporal | Informação Forense Principal |
| :--- | :--- | :--- |
| **`domgmt*`** | Limitados a `32 KiB`; abrangência temporal **superior a 1 ano** | Registos de gestão do serviço a longo prazo. |
| **`dosvc*`** | Limitados aos **últimos 28 dias** | Contêm o campo **`ExternalIPAddress`** (IP público da máquina numa data específica). |

* **Valor forense**: a geolocalização do `ExternalIPAddress` permite inferir a localização aproximada do computador numa data concreta (com a ressalva de que a geolocalização de banda larga pode não ser exata).
* **Extração rápida em PowerShell** (em modo administrador):
  ```powershell
  Get-DeliveryOptimizationLog | Where-Object Message -Like "*ExternalIpAddress*"
  ```

*(Nota: os diapositivos referem a Ficha 04.05 — ETL + DeliveryOptimization, cujo enunciado não integra os materiais fornecidos.)*

---

## Perguntas de revisão

1. **Qual a diferença entre os ficheiros `domgmt*` e `dosvc*` do Delivery Optimization?**

> [!success]- Ver Resposta
> Os `domgmt*` têm limite de `32 KiB` mas mantêm histórico superior a 1 ano; os `dosvc*` cobrem apenas os **últimos 28 dias**, mas registam o **`ExternalIPAddress`**, útil para estimar a localização da máquina.

2. **Que ferramentas nativas permitem processar um ficheiro `.etl` e que cmdlet PowerShell extrai diretamente os IPs externos do Delivery Optimization?**

> [!success]- Ver Resposta
> O utilitário CLI `tracerpt` e o Event Viewer. Em PowerShell (como administrador): `Get-DeliveryOptimizationLog | Where-Object Message -Like "*ExternalIpAddress*"`.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Memory Dumps (.dmp) e Windows Error Reporting (WER)]] | `mesmo bloco` |
| **Seguinte** | [[Análise Forense de Logs do OneDrive (ODL, SQLite e OneDriveExplorer)]] | `mesmo bloco` |
| **Índice** | [[Capítulo 4 - Logs]] · [[00 ASSI]] | `Bloco 04` |

### Conceitos Relacionados

* [[Serviço Delivery Optimization]] · `ASSI · Cap. 1`
* [[Serviço BITS]] · `ASSI · Cap. 1`
