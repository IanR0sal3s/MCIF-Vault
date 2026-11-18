---
title: Princípios Fundamentais de Desenho Seguro, Attack Surfaces e Attack Trees
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Segurança em Redes de Computadores
sigla_uc: SRC
capitulo: 1
bloco: 2
fonte_aula: 1_fundamentals.pdf (Slides 25–26); ch1_Computer_Network_Security_Concepts.pdf (Secções 1.6–1.7)
tags:
  - src
  - seguranca
  - design-principles
  - attack-surface
  - attack-tree
aliases:
  - Princípios de Saltzer e Schroeder
  - Attack Surface
  - Attack Tree
atualizado: 2026-11-15
---
# Princípios Fundamentais de Desenho Seguro, Attack Surfaces e Attack Trees

A construção de sistemas e redes resilientes assenta em **princípios clássicos de desenho seguro** (*Saltzer & Schroeder*, 1975, e *NCAE*), complementados pela **redução da superfície de ataque** e pela **modelação hierárquica via *attack trees***.

> [!TIP] Lógica de Funcionamento e Valor de Segurança
> * **Porque existe (Engenharia)**: Como é impossível eliminar sistematicamente todas as falhas de implementação, princípios como *fail-safe defaults*, *least privilege* e *open design* reduzem o impacto de erros e facilitam a verificação.
> * **Porque importa (Segurança)**: Combinar **defesa em profundidade** (*layering*) com **redução da superfície de ataque** diminui o risco global; *attack trees* estruturam cenários reais de compromisso (ex.: autenticação bancária) para priorizar contramedidas.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Open design** exige que os **algoritmos sejam públicos/conhecidos**, mantendo apenas as **chaves secretas** (*security through obscurity* viola este princípio).
>   * **Fail-safe defaults** significa que o estado por omissão é **"falta de acesso"** (*lack of access*): um erro de implementação falha de forma segura (negando acesso) em vez de permitir acesso indevido.

---

## 1. Princípios Fundamentais de Desenho Seguro (Slides + Stallings 1.6)

Os oito princípios originais de *Saltzer & Schroeder* (1975) e os cinco princípios adicionais listados pelo NCAE:

| Princípio | Significado (Slides / Stallings) |
| :--- | :--- |
| **1. Economy of mechanism** | Mecanismos "leves" e simples são mais fáceis de testar, verificar e manter com menos falhas. |
| **2. Fail-safe defaults** | Omissão = **"lack of access"**; decisões baseadas em permissão explícita e não em exclusão. |
| **3. Complete mediation** | Verificação contínua de cada acesso; evitar confiar em decisões de acesso em *cache*. |
| **4. Open design** | Algoritmos e desenho abertos ao escrutínio público (ex.: normalização NIST); apenas as chaves são secretas. |
| **5. Separation of privilege** | Exigir múltiplos atributos/condições para acesso restrito (ex.: autenticação multifator) ou separar processos privilegiados. |
| **6. Least privilege** | Conceder apenas os privilégios mínimos necessários para desempenhar uma função (incluindo dimensão temporal). |
| **7. Least common mechanism** | Minimizar funções/mecanismos partilhados entre utilizadores diferentes para reduzir canais indesejados. |
| **8. Psychological acceptability** | Mecanismos não intrusivos e alinhados com o modelo mental do utilizador (evita que os utilizadores os desativem). |
| **9. Isolation** | Isolar sistemas públicos de recursos críticos, processos/ficheiros de utilizadores e mecanismos criptográficos. |
| **10. Encapsulation** | Forma de isolamento orientada a objetos: dados e procedimentos protegidos num domínio com pontos de entrada definidos. |
| **11. Modularity** | Módulos interligados com funções bem definidas (ex.: módulo criptográfico comum reutilizável e atualizável). |
| **12. Layering** | Vários níveis de proteção sobrepostos (físico, lógico, operacional) — **defesa em profundidade**. |
| **13. Least astonishment** | A interface/programa deve responder da forma menos surpreendente e mais intuitiva possível para o utilizador. |

---

## 2. *Attack Surfaces* e *Attack Trees* (Stallings 1.7)

### 2.1. Superfície de Ataque (*Attack Surface*)
Conjunto de vulnerabilidades alcançáveis e exploráveis num sistema (portos abertos, serviços internos a uma firewall, código que processa dados externos, formulários web/SQL, colaboradores). Divide-se em:
* **Network attack surface**: vulnerabilidades em protocolos de rede, `DoS`, ligações e intrusão remota.
* **Software attack surface**: vulnerabilidades em aplicações, utilitários ou sistema operativo (ex.: servidores web).
* **Human attack surface**: vulnerabilidades criadas por pessoas — engenharia social, erro humano, *insiders*.

> A combinação de **Layering (profundidade de defesa)** com **redução da Attack Surface** move o sistema de risco elevado para baixo risco (Figura 1.3 de Stallings).

### 2.2. Árvores de Ataque (*Attack Trees*)
Estrutura hierárquica em árvore que representa técnicas potenciais para explorar vulnerabilidades:
* **Nó raiz**: objetivo final do ataque (ex.: comprometer conta bancária).
* **Nós intermédios**: sub-objetivos do tipo **`AND`** (todos os filhos necessários) ou **`OR`** (basta um filho).
* **Nós folha**: formas iniciais de lançar o ataque (podem ser anotados com custo, dificuldade, etc.).

---

## Perguntas de revisão

1. **Porque é que *Fail-safe defaults* é preferível a uma política de "permitir por omissão e bloquear exceções"?**

> [!success]- Ver Resposta
> Porque, se ocorrer um erro de implementação ou configuração numa política de permissão explícita (*default = lack of access*), a falha tende a recusar acesso (falha segura e rapidamente detetável), ao passo que numa política de exclusão uma falha tende a permitir acesso não autorizado sem ser notada.

2. **Qual a diferença entre um nó `AND` e um nó `OR` numa *Attack Tree*?**

> [!success]- Ver Resposta
> Num nó `AND`, o atacante precisa de concretizar **todos** os sub-objetivos filhos para atingir o objetivo desse nó; num nó `OR`, basta concretizar **pelo menos um** dos sub-objetivos filhos.

## Notas relacionadas

- [[Conceitos Fundamentais de Segurança (CIA, Ameaça, Vulnerabilidade e Ataque)]]
- [[Serviços e Mecanismos de Segurança (ITU-T X.800)]]
