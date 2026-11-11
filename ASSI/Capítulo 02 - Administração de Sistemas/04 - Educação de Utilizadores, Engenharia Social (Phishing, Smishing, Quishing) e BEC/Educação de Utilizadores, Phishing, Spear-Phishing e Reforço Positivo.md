---
title: Educação de Utilizadores, Phishing, Spear-Phishing e Reforço Positivo
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 2
bloco: 4
fonte_aula: System Administration - Access Control.pdf
fontes:
  - "https://research.google.com/pubs/pub46437.html"
  - "http://www.zdnet.com/article/criminals-push-malware-by-losing-usb-sticks-in-parking-lots/"
  - "https://www.newyorker.com/magazine/2017/03/06/trump-putin-and-the-new-cold-war"
tags:
  - assi
  - administracao-sistemas
  - controlo-acessos
  - user-education
  - phishing
  - spear-phishing
  - keyloggers
  - road-apples
  - positive-reinforcement
aliases:
  - User Education
  - Phishing e Spear-Phishing
  - Road Apples
  - Reforço Positivo em Cibersegurança
  - Caso NATO Cabul 2008
atualizado: 2026-11-11
---

# Educação de Utilizadores, Phishing, Spear-Phishing e Reforço Positivo

A educação contínua de utilizadores combina treino prático com testes periódicos para mitigar phishing, spear-phishing, keyloggers e *"road apples"*, sustentada por uma cultura de reforço positivo.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema / Ameaça)**: Os atacantes exploram a propensão humana para confiar e a ausência de hábitos defensivos, utilizando engenharia social, páginas falsas, suborno a internos e suportes físicos contaminados para contornar barreiras técnicas e redes isoladas.
> * **Porque importa (Segurança / Forense)**: Sem o ciclo contínuo `Train + test` e sem uma política não punitiva integrada na Resposta a Incidentes, as vítimas ocultam compromissos iniciais, atrasando a contenção e a recolha de artefactos críticos (`MOTW`, `.LNK`, `USBSTOR`).
> * **Pontos Críticos e Armadilhas para Exame**:
>   * Estudo **Thomas et al. (2017)**: `250,000` logins/semana, `788,000` por *keyloggers*, `12M` via *phishing*, `1.9B` em *data breaches* e apenas **`3.1%`** de adoção de 2FA após recuperação.
>   * **Verizon DBIR 2017**: **`95%`** dos ataques de *phishing* bem-sucedidos instalam software; **`81%`** das violações por *hacking* exploram passwords roubadas ou fracas.
>   * **Caso Cabul (2008)**: infeção da rede militar classificada *air-gapped* com **`Agent.btz`** via pens USB baratas vendidas em quiosques junto ao QG da NATO.
>   * Regra de ouro do reforço positivo: *"better to report a false positive than to let go a true problem"*.

---

## 1. Dimensão Empírica do Roubo de Credenciais (Thomas et al., 2017 — Slide 3)

O estudo científico conduzido pela Google e pela UC Berkeley entre março de 2016 e março de 2017 — K. Thomas et al. (2017), *"Data Breaches, Phishing, or Malware? Understanding the Risks of Stolen Credentials"*, publicado na 24.ª ACM CCS ([Estudo Google / UC Berkeley (CCS 2017)](https://research.google.com/pubs/pub46437.html)) — quantificou a escala real do roubo de credenciais:

| Vetor de Comprometimento / Métrica | Volume Registado (Março 2016 – Março 2017) |
| :--- | :--- |
| **Logins válidos roubados por semana** | **`250,000`** combinações válidas de utilizador e palavra-passe por semana |
| **Credenciais roubadas via `Keyloggers`** | **`788,000`** credenciais capturadas por *malware* de registo de teclas |
| **Credenciais roubadas via `Phishing`** | **`12 milhões`** (`12,000,000`) de credenciais recolhidas por páginas falsas |
| **Credenciais expostas em `Data Breaches`** | **`1.9 mil milhões`** (`1,900,000,000`) de credenciais divulgadas em fugas de dados |
| **Adoção de 2FA após recuperação da conta** | Apenas **`3.1%`** dos utilizadores cujas contas foram sequestradas ativaram 2FA após recuperarem o acesso |

---

## 2. Utilizadores como Alvos: Engenharia Social, Suborno, *Phishing* e *Spear-Phishing* (Slides 4–5)

### 2.1. Vetores contra Utilizadores Regulares (Slide 4)

* Os utilizadores comuns são alvos diretos de **Phishing** e **Ransomware**.
* Os atacantes recorrem frequentemente à **engenharia social** para obter acesso inicial, explorando a tendência natural dos seres humanos para confiar.
* **Suborno a Pessoal Interno (*Bribe Inside Personnel*)**: em certos cenários, os criminosos abordam diretamente colaboradores para comprar acesso interno (caso reportado pela BBC de um especialista em TI abordado por atacantes num bar em Londres com oferta monetária para instalar *malware* na empresa).

### 2.2. *Phishing* vs. *Spear-Phishing* (Slide 5)
O *phishing* engloba ataques concebidos para induzir as vítimas a revelar informação confidencial (credenciais, dados bancários), tendo evoluído de campanhas genéricas para alvos cirúrgicos:

| Critério | *Phishing* Clássico (Em Massa) | *Spear-Phishing* (Direcionado) |
| :--- | :--- | :--- |
| **Alcance e Seleção** | Envio genérico em massa para milhares de endereços sem personalização. | Altamente direcionado a indivíduos ou funções específicas dentro de uma organização. |
| **Pretexto e Remetente** | Remetentes genéricos ou pré-fabricados (ex.: burlas antigas de *"príncipes"* a pedir transferências bancárias). | Aparenta provir de uma pessoa conhecida da vítima (colega, superior hierárquico ou parceiro habitual). |
| **Capacidade de Deteção** | Facilmente sinalizado por utilizadores com formação básica e filtros automáticos. | **Extremamente difícil de detetar mesmo por utilizadores treinados e educados**, exigindo verificação adicional. |

---

## 3. Como Educar Utilizadores: `Train + Test`, Proibição de *"Road Apples"* e Caso NATO/Cabul (Slides 6–7, 9)

### 3.1. Educar vs. Apenas Treinar (`Train + test` — Slide 6)

* Os utilizadores precisam de ser **educados continuamente**, e não submetidos apenas a ações pontuais de formação.
* **Abordagem `Train + test`**: o conhecimento teórico não exercitado dissipa-se rapidamente; por isso, a formação deve ser combinada com simulações periódicas e testes práticos de *phishing*.
* **Estatísticas do *Verizon Data Breach Investigations Report (DBIR 2017)***:
  * **`95%`** dos ataques de *phishing* que originaram uma violação de dados foram seguidos de **instalação de software**;
  * **`62%`** das violações envolveram *hacking*, **`51%`** envolveram *malware* e **`81%`** das violações associadas a *hacking* exploraram **palavras-passe roubadas e/ou fracas**;
  * **`43%`** das violações envolveram **engenharia social**.

### 3.2. Regras Estritas contra *"Road Apples"* e o Caso NATO/Cabul (Slides 7 e 9)
As organizações devem impor proibições estritas contra comportamentos perigosos, destacando-se a interdição absoluta de ligar pens USB ou suportes desconhecidos — técnica conhecida em testes de intrusão como ***"road apples"*** ([ZDNet — USB Drop Attacks](http://www.zdnet.com/article/criminals-push-malware-by-losing-usb-sticks-in-parking-lots/)):

* **Exemplos Típicos de *"Road Apples"***:
  1. Venda de pens USB baratas (previamente infetadas com *spyware*) nas imediações da organização-alvo;
  2. Um CD abandonado com a inscrição manuscrita *"Vacation photos"*;
  3. Uma pen USB deixada deliberadamente no parque de estacionamento ou num corredor.
* **Caso Histórico Real — Rede Classificada do Pentágono / NATO em Cabul (2008 — Slide 9)**:
  * Documentado na obra *Dark Territory* de Fred Kaplan ([The New Yorker — Fred Kaplan](https://www.newyorker.com/magazine/2017/03/06/trump-putin-and-the-new-cold-war));
  * Em **2008**, atacantes russos comprometeram uma rede militar classificada dos EUA totalmente desligada da Internet pública (*air-gapped*);
  * **Execução**: forneceram **pens USB baratas infetadas com o vírus `Agent.btz` a quiosques de venda a retalho junto ao quartel-general da NATO em Cabul (Afeganistão)**, antecipando que um militar norte-americano compraria uma unidade e a ligaria a um terminal seguro.

---

## 4. Reforço Positivo e Resposta a Incidentes (Slide 8)

Adotar uma cultura punitiva perante erros humanos compromete diretamente a defesa organizacional:

* **Princípio do Reforço Positivo**:
  * Transmitir aos utilizadores que cair num ataque de *phishing* ou *ransomware* pode acontecer e não implica sanção disciplinar;
  * **Punir ou envergonhar as vítimas faz apenas com que escondam incidentes futuros**, prolongando o tempo de permanência do atacante na rede.
* **Integração no Procedimento de Resposta a Incidentes (*Incident Response*)**:
  * Perante qualquer anomalia, o utilizador deve sentir confiança para **alertar imediatamente a equipa de TI**;
  * **Regra de ouro**: *"better to report a false positive than to let go a true problem"* (é sempre preferível reportar um falso positivo do que deixar passar um problema verdadeiro);
  * O canal de reporte deve integrar formalmente o procedimento de **Resposta a Incidentes**, devendo a organização **recompensar** os utilizadores que reportem suspeitas legítimas.

---

## Além da aula

* **Articulação com Ataques USB (`BadUSB` e `.LNK`) e Perícia Forense (`ASSI` Cap. 1 e Cap. 2)**: A técnica de *"road apples"* e o caso `Agent.btz` ligam-se diretamente aos vetores físicos tratados em [[Vetores de Ataque USB (BadUSB, Rubber Ducky, LNK, USB-Killer) e Defesas (GPO, Pad Jack, ESD Dogs)]], ao abuso de atalhos em [[Abuso e Vetores de Ataque com Ficheiros LNK]] e ao rasto pericial no Registry analisado em [[Artefactos Forenses de Dispositivos USB]].
* **Proveniência de Ficheiros Descarregados em Phishing (`ASSI` Cap. 3 Bloco 02)**: Como `95%` das violações originadas por *phishing* desencadeiam instalação de software, a defesa no Windows apoia-se na marcação de origem [[Mark of the Web (MOTW) e Zone.Identifier - Formato, Zonas URLZONE e Verbosidade dos Browsers|Mark of the Web (MOTW)]] e no controlo [[Exceções à MOTW (Ficheiros Compactados, 7-Zip, certutil LOLBin) e Microsoft Defender SmartScreen|Microsoft Defender SmartScreen]].

---

## Perguntas de revisão

1. **Quais são os principais números do estudo de Thomas et al. (2017) relativos ao roubo semanal de logins, keyloggers, phishing, data breaches e adoção de 2FA?**

> [!success]- Ver Resposta
> O estudo registou **`250,000`** logins válidos roubados por semana, **`788,000`** credenciais capturadas por *keyloggers*, **`12 milhões`** via *phishing*, **`1.9 mil milhões`** expostas em *data breaches*, e verificou que apenas **`3.1%`** das vítimas ativaram 2FA após recuperarem a conta.

2. **O que distingue o *phishing* clássico do *spear-phishing* e qual o papel da metodologia `Train + test` face aos dados do Verizon DBIR 2017?**

> [!success]- Ver Resposta
> Enquanto o *phishing* clássico usa e-mails genéricos em massa, o *spear-phishing* imita remetentes conhecidos da vítima (colegas, chefias, parceiros), sendo difícil de detetar mesmo por pessoal formado. A metodologia `Train + test` reforça a teoria com simulações práticas contínuas, crucial porque **`95%`** das violações iniciadas por *phishing* resultam em instalação de software e **`81%`** das intrusões exploram palavras-passe roubadas ou fracas (com `43%` envolvendo engenharia social).

3. **O que são *"road apples"* e como foi comprometida a rede classificada do Pentágono em Cabul em 2008?**

> [!success]- Ver Resposta
> *"Road apples"* são suportes físicos contaminados (pens USB ou CDs como *"Vacation photos"*) deixados ou vendidos junto ao alvo para explorar a curiosidade humana. Em 2008, agentes russos abasteceram quiosques perto do QG da NATO em Cabul com pens USB baratas infetadas com o vírus **`Agent.btz`**, conseguindo entrar numa rede militar *air-gapped* quando um militar ligou uma dessas pens a um terminal classificado.

4. **Por que razão punir utilizadores que clicam em *phishing* agrava o risco de segurança e como deve funcionar o reforço positivo?**

> [!success]- Ver Resposta
> Punir ou envergonhar vítimas leva-as a esconder futuros incidentes por receio de represálias, atrasando a contenção. O reforço positivo integra o reporte no procedimento de **Resposta a Incidentes**, recompensa quem alerta atempadamente a equipa de TI e aplica o princípio *"better to report a false positive than to let go a true problem"*.

## Notas relacionadas

- [[Capítulo 2 - Administração de Sistemas]]
- [[Smishing, Estações SMS Blaster (Downgrade 2G) e Quishing (Códigos QR)]]
- [[Business Email Compromise (BEC) e Fraudes Executivas com Deepfake de Áudio e Vídeo]]
- [[Vetores de Ataque USB (BadUSB, Rubber Ducky, LNK, USB-Killer) e Defesas (GPO, Pad Jack, ESD Dogs)]]
- [[Abuso e Vetores de Ataque com Ficheiros LNK]]
- [[Artefactos Forenses de Dispositivos USB]]
- [[Mark of the Web (MOTW) e Zone.Identifier - Formato, Zonas URLZONE e Verbosidade dos Browsers]]
- [[Exceções à MOTW (Ficheiros Compactados, 7-Zip, certutil LOLBin) e Microsoft Defender SmartScreen]]
