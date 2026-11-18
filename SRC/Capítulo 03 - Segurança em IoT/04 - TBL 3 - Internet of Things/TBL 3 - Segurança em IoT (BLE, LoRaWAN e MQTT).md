---
title: TBL 3 - Segurança em IoT (BLE, LoRaWAN e MQTT)
tipo: exercicio
mestrado: Cibersegurança e Informática Forense
uc: Segurança em Redes de Computadores
sigla_uc: SRC
capitulo: 3
bloco: 4
fonte_aula: TBL_3_EN_IoT.pdf
tags:
  - src
  - tbl
  - iot
  - ble
  - lorawan
  - mqtt
aliases:
  - TBL 3 SRC
  - TBL IoT
atualizado: 2026-11-15
---

# `TBL #3` — Segurança em IoT (`BLE`, `LoRaWAN` e `MQTT`)

Síntese e fundamentação dos **10 cenários práticos** do `TBL #3` (`TBL_3_EN_IoT.pdf`) aplicados a sensores, `LoRaWAN`, `BLE` e `MQTT`.

---

## Cenários e Decisões Arquiteturais

| # | Cenário / Tecnologia | Decisão Correta e Justificação Técnica |
| :---: | :--- | :--- |
| **1** | Sensor com *firmware* adulterado fisicamente envia leituras falsas mas autenticadas por TLS | **c) Proteger a integridade do *firmware* do dispositivo e cruzar leituras com medições independentes.** *(Cifragem de transporte e assinaturas não impedem um sensor já comprometido de assinar dados falsos).* |
| **2** | `LoRaWAN` com *gateways* externos, `NS` e `AS` | **b) Dados aplicacionais cifrados entre sensores e `AS` (`AppSKey`) e `NS` verifica integridade (`NwkSKey`); porém, um *gateway* comprometido pode ainda descartar ou atrasar mensagens legítimas.** |
| **3** | Sensor `LoRaWAN` `ABP` reinicia e perde o *frame counter* mantendo chaves de sessão | **a) Preservar os *frame counters* entre reinícios ou aprovisionar de forma segura novas chaves de sessão antes de reiniciar os contadores.** *(Reiniciar o contador no `NS` mantendo as chaves permite replay).* |
| **4** | Fechadura `BLE` sem ecrã nem teclado com *LE Secure Connections + Just Works* | **d) Usar emparelhamento `OOB` (*Out-of-Band*) autenticado, como mecanismo `NFC` seguro.** *(Sem ecrã/teclado não há Numeric Comparison nem Passkey Entry).* |
| **5** | Sensor `BLE` atualizado de *LE Legacy* para *LE Secure Connections* mantendo *Just Works* | **b) A escuta passiva durante o emparelhamento torna-se significativamente mais difícil (`ECDH P-256`), mas ataques ativos `MITM` continuam possíveis.** |
| **6** | Sensor de temperatura `MQTT` comprometido usa certificado TLS válido para publicar `STOP` em `factory/pumps/commands` | **b) Impor permissões por dispositivo e por tópico para operações `PUBLISH` e `SUBSCRIBE` (ACLs).** *(Autenticação TLS por si só não impede movimento lateral entre tópicos sem autorização granular).* |
| **7** | Publicador `MQTT` cifra *payloads* fim-a-fim antes de enviar por *broker* de terceiros sobre TLS | **a) O *broker* não consegue ler os valores dos sensores, mas continua a observar nomes dos tópicos e temporização das mensagens.** *(O *broker* precisa dos tópicos para encaminhar mensagens).* |
| **8** | Milhares de sensores agrícolas a bateria com *gateways* externos; proteger comandos e atualizações | **c) Usar mecanismos de segurança leves em cada sensor para autenticar/autorizar comandos sensíveis e verificar atualizações de software, delegando monitorização e gestão intensiva para *gateways* e *cloud*.** |
| **9** | Conta de gestão comprometida envia milhares de pedidos autenticados a sensores de incêndio para esgotar bateria | **c) Impor limites de pedidos por dispositivo nos *gateways* e limitar independentemente operações intensivas nos sensores, sem atrasar alarmes críticos gerados pelos sensores.** |
| **10** | Cidade inteligente: `BLE` (configuração) + `LoRaWAN` (transmissão) + `MQTT` *broker* de terceiros | **d) Emparelhamento `BLE OOB` autenticado; *gateways* `LoRaWAN` sem `AppSKey`; cifragem de *payload* `MQTT` para os subscritores.** |

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Modelo de Ameaças em LPWAN - Vetores, Atores e Classificação de Ataques (Stanco)]] | `Bloco 03` |
| **Seguinte** | [[Capítulo 3 - Segurança em IoT]] · [[00 SRC]] | Fim do capítulo |
| **Índice** | [[Capítulo 3 - Segurança em IoT]] · [[00 SRC]] | `Bloco 04` |

### Conceitos Relacionados

* [[Desafios e Requisitos de Segurança em Arquiteturas IoT (Sharma)]] · `Bloco 01`
* [[Segurança em BLE - Pairing Feature Exchange, LE Legacy e LE Secure Connections (Lacava)]] · `Bloco 02`
* [[LPWAN e Arquitetura LoRaWAN - Entidades, Classes e Chaves (Stanco)]] · `Bloco 03`
