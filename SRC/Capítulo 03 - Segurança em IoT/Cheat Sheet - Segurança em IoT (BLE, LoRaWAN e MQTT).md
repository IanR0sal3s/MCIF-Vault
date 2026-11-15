---
title: Cheat Sheet - Segurança em IoT (BLE, LoRaWAN e MQTT)
tipo: cheatsheet
mestrado: Cibersegurança e Informática Forense
uc: Segurança em Redes de Computadores
sigla_uc: SRC
capitulo: 3
fonte_aula: Sharma_yellow.pdf; Lacava_yellow.pdf; Stanco_yellow.pdf; TBL_3_EN_IoT.pdf
tags:
  - cheatsheet
  - src
  - iot
  - ble
  - lorawan
  - mqtt
aliases:
  - Cheat Sheet Capítulo 3 SRC
  - Cheat Sheet IoT SRC
atualizado: 2026-11-15
---

# Cheat Sheet — Segurança em IoT (`BLE`, `LoRaWAN` e `MQTT`)

Guia de consulta rápida do **[[Capítulo 3 - Segurança em IoT]]** de [[00 SRC|SRC]].

---

## 1. Arquitetura IoT em 5 Camadas (*Sharma*)

| Camada | Protocolos / Tech | Riscos Principais |
| :--- | :--- | :--- |
| **Perception** | `BLE`, `RFID`, `NFC`, `LoRaWAN` | Adulteração física, roubo/clonagem, *side-channel*, exaustão de bateria, falta de CPU |
| **Network** | `6LoWPAN`, `RPL`, `CARP` | *Sinkhole*, *Blackhole* (descarta tudo), *Selective Forwarding* (descarta parte), *Wormhole*, *Flooding* |
| **Processing** | *Cloud*, *Big Data*, `DBMS` | Integridade/consistência, *backup* seguro sem violar tempo real |
| **Application** | `MQTT`, `CoAP`, `XMPP`, `AMQP` | *Code injection*, credenciais por omissão, ACLs em falta, APIs inseguras |
| **Business** | `HTTP`, `FTP` | Conformidade, titularidade de dados, gestão de risco |

---

## 2. `BLE` (*Lacava*): *LE Legacy* vs. *LE Secure Connections*

| Aspeto | *LE Legacy Pairing* (`SC=0` em $\ge 1$ lado) | *LE Secure Connections* (`SC=1` em ambos) |
| :--- | :--- | :--- |
| **Modelos de associação** | `Just Works`, `Passkey Entry`, `OOB` | Adiciona **`Numeric Comparison`** (6 dígitos confirmados em ambos) |
| **Troca / Chaves** | `TK` $\rightarrow$ `STK` (128 bits) $\rightarrow$ distribui `LTK`, `CSRK`, `IRK` | **`ECDH P-256`** $\rightarrow$ `DHKey` $\rightarrow$ `LTK` + `MacKey` (checks $E_a, E_b$) |
| **`Just Works` vs. MITM/Escuta** | Vulnerável a escuta passiva **e** MITM | Escuta passiva muito mais difícil, mas **MITM continua possível** |
| **Sem ecrã nem teclado** | Usar **`OOB` autenticado** (ex.: `NFC`) | Usar **`OOB` autenticado** (ex.: `NFC`) |

---

## 3. `LoRaWAN` (*Stanco*) e `MQTT` (`TBL #3`)

* **`LoRaWAN` Chaves**:
  * **`AppSKey`**: cifra dados aplicacionais (`AES-128`) entre *End Device* $\leftrightarrow$ `AS` (os *gateways* e o `NS` não leem o *payload*).
  * **`NwkSKey`**: calcula `MIC` (`AES-CMAC`) entre *End Device* $\leftrightarrow$ `NS`.
  * **Limitação de *Gateway***: não lê nem forja sem deteção, mas **pode descartar ou atrasar mensagens**.
  * **`ABP` após reinício**: preservar *frame counters* ou aprovisionar novas chaves antes de zerar contadores.
* **`MQTT`**:
  * TLS autentica clientes ao *broker*, mas exige **ACLs por dispositivo e por tópico (`PUBLISH`/`SUBSCRIBE`)** para impedir movimento lateral.
  * Cifragem de *payload* fim-a-fim oculta valores ao *broker*, mas **tópicos e temporização continuam visíveis** ao *broker*.

---

## Navegação

- [[Capítulo 3 - Segurança em IoT|Voltar ao MOC do Capítulo 3]]
- [[00 SRC|Voltar ao MOC Geral de SRC]]
