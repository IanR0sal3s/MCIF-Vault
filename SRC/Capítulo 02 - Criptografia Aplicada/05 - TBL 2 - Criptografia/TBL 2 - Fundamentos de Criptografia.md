---
title: TBL 2 - Fundamentos de Criptografia
tipo: exercicio
mestrado: Cibersegurança e Informática Forense
uc: Segurança em Redes de Computadores
sigla_uc: SRC
capitulo: 2
bloco: 5
fonte_aula: TBL_Cryptography_EN_202627.pdf
tags:
  - src
  - tbl
  - criptografia
  - exercicio
aliases:
  - TBL 2 SRC
  - TBL Cryptography
atualizado: 2026-11-15
---

# `TBL #2` — Fundamentos de Criptografia

Mapeamento e fundamentação das **10 questões** do *Team-Based Learning* (`TBL_Cryptography_EN_202627.pdf`) sobre criptografia simétrica, assimétrica, funções de *hash* e `MAC`.

---

## Questões e Fundamentação Técnica

| # | Tópico Avaliado | Opção Correta e Justificação |
| :---: | :--- | :--- |
| **1** | Requisitos para cifragem segura convencional | **b) Deve ser impossível obter o *plaintext* sem a chave, mesmo que o algoritmo seja conhecido.** *(O algoritmo é aberto; a segurança depende exclusivamente da chave — modelo convencional / princípio de open design).* |
| **2** | O que envolve a criptanálise | **d) Análise estatística do *plaintext* e/ou do *ciphertext* correspondente, com o objetivo de descobrir a chave ou o *plaintext*.** |
| **3** | Características desejáveis numa cifra de substituição/permutação | **a) Blocos de dados grandes, chaves grandes e algoritmo difícil de analisar.** *(Aumentam difusão, confusão e resistência a análise estatística/força bruta).* |
| **4** | Identificar o algoritmo que **não** é cifra simétrica de blocos | **b) `RC4`.** *(`RC4` é uma cifra de **stream**; `RC5`, `Feistel` e `AES` são cifras de blocos).* |
| **5** | Vantagens da criptografia assimétrica sobre a simétrica | **d) Permite métodos de autenticação e distribuição segura de chaves.** *(A assimétrica complementa — não substitui — a simétrica).* |
| **6** | Significado de $Y = E(PR_A, X)$ | **b) A autenticação da mensagem é garantida, e a mensagem está cifrada.** *(Apenas $A$ tem $PR_A$, provando autenticidade; qualquer um com $PU_A$ decifra, logo **não** há confidencialidade).* |
| **7** | Melhor forma de fornecer **apenas** autenticação da mensagem | **c) $M + H(M \parallel S)$.** *($M$ segue em claro — sem confidencialidade — e $S$ é um segredo partilhado que autentica o resumo sem cifrar a mensagem).* |
| **8** | Serviços garantidos por $Z = E(PU_B, E(PR_A, X))$ | **b) Autenticação e integridade, com confidencialidade.** *(Assinatura interna com $PR_A$ + cifragem externa com $PU_B$).* |
| **9** | Características de uma função de *hash* | **a) Entrada de tamanho variável, saída de tamanho fixo, e computacionalmente impraticável que duas entradas distintas produzam a mesma saída.** |
| **10** | Melhor opção com `MAC` para garantir confidencialidade de toda a mensagem | **a) $E(K_2, [M \parallel C(K_1, M)])$ ou c) $E(K_2, M) + C(K_1, E(K_2, M))$** *(Ambas cifram $M$ com $K_2$ e autenticam com $K_1$; na opção **a)** cifra-se mensagem+MAC juntos; na **c)** — Encrypt-then-MAC — o MAC protege o texto cifrado e a mensagem fica totalmente cifrada).* |

> [!NOTE] Nota sobre a Questão 10
> A opção **d)** (`E(K2, M) + C(K1, M)`) aplica *Encrypt-and-MAC*, que pode vazar informação sobre `M` através do MAC determinístico; a opção **b)** (`M + C(K, M)`) envia `M` em claro sem confidencialidade. Tanto **a)** (*MAC-then-Encrypt*) como **c)** (*Encrypt-then-MAC*) cifram `M` integralmente, sendo **c)** a construção preferida em protocolos modernos (como TLS/IPSec).

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Redes Privadas Virtuais (VPN) - IPSec e OpenVPN]] | `Bloco 04` |
| **Seguinte** | [[Capítulo 2 - Criptografia Aplicada]] · [[00 SRC]] | Fim do capítulo |
| **Índice** | [[Capítulo 2 - Criptografia Aplicada]] · [[00 SRC]] | `Bloco 05` |

### Conceitos Relacionados

* [[Criptografia Simétrica - Modelo Convencional, Criptanálise e Cifras Clássicas]] · `Bloco 01`
* [[Cifras de Blocos vs. Stream - Feistel, DES, 3DES, AES e RC4]] · `Bloco 01`
* [[Criptografia Assimétrica - Princípios, Diffie-Hellman, ECC e Algoritmo RSA]] · `Bloco 02`
* [[Funções de Hash Criptográficas e Integridade (MD5, SHA-1, SHA-2 e SHA-3)]] · `Comum/`
* [[Autenticação de Mensagens (MAC, HMAC) e Assinaturas Digitais]] · `Bloco 03`
