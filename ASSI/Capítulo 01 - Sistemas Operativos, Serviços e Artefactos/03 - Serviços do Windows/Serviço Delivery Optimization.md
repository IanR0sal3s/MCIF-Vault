---
title: Serviço Delivery Optimization
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 3
tipo: conceito
tags:
  - assi
  - windows
  - servicos
  - windows-update
  - p2p
  - redes
aliases:
  - DoSvc
  - DeliveryOptimization
  - Delivery Optimization Service
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v4.pdf
atualizado: 2026-11-21
---

# Serviço Delivery Optimization (`DoSvc`)

O **Delivery Optimization (`DoSvc`)** é um serviço do Windows (empregue pelo Windows Update) que utiliza um protocolo **P2P (estilo BitTorrent)** para descarregar e partilhar conteúdos com computadores na proximidade.

## 1. Funcionamento e Diferença face ao BITS

* **Arquitetura P2P**: em vez de cada máquina descarregar individualmente todos os ficheiros da Internet, interage com outros PCs próximos na rede local (ou Internet) para partilhar blocos de atualizações.
* **Diferença face ao [[Serviço BITS]]**: o BITS transfere em modelo cliente-servidor aproveitando largura de banda ociosa; o Delivery Optimization distribui conteúdos em malha P2P entre pares.
* **Valor forense (Capítulo 4)**: os seus logs `.etl` (`dosvc*`) registam o `ExternalIPAddress` dos últimos 28 dias — ver [[Logs ETL e Caso de Estudo Delivery Optimization (IP Externo)]].

---

## Além da aula

* **Execução e rede**: corre sob `svchost.exe -k NetworkService -p` (`NT Authority\NetworkService`, arranque `AUTO_START (DELAYED)`), utilizando tipicamente a porta `7680/TCP` (e UDP) para tráfego P2P.
* **Hardening via GPO**: em redes corporativas configura-se `GroupMode = 1` para restringir a partilha P2P apenas à rede local (LAN).

---

## Perguntas de revisão

1. **Que protocolo utiliza o serviço Delivery Optimization e qual a sua finalidade no Windows Update?**

> [!success]- Ver Resposta
> Utiliza um protocolo **P2P (estilo BitTorrent)** para descarregar e partilhar atualizações com outros computadores na proximidade, reduzindo o consumo repetido de largura de banda externa.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Serviço BITS]] | `mesmo bloco` |
| **Seguinte** | [[Windows Search]] | `mesmo bloco` |
| **Índice** | [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]] · [[00 ASSI]] | `Bloco 03` |

### Conceitos Relacionados

* [[svchost.exe]] · `mesmo bloco`
* [[Serviços Windows]] · `mesmo bloco`
* [[Logs ETL e Caso de Estudo Delivery Optimization (IP Externo)]] · `ASSI · Cap. 4`
