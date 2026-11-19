---
title: Limite do bcrypt (Okta Bypass), Credential Stuffing e Caso FortiBleed
tipo: analise
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 2
bloco: 5
fonte_aula: System Administration - Access Control.pdf
fontes:
  - "https://x.com/bcrypt/status/1852575080989257893"
  - "https://tech-insider.org/fortibleed-fortinet-firewall-breach-2026/"
tags:
  - assi
  - administracao-sistemas
  - controlo-acessos
  - bcrypt
  - okta
  - argon2
  - credential-stuffing
  - fortibleed
aliases:
  - Limite 72 Bytes do bcrypt
  - Okta bcrypt Bypass
  - Credential Stuffing
  - Caso FortiBleed
atualizado: 2026-11-11
---

# Limite do `bcrypt` (Okta Bypass), *Credential Stuffing* e Caso `FortiBleed`

O limite de `56–72 bytes` da cifra *Blowfish* no `bcrypt` originou o *bypass* de autenticação na Okta, enquanto a reutilização de credenciais alimenta o *credential stuffing* e ataques agregados como o `FortiBleed`.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema / Ameaça)**: Algoritmos lentos como `bcrypt`, `scrypt` e `Argon2` travam a força bruta paralela em GPUs (`RTX 5090`), mas a estrutura interna *Blowfish* do `bcrypt` descarta silenciosamente dados após `56–72 bytes`; em paralelo, listas vazadas permitem testar credenciais reutilizadas em massa.
> * **Porque importa (Segurança / Forense)**: Concatenar identificadores antes da password num hash `bcrypt` cria falhas críticas de *authentication bypass*, e não rodar credenciais nem impor 2FA transforma fugas isoladas em recolhas agregadas de longa duração (`FortiBleed`).
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **`bcrypt` vs. `Argon2`/`scrypt`**: `Argon2` e `scrypt` são *memory-hard* (exigem muita RAM, dificultando paralelização em GPU).
>   * **Bug `Okta AD/LDAP DelAuth` (Nov 2024)**: `bcrypt(userId + ":" + username + ":" + password)` fazia com que **`username > 56 bytes`** saturasse o `bcrypt`, **ignorando totalmente a password**.
>   * **`FortiBleed` (Junho 2026)**: exposição de credenciais funcionais de **`86,644` firewalls Fortinet** (`>21,000` IPs em `194` países) num **ataque de agregação** (fugas antigas + força bruta + configurações via `CVE-2018-13379` + hashes quebrados).

---

## 1. Resistência a Força Bruta em GPUs (`12 x RTX 5090`) e o Limite do `bcrypt` (Slides 47–48)

### 1.1. Tempos de Ataque contra `bcrypt` vs. Funções *Memory-Hard* (Slide 47)
A avaliação de tempos de força bruta no pior caso com um *cluster* de **`12 x NVIDIA RTX 5090`** contra hashes **`bcrypt`** evidencia dois factos operacionais:

* **Vantagem do `Argon2` e `scrypt`**: embora o `bcrypt` seja um algoritmo sólido de derivação/hashing de passwords, **`Argon2`** e **`scrypt`** oferecem maior resistência contra hardware paralelo (GPUs/ASICs) por serem ***memory-hard*** (impõem consumo elevado de memória RAM por tentativa);
* **Impacto do Comprimento**: senhas curtas (`4 a 7` caracteres), mesmo usando todo o conjunto de símbolos, são quebradas entre segundos e poucas semanas/anos; a partir de **`>= 11–15` caracteres** variados, o custo computacional contra `bcrypt` escala para milhares ou milhões de anos.

### 1.2. Truncagem Silenciosa (`56–72 Bytes`) e Vulnerabilidade na `Okta` (Slide 48)

> [!TIP] Simulador Interativo do Bug dos 72 Bytes (`Okta Bypass`)
> Para testar como um prefixo `userId + ":" + username + ":"` longo empurra a password para lá do byte `72` e faz o `bcrypt` ignorá-la, abre [assi_passwords_entropia.html](../../../_assets/assi_passwords_entropia.html) (separador **2. Bug bcrypt 72 Bytes**).

* **Limitação Arquitetural do `bcrypt`**: devido à sua base na cifra por blocos **Blowfish**, a maioria das implementações de **`bcrypt` processa apenas os primeiros `56 a 72 bytes` da string de entrada**, truncando silenciosamente qualquer byte adicional sem devolver erro.

**Caso Real — `Okta AD/LDAP DelAuth` (Novembro de 2024):** conforme reportado em [Aviso Técnico sobre Okta / bcrypt (X)](https://x.com/bcrypt/status/1852575080989257893), o agente calculava uma chave de cache concatenando o identificador e o nome de utilizador antes da password:

$$\text{Hash} = \text{bcrypt}(\text{username} \;\|\; \text{password})$$

Mais concretamente, a construção usada era:

```text
bcrypt(userId + ":" + username + ":" + password)
```

* **Consequência Crítica (*Authentication Bypass*)**: sempre que **`username > 56 bytes`**, o prefixo `userId + ":" + username + ":"` preenche sozinho o limite máximo processado pelo `bcrypt`. Assim, **a `password` é truncada e completamente ignorada**, permitindo autenticar na conta com qualquer palavra-passe (ou até sem introduzir nenhuma).

---

## 2. Reutilização de Credenciais: *Credential Stuffing* e Caso `FortiBleed` (Slides 51–52)

### 2.1. *Credential Stuffing* e Listas de Combinação (Slide 51)

* **Mecanismo**: o *Credential Stuffing* é um ataque automatizado que explora diretamente a **reutilização de palavras-passe** pelos utilizadores em serviços diferentes.
* Os atacantes alimentam *bots* distribuídos com enormes compilações públicas no formato `email:password` extraídas de violações anteriores — como a **`Anti Public Combo List`** — e testam os pares em massa contra portais bancários, comércio eletrónico, redes sociais e VPNs empresariais.

### 2.2. Caso de Estudo: `FortiBleed` (Junho de 2026 — Slide 52)
Documentado em [Tech Insider — FortiBleed (2026)](https://tech-insider.org/fortibleed-fortinet-firewall-breach-2026/), o incidente `FortiBleed` revelou a persistência de falhas operacionais em perímetros críticos:

* **Dimensão da Exposição**: base de dados descoberta num servidor aberto em **junho de 2026** contendo credenciais válidas de **administrador e de VPN para `86,644` firewalls Fortinet**, abrangendo **mais de `21,000` endereços IP em `194` países**;
* **Natureza do Ataque (*Aggregation Attack*)**: o `FortiBleed` não decorreu de uma falha *zero-day* única, mas de um **ataque de agregação** que consolidou ao longo do tempo:
  1. **Anos de credenciais vazadas** (*leaked credentials*);
  2. **Logins obtidos por força bruta**;
  3. **Ficheiros de configuração exfiltrados** através de vulnerabilidades antigas conhecidas (como **`CVE-2018-13379`**);
  4. **Hashes previamente quebrados** (*cracked hashes*).
* **Causa Raiz da Persistência**: as credenciais permaneceram válidas durante anos porque os administradores **não efetuaram rotação de passwords** após correções/incidentes nem ativaram **2FA**, obrigando a própria Fortinet e agências nacionais de cibersegurança a emitir alertas de emergência.

---

## Além da aula

* **Armazenamento Seguro no Servidor e Quebra com Hashcat (`ASSI` Cap. 2 Bloco 06)**: As propriedades de *salting*, *key stretching* e escolha de KDFs (`PBKDF2`, `bcrypt`, `scrypt`, `Argon2id`) são aprofundadas em [[Armazenamento Seguro de Passwords (Salting e Key Stretching) e Casos RockYou e LastPass]], enquanto a execução prática de ataques sobre hashes reais é tratada em [[Cracking e Auditoria de Passwords com Hashcat (Hashcat 101 e Máscaras)]].
* **Correlação com CVEs Antigas Não Mitigadas**: A exploração contínua da `CVE-2018-13379` no incidente `FortiBleed` reforça que a aplicação de atualizações de segurança sem rotação imediata das credenciais potencialmente exfiltradas não neutraliza o acesso persistente, cumprindo as exceções de rotação definidas pelo `NIST SP 800-63-4` em [[Segurança de Passwords, Paradigma xkcd e Diretrizes NIST (2003 vs SP 800-63-4)]].

---

## Perguntas de revisão

1. **Por que razão `Argon2` e `scrypt` oferecem maior resistência do que o `bcrypt` contra clusters de GPUs como `12 x RTX 5090`?**

> [!success]- Ver Resposta
> Embora o `bcrypt` seja resistente quando combinado com passwords longas ($\ge 11\text{–}15$ caracteres), o `Argon2` e o `scrypt` são algoritmos ***memory-hard***, impondo o consumo de grandes quantidades de memória RAM por cada tentativa de cálculo e limitando fortemente o paralelismo massivo em GPUs e ASICs.

2. **Qual é o limite de entrada do `bcrypt` e como provocou o *bypass* de autenticação na `Okta AD/LDAP DelAuth` em novembro de 2024?**

> [!success]- Ver Resposta
> Baseado na cifra Blowfish, o `bcrypt` processa apenas os primeiros **`56 a 72 bytes`** da string de entrada e trunca silenciosamente o restante. Na `Okta`, a chave de cache calculava `bcrypt(userId + ":" + username + ":" + password)`: quando **`username > 56 bytes`**, o prefixo esgotava o limite do `bcrypt` e a **`password` era totalmente ignorada**, permitindo autenticar com qualquer valor.

3. **Em que consiste um ataque de *Credential Stuffing* e que tipo de listas utiliza?**

> [!success]- Ver Resposta
> É um ataque automatizado que explora a reutilização de palavras-passe em múltiplos sites, testando em massa pares `email:password` extraídos de violações antigas (como a **`Anti Public Combo List`**) contra outros serviços (bancos, lojas, VPNs).

4. **Por que razão o caso `FortiBleed` (2026) é classificado como um *Aggregation Attack* e que falhas organizacionais permitiram o seu impacto?**

> [!success]- Ver Resposta
> O `FortiBleed` (`86,644` firewalls Fortinet em `194` países) não explorou uma vulnerabilidade inédita, mas agregou credenciais antigas vazadas, logins obtidos por força bruta, hashes quebrados e configurações exfiltradas por CVEs conhecidas (como `CVE-2018-13379`). As credenciais continuaram válidas pela ausência de **rotação após compromissos/correções** e falta de **2FA**.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Segurança de Passwords, Paradigma xkcd e Diretrizes NIST (2003 vs SP 800-63-4)]] | `mesmo bloco` |
| **Seguinte** | [[Entropia de Passwords e Entropia de Ficheiros (ent e Detect It Easy)]] | `mesmo bloco` |
| **Índice** | [[Capítulo 2 - Administração de Sistemas]] · [[00 ASSI]] | `Bloco 05` |

### Conceitos Relacionados

* [[Armazenamento Seguro de Passwords (Salting e Key Stretching) e Casos RockYou e LastPass]] · `Bloco 06`
* [[Cracking e Auditoria de Passwords com Hashcat (Hashcat 101 e Máscaras)]] · `Bloco 06`
* [[Autenticação 2FA (Protocolo TOTP RFC 6238) e Passkeys (FIDO2 - WebAuthn e CTAP)]] · `Bloco 06`
