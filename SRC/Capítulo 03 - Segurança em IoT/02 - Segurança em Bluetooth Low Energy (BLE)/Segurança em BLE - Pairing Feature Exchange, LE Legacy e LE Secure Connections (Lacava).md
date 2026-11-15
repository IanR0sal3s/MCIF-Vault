---
title: Segurança em BLE - Pairing Feature Exchange, LE Legacy e LE Secure Connections (Lacava)
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Segurança em Redes de Computadores
sigla_uc: SRC
capitulo: 3
bloco: 2
fonte_aula: Lacava_yellow.pdf (Secções 3, 3.1, 3.2, 3.3)
tags:
  - src
  - iot
  - ble
  - bluetooth
  - pairing
aliases:
  - Segurança BLE
  - LE Legacy Pairing
  - LE Secure Connections
  - Pairing Feature Exchange
atualizado: 2026-11-15
---

# Segurança em BLE — *Pairing Feature Exchange*, *LE Legacy* e *LE Secure Connections* (*Lacava*)

No *Bluetooth Low Energy* (`BLE`), o emparelhamento (*pairing*) estabelece chaves para cifrar a ligação e autenticar dispositivos, distinguindo-se dois métodos principais: ***LE Legacy Pairing*** (baseado em `TK`/`STK`) e ***LE Secure Connections*** (baseado em criptografia de curvas elípticas `ECDH P-256` e `LTK`).

> [!TIP] Lógica de Funcionamento e Valor de Segurança
> * **Porque existe (Protocolo)**: Dispositivos BLE têm capacidades de entrada/saída muito diversas (ecrã, teclado, ou nenhum), pelo que o *Security Manager Protocol* (`SMP`) negocia dinamicamente o método e o modelo de associação adequados.
> * **Porque importa (Segurança)**: O modelo ***Just Works*** **não oferece proteção contra ataques ativos *Man-in-the-Middle* (MITM)** em nenhum dos métodos; contudo, migrar de *LE Legacy* para *LE Secure Connections* (com `ECDH P-256`) torna a **escuta passiva (*passive eavesdropping*) durante o emparelhamento significativamente mais difícil**.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * Se **pelo menos um** dos dispositivos não tiver a flag `SC` (*Secure Connection*) ativa, é escolhido o **`LE Legacy Pairing`**.
>   * No **`LE Legacy Pairing`**, a `TK` (ex.: 6 dígitos no *Passkey Entry* ou `0` no *Just Works*) é usada para derivar a `STK` — logo, se um observador passivo capturar a troca inicial em *Just Works* (entropia 0) ou *Passkey Entry*, pode quebrar a `STK`.
>   * No **`LE Secure Connections`**, introduz-se o modelo **`Numeric Comparison`** (número de 6 dígitos confirmado em ambos os dispositivos) e a chave `LTK` deriva de **`ECDH` na curva `P-256`**, sem que os dados introduzidos pelo utilizador determinem a entropia da chave.

---

## 1. Fase 1 Comum: *Pairing Feature Exchange* (Secção 3.1)

O iniciador envia um **`SMP Pairing Request`** e o respondedor responde com um **`SMP Pairing Response`**, trocando os campos:
* `IO Capability` (capacidades de ecrã/teclado), `SC` (*Secure Connections*), `MitM`, `OOB`, `Maximum Encryption Key Size`, `Initiator Key Distribution` e `Responder Key Distribution`.

Esta troca decide:
1. O método de emparelhamento (**`LE Legacy Pairing`** vs. **`LE Secure Connections`**);
2. Se haverá autenticação e qual o **modelo de associação**;
3. O tamanho da `LTK` e quais as chaves a distribuir (`LTK`, `CSRK`, `IRK`).

---

## 2. *LE Legacy Pairing* (Secção 3.2)

Escolhido quando **qualquer um** dos dispositivos tem `SC = 0`. Processa-se em **3 fases**:
* **Fase 1 (Modelo de associação)**:
  1. **`Just Works`**: sem interação do utilizador (`MitM = 0`, ou sem capacidades de IO para *Passkey* e sem `OOB`). Entropia da `TK` é **0**; **vulnerável a escuta passiva e MITM**.
  2. **`Passkey Entry`**: um dispositivo exibe um número de 6 dígitos e o utilizador introdu-lo manualmente no outro.
  3. **`OOB` (*Out-of-Band*)**: troca de dados por canal externo ao Bluetooth (ex.: NFC, QR code) tipicamente resistente a MITM.
* **Fase 2 (Geração da `STK` e Autenticação)**:
  1. Gera a **`TK`** (*Temporary Key*, 128 bits, preenchida com zeros conforme o modelo);
  2. Autentica ambos os dispositivos provando o conhecimento da `TK`;
  3. Deriva a **`STK`** (*Short Term Key*, 128 bits) para cifrar temporariamente a ligação na Fase 3.
* **Fase 3 (Distribuição de Chaves)**: envia sobre o canal cifrado com `STK` a **`LTK`** (*Long Term Key*), **`CSRK`** (*Connection Signature Resolving Key*), **`IRK`** (*Identity Resolving Key*), além de `EDIV` e `RAND` (identificadores da `LTK`).

---

## 3. *LE Secure Connections* (Secção 3.3)

Usado apenas quando **ambos** os dispositivos suportam e definem `SC = 1`. Também tem **3 fases**:
* **Fase 1**: semelhante ao Legacy, mas **adiciona o modelo `Numeric Comparison`** (um número aleatório de 6 dígitos é exibido em **ambos** os dispositivos e o utilizador confirma se são iguais com *Sim/Não*). O *Passkey Entry* passa a ter duas variantes (inserir 6 dígitos em ambos, ou exibir num e inserir noutro).
* **Fase 2 (`ECDH` na curva `P-256` em 4 passos)**:
  1. **Public Key Exchange**: troca de chaves públicas (`SMP Pairing Public Key PDU`) e validação de que pertencem à mesma curva elíptica;
  2. **Calculate `DHKey`**: cálculo do segredo partilhado $DHKey = P256(SK_A, PK_B) = P256(SK_B, PK_A)$;
  3. **Authentication Stage 1**: depende do modelo escolhido (*Just Works* não vai além da verificação $C_b$; *OOB* combina parte Out-of-Band e In-Band);
  4. **Authentication Stage 2**: cálculo de **`LTK`** e **`MacKey`**, seguido de verificação mútua de valores $E_a$ e $E_b$ (aborta se falhar) e cifragem da ligação diretamente com **`LTK`**.
* **Fase 3**: distribuição de `IRK` e `CSRK` (o endereço Bluetooth do dispositivo passa a identificar a `LTK` na base de dados).

---

## Perguntas de revisão

1. **Se um sensor BLE passar de *LE Legacy Pairing* para *LE Secure Connections* mantendo o modelo *Just Works*, o que melhora e o que continua vulnerável?**

> [!success]- Ver Resposta
> A **escuta passiva (*passive eavesdropping*)** durante o emparelhamento torna-se significativamente mais difícil graças ao acordo de chaves `ECDH` (`P-256`), mas os **ataques ativos *Man-in-the-Middle* (MITM) continuam possíveis**, pois *Just Works* não realiza autenticação do canal/utilizador.

2. **Num dispositivo BLE sem ecrã nem teclado (ex.: fechadura inteligente), qual a melhor forma de prevenir ataques MITM durante o emparelhamento?**

> [!success]- Ver Resposta
> Utilizar emparelhamento **`OOB` (*Out-of-Band*) autenticado** (por exemplo, via `NFC`), uma vez que *Numeric Comparison* e *Passkey Entry* exigem capacidades de ecrã/entrada e *Just Works* não autentica contra MITM.

## Notas relacionadas

- [[Desafios e Requisitos de Segurança em Arquiteturas IoT (Sharma)]]
- [[TBL 3 - Segurança em IoT (BLE, LoRaWAN e MQTT)]]
- [[Criptografia Assimétrica - Princípios, Diffie-Hellman, ECC e Algoritmo RSA]]
