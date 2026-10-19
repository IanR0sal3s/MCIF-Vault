---
title: Registo, Etiquetagem e Fotografia Pericial (Regras LabCIF)
tipo: procedimento
mestrado: Cibersegurança e Informática Forense
uc: Análise Forense Digital I
sigla_uc: AFD1
capitulo: 1
bloco: 3
fonte_aula: MCIF – Digital Forensic Analysis 1 - Investigation Method.pdf
tags:
  - afd1
  - forense
  - handling
  - labcif
  - etiquetagem
  - fotografia-forense
  - catalogacao
aliases:
  - Regras LabCIF
  - Tagging rules at LabCIF
  - Fotografia Forense
  - Catalogação de Dispositivos
atualizado: 2026-10-19
---

# Registo, Etiquetagem e Fotografia Pericial (Regras LabCIF)

A quinta diretriz de manuseamento (**5 – Log**) exige a documentação exaustiva de todas as ações periciais, a atribuição de etiquetas únicas hierárquicas aos dispositivos e serviços analisados e o registo fotográfico rigoroso com escala métrica. No **LabCIF**, a nomenclatura de etiquetagem segue o formato `ownerID.deviceID[.inside_deviceID]` e as fotografias obedecem às vistas padronizadas de uma caixa tridimensional (`Top`, `Bottom`, `Left`, `Right`, `Front`, `Back`) com nomes de ficheiro estruturados (`tagID-view_name[-detail].jpg`).

---

## 5 — Registo e Documentação (*Log*)

* **Registar e documentar todas as ações realizadas**:
  * Ajuda a identificar o que já foi feito e quais foram os resultados obtidos.
  * Ajuda a identificar que pesquisas ainda faltam realizar.
  * Numa análise *live*, ou ao executar técnicas que modifiquem dados, é crítico documentar cada passo para poder justificar posteriormente **quais as alterações no sistema que resultaram das ações do investigador**.

---

## Identificação Física, Receção e Etiquetagem

Na receção de material para análise:
1. **Verificar a lista de dispositivos entregues** para análise.
2. **Etiquetar os dispositivos (*tagging*)**, tendo em atenção que um único processo judicial pode envolver:
   * Um único suspeito com vários dispositivos, ou
   * Vários suspeitos e múltiplos dispositivos (*existem processos reais com mais de 30 suspeitos e mais de 200 dispositivos!*).

### Regras Gerais de Fotografia Após Etiquetagem
* Criar etiquetas (*tags*) para identificar univocamente os dispositivos (ex.: `PC01`, `PC01.1`, `PC01.2`, ...).
* **Tirar fotografias sempre depois de colocar as etiquetas**.
* Deve ser fácil ler qualquer informação relevante: se necessário, tirar uma **fotografia geral (*overview photo*)** e depois uma **fotografia de pormenor (*close-up shot*)** (marca, modelo, número de série, ligações de cabos de rede, etc.).

> [!WARNING] Problemas Comuns em Fotografias Periciais
> Na análise crítica de exemplos fotográficos incorretos identificam-se quatro erros periciais a evitar:
> 1. **Cartão SIM (`tmn`)**: ausência de etiqueta identificadora (*tag*) e ausência de régua/escala métrica.
> 2. **Telemóvel com etiqueta manuscrita colada**: ausência de régua/escala, etiqueta improvisada difícil de ler e reflexo de luz (*flash*) sobre a câmara/ecrã.
> 3. **Telemóvel Nokia com esquadro**: embora possua escala, não tem etiqueta identificadora (*tag ID*) visível e os detalhes do número de série/IMEI não são legíveis àquela distância.
> 4. **Disco rígido com post-it manuscrito ("TABELAS PARTIÇÃO")**: colocação de notas manuscritas informais diretamente sobre a prova em vez de uma etiqueta formal padronizada, e resolução insuficiente para ler o número de série no rótulo técnico.

---

## Regras de Etiquetagem no LabCIF (*Tagging Rules at LabCIF*)

1. **Identificação dos proprietários (*owners*)**: utilizam-se **letras maiúsculas** para identificar os proprietários dos dispositivos num determinado processo:
   * `A`, `B`, `C`, ...
2. **Identificação do tipo de dispositivo**: utiliza-se um **acrónimo** para cada tipo de dispositivo, seguido de um **número de 2 dígitos**:
   * `FPHxx` (*Feature Phone*), `SPHxx` (*Smartphone*), `SIMxx` (*SIM card*), `MCxx` (*Memory Card*), `GPSxx` (*GPS device*), `CAMxx` (*Camera*), `PCxx` (*Desktop PC*), `LAPxx` (*Laptop*), `HDDxx` (*Hard Disk Drive*), `SSDxx` (*Solid State Drive*), `PENxx` (*USB Pen Drive*), ...
3. **Estrutura da etiqueta (*Tag*)**:
   ```text
   ownerID.deviceID[.inside_deviceID]
   ```

### Exemplo Prático (Smartphone do Suspeito A com 2 Cartões SIM e 1 Cartão de Memória)
* `A.SPH01` — o equipamento principal (*handset*) pertencente ao proprietário `A`
* `A.SPH01.SIM01` — primeiro cartão SIM no interior do smartphone
* `A.SPH01.SIM02` — segundo cartão SIM no interior do smartphone
* `A.SPH01.MC01` — cartão de memória no interior do smartphone

---

## Regras de Fotografia Pericial no LabCIF (*Our Photograph Rules*)

1. **Incluir sempre a escala de uma régua** (*scale of a ruler*) na fotografia.
2. **Fotografar todas as vistas importantes**:
   * Existem vistas obrigatórias por tipo de dispositivo e algumas opcionais.
   * Especial atenção aos detalhes, como números de série, IMEI, etc.
3. **Aplicar os nomes das vistas de acordo com a caixa 3D (*3D box*)**:
   * As 6 faces padronizadas são: `Top` (Topo), `Bottom` (Base), `Left` (Esquerda), `Right` (Direita), `Front` (Frente) e `Back` (Traseira).
   * A **posição do dispositivo** dentro da caixa imaginária 3D é fundamental (para alguns objetos pode ser ambíguo qual é a frente, ex.: cartão SIM, pen USB, cartão SD, câmara fotográfica). Nos diagramas de referência de posicionamento, a face com o ecrã, lente principal, contactos/logótipo principal ou conector frontal voltado para o observador define a vista `Front`.
4. **Nomenclatura dos ficheiros de imagem**:
   ```text
   tagID-view_name[-detail].jpg
   ```
   * **Exemplos**:
     * `A.SPH01-front.jpg`
     * `A.SPH01-back-serial.jpg`
     * `A.SPH01.MC01-front.jpg`

---

## Templates de Catalogação de Dispositivos e Serviços

Devem ser criados modelos (*templates*) padronizados para catalogar e identificar univocamente cada dispositivo físico ou serviço lógico analisado.

### Exemplo 1: Disco Rígido (`PC01.HD03`) e Serviço DNS (`DNS01`)

| Campo (Dispositivo) | Valor (`PC01.HD03`) | Campo (Serviço) | Valor (`DNS01`) |
| :--- | :--- | :--- | :--- |
| **Tag ID** | `PC01.HD03` | **Tag ID** | `DNS01` |
| **Device** | Hard disc drive, 2.5" | **Domain name** | `lotreur.com` |
| **Type of information** | — | **Type of information** | DNS history |
| **Brand** | Seagate | **Registrar** | Center of Ukrainian Internet Names (UKR-NAMES) |
| **Model** | Momentus 5400.6 ST9250315AS | **Creation date** | `01-Mar-2013` |
| **Serial number** | `5VC9CWTT` | **Current state** | expired |
| **Interface** | SATA | **Registrant email** | `c152136@rmqkr.net` |
| **Capacity** | 250,0 GB | **Annexes** | Yes, see Annex A |
| **Type of intervention** | Forensic copy | | |
| **Working condition** | Normal | | |
| **Pictures** | Yes, see Fig. 1 and 2 | | |
| **Observations** | None | | |

### Exemplo 2: Catalogação Completa de Smartphone (`A.SPH01`)
Atributos essenciais a registar: `tag ID`, tipo de dispositivo, marca e modelo, número de série / `IMEI` / `UICCID`, tipo de intervenção (aquisição lógica ou física), estado de funcionamento (*working / non-working*), conteúdos internos (cartões SIM ou de memória), fotografias e observações relevantes:

| Atributo | Registo Pericial (`A.SPH01`) |
| :--- | :--- |
| **Tag ID** | `A.SPH01` |
| **Device type** | Smartphone |
| **Brand** | Samsung GSM |
| **Model** | GT-S5310 |
| **Serial n.** | `RV1D737C8AT` |
| **IMEI** | `356 431 051 982 186` |
| **SIM card** | 2: `A.SPH01.SIM01` and `A.SPH01.SIM02` |
| **Memory card** | 1: `A.SPH01.MC01` |
| **Photos** | Fig. 1, 2 and 3 |
| **Condition** | Working |
| **Observations** | Battery not working |
| **Intervention** | Logic acquisition |

---

## Implicações Forenses

* **Rastreabilidade em Processos Complexos**: A notação hierárquica `ownerID.deviceID.inside_deviceID` impede trocas acidentais de cartões SIM ou discos rígidos quando dezenas de equipamentos idênticos de múltiplos suspeitos dão entrada em simultâneo no laboratório.
* **Rigor Fotográfico**: Fotografar sempre *após* a colocação da etiqueta física e *com* régua milimétrica garante que a fotografia prova inequivocamente a associação entre o objeto físico, as suas dimensões reais e o código identificador constante no relatório pericial.

---

## Perguntas de revisão

- Qual é a sintaxe completa de uma etiqueta (*tag*) segundo as regras do LabCIF? Como seriam etiquetados um portátil e os seus dois discos internos pertencentes ao suspeito B?
- Que regras devem ser seguidas na realização de fotografias periciais e na atribuição do nome aos respetivos ficheiros `.jpg`?
- Que campos obrigatórios constam na tabela de catalogação de um smartphone apreendido?

## Notas relacionadas

- [[Princípios e Rota do Manuseamento de Evidência Digital]]
- [[Diretrizes de Manuseamento - Identificação, Preservação, Isolamento e Correlação]]
- [[Exercício de Projeto - Catalogação e Etiquetagem de Dispositivos e Serviços]]
- [[Capítulo 1 - Método de Investigação]]
