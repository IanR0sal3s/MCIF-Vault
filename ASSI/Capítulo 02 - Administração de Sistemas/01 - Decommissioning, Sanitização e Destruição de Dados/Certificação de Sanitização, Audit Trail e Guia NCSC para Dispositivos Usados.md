---
title: Certificação de Sanitização, Audit Trail e Guia NCSC para Dispositivos Usados
tipo: procedimento
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 2
bloco: 1
fonte_aula: System Administration - System and Data Management.pdf
tags:
  - assi
  - administracao-sistemas
  - data-disposal
  - audit-trail
  - certificacao-sanitizacao
  - ncsc
  - e-waste
  - chain-of-custody
aliases:
  - Certificação de Sanitização
  - Data disposal DO
  - Audit Trail de Destruição
  - Guia NCSC Dispositivos Usados
atualizado: 2026-11-11
---

# Certificação de Sanitização, Audit Trail e Guia NCSC para Dispositivos Usados

A sanitização exige **certificação por dispositivo**, controlo interno e **audit trail** (*When, what, who, where, how?*) com número de série e fotos, complementados pelo guia **NCSC** de venda e compra segura.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: Sem documentação individualizada que associe o número de série físico de cada suporte ao método e resultado da eliminação, a organização não dispõe de prova verificável de que os dados foram destruídos antes de o equipamento sair das instalações.
> * **Porque importa (Segurança / Forense)**: A ausência de controlo interno (*in-house*) e de rasto de auditoria origina falhas catastróficas como o caso **Morgan Stanley** e compromete a defesa perante auditores do RGPD. Em contexto forense e pericial, o *audit trail* de destruição espelha a cadeia de custódia, enquanto o guia **NCSC** previne tanto a fuga de dados na venda como a persistência de *malware* em hardware comprado em segunda mão.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Certificação individual**: o processo tem de ser certificado **para cada dispositivo descartado** (ex.: certificado `Active@ KillDisk` com `S/N`, setores, método, % de verificação, carimbos temporais, `SUCCESS` e assinatura);
>   * **5 questões do *Audit Trail***: *When, what, who, where, how?* — registando obrigatoriamente **número de série**, **método(s)**, **fotografia(s)** e **pessoa responsável**;
>   * **Guia NCSC (*Selling* vs. *Buying*)**: ao vender, nunca esquecer de terminar sessão (*Activation Lock* / cloud) e **remover cartões SIM e SD/MicroSD** antes de apagar; ao comprar, executar **factory reset imediato** antes de usar e atualizar o SO.

---

## 1. Certificação Individual de Sanitização (Slide 20)

O processo de eliminação de dados **tem de ser formalmente certificado**: para cada dispositivo descartado é obrigatório emitir e arquivar um documento comprovativo (certificado ou relatório de eliminação).

### Anatomia de um Certificado Real (`Active@ KillDisk` — Slide 20)

| Campo do Certificado | Exemplo de Registo (Slide 20) | Significado de Auditoria |
| :--- | :--- | :--- |
| **Modelo / Dispositivo** | `SanDisk Cruzer Fit 1.27` | Identificação exata do suporte sanitizado |
| **Número de Série (`S/N`)** | Identificador único de fábrica | Rastreabilidade individual no inventário e arquivo |
| **Capacidade / Setores** | `14.9 GB` / `31,266,816` setores | Confirma que toda a área endereçável foi abrangida |
| **Método Aplicado** | `One Pass Zeros` | Prova a técnica de sanitização executada |
| **Verificação** | `Verification: Yes (10%)` | Confirma amostragem de leitura após a escrita |
| **Carimbos Temporais e Estado** | Hora de início, duração e estado **`SUCCESS`** | Garante que a operação concluiu sem erros |
| **Responsável e Validação** | *Performed by* + **assinatura do técnico** | Atribui responsabilidade nominal pela execução |

---

## 2. Boas Práticas Organizacionais e *Audit Trail* (`Data disposal - DO` — Slide 25)

1. **Manter o controlo internamente (*Bring control in-house*)**: evitar delegar cegamente o abate em prestadores sem certificação nem auditoria (prevenindo falhas como a da Morgan Stanley).
2. **Manter um rasto de auditoria (*Audit trail of destruction*)**:
   * Deve responder às cinco questões periciais: ***When, what, who, where, how?*** (Quando, o quê, quem, onde e como?);
   * Cada dispositivo — **especialmente suportes de armazenamento** — deve ter uma entrada dedicada no **arquivo do sistema (*system archive*)** contendo:
     * **Número de série (*Serial number*)**;
     * **Método(s) de remoção ou destruição**;
     * **Fotografia(s)** do equipamento e do processo de destruição;
     * **Pessoa responsável (*person in charge*)**.
3. **Descarte ambientalmente responsável (*e-waste*)**: após a sanitização certificada, encaminhar o hardware para reciclagem eletrónica licenciada (ex.: projetos como *ReciQwerty*).

---

## 3. Guia do NCSC — *Buying & Selling Used Devices* (Slide 26)

O *National Cyber Security Centre* ([NCSC — ncsc.gov.uk](https://www.ncsc.gov.uk/)) define procedimentos distintos consoante o utilizador esteja a vender/descartar ou a adquirir equipamentos usados (telemóveis, portáteis, tablets ou discos):

| Cenário | Passo | Ação Obrigatória | Finalidade de Segurança |
| :--- | :---: | :--- | :--- |
| **Ao Vender / Descartar (*Selling*)** | **1** | **Back up** dos dados a preservar | Evita perda irreversível antes do apagamento. |
| | **2** | **Sign out** (terminar sessão e desvincular contas) | Remove acessos cloud, e-mail, redes sociais e bloqueios *Find My Device* / *Activation Lock*. |
| | **3** | **Remove cards** (remover cartões externos) | Retira cartões **SIM** e cartões de memória **SD / MicroSD** que não fazem parte do armazenamento interno. |
| | **4** | **Erase data** (apagar os dados) | Executa *factory reset* seguro ou sanitização certificada (idealmente sobre dados já cifrados). |
| **Ao Comprar (*Buying*)** | **1** | Comprar apenas a **retalhistas reputados** | Reduz o risco de hardware adulterado ou roubado. |
| | **2** | Executar **factory reset imediato** antes de usar | Elimina eventual *malware* ou perfis de gestão pré-instalados. |
| | **3** | **Update OS** (atualizar SO e firmware) | Fecha vulnerabilidades conhecidas e confirma se o equipamento ainda recebe *patches* de segurança. |

---

## Além da aula

* **Rasto de Auditoria no Abate vs. Regras de Catalogação e Fotografia do LabCIF (`AFD1` Cap. 1)**: A exigência de registar no arquivo do sistema o número de série, método, responsável e fotografia(s) — respondendo a *When, what, who, where, how?* — aplica na administração de sistemas exatamente os mesmos princípios de integridade, etiquetagem hierárquica e registo fotográfico em escala pericial estudados em [[Registo, Etiquetagem e Fotografia Pericial (Regras LabCIF)]], [[Princípios e Rota do Manuseamento de Evidência Digital]] e [[Investigação Digital e Evidência Digital]].
* **Articulação com o Bloco 01**: As técnicas concretas de sanitização que alimentam este processo de certificação estão detalhadas em [[Sanitização e Destruição de Discos Magnéticos (HDDs) - Wiping, Degaussing e Destruição Física]] e [[Arquitetura SSD e Memória NAND (Wear Leveling e Garbage Collection)]], enquanto o enquadramento legal (WEEE, RoHS, RGPD) e o caso Morgan Stanley constam em [[Decommissioning de Equipamentos, Destruição de Papel (P-1 a P-7) e Enquadramento Legal UE]].

---

## Perguntas de revisão

1. **Que elementos técnicos e de validação devem constar num certificado individual de sanitização como o emitido pelo `Active@ KillDisk`?**

> [!success]- Ver Resposta
> Deve incluir a identificação do dispositivo/modelo (ex.: `SanDisk Cruzer Fit 1.27`), o número de série (`S/N`), a capacidade e contagem de setores (ex.: `14.9 GB` / `31,266,816` setores), o método aplicado (ex.: `One Pass Zeros`), a confirmação e percentagem de verificação (ex.: `Verification: Yes (10%)`), os carimbos temporais, o estado final (`SUCCESS`), a identificação do técnico (*Performed by*) e a respetiva assinatura.

2. **Quais são as três regras de `Data disposal - DO` e que quatro elementos têm de ficar registados na entrada de arquivo de cada dispositivo?**

> [!success]- Ver Resposta
> As três regras são: (1) manter o controlo internamente (*bring control in-house*); (2) manter um *audit trail* que responda a *When, what, who, where, how?*; e (3) encaminhar o hardware para reciclagem certificada de *e-waste* (ex.: *ReciQwerty*). Cada entrada no arquivo do sistema deve conter: **número de série**, **método(s) de remoção/destruição**, **fotografia(s)** e **pessoa responsável**.

3. **Quais são os 4 passos recomendados pelo NCSC ao vender/descartar um dispositivo usado e os 3 passos ao comprar um dispositivo usado?**

> [!success]- Ver Resposta
> **Ao vender**: (1) fazer *back up* dos dados a manter; (2) fazer *sign out* de todas as contas e bloqueios (*Activation Lock*); (3) remover cartões externos (**SIM** e **SD/MicroSD**); e (4) apagar os dados (*erase data*). **Ao comprar**: (1) comprar apenas a retalhistas reputados; (2) realizar *factory reset* imediato antes de utilizar; e (3) atualizar o sistema operativo e verificar se continua a receber atualizações de segurança.

---

## Notas relacionadas

- [[Capítulo 2 - Administração de Sistemas]]
- [[Decommissioning de Equipamentos, Destruição de Papel (P-1 a P-7) e Enquadramento Legal UE]]
- [[Sanitização e Destruição de Discos Magnéticos (HDDs) - Wiping, Degaussing e Destruição Física]]
- [[Arquitetura SSD e Memória NAND (Wear Leveling e Garbage Collection)]]
- [[Registo, Etiquetagem e Fotografia Pericial (Regras LabCIF)]]
- [[Princípios e Rota do Manuseamento de Evidência Digital]]
- [[Investigação Digital e Evidência Digital]]
