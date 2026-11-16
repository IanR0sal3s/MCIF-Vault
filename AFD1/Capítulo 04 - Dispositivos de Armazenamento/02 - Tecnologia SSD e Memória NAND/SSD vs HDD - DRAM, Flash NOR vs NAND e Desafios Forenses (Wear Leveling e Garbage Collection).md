---
title: SSD vs HDD - DRAM, Flash NOR vs NAND e Desafios Forenses (Wear Leveling e Garbage Collection)
tipo: nota
mestrado: Cibersegurança e Informática Forense
uc: Análise Forense Digital I
sigla_uc: AFD1
capitulo: 4
bloco: 2
tags:
  - afd1
  - forense
  - ssd
  - nand
  - nor
  - wear-leveling
  - garbage-collection
atualizado: 2026-11-16
---

# SSD vs HDD - DRAM, Flash NOR vs NAND e Desafios Forenses (Wear Leveling e Garbage Collection)

**Capítulo:** [[Capítulo 4 - Dispositivos de Armazenamento]]

> [!TIP] Lógica de Funcionamento e Valor Forense
> Ao contrário dos `HDDs` (onde a investigação digital é praticamente idêntica entre modelos e marcas), os `SSDs` possuem **processador e firmware próprios** que gerem ativamente *wear leveling* e *garbage collection*. O perito enfrenta aqui um desafio crítico: **um *write blocker* impede escritas do sistema operativo, mas não impede que o SSD apague blocos livres autonomamente assim que recebe alimentação elétrica**.

## 1. HDD vs. SSD: Contexto e Vantagens dos SSDs

- **HDD:** Poucos fabricantes (concentração por fusões/aquisições), tecnologia madura e comportamento forense muito uniforme entre modelos e marcas.
- **SSD:** Componentes físicos semelhantes, mas **firmware muito variável** entre modelos/fabricantes; ao contrário de uma pen flash (que usa driver e CPU do host), o SSD tem a sua **própria unidade de processamento**.
- **Vantagens do SSD:**
  - Mecanicamente mais fiável (sem partes móveis, resistente a quedas).
  - Velocidade de leitura independente da localização física dos dados.
  - Menor consumo energético (+1h a 2h de autonomia em portátil).
  - Sem ruído nem vibrações; menor aquecimento e peso reduzido (sem carcaça metálica pesada).

## 2. Tipos de SSD: `DRAM` vs. Memória `Flash` (`NOR` vs. `NAND`)

- **SSD baseado em `DRAM`:** Tecnologia mais antiga (>30 anos), **volátil** — requer bateria ou fonte redundante e um disco tradicional para persistência permanente; usada em sistemas de alto desempenho (banca, bolsas, militar). Em **2004**, o custo da memória Flash caiu abaixo da DRAM.
- **Memória `Flash` (não volátil):** Divide-se em portas lógicas **`NOR`** e **`NAND`**:

| Característica | Flash `NOR` | Flash `NAND` |
| :--- | :--- | :--- |
| **Aplicação típica** | Pequenas memórias (`< 16 MB`), ex.: **BIOS**, boot firmware | **USB pen drives** e **SSDs** (substitui HDD) |
| **Densidade** | Baixa | **Elevada densidade de bits** |
| **Leitura** | Muito rápida; acesso **byte a byte** (interface SRAM) | Ligeiramente mais lenta; acesso em **blocos de bytes** |
| **Execução de código** | Permite **execução local** sem carregar para RAM | Não permite execução direta no local |
| **Escrita / Apagamento** | Lenta (até **5 segundos**); 10$\times$ menos ciclos de escrita | Rápida (até **4 ms**), mas unidade mínima de escrita $\ne$ apagamento |
| **Gestão interna** | Simples | Complexa (acesso série, *wear leveling*, *garbage collection*) |

## 3. Funcionamento Interno e Hierarquia da Memória `NAND`

- **Estados lógicos:** Em repouso armazena **`1`**; com carga elétrica armazena **`0`** *(nota: após apagamento de bloco no diagrama estrutural, as células regressam ao estado inicializado).*
- **Camadas por célula:** `SLC` (*Single Layer Cell*) oferece maior desempenho e longevidade; **`MLC`** (*Multi Layer Chip*) aumenta a densidade e reduz o custo, lendo/escrevendo vários bits em simultâneo com menor desempenho.
- **Gestão de *Bad Blocks*:** Todos os chips NAND saem de fábrica com blocos defeituosos (não compensa fabricar wafers perfeitos); coloca-se capacidade extra e mapeiam-se/removem-se os endereços defeituosos no teste inicial.
- **Hierarquia Física (`Cell` $\rightarrow$ `Byte` $\rightarrow$ `Sector/Page` $\rightarrow$ `Block`):**
  - `Cell` (1 bit) $\rightarrow$ `Byte` (8 células)
  - **`Sector` / *Page* (unidade mínima de escrita):** `(512 + 16)` ou `(2 048 + 64)` bytes (múltiplo de *word lines* de 16 bits; os 16/64 B extra guardam metadados: *data status flag*, *block status flag*, dados proprietários e *ECC*).
  - **`Block` (unidade mínima de apagamento):** `16`, `32` ou `64` setores (tipicamente **128 KB**, ex.: $64 \times 2048\text{ B}$). **Não é possível apagar um único setor isoladamente** — o apagamento exige uma carga elétrica em bloco inteiro (semelhante a um flash fotográfico).

## 4. *Wear Leveling*, *Garbage Collection* e Impacto Forense

- **Wear Leveling (Nivelamento de Desgaste):** Cada célula suporta aproximadamente **100 000 ciclos de apagamento**. Para evitar que setores frequentemente alterados se queimem depressa, o **firmware do SSD muda continuamente a localização física dos dados** entre células.
- **Garbage Collection (Recolha de Lixo):** Mantém uma lista de setores libertados e apaga um bloco inteiro apenas quando todos os seus setores estão marcados como livres. **Executa autonomamente assim que o SSD tem alimentação elétrica — mesmo sem cabo de dados ligado — e retoma após falha de energia.**

### Consequências Diretas: `HDD` vs. `SSD` na Escrita e Eliminação

| Operação / Métrica | `HDD` | `SSD` |
| :--- | :--- | :--- |
| **Unidade mínima de escrita** | 1 setor (`512 B`) | 1 setor (`512 B` ou `2 048 B`) |
| **Unidade mínima de apagamento** | 1 setor (`512 B`) | **1 bloco** (`16`, `32` ou `64` setores, típ. `128 KB`) |
| **Unidade mínima de *bad block*** | 1 setor (`512 B`) | **1 bloco** (qualquer célula má marca o bloco inteiro) |
| **Ao modificar um ficheiro** | Pode sobrescrever o mesmo setor | **Não pode escrever sem apagar antes:** grava num novo setor vazio e marca o original para *garbage collection* |
| **Ao apagar um ficheiro no SO** | Dados mantêm-se no setor até serem sobrescritos | Apenas mudam flags; o *garbage collection* pode **apagar fisicamente o bloco em segundos/minutos**, destruindo dados apagados e *slack space* |
| **Efeito de *Write Blocker*** | Bloqueia **qualquer** alteração ao disco | **NÃO impede** o *garbage collection* nem o *wear leveling* internos do firmware! Além disso, a localização física de um setor muda ao longo do tempo. |

## Além da aula

> [!NOTE] Conteúdo Complementar (Além da aula)
> Boas práticas periciais face a SSDs com `TRIM` e *Garbage Collection*:

- **Urgência na Aquisição Física:** Como a simples alimentação elétrica permite que o controlador do SSD execute *garbage collection* em segundo plano (especialmente após comandos `TRIM` emitidos antes da apreensão), um SSD apreendido **não deve ficar ligado em espera** numa estação de aquisição antes de iniciar a imagem forense (`dd`/`ewfacquire`).
- **Implicação para Repetibilidade de Hashes:** Em casos raros de SSDs que continuam a remapar blocos internamente ou onde o *TRIM* ainda estava pendente, o *hash* de uma leitura física direta sem desabilitar/isolar o controlador pode divergir se o firmware reorganizar páginas internas — documente sempre o modelo exato do SSD e o método de aquisição utilizado.

## Perguntas de revisão

1. **Porque é que um *write blocker* de hardware não garante que dados apagados num SSD permaneçam intactos?**
   > [!success]- Ver Resposta
   > Porque o *write blocker* apenas bloqueia comandos de escrita vindos do computador/SO através da interface; o **processador interno do SSD**, assim que recebe energia elétrica, continua a executar autonomamente rotinas de *garbage collection* e *wear leveling*, podendo apagar definitivamente blocos libertados.

2. **Qual a diferença entre a unidade mínima de escrita e a unidade mínima de apagamento numa memória `NAND`?**
   > [!success]- Ver Resposta
   > A unidade mínima de escrita é um **setor/página** (`512` ou `2 048` bytes úteis + metadados), enquanto a unidade mínima de apagamento é um **bloco inteiro** (16, 32 ou 64 setores, tipicamente `128 KB`). Por isso, ao modificar um ficheiro, o SSD grava numa nova página vazia e agenda a antiga para apagamento em bloco.

## Notas relacionadas
- [[Arquitetura SSD vs Pen USB, Conetores M.2, PCIe e Apple SSD]]
- [[Procedimentos de Aquisição - Post-Mortem vs Live, Erros de Disco, HPA-DCO e Write Blockers]]
- [[Acesso a Discos (BIOS vs Direto) e Geometria de Discos Rígidos (CHS vs LBA)]]
