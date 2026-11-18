---
title: Código de Ética na Investigação Forense Digital (ISFCE)
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Análise Forense Digital I
sigla_uc: AFD1
capitulo: 1
bloco: 4
fonte_aula: MCIF – Digital Forensic Analysis 1 - Investigation Method.pdf
tags:
  - afd1
  - forense
  - etica
  - isfce
  - perito
aliases:
  - Ethical Code
  - ISFCE
  - International Society of Forensic Computer Examiners
  - Ética Forense
atualizado: 2026-11-11
---

# Código de Ética na Investigação Forense Digital (ISFCE)

O **Código de Ética da ISFCE** protege a integridade da perícia através de deveres obrigatórios e proibições absolutas, vedando ao examinador omitir provas relevantes ou opinar sobre culpa ou inocência.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Método / Sistema)**: O acesso privilegiado a sistemas e dados privados exige balizas deontológicas objetivas que garantam imparcialidade, rigor metodológico e fidelidade à autorização legal do exame.
> * **Porque importa (Forense / Tribunal)**: Um perito parcial, fora do âmbito do mandado (*scope*) ou sem transparência técnica destrói a credibilidade do relatório e pode conduzir à nulidade processual da prova.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Factos vs. juízo de culpa**: o examinador **nunca** expressa opinião sobre culpa ou inocência — apresenta apenas factos técnicos verificados dentro do âmbito autorizado.
>   * **Proibição de ocultar provas**: **nunca** omitir ou reter qualquer evidência relevante, quer incrimine quer ilibe o suspeito.
>   * **Âmbito (*scope*) e competência**: **nunca** exceder a autorização do exame nem aceitar conscientemente trabalho para além da própria capacidade técnica.

---

## Propósito do Código de Ética

* Necessário para **proteger a integridade do processo de investigação digital**.
* Existem vários códigos deontológicos internacionais, destacando-se o [Código de Ética da International Society of Forensic Computer Examiners (ISFCE)](https://www.isfce.com/ethics2.htm).

---

## Diretrizes da ISFCE

### Um examinador forense fará SEMPRE (*Will Always*):

1. Demonstrar **compromisso e diligência** no desempenho das funções atribuídas.
2. Demonstrar **integridade** na conclusão dos trabalhos profissionais.
3. Manter a **máxima objetividade** em todos os exames forenses e apresentar as conclusões com precisão.
4. Conduzir exames baseados em **procedimentos estabelecidos e validados**.
5. Respeitar os mais elevados padrões morais e éticos e cumprir este Código.
6. **Testemunhar com verdade** em todas as matérias perante qualquer comissão, tribunal ou processo.
7. Evitar qualquer ação que possa apresentar conscientemente um **conflito de interesses**.
8. Cumprir todas as **ordens legais dos tribunais**.
9. Examinar exaustivamente todas as evidências **dentro do âmbito (*scope*) da intervenção**.

### Um examinador forense NUNCA fará (*Will Never*):

1. **Omitir ou reter qualquer evidência relevante**, quer incrimine quer ilibe.
2. **Revelar quaisquer assuntos confidenciais** ou conhecimentos obtidos num exame sem uma ordem de um tribunal de jurisdição competente ou sem a permissão expressa do cliente.
3. **Expressar uma opinião sobre a culpa ou inocência de qualquer parte**.
4. Envolver-se em qualquer **conduta antiética ou ilegal**.
5. Aceitar conscientemente uma tarefa **para além da sua capacidade técnica**.
6. **Deturpar** a sua formação académica, treino ou credenciais.
7. Demonstrar **enviesamento ou preconceito** nas conclusões ou nos exames.
8. **Exceder a autorização** na condução dos exames.

### Síntese Comparativa por Eixo Deontológico

| Eixo Deontológico | Dever Positivo (*Will Always*) | Proibição Absoluta (*Will Never*) |
| :--- | :--- | :--- |
| **Objetividade e Prova** | Máxima objetividade, precisão e exame exaustivo dentro do *scope* | Omitir/reter evidência relevante ou demonstrar enviesamento/preconceito |
| **Verdade e Papel Judicial** | Testemunhar com verdade e respeitar ordens legais dos tribunais | Expressar opinião sobre a culpa ou inocência de qualquer parte |
| **Rigor e Competência** | Usar procedimentos estabelecidos e validados; manter integridade | Aceitar tarefa além da capacidade técnica ou deturpar credenciais |
| **Autorização e Sigilo** | Evitar conflitos de interesses e agir dentro do *scope* autorizado | Exceder a autorização ou revelar confidências sem ordem judicial/permissão do cliente |

---

## Implicações Forenses

* **Factos vs. Juízo de Culpa**: Ao perito forense compete exclusivamente relatar factos técnicos verificáveis (ex.: *"o ficheiro X foi descarregado às 14:32 através de uma sessão interativa da conta Y"*), cabendo exclusivamente ao juiz ou ao tribunal pronunciar-se sobre a culpa ou inocência jurídica do arguido.
* **Respeito pelo Mandado (*Scope*)**: Exceder o âmbito da autorização judicial (analisando períodos temporais, pastas ou dispositivos não abrangidos pelo mandado) viola simultaneamente o código ético e a lei processual penal, gerando prova nula.
* **Rigor e Objetividade na Interpretação de Artefactos do Windows ([[00 ASSI|ASSI]])**: O dever ético de *"apresentar as conclusões com precisão"* e de *"nunca demonstrar enviesamento"* proíbe extrapolações técnicas abusivas — por exemplo, nunca afirmar que uma entrada na [[Application Compatibility e ShimCache (AppCompatCache)|ShimCache]] ou [[Extração da AmCache e Comparação Forense com a ShimCache|AmCache]] prova a execução de um programa no Windows 10/11, nunca declarar que uma miniatura na [[Caches de Ícones e Miniaturas (IconCache e Thumbcache)|Thumbcache]] prova visualização consciente pelo arguido, nem ignorar o risco de falsos positivos de incremento na chave [[Artefacto Forense UserAssist|UserAssist]].

---

## Perguntas de revisão

1. **Qual é a finalidade primordial de um Código de Ética na investigação forense digital?**

> [!success]- Ver Resposta
> Proteger a **integridade do processo de investigação digital**, assegurando imparcialidade, rigor metodológico e conformidade legal em toda a intervenção do perito.

2. **Porque é que um perito forense nunca deve expressar uma opinião sobre a culpa ou inocência de um suspeito no seu relatório ou depoimento?**

> [!success]- Ver Resposta
> Porque o código da ISFCE proíbe expressamente esse juízo e o papel do perito restringe-se a apresentar factos técnicos verificáveis com objetividade e precisão; decidir sobre culpa ou inocência cabe exclusivamente ao tribunal.

3. **Que atitude deve tomar o examinador perante uma evidência que contraria a tese da entidade que o contratou ou perante uma perícia que ultrapassa as suas competências técnicas?**

> [!success]- Ver Resposta
> Nunca pode omitir ou reter qualquer evidência relevante (quer incrimine quer ilibe) e nunca pode aceitar conscientemente uma tarefa para além da sua capacidade técnica nem deturpar as suas credenciais.

4. **Em que condições excecionais pode o examinador revelar assuntos confidenciais obtidos num exame, e o que significa respeitar o *scope*?**

> [!success]- Ver Resposta
> Só pode revelar assuntos confidenciais mediante **ordem de um tribunal de jurisdição competente** ou **permissão expressa do cliente**. Respeitar o *scope* significa examinar exaustivamente as evidências apenas dentro dos limites exatos da autorização recebida, nunca os excedendo.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Registo, Etiquetagem e Fotografia Pericial (Regras LabCIF)]] | `Bloco 03` |
| **Seguinte** | [[Exercício de Projeto - Catalogação e Etiquetagem de Dispositivos e Serviços]] | `mesmo bloco` |
| **Índice** | [[Capítulo 1 - Método de Investigação]] · [[00 AFD1]] | `Bloco 04` |

### Conceitos Relacionados

* [[Investigação Digital e Evidência Digital]] · `Bloco 01`
* [[Princípios e Rota do Manuseamento de Evidência Digital]] · `Bloco 03`
* [[Taxonomia dos Artefactos de Execução no Windows]] · `ASSI · Cap. 1`
* [[Extração da AmCache e Comparação Forense com a ShimCache]] · `ASSI · Cap. 1`
* [[Caches de Ícones e Miniaturas (IconCache e Thumbcache)]] · `ASSI · Cap. 1`
* [[Artefacto Forense UserAssist]] · `ASSI · Cap. 1`
