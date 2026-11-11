---
title: Gestores de Passwords (Cloud vs KeePassXC), KeeShare e Copy-Paste Hijacking
tipo: ferramenta
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 2
bloco: 5
fonte_aula: System Administration - Access Control.pdf
fontes:
  - "https://keepass.info"
  - "https://passwords.google.com/"
  - "http://bit.ly/2yzT6Z8"
tags:
  - assi
  - administracao-sistemas
  - controlo-acessos
  - password-managers
  - keepass
  - keepassxc
  - keeshare
  - bitwarden
  - copy-paste-hijacking
aliases:
  - Gestores de Passwords
  - KeePass e KeePassXC
  - KeeShare
  - Copy-Paste Hijacking
  - Bitwarden
  - Ficha 10 keepassXC + entropy
atualizado: 2026-11-11
---

# Gestores de Passwords (*Cloud* vs. `KeePassXC`), `KeeShare` e *Copy-Paste Hijacking*

Os gestores de passwords (*cloud* como `Bitwarden` ou locais como `KeePassXC`) eliminam a reutilização de credenciais e mitigam *phishing* via *auto-fill*, exigindo cuidados face a *copy-paste hijacking*.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema / Ameaça)**: Cumprir a regra de passwords únicas e longas ($\ge 15$ caracteres) em dezenas de serviços ultrapassa a memória humana; contudo, copiar manualmente segredos através da área de transferência expõe-nos a *clipper malware* e ao histórico do sistema operativo.
> * **Porque importa (Segurança / Forense)**: O *auto-fill* valida o domínio exato contra ataques homográficos (`mail.g0ogle.com`), o `KeePassXC` protege o *clipboard* limpando-o aos `10s` com a flag `ClipboardViewerIgnore`, e o `KeeShare` permite partilha colaborativa autenticada.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **`KeePass`** (GPL v2+): usa **`AES/Rijndael`** e **`Twofish`**; *Master Key* aceita **`Password`**, **`Key file`** ou **`Password + Key file`** (recomendado), com suporte a *plugins*.
>   * **`KeePassXC`** (**Ficha 10**): *fork open-source* multiplataforma com bases **`.kdbx`** cifradas por **`AES-256`**, **`ChaCha20`** ou **`Twofish`**.
>   * **`KeeShare`**: partilha sincronizada de grupos/entradas via contentor intermédio (Dropbox, Google Drive, Nextcloud) com **assinaturas criptográficas** e **E2EE**.
>   * ***Copy-paste hijacking***: *clipper malware* alterou endereços Bitcoin no *clipboard* roubando **`13 BTC`** (`$36,000` em jun/2017 $\to$ `$905,801` em nov/2024).

---

## 1. Gestores *Cloud-Based* vs. Gestores Locais (Slides 62–63)

| Critério | Gestores *Cloud-Based* (Online) | Gestores Locais (*Offline*) |
| :--- | :--- | :--- |
| **Exemplos Principais** | **`1Password`**, **`Bitwarden`**, **`LastPass`**, **`Google Password Manager`** | **`KeePass`** ([keepass.info](https://keepass.info)) e **`KeePassXC`** |
| **Armazenamento e Sincronização** | Base cifrada alojada em servidores remotos com sincronização automática entre dispositivos; o utilizador memoriza apenas a **Master Password**. | Ficheiro de base de dados local cifrado (**`.kdbx`**) sob controlo exclusivo do utilizador. |
| **Proteção contra *Phishing* (*Auto-fill*)** | Extensões de navegador preenchem apenas no domínio legítimo: preenchem em `mail.google.com`, mas **recusam preencher em `mail.g0ogle.com`** (*typosquatting* / ataques homográficos). | Reforçáveis com **ficheiro-chave (*key file*)** ou **token de hardware** (ex.: YubiKey); o uso por *copy-paste* manual fica exposto a *copy-paste hijacking*. |

---

## 2. *Copy-Paste Hijacking* (*Clipper Malware* — Slide 64)

* **Mecanismo do Ataque**: *malware* instalado na máquina (*clipper malware*) monitoriza continuamente a área de transferência (*clipboard*), capturando palavras-passe copiadas do gestor local ou **substituindo silenciosamente strings copiadas no instante da colagem (*paste*)**.
* **Caso Real com Bitcoin ([Caso Bitcoin Clipper](http://bit.ly/2yzT6Z8))**: ao copiar um endereço Bitcoin longo para efetuar um pagamento, o *malware* deteta o padrão na área de transferência e troca-o pelo endereço do atacante. No caso documentado na aula, um único endereço malicioso acumulou **`13 BTC`** (avaliados em **`$36,000 USD`** em junho de 2017 e **`$905,801 USD`** em novembro de 2024).

---

## 3. Análise das Soluções: `KeePass`, `KeePassXC`, `KeeShare`, `Google` e `Bitwarden` (Slides 66–70, 79)

1. **`KeePass` (Slide 66)**:
   * Software *open source* (licença **GPL v2 ou posterior**) para Windows, Linux, Android e iOS;
   * Cifra a base de dados local com **`AES/Rijndael`** e **`Twofish`** e suporta *plugins*;
   * **Composição da *Master Key***: apenas **`Password`**, apenas **`Key file`**, ou **`Password + Key file`**.
2. **`KeePassXC` (Slide 67 — `Ficha 10: keepassXC + entropy`, Slide 79)**:
   * *Fork* comunitário *open-source* e multiplataforma (**Windows, macOS e Linux**);
   * Utiliza o formato **`.kdbx`** (compatível com KeePass) com algoritmos de cifragem modernos: **`AES-256`**, **`ChaCha20`** e **`Twofish`**.
3. **Partilha Segura com `KeeShare` (Slide 68)**:
   * Mecanismo integrado no `KeePassXC` para **gestão colaborativa de passwords** em equipa;
   * Sincroniza **grupos ou entradas específicas** através de um contentor intermédio baseado em ficheiros (partilhável via **Dropbox, Google Drive, Nextcloud**, etc.);
   * Garante **autenticidade e integridade por assinaturas criptográficas** e **cifragem ponta a ponta (E2EE)** protegida por password e certificado assinado.
4. **`Google Password Manager` (Slide 69)**: acessível via conta Google ([Google Password Manager](https://passwords.google.com/)), Chrome e Android; disponibiliza gravação, *auto sign-in*, exportação e opção de cifragem local no dispositivo (*on-device encryption*).
5. **`Bitwarden` (Slide 70)**: gestor *cloud-based* e ***open source*** autenticado por endereço de e-mail, disponível em *mobile*, *desktop* (Windows/Linux/macOS) e extensões de *auto-fill* para navegadores.

---

## Além da aula

* **Forense do *Clipboard* no Windows (`ASSI` Cap. 1 Bloco 14)**: O risco de *copy-paste hijacking* articula-se diretamente com a persistência da área de transferência analisada em [[Recuperação de Clipboard e Sincronização na Timeline]]: com o histórico `Win+V` ou a sincronização na *cloud* (`ActivitiesCache.db`) ativos, conteúdos copiados são gravados em disco em Base64. Para mitigar essa exposição, o **`KeePassXC`** limpa automaticamente o *clipboard* **`10 segundos`** após copiar uma senha e aplica a flag **`ClipboardViewerIgnore`** (`ExcludeClipboardContentFromMonitorProcessing`) para impedir o registo no histórico do Windows 10/11.
* **Segurança de Cofres na Cloud e Contingência (`ASSI` Cap. 2 Blocos 05–06)**: Os riscos associados a serviços *cloud* como o **LastPass** (iteração insuficiente de PBKDF2 e fugas de metadados) são examinados em [[Armazenamento Seguro de Passwords (Salting e Key Stretching) e Casos RockYou e LastPass]], enquanto a utilização do `KeePassXC` para responder a perguntas de segurança e planear contingência é detalhada em [[Contingência de Credenciais (Cantor Fitzgerald) e Perguntas de Segurança (Sarah Palin)]].

---

## Perguntas de revisão

1. **Qual é a principal vantagem de segurança do preenchimento automático (*auto-fill*) dos gestores de passwords face ao *copy-paste* manual?**

> [!success]- Ver Resposta
> O *auto-fill* verifica o domínio exato do URL antes de injetar as credenciais, protegendo contra sites falsos visualmente idênticos (*typosquatting* / ataques homográficos, ex.: preenche em `mail.google.com` mas recusa preencher em `mail.g0ogle.com`), além de evitar expor a password na área de transferência a *clipper malware*.

2. **Como funciona o *Copy-paste hijacking* e que proteções forenses integra o `KeePassXC` na cópia de credenciais?**

> [!success]- Ver Resposta
> Um *clipper malware* monitoriza o *clipboard* para ler senhas copiadas ou substituir silenciosamente dados no momento da colagem (tendo roubado **`13 BTC`** num caso documentado na aula). Para proteger a área de transferência contra leitura e persistência no histórico do Windows (`Win+V` / `ActivitiesCache.db`), o `KeePassXC` limpa o *clipboard* após **`10 segundos`** e marca os dados com a flag **`ClipboardViewerIgnore`** (`ExcludeClipboardContentFromMonitorProcessing`).

3. **Compare os algoritmos de cifragem e as opções de *Master Key* entre `KeePass` e `KeePassXC`.**

> [!success]- Ver Resposta
> O **`KeePass`** (licença GPL v2+) suporta **`AES/Rijndael`** e **`Twofish`**, *plugins*, e permite compor a *Master Key* com **`Password`**, **`Key file`** ou **`Password + Key file`**. O **`KeePassXC`** (multiplataforma Windows/macOS/Linux) utiliza ficheiros **`.kdbx`** compatíveis e suporta **`AES-256`**, **`ChaCha20`** e **`Twofish`**.

4. **Para que serve o `KeeShare` no `KeePassXC` e como assegura a partilha entre equipas?**

> [!success]- Ver Resposta
> O **`KeeShare`** permite partilhar de forma sincronizada apenas grupos ou entradas específicas de uma base de dados através de um ficheiro contentor (via Dropbox, Google Drive ou Nextcloud), assegurando confidencialidade e integridade com **cifragem ponta a ponta (E2EE)**, **certificado assinado** e **assinaturas criptográficas**.

## Notas relacionadas

- [[Capítulo 2 - Administração de Sistemas]]
- [[Segurança de Passwords, Paradigma xkcd e Diretrizes NIST (2003 vs SP 800-63-4)]]
- [[Higiene de Credenciais - Clean Desk, Google Dorks, PINs e Shoulder Surfing]]
- [[Contingência de Credenciais (Cantor Fitzgerald) e Perguntas de Segurança (Sarah Palin)]]
- [[Recuperação de Clipboard e Sincronização na Timeline]]
- [[Armazenamento Seguro de Passwords (Salting e Key Stretching) e Casos RockYou e LastPass]]
