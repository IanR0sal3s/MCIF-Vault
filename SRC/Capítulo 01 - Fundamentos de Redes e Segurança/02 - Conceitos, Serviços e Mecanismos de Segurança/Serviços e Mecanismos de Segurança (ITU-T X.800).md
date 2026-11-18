---
title: Serviços e Mecanismos de Segurança (ITU-T X.800)
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Segurança em Redes de Computadores
sigla_uc: SRC
capitulo: 1
bloco: 2
fonte_aula: 1_fundamentals.pdf (Slides 22–24); ch1_Computer_Network_Security_Concepts.pdf (Secções 1.4–1.5)
tags:
  - src
  - seguranca
  - x800
  - itu-t
aliases:
  - ITU-T X.800
  - Serviços de Segurança X.800
  - Mecanismos de Segurança X.800
atualizado: 2026-11-15
---

# Serviços e Mecanismos de Segurança (ITU-T X.800)

A recomendação **ITU-T X.800** (*Security Architecture for OSI*) separa os **serviços de segurança** (o que o sistema deve garantir nas comunicações) dos **mecanismos de segurança** (os blocos técnicos usados para implementar esses serviços).

> [!TIP] Lógica de Funcionamento e Valor de Segurança
> * **Porque existe (Arquitetura)**: Permite especificar requisitos de segurança (*serviços*) de forma independente da tecnologia concreta (*mecanismos*), facilitando a interoperabilidade entre sistemas heterogéneos.
> * **Porque importa (Segurança)**: Um mesmo serviço pode exigir múltiplos mecanismos (ex.: confidencialidade de fluxo usa cifragem + *traffic padding* + controlo de encaminhamento), e um mecanismo (como cifragem) pode servir vários serviços.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * A `X.800` distingue **mecanismos específicos** (ligados a uma camada protocolar, como cifragem ou assinatura digital) de **mecanismos pervasivos / transversais** (não específicos de nenhuma camada, como auditoria ou políticas de confiança).
>   * **Autenticação** na `X.800` divide-se em *Peer Entity Authentication* (identidade de entidades numa ligação) e *Data Origin Authentication* (origem dos dados sem ligação contínua).

---

## 1. Serviços de Segurança (`ITU-T X.800`)

| Serviço | Subcategorias / Foco na Aula | Objetivo |
| :--- | :--- | :--- |
| **Confidencialidade de Dados (*Data Confidentiality*)** | Ligação (*Connection*), Sem Ligação, Seletiva, Fluxo de Tráfego (*Traffic*) | Proteger dados contra divulgação não autorizada e ocultar padrões de tráfego. |
| **Integridade de Dados (*Data Integrity*)** | Com/sem recuperação, seletiva, com/sem ligação | Garantir que os dados recebidos são exatamente os enviados, sem alterações em trânsito. |
| **Controlo de Acesso (*Access Control*)** | Recursos (equipamentos e serviços) | Prevenir uso ou acesso não autorizado a recursos. |
| **Autenticação (*Authentication*)** | *Peer Entity Authentication* e *Data Origin Authentication* | Garantir que a entidade comunicante ou a origem dos dados é quem afirma ser. |
| **Não-Repúdio (*Non-repudiation*)** | Origem (*Origin*) e Destino (*Destination*) | Impedir que o remetente negue ter enviado ou que o destinatário negue ter recebido. |
| **Disponibilidade (*Availability Service*)** | Continuidade de serviço | Assegurar que o sistema/rede permanece operacional e acessível a utilizadores autorizados (tratado em `X.800` e `RFC 4949`). |

---

## 2. Mecanismos de Segurança (`ITU-T X.800`)

Os slides e Stallings (Tabela 1.3) agrupam os mecanismos em duas categorias:

### 2.1. Mecanismos Específicos (*Specific Security Mechanisms*)
Implementados numa camada protocolar específica para fornecer um serviço:
* **Cifragem (*Enciphering*)**
* **Assinaturas digitais (*Digital signatures*)**
* **Controlo de acesso (*Access Control*)**
* **Integridade de dados (*Data integrity*)**
* **Troca de autenticação (*Authentication Exchange*)**
* **Preenchimento de tráfego (*Traffic padding*)** — inserção de bits/tráfego fictício para frustrar análise de tráfego
* **Controlo de encaminhamento (*Routing control*)** — escolha de rotas fisicamente seguras ou mudança de rota perante suspeita
* **Certificação / Notarização digital (*Notarization*)** — terceiro de confiança para assegurar propriedades da troca de dados

### 2.2. Mecanismos Pervasivos / Transversais (*Pervasive Security Mechanisms*)
Não estão associados a nenhum serviço ou camada protocolar em particular (nos slides referidos na coluna *Intrusive* / transversais):
* **Políticas de segurança e confiança (*Security and trust policies* / *Trusted functionality*)**
* **Etiquetagem digital de segurança (*Security digital labelling*)**
* **Deteção de eventos relevantes (*Relevant events detection*)**
* **Auditoria de segurança (*Security auditing*)**
* **Procedimentos de recuperação (*Recovery procedures*)**

---

## Perguntas de revisão

1. **Qual a diferença entre *Peer Entity Authentication* e *Data Origin Authentication* na `X.800`?**

> [!success]- Ver Resposta
> *Peer Entity Authentication* verifica a identidade das entidades intervenientes no estabelecimento ou durante uma ligação lógica; *Data Origin Authentication* garante a identidade da origem de uma unidade de dados (ex.: em comunicações sem ligação), sem proteger contra repetição ou modificação por si só.

2. **Para que servem os mecanismos de *Traffic Padding* e *Notarization*?**

> [!success]- Ver Resposta
> *Traffic padding* insere dados fictícios nos intervalos entre transmissões reais para impedir a análise de tráfego (apoiando a confidencialidade de fluxo); *Notarization* recorre a uma terceira entidade de confiança para atestar propriedades como integridade, origem, tempo ou destino de uma comunicação.

## Notas relacionadas

- [[Conceitos Fundamentais de Segurança (CIA, Ameaça, Vulnerabilidade e Ataque)]]
- [[Governação da Internet - IXPs, Infraestrutura Submarina, DNS e RFCs]]
