---
title: Arquitetura SSD e Memória NAND (Wear Leveling e Garbage Collection)
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Transversal (AFD1 e ASSI)
sigla_uc: COMUM
ucs_relacionadas:
  - AFD1
  - ASSI
tags:
  - comum
  - ssd
  - nand-flash
  - wear-leveling
  - garbage-collection
  - sanitizacao
  - forense
aliases:
  - SSD vs HDD - DRAM, Flash NOR vs NAND e Desafios Forenses (Wear Leveling e Garbage Collection)
  - Eliminação Segura de Dados em SSDs SATA, NVMe e Memórias Flash
atualizado: 2026-11-18
---

# Arquitetura SSD e Memória NAND (Wear Leveling e Garbage Collection)

Os SSDs armazenam dados em células semicondutoras `NAND Flash` geridas por um controlador próprio (*FTL*), criando assimetrias entre escrita em página e apagamento em bloco que desafiam tanto a aquisição forense como a sanitização segura.

> [!TIP] Lógica de Funcionamento e Valor Transversal
> * **Porque existe (Hardware)**: As células `NAND Flash` não permitem sobrescrita direta sem apagamento prévio de um bloco inteiro e degradam-se após cerca de 100 000 ciclos. Para garantir desempenho e longevidade, o controlador (*Flash Translation Layer — FTL*) distribui as escritas (*wear leveling*), redireciona alterações para páginas limpas, executa *garbage collection* em segundo plano e reserva **5% a 10% de capacidade oculta (*over-provisioning*)**.
> * **Porque importa (Forense vs. Segurança)**: Em **AFD1**, um *write blocker* impede escritas do sistema operativo, mas **não impede que o controlador do SSD apague blocos livres autonomamente** assim que recebe energia elétrica. Em **ASSI**, a mesma arquitetura torna o *degaussing* inútil e o *overwriting* clássico (`DoD 5220.22-M`) ineficaz, permitindo recuperar ficheiros em células não endereçáveis se não forem usados métodos de cifragem ou comandos de firmware.
> * **Pontos Críticos para Exame**:
>   * **Unidade de escrita vs. apagamento**: escreve-se por **setor/página** (`512` ou `2 048 B` + metadados), mas apaga-se por **bloco inteiro** (`16`, `32` ou `64` páginas, típ. `128 KB`);
>   * **Imunidade magnética**: o *degaussing* tem **zero efeito** em `NAND Flash`;
>   * **Estudo Alnaqbi et al. (2025, ISDFS)**: após 3 passagens `DoD 5220.22-M` numa pen USB de `16 GB`, o `PhotoRec` recuperou **`391` ficheiros** e o `Scalpel` **`1946` ficheiros**;
>   * **`nvme sanitize` vs. `Format NVM`**: o `Sanitize` atua em toda a NAND física e **não pode ser interrompido** (retoma após corte de energia); em `nvme sanitize -a 2 /dev/nvme1`, `-a 2` indica **Block Erase**.

---

## 1. HDD vs. SSD e Tipos de Memória (DRAM vs. Flash NOR/NAND)

### Contexto Arquitetural: HDD vs. SSD

* **HDD (*Hard Disk Drive*)**: Tecnologia madura com poucos fabricantes (concentração por fusões/aquisições) e comportamento forense muito uniforme entre modelos e marcas.
* **SSD (*Solid State Drive*)**: Componentes físicos semelhantes, mas **firmware muito variável** entre modelos e fabricantes. Ao contrário de uma pen USB flash (que depende do driver e da CPU do *host*), o SSD integra a sua **própria unidade de processamento (controlador)**.
* **Vantagens operacionais do SSD**:
  * Mecanicamente mais fiável (sem partes móveis, resistente a quedas);
  * Velocidade de leitura independente da localização física dos dados;
  * Menor consumo energético (+1h a 2h de autonomia em portátil);
  * Sem ruído nem vibrações; menor aquecimento e peso reduzido (sem carcaça metálica pesada).

### SSD Baseado em `DRAM` vs. Memória `Flash` (`NOR` e `NAND`)

* **SSD baseado em `DRAM`**: Tecnologia mais antiga (>30 anos), **volátil** — requer bateria ou fonte redundante e um disco tradicional para persistência permanente; utilizada em sistemas de alto desempenho (banca, bolsas, militar). Em **2004**, o custo da memória Flash caiu abaixo da DRAM.
* **Memória `Flash` (não volátil)**: Divide-se em portas lógicas **`NOR`** e **`NAND`**:

| Característica | Flash `NOR` | Flash `NAND` |
| :--- | :--- | :--- |
| **Aplicação típica** | Pequenas memórias (`< 16 MB`), ex.: **BIOS**, *boot firmware* | **USB pen drives** e **SSDs** (substitui HDD) |
| **Densidade** | Baixa | **Elevada densidade de bits** |
| **Leitura** | Muito rápida; acesso **byte a byte** (interface SRAM) | Ligeiramente mais lenta; acesso em **blocos de bytes** |
| **Execução de código** | Permite **execução local** sem carregar para RAM | Não permite execução direta no local |
| **Escrita / Apagamento** | Lenta (até **5 segundos**); $10\times$ menos ciclos de escrita | Rápida (até **4 ms**), mas unidade mínima de escrita $\ne$ apagamento |
| **Gestão interna** | Simples | Complexa (acesso série, *wear leveling*, *garbage collection*) |

---

## 2. Arquitetura Interna NAND Flash (Células, Páginas, Blocos e FTL)

* **Estados lógicos**: Em repouso armazena **`1`**; com carga elétrica armazena **`0`** *(após o apagamento de um bloco, as células regressam ao estado inicializado)*.
* **Camadas por célula**:
  * **`SLC`** (*Single Layer Cell*): 1 bit por célula; oferece maior desempenho e longevidade.
  * **`MLC`** (*Multi Layer Chip*): aumenta a densidade e reduz o custo, lendo/escrevendo vários bits em simultâneo com menor desempenho.
* **Gestão de *Bad Blocks***: Todos os chips NAND saem de fábrica com blocos defeituosos (não compensa fabricar *wafers* perfeitos); inclui-se capacidade extra e mapeiam-se/removem-se os endereços defeituosos no teste inicial.
* **Hierarquia Física (`Cell` $\rightarrow$ `Byte` $\rightarrow$ `Sector/Page` $\rightarrow$ `Block`)**:
  * **`Cell`** (1 bit) $\rightarrow$ **`Byte`** (8 células).
  * **`Sector` / *Page* (unidade mínima de escrita)**: `(512 + 16)` ou `(2 048 + 64)` bytes (múltiplo de *word lines* de 16 bits; os `16` ou `64` bytes extra guardam metadados: *data status flag*, *block status flag*, dados proprietários e *ECC*).
  * **`Block` (unidade mínima de apagamento)**: `16`, `32` ou `64` páginas/setores (tipicamente **`128 KB`**, ex.: $64 \times 2\,048\text{ B}$). **Não é possível apagar uma única página isoladamente** — o apagamento exige uma carga elétrica em bloco inteiro (semelhante a um *flash* fotográfico).
* ***Flash Translation Layer* (`FTL`)**: Camada de firmware do controlador que traduz endereços lógicos (LBA vistos pelo SO) para páginas e blocos físicos, distribuindo os dados por todos os chips do SSD.

---

## 3. Wear Leveling, Garbage Collection, Over-provisioning e Imunidade ao Degaussing

* ***Wear Leveling* (Nivelamento de Desgaste)**: Cada célula suporta aproximadamente **100 000 ciclos de apagamento**. Para evitar que blocos frequentemente alterados se degradem prematuramente, o **firmware do SSD muda continuamente a localização física dos dados** entre células e blocos limpos.
* ***Garbage Collection* (Recolha de Lixo)**: Mantém uma lista de páginas libertadas/inválidas e apaga fisicamente um bloco inteiro apenas quando todas as suas páginas estão marcadas como livres. **Executa autonomamente assim que o SSD recebe alimentação elétrica — mesmo sem cabo de dados ligado — e retoma após falha de energia.**
* ***Over-provisioning* (5% a 10% de blocos ocultos ao SO)**: Todo o SSD reserva entre **5% e 10%** de blocos físicos indisponíveis ao sistema operativo para gestão interna, *wear leveling* e substituição de blocos gastos. Estas áreas nunca são diretamente endereçáveis por ferramentas comuns do SO.
* **Imunidade ao *Degaussing***: Como a memória NAND Flash armazena bits através de carga elétrica em células semicondutoras e não de domínios magnéticos, **o *degaussing* não tem qualquer efeito** sobre SSDs ou pens USB.

### Tabela Comparativa: HDD Magnético vs. SSD / Memória NAND Flash

| Critério Técnico | Disco Magnético (`HDD`) | `SSD` / Memória `NAND Flash` |
| :--- | :--- | :--- |
| **Meio físico de gravação** | Domínios magnéticos em pratos rotativos | Carga elétrica em células semicondutoras (páginas/blocos) |
| **Unidade mínima de escrita** | 1 setor (`512 B`) | 1 setor/página (`512 B` ou `2 048 B` + metadados) |
| **Unidade mínima de apagamento** | 1 setor (`512 B`) | **1 bloco** (`16`, `32` ou `64` páginas, típ. `128 KB`) |
| **Unidade mínima de *bad block*** | 1 setor (`512 B`) | **1 bloco** (qualquer célula má marca o bloco inteiro) |
| **Ao modificar um ficheiro** | Pode sobrescrever o mesmo setor | **Não pode escrever sem apagar antes:** grava numa nova página vazia e marca a original para *garbage collection* |
| **Zonas ocultas e retenção ao apagar** | Eventual HPA/DCO ou setores realocados; dados ficam no setor até sobrescrita | **5%–10% de *over-provisioning*** + páginas antigas em células não endereçáveis até *garbage collection* |
| **Efeito do *Degaussing*** | Destrói dados e *tracks* (inutiliza o HDD) | **Zero efeito** (imune a campos magnéticos) |
| **Efeito do *Overwriting* pelo SO** | Eficaz nos setores endereçáveis; permite reutilização | **Insuficiente** (deixa dados em *over-provisioning* e células remapeadas) |
| **Efeito de *Write Blocker*** | Bloqueia **qualquer** alteração ao disco | **NÃO impede** *garbage collection* nem *wear leveling* internos do firmware |
| **Método seguro reutilizável** | *Wiping* completo (`Eraser`, `DBAN`, `KillDisk`) | **`Cryptographic Erasure`**, **SATA `Secure Erase`**, **NVMe `Format NVM` / `Sanitize`** |

---

## Aplicação por UC

### Em AFD1 (Desafios Forenses, Aquisição e Carving)

* **Assimetria escrita/apagamento e retenção em células não endereçáveis**: Quando um ficheiro é apagado no sistema operativo, apenas mudam as *flags* lógicas; os dados antigos podem sobreviver temporariamente em páginas marcadas como inválidas ou fora do espaço endereçável pelo SO até à atuação do *garbage collection*.
* **Destruição silenciosa por `TRIM` + *Garbage Collection***: Se o sistema operativo emitiu comandos `TRIM` antes da apreensão, o controlador do SSD tem a lista de blocos libertados e pode apagá-los fisicamente em segundos ou minutos assim que tiver energia elétrica.
* **Limitação do *Write Blocker***: Um bloqueador de escrita de hardware bloqueia apenas comandos vindos do *host* pela interface SATA/USB/PCIe; não impede o processador interno do SSD de reorganizar blocos (*wear leveling*) nem de executar *garbage collection* ao ser alimentado.
* **Boas práticas na aquisição física**:
  * **Urgência**: Um SSD apreendido **não deve ficar ligado em espera** numa estação de aquisição antes de iniciar a imagem forense (`dd`/`ewfacquire`), sobretudo em sistemas modernos com SSDs soldados que exigem arranque controlado (ver [[Arranque Forense e Processo de Boot (BIOS e Código Máquina)]] e [[Procedimentos de Aquisição - Post-Mortem vs Live, Erros de Disco, HPA-DCO e Write Blockers]]).
  * **Repetibilidade de *hashes***: Caso o firmware continue a remapar blocos internamente ou processe `TRIM` pendente durante a leitura, o *hash* de duas aquisições consecutivas pode divergir; documente sempre o modelo exato do SSD, o estado do `TRIM` e o método de aquisição (ver [[Arquitetura SSD vs Pen USB, Conetores M.2, PCIe e Apple SSD]] e [[Cheat Sheet - Dispositivos de Armazenamento (HDD, ATA-SCSI, SSD e M.2)]]).

### Em ASSI (Sanitização e Eliminação Segura em Flash/NVMe)

#### Ineficácia do *Overwriting* Clássico (Estudo de Alnaqbi et al., 2025 — ISDFS)

No estudo empírico de **Alnaqbi, M. M., Alblooshi, S. T., Alshamsi, E. A., Seghid, N., & Iqbal, F. (2025, Abril)** — *"An Empirical Analysis of Security and Privacy Issues Associated with Selling and Purchasing of Secondhand Storage Devices"* (*2025 13th International Symposium on Digital Forensics and Security — ISDFS*):

* Os autores analisaram uma **pen USB de `16 GB` adquirida em segunda mão**;
* Aplicaram sobreposição de dados com a norma **`DoD 5220.22-M` (3 passagens)**;
* **Resultados forenses obtidos após as 3 passagens**:
  * **`391` ficheiros recuperados** com a ferramenta de *file carving* **`PhotoRec`**;
  * **`1946` ficheiros recuperados** com a ferramenta de *file carving* **`Scalpel`**.
* **Conclusão**: os utilitários tradicionais de *overwriting* desenhados para discos magnéticos **não são adequados para dispositivos baseados em memória flash**, pois não alcançam o *over-provisioning* nem páginas remapeadas pelo *wear leveling*.

#### Os 3 Métodos Seguros para Sanitizar SSDs Sem Destruição Física

1. **Apagamento Criptográfico (*Cryptographic Erasure*)**: Cifrar previamente toda a unidade (ex.: com **`VeraCrypt`** — ver [[Gestão de Ativos (Asset Management) e Políticas de Armazenamento Amovível (VeraCrypt)]] — ou cifragem de hardware num *Self-Encrypting Drive — SED*) usando uma chave forte aleatória. No abate, elimina-se apenas a *Master Encryption Key*, tornando todos os blocos físicos (incluindo os 5%–10% de *over-provisioning*) instantaneamente indecifráveis.
2. **Limpeza Segura de SSDs SATA (*SATA SSD Secure Erase*)**: Aciona diretamente o controlador para descarga elétrica interna de todas as células NAND (incluindo áreas ocultas), através da função **`"Secure Erase"` integrada na BIOS/UEFI** ou do utilitário oficial do fabricante (ex.: **`Samsung Magician`**).
3. **Limpeza Segura de Unidades NVMe (`Format NVM` vs. `Sanitize`)**:
   * **`Format NVM`**: Formata o *namespace* NVMe a baixo nível. Em unidades compatíveis com **`Cryptographic Erase`**, elimina a chave de encriptação interna do controlador e gera uma nova chave, invalidando instantaneamente os dados.
   * **`Sanitize`**: Operação profunda executada diretamente pelo firmware sobre toda a memória NAND física da unidade (incluindo *over-provisioning* e caches). **Não pode ser interrompida**: mesmo após um corte de energia ou reinício, o controlador NVMe retoma automaticamente a operação `Sanitize` no arranque até à conclusão.

#### Anatomia Didática do Comando Linux `nvme sanitize`

```text
nvme sanitize -a 2 /dev/nvme1
│    │        │  │  └─ Dispositivo de blocos alvo (controlador/unidade NVMe 1)
│    │        │  └──── Código de ação 2 = Block Erase ("block sanitize": limpa eletricamente todos os blocos NAND)
│    │        └─────── Flag -a (--sanact): especifica a ação de sanitização do controlador
│    └──────────────── Subcomando administrativo que inicia operação persistente no firmware (não interrompível)
└───────────────────── Utilitário CLI do pacote nvme-cli em Linux
```

#### Comparação: SATA `Secure Erase` vs. NVMe `Format NVM` vs. NVMe `Sanitize`

| Método de Firmware | Protocolo / Camada | Mecanismo Interno | Cobertura de Áreas Ocultas | Comportamento após Corte de Energia |
| :--- | :--- | :--- | :--- | :--- |
| **SATA `Secure Erase`** | ATA/SATA (via BIOS/UEFI ou ex.: `Samsung Magician`) | Descarga elétrica ou *reset* interno pelo controlador SATA | Inclui blocos físicos e *over-provisioning* | Depende da implementação do firmware; normalmente exige reinício do procedimento |
| **NVMe `Format NVM`** | NVMe (*Namespace*) | Formatação lógica/baixo nível ou **`Cryptographic Erase`** (rotação de chave) | Depende da opção; com *Crypto Erase* invalida toda a NAND cifrada | Comando de conclusão rápida na variante criptográfica |
| **NVMe `Sanitize`** | NVMe (Controlador global) | Limpeza física global (ex.: `-a 2` *Block Erase*) sobre toda a NAND | **Cobertura total** (NAND completa, caches e *over-provisioning*) | **Não pode ser parado**: o controlador retoma automaticamente no arranque seguinte |

---

## Perguntas de revisão

1. **Porque é que um *write blocker* de hardware não garante que dados apagados num SSD permaneçam intactos?**

> [!success]- Ver Resposta
> Porque o *write blocker* apenas bloqueia comandos de escrita vindos do computador/SO através da interface; o **processador interno do SSD**, assim que recebe alimentação elétrica, continua a executar autonomamente rotinas de *garbage collection* e *wear leveling*, podendo apagar definitivamente blocos libertados (especialmente após comandos `TRIM`).

2. **Qual a diferença entre a unidade mínima de escrita e a unidade mínima de apagamento numa memória `NAND Flash`?**

> [!success]- Ver Resposta
> A unidade mínima de escrita é uma **página/setor** (`512` ou `2 048` bytes úteis + `16`/`64` bytes de metadados), enquanto a unidade mínima de apagamento é um **bloco inteiro** (`16`, `32` ou `64` páginas, tipicamente `128 KB`). Por isso, ao modificar um ficheiro, o controlador grava numa nova página vazia e agenda a antiga para apagamento em bloco.

3. **O que demonstrou o estudo de Alnaqbi et al. (2025) após aplicar 3 passagens da norma `DoD 5220.22-M` numa pen USB usada de `16 GB`?**

> [!success]- Ver Resposta
> Mesmo após 3 passagens de sobreposição `DoD 5220.22-M`, o `PhotoRec` recuperou **`391` ficheiros** e o `Scalpel` recuperou **`1946` ficheiros**, provando que ferramentas de *overwriting* concebidas para discos magnéticos são ineficazes em memórias flash devido ao *wear leveling* e ao *over-provisioning* (5%–10% de blocos ocultos ao SO).

4. **Apresente as razões técnicas pelas quais o *degaussing* falha nos SSDs e indique os três métodos seguros para os sanitizar sem destruição física.**

> [!success]- Ver Resposta
> A memória `NAND Flash` armazena bits por carga elétrica em células semicondutoras e não por domínios magnéticos, pelo que o *degaussing* tem zero efeito. Os três métodos seguros reutilizáveis são: (1) **`Cryptographic Erasure`** (cifrar todo o disco previamente com `VeraCrypt` ou hardware SED e destruir a chave); (2) **SATA `Secure Erase`** (via BIOS/UEFI ou utilitário como `Samsung Magician`); e (3) **Comandos nativos NVMe** (`Format NVM` com `Cryptographic Erase` ou `Sanitize`).

5. **O que distingue o `Format NVM` do comando `Sanitize` em NVMe e o que significa cada componente de `nvme sanitize -a 2 /dev/nvme1`?**

> [!success]- Ver Resposta
> O `Format NVM` atua sobre o *namespace* NVMe (podendo fazer *Cryptographic Erase* por rotação de chave), enquanto o `Sanitize` executa uma sanitização física global em toda a memória NAND do controlador que **não pode ser interrompida** (retoma automaticamente após corte de energia). No comando, `nvme` é o utilitário CLI (`nvme-cli`), `sanitize` inicia a operação persistente no firmware, `-a 2` seleciona a ação `2` (*Block Erase* em todos os blocos NAND) e `/dev/nvme1` indica o dispositivo alvo.

---

## Notas relacionadas

- [[Arquitetura SSD vs Pen USB, Conetores M.2, PCIe e Apple SSD]]
- [[Cheat Sheet - Dispositivos de Armazenamento (HDD, ATA-SCSI, SSD e M.2)]]
- [[Procedimentos de Aquisição - Post-Mortem vs Live, Erros de Disco, HPA-DCO e Write Blockers]]
- [[Acesso a Discos (BIOS vs Direto) e Geometria de Discos Rígidos (CHS vs LBA)]]
- [[Arranque Forense e Processo de Boot (BIOS e Código Máquina)]]
- [[Ferramentas Gráficas de Aquisição Forense (Guymager, Paladin Toolbox, Tableau Imager e FTK Imager)]]
- [[Sanitização e Destruição de Discos Magnéticos (HDDs) - Wiping, Degaussing e Destruição Física]]
- [[Certificação de Sanitização, Audit Trail e Guia NCSC para Dispositivos Usados]]
- [[Decommissioning de Equipamentos, Destruição de Papel (P-1 a P-7) e Enquadramento Legal UE]]
- [[Gestão de Ativos (Asset Management) e Políticas de Armazenamento Amovível (VeraCrypt)]]
- [[System e OS Hardening e Vulnerabilidade BitLocker YellowKey (CVE-2026-45585)]]
