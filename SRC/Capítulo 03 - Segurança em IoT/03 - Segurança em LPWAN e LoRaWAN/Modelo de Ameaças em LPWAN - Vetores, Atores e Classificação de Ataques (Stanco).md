---
title: Modelo de Ameaças em LPWAN - Vetores, Atores e Classificação de Ataques (Stanco)
tipo: analise
mestrado: Cibersegurança e Informática Forense
uc: Segurança em Redes de Computadores
sigla_uc: SRC
capitulo: 3
bloco: 3
fonte_aula: Stanco_yellow.pdf (Secções 5, 5.1, 5.2, 5.3, 5.4; Fig. 7)
tags:
  - src
  - iot
  - lpwan
  - threat-model
  - lorawan
aliases:
  - Modelo de Ameaças LPWAN
  - Vetores de Ataque LPWAN
atualizado: 2026-11-15
---

# Modelo de Ameaças em `LPWAN` — Vetores, Atores e Classificação de Ataques (*Stanco*)

Uma arquitetura `LPWAN` apresenta uma superfície de ataque distribuída — desde os dispositivos finais no terreno até às aplicações na *cloud* — exigindo a proteção das propriedades **`CIAA`** (*Confidentiality, Integrity, Availability, Authorization*) ao longo de **5 vetores de ataque** principais.

> [!TIP] Lógica de Funcionamento e Valor de Segurança
> * **Porque existe (Modelação)**: Um compromisso num único ponto (ex.: *end device* adulterado ou *gateway* malicioso) pode propagar-se e degradar toda a rede `LPWAN`.
> * **Porque importa (Segurança)**: Permite classificar os incidentes em `LPWAN` em 6 categorias operacionais (`DoS`/bateria, `MITM`, *Replay*, *Wormhole*, *Jamming*, *Physical tampering*) e associá-los aos respetivos pontos de entrada.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Propriedades `CIAA`** (Secção 5.1): *Confidentiality*, *Integrity*, *Availability* e ***Authorization***.
>   * **Drenagem de bateria via rádio**: tanto ataques de *DoS* (acordar dispositivos em *sleep* desnecessariamente) como *Jamming* (forçar o nó a aumentar potência de transmissão por baixa qualidade de canal) esgotam rapidamente a bateria dos nós.

---

## 1. Ativos Críticos e Propriedades `CIAA` (Secção 5.1)

* **Ativos críticos**: *end devices*, *gateways*, infraestrutura de rede, dados em trânsito, servidores (`NS`/`JS`/`AS`), mecanismos de autenticação, *firmware*/software e interfaces de utilizador.
* **Propriedades `CIAA`**:
  1. **Confidencialidade (*Confidentiality*)**: dados acessíveis apenas a utilizadores/dispositivos autorizados.
  2. **Integridade (*Integrity*)**: dados inalterados durante a transmissão.
  3. **Disponibilidade (*Availability*)**: serviços e recursos operacionais quando necessários.
  4. **Autorização (*Authorization*)**: concessão ou restrição de acesso conforme privilégios definidos.

---

## 2. Os 5 Vetores de Ataque na Arquitetura `LPWAN` (Secção 5.2 e Fig. 7)

| Vetor (Fig. 7) | Componente / Ligação Alvo | Impacto Típico |
| :---: | :--- | :--- |
| **1** | ***End devices*** | Adulteração física ou roubo, geração de leituras falsas para provocar disfunções ou atacar outros dispositivos |
| **2** | **Comunicação sem fios (*End device* $\leftrightarrow$ *Gateway*)** | Escuta passiva (*eavesdropping*) e interferência rádio sobre o ar (*over-the-air*) |
| **3** | ***Gateways* / Estações Base comprometidos (*rogue*)** | Descarte seletivo de pacotes, recusa falsa de acesso, escuta ou redirecionamento de tráfego |
| **4** | **Ligação *Backhaul* (*Gateway* $\leftrightarrow$ Servidor LPWAN)** | Atraso de comunicações ou ataques *Man-in-the-Middle* clássicos (escuta/manipulação) |
| **5** | **Plano de Aplicação (*APIs* e interfaces Web)** | Exploração de vulnerabilidades de software/protocolo (ex.: *Cross-Site Scripting* `XSS`, *SQL Injection*) |

---

## 3. Atores de Ameaça (Secção 5.3) e Classificação de Ataques (Secção 5.4)

**4 Perfis de Atores de Ameaça:**
* **Cibercriminosos** (ganho financeiro, roubo de dados/propriedade intelectual, fraude);
* **Concorrentes / rivais comerciais** (vantagem competitiva, sabotagem);
* **Atores patrocinados por Estados (*Nation-state*)** (espionagem, disrupção de infraestruturas críticas);
* **Utilizadores internos (*Insiders*)** (colaboradores/contratados com abuso intencional ou acidental de privilégios).

**6 Categorias de Ataques:**
1. **`DoS` e *Battery Draining***: inundação de tráfego, falsificação de estação base ou ativação forçada de nós em modo *sleep* para esgotar baterias.
2. ***Man-in-the-Middle* (`MITM`)**: interceção rádio, falsificação/*spoofing* de dispositivos ou servidores e adulteração de leituras/comandos.
3. ***Replay***: captura e retransmissão repetida de mensagens legítimas (causando ações duplicadas ou `DoS`).
4. ***Wormhole***: dois nós maliciosos criam um túnel virtual rápido entre si para contornar o encaminhamento normal e descartar/manipular pacotes seletivamente.
5. ***Jamming***: transmissão de sinais rádio potentes na mesma banda, bloqueando comunicações ou forçando os nós a aumentar a potência de emissão (drenando baterias).
6. ***Physical Tampering***: acesso físico não autorizado para extrair segredos de hardware, modificar *firmware*, substituir componentes ou instalar *spyware*.

---

## Perguntas de revisão

1. **Quais são os 5 vetores de ataque identificados no modelo de ameaças `LPWAN` de *Stanco*?**

> [!success]- Ver Resposta
> (1) *End devices* (adulteração/roubo); (2) Comunicação sem fios entre *end devices* e *gateways*; (3) *Gateways*/estações base comprometidos ou *rogue*; (4) Ligação *backhaul* entre *gateways* e servidores LPWAN; e (5) Plano de aplicação (APIs e interfaces web, ex.: XSS/SQLi).

2. **Como pode um ataque de *Jamming* ou de *DoS* afetar a autonomia energética de um nó `LPWAN`?**

> [!success]- Ver Resposta
> No *DoS* dirigido à energia, o atacante acorda repetidamente dispositivos em modo *sleep*; no *Jamming*, o ruído rádio faz o dispositivo percecionar baixa qualidade de canal e aumentar a potência de transmissão, acelerando a descarga da bateria em ambos os casos.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[LPWAN e Arquitetura LoRaWAN - Entidades, Classes e Chaves (Stanco)]] | `mesmo bloco` |
| **Seguinte** | [[TBL 3 - Segurança em IoT (BLE, LoRaWAN e MQTT)]] | `muda para Bloco 04` |
| **Índice** | [[Capítulo 3 - Segurança em IoT]] · [[00 SRC]] | `Bloco 03` |

### Conceitos Relacionados

* [[Ataques e Contramedidas por Camada em IoT (Sharma)]] · `Bloco 01`
