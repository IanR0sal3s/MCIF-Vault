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
atualizado: 2026-11-11
---

# Registo, Etiquetagem e Fotografia Pericial (Regras LabCIF)

A diretriz **Registo** (*Log*) exige documentar todas as ações e seguir as normas **LabCIF** de etiquetagem (`ownerID.deviceID[.inside_deviceID]`) e fotografia com escala métrica e vistas 3D.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Método / Sistema)**: Processos reais chegam a envolver mais de 30 suspeitos e 200 dispositivos; sem etiquetagem hierárquica única e registo fotográfico padronizado, cartões SIM, discos e telemóveis idênticos misturam-se facilmente em laboratório.
> * **Porque importa (Forense / Tribunal)**: Documentar cada comando em análise *live* permite justificar alterações causadas pelo perito, enquanto fotografar com etiqueta formal e régua prova inequivocamente a identidade física e dimensões do objeto.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Ordem obrigatória**: colocar a etiqueta identificadora **sempre antes** de fotografar (e nunca usar *post-its* ou notas manuscritas informais sobre a prova).
>   * **Sintaxe LabCIF**: `ownerID` em maiúscula (`A`, `B`, `C`), acrónimo + 2 dígitos (`SPH01`, `SIM02`), e ficheiros `.jpg` como `tagID-view_name[-detail].jpg`.
>   * **Erros fotográficos a evitar**: ausência de régua/escala métrica, falta de `tag ID` visível, reflexos de *flash* e distância sem legibilidade do número de série/IMEI.

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
2. **Etiquetar os dispositivos**, tendo em atenção que um único processo judicial pode envolver:
   * Um único suspeito com vários dispositivos, ou
   * Vários suspeitos e múltiplos dispositivos (*existem processos reais com mais de 30 suspeitos e mais de 200 dispositivos!*).

### Regras Gerais de Fotografia Após Etiquetagem

* Criar etiquetas para identificar univocamente os dispositivos (ex.: `PC01`, `PC01.1`, `PC01.2`, ...).
* **Tirar fotografias sempre depois de colocar as etiquetas**.
* Deve ser fácil ler qualquer informação relevante: se necessário, tirar uma **fotografia geral** e depois uma **fotografia de pormenor** (marca, modelo, número de série, ligações de cabos de rede, etc.).

> [!WARNING] Problemas Comuns em Fotografias Periciais
> Na análise crítica de exemplos fotográficos incorretos identificam-se quatro erros periciais a evitar:
> 1. **Cartão SIM (`tmn`)**: ausência de etiqueta identificadora e ausência de régua/escala métrica.
> 2. **Telemóvel com etiqueta manuscrita colada**: ausência de régua/escala, etiqueta improvisada difícil de ler e reflexo de *flash* sobre a câmara/ecrã.
> 3. **Telemóvel Nokia com esquadro**: embora possua escala, não tem etiqueta identificadora (`tag ID`) visível e os detalhes do número de série/IMEI não são legíveis àquela distância.
> 4. **Disco rígido com post-it manuscrito ("TABELAS PARTIÇÃO")**: colocação de notas manuscritas informais diretamente sobre a prova em vez de uma etiqueta formal padronizada, e resolução insuficiente para ler o número de série no rótulo técnico.

---

## Regras de Etiquetagem no LabCIF

### Sintaxe e Componentes

```text
ownerID.deviceID[.inside_deviceID]
```

1. **Identificação dos proprietários (`ownerID`)**: utilizam-se **letras maiúsculas** para identificar os proprietários num processo (`A`, `B`, `C`, ...).
2. **Identificação do dispositivo (`deviceID` / `inside_deviceID`)**: utiliza-se um **acrónimo** para cada tipo de dispositivo seguido de um **número de 2 dígitos**.

| Acrónimo | Tipo de Dispositivo (Origem EN / PT) | Exemplo Prático (`Suspeito A`) |
| :--- | :--- | :--- |
| **`FPHxx`** | *Feature Phone* (telemóvel clássico) | `A.FPH01` — telemóvel clássico do suspeito `A` |
| **`SPHxx`** | *Smartphone* | `A.SPH01` — equipamento principal do suspeito `A` |
| **`SIMxx`** | *SIM card* (cartão SIM) | `A.SPH01.SIM01`, `A.SPH01.SIM02` — 1.º e 2.º SIM dentro do smartphone |
| **`MCxx`** | *Memory Card* (cartão de memória) | `A.SPH01.MC01` — cartão de memória dentro do smartphone |
| **`GPSxx`** | *GPS device* (dispositivo GPS) | `A.GPS01` — recetor GPS autónomo |
| **`CAMxx`** | *Camera* (câmara fotográfica/vídeo) | `A.CAM01` — câmara digital |
| **`PCxx`** | *Desktop PC* (computador de secretária) | `A.PC01` — computador fixo |
| **`LAPxx`** | *Laptop* (computador portátil) | `A.LAP01` — portátil |
| **`HDDxx`** | *Hard Disk Drive* (disco rígido) | `A.PC01.HDD01` — disco rígido interno |
| **`SSDxx`** | *Solid State Drive* (unidade SSD) | `A.LAP01.SSD01` — unidade SSD interna |
| **`PENxx`** | *USB Pen Drive* (memória USB) | `A.PEN01` — pen USB externa |

---

## Regras de Fotografia Pericial no LabCIF

| Regra LabCIF | Norma Obrigatória | Detalhes Técnicos e Exemplos |
| :--- | :--- | :--- |
| **1. Escala métrica** | **Incluir sempre a escala de uma régua** | Permite comprovar as dimensões reais do dispositivo e pormenores |
| **2. Vistas e pormenor** | **Fotografar todas as vistas importantes** | Combinar vistas obrigatórias (por tipo de dispositivo) e opcionais; focar números de série, IMEI, etc. |
| **3. Nomes de vista (Caixa 3D)** | **Aplicar as 6 faces padronizadas da caixa 3D** | `Top` (Topo), `Bottom` (Base), `Left` (Esquerda), `Right` (Direita), `Front` (Frente), `Back` (Traseira). A **posição do dispositivo** dentro da caixa imaginária 3D define a face `Front` (ecrã, lente principal, contactos/logótipo principal ou conector frontal voltado para o observador em objetos ambíguos como cartão SIM, pen USB, cartão SD ou câmara) |
| **4. Nomenclatura de ficheiros** | **`tagID-view_name[-detail].jpg`** | Exemplos: `A.SPH01-front.jpg`, `A.SPH01-back-serial.jpg`, `A.SPH01.MC01-front.jpg` |

---

## Templates de Catalogação de Dispositivos e Serviços

Devem ser criados modelos padronizados para catalogar e identificar univocamente cada dispositivo físico ou serviço lógico analisado.

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
Atributos essenciais a registar: `tag ID`, tipo de dispositivo, marca e modelo, número de série / `IMEI` / `UICCID`, tipo de intervenção (aquisição lógica ou física), estado de funcionamento, conteúdos internos (cartões SIM ou de memória), fotografias e observações relevantes:

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

## Além da aula

* **Correlação entre a Catalogação Física (LabCIF) e os Vestígios Lógicos no Windows ([[00 ASSI|ASSI]])**:
  * **Pens USB e Discos Externos (`PENxx` / `HDDxx`)**: Ao catalogar a Marca, Modelo e Número de Série físico de uma pen USB apreendida, o perito pode comprovar se esse dispositivo específico esteve ligado ao computador do suspeito cruzando os dados com a chave `USBSTOR` e o ficheiro `setupapi.dev.log` ([[Artefactos Forenses de Dispositivos USB]]) ou com o relatório `DevicePnps.csv` da [[Extração da AmCache e Comparação Forense com a ShimCache|AmCache]]. Deve ter-se especial cuidado com a armadilha forense do *Windows Assigned Device ID* (quando o identificador tem um `&` na 2.ª posição, significando que a pen não possui número de série de fábrica).
  * **Identificadores de Volume e Rede em Atalhos**: Mesmo que um suporte externo `HDDxx` ou `PENxx` não tenha sido apreendido no local, os [[Ficheiros LNK (Shell Links) - Metadados e Formato Binário|ficheiros LNK]] e as [[Jump Lists - Arquitetura, AppIDs e Carving|Jump Lists]] preservam o *Volume Serial Number*, o rótulo do volume, o nome NetBIOS e o endereço físico MAC da placa de rede do computador original.
  * **Inventário de Hardware do Próprio Computador (`PCxx` / `LAPxx`)**: Os atributos de fabricante (`DeviceMake`), modelo (`DeviceModel`) e nome da máquina (`DeviceName`) ficam igualmente registados na chave `TaskFlow\DeviceCache` da [[Windows Activity Timeline - Arquitetura e Base SQLite]] e na base `DeviceCensus.db` da [[AmCache - Arquitetura, Hives e Evolução para SQLite]].

---

## Perguntas de revisão

1. **Qual é a sintaxe completa de uma etiqueta segundo as regras do LabCIF e como seriam etiquetados um portátil e os seus dois discos internos pertencentes ao suspeito B?**

> [!success]- Ver Resposta
> A sintaxe completa é `ownerID.deviceID[.inside_deviceID]`. Um portátil do suspeito `B` seria `B.LAP01` e os seus dois discos internos seriam, por exemplo, `B.LAP01.HDD01` e `B.LAP01.HDD02` (ou `SSD01`/`SSD02`, consoante o tipo de unidade).

2. **Que regras devem ser seguidas na realização de fotografias periciais e na atribuição do nome aos respetivos ficheiros `.jpg`?**

> [!success]- Ver Resposta
> Fotografar **sempre depois de colocar a etiqueta**, incluir **sempre a escala de uma régua**, captar todas as vistas obrigatórias e detalhes legíveis (S/N, IMEI), usar as 6 vistas padronizadas da caixa 3D (`Top`, `Bottom`, `Left`, `Right`, `Front`, `Back`) e nomear cada imagem segundo **`tagID-view_name[-detail].jpg`** (ex.: `A.SPH01-back-serial.jpg`).

3. **Que campos essenciais constam na tabela de catalogação de um smartphone apreendido?**

> [!success]- Ver Resposta
> `Tag ID`, tipo de dispositivo, marca e modelo, número de série / `IMEI` / `UICCID`, cartões SIM e cartões de memória associados, referências fotográficas, estado de funcionamento, observações relevantes e tipo de intervenção (aquisição lógica ou física).

4. **Quais são os quatro erros fotográficos clássicos identificados nos diapositivos da aula e porque é crítica a diretriz `Log` numa análise *live*?**

> [!success]- Ver Resposta
> Os erros são: ausência de etiqueta identificadora (`tag ID`), ausência de régua/escala métrica, reflexo de *flash* / baixa legibilidade dos números de série e colocação de notas manuscritas informais (ex.: *post-it*) sobre a prova. Registar todas as ações (`Log`) em análise *live* permite justificar posteriormente quais as alterações no sistema causadas pelo próprio investigador.

## Notas relacionadas

- [[Princípios e Rota do Manuseamento de Evidência Digital]]
- [[Diretrizes de Manuseamento - Identificação, Preservação, Isolamento e Correlação]]
- [[Exercício de Projeto - Catalogação e Etiquetagem de Dispositivos e Serviços]]
- [[Artefactos Forenses de Dispositivos USB]]
- [[Sanitização e Destruição de Discos Magnéticos (HDDs) - Wiping, Degaussing e Destruição Física]]
- [[Gestão de Ativos (Asset Management) e Políticas de Armazenamento Amovível (VeraCrypt)]]
- [[Ficheiros LNK (Shell Links) - Metadados e Formato Binário]]
- [[Windows Activity Timeline - Arquitetura e Base SQLite]]
- [[Capítulo 1 - Método de Investigação]]
