---
title: Smishing, Estações SMS Blaster (Downgrade 2G) e Quishing (Códigos QR)
tipo: analise
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 2
bloco: 4
fonte_aula: System Administration - Access Control.pdf
fontes:
  - "https://www.wired.com/story/usps-scam-text-smishing-triad/"
  - "https://x.com/sickcodes/status/1859979785847570718"
  - "https://www.youtube.com/watch?v=LELn9cpMvs4"
tags:
  - assi
  - administracao-sistemas
  - controlo-acessos
  - smishing
  - sms-blaster
  - 2g
  - quishing
  - qr-code
  - smishing-triad
aliases:
  - Smishing
  - SMS Blaster
  - Smishing Triad
  - Quishing
  - Phishing por QR Code
atualizado: 2026-11-11
---

# Smishing, Estações SMS Blaster (Downgrade 2G) e Quishing (Códigos QR)

O smishing por SMS e estações rádio `2G` (`SMS Blaster`) e o quishing por códigos QR contornam filtros tradicionais de correio eletrónico para recolher credenciais e dados financeiros em dispositivos móveis.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema / Ameaça)**: O SMS apresenta taxas de abertura muito superiores ao e-mail e o protocolo celular `2G` carece de cifragem e autenticação de torre; já os códigos QR encapsulam URLs em imagens, iludindo filtros de texto e desviando o acesso para telemóveis pessoais fora do perímetro corporativo.
> * **Porque importa (Segurança / Forense)**: Distinguir o *quishing* web (`https://...`) dos códigos QR criptográficos legítimos (`otpauth://` e `FIDO:/`) e desativar a banda `2G` no sistema operativo móvel reduz drasticamente o sequestro de sessões e a fraude financeira.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Smishing**: **`98%`** de abertura vs. **`20%`** no e-mail; **`60%`** lidos em **`1–5 minutos`**; **`4.5x`** mais probabilidade de resposta.
>   * **`Smishing Triad`**: `100,000` SMS/dia (USPS), **`438,669`** cartões únicos em **`1,133`** domínios, `50,000+` e-mails e **`20`** domínios governamentais/militares.
>   * **`SMS Blaster`**: usa *Cell Broadcast*, não precisa dos números das vítimas, atrai pelo sinal mais forte, força ***downgrade* para `2G`** sem cifragem nem autenticação (*Sender ID spoofing*) — mitigável no **`Android 12+`**.
>   * **Quishing (Trellix, 4 passos)**: transfere o clique do PC corporativo para o smartphone e captura credenciais e *tokens* 2FA via *proxy* AitM.

---

## 1. Smishing (`SMS` + `Phishing`) e o Caso *Smishing Triad* (Slides 10–13)

### 1.1. Definição, Métricas e Cadeia de Ataque (Slide 11)

* **Smishing**: ataque de *phishing* por mensagens de texto (`SMS` + `phishing`) desenhado para obter credenciais, dados pessoais ou informação bancária.
* **Eficácia Comparada ao E-mail**:
  * **Taxa de abertura de `98%`**, muito acima do e-mail (**`20%`**);
  * **`60%`** dos destinatários abrem o SMS entre **`1 a 5 minutos`** após a receção;
  * Probabilidade **`4.5 vezes` superior de resposta** face ao correio eletrónico.
* **As 4 Etapas do Ataque de Smishing**:
  1. **Distribute (Envio)**: difusão de um SMS urgente (encomenda retida, bloqueio bancário, portagem);
  2. **Deceive (Engano)**: a vítima abre a ligação incluída na mensagem;
  3. **Harvest (Recolha)**: a página falsa capta credenciais ou dados de cartão de crédito;
  4. **Exploit (Exploração)**: monetização financeira ou tomada de controlo da conta.

### 1.2. Caso de Estudo: *Smishing Triad* e Domínios Reais (Slides 12–13)
Documentado pela [Wired — Smishing Triad](https://www.wired.com/story/usps-scam-text-smishing-triad/), o grupo **Smishing Triad** ilustra a industrialização deste vetor:

* **Volume e Pretexto (USPS)**: envio de até **`100,000` SMS fraudulentos por dia** alegando falhas na entrega de encomendas (*"The United States Postal Service is trying to deliver a parcel but needs more details, including your credit card number"*);
* **Impacto Quantificado**:
  * Recolha de **`438,669` cartões de crédito únicos** através de **`1,133` domínios** operados pelos atacantes;
  * Registo de **mais de `50,000` endereços de e-mail**, incluindo centenas de contas universitárias e **`20` domínios militares ou governamentais**.
* **Exemplos Reais de Domínios Utilizados (Slide 13)**:
  * `nycitypayinvoice[.]com`
  * `southernconnectortolls[.]com`
  * `uspsmailupdate[.]com`
  * `gapeachpasstolls[.]com`
  * `paturnpikeinvoices[.]com`
  * `bcpay-infraction[.]com`
  * `us-courtweb[.]com`

---

## 2. Smishing em Larga Escala via `SMS Blaster` (*Downgrade* para `2G` — Slides 14–15)

### 2.1. Arquitetura Técnica e Mitigação no `Android 12+` (Slide 14)
Ao contrário do smishing tradicional dependente de listas telefónicas e *gateways* comerciais, um **`SMS Blaster`** é uma estação base celular portátil (transportada numa mochila ou automóvel):

1. **Difusão Geográfica (*SMS Cell Broadcast*)**: injeta mensagens em todos os telemóveis dentro de um perímetro físico;
2. **Sem Alvo Numérico Prévio**: **não precisa de conhecer os números de telefone** das vítimas;
3. **Imitação de Torre e *Downgrade* para `2G`**:
   * Emite um sinal rádio de elevada potência para captar automaticamente os telemóveis próximos, que se associam à antena com o **sinal mais forte**;
   * Força o ***downgrade* para o protocolo `2G` (GSM)**, que **não utiliza cifragem** e **permite entregar SMS diretamente sem autenticação da rede**, possibilitando ainda *Sender ID spoofing* (inserindo mensagens no histórico legítimo de bancos ou serviços postais).
4. **Mitigação Nativa**: o **`Android 12+`** (versão 12 ou superior) disponibiliza nas definições de rede móvel um interruptor para **desligar completamente o suporte a `2G`**.

### 2.2. Caso Real em Banguecoque, Tailândia (Slide 15)
Documentado por Sick Codes ([Sick Codes (X)](https://x.com/sickcodes/status/1859979785847570718) e [Vídeo Sick Codes (YouTube)](https://www.youtube.com/watch?v=LELn9cpMvs4)):

* Autoridades tailandesas detiveram operadores que circulavam por zonas comerciais de **Banguecoque** com um `SMS Blaster` alimentado por bateria e inversor na bagageira de uma viatura;
* O sistema debitava cerca de **`100,000` SMS por hora** (alcançando **`1,000,000` de mensagens** num raio de **`3 km`**), personificando bancos e programas governamentais.

---

## 3. Quishing — Phishing com Códigos QR (Slides 16–18)

### 3.1. Evasão de Filtros e Mudança de Perímetro (Slide 16)

* **Quishing (`QR codes` + `phishing`)**: uso de códigos QR para encaminhar vítimas para páginas maliciosas ou descargas nocivas.
* **Dupla Vantagem para o Atacante**:
  * Encapsular o URL numa imagem QR evita que analisadores textuais *anti-phishing* do servidor de correio inspecionem o endereço malicioso;
  * Ao ler o código com a **câmara do smartphone pessoal**, a vítima abandona o computador corporativo e as suas proteções de rede/endpoint, navegando frequentemente fora do perímetro empresarial.

### 3.2. Cadeia de Ataque em 4 Passos (Trellix — Slides 17–18)
Segundo o modelo da *Trellix* (*"Scanning Danger: Unmasking the Threats of Quishing"*):

1. **E-mail com Código QR**: envio de falso aviso de entrega falhada (**FedEx**, **DHL**), atualização obrigatória de MFA **Microsoft 365** ou falsa multa/infração;
2. **Leitura no Telemóvel**: a vítima lê o código QR do ecrã do PC com o smartphone e abre o URL oculto;
3. **Recolha de Credenciais e Tokens**: a página fraudulenta (muitas vezes operando como *adversary-in-the-middle proxy*) capta utilizador, palavra-passe e **tokens de sessão/2FA**;
4. **Account Takeover**: o atacante assume o controlo da conta corporativa.

---

## 4. Comparação: Smishing Tradicional vs. `SMS Blaster 2G` vs. Quishing

| Dimensão | Smishing Tradicional | Estação `SMS Blaster` (`2G`) | Quishing (Códigos QR) |
| :--- | :--- | :--- | :--- |
| **Vetor de Entrega** | Redes móveis públicas / *gateways* SMS. | Torre celular falsa portátil (*Cell Broadcast*). | Imagem com código QR dentro de e-mail ou documento. |
| **Dependência de Lista de Contactos** | Requer números de telefone das vítimas. | **Não necessita dos números** (atinge toda a área rádio). | Requer endereço de e-mail da vítima. |
| **Mecanismo de Evasão / Exploração** | Alta taxa de abertura (`98%`) e urgência social. | Sinal mais forte + *downgrade* `2G` sem cifragem nem autenticação + *Sender ID spoofing*. | Imagem escapa a filtros de URL no e-mail + transição para telemóvel fora da rede corporativa. |
| **Exemplo / Escala** | `Smishing Triad`: `100,000`/dia, `438,669` cartões em `1,133` domínios. | Banguecoque: `100,000`/hora, até `1,000,000` em `3 km`. | Falsos avisos FedEx, DHL, MFA Microsoft 365 e multas. |
| **Defesa Principal** | Educação, verificação de domínios e MFA resistente a *phishing*. | **Desativar `2G`** nas definições de rede (`Android 12+`). | Inspeção de imagens QR no *gateway* de e-mail e **Passkeys (`FIDO2`)**. |

---

## Além da aula

* **Códigos QR Maliciosos (`Quishing`) vs. Códigos QR Legítimos (`TOTP` e `Passkeys`)**: É essencial distinguir um QR de *quishing* (URL `https://...` aberto no navegador Web) dos usos legítimos em [[Autenticação 2FA (Protocolo TOTP RFC 6238) e Passkeys (FIDO2 - WebAuthn e CTAP)]]:
  1. No registo **TOTP (`RFC 6238`)**, o QR (`otpauth://totp/...`) transfere a chave secreta Base32 para a aplicação autenticadora;
  2. Na autenticação *cross-device* com **Passkeys (`FIDO2`)**, o QR (`FIDO:/...`) contém um desafio único e exige **proximidade física via Bluetooth** entre o computador e o smartphone, bloqueando ataques remotos.
* **Relação com Intercetores `StingRay`**: A captura por torre falsa e *downgrade* para `2G` do `SMS Blaster` assenta no mesmo princípio rádio dos equipamentos **`StingRay`**, tratados em [[Falhas de Autenticação por SMS - Protocolo SS7, SIM-Jacking, Vishing e StingRay]] e nas ameaças em viagens em [[Ataques Físicos em Viagens - Evil Maid (FlowCloud) e Burner Phones]].

---

## Perguntas de revisão

1. **Que estatísticas explicam a elevada eficácia do *smishing* face ao e-mail e quais são as quatro etapas típicas deste ataque?**

> [!success]- Ver Resposta
> O SMS apresenta **`98%`** de taxa de abertura (contra **`20%`** no e-mail), **`60%`** das mensagens são lidas entre **1 e 5 minutos** após a receção e existe uma probabilidade **`4.5 vezes` maior de resposta**. O ataque segue 4 etapas: **Distribute** (envio), **Deceive** (clique no link), **Harvest** (recolha de credenciais/cartões) e **Exploit** (exploração financeira ou sequestro de conta).

2. **Qual foi a dimensão e o impacto da rede *Smishing Triad*?**

> [!success]- Ver Resposta
> Operando sobretudo com o pretexto de encomendas da **USPS**, a *Smishing Triad* enviou até **`100,000` SMS por dia**, capturando **`438,669` cartões de crédito únicos** em **`1,133` domínios**, além de mais de **`50,000` endereços de e-mail** (incluindo **`20` domínios governamentais ou militares**).

3. **Como funciona tecnicamente uma estação `SMS Blaster`, que impacto atingiu em Banguecoque e como pode ser mitigada em smartphones?**

> [!success]- Ver Resposta
> Um `SMS Blaster` simula uma torre celular de sinal dominante para capturar os telemóveis na área e força o ***downgrade* para `2G`**, permitindo enviar mensagens via *Cell Broadcast* sem conhecer os números das vítimas, sem cifragem, sem autenticação de rede e com *Sender ID spoofing*. Em Banguecoque, debitou **`100,000` SMS/hora** (até **`1,000,000`** num raio de **`3 km`**). A mitigação no **`Android 12+`** consiste em desligar a conectividade **`2G`** nas definições de rede móvel.

4. **Por que razão o *quishing* consegue contornar as defesas corporativas de correio eletrónico e em que difere do QR usado em Passkeys `FIDO2`?**

> [!success]- Ver Resposta
> Ao ocultar o URL dentro de uma imagem QR, o atacante evita os filtros textuais de URL do servidor de e-mail e leva o utilizador a abrir o link no seu smartphone pessoal, fora do perímetro protegido da empresa. Ao contrário do *quishing* (`https://...`), um QR de **Passkeys (`FIDO2`)** usa o esquema `FIDO:/...` e exige verificação de proximidade via **Bluetooth**, impedindo ataques à distância.

## Notas relacionadas

- [[Capítulo 2 - Administração de Sistemas]]
- [[Educação de Utilizadores, Phishing, Spear-Phishing e Reforço Positivo]]
- [[Business Email Compromise (BEC) e Fraudes Executivas com Deepfake de Áudio e Vídeo]]
- [[Falhas de Autenticação por SMS - Protocolo SS7, SIM-Jacking, Vishing e StingRay]]
- [[Autenticação 2FA (Protocolo TOTP RFC 6238) e Passkeys (FIDO2 - WebAuthn e CTAP)]]
- [[Ataques Físicos em Viagens - Evil Maid (FlowCloud) e Burner Phones]]
