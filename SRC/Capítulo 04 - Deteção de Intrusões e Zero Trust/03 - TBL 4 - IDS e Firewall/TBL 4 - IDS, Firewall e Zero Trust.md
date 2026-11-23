---
title: TBL 4 - IDS, Firewall e Zero Trust
tipo: exercicio
mestrado: Cibersegurança e Informática Forense
uc: Segurança em Redes de Computadores
sigla_uc: SRC
capitulo: 4
bloco: 3
fonte_aula: MCIF #4 IDS & Firewall (EN)
tags:
  - src
  - tbl
  - ids
  - firewall
  - zero-trust
  - microsegmentacao
aliases:
  - TBL 4 SRC
  - TBL IDS e Firewall
  - MCIF #4 IDS & Firewall
atualizado: 2026-11-23
---

# `TBL #4` — `IDS`, *Firewall* e *Zero Trust*

Síntese e fundamentação das **9 questões** do `TBL #4` (`MCIF #4 IDS & Firewall (EN)`) sobre sistemas de deteção de intrusões (`SIDS`/`AIDS`, `HIDS`/`NIDS`, métricas, evasão por fragmentação), microsegmentação e *Zero Trust Architecture* (`NIST SP 800-207`).

---

## Cenários e Respostas Fundamentadas

| # | Tema / Cenário | Resposta Correta e Justificação Técnica |
| :---: | :--- | :--- |
| **1** | Compromisso (*trade-off*) principal entre `SIDS` (*signature-based*) e `AIDS` (*anomaly-based*) | **B) A deteção baseada em anomalias (`AIDS`) identifica desvios associados a ataques desconhecidos (*zero-day*), mas distinguir comportamento malicioso de alterações legítimas pode aumentar os falsos positivos (`FP`).** |
| **2** | Comparação entre `HIDS` e `NIDS` | **C) `HIDS` e `NIDS` fornecem informação complementar: a atividade no *host* revela processos e acesso a ficheiros (inclusive após decifragem), enquanto a monitorização de rede revela padrões de comunicação e metadados de tráfego.** *(Um `NIDS` não lê *payload* cifrado sem chaves, mas continua a poder usar metadados/estatísticas de fluxo em `HTTPS`).* |
| **3** | `IDS` processa `10 000` eventos (`100` ataques): deteta `80` ataques (`TP=80`, `FN=20`) e gera `200` falsos positivos (`FP=200`, `TN=9700`). Qual a **Precision**? | **C) `28.6%`.** $$\text{Precision} = \frac{TP}{TP + FP} = \frac{80}{80 + 200} = \frac{80}{280} \approx 28.6\%$$ *(Armadilhas: `80%` é Recall/`TPR`; `97.8%` é `Accuracy` enganadora por desbalanceamento de classes; `2.0%` é `FPR`).* |
| **4** | Fraqueza técnica explorada na evasão de `NIDS` por **fragmentação de pacotes** | **D) Diferenças na forma como o `IDS` e o *host* de destino remontam ou interpretam fragmentos podem fazer com que o `IDS` não detete conteúdo malicioso que acaba processado pelo destino** (*overlap*, *overwrite*, *timeouts*). |
| **5** | Princípio fundamental de *Zero Trust* (`NIST SP 800-207`) | **A) O acesso a recursos empresariais deve ser autorizado através de políticas explícitas, sem conceder confiança implícita baseada apenas na localização na rede ou propriedade do dispositivo.** |
| **6** | Relação entre `PE`, `PA` e `PEP` numa `ZTA` | **C) O `PE` (*Policy Engine*) toma decisões de acesso, o `PA` (*Policy Administrator*) estabelece ou termina caminhos de comunicação autorizados e o `PEP` (*Policy Enforcement Point*) impõe o acesso aos recursos protegidos.** |
| **7** | Desenho de política de *firewall* para **microsegmentação** (limitar movimento lateral entre servidores aplicacionais mantendo acesso a BDs/serviços necessários) | **B) Definir políticas de comunicação granulares entre *workloads*, permitindo explicitamente os serviços necessários (*least privilege*) e negando ligações desnecessárias (*default deny*).** |
| **8** | Mapeamento das 3 abordagens de implementação `ZTA` (`NIST SP 800-207`, Secção 3.1) | **D) *Enhanced Identity Governance* $\to$ decisões de acesso baseadas em identidade e atributos; *Microsegmentation* $\to$ isolamento de recursos ou grupos de recursos; *Network Infrastructure / SDP* $\to$ caminhos controlados de acesso de rede aos recursos.** |
| **9** | Como devem alertas de `IDS` influenciar decisões de controlo de acesso em `ZTA`? | **C) Alertas de `IDS` podem contribuir para a avaliação dinâmica de risco (no `PE`), podendo acionar verificação adicional (reautenticação), restrições de acesso ou terminação de sessão conforme a política de segurança.** *(Nem terminam cegamente qualquer anomalia devido a falsos positivos, nem são ignorados em sessões ativas).* |

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Zero Trust Architecture (NIST SP 800-207) - Fundamentos, Componentes Lógicos e Planos]] | `Bloco 02` |
| **Seguinte** | [[Capítulo 4 - Deteção de Intrusões e Zero Trust]] · [[00 SRC]] | Fim do capítulo |
| **Índice** | [[Capítulo 4 - Deteção de Intrusões e Zero Trust]] · [[00 SRC]] | `Bloco 03` |

### Conceitos Relacionados

* [[IDS - Taxonomia (SIDS, AIDS, Híbridos) e Posicionamento (HIDS vs. NIDS) (Khraisat)]] · `Bloco 01`
* [[IDS - Métricas de Desempenho, Técnicas de Evasão e Desafios (Khraisat)]] · `Bloco 01`
* [[Cheat Sheet e Questionário - IDS e Zero Trust Architecture]] · `Cap. 4`
