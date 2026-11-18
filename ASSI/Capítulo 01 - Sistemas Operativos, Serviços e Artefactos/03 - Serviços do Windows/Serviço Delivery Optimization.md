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
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
atualizado: 2026-09-24
---

# Serviço Delivery Optimization (DoSvc)

O **Delivery Optimization (`DoSvc`)** é o serviço do Windows que otimiza o descarregamento e distribuição de atualizações do Windows Update e da Microsoft Store através de uma arquitetura híbrida cliente-servidor e ponto a ponto (**P2P**).

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: Evita que centenas de computadores numa mesma organização saturem a ligação à Internet (WAN) ao descarregarem individualmente os mesmos gigabytes de atualizações; um posto descarrega os pacotes e partilha blocos localmente na LAN via P2P (estilo BitTorrent).
> * **Porque importa (Forense / Segurança)**: Gera tráfego P2P intenso (porta **7680/TCP** e UDP) que pode produzir falsos positivos em análises de tráfego de rede (aparentando *torrents* ilícitos ou exfiltração); se mal configurado sem restrição GPO (`GroupMode = 1`), pode partilhar blocos com máquinas na Internet pública.
> * **Pontos Críticos para Exame**:
>   * Nome interno: **`DoSvc`**, alojado num [[svchost.exe]] partilhado (`svchost.exe -k NetworkService -p`) sob a conta `NT Authority\NetworkService` com arranque `AUTO_START (DELAYED)`.
>   * Distinção crítica face ao [[Serviço BITS]]: o BITS gere a fila cliente-servidor usando largura de banda ociosa; o `DoSvc` distribui blocos em malha P2P entre computadores vizinhos.

---

## Princípio de Funcionamento P2P

Em vez de cada computador descarregar individualmente os mesmos ficheiros pesados a partir dos servidores em nuvem da Microsoft, o Delivery Optimization tira partido da proximidade física e de rede das máquinas:

* **Protocolo P2P (estilo BitTorrent)**: O serviço interage com outros computadores na mesma rede local (LAN) ou na Internet para partilhar e descarregar segmentos de ficheiros.
* **Redução de Consumo de Largura de Banda WAN**: Numa rede corporativa ou académica com centenas de postos, o primeiro computador descarrega a atualização a partir da Internet e distribui os blocos localmente aos restantes postos a alta velocidade através da rede interna.

---

## Configuração do Serviço no Windows (`sc qc DoSvc`)

A inspeção do serviço através do utilitário `sc` revela a sua arquitetura de execução:

```cmd
sc qc DoSvc
```

| Parâmetro (`sc qc`) | Valor Configurado no `DoSvc` | Significado Operacional |
| :--- | :--- | :--- |
| **`SERVICE_NAME`** | `DoSvc` | Identificador interno do serviço Delivery Optimization. |
| **`BINARY_PATH_NAME`** | `C:\WINDOWS\System32\svchost.exe -k NetworkService -p` | Executado como processo partilhado [[svchost.exe]] sob o grupo `NetworkService`. |
| **`START_TYPE`** | `2   AUTO_START (DELAYED)` | Arranque automático com atraso para não sobrecarregar a inicialização do sistema. |
| **`DEPENDENCIES`** | `RPCSS` | Depende do serviço de chamadas remotas de procedimentos (`RPCSS`). |
| **`SERVICE_START_NAME`** | `NT Authority\NetworkService` | Opera com privilégios restritos de serviço de rede (em vez de `LocalSystem`). |

---

## Comparação Direta: Delivery Optimization (`DoSvc`) vs. BITS

Embora ambos estejam envolvidos em transferências do Windows Update, operam em modelos arquiteturais distintos:

| Critério | [[Serviço BITS]] (`BITS`) | Delivery Optimization (`DoSvc`) |
| :--- | :--- | :--- |
| **Arquitetura de Rede** | Cliente-Servidor tradicional (ponto único de origem para o cliente). | Híbrida Cliente-Servidor e malha distribuída **P2P** (estilo BitTorrent). |
| **Mecanismo de Otimização** | Gere a fila local utilizando exclusivamente **largura de banda ociosa** da ligação. | Divide ficheiros em múltiplos blocos obtidos a partir de **computadores vizinhos na LAN** (ou Internet). |
| **Instância `svchost.exe`** | `svchost.exe -k netsvcs -p` | `svchost.exe -k NetworkService -p` |
| **Foco de Auditoria** | Persistência LOLBIN, Event Log e base de dados ESE `qmgr.db`. | Tráfego P2P na rede interna (porta 7680/TCP e UDP) e políticas de grupo (`GroupMode = 1`). |

---

## Implicações de Administração e Segurança de Redes

1. **Gestão de Tráfego e Políticas de Grupo (GPO)**:
   * Em redes corporativas, o Delivery Optimization deve ser configurado via políticas de grupo para restringir a partilha de conteúdos apenas à rede local (`GroupMode = 1`), impedindo que computadores da organização atuem como nós de partilha para máquinas desconhecidas na Internet pública.
2. **Auditoria de Tráfego Anómalo**:
   * Analistas de rede e segurança que detetem elevado tráfego de saída ponto a ponto (portas 7680/TCP ou ligações UDP) a partir de postos Windows devem correlacionar esses fluxos com a atividade do `DoSvc` antes de presumir tráfego ilícito de torrents ou exfiltração de dados.

---

## Perguntas de revisão

1. **Qual é a diferença fundamental entre o modo como o serviço BITS e o serviço Delivery Optimization (`DoSvc`) otimizam o descarregamento de atualizações do Windows?**

> [!success]- Ver Resposta
> O **BITS** opera num modelo cliente-servidor gerindo a fila local para consumir apenas a largura de banda ociosa da máquina. O **Delivery Optimization (`DoSvc`)** opera numa arquitetura P2P (estilo BitTorrent), dividindo as atualizações em blocos que são partilhados entre computadores vizinhos na rede local (LAN) para poupar largura de banda WAN.

2. **Que parâmetros devolve o comando `sc qc DoSvc` relativamente ao caminho do binário (`BINARY_PATH_NAME`), tipo de arranque (`START_TYPE`) e conta de execução (`SERVICE_START_NAME`)?**

> [!success]- Ver Resposta
> * **`BINARY_PATH_NAME`**: `C:\WINDOWS\System32\svchost.exe -k NetworkService -p`
> * **`START_TYPE`**: `2 AUTO_START (DELAYED)` (arranque automático diferido)
> * **`SERVICE_START_NAME`**: `NT Authority\NetworkService`

3. **Que medida de endurecimento via GPO deve ser aplicada ao `DoSvc` em redes empresariais e que porta de rede está associada ao seu tráfego P2P?**

> [!success]- Ver Resposta
> Deve configurar-se a política de grupo com `GroupMode = 1` para restringir a partilha P2P exclusivamente a máquinas da mesma rede local (LAN), impedindo a partilha com a Internet pública. O tráfego P2P do serviço utiliza tipicamente a porta **7680/TCP** (além de ligações UDP).

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
