---
title: Segurança de Passwords, Paradigma xkcd e Diretrizes NIST (2003 vs SP 800-63-4)
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 2
bloco: 5
fonte_aula: System Administration - Access Control.pdf
fontes:
  - "https://xkcd.com/936/"
  - "https://haveibeenpwned.com"
  - "https://haveibeenpwned.com/Passwords"
  - "https://pages.nist.gov/800-63-4/sp800-63b.html"
  - "https://www.wired.com/story/7-steps-to-password-perfection/"
tags:
  - assi
  - administracao-sistemas
  - controlo-acessos
  - passwords
  - nist-sp-800-63-4
  - xkcd
  - haveibeenpwned
  - ihg-hack
aliases:
  - Diretrizes NIST SP 800-63-4
  - NIST 2003 Bill Burr
  - Paradigma xkcd 936
  - 7 Steps to Password Perfection
  - Caso IHG Hack
atualizado: 2026-11-11
---

# Segurança de Passwords, Paradigma `xkcd` e Diretrizes NIST (2003 vs. `SP 800-63-4`)

As palavras-passe sofrem com escolhas humanas previsíveis e regras antigas de complexidade; as diretrizes `NIST SP 800-63-4` e o paradigma `xkcd` privilegiam comprimento elevado e abolem rotações periódicas.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema / Ameaça)**: Como fator único baseado em *"algo que sabe"*, a palavra-passe sofre de duas fragilidades: escolhas humanas previsíveis (ex.: `123456`, `Qwerty1234`) e políticas obsoletas (NIST 2003) que forçavam substituições artificiais e alterações a cada 90 dias.
> * **Porque importa (Segurança / Forense)**: As recomendações modernas (`NIST SP 800-63-4`) maximizam a entropia real através do comprimento ($\ge 15$ caracteres até $64$), validam senhas contra fugas conhecidas (`Pwned Passwords`) e evitam o desgaste cognitivo que induz padrões incrementais.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **`xkcd #936`**: `Tr0ub4dor&3` tem apenas **`~28 bits`** (~3 dias a 1000 tentativas/s), enquanto `correct horse battery staple` ($4 \times 11$ bits) atinge **`44 bits`** (~550 anos a 1000 tentativas/s).
>   * **NIST 2003 (Bill Burr) vs. `NIST SP 800-63-4` (2024)**: as novas diretrizes baseiam-se em fugas reais, **proíbem alterações periódicas obrigatórias** (salvo violação de dados ou *credential stuffing*), exigem mínimo `8` (idealmente **`>= 15`** até **`64`** caracteres) e permitem **espaços ASCII e Unicode**.
>   * **IHG Hack**: cofre corporativo comprometido por *ransomware* LockBit devido à password **`Qwerty1234`**.

---

## 1. Fragilidade das Passwords Escolhidas por Humanos e Caso *IHG Hack* (Slides 25–30)

* **Autenticação de Fator Único (*Single-Factor Authentication*)**: as palavras-passe baseiam-se exclusivamente em **"algo que sabe" (*"something you know"*)**, razão pela qual devem ser reforçadas sempre que possível por autenticação a dois fatores (2FA).
* **O Paradoxo da Aleatoriedade**: uma password ideal deve ser aleatória e longa (ex.: `2ab919e8d28bcbc74be0598358c2183f` com 32 caracteres), mas o cérebro humano memoriza mal sequências sem significado.
* **As 10 Passwords Mais Comuns de 2021 (Slide 28)**:
  1. `123456` (a palavra-passe mais utilizada no mundo — Slide 26)
  2. `123456789`
  3. `qwerty`
  4. `password`
  5. `1234567`
  6. `12345678`
  7. `12345`
  8. `Iloveyou`
  9. `111111`
  10. `123123`
* **Caso Real — *IHG Hack* (*InterContinental Hotels Group*, Slide 30)**: atacantes comprometeram os sistemas internos do grupo hoteleiro cotado no FTSE 100 e executaram *ransomware* (**LockBit**) após acederem ao cofre corporativo protegido por uma password trivial: **`Qwerty1234`**.

---

## 2. O Paradigma `xkcd #936` e Verificação em `haveibeenpwned.com` (Slides 31, 33–35)

### 2.1. Comprimento vs. Complexidade Artificial (`xkcd #936` — Slide 31)
A banda desenhada de Randall Munroe ([xkcd #936 — Password Strength](https://xkcd.com/936/)) ilustra a falha das regras clássicas de substituição de caracteres:

* **`Tr0ub4dor&3`** (palavra comum com trocas previsíveis `o` $\to$ `0`, `a` $\to$ `4`, maiúscula e símbolo):
  * Possui apenas **`~28 bits` de entropia** ($2^{28}$ tentativas $\approx$ **3 dias** a `1000` tentativas/segundo);
  * É difícil de memorizar para humanos e fácil de adivinhar por algoritmos de ataque.
* **`correct horse battery staple`** (frase-passe com 4 palavras comuns sorteadas aleatoriamente):
  * Selecionando 4 palavras de um dicionário de $2048$ ($2^{11}$) palavras comuns, obtêm-se $4 \times 11 =$ **`44 bits` de entropia** ($2^{44}$ tentativas $\approx$ **550 anos** a `1000` tentativas/segundo);
  * É fácil de memorizar visualmente e ordens de grandeza mais resistente a força bruta.

### 2.2. Auditoria de Fugas: `haveibeenpwned.com` (Slides 33–35)

* **[Have I Been Pwned](https://haveibeenpwned.com)** (mantido por Troy Hunt): permite confirmar se um endereço de e-mail ou número de telefone foi exposto em fugas de dados públicas.
  * **Regra fundamental**: **não reutilizar palavras-passe** entre diferentes sites ou contas de e-mail.
* **[Pwned Passwords](https://haveibeenpwned.com/Passwords)** (Slide 34): contabiliza quantas vezes uma palavra-passe já apareceu em fugas reais — a sequência **`123456`** já foi observada **`210,461,208` vezes**!
* **Nota Histórica de Engenharia Social em IRC (Slide 35)**: o célebre registo de chat ([bash.org #244321](http://bash.org/?244321)) mostra como um utilizador (`AzureDiamond`) foi convencido de que o IRC mascarava automaticamente passwords com asteriscos (`*******`), levando-o a escrever em texto limpo a sua password real **`hunter2`**.

---

## 3. Evolução das Diretrizes NIST: 2003 (Bill Burr) vs. `NIST SP 800-63-4` (2024) (Slides 27, 32, 49)

| Critério | **NIST 2003** (*Bill Burr — NIST 800-63B*, Slides 27 e 32) | **[NIST SP 800-63-4 (2024)](https://pages.nist.gov/800-63-4/sp800-63b.html)** (Slide 49) |
| :--- | :--- | :--- |
| **Base Empírica** | Em 2003 praticamente não existiam conjuntos públicos de passwords reais; as regras assentavam em suposições teóricas (*common sense*). | Fundamentado na análise empírica de milhares de milhões de palavras-passe reais expostas em fugas de dados. |
| **Alteração Periódica** | Impunha **alteração periódica obrigatória** (ex.: a cada **`90 dias`**) e proibia repetir a anterior. | **Proíbe exigir alterações periódicas** sem motivo: os utilizadores não investem em passwords fortes se expirarem rápido (limitam-se a incrementar sufixos). **Exceção obrigatória**: evidência de *data breach* ou *credential stuffing*. |
| **Comprimento e Caracteres** | Exigia **mistura forçada de classes** (maiúsculas, minúsculas, dígitos e símbolos, ex.: `wOr342TA-Hdf12`). | Mínimo de **`8` caracteres**, idealmente **`>= 15` caracteres** e suporte até pelo menos **`64` caracteres**. Aceita todos os caracteres **`ASCII` (incluindo espaços) e `Unicode`** (acentos e emojis). |

---

## 4. Os *7 Steps to Password Perfection* (Wired — Slide 50)

Síntese das sete práticas recomendadas em [Wired — 7 Steps to Password Perfection](https://www.wired.com/story/7-steps-to-password-perfection/):

1. **Usar um gestor de passwords**: evita reutilização e facilita senhas aleatórias longas (`KeePass`, `KeePassXC`, `Bitwarden`, `1Password`, `LastPass`);
2. **Apostar no comprimento**: palavras-passe longas oferecem maior segurança — adotar **`>= 15` caracteres** ou mais;
3. **Separar os caracteres especiais**: não concentrar todos os símbolos no início ou no final da password;
4. **Não alterar periodicamente sem causa**: rotações arbitrárias degradam a qualidade das escolhas;
5. **Uso único (*Single-serve only*)**: nunca reutilizar a mesma password entre serviços distintos;
6. **Não confiar no navegador**: evitar depender do gestor básico do *browser* sem proteção criptográfica forte da chave mestra;
7. **Ativar autenticação a dois fatores (2FA) sempre que possível**.

---

## Além da aula

* **Formalização Matemática e Armazenamento no Servidor**: A comparação intuitiva do paradigma `xkcd` é formalizada pela fórmula $E = L \times \log_2(R)$ em [[Entropia de Passwords e Entropia de Ficheiros (ent e Detect It Easy)]]. Já os riscos da reutilização e da truncagem de passwords longas em funções de hash são analisados em [[Limite do bcrypt (Okta Bypass), Credential Stuffing e Caso FortiBleed]], enquanto o armazenamento com *salting* e *key stretching* no servidor é aprofundado em [[Armazenamento Seguro de Passwords (Salting e Key Stretching) e Casos RockYou e LastPass]].
* **Operacionalização com Gestores e 2FA**: Os passos 1 e 7 da lista da Wired concretizam-se na prática através de [[Gestores de Passwords (Cloud vs KeePassXC), KeeShare e Copy-Paste Hijacking]] e de [[Autenticação 2FA (Protocolo TOTP RFC 6238) e Passkeys (FIDO2 - WebAuthn e CTAP)]].

---

## Perguntas de revisão

1. **Por que razão `correct horse battery staple` oferece maior segurança e usabilidade do que `Tr0ub4dor&3` segundo o paradigma `xkcd #936`?**

> [!success]- Ver Resposta
> `Tr0ub4dor&3` aplica substituições previsíveis (`o` $\to$ `0`, `a` $\to$ `4`) que resultam em apenas **`~28 bits` de entropia** (~3 dias de força bruta a `1000` tentativas/s), sendo simultaneamente difícil de memorizar. Já `correct horse battery staple` combina 4 palavras comuns sorteadas de um vocabulário de `2048` ($2^{11}$) palavras, alcançando **`44 bits` de entropia** (~550 anos a `1000` tentativas/s) com memorização visual simples.

2. **Quais são as três principais diferenças entre as diretrizes NIST de 2003 (Bill Burr) e o `NIST SP 800-63-4` (2024)?**

> [!success]- Ver Resposta
> (1) **Base empírica**: 2003 baseava-se em senso comum teórico, enquanto 2024 assenta na análise de grandes fugas reais de passwords; (2) **Rotação**: 2003 forçava alterações periódicas (ex.: 90 dias), enquanto 2024 **proíbe alterações periódicas obrigatórias**, exigindo troca apenas perante evidência de *data breach* ou *credential stuffing*; (3) **Composição e comprimento**: 2003 forçava mistura de tipos de caracteres, enquanto 2024 privilegia comprimento (mínimo **`8`**, ideal **`>= 15`**, até **`64` caracteres**) e exige suporte a espaços **`ASCII`** e **`Unicode`**.

3. **Que impacto teve uma password fraca no caso *IHG Hack* e o que demonstra o registo de `123456` no *Pwned Passwords*?**

> [!success]- Ver Resposta
> No caso *IHG Hack* (*InterContinental Hotels Group*), atacantes entraram no cofre de passwords corporativo protegido por **`Qwerty1234`** e executaram o *ransomware* LockBit. No serviço *Pwned Passwords* (`haveibeenpwned.com/Passwords`), a password **`123456`** já foi contabilizada **`210,461,208` vezes** em violações reais, provando o risco extremo de senhas comuns.

4. **Enumere os 7 passos para a perfeição em palavras-passe segundo o artigo da Wired.**

> [!success]- Ver Resposta
> (1) Usar um gestor de passwords; (2) Apostar no comprimento (`>= 15` caracteres); (3) Manter os caracteres especiais separados em vez de os agrupar no início/fim; (4) Não alterar periodicamente a password sem motivo; (5) Usar cada password apenas num único serviço (*single-serve only*); (6) Não confiar no gestor básico do navegador; (7) Ativar autenticação a dois fatores (2FA) sempre que possível.

## Notas relacionadas

- [[Capítulo 2 - Administração de Sistemas]]
- [[Limite do bcrypt (Okta Bypass), Credential Stuffing e Caso FortiBleed]]
- [[Entropia de Passwords e Entropia de Ficheiros (ent e Detect It Easy)]]
- [[Gestores de Passwords (Cloud vs KeePassXC), KeeShare e Copy-Paste Hijacking]]
- [[Armazenamento Seguro de Passwords (Salting e Key Stretching) e Casos RockYou e LastPass]]
- [[Autenticação 2FA (Protocolo TOTP RFC 6238) e Passkeys (FIDO2 - WebAuthn e CTAP)]]
