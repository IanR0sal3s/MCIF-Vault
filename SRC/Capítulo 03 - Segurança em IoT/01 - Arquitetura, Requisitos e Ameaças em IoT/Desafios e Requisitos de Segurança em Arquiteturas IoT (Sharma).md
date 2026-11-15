---
title: Desafios e Requisitos de Segurança em Arquiteturas IoT (Sharma)
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Segurança em Redes de Computadores
sigla_uc: SRC
capitulo: 3
bloco: 1
fonte_aula: Sharma_yellow.pdf (Secções 3.1–3.5, 4.1–4.4, 7.2.1–7.2.4; Fig. 1; Table 3)
tags:
  - src
  - iot
  - arquitetura-iot
  - seguranca-iot
aliases:
  - Arquitetura IoT Sharma
  - Desafios de Segurança IoT
  - Requisitos de Segurança IoT
atualizado: 2026-11-15
---

# Desafios e Requisitos de Segurança em Arquiteturas IoT (*Sharma*)

Os ecossistemas IoT organizam-se numa arquitetura de **cinco camadas** (*Perception*, *Network*, *Application*, *Processing* e *Business*), cada qual com protocolos e desafios de segurança específicos condicionados por **restrições de energia, memória, computação e heterogeneidade**.

> [!TIP] Lógica de Funcionamento e Valor de Segurança
> * **Porque existe (Arquitetura)**: Cada camada desempenha um papel distinto — desde a recolha física de dados (*Perception*) até à visualização empresarial (*Business*) — exigindo controlos de segurança adaptados ao seu perfil de recursos.
> * **Porque importa (Segurança)**: Algoritmos criptográficos convencionais e mecanismos pesados de privacidade são frequentemente inviáveis em nós sensores com bateria limitada e modos *sleep*, criando vetores de ataque específicos (exaustão de bateria, manipulação física e *spoofing*).
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **5 Camadas (Tabela 3 de Sharma)**: *Perception*, *Network*, *Processing*, *Application* e *Business*.
>   * **Modos *sleep***: durante os períodos de poupança de energia, funções de segurança ficam frequentemente inativas, abrindo janelas de vulnerabilidade.

---

## 1. Desafios de Segurança nas 5 Camadas IoT (Secções 3.1–3.5 e Tabela 3)

| Camada | Função Primária | Protocolos / Tecnologias | Principais Desafios de Segurança |
| :--- | :--- | :--- | :--- |
| **1. *Perception* (Sensorização)** | Recolher dados do ambiente, atuar e converter sinais físicos em digitais | `Bluetooth`, `RFID`, `NFC`, `LoRaWAN` | **Adulteração física (*physical tampering*)**, roubo/substituição em ambientes remotos, **recursos limitados** (energia, memória, CPU), dificuldade em cifrar ao nível do dispositivo, heterogeneidade e limitações de atualização de *firmware*. |
| **2. *Network* (Rede)** | Transmitir dados da camada *Perception* e definir encaminhamento | `6LoWPAN`, `RPL`, `CARP` (`Wi-Fi`, `BLE`, `LoRaWAN`) | Transmissão segura, **autenticação de dispositivos**, gestão de escalabilidade, interoperabilidade entre protocolos, **gestão de chaves** e fiabilidade/perda de pacotes (retransmissões consomem energia); mobilidade complica *routing*. |
| **3. *Processing* (Processamento)** | Computação, agregação, cifragem, armazenamento e *backup* (alivia *Application*) | *Big Data*, `DBMS`, *Cloud Computing* | Processamento seguro de dados, **integridade e consistência**, armazenamento e *backup* seguros sem comprometer requisitos de **tempo real**. |
| **4. *Application* (Aplicação)** | Receber/interpretar dados, DSS, interfaces para utilizadores finais | `MQTT`, `CoAP`, `XMPP`, `AMQP` | Privacidade e integridade dos dados, **autenticação e controlo de acesso**, gestão segura de APIs, vulnerabilidades de software/malware e interoperabilidade. |
| **5. *Business* (Negócio)** | Visualização gráfica, apoio à decisão e processos de negócio | `HTTP`, `FTP` | Conformidade regulatória, gestão de confiança, titularidade e privacidade dos dados, gestão de risco, segurança financeira e aplicação uniforme de políticas. |

---

## 2. Desafios Comuns Associados à Segurança (Secções 4.1–4.4)

1. **Armazenamento em massa e processamento (4.1)**: Volume massivo de dados heterogéneos gerados por sensores exige cifragem e controlo de acesso em ambientes restritos, levando ao recurso à *cloud* para armazenamento e *backup*.
2. **Consumo de energia (4.2)**: Atacantes exploram a camada *Perception* para forçar consumo excessivo de energia e esgotar baterias rapidamente; autenticação robusta na camada *Perception* é essencial.
3. **Implementação em tempo real (4.3)**: *Offloading* para a *cloud* introduz latência; atacantes podem explorar ou induzir atrasos para perturbar sistemas críticos (ex.: transportes inteligentes).
4. **Segurança e privacidade (4.4)**: Algoritmos tradicionais são frequentemente ineficientes em IoT; dispositivos ligados à Internet transmitem dados sensíveis recolhidos por sensores (ex.: drones com câmara em zonas sensíveis), exigindo soluções leves (*lightweight*) adaptadas.

---

## 3. Requisitos Específicos de Segurança em IoT (Secções 7.2.1–7.2.4)

* **7.2.1 Gestão de Identidade (*Identity Management*)**: Atribuir um ID único a cada entidade para prevenir *identity spoofing*, *credential stuffing* e MITM; escalabilidade exige técnicas como `PKI` ou soluções descentralizadas (*blockchain*).
* **7.2.2 Mobilidade**: Dispositivos que mudam dinamicamente de rede complicam autenticação e integridade contínua, aumentando risco de MITM e `DoS` (requer cifragem robusta e gestão dinâmica de chaves).
* **7.2.3 Privacidade**: Domínios como saúde e IIoT recolhem dados altamente sensíveis; soluções tradicionais de privacidade têm demasiado *overhead*, exigindo mecanismos leves específicos para IoT.
* **7.2.4 Energia e Poder Computacional**: Adaptações leves de criptografia podem reduzir robustez; além disso, nós entram em *low-power/sleep mode* (desativando temporariamente funções de segurança) e comunicam por canais sem fios inerentemente suscetíveis a interceção.

---

## Perguntas de revisão

1. **Porque é que a camada *Perception* é particularmente crítica em termos de segurança IoT segundo Sharma?**

> [!success]- Ver Resposta
> Porque os dispositivos operam frequentemente em ambientes remotos sem supervisão humana (expostos a adulteração física, roubo ou substituição), possuem restrições severas de CPU, memória e bateria que dificultam cifragem, gestão de chaves e atualizações de *firmware*, e utilizam ligações sem fios suscetíveis a interceção.

2. **Qual o impacto dos modos *sleep* e da heterogeneidade nos requisitos específicos de segurança IoT?**

> [!success]- Ver Resposta
> Os modos *sleep* desativam temporariamente funções de segurança para poupar bateria (abrindo janelas de ataque e alvos de exaustão energética), enquanto a heterogeneidade e a mobilidade dificultam a gestão uniforme de identidades, chaves e políticas entre protocolos distintos.

## Notas relacionadas

- [[Ataques e Contramedidas por Camada em IoT (Sharma)]]
- [[LPWAN e Arquitetura LoRaWAN - Entidades, Classes e Chaves (Stanco)]]
- [[TBL 3 - Segurança em IoT (BLE, LoRaWAN e MQTT)]]
