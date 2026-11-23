---
title: IDS - Métricas de Desempenho, Técnicas de Evasão e Desafios (Khraisat)
tipo: analise
mestrado: Cibersegurança e Informática Forense
uc: Segurança em Redes de Computadores
sigla_uc: SRC
capitulo: 4
bloco: 1
fonte_aula: s42400-019-0038-7.pdf (Performance Metrics / Table 6, IDS Evasion Techniques, Challenges, Discussion & Conclusion)
tags:
  - src
  - ids
  - evasao
  - matriz-confusao
  - scada
aliases:
  - Evasão de IDS
  - Matriz de Confusão IDS
  - Desafios IDS
atualizado: 2026-11-15
---

# `IDS` — Métricas de Desempenho, Técnicas de Evasão e Desafios (*Khraisat*)

A eficácia de um `IDS` é avaliada através da **matriz de confusão**, mas a sua operação prática enfrenta **quatro grandes técnicas de evasão** (*Fragmentation*, *Flooding*, *Obfuscation* e *Encryption*) e desafios críticos em sistemas **ICS/SCADA** e na obsolescência de *datasets*.

> [!TIP] Lógica de Funcionamento e Valor de Segurança
> * **Porque existe (Avaliação)**: Medir um `IDS` exige distinguir deteções corretas (`TP`/`TN`) de falsos alarmes (`FP`) e ataques não detetados (`FN`).
> * **Porque importa (Segurança)**: Atacantes exploram desfasamentos entre o `IDS` e o *host* destino (ex.: *timeouts* de fragmentação IP, codificação dupla/Unicode) ou cifram canais (`HTTPS`) para contornar inspeção baseada em conteúdo.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **4 Técnicas de Evasão (p. 17–18)**: *Fragmentation* (*overlap*, *overwrite*, *timeouts*), *Flooding* (sobrecarregar o detetor até falhar), *Obfuscation* (hex/Unicode/UTF-8, dupla codificação) e *Encryption* (`HTTPS` impede inspeção de *payload* $\rightarrow$ motiva uso de características estatísticas de fluxo).
>   * **ICS/SCADA**: sistemas legados muitas vezes sem *patches* (ex.: `Stuxnet`, `Conficker`, `WannaCry`) exigem `IDS` que combinem hardware e software (`HIDS` + `NIDS`) respeitando operação em tempo real.

---

## 1. Métricas de Desempenho e Matriz de Confusão (Tabela 6, p. 11–12)

| Classe Real \ Classe Prevista | **Normal** (Previsto) | **Attack** (Previsto) |
| :--- | :---: | :---: |
| **Normal** (Real) | **True Negative (`TN`)** | **False Positive (`FP`)** — falso alarme |
| **Attack** (Real) | **False Negative (`FN`)** — ataque não detetado | **True Positive (`TP`)** — ataque corretamente detetado |

* **`TPR`** (*True Positive Rate* / *Detection Rate* / *Sensitivity*): proporção de ataques corretamente detetados:
  $$\text{TPR} = \frac{TP}{TP + FN}$$
* **`FPR`** (*False Positive Rate* / *False Alarm Rate*): proporção de tráfego normal incorretamente classificado como ataque:
  $$\text{FPR} = \frac{FP}{FP + TN}$$
* **`FNR`** (*False Negative Rate*): proporção de ataques que escaparam ao detetor:
  $$\text{FNR} = \frac{FN}{FN + TP}$$
* **`Accuracy` (`CR` — *Classification Rate*)**: percentagem global de classificações corretas:
  $$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$$
* **`Precision`** (*Valor Preditivo Positivo*): proporção dos alertas emitidos pelo `IDS` que correspondem efetivamente a ataques reais (essencial quando existe forte desbalanceamento de classes, onde `Accuracy` alta pode mascarar muitos falsos positivos):
  $$\text{Precision} = \frac{TP}{TP + FP}$$
* **Curva `ROC`** (*Receiver Operating Characteristic*): representa `TPR` (eixo $Y$) em função de `FPR` (eixo $X$) para vários limiares de decisão (*cut-off points*). Um classificador perfeito passa pelo canto superior esquerdo (`100%` *sensitivity*, `0%` *FPR*).

---

## 2. Técnicas de Evasão de `IDS` (p. 17–18)

| Técnica | Mecanismo de Evasão | Impacto / Contramedida |
| :--- | :--- | :--- |
| **1. *Fragmentation*** | Divide o pacote malicioso em fragmentos usando ***overlap***, ***overwrite*** ou ***timeouts*** (envio lento para expirar o estado em memória do IDS antes do *host* destino). | Exige que o `NIDS` mantenha estado e remonte fragmentos exatamente como o recetor. |
| **2. *Flooding*** | Inunda o detetor com tráfego (ex.: *spoofing* de `UDP`/`ICMP`) para esgotar recursos e forçar falha do mecanismo de controlo (permitindo passagem de tráfego ou ocultando pacotes maliciosos). | Redimensionamento, filtragem e resistência a congestão. |
| **3. *Obfuscation*** | Altera a representação do código/mensagem mantendo a funcionalidade (ex.: **codificação hexadecimal**, múltiplos formatos **`Unicode/UTF-8`**, **dupla codificação**) para evitar *matches* de assinatura. | O `IDS` deve normalizar e decodificar formatos (hex, Unicode) antes de aplicar assinaturas. |
| **4. *Encryption*** | Cifragem (ex.: `HTTPS`) oculta o conteúdo do pacote, impedindo `SIDS` e `AIDS` baseados em conteúdo de ler o *payload*. | Motiva análise de **características estatísticas de fluxo de rede** (sem depender do conteúdo do pacote). |

---

## 3. Desafios Atuais e Conclusões (p. 18–19)

1. **Desafios em `ICS` / `SCADA`**:
   * Sistemas industriais têm arquiteturas específicas, requisitos de tempo real e frequentemente executam sistemas operativos legados sem atualizações possíveis.
   * Casos históricos citados: **`Stuxnet`** (programa nuclear iraniano), **`Conficker`** (2008), ataque ao sistema de elétricos (2009) e **`WannaCry`** (2017, NHS no Reino Unido).
   * Necessidade de integrar deteção a nível de **hardware e software**, combinando funcionalidades de `HIDS` e `NIDS`.
2. **Robustez contra Evasão**:
   * Expressões regulares em `SIDS` detetam mutações simples (ex.: espaços), mas falham perante técnicas de cifragem e ofuscação avançada.
3. **Limitação dos *Datasets* de Avaliação**:
   * Como o tráfego normal evolui continuamente, *datasets* antigos tornam-se obsoletos; são necessários *datasets* mais recentes e abrangentes (ex.: `CICIDS2017`, `Bot-IoT` de 2018 na Tabela 13) e redução de falsos alarmes em modelos de `ML`.

---

## Perguntas de revisão

1. **Como funciona a evasão por *Fragmentation Timeout* contra um `NIDS`?**

> [!success]- Ver Resposta
> O atacante envia fragmentos do pacote malicioso espaçados por um intervalo superior ao tempo durante o qual o `NIDS` retém o estado da ligação em memória, mas inferior ao *timeout* do *host* destino; assim, o `NIDS` descarta os fragmentos sem remontar o ataque, enquanto o destino remonta e executa o pacote completo.

2. **Que abordagem permite a um `NIDS` detetar atividade maliciosa quando o tráfego está cifrado com `HTTPS`?**

> [!success]- Ver Resposta
> O recurso a **características estatísticas dos fluxos de rede** (temporização, dimensão, ritmo), que não dependem da inspeção do conteúdo cifrado dos pacotes, ou a combinação com `HIDS` nos *endpoints*.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[IDS - Taxonomia (SIDS, AIDS, Híbridos) e Posicionamento (HIDS vs. NIDS) (Khraisat)]] | `mesmo bloco` |
| **Seguinte** | [[Zero Trust Architecture (NIST SP 800-207) - Fundamentos, Componentes Lógicos e Planos]] | `muda para Bloco 02` |
| **Índice** | [[Capítulo 4 - Deteção de Intrusões e Zero Trust]] · [[00 SRC]] | `Bloco 01` |

### Conceitos Relacionados

* [[Modelo TCP-IP, Encapsulamento e Visibilidade de Tráfego HTTPS]] · `Cap. 1`
