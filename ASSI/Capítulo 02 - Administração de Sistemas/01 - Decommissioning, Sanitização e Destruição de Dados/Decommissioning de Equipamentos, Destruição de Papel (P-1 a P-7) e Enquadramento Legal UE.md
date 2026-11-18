---
title: Decommissioning de Equipamentos, Destruição de Papel (P-1 a P-7) e Enquadramento Legal UE
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 2
bloco: 1
fonte_aula: System Administration - System and Data Management.pdf
tags:
  - assi
  - administracao-sistemas
  - decommissioning
  - data-disposal
  - din-66399
  - weee
  - rohs
  - gdpr
aliases:
  - Decommissioning
  - Destruição de Papel P-1 a P-7
  - UNSHREDDER
  - WEEE RoHS GDPR
  - Morgan Stanley Data Disposal
atualizado: 2026-11-11
---

# Decommissioning de Equipamentos, Destruição de Papel (P-1 a P-7) e Enquadramento Legal UE

O **Decommissioning** retira sistemas e equipamentos de operação ativa garantindo remoção segura de peças, eliminação de dados (papel `P-1` a `P-7` e suportes digitais) e conformidade com WEEE, RoHS e RGPD.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: Todos os equipamentos e documentos atingem o fim de vida operacional ou económica; sem um procedimento formal de abate e triagem por criticidade (*staging for disposal*), hardware obsoleto, impressoras multifunções e arquivos em papel abandonam a organização com dados residuais intactos.
> * **Porque importa (Segurança / Forense)**: O descarte negligente alimenta ataques de *Dumpster Diving*, fugas massivas no mercado secundário (como nos casos **MIT** e **Morgan Stanley**) e sanções severas sob o **RGPD**. Em perícia e contraespionagem, tiras de papel mal trituradas e discos internos de fotocopiadoras permitem reconstrução documental integral (ex.: sistema `UNSHREDDER`).
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Lixo na via pública**: a partir do momento em que é colocado na rua para recolha, torna-se geralmente aberto ao público para terceiros e *pentesters*;
>   * **Classes DIN 66399**: trituradoras de tiras (`P-1` e `P-2`) permitem reconstrução humana ou computacional, exigindo corte cruzado/microcorte (`P-4` a `P-7`) para informação sensível e secreta;
>   * **Multifunções e RGPD**: impressoras e fotocopiadoras possuem **memória não volátil e discos rígidos internos** que têm de ser apagados antes do abate; as coimas do RGPD atingem **20 milhões de euros ou 4% do volume de negócios anual global** (o valor mais elevado).

---

## 1. Conceito de *Decommissioning* e Triagem por Criticidade (Slides 2–4)

### 1.1. Definição, Âmbito e Três Garantias (`Decommissioning #0`)
O **Decommissioning** consiste na retirada formal de um equipamento, sistema, instalação ou ativo de serviço ou operação ativa quando este deixa de ser necessário, eficaz, seguro ou viável, aplicando-se desde infraestruturas industriais e nucleares até sistemas de TI obsoletos.

Durante o processo, a organização deve assegurar **três garantias fundamentais**:

1. **Remoção segura de componentes**: desmontagem controlada sem exposição acidental de peças perigosas ou reutilizáveis;
2. **Eliminação de dados sensíveis**: sanitização ou destruição verificada de toda a informação armazenada antes da saída do ativo;
3. **Minimização dos impactos ambientais**: encaminhamento correto de componentes perigosos e resíduos eletrónicos.

### 1.2. Triagem por Classes de Dados (`Decommissioning #1`)
O fim de vida em TI constitui uma etapa crítica de segurança pelo risco de exposição de dados confidenciais, exigindo **triagem prévia (*staging for disposal*)** consoante a sensibilidade da informação:

* **Classes de dados menos críticas**: uma limpeza lógica simples do armazenamento (*simple data storage wipe*) pode ser suficiente, permitindo reutilizar ou revender o suporte;
* **Classes de dados críticas**: podem exigir a **destruição física do suporte de armazenamento**.

---

## 2. *Dumpster Diving* e Destruição de Papel (Slides 5–8)

### 2.1. Caso Real de *Pentesting*: *"One man's trash is another man's identity"* (Slide 5)
Um relato clássico do *pentester* Jim Stickley ([Today — Identity Theft](https://www.today.com/popculture/identitytheft-your-trash-their-treasure-wbna27011491)) ilustra a vulnerabilidade dos resíduos documentais:

* Sem autorização para invadir as residências dos executivos da empresa-alvo, o *pentester* seguia a equipa de gestão desde o parque de estacionamento até casa para inspecionar o **lixo doméstico**;
* **Regra operacional e jurídica**: existe um mercado lucrativo para ladrões de identidade nos resíduos pessoais e corporativos, agravado pelo facto de o lixo colocado na rua para recolha se tornar, por regra, **aberto ao público**.

### 2.2. Procedimentos e Reconstrução de Papel Triturado (Slides 6–7)
As organizações devem instituir **armazenamento seguro prévio à destruição** e procedimentos formais de trituração ou incineração. Quando a trituração produz fragmentos demasiado grandes, os documentos continuam recuperáveis.

> [!WARNING] Reconstrução de Papel Triturado (Humana e Assistida por Computador)
> Casos históricos demonstram a fragilidade da trituração inadequada ([Slate — Reconstrução de Papel](http://slate.me/2xHu3Gl)):
> * **Embaixada dos EUA em Teerão, Irão (1979)**: funcionários tentaram destruir milhares de documentos da CIA com trituradoras em tiras (*strip-cut*). Estudantes iranianos recorreram a **tecelões de tapetes persas locais** para reconstruir manualmente página a página, publicando mais de **60 volumes** intitulados *"Documents From the U.S. Espionage Den"* (episódio retratado no filme *Argo*);
> * **Stanford Financial Group (fraude Ponzi de \$7 mil milhões)**: peritos reconstruíram documentos financeiros triturados utilizados como prova em tribunal;
> * **Caso Michael Cohen (`Cohen v. United States`, 2018)**: em abril de 2018, nas buscas ao escritório, residência e quarto de hotel de Michael Cohen, o FBI apreendeu uma trituradora e o respetivo depósito, **reconstruindo 16 páginas** com auxílio de software automático como o **`UNSHREDDER`** (que digitaliza cada fragmento, atribui um identificador único e correlaciona tamanho, cor do papel, indentação, linhas de texto e fonte/caligrafia).

### 2.3. Norma DIN 66399 (`P-1` a `P-7`) e Métodos Complementares (Slide 8)

As trituradoras de papel classificam-se segundo sete níveis crescentes de segurança, de **`P-1`** (menor segurança) a **`P-7`** (máxima segurança):

|  Classe   | Nível de Criticidade dos Dados                                   | Dimensão Máxima da Partícula / Largura da Tira                                                     |
| :-------: | :--------------------------------------------------------------- | :------------------------------------------------------------------------------------------------- |
| **`P-1`** | Dados gerais (*General data* — menos segura)                     | Área $\le 2000\text{ mm}^2$ **ou** largura de tira $\le 12\text{ mm}$ (comprimento ilimitado)      |
| **`P-2`** | Dados internos (*Internal data*)                                 | Área $\le 800\text{ mm}^2$ **ou** largura de tira $\le 6\text{ mm}$ (comprimento ilimitado)        |
| **`P-3`** | Dados sensíveis e confidenciais                                  | Área $\le 320\text{ mm}^2$ (ex.: $6 \times 50\text{ mm}$) **ou** largura de tira $\le 2\text{ mm}$ |
| **`P-4`** | Dados particularmente sensíveis e confidenciais                  | Área $\le 160\text{ mm}^2$ **e** largura de tira $\le 6\text{ mm}$ (ex.: $4 \times 40\text{ mm}$)  |
| **`P-5`** | Dados secretos (*Secret data*)                                   | Área $\le 30\text{ mm}^2$ **e** largura de tira $\le 2\text{ mm}$ (ex.: $2 \times 15\text{ mm}$)   |
| **`P-6`** | Dados secretos com padrões elevados de segurança                 | Área $\le 10\text{ mm}^2$ **e** largura de tira $\le 1\text{ mm}$ (ex.: $0.8 \times 12\text{ mm}$) |
| **`P-7`** | Dados estritamente secretos (*Top Secret* — ex.: DoD `K-12.2P7`) | Área $\le 5\text{ mm}^2$ **e** largura de tira $\le 1\text{ mm}$ (ex.: $0.8 \times 5\text{ mm}$)   |

* **Outros métodos de destruição de papel**:
  * **Água com lixívia**: dissolve quimicamente as fibras de celulose reduzindo o papel a uma pasta ilegível;
  * **Fogo**: incineração completa dos documentos.

---

## 3. Dados Digitais vs. Papel, Impressoras e Fotocopiadoras (Slide 9)

A concentração de informação em suportes digitais amplia drasticamente o impacto de um abate descuidado ([Análise sobre Descarte Digital](http://bit.ly/2kQC1qE)):

* **Densidade de informação**: **$1\text{ GB}$ de dados equivale aproximadamente a $650\,000$ folhas de papel**;
* **Estatísticas de abate sem limpeza**:
  * Cerca de **60% dos PCs processados em fim de vida ainda contêm dados**;
  * Num estudo do **MIT** sobre **158 discos rígidos usados** adquiridos no mercado secundário, foram recuperados **mais de $5000$ números de cartões de crédito**, relatórios médicos e registos financeiros corporativos, tendo **28 discos** sido vendidos sem qualquer tentativa de limpeza.
* **Impressoras e Fotocopiadoras (*Printers & Copiers*)**:
  * Os equipamentos multifunções modernos guardam registos e imagens de cada documento digitalizado, impresso, enviado por fax ou por e-mail;
  * Muitas impressoras e fotocopiadoras empresariais integram **discos rígidos internos e memória não volátil**;
  * **Procedimento obrigatório pré-abate**: apagar a memória interna e sanitizar/apagar o disco rígido interno antes de devolver equipamentos em *leasing* ou enviá-los para reciclagem.

---

## 4. Caso Morgan Stanley (2022) e Enquadramento Legal na UE (Slides 13–14)

### 4.1. Caso de Estudo: *Morgan Stanley Data Disposal Failure* (Slide 13)

* Em 2016, a instituição financeira **Morgan Stanley** contratou uma empresa de mudanças e armazenamento — sem experiência nem certificação em destruição de dados — para desativar dois centros de dados e milhares de equipamentos ([PCMag — Morgan Stanley](https://www.pcmag.com/news/morgan-stanley-discarded-old-hard-drives-without-deleting-customer-data));
* Milhares de discos rígidos e servidores com **dados pessoais e financeiros não cifrados de milhões de clientes** não foram apagados e acabaram vendidos em leilões online;
* **Consequências financeiras**: multa de **\$35 milhões pela SEC** em setembro de 2022, somando-se a uma coima anterior de **\$60 milhões do OCC** (2020) e a **\$60 milhões** para encerrar uma ação coletiva dos clientes;
* O receio deste tipo de responsabilidade leva muitas tecnológicas (*Big Tech*) a triturar milhões de unidades de armazenamento ainda funcionais ([Ars Technica — Big Tech Shredding](https://arstechnica.com/information-technology/2022/10/why-big-tech-shreds-millions-of-storage-devices-it-could-reuse/)).

### 4.2. Diretivas e Regulamentos da União Europeia (Slide 14)

| Diploma Europeu | Foco Regulatório e Obrigações no Abate de Equipamentos e Dados |
| :--- | :--- |
| **Diretiva WEEE** (*Waste Electrical and Electronic Equipment* — REEE) | • Os **fabricantes de equipamento eletrónico são responsáveis pelo fim de vida dos seus produtos**.<br>• Impõe a recolha, tratamento e reciclagem ambientalmente adequada de resíduos eletrónicos (*e-waste*). |
| **Diretiva RoHS** (*Restriction of Hazardous Substances*) | • Restringe a utilização de substâncias perigosas — como **chumbo, mercúrio e cádmio** — em equipamentos elétricos e eletrónicos.<br>• Reduz a poluição e os riscos de saúde pública no tratamento de *e-waste*. |
| **RGPD / GDPR** ([GDPR.eu](https://gdpr.eu/what-is-gdpr/)) | • Protege **qualquer informação relativa a uma pessoa singular identificada ou identificável**, abrangendo **identificadores diretos** (ex.: nomes) e **identificadores indiretos** (ex.: endereços IP).<br>• A eliminação negligente de dados pessoais acarreta coimas até **20 milhões de euros (`€20 million`)** ou **4% do volume de negócios anual global total**, consoante o que for mais elevado. |

---

## Além da aula

* **Reconstrução de Evidências Fragmentadas (`AFD1` Cap. 1)**: A reconstrução automática de documentos triturados pelo FBI no caso *Cohen v. United States* com o sistema `UNSHREDDER` constitui o paralelo físico direto das técnicas de [[Pesquisa de Evidências e Reconstrução de Eventos]] e de *file carving* aplicadas a suportes digitais fragmentados.
* **Continuidade Operacional no Bloco 01**: As ameaças físicas a equipamentos em viagem (*Evil Maid* / `FlowCloud` e *burner phones*) estão aprofundadas em [[Ataques Físicos em Viagens - Evil Maid (FlowCloud) e Burner Phones]], enquanto os controlos internos e o *audit trail* que evitam falhas como a da Morgan Stanley constam em [[Certificação de Sanitização, Audit Trail e Guia NCSC para Dispositivos Usados]].

---

## Perguntas de revisão

1. **O que define o processo de *Decommissioning* e quais são as três garantias fundamentais que deve assegurar?**

> [!success]- Ver Resposta
> O *Decommissioning* é a retirada de serviço ativo de um equipamento, sistema, instalação ou ativo quando deixa de ser necessário, eficaz, seguro ou viável. Deve assegurar: (1) a remoção segura de componentes, (2) o apagamento de dados sensíveis e (3) a minimização dos impactos ambientais.

2. **Porque é que o lixo doméstico ou empresarial colocado na via pública representa um risco jurídico e operacional em *Dumpster Diving*?**

> [!success]- Ver Resposta
> A partir do momento em que os resíduos são colocados na rua para recolha pública, deixam geralmente de estar sob proteção privada e tornam-se abertos ao público, permitindo a terceiros ou *pentesters* (como no relato de Jim Stickley) extrair faturas, identificadores e documentação interna sem cometer invasão de propriedade.

3. **Qual é a diferença de segurança entre as classes `P-1`, `P-4` e `P-7` da norma DIN 66399 e o que comprovam os casos do Irão (1979) e de Michael Cohen (2018)?**

> [!success]- Ver Resposta
> Na norma DIN 66399, a classe `P-1` (dados gerais) admite partículas até $2000\text{ mm}^2$ ou tiras até $12\text{ mm}$ de largura sem limite de comprimento; a classe `P-4` (particularmente sensível) exige partículas $\le 160\text{ mm}^2$ com largura $\le 6\text{ mm}$; e a classe `P-7` (*Top Secret*) exige partículas $\le 5\text{ mm}^2$ e largura $\le 1\text{ mm}$. Os casos da Embaixada dos EUA em Teerão (mais de 60 volumes reconstruídos por tecelões persas a partir de tiras *strip-cut*) e de Michael Cohen (16 páginas reconstruídas pelo FBI via `UNSHREDDER`) comprovam que cortes largos ou em tiras são reversíveis.

4. **Que cuidados específicos devem ser aplicados a impressoras e fotocopiadoras antes do seu *decommissioning* e porquê?**

> [!success]- Ver Resposta
> As impressoras e fotocopiadoras empresariais armazenam registos dos documentos digitalizados, impressos, enviados por fax ou por e-mail em memória não volátil e discos rígidos internos. Antes do abate ou devolução, é obrigatório apagar a memória interna e sanitizar/apagar o disco rígido interno do equipamento.

5. **Em que falhou a Morgan Stanley (2022) e quais são as obrigações e coimas previstas nas diretivas europeias WEEE, RoHS e no RGPD?**

> [!success]- Ver Resposta
> A Morgan Stanley contratou em 2016 uma empresa de mudanças não certificada para desativar dois centros de dados, resultando na venda em leilão online de discos não cifrados com dados de clientes (multas de \$35M da SEC, \$60M do OCC e \$60M em ação coletiva). Na UE: a **WEEE** responsabiliza os fabricantes pelo fim de vida e reciclagem de *e-waste*; a **RoHS** restringe substâncias perigosas (chumbo, mercúrio, cádmio); e o **RGPD** protege identificadores diretos e indiretos (como IPs), com coimas até **€20 milhões ou 4% do volume de negócios anual global** (o mais elevado).

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Capítulo 2 - Administração de Sistemas]] | Início do capítulo |
| **Seguinte** | [[Ataques Físicos em Viagens - Evil Maid (FlowCloud) e Burner Phones]] | `mesmo bloco` |
| **Índice** | [[Capítulo 2 - Administração de Sistemas]] · [[00 ASSI]] | `Bloco 01` |

### Conceitos Relacionados

* [[Sanitização e Destruição de Discos Magnéticos (HDDs) - Wiping, Degaussing e Destruição Física]] · `mesmo bloco`
* [[Certificação de Sanitização, Audit Trail e Guia NCSC para Dispositivos Usados]] · `mesmo bloco`
* [[Arquitetura SSD e Memória NAND (Wear Leveling e Garbage Collection)]] · `Comum/`
* [[Licenciamento de Software, Fugas em Partilha de Dados (SAS Tokens) e Falhas de Redação]] · `Bloco 03`
* [[Pesquisa de Evidências e Reconstrução de Eventos]] · `AFD1 · Cap. 1`
