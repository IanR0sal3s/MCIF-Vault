---
title: Ataques e Contramedidas por Camada em IoT (Sharma)
tipo: analise
mestrado: Cibersegurança e Informática Forense
uc: Segurança em Redes de Computadores
sigla_uc: SRC
capitulo: 3
bloco: 1
fonte_aula: Sharma_yellow.pdf (Secções 8.1.1–8.1.3, 9.1–9.8; Table 8)
tags:
  - src
  - iot
  - ataques-iot
  - contramedidas
  - rpl
  - ids
aliases:
  - Ataques por Camada IoT
  - Contramedidas IoT
atualizado: 2026-11-15
---

# Ataques e Contramedidas por Camada em IoT (*Sharma*)

Nenhuma política ou algoritmo único protege todas as camadas IoT: cada camada (*Perception*, *Network* e *Application*) apresenta vetores de ataque próprios que exigem contramedidas específicas e combinadas (*defense in depth*).

> [!TIP] Lógica de Funcionamento e Valor de Segurança
> * **Porque existe (Taxonomia)**: Mapear ataques por camada permite associar rapidamente sintomas (ex.: perda seletiva de pacotes, drenagem de bateria, execução de código) às respetivas defesas técnicas.
> * **Porque importa (Segurança)**: Ataques de encaminhamento (`Sinkhole`, `Blackhole`, `Wormhole`, `Selective Forwarding`) e ataques passivos (*Side-channel*, *Traffic analysis*) não alteram necessariamente os pacotes individuais, exigindo `IDS`, monitorização de vizinhos e *multipath routing*.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Blackhole vs. Selective Forwarding**: o *Blackhole* descarta **todos** os pacotes; o *Selective Forwarding* descarta **apenas alguns** e encaminha outros, sendo mais difícil de detetar.
>   * **Broker MQTT como ponto crítico (Secção 8.1.1)**: se o *broker* central for comprometido, o atacante ganha controlo extensivo sobre o fluxo de mensagens e integridade dos dados.

---

## 1. Ataques por Camada (Secções 8.1.1–8.1.3 e Tabela 8)

### 1.1. Camada *Perception*
* **`DDoS` / *Jamming***: tráfego malicioso ou interferência rádio esgota bateria e largura de banda.
* ***Node Destroy* / *Physical Vulnerability***: destruição física, substituição por nó falso ou injeção contínua de dados falsos para manter alarmes ativos e drenar bateria.
* ***Node Capturing***: aproximação física (ex.: Bluetooth/ZigBee) para assumir controlo total do nó, violar privacidade e pivotar para camadas superiores.
* ***Malicious Code Injection***: instalação/execução de *scripts* maliciosos ou *buffer overflow* na ausência de *firewalls* locais.
* ***Side-Channel Attack***: inferência de segredos através de fugas indiretas (consumo elétrico, ciclos de CPU, padrões de largura de banda) sem alterar pacotes.
* ***Eavesdropping*, *Spoofing* e *MITM***: interceção de tráfego sem fios, falsificação de IP/MAC e manipulação de pacotes (incluindo comprometimento de *broker* MQTT).

### 1.2. Camada *Network*
* ***Traffic Analysis***: análise passiva de padrões de pacotes sem os alterar (mitigação: cifragem + *padding* / *traffic shaping*).
* ***Flooding Attack***: pedidos para caminhos inexistentes ou *join requests* excessivos em `RPL` para esgotar bateria, memória e largura de banda.
* **Ataques de Encaminhamento (*Routing Attacks*, ex.: `RPL`)**:
  * ***Sinkhole***: nó malicioso anuncia falsa rota mais curta para atrair todo o tráfego;
  * ***Blackhole***: nó malicioso descarta **todos** os pacotes recebidos;
  * ***Selective Forwarding***: nó descarta seletivamente apenas alguns pacotes;
  * ***Wormhole***: dois ou mais nós maliciosos criam um túnel privado entre si para simular o caminho mais rápido/curto e intercetar, atrasar ou descartar pacotes.

### 1.3. Camada *Application*
* ***Malicious Code Injection* / *Reprogramming***: inserção de *scripts* nocivos por falta de validação de *input*, protocolos inseguros ou software desatualizado (podendo integrar o dispositivo numa *botnet*).
* **Tabela 8 inclui ainda**: *Eavesdropping*, *MITM*, *Flooding*, `DDoS`, *Reprogramming Attack* e *Side-Channel Attack*.

---

## 2. Contramedidas Contra Ataques Críticos (Secções 9.1–9.8 e Tabela 8)

| Área / Ameaça | Contramedidas Destacadas (Secção 9 & Tabela 8) |
| :--- | :--- |
| **9.1 *Routing*** | Autenticação e cifragem em `RPL`, ***multipath routing*** (rotas alternativas), **`IDS`** em tempo real, *trust-based frameworks* e **monitorização de vizinhos** (contagem de *hops*). |
| **9.2 `DoS` / `DDoS`** | Algoritmos de `ML`/`DL` (*KNN*, *SVM*, *Decision Tree*, *Random Forest*, *CNN* — com atenção ao custo computacional), filtragem de pacotes, múltiplas políticas de autenticação e controladores **`SDN`**. |
| **9.3 `MITM`** | Cifragem + gestão de chaves (com apoio de *fog computing*), monitorização do tempo de chegada de pacotes e funções de *hash* (com cuidado face a colisões e *length extension attacks*). |
| **9.4 *Code Injection*** | Atualização de software/OS, validação estrita de *input*, eliminação de credenciais por omissão (*default passwords*) e autenticação robusta. |
| **9.5 *Side-Channel*** | Técnicas de ***hiding*** e ***masking*** (tornar consumo/tempo independentes da chave), hardware especializado e injeção de pacotes falsos (*dummy data*) para confundir análise. |
| **9.6 `IDS`** | `IDS` centralizado ou leve nos dispositivos finais; deteção baseada em anomalias para identificar novos padrões; análise estatística quando `ML`/`DL` excedem a capacidade do nó. |
| **9.7 Autenticação Forte** | Esquemas leves, em tempo real e adaptáveis (ex.: em `MQTT`), incluindo abordagens descentralizadas quando aplicável. |
| **9.8 Esquemas de Cifragem** | Cifrar dados e credenciais em trânsito (ex.: em `MQTT`, onde por omissão podem viajar em claro), assegurando gestão segura de chaves. |

---

## Perguntas de revisão

1. **Qual a diferença entre um ataque *Blackhole*, *Selective Forwarding* e *Wormhole* na camada de rede IoT?**

> [!success]- Ver Resposta
> No *Blackhole*, o nó malicioso descarta todos os pacotes que recebe; no *Selective Forwarding*, descarta apenas alguns e encaminha os restantes (mais difícil de detetar); no *Wormhole*, dois ou mais nós coligam-se através de um túnel privado para parecerem mais próximos e atrair tráfego para interceção, atraso ou descarte.

2. **Que técnicas mitigam ataques *Side-Channel* e *Traffic Analysis* em IoT?**

> [!success]- Ver Resposta
> Para *Side-Channel*: *hiding* e *masking* (desacoplar consumo/tempo da chave criptográfica), hardware dedicado e injeção de ruído/*dummy data*. Para *Traffic Analysis*: cifragem combinada com *traffic shaping*, *padding* e pacotes fictícios.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Desafios e Requisitos de Segurança em Arquiteturas IoT (Sharma)]] | `mesmo bloco` |
| **Seguinte** | [[Segurança em BLE - Pairing Feature Exchange, LE Legacy e LE Secure Connections (Lacava)]] | `muda para Bloco 02` |
| **Índice** | [[Capítulo 3 - Segurança em IoT]] · [[00 SRC]] | `Bloco 01` |

### Conceitos Relacionados

* [[Modelo de Ameaças em LPWAN - Vetores, Atores e Classificação de Ataques (Stanco)]] · `Bloco 03`
* [[TBL 3 - Segurança em IoT (BLE, LoRaWAN e MQTT)]] · `Bloco 04`
