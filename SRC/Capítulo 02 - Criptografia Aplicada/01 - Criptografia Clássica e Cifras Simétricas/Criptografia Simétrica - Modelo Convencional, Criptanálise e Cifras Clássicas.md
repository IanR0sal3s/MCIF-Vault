---
title: Criptografia Simétrica - Modelo Convencional, Criptanálise e Cifras Clássicas
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Segurança em Redes de Computadores
sigla_uc: SRC
capitulo: 2
bloco: 1
fonte_aula: aula_02_update.pdf (Slides 3–13); aula02_leituras_resumo.pdf (Stallings Cap. 3)
tags:
  - src
  - criptografia
  - criptanalise
  - cifras-classicas
aliases:
  - Modelo Convencional
  - Cifra de César
  - Cifras Monoalfabéticas
  - Criptanálise
atualizado: 2026-11-15
---

# Criptografia Simétrica — Modelo Convencional, Criptanálise e Cifras Clássicas

A criptologia divide-se em **criptografia** (construção de sistemas de cifragem e decifragem) e **criptanálise** (estudo de técnicas para decifrar mensagens sem conhecimento da chave ou dos detalhes secretos da cifra).

> [!TIP] Lógica de Funcionamento e Valor de Segurança
> * **Porque existe (Fundamento)**: O modelo convencional estabelece que a segurança de uma cifra não deve depender do segredo do algoritmo (que deve ser aberto), mas exclusivamente da **chave secreta** partilhada entre emissor e recetor.
> * **Porque importa (Segurança)**: As cifras clássicas ilustram porque um espaço de chaves grande por si só não chega: cifras monoalfabéticas têm $26! > 4 \times 10^{26}$ chaves, mas são facilmente quebradas por **análise de frequência** de letras e digramas/trigramas.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Força bruta** testa todas as chaves possíveis; **criptanálise** explora propriedades matemáticas/estatísticas do algoritmo e do texto cifrado/claro.
>   * **Requisitos de segurança computacional**: o custo para quebrar a cifra deve exceder o valor da informação, e o tempo necessário deve exceder a vida útil da informação.

---

## 1. Modelo Convencional e Requisitos

Num sistema de cifragem simétrica (convencional), intervêm cinco elementos:
1. **Mensagem original (*plaintext*)**: dados legíveis de entrada.
2. **Algoritmo de encriptação**: substituições e transformações aplicadas ao *plaintext*.
3. **Chave secreta**: *input* independente da mensagem e do algoritmo, partilhado por canal seguro entre os *peers*.
4. **Mensagem codificada (*ciphertext*)**: saída cifrada.
5. **Algoritmo de desencriptação**: inverso do algoritmo de encriptação usando a mesma chave.

**Requisitos da criptografia convencional (Slide 6 / Stallings):**
* Algoritmo forte e **aberto** (a segurança depende apenas da chave e não do desconhecimento do algoritmo);
* Computacionalmente impraticável (em custo e tempo) obter o *plaintext* sem a chave;
* Canal seguro para a troca da chave secreta entre os *peers*.

---

## 2. Cifras Clássicas: Substituição, Transposição e Rotores

| Técnica | Mecanismo | Fragilidade Principal |
| :--- | :--- | :--- |
| **Cifra de César** | Substitui cada letra pela 3.ª seguinte (generalizável a deslocamento $n$) | Apenas **26 chaves**; ataque trivial por força bruta e contexto linguístico |
| **Cifras Monoalfabéticas** | Permutação arbitrária de um único alfabeto ($26! > 4 \times 10^{26}$ chaves) | Preserva frequências estatísticas da língua; quebrável por **análise de frequência** (di/tri/*n*-gramas) |
| **Cifras Polialfabéticas** | Múltiplos alfabetos de substituição (ex.: *Vigenère*, *Vernam*) | Reduz assinatura de frequência simples (embora *Vigenère* seja atacável por período) |
| **Transposição** | Permuta a posição dos caracteres sem os substituir (*rail fence*, diagonal, retangular/colunas) | Preserva a frequência exata das letras originais; exige múltiplas permutações |
| **Máquinas de Rotores** | Cilindros rotativos ligados em série que alteram a substituição a cada letra (*Enigma*, *Purple*) | Precursora do DES; quebrada historicamente pela *Bombe* (Alan Turing) e *Colossus* |

---

## Perguntas de revisão

1. **Porque é que uma cifra monoalfabética é vulnerável mesmo possuindo mais de $4 \times 10^{26}$ chaves possíveis?**

> [!success]- Ver Resposta
> Porque utiliza apenas um alfabeto de substituição fixo, preservando a distribuição estatística das letras, digramas e trigramas da língua original, o que permite a criptanálise por análise de frequência sem testar todas as chaves.

2. **Segundo o modelo convencional, o algoritmo de cifragem deve ser mantido secreto?**

> [!success]- Ver Resposta
> Não. O algoritmo deve ser aberto ao escrutínio; a segurança deve depender exclusivamente da confidencialidade da chave secreta partilhada entre emissor e recetor.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Capítulo 2 - Criptografia Aplicada]] | Início do capítulo |
| **Seguinte** | [[Cifras de Blocos vs. Stream - Feistel, DES, 3DES, AES e RC4]] | `mesmo bloco` |
| **Índice** | [[Capítulo 2 - Criptografia Aplicada]] · [[00 SRC]] | `Bloco 01` |

### Conceitos Relacionados

* [[Princípios Fundamentais de Desenho Seguro, Attack Surfaces e Attack Trees]] · `Cap. 1`
