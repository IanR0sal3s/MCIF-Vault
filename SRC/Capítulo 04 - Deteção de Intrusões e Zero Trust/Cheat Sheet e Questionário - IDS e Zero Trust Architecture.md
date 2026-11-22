---
title: Cheat Sheet e Questionário - IDS e Zero Trust Architecture
tipo: cheatsheet
mestrado: Cibersegurança e Informática Forense
uc: Segurança em Redes de Computadores
sigla_uc: SRC
capitulo: 4
fonte_aula: s42400-019-0038-7.pdf; NIST.SP.800-207.pdf
tags:
  - cheatsheet
  - exercicio
  - src
  - ids
  - zero-trust
  - zta
  - nist
aliases:
  - Cheat Sheet Capítulo 4 SRC
  - Questionário Capítulo 4 SRC
  - Revisão IDS e Zero Trust
atualizado: 2026-11-22
---

# Cheat Sheet e Questionário — `IDS` e *Zero Trust Architecture* (`ZTA`)

Folha de consulta rápida e questionário de cenários (estilo TBL) do **[[Capítulo 4 - Deteção de Intrusões e Zero Trust]]** de [[00 SRC|SRC]].

---

## Parte 1 — Cheat Sheet Rápida

### 1.1. `IDS` (*Khraisat et al., 2019*)

| Eixo | Comparação Crítica | Pontos de Exame |
| :--- | :--- | :--- |
| **Metodologia** | **`SIDS`** (assinaturas, baixos `FP`, **não deteta *zero-day***) vs. **`AIDS`** (anomalias, **deteta *zero-day***, altos `FP`, não lê cifrados) vs. **Híbrido** (`SIDS + AIDS`) | Híbridos combinam precisão do `SIDS` com deteção de desconhecidos do `AIDS`. |
| **Posicionamento** | **`HIDS`** (*logs*, APIs, *system calls*; **analisa após decifragem fim-a-fim** e *insiders*, mas consome recursos do *host*) vs. **`NIDS`** (pacotes, `SNMP`, `NetFlow`; monitoriza vários *hosts* sem agente, mas **falha em *payload* cifrado**) | Combinar `HIDS + NIDS` é essencial sobretudo em ambientes **ICS/SCADA**. |
| **Métricas** | $\text{TPR}=\frac{TP}{TP+FN}$ · $\text{FPR}=\frac{FP}{FP+TN}$ · $\text{FNR}=\frac{FN}{FN+TP}$ · $\text{Acc}=\frac{TP+TN}{TP+TN+FP+FN}$ | **Curva `ROC`**: `TPR` ($Y$) vs. `FPR` ($X$); ideal = canto superior esquerdo (`100%` TPR, `0%` FPR). |
| **4 Evasões** | **1. *Fragmentation*** (*overlap*, *overwrite*, *timeouts*) · **2. *Flooding*** · **3. *Obfuscation*** (hex, Unicode/UTF-8, dupla codificação) · **4. *Encryption*** (`HTTPS`) | Contra `HTTPS`, o `NIDS` recorre a **características estatísticas de fluxo** (ou `HIDS`). |

### 1.2. *Zero Trust Architecture* (`NIST SP 800-207`)

* **Premissa:** nunca conceder confiança implícita pela localização na rede; encolher a **zona de confiança implícita** ao mínimo possível aproximando `PDP`/`PEP` do recurso.
* **Componentes Lógicos:**
  * **`PE` (*Policy Engine*)**: toma e regista a decisão (*trust algorithm* + fontes `CDM`, `PKI`, `ID Mgmt`, `SIEM`, *Threat Intel*, *Logs*, políticas).
  * **`PA` (*Policy Administrator*)**: executa a decisão, gera credenciais de sessão e comanda o `PEP` no *Control Plane*.
  * **`PEP` (*Policy Enforcement Point*)**: único ponto de passagem no *Data Plane* (ativa, monitoriza e termina ligações).
* **Separação de Planos:** ***Control Plane*** (`PE` $\leftrightarrow$ `PA` $\leftrightarrow$ `PEP`, inacessível a ativos comuns) vs. ***Data Plane*** (tráfego aplicacional só após autorização; sem recurso alcançável fora do `PEP`; nunca identificar ativos por endereço `MAC`).
* **7 Tenets (Secção 2.1):** (1) tudo é recurso; (2) toda comunicação protegida independentemente da rede; (3) acesso *per-session* e menor privilégio; (4) política dinâmica baseada em identidade/estado/comportamento; (5) monitorização contínua de integridade/postura (`CDM`); (6) autenticação/autorização dinâmicas antes e durante o acesso (`ICAM`/`MFA`); (7) recolha máxima de telemetria para melhoria contínua.

---

## Parte 2 — Questionário de Cenários (Estilo TBL)

### 1. `NIDS` perante Tráfego `HTTPS`
Uma organização usa apenas um `NIDS` baseado em assinaturas (`SIDS`) no perímetro. Um atacante estabelece um canal C2 totalmente cifrado sobre `HTTPS`. Qual a limitação principal e a melhor resposta arquitetural?
* **A)** O `SIDS` lê automaticamente o *payload* `HTTPS` sem chaves desde que esteja em modo promíscuo.
* **B)** Basta atualizar a base de assinaturas do `SIDS` para decifrar ligações `TLS 1.3`.
* **C)** O `NIDS` baseado em conteúdo não consegue inspecionar o *payload* cifrado; deve combinar-se análise de características estatísticas de fluxo no `NIDS` com `HIDS` nos *endpoints* (que observa eventos após decifragem).
* **D)** Desativar `HTTPS` na rede corporativa para restaurar a eficácia das regras do `SIDS`.

### 2. `SIDS` vs. `AIDS` face a um Ataque *Zero-Day*
Um novo *exploit* nunca visto antes atinge um servidor interno. Que comportamento é esperado de um `SIDS` puro vs. um `AIDS`?
* **A)** O `SIDS` tende a falhar por ausência de assinatura prévia (`FN`), enquanto o `AIDS` tem capacidade para detetar o desvio face ao comportamento normal (embora sujeito a maior taxa de falsos positivos `FP`).
* **B)** O `SIDS` deteta imediatamente com zero falsos positivos; o `AIDS` não consegue detetar ataques desconhecidos.
* **C)** Ambos detetam exclusivamente ataques cuja assinatura esteja registada no `Snort`.
* **D)** Nenhum dos dois consegue monitorizar tráfego em redes baseadas na pilha TCP/IP.

### 3. Evasão por *Fragmentation Timeout*
Como consegue um atacante contornar um `NIDS` usando *fragmentation timeout*?
* **A)** Enviando um único pacote `HTTPS` de 10 MB sem fragmentação IP.
* **B)** Codificando a URL do pedido HTTP em dupla codificação UTF-8.
* **C)** Inundando o `NIDS` com pacotes `ICMP` até esgotar o CPU e reiniciar o servidor.
* **D)** Enviando fragmentos espaçados por um intervalo superior ao *timeout* de memória do `NIDS`, mas inferior ao *timeout* de remontagem do *host* destino — o `NIDS` descarta o estado enquanto o destino remonta o ataque.

### 4. Interpretação da Curva `ROC`
Numa avaliação comparativa de dois `IDS` através da curva `ROC` (`FPR` no eixo $X$, `TPR` no eixo $Y$), o que indica um ponto próximo do canto superior esquerdo (`FPR ≈ 0`, `TPR ≈ 1`)?
* **A)** O `IDS` gera muitos falsos alarmes e falha a deteção da maioria dos ataques.
* **B)** Elevada taxa de deteção de ataques reais (`TPR` alta) com taxa muito baixa de falsos alarmes (`FPR` baixa) — discriminação próxima da ideal.
* **C)** Que o `IDS` só opera em modo *offline* sobre capturas gravadas.
* **D)** Que o número de falsos negativos (`FN`) é igual ao de verdadeiros positivos (`TP`).

### 5. `PE` vs. `PA` vs. `PEP` no `NIST SP 800-207`
Qual componente lógico da `ZTA` gera credenciais/tokens específicos de sessão e instrui o *gateway* a abrir ou fechar o caminho de comunicação após a decisão tomada?
* **A)** `Policy Engine` (`PE`)
* **B)** `Policy Administrator` (`PA`)
* **C)** `Policy Enforcement Point` (`PEP`)
* **D)** `Continuous Diagnostics and Mitigation` (`CDM`)

### 6. Separação *Control Plane* vs. *Data Plane*
Numa implementação `ZTA` conforme a Secção 3.4 do `NIST SP 800-207`, qual prática **viola** os requisitos de rede?
* **A)** Impedir que ativos no *Data Plane* acedam diretamente ao `PE` e ao `PA`.
* **B)** Recolher metadados de todo o tráfego do *Data Plane* para alimentar o `PE`.
* **C)** Permitir que trabalhadores remotos acedam diretamente a serviços `SaaS` via `PEP` sem passar primeiro por uma `VPN` corporativa.
* **D)** Confiar no endereço `MAC` da placa de rede para distinguir ativos geridos pela empresa e permitir acesso direto a um servidor interno sem passar por um `PEP`.

### 7. *Implicit Trust Zone* e Perímetro Tradicional
Porque falha o modelo de segurança baseado em perímetro tradicional face aos 7 *Tenets* do *Zero Trust*?
* **A)** Porque o perímetro tradicional assume confiança implícita dentro da rede interna, permitindo movimento lateral após um único compromisso e não cobrindo adequadamente trabalho remoto ou *cloud*.
* **B)** Porque o *Zero Trust* proíbe a utilização de `PKI` e autenticação multifator (`MFA`).
* **C)** Porque o *Zero Trust* exige uma única zona de confiança alargada para toda a organização.
* **D)** Porque o perímetro tradicional só funciona em redes industriais `LoRaWAN`.

### 8. `ICS` / `SCADA` e `IDS`
Segundo *Khraisat et al.*, porque exigem sistemas `ICS`/`SCADA` uma abordagem cuidadosa de `IDS`?
* **A)** Porque executam sempre a versão mais recente do Windows 11 com *patches* automáticos diários.
* **B)** Porque não comunicam por rede nem geram registos de atividade analisáveis.
* **C)** Porque têm requisitos estritos de tempo real e sistemas operativos legados muitas vezes sem *patches* possíveis (ex.: `Stuxnet`, `WannaCry`), exigindo combinar `HIDS` e `NIDS` em hardware e software sem perturbar a operação.
* **D)** Porque os *datasets* de 1998 (`KDD99`) representam perfeitamente o tráfego industrial contemporâneo.

---

## Gabarito Comentado

| # | Opção | Referência |
| :---: | :---: | :--- |
| **1** | **C** | [[IDS - Taxonomia (SIDS, AIDS, Híbridos) e Posicionamento (HIDS vs. NIDS) (Khraisat)]] · [[IDS - Métricas de Desempenho, Técnicas de Evasão e Desafios (Khraisat)]] |
| **2** | **A** | [[IDS - Taxonomia (SIDS, AIDS, Híbridos) e Posicionamento (HIDS vs. NIDS) (Khraisat)]] |
| **3** | **D** | [[IDS - Métricas de Desempenho, Técnicas de Evasão e Desafios (Khraisat)]] |
| **4** | **B** | [[IDS - Métricas de Desempenho, Técnicas de Evasão e Desafios (Khraisat)]] |
| **5** | **B** | [[Zero Trust Architecture (NIST SP 800-207) - Fundamentos, Componentes Lógicos e Planos]] |
| **6** | **D** | [[Zero Trust Architecture (NIST SP 800-207) - Fundamentos, Componentes Lógicos e Planos]] |
| **7** | **A** | [[Zero Trust Architecture (NIST SP 800-207) - Fundamentos, Componentes Lógicos e Planos]] |
| **8** | **C** | [[IDS - Métricas de Desempenho, Técnicas de Evasão e Desafios (Khraisat)]] |

---

## Navegação

- [[Capítulo 4 - Deteção de Intrusões e Zero Trust|Voltar ao MOC do Capítulo 4]]
- [[00 SRC|Voltar ao MOC Geral de SRC]]
