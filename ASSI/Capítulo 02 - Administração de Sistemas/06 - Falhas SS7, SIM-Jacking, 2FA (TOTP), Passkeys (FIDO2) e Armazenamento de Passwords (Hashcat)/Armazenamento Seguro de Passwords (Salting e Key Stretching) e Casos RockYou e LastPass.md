---
title: Armazenamento Seguro de Passwords (Salting e Key Stretching) e Casos RockYou e LastPass
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 2
bloco: 6
fonte_aula: System Administration - Access Control.pdf
tags:
  - assi
  - administracao-sistemas
  - controlo-acessos
  - salting
  - key-stretching
  - argon2
  - pbkdf2
  - scrypt
  - bcrypt
  - rainbow-tables
  - rockyou
  - lastpass
aliases:
  - Armazenamento Seguro de Passwords
  - Per-Credential Salt
  - Key Stretching Argon2 PBKDF2
  - Caso RockYou 2009
  - Caso LastPass 2022
  - Rainbow Tables
atualizado: 2026-11-11
---

# Armazenamento Seguro de Passwords (Salting e Key Stretching) e Casos RockYou e LastPass

Perante a inevitabilidade de fugas de dados, as passwords exigem um salt único por credencial e Key Stretching lento (Argon2, PBKDF2, scrypt ou bcrypt), prevenindo falhas como RockYou (2009) e LastPass (2022).

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema / Segurança)**: Como a exfiltração da base de dados de autenticação é uma questão de tempo (*"not if, but when"*), o formato armazenado tem de inviabilizar ataques offline em GPU e pesquisas pré-computadas.
> * **Porque importa (Segurança / Forense)**: O **`per-credential salt`** garante hashes distintos para passwords idênticas e anula *Rainbow Tables*, enquanto o **`Key Stretching`** com elevado fator de custo reduz drasticamente o débito de tentativas offline após um incidente.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * As passwords **NUNCA DEVEM (*SHALL NEVER*)** ser guardadas em texto limpo (caso **`RockYou` 2009** — `32M`) nem com hashes rápidos sem *salt* (`MD5`), ou com *salt* global/por utilizador.
>   * Ordem de preferência do `Key Stretching`: **1. `Argon2`** > **2. `PBKDF2`** > **3. `scrypt`** > **4. `bcrypt`**.
>   * No caso **`LastPass` (2022)**, contas antigas mantinham apenas **`500` iterações** de `PBKDF2`, muito abaixo das `100,100` anteriores e das **`300,000` / `600,000`** recomendadas.

---

## 1. Inevitabilidade de Violações, Ataques Offline e *Rainbow Tables* (Slides 105–107)

* **Princípio de Defesa (*Not "if", but "when"*)**: evitar todas as violações de dados é tecnicamente difícil e dispendioso; a questão operacional não é *"se"* a base de autenticação será comprometida, mas *"quando"*.
* **Ataques Offline**: assim que obtém os resumos da base de dados, o atacante calcula `Hash(attempt_password)` fora de linha e compara com os valores armazenados, recorrendo a duas técnicas aceleradas:
  1. **Dicionários (*Dictionaries*)**: listas de passwords reais reutilizadas e variações;
  2. **Tabelas de Pesquisa / *Rainbow Tables***: estruturas pré-computadas contendo milhares de milhões de hashes (disponíveis comercialmente em disco, ex.: [Rainbow Tables da OSForensics](https://www.osforensics.com/tools/rainbow-tables/index.html) — Slide 107).

---

## 2. `Per-Credential Salt` e `Key Stretching` (Slides 106, 108–109)

### 2.1. Regra do `Per-Credential Salt` (Sal Único por Credencial)

* **Proibição Absoluta**: as palavras-passe **NUNCA DEVEM (*SHALL NEVER*)** ser guardadas em texto limpo (*clear text*), e aplicar apenas um hash criptográfico rápido como **`MD5`** oferece proteção residual quase nula.
* **Aplicação Correta do `Salt` (`Hash(password + num_salt)`)**:
  * O sistema tem de gerar um **`salt` aleatório e único para cada credencial armazenada (*per-credential salt*)** — e **não apenas um sal por utilizador ou um sal global para todo o sistema**.
  * **Duas Garantias Criptográficas**:
    1. **Impede que duas palavras-passe idênticas produzam o mesmo hash** na base de dados;
    2. **Invalida integralmente *lookup tables* e *Rainbow Tables* pré-computadas**, forçando o atacante a testar cada credencial separadamente.

### 2.2. Funções Unidirecionais com `Key Stretching` — Ordem de Preferência (Slide 109)

| Ordem de Preferência | Função de Derivação / Hashing | Características Técnicas |
| :---: | :--- | :--- |
| **1.º (Preferida)** | **`Argon2`** | Vencedora da *Password Hashing Competition* (2015); resistente a GPUs/ASICs e canais laterais (*memory-hard* e *CPU-hard*). |
| **2.º** | **`PBKDF2`** | Norma NIST / PKCS #5; aplica iterativamente uma função pseudoaleatória (como `HMAC-SHA256`). |
| **3.º** | **`scrypt`** | Função *memory-hard* e *CPU-hard* que consome RAM significativa para travar paralelismo em hardware dedicado. |
| **4.º** | **`bcrypt`** | Baseada na cifra *Blowfish* com fator de custo ajustável (sujeita ao limite interno de 56–72 bytes de entrada). |

* **Mecanismo do `Key Stretching`**: todas estas funções integram um **contador de iterações ajustável (*iteration count* / fator de custo)** e são concebidas para executar de forma **deliberadamente lenta**, tornando ataques de força bruta em massa computacionalmente inviáveis.

---

## 3. Casos de Estudo: `RockYou` (2009) e `LastPass` (2022) (Slides 110–111)

### 3.1. Caso `RockYou` Data Breach (2009 — Slide 110)

* **Contexto e Falha**: a empresa *RockYou* (desenvolvedora de aplicações e *widgets* para MySpace e Facebook) foi comprometida via **SQL Injection**, expondo **`32 milhões` de passwords guardadas em texto limpo (*plaintext*)** sem cifragem nem hash, sem notificação atempada aos utilizadores.

**Legado no Kali Linux:** a fuga originou o dicionário padrão de auditoria `rockyou.txt`, composto por **`14,340,000` passwords únicas** extraídas de **`32,603,000` contas**, pré-instalado no Kali Linux em:

```bash
/usr/share/wordlists/rockyou.txt.gz
```

e espelhado online em [rockyou.txt.bz2 (SkullSecurity)](http://downloads.skullsecurity.org/passwords/rockyou.txt.bz2).

### 3.2. Caso `LastPass` Data Breach e Iterações `PBKDF2` (2022 — Slide 111)

* **Cronologia da Divulgação**:
  * **Agosto de 2022**: a LastPass reporta uma intrusão garantindo que apenas código-fonte fora acedido e que nenhum dado de clientes fora comprometido;
  * **Novembro de 2022**: reconhece o acesso a *"certos elementos de informação de clientes"*;
  * **Dezembro de 2022**: revela que os atacantes usaram a informação obtida em agosto para comprometer o computador doméstico de um engenheiro DevOps através de uma vulnerabilidade no servidor multimédia **Plex**, roubando as chaves de acesso aos backups na *cloud* com os **cofres de passwords cifrados (*data vaults*) dos clientes**.
* **Falha de `Key Stretching` (`PBKDF2`)**:
  * Embora os cofres fossem protegidos com **`PBKDF2`**, contas de utilizadores mais antigos (*initial users*) mantinham apenas **`500` iterações** (e o padrão anterior de **`100,100`** iterações já estava desatualizado);
  * As recomendações atuais (OWASP/NIST) apontam para **`300,000` iterações** (ou **`600,000`** para `PBKDF2-HMAC-SHA256`), ampliando substancialmente o custo do *cracking* offline dos cofres exfiltrados.

---

## 4. Os 4 Cenários de Base Comprometida, Guia NCSC e Referências (Slides 115–116, 118–119)

### 4.1. Comparação da Resistência Quando a Base de Dados é Comprometida (Slide 115)

| Como as Passwords Estão Armazenadas | Consequência e Viabilidade do Ataque |
| :--- | :--- |
| **1. Em texto limpo (*Plain text*)** | **Comprometimento imediato (*"It's game over"*)** — todas as credenciais ficam legíveis sem esforço computacional. |
| **2. Hash sem `salt` ou com *salt* global do sistema** | Vulnerável a **ataques de dicionário em massa** e a **tabelas pré-computadas (*lookup / rainbow tables*)**; senhas iguais geram o mesmo hash. |
| **3. Hash rápido com `per-credential salt`** | Neutraliza *lookup/rainbow tables*, mas permanece vulnerável a **ataques rápidos de dicionário e força bruta em GPU** (milhares de milhões de hashes/s). |
| **4. `Per-credential salt` + função lenta com `Key Stretching` (`Argon2`, `PBKDF2`, `scrypt`, `bcrypt`)** | **Força bruta e dicionários tornam-se extremamente lentos**, protegendo eficazmente todas as passwords não triviais. |

### 4.2. Infografia NCSC e Bibliografia Científica (Slides 116, 118–119)

* **Diretrizes NCSC (*Password Security*, Slide 116)**:
  * **Administradores (*Sysadmins*)**: não confiar apenas em passwords; **nunca guardar em *plaintext***; aplicar **hash com `salt` + função lenta**; exigir **2FA**; **não impor expiração periódica**; bloquear senhas comuns (*blacklist*).
  * **Utilizadores**: **não reutilizar passwords**; usar **gestor de passwords**; ativar **2FA**; escolher senhas longas (ex.: 3 palavras aleatórias / $\ge 15$ caracteres).
* **Referências de Aprofundamento**:
  * [OWASP Password Storage Cheat Sheet](http://bit.ly/1gVO8Xa) e [OWASP Cryptographic Storage Cheat Sheet](http://bit.ly/2p0le4S);
  * [OpenWall (2012)](http://bit.ly/2ztxSvc) — *"Password security: past, present, future"*;
  * Pearman, S. et al. (2017) — *"Let's Go in for a Closer Look: Observing Passwords in Their Natural Habitat"* (*ACM SIGSAC CCS*);
  * Hitaj, B., Gasti, P., Ateniese, G., & Perez-Cruz, F. (2017) — ***"PassGAN: A Deep Learning Approach for Password Guessing"*** (GANs treinadas sobre o *dataset* *RockYou* para gerar candidatas realistas);
  * Brotherston, L. & Berlin, A. (2016) — *Defensive Security Handbook* (Caps. 5 e 13).

---

## Além da aula

* **Porque o `CrackStation` Falha Perante `Salting` e `Key Stretching` (`AFD1` Cap. 1 Bloco 02)**: Em [[Preservação do Sistema e Integridade de Dados]] e [[Exercícios Práticos - Integridade de Dados e Hashes]], o serviço `CrackStation` inverte instantaneamente hashes `MD5` e `SHA-256` não salgados recorrendo a *lookup tables* gigantescas; a introdução do **`per-credential salt`** invalida essas tabelas, enquanto o **`Key Stretching`** trava a auditoria offline estudada em [[Cracking e Auditoria de Passwords com Hashcat (Hashcat 101 e Máscaras)]].
* **Armadilha Arquitetural do `bcrypt` (`ASSI` Cap. 2 Bloco 05)**: Embora o `bcrypt` figure na lista de funções recomendadas, a sua truncagem interna entre `56` e `72` bytes exige cuidado na concatenação de entradas, como demonstra o bypass da Okta em [[Limite do bcrypt (Okta Bypass), Credential Stuffing e Caso FortiBleed]].

---

## Perguntas de revisão

1. **Porque é que o `salt` deve ser gerado aleatoriamente por cada credencial armazenada (`per-credential salt`) em vez de por utilizador ou globalmente, e que duas garantias oferece?**

> [!success]- Ver Resposta
> Um *salt* global ou reutilizado permite ao atacante construir ou reutilizar tabelas pré-computadas e identificar senhas repetidas. O **`per-credential salt`** garante que: (1) duas palavras-passe idênticas produzem hashes completamente diferentes na base de dados; e (2) as *lookup tables* e *Rainbow Tables* pré-computadas tornam-se inúteis, obrigando a atacar cada credencial individualmente.

2. **Liste as quatro funções de `Key Stretching` por ordem de preferência e explique o papel do parâmetro `iteration count`.**

> [!success]- Ver Resposta
> Ordem de preferência: **1. `Argon2`**, **2. `PBKDF2`**, **3. `scrypt`**, **4. `bcrypt`**. O **`iteration count`** (fator de custo) ajusta quantas rondas internas a função executa, tornando a derivação deliberadamente lenta para inviabilizar ataques de força bruta em massa.

3. **Qual foi o impacto da violação da `RockYou` (2009) na auditoria de passwords e qual foi a falha crítica de configuração na violação da `LastPass` (2022)?**

> [!success]- Ver Resposta
> Na **`RockYou` (2009)**, uma falha de SQL Injection expôs **`32 milhões`** de passwords em texto limpo, originando o dicionário `/usr/share/wordlists/rockyou.txt.gz` no Kali Linux (`14,340,000` senhas únicas de `32,603,000` contas). Na **`LastPass` (2022)**, após o roubo dos cofres cifrados em backups na *cloud* (via PC de um DevOps com Plex vulnerável), descobriu-se que contas antigas utilizavam apenas **`500` iterações** de `PBKDF2`, muito abaixo das **`300,000`** (ou `600,000`) recomendadas.

4. **Compare a resiliência de uma base de dados comprometida nos quatro cenários possíveis de armazenamento (do texto limpo ao *salting* com *Key Stretching*).**

> [!success]- Ver Resposta
> (1) **Texto limpo**: comprometimento imediato (*"game over"*); (2) **Hash sem *salt* ou *salt* global**: vulnerável a dicionário em massa e *Rainbow Tables*; (3) **Hash rápido com `per-credential salt`**: derrota *Rainbow Tables*, mas é quebrado rapidamente por força bruta/dicionário em GPU; (4) **`Per-credential salt` + `Key Stretching` lento**: torna os ataques offline extremamente lentos, protegendo passwords não triviais.

## Notas relacionadas

- [[Capítulo 2 - Administração de Sistemas]]
- [[Cracking e Auditoria de Passwords com Hashcat (Hashcat 101 e Máscaras)]]
- [[Segurança de Passwords, Paradigma xkcd e Diretrizes NIST (2003 vs SP 800-63-4)]]
- [[Limite do bcrypt (Okta Bypass), Credential Stuffing e Caso FortiBleed]]
- [[Preservação do Sistema e Integridade de Dados]]
- [[Exercícios Práticos - Integridade de Dados e Hashes]]
- [[Cheat Sheet - Administração de Sistemas e Controlo de Acessos]]
