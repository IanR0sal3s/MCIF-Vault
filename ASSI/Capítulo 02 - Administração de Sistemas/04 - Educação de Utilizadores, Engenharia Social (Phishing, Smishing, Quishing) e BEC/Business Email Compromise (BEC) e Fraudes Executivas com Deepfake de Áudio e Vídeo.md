---
title: Business Email Compromise (BEC) e Fraudes Executivas com Deepfake de Áudio e Vídeo
tipo: analise
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 2
bloco: 4
fonte_aula: System Administration - Access Control.pdf
fontes:
  - "https://www.bbb.org/globalassets/local-bbbs/council-113/media/bbb-explosion-of-bec-scams.pdf"
  - "https://tinyurl.com/y4xwb8uj"
  - "https://www.darkreading.com/attacks-breaches/deepfake-audio-scores-35-million-in-corporate-heist"
  - "https://tinyurl.com/5n6zm3dd"
tags:
  - assi
  - administracao-sistemas
  - controlo-acessos
  - bec
  - business-email-compromise
  - deepfake
  - social-engineering
  - rimasauskas
aliases:
  - Business Email Compromise
  - BEC
  - Caso Evaldas Rimasauskas Quanta
  - BEC com Deepfake de Áudio
  - BEC com Deepfake de Vídeo Hong Kong
atualizado: 2026-11-11
---

# Business Email Compromise (BEC) e Fraudes Executivas com Deepfake de Áudio e Vídeo

O **Business Email Compromise (BEC)** explora a personificação de executivos, fornecedores ou advogados sob urgência financeira, combinando hoje e-mails forjados com *deepfakes* de áudio e vídeo em tempo real.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema / Ameaça)**: Os fluxos financeiros corporativos dependem frequentemente da validação humana de ordens por e-mail, voz ou videoconferência; os atacantes exploram essa autoridade e urgência artificial em vez de vulnerabilidades técnicas puras.
> * **Porque importa (Segurança / Forense)**: Mesmo quando a vítima desconfia do e-mail inicial (como no caso de Hong Kong), a clonagem sintética de voz e imagem anula a confirmação visual/auditiva informal, exigindo verificação independente fora de banda (*out-of-band*) e controlos multi-assinatura.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **FBI IC3 (2020)**: 5.º ano consecutivo no **1.º lugar** em perdas; subida de **`$360M` (2016)** para **`$1.8B` (2020)**, com perda média de **`$96,372`** por vítima.
>   * **Evaldas Rimasauskas**: empresa homónima à **`Quanta Computer`** na Letónia e contas na Letónia/Chipre — **`>$100M`** (**`$23M`** Google + **`$98M`** Facebook).
>   * **EAU (`$35M`)**: clonagem de voz via redes neuronais requer hoje **menos de `5 minutos`** de áudio amostrado (vs. **`2–3 horas`** para qualidade máxima).
>   * **Hong Kong (2024, `$25.6M`)**: **`15` transferências** para **`5` contas** após videoconferência ao vivo onde CFO e restantes executivos eram *deepfakes*.

---

## 1. Anatomia, Estatísticas e Modalidades do *Business Email Compromise (BEC)* (Slides 19–22)

### 1.1. Mecanismo, Alvos e Pedidos Típicos (Slide 20)

* **Alvos Diretos**: indivíduos responsáveis por **pagar faturas ou autorizar transferências bancárias** em empresas, organismos públicos e instituições.
* **Personificação de Fonte Fidedigna**: o atacante assume a identidade de uma figura de autoridade ou confiança — **o chefe/CEO, um fornecedor habitual ou um advogado**.
* **Sentido de Urgência**: imposição de pressão temporal extrema para que a vítima atue **imediatamente (*right now*)**, inibindo verificações secundárias.
* **Os 3 Pedidos Típicos num Ataque BEC**:
  1. **Pagar uma fatura** (frequentemente com alteração do IBAN/conta bancária de destino);
  2. **Transferir dinheiro (*wire transfer*)** para uma conta indicada;
  3. **Comprar cartões de oferta (*gift cards*)** em nome do superior e enviar os códigos.
* **Pretextos Clássicos**: um diretor retido no estrangeiro com o cartão cancelado a exigir transferência imediata, ou um fornecedor a pedir liquidação urgente de fatura numa nova conta.

### 1.2. Impacto Económico — Relatório FBI IC3 (Slide 21)
Segundo os relatórios do **FBI *Internet Crime Complaint Center (IC3)***, o BEC constitui a ameaça cibercriminosa mais comum e financeiramente dispendiosa:

* Em **2020**, ocupou pelo **5.º ano consecutivo** o **1.º lugar** em volume de perdas financeiras;
* **Crescimento das Perdas Totais**: passou de **`$360 milhões` (2016)** para **`$1.8 mil milhões` (2020)**;
* **Perda Média por Vítima**: **`$96,372 USD`**.

### 1.3. Quatro Tipos de Fraudes BEC (BBB) e o Caso *Evaldas Rimasauskas* (Slide 22)
O relatório do *Better Business Bureau* ([Relatório BBB sobre BEC](https://www.bbb.org/globalassets/local-bbbs/council-113/media/bbb-explosion-of-bec-scams.pdf)) identifica quatro variantes principais:

1. **CEO Fraud**: o suposto CEO ordena ao CFO (por e-mail ou voz falsa) que transfira fundos;
2. **Fatura de Fornecedor (*Vendor/Supplier Invoice*)**: pedido fraudulento para alterar os dados bancários de pagamento de um fornecedor;
3. **Transações Imobiliárias (*Real Estate / Lawyers*)**: falsos advogados desviam o montante da venda de um imóvel para outra conta;
4. **Compra de *Gift Cards***: pedido a um subordinado para adquirir cartões de oferta em nome do superior.

> [!IMPORTANT] Caso de Estudo: Evaldas Rimasauskas vs. Google e Facebook (`>$100M`)
> * **Execução ([Artigo sobre Evaldas Rimasauskas](https://tinyurl.com/y4xwb8uj))**: O cidadão lituano **Evaldas Rimasauskas** registou na **Letónia** uma empresa com o nome exato da fabricante taiwanesa **`Quanta Computer`**, fornecedora habitual de hardware para centros de dados da **Google** e do **Facebook**.
> * **Engenharia Documental**: Enviou e-mails aos departamentos financeiros de ambas as gigantes fingindo representar a *Quanta*, acompanhados de **faturas e contratos forjados** para pagamento em contas bancárias na **Letónia** e em **Chipre**.
> * **Impacto**: Desviou **mais de `$100 milhões USD`** (cerca de **`$23 milhões`** da Google e **`$98 milhões`** do Facebook) antes da deteção da fraude.

---

## 2. BEC Potenciado por IA: *Deepfake* de Áudio e Vídeo (Slides 23–24)

### 2.1. BEC + *Deepfake* de Áudio: Roubo de `$35 Milhões` nos EAU (Slide 23)
Documentado pelo [Dark Reading — Deepfake Audio USD 35M](https://www.darkreading.com/attacks-breaches/deepfake-audio-scores-35-million-in-corporate-heist):

* **O Ataque**: burlões desviaram **`$35 milhões USD`** combinando **e-mails forjados** com **áudio *deepfake*** para convencer o gerente de uma sucursal bancária nos **Emirados Árabes Unidos (EAU)** de que o diretor de uma empresa cliente autorizava uma transferência para uma aquisição confidencial.
* **Cadeia Técnica**: após e-mails falsos atribuídos ao diretor e a um advogado sediado nos EUA, uma chamada telefónica utilizou **áudio sintético gerado por *machine learning* (redes neuronais)** que replicava com fidelidade a voz do diretor conhecido pelo gerente.
* **Requisitos de Amostragem de Voz**:
  * Especialistas (como Etay Maor) indicam que bastam **menos de `5 minutos` de áudio amostrado** para sintetizar uma voz convincente (enquanto modelos de altíssima qualidade podem usar **`2 a 3 horas`** de áudio bruto, e sínteses básicas exigem ainda menos);
  * Para executivos públicos, o material de treino é recolhido facilmente em entrevistas no YouTube, conferências, *podcasts* e apresentações de resultados.

### 2.2. BEC + Vídeo e Áudio *Deepfake* em Tempo Real: Caso de Hong Kong (`$25.6M` — Slide 24)
Documentado na imprensa internacional ([Caso Hong Kong Deepfake](https://tinyurl.com/5n6zm3dd)):

* **Contexto (2024)**: um funcionário do departamento financeiro em **Hong Kong** recebeu uma mensagem inicial sobre uma transação confidencial — da qual chegou a desconfiar tratar-se de *phishing* — mas aceitou participar numa **videoconferência em direto** com vários interlocutores.
* **Engano Multi-Participante**: na chamada surgiram o **CFO** e outros executivos seniores da empresa conhecidos da vítima; contudo, **todos os participantes exceto a vítima eram recriações *deepfake* de vídeo e áudio em tempo real**, treinadas com registos públicos.
* **Impacto**: convencido pela aparência e voz dos superiores, o funcionário realizou **`15` transferências bancárias** para **cinco contas em Hong Kong**, totalizando **`$25.6 milhões USD`** (cerca de `200 milhões HKD`).

---

## 3. Quadro Comparativo dos 3 Casos Reais de BEC

| Caso Real | Ano / Alvo | Vetor Técnico e Personificação | Pretexto / Mecanismo | Montante Desviado |
| :--- | :--- | :--- | :--- | :--- |
| **Evaldas Rimasauskas** | 2013–2015 / Google e Facebook | E-mails forjados + empresa homónima à **`Quanta Computer`** (Letónia/Chipre) | Faturas e contratos falsos de hardware de *data center* | **`>$100M USD`** (`$23M` Google + `$98M` Facebook) |
| **Sucursal Bancária nos EAU** | 2020–2021 / Gerente bancário (EAU) | E-mails forjados + **áudio *deepfake*** por redes neuronais | Autorização de transferência para aquisição confidencial | **`$35M USD`** |
| **Multinacional em Hong Kong** | 2024 / Funcionário financeiro | Mensagem inicial + **videoconferência ao vivo** com CFO e executivos *deepfake* | Transação secreta validada em chamada multi-participante | **`$25.6M USD`** (`~200M HKD`, `15` transferências) |

---

## Além da aula

* **Controlos Arquiteturais Contra BEC e *Deepfakes***: A confirmação auditiva ou visual em chamadas em direto deixou de garantir autenticidade. A mitigação exige:
  1. **Verificação fora de banda (*out-of-band*)** iniciada pela equipa financeira através de contactos pré-registados independentes;
  2. **Aprovação multi-assinatura** para alterações de IBAN e transferências elevadas;
  3. Autenticação de correio (`SPF`, `DKIM`, `DMARC`) conjugada com autenticação criptográfica forte de sessão como [[Autenticação 2FA (Protocolo TOTP RFC 6238) e Passkeys (FIDO2 - WebAuthn e CTAP)|Passkeys FIDO2]], evitando canais vulneráveis a [[Falhas de Autenticação por SMS - Protocolo SS7, SIM-Jacking, Vishing e StingRay|Vishing e spoofing]].

---

## Perguntas de revisão

1. **Quem são os alvos típicos de um ataque BEC e quais são os três pedidos financeiros mais frequentes?**

> [!success]- Ver Resposta
> O BEC visa colaboradores responsáveis por **pagar faturas ou autorizar transferências bancárias** em empresas ou entidades públicas. Personificando um CEO/chefe, fornecedor ou advogado sob forte sentido de urgência, os atacantes pedem tipicamente: **(1) pagar uma fatura** (com alteração de conta), **(2) efetuar uma transferência bancária (*wire transfer*)**, ou **(3) comprar cartões de oferta (*gift cards*)**.

2. **Qual foi a evolução das perdas por BEC no relatório IC3 do FBI entre 2016 e 2020 e como atuou Evaldas Rimasauskas?**

> [!success]- Ver Resposta
> No relatório IC3 do FBI (2020), o BEC liderou as perdas pelo 5.º ano consecutivo, crescendo de **`$360 milhões` (2016)** para **`$1.8 mil milhões` (2020)**, com uma perda média de **`$96,372 USD` por vítima**. **Evaldas Rimasauskas** registou na Letónia uma empresa homónima à fornecedora **`Quanta Computer`**, enviando faturas e contratos falsos para contas na Letónia e em Chipre que levaram a Google (**`$23M`**) e o Facebook (**`$98M`**) a transferir **`>$100 milhões USD`**.

3. **Como foi executado o roubo de `$35 milhões` nos EAU e que volume de áudio é necessário para clonar a voz de um executivo?**

> [!success]- Ver Resposta
> Os criminosos combinaram e-mails falsos de um diretor e de um advogado nos EUA com uma chamada telefónica usando **áudio *deepfake* gerado por redes neuronais** para convencer um gerente bancário nos EAU a autorizar a transferência. Para criar uma síntese vocal convincente bastam hoje **menos de `5 minutos` de áudio amostrado** (embora sínteses de altíssima fidelidade usem **`2 a 3 horas`**), frequentemente obtido em entrevistas públicas, *podcasts* e YouTube.

4. **Por que razão a vítima do caso de Hong Kong (`$25.6 milhões`, 2024) acabou por executar `15` transferências apesar de ter suspeitado da mensagem inicial?**

> [!success]- Ver Resposta
> Porque foi convidada para uma **videoconferência em direto com múltiplos participantes** onde todos os outros interlocutores (incluindo o **CFO** e outros executivos conhecidos) eram **recriações *deepfake* de vídeo e áudio em tempo real**, dissipando a suspeita inicial e levando-a a realizar **`15` transferências** para **5 contas** em Hong Kong.

## Notas relacionadas

- [[Capítulo 2 - Administração de Sistemas]]
- [[Educação de Utilizadores, Phishing, Spear-Phishing e Reforço Positivo]]
- [[Smishing, Estações SMS Blaster (Downgrade 2G) e Quishing (Códigos QR)]]
- [[Falhas de Autenticação por SMS - Protocolo SS7, SIM-Jacking, Vishing e StingRay]]
- [[Autenticação 2FA (Protocolo TOTP RFC 6238) e Passkeys (FIDO2 - WebAuthn e CTAP)]]
