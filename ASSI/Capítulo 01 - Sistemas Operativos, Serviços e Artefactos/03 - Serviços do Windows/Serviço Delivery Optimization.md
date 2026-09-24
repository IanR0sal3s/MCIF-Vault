---
title: Serviço Delivery Optimization
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
tipo: conceito
tags:
  - windows
  - servicos
  - windows-update
  - p2p
  - redes
aliases:
  - DoSvc
  - DeliveryOptimization
  - Delivery Optimization Service
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
atualizado: 2026-09-24
---

# Serviço Delivery Optimization (DoSvc)

O **Delivery Optimization (DoSvc)** é um serviço do Windows concebido para otimizar o descarregamento e a distribuição de atualizações do sistema operativo (**Windows Update**), aplicações da Microsoft Store e outros ficheiros de instalação da Microsoft através de uma arquitetura híbrida cliente-servidor e ponto a ponto (**P2P**).

---

## Princípio de Funcionamento P2P

Em vez de cada computador descarregar individualmente os mesmos ficheiros pesados a partir dos servidores em nuvem da Microsoft, o Delivery Optimization tira partido da proximidade física e de rede das máquinas:
* **Protocolo P2P (estilo BitTorrent)**: O serviço interage com outros computadores na mesma rede local (LAN) ou na Internet para partilhar e descarregar segmentos de ficheiros.
* **Redução de Consumo de Largura de Banda WAN**: Numa rede corporativa ou académica com centenas de postos, o primeiro computador descarrega a atualização a partir da Internet e distribui os blocos localmente aos restantes postos a alta velocidade através da rede interna.

---

## Configuração do Serviço no Windows

A inspeção do serviço através do utilitário `sc` revela a sua arquitetura de execução:

```cmd
sc qc DoSvc
```

Parâmetros chave da configuração:
* **`SERVICE_NAME`**: `DoSvc`
* **`BINARY_PATH_NAME`**: `C:\WINDOWS\System32\svchost.exe -k NetworkService -p` (executado como processo partilhado [[svchost.exe]] sob o grupo `NetworkService`).
* **`START_TYPE`**: `2   AUTO_START (DELAYED)` (arranque automático com atraso para não sobrecarregar a inicialização do sistema).
* **`DEPENDENCIES`**: Depende do serviço de chamadas remotas de procedimentos (`RPCSS`).
* **`SERVICE_START_NAME`**: `NT Authority\NetworkService` (opera com privilégios de serviço de rede).

---

## Distinção entre Delivery Optimization e BITS

Embora ambos estejam envolvidos em transferências do Windows Update, operam em níveis distintos:
* **[[Serviço BITS]]**: Gere a fila local e o agendamento de transferências utilizando exclusivamente a largura de banda ociosa entre o cliente e o servidor de origem.
* **Delivery Optimization**: Gere a malha de distribuição distribuída P2P, dividindo ficheiros em múltiplos blocos obtidos a partir de computadores vizinhos na rede.

---

## Implicações de Administração e Segurança de Redes

1. **Gestão de Tráfego e Políticas de Grupo (GPO)**:
   * Em redes corporativas, o Delivery Optimization deve ser configurado via políticas de grupo para restringir a partilha de conteúdos apenas à rede local (`GroupMode = 1`), impedindo que computadores da organização atuem como nós de partilha para máquinas desconhecidas na Internet pública.
2. **Auditoria de Tráfego Anómalo**:
   * Analistas de rede e segurança que detetem elevado tráfego de saída ponto a ponto (portas 7680/TCP ou ligações UDP) a partir de postos Windows devem correlacionar esses fluxos com a atividade do `DoSvc` antes de presumir tráfego ilícito de torrents ou exfiltração de dados.

## Notas relacionadas

- [[svchost.exe]]
- [[Serviço BITS]]
- [[Serviços Windows]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
