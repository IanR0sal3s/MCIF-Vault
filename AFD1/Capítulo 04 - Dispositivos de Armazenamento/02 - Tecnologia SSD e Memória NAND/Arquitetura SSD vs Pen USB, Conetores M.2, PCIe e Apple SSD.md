---
title: Arquitetura SSD vs Pen USB, Conetores M.2, PCIe e Apple SSD
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
  - usb
  - m2
  - nvme
  - pcie
  - apple-ssd
atualizado: 2026-11-16
---

# Arquitetura SSD vs Pen USB, Conetores M.2, PCIe e Apple SSD

**Capítulo:** [[Capítulo 4 - Dispositivos de Armazenamento]]

> [!TIP] Lógica de Funcionamento e Valor Forense
> Na receção de evidências no laboratório, o perito precisa de distinguir imediatamente entre um conetor físico (`M.2`), a interface elétrica de ligação (`SATA` vs. `PCIe`) e o protocolo de transporte (`AHCI` vs. `NVMe`), além de reconhecer conetores proprietários (como os da Apple) e perceber porque é que a recuperação física de um `SSD` avariado é radicalmente mais complexa do que a de um `HDD`.

## 1. Produção de Memória Flash: *Consumer* vs. *Industrial Grade*

Segundo a **Micron** (maior fabricante mundial de chips NAND), após o fabrico do *wafer*, as células são testadas e classificadas em *bad*, *weak* e *strong die*:
- Os blocos maus (*bad*) são marcados/excluídos.
- Os restantes são separados em memória Flash de qualidade **industrial** e de **consumo (*consumer grade*)**, sendo esta última a que chega às lojas de retalho — explicando as enormes diferenças de velocidade de escrita entre dispositivos aparentemente semelhantes.

## 2. Arquitetura: USB Pen Drive vs. SSD

| Aspeto | USB Pen Drive | Solid-State Drive (SSD) |
| :--- | :--- | :--- |
| **Processador próprio** | **Não possui** processador interno dedicada. | **Possui processador interno** próprio. |
| **Dependência de CPU/Driver** | Requer **driver de armazenamento em massa** no SO e usa o **CPU do computador** para calcular `ECC`, gerir *bad blocks* e *wear leveling*. | **Não requer driver especial** nem CPU do host (emula comandos `SATA` para compatibilidade). |
| **Componentes internos** | Memória flash + interface USB simples. | Controlador Flash + **Processador interno** + **Cache `SRAM`** + **Flash `NOR` de boot** + módulo **`ECC`** + **Buffers** + bancos de chips **`NAND`**. |
| **Reparação / Recuperação física** | Limitada ao chip NAND (*chip-off*). | **Extremamente complexa**, possível apenas em laboratórios altamente especializados (ao contrário do `HDD`, onde se trocam placas controladoras ou cabeças mantendo os pratos). |

## 3. Camadas de Ligação: Conetores, Interfaces e Protocolos

1. **Conetores (Layer 1 — Interface física):** Ex.: `M.2`, `RJ45`, `SATA`...
2. **Interfaces de Ligação / *Link Interfaces* (Layer 2 — Codificação de dados):** Ex.: `PCIe`, `SATA`.
3. **Protocolos de Transporte (Layer 3 — Comunicação de dados):** Ex.: `NVMe`, `AHCI`, `IDE`.

### M.2 (antigo *NGFF — Next Generation Form Factor*)
Substitui o padrão `mSATA`, sendo flexível e ideal para ultrabooks, tablets e SSDs compactos. **Um único conetor físico `M.2` suporta múltiplas combinações:**
- `M.2` = interface `SATA` + protocolo `SATA`
- `M.2` = interface `PCIe` + protocolo `AHCI`
- `M.2` = interface `PCIe 3.0` (até 4 pistas) + protocolo **`NVMe`** (*Non-Volatile Memory Express*, desenhado para paralelizar milhares de operações I/O em PCIe).
- Suporta ainda `SATA 3.0` e `USB 3.0` (o fabricante decide quais interfaces estão ativas).

### Entalhes de Chaveamento (*Keying Notches*) no M.2
Para impedir a inserção em slots incompatíveis (SSD, Wi-Fi, modem 4G, etc.), existem entalhes distintos:
- **`B key`:** entalhe de 6 contactos/pinos (posições 12–19).
- **`M key`:** entalhe de 5 contactos/pinos (posições 59–66) — típico de SSDs `PCIe x4 NVMe`.
- **`B & M key`:** ambos os entalhes — comum em SSDs `M.2 SATA` ou `PCIe x2`.

## 4. Barramento `PCIe` e Conetores Proprietários Apple SSD

### Evolução do Barramento `PCIe` (`GT/s` = Gigatransfers/s)

| Versão | Ano | Taxa de Transferência | $\times 1$ | $\times 4$ (típico M.2) | $\times 16$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **PCIe 1.0** | 2003 | 2,5 GT/s | 250 MB/s | 1,00 GB/s | 4,00 GB/s |
| **PCIe 2.0** | 2007 | 5,0 GT/s | 500 MB/s | 2,00 GB/s | 8,00 GB/s |
| **PCIe 3.0** | 2010 | 8,0 GT/s | 984,6 MB/s | 3,94 GB/s | 15,75 GB/s |
| **PCIe 4.0** | 2017 | 16,0 GT/s | 1 969 MB/s | 7,88 GB/s | 31,51 GB/s |
| **PCIe 5.0** | 2019 | 32,0 GT/s | 3 938 MB/s | 15,75 GB/s | 63,02 GB/s |

### Conetores Proprietários Apple SSD (MacBook Air / Pro)

| Geração | Ano | Conetor (pinos) | Interface |
| :--- | :---: | :---: | :--- |
| **G1** | 2010 | `6+12` | `mSATA 3` |
| **G2** | 2011 | `7+17` | `mSATA 3` |
| **G3** | 2012 | `12+16` | `PCIe 2.0 x2` |
| **G4** | 2013 | `12+16` | `PCIe 3.0 x4` |
| **G5A / G5B** | 2015 | `22+34` / `12+16` | `PCIe 3.0 x4 NVMe` |

## Além da aula

> [!NOTE] Conteúdo Complementar (Além da aula)
> Preparação de adaptadores num kit de aquisição forense:

- **Identificação de M.2 SATA vs. M.2 NVMe antes de ligar:** Um adaptador USB-to-M.2 barato frequentemente suporta **apenas** `M.2 SATA` **ou** **apenas** `M.2 NVMe` (embora existam pontes dual-protocolo `RTL9210B`). Verifique sempre as especificações do SSD apreendido e a chave (`M` vs. `B&M`) antes de adquirir; para MacBooks com SSD removível (2010–2015), é indispensável manter adaptadores específicos `G1`–`G5` para ligar ao *write blocker*.

## Perguntas de revisão

1. **Porque é que uma pen USB sobrecarrega o CPU do computador durante a escrita/leitura enquanto um SSD não o faz?**
   > [!success]- Ver Resposta
   > Porque a **pen USB não tem processador próprio**, dependendo de um driver de software no SO e do CPU do host para calcular `ECC`, gerir *bad blocks* e executar *wear leveling*. O **SSD possui o seu próprio processador interno** para gerir todas essas operações autonomamente.

2. **Um conetor físico `M.2` implica automaticamente que o disco utiliza o protocolo `NVMe`?**
   > [!success]- Ver Resposta
   > Não. `M.2` é apenas o **conetor físico** (Layer 1). Um SSD M.2 pode usar interface `SATA` + protocolo `SATA`, interface `PCIe` + protocolo `AHCI`, ou interface `PCIe` + protocolo `NVMe`.

## Notas relacionadas
- [[Arquitetura SSD e Memória NAND (Wear Leveling e Garbage Collection)]]
- [[Interfaces de Disco - ATA (IDE-PATA-SATA) e Áreas Protegidas (HPA e DCO)]]
- [[Interface SCSI, SAS e Comparação SCSI vs ATA]]
