---
title: 00 Comum
tipo: indice
mestrado: Cibersegurança e Informática Forense
uc: Transversal (AFD1, ASSI, COD1, SRC)
sigla_uc: COMUM
tags:
  - moc
  - comum
  - fundamentos
  - transversais
aliases:
  - Fundamentos Comuns
  - Núcleo Comum MCIF
atualizado: 2026-11-18
---

# Núcleo Comum — Conceitos Transversais entre UCs

Índice central dos **nós de conhecimento partilhados** entre `AFD1`, `ASSI`, `COD1` e `SRC`, desenhado para eliminar redundância teórica e evidenciar ligações transversais no *Graph View* do Obsidian.

> [!NOTE] Estrutura de cada nota em `Comum/`
> Cada nota começa pelo **fundamento técnico único** e termina com uma secção **`## Aplicação por UC`** dedicada ao ângulo específico de exame de cada Unidade Curricular.

---

## Mapa dos Conceitos Partilhados

| Tema Transversal | UCs Ligadas | Foco Principal e Aplicações |
| :--- | :--- | :--- |
| [[Arquitetura SSD e Memória NAND (Wear Leveling e Garbage Collection)]] | `AFD1`, `ASSI` | Páginas/blocos `NAND`, `FTL`, *Wear Leveling*, *Garbage Collection*, desafios de *carving* (`AFD1`) e sanitização segura (`ASSI`). |
| [[Timestamps e Épocas Temporais (UNIX Epoch vs. Windows FILETIME)]] | `AFD1`, `ASSI` | *UNIX Epoch* (`1970`), `FILETIME` (`1601`), constante `11644473600`, *queries* SQLite (`AFD1`) e `SYSTEMTIME` / `w32tm` (`ASSI`). |
| [[Conceitos Fundamentais de Segurança (CIA, Ameaça, Vulnerabilidade e Ataque)]] | `COD1`, `SRC` | Tríade `CIA`, cadeia de risco, taxonomia `RFC 4949` (`SRC`) e vetores de ataque / *Ethical Hacking* (`COD1`). |
| [[Gestão de Vulnerabilidades, CVE e Sistemas de Pontuação (CVSS e CWE)]] | `ASSI`, `COD1` | Identificadores `CVE`, escala `CVSS` (`v3`/`v4`), `SCAP` e `CWE Top 10` (`ASSI`), avaliação em *pentesting* (`COD1`). |
| [[Funções de Hash Criptográficas e Integridade (MD5, SHA-1, SHA-2 e SHA-3)]] | `SRC`, `AFD1`, `ASSI` | Resistência a colisões e algoritmos (`SRC`), cadeia de custódia (`AFD1`), armazenamento de passwords e *IOCs* (`ASSI`). |
| [[Assinaturas Digitais, PKI e GnuPG]] | `SRC`, `AFD1`, `ASSI` | Certificados `X.509`, `CA` com `OpenSSL` e `GnuPG` (`SRC`), assinatura de *hashes* forenses (`AFD1`), `Secure Boot` e código assinado (`ASSI`). |

---

## Navegação

- [[Home]]
- [[00 AFD1]] | [[00 ASSI]] | [[00 COD1]] | [[00 SRC]]
