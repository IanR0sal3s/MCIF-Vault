---
title: Higiene de Credenciais - Clean Desk, Google Dorks, PINs e Shoulder Surfing
tipo: procedimento
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 2
bloco: 5
fonte_aula: System Administration - Access Control.pdf
fontes:
  - "https://github.com/Xyl2k/TSA-Travel-Sentry-master-keys"
  - "https://www.wired.com/2015/09/lockpickers-3-d-print-tsa-luggage-keys-leaked-photos/"
  - "https://www.exploit-db.com/google-hacking-database"
  - "https://medium.freecodecamp.org/discovering-the-hidden-mine-of-credentials-and-sensitive-information-8e5ccfef2724"
  - "https://twitter.com/thorsheim/status/269381568022339584"
  - "https://www.kitploit.com/2018/07/tp-link-defaults-python-script-for.html"
  - "https://www.bbc.com/news/technology-45757528"
tags:
  - assi
  - administracao-sistemas
  - controlo-acessos
  - clean-desk
  - google-dorks
  - ghdb
  - shoulder-surfing
  - default-passwords
  - sextortion
aliases:
  - Clean Desk Policy
  - Google Dorks Trello
  - Shoulder Surfing
  - Email Sextortion
  - California SB-327
atualizado: 2026-11-11
---

# Higiene de Credenciais — *Clean Desk*, *Google Dorks*, PINs e *Shoulder Surfing*

A higiene de credenciais previne fugas físicas e visuais através da política `Clean Desk`, auditoria de *Google Dorks*, mitigação de PINs previsíveis, troca de *default passwords* e defesa contra *shoulder surfing*.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema / Ameaça)**: Palavras-passe fortes falham de imediato se forem expostas em notas adesivas, captadas em fotografias/vídeo, publicadas por erro em quadros indexados por motores de busca, deduzidas por desgaste mecânico ou mantidas com credenciais de fábrica.
> * **Porque importa (Segurança / Forense)**: Controlos operacionais de higiene — sanitização visual do espaço de trabalho, remoção de segredos públicos via `GHDB`, eliminação de *default passwords* (`SB-327`) e filtros de privacidade — fecham vetores triviais frequentemente explorados antes de qualquer ataque técnico complexo.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Fugas em Fotos/Vídeo**: Havai EMA (`2017.07` — *post-it* amarelo, *"Sanitize your environment!"*), `TV5Monde` (`2015` — `"lemotdepassedeyoutube"`), e **7 chaves mestras da `TSA`** reproduzidas por impressão 3D (`CAD`).
>   * **Desgaste de Teclados (`#2 #3 #5 #0`)**: reduz $10^4 = 10\,000$ códigos para apenas **$4! = 24$** (ou $4^4 = 256$ com repetição).
>   * **PINs de 4 dígitos**: **`1234` (>10%)**, `1111`, `0000`, `1212`, datas (`DDMM`/`MMDD`) e linha horizontal **`19xx`/`20xx`**.
>   * ***Email Sextortion***: uso de senha antiga vazada como falsa prova de *trojan* — endereço BTC `1JsACYBoRCYkz7DSgyKurMyibbmHwcHbPd` acumulou **`4257.210 BTC`**.
>   * **Legislação**: Lei da Califórnia **`SB-327` (2018)** proíbe *default passwords* universais em dispositivos ligados à Internet.

---

## 1. Política *Clean Desk* e Fugas em Fotografias e Vídeos (Slides 53–56)

### 1.1. Regras Base de Educação (Slide 53)

* **Nunca deixar palavras-passe escritas à vista**: aplicar o princípio de **Secretária Limpa (*Clean Desk*)** a post-its, cadernos e qualquer documento sensível;
* **Não partilhar palavras-passe**: se alguém solicitar a credencial a um utilizador, este deve reportar de imediato à equipa de TI (salvaguardando apenas procedimentos formais e auditados de partilha de emergência definidos pela organização).

### 1.2. Incidentes Reais em Fotos, Vídeos e Chaves Físicas (Slides 54–56)

* **Agência de Gestão de Emergências do Havai (`2017.07` — Slide 54)**: durante uma entrevista jornalística nas instalações da agência, uma fotografia publicada na imprensa revelou um *post-it* amarelo colado ao monitor com `"Password:"` e a senha real legível $\to$ **Regra operacional**: *"Sanitize your environment!"* antes de visitas ou filmagens.
* **Estação Televisiva `TV5Monde` (`2015` — Slide 55)**: numa entrevista televisiva em direto, atrás do jornalista estavam afixadas folhas com as passwords das redes sociais da estação (sendo visível em alta definição a senha do YouTube **`"lemotdepassedeyoutube"`**), pouco antes de a emissora sofrer um ciberataque grave.
* **Chaves Mestras da `TSA` Impressas em 3D (Slide 56)**: o *Washington Post* publicou inadvertidamente uma fotografia das **7 chaves mestras da TSA** usadas nos aeroportos para abrir malas com fecho *Travel Sentry*. Investigadores converteram a imagem em modelos **`CAD` para impressão 3D** ([GitHub — Xyl2k TSA Master Keys](https://github.com/Xyl2k/TSA-Travel-Sentry-master-keys) e [Wired — TSA 3D Print Keys](https://www.wired.com/2015/09/lockpickers-3-d-print-tsa-luggage-keys-leaked-photos/)), permitindo imprimir chaves físicas funcionais em casa.

---

## 2. Credenciais Expostas na Web e *Google Dorks* (Slides 57–58)

* **`Google Dorks` e `GHDB`**: pesquisas avançadas no motor de busca Google que localizam informação sensível deixada pública por erro de configuração, catalogadas na **Google Hacking Database (`GHDB`)** ([Exploit-DB — GHDB](https://www.exploit-db.com/google-hacking-database)).

**Caso Real — Quadros Públicos do `Trello` (Slide 58):** administradores e programadores deixaram quadros de projeto no **Trello** configurados em modo público ([freeCodeCamp / Medium — Trello Leaks](https://medium.freecodecamp.org/discovering-the-hidden-mine-of-credentials-and-sensitive-information-8e5ccfef2724)), expondo chaves SSH, senhas de servidores e contas de e-mail detetáveis através das consultas:

```text
inurl:https://trello.com AND intext:ssh AND intext:password
inurl:https://trello.com AND intext:@gmail.com AND intext:password
```

---

## 3. Teclados Gastos, Padrões de PINs e *Email Sextortion* (Slides 59–61)

* **Desgaste Físico em Teclados Numéricos (`#2 #3 #5 #0` — Slide 59)**: num terminal de acesso físico em que apenas as teclas `2`, `3`, `5` e `0` mostram desgaste visível na tinta ([Per Thorsheim (Twitter/X)](https://twitter.com/thorsheim/status/269381568022339584)), o espaço de busca de um PIN de 4 dígitos cai de $10^4 = 10\,000$ para apenas **$4! = 24$** combinações sem repetição (ou $4^4 = 256$ admitindo repetições).
* **Mapa de Calor de PINs de 4 Dígitos (Slide 60)**: a análise estatística ($00\text{–}99 \times 00\text{–}99$) evidencia forte enviesamento humano:
  * **`1234`** representa sozinho **mais de `10%`** de todos os PINs, seguido por **`1111`**, **`0000`** e **`1212`**;
  * Datas de nascimento (**`DDMM` / `MMDD`**) e anos de nascimento (**`19xx`** — criando uma linha brilhante entre `1900` e `1999` — e **`20xx`**) concentram grande parte das escolhas restantes.
* **Campanhas de *Email Sextortion* (Slide 61)**: burlões incluem no início do e-mail **uma palavra-passe real antiga da vítima** (recolhida de *data breaches*) como falsa "prova" de infeção por *trojan* e captura de *webcam*, exigindo resgate em Bitcoin. No exemplo da aula, a carteira **`1JsACYBoRCYkz7DSgyKurMyibbmHwcHbPd`** acumulou **`4257.210 BTC`**, equivalentes a **`$230,811,433.47`** em `2021.10.09` e a **`$296,533,621.08`** em `2024.11.02`.

---

## 4. *Default Passwords* (`SB-327`) e *Shoulder Surfing* (Slides 73–75)

### 4.1. Palavras-Passe por Omissão e Lei `SB-327` (Slides 73–74)

* **Risco em Equipamentos de Rede e IoT**: *routers*, *switches*, impressoras, câmaras IP e dispositivos IoT são frequentemente expedidos com credenciais padrão públicas (ex.: `admin/admin`) ou geradores previsíveis explorados por ferramentas como `TP-Link-defaults` ([KitPloit — TP-Link Defaults](https://www.kitploit.com/2018/07/tp-link-defaults-python-script-for.html)).
* **Dever do Administrador**: verificar todos os equipamentos recém-instalados e auditar periodicamente o parque existente para **alterar ou desativar credenciais por omissão**.
* **Califórnia `SB-327` (2018)**: primeira legislação nos EUA a proibir a venda de dispositivos ligados à Internet com passwords padrão universais ([BBC News — California SB-327](https://www.bbc.com/news/technology-45757528)), exigindo senha única por unidade ou alteração obrigatória no primeiro arranque.

### 4.2. *Shoulder Surfing* e Medidas de Proteção (Slide 75)

* **Ameaça**: observação direta por cima do ombro (ou via câmaras/binóculos em comboios, cafés e aeroportos) para capturar PINs, passwords digitadas ou comunicações confidenciais.
* **Controlos de Mitigação**:
  1. **Gestor de passwords** (preenche sem digitação manual visível);
  2. **Autenticação a dois fatores (2FA)**;
  3. **Filtros de privacidade no ecrã** ou, em ambientes de ameaça extrema, cobrir cabeça e teclado com uma manta opaca (**"Blanket of security"**, técnica adotada por **Edward Snowden**).

---

## Além da aula

* **Exposição de Segredos em Repositórios Públicos**: As pesquisas via *Google Dorks* em quadros públicos do Trello integram o mesmo problema estrutural das fugas acidentais de credenciais e tokens em repositórios públicos (como o caso dos *SAS tokens* da Microsoft no GitHub abordado no Bloco 03 deste capítulo), exigindo auditoria contínua e rotação imediata de segredos expostos.
* **Operacionalização e Codificação**: A eliminação de *shoulder surfing* e da reutilização de passwords expostas em *sextortion* apoia-se diretamente em [[Gestores de Passwords (Cloud vs KeePassXC), KeeShare e Copy-Paste Hijacking]] e na verificação de fugas em [[Segurança de Passwords, Paradigma xkcd e Diretrizes NIST (2003 vs SP 800-63-4)]], enquanto a validação dos endereços Bitcoin de extorsão usa [[Codificação Binário-para-Texto (Base16, Base64 e Base58)|Base58Check]].

---

## Perguntas de revisão

1. **O que demonstram os casos da Agência de Emergências do Havai (2017), da `TV5Monde` (2015) e das chaves mestras da `TSA` sobre higiene física e visual?**

> [!success]- Ver Resposta
> Demonstram que segredos escritos em *post-its* ou folhas no campo de visão de câmaras/fotografias (Havai e `TV5Monde` com `"lemotdepassedeyoutube"`) e fotografias de chaves físicas (as 7 chaves mestras da `TSA` convertidas para impressão 3D via `CAD`) comprometem imediatamente a segurança, impondo a política *Clean Desk* e a regra *"Sanitize your environment!"*.

2. **Que consultas *Google Dorks* permitiram localizar credenciais sensíveis em quadros públicos do Trello?**

> [!success]- Ver Resposta
> Através de consultas indexadas na `GHDB` como `inurl:https://trello.com AND intext:ssh AND intext:password` e `inurl:https://trello.com AND intext:@gmail.com AND intext:password`.

3. **Como é que o desgaste físico das teclas `#2 #3 #5 #0` reduz o espaço de busca de um código de 4 dígitos e que padrões dominam os PINs de 4 dígitos?**

> [!success]- Ver Resposta
> O desgaste visível em 4 teclas reduz o universo de $10^4 = 10\,000$ códigos possíveis para apenas **$4! = 24$** combinações (ou $4^4 = 256$ com repetição). Nos PINs de 4 dígitos, **`1234`** representa mais de **`10%`** do total, acompanhado por `1111`, `0000`, `1212`, datas (`DDMM`/`MMDD`) e anos de nascimento **`19xx`** e **`20xx`**.

4. **Como funcionam os ataques de *Email Sextortion* e qual foi o impacto observado na carteira Bitcoin analisada na aula?**

> [!success]- Ver Resposta
> Os atacantes incluem uma palavra-passe real antiga da vítima obtida num *data breach* como falsa prova de que instalaram um *trojan* e gravaram a *webcam*. A carteira Bitcoin monitorizada (`1JsACYBoRCYkz7DSgyKurMyibbmHwcHbPd`) acumulou **`4257.210 BTC`** (`$230,811,433.47` em `2021.10.09`, valorizados em `$296,533,621.08` em `2024.11.02`).

5. **O que exige a lei da Califórnia `SB-327` (2018) sobre *default passwords* e que medidas mitigam o *Shoulder Surfing*?**

> [!success]- Ver Resposta
> A lei `SB-327` proíbe vender dispositivos ligados à Internet com passwords por omissão universais, exigindo uma senha única de fábrica ou definição obrigatória no primeiro arranque. Para prevenir *Shoulder Surfing*, recorre-se a **gestores de passwords**, **2FA**, **filtros de privacidade** e, em cenários extremos, à técnica *"Blanket of security"* usada por Edward Snowden.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Caso de Estudo Coldcard (1800 BTC) - Falha de Entropia e Reconstrução de Seeds]] | `mesmo bloco` |
| **Seguinte** | [[Gestores de Passwords (Cloud vs KeePassXC), KeeShare e Copy-Paste Hijacking]] | `mesmo bloco` |
| **Índice** | [[Capítulo 2 - Administração de Sistemas]] · [[00 ASSI]] | `Bloco 05` |

### Conceitos Relacionados

* [[Segurança de Passwords, Paradigma xkcd e Diretrizes NIST (2003 vs SP 800-63-4)]] · `mesmo bloco`
* [[Contingência de Credenciais (Cantor Fitzgerald) e Perguntas de Segurança (Sarah Palin)]] · `mesmo bloco`
* [[Codificação Binário-para-Texto (Base16, Base64 e Base58)]] · `AFD1 · Cap. 3`
