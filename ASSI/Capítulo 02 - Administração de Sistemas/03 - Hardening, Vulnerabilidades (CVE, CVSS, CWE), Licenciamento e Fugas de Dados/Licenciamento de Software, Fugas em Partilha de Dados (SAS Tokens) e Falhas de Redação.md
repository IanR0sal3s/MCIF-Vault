---
title: Licenciamento de Software, Fugas em Partilha de Dados (SAS Tokens) e Falhas de Redação
tipo: analise
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 2
bloco: 3
fonte_aula: System Administration - System and Data Management.pdf
tags:
  - assi
  - administracao-sistemas
  - licenciamento
  - sas-tokens
  - azure
  - wiz
  - data-breach
  - aima
  - redacao-documentos
aliases:
  - Software Licensing
  - SAS Tokens Microsoft 38TB
  - Falha de Redação de Dados
  - Caso NSA Keygen
  - Caso AIMA E-mails
atualizado: 2026-11-11
---

# Licenciamento de Software, Fugas em Partilha de Dados (SAS Tokens) e Falhas de Redação

A governação de software exige auditoria de licenças (casos **Rafael Quinn** e **NSA**) e prevenção de fugas por **SAS Tokens** na *cloud* (**Microsoft 38 TB**), erros de `CC/BCC` (**AIMA**) e rasuras incorretas.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: O inventário de licenciamento assegura conformidade contratual e rastreabilidade dos binários em execução, enquanto mecanismos de delegação na *cloud* (**Azure SAS Tokens**), clientes de e-mail e editores PDF exigem definição estrita de âmbito (*Blob/Service* vs. *Account*, `BCC` vs. `CC`, eliminação da camada de texto vs. sobreposição visual).
> * **Porque importa (Segurança / Forense)**: Software pirata e *keygens* servem de vetor direto de *malware* e exfiltração (caso do contratado da **NSA**), ao passo que um único *Account-level SAS* publicado no GitHub expôs **38 TB** de backups e segredos da Microsoft. Em perícia e investigação OSINT, documentos mal rasurados preservam integralmente o texto oculto sob retângulos pretos.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Duplo risco da pirataria**: financeiro/legal (**Rafael Quinn**, 75 PCs no Panamá $\to$ `>$100k` multas + `>$100k` licenças) e de cibersegurança (**contratado da NSA**, *keygen* trojanizado + envio de amostras pelo Kaspersky para Moscovo);
>   * **Erro nos *SAS Tokens* (Microsoft AI / Wiz, 2023)**: token configurado ao nível da conta inteira (**`Account-level SAS`**, 18 contentores, validade **2020–2051**) em vez de restrito ao recurso público;
>   * **Rasura incorreta**: desenhar uma caixa preta sobre o texto num PDF não remove o texto subjacente (recuperável via *copy-paste*, `pdftotext` ou `strings`).

---

## 1. Licenciamento de Software e *Due Diligence* (Slides 57–58 + PDF 2 Slide 117)

### 1.1. Obrigações Administrativas (Slide 58)
O administrador de sistemas tem de manter duas práticas contínuas:

1. **Manter todas as licenças de software atualizadas**;
2. **Saber exatamente o que está a ser executado** nas máquinas da organização.

### 1.2. Risco Legal e Financeiro: Caso Rafael Quinn (Panamá — Slide 58)

* Num processo de *software due diligence* durante a aquisição de um *call center* com **75 computadores** no Panamá, detetou-se que um técnico local instalara sistemas operativos e pacotes **Microsoft piratas** ([Publicação de Rafael Quinn](https://x.com/rafaquinn/status/1766847092893298756));
* As autoridades e representantes legais executaram uma inspeção judicial (*raid*);
* **Consequência**: pagamento de **mais de `$100,000 USD` em multas** e **mais de `$100,000 USD` em licenças legítimas**, somado à paralisação operacional.

### 1.3. Risco de Cibersegurança: Contratado da NSA e *Keygen* Trojanizado (PDF 2: Slide 117)
Utilizar software pirata ou ativadores ilegítimos equivale a abrir acesso aos sistemas para atacantes ([CNET — Caso NSA Keygen](https://www.cnet.com/news/nsa-contractors-pirated-microsoft-office-exposed-hacking-tools/)):

* Um funcionário contratado da **NSA (*National Security Agency*)** levou para casa material altamente classificado (ferramentas secretas de *hacking* da agência) e armazenou-o no seu computador pessoal;
* Para instalar uma versão pirata do **Microsoft Office**, utilizou um **`keygen` trojanizado**, desativando temporariamente o antivírus **Kaspersky**;
* Quando o antivírus voltou a ser ativado, detetou o *malware* e os ficheiros suspeitos e enviou amostras para os servidores da Kaspersky em **Moscovo**, onde hackers governamentais russos intercetaram e exfiltraram o arsenal de ferramentas da NSA.

---

## 2. Partilha de Dados Mal Configurada: *SAS Tokens* no Azure (Slides 59–60)

### 2.1. *Account-level SAS* vs. *Blob/Service SAS*
No **Microsoft Azure Storage**, um token **SAS (*Shared Access Signature*)** é um URI assinado criptograficamente que delega acesso a recursos (contentores, *blobs*, filas ou tabelas) com permissões (leitura, escrita, listagem, apagamento) e validade incorporadas no próprio URL, dispensando autenticação adicional.

* **Erro crítico de âmbito**: gerar um **`Account-level SAS`** (para toda a conta de armazenamento) em lugar de um **`Blob/Service SAS`** restrito ao ficheiro público pretendido expõe todos os contentores privados alojados nessa conta.

### 2.2. Caso Microsoft AI Research Descoberto pela `Wiz` (2023 — Slide 60)

* A equipa de investigação em IA da Microsoft publicou no repositório aberto **GitHub** `robust-models-transfer` um link de descarregamento para modelos *open-source* ([Wiz — Exposição SAS 38 TB](https://twitter.com/wiz_io/status/1703759418507026663));
* Contudo, o URL utilizava um **token SAS mal configurado** que concedia acesso a **toda a conta de armazenamento (18 contentores)** com validade estendida de **2020 até outubro de 2051**;
* **Dados privados expostos (`38 TB` adicionais descobertos pela `Wiz`)**:
  1. **Cópias de segurança completas (*backups*)** dos discos pessoais de **dois funcionários** da Microsoft;
  2. **Segredos, palavras-passe e chaves privadas** de serviços internos;
  3. **Mais de `30,000` mensagens internas do Microsoft Teams** pertencentes a **`359` funcionários**.

---

## 3. Violações de Dados Pessoais na Partilha e Redação de Ficheiros (Slide 61)

Três erros operacionais recorrentes originam fugas graves de dados pessoais puníveis ao abrigo do RGPD:

### 3.1. Envio para Destinatários Errados ou Visíveis (`CC` vs. `BCC`)

* **Caso Real em Portugal — AIMA (Setembro de 2024)**: a **AIMA (Agência para a Integração, Migrações e Asilo)** enviou um e-mail sobre cobrança de taxas processuais a **547 cidadãos imigrantes** colocando todos os endereços eletrónicos em campos visíveis (`Para` / `CC`) em vez de `BCC` (*Cópia Oculta*), expondo os contactos pessoais de todos os destinatários entre si.

### 3.2. Falha em Rasurar e Rasura Incorreta (*Incorrectly Redacted Files*)

* Ocorre quando uma organização tenta ocultar nomes, identificadores ou segredos num documento (frequentemente PDF) desenhando apenas um **retângulo preto sobre o texto** sem eliminar a camada de texto subjacente;
* **Recuperação trivial**: qualquer utilizador pode selecionar o texto sob a caixa preta, efetuar ***copy-paste* para o Bloco de Notas** ou correr ferramentas como `pdftotext` e `strings`, recuperando integralmente a informação;
* **Correção obrigatória**: utilizar ferramentas de **redação destrutiva** que eliminam os objetos de texto e metadados subjacentes (e rasterizam a área afetada) antes da publicação.

---

## 4. Bibliografia Recomendada de *System and Data Management* (Slide 62)

* **Brotherston, Lee & Berlin, Amanda (2016)**. *Defensive Security Handbook: Best Practices for Securing Infrastructure*. O'Reilly Media.
* **Bollinger, Jeff, Enright, Brandon & Valites, Matthew (2015)**. *Crafting the InfoSec Playbook*. O'Reilly Media.

---

## Além da aula

* **Extração de Texto Oculto em Ficheiros Mal Rasurados (`ASSI` Cap. 3)**: A análise de documentos publicados com rasura visual incorreta liga-se diretamente às técnicas de extração de cadeias ASCII e UTF-16 do [[Capítulo 3 - YARA - MOTW - Strings]], utilizando [[Conceito de Strings e Comando strings em Unix-Linux]], [[Extração de Strings no Windows - Sysinternals strings e Swiss File Knife (sfk)]] e [[Eric Zimmerman bstrings - Parâmetros, Expressões Regulares e Exercícios]].
* **Exposição Acidental no GitHub e *Google Dorks* (`ASSI` Cap. 2 Bloco 05)**: A publicação pública de tokens SAS no GitHub relaciona-se com a descoberta de credenciais e repositórios mal configurados através de *Google Dorks*, estudada em [[Higiene de Credenciais - Clean Desk, Google Dorks, PINs e Shoulder Surfing]].

---

## Perguntas de revisão

1. **Que dois tipos de risco decorrem da utilização de software não licenciado ou *keygens*, e como os ilustram os casos de Rafael Quinn e da NSA?**

> [!success]- Ver Resposta
> O primeiro é o **risco legal e financeiro**, ilustrado pelo caso de **Rafael Quinn** no Panamá (75 PCs com software Microsoft pirata detetados em *due diligence*, resultando em mais de \$100,000 em multas mais mais de \$100,000 em licenças). O segundo é o **risco de cibersegurança**, ilustrado pelo **contratado da NSA** que usou um `keygen` trojanizado do MS Office após desativar o Kaspersky; ao reativar o antivírus, as amostras enviadas para Moscovo permitiram o roubo de ferramentas classificadas da NSA.

2. **Qual foi a falha técnica na configuração do token SAS no incidente da Microsoft AI Research (2023) e que dados foram expostos nos 38 TB descobertos pela `Wiz`?**

> [!success]- Ver Resposta
> A equipa publicou no GitHub (`robust-models-transfer`) um token **`Account-level SAS`** (para os 18 contentores da conta inteira, com validade de 2020 a 2051) em vez de um token restrito apenas aos ficheiros públicos. Isso expôs **38 TB** de dados privados, incluindo backups completos de discos pessoais de 2 funcionários, segredos/palavras-passe/chaves privadas internas e mais de **30,000 mensagens do Teams de 359 funcionários**.

3. **De que forma um documento PDF com um retângulo preto desenhado sobre informação sensível continua vulnerável a fuga de dados e que caso nacional ilustra falhas de envio de e-mail?**

> [!success]- Ver Resposta
> Um retângulo preto apenas oculta visualmente o texto se não for aplicada redação destrutiva à estrutura do documento; a camada de texto subjacente permanece intacta e pode ser recuperada por simples *copy-paste* ou ferramentas como `pdftotext` e `strings`. No envio de e-mails, o erro de usar `Para`/`CC` em vez de `BCC` é ilustrado pelo caso da **AIMA** (setembro de 2024), que expôs os endereços de **547 cidadãos imigrantes**.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Gestão de Vulnerabilidades, CVE e Sistemas de Pontuação (CVSS e CWE)]] | `Comum/` · `mesmo bloco` |
| **Seguinte** | [[Educação de Utilizadores, Phishing, Spear-Phishing e Reforço Positivo]] | `muda para Bloco 04` |
| **Índice** | [[Capítulo 2 - Administração de Sistemas]] · [[00 ASSI]] | `Bloco 03` |

### Conceitos Relacionados

* [[Decommissioning de Equipamentos, Destruição de Papel (P-1 a P-7) e Enquadramento Legal UE]] · `Bloco 01`
* [[Gestão de Ativos (Asset Management) e Políticas de Armazenamento Amovível (VeraCrypt)]] · `Bloco 02`
* [[Higiene de Credenciais - Clean Desk, Google Dorks, PINs e Shoulder Surfing]] · `Bloco 05`
* [[Conceito de Strings e Comando strings em Unix-Linux]] · `Cap. 3`
* [[Extração de Strings no Windows - Sysinternals strings e Swiss File Knife (sfk)]] · `Cap. 3`
* [[Eric Zimmerman bstrings - Parâmetros, Expressões Regulares e Exercícios]] · `Cap. 3`
