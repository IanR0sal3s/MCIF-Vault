---
title: Cheat Sheet - Dispositivos de Armazenamento (HDD, ATA-SCSI, SSD e M.2)
tipo: cheat-sheet
mestrado: Cibersegurança e Informática Forense
uc: Análise Forense Digital I
sigla_uc: AFD1
capitulo: 4
tags:
  - afd1
  - cheat-sheet
  - forense
  - hdd
  - ssd
  - hpa
  - dco
  - hdparm
atualizado: 2026-11-16
---

# Cheat Sheet — Dispositivos de Armazenamento (HDD, ATA/SCSI, SSD e M.2)

**Capítulo:** [[Capítulo 4 - Dispositivos de Armazenamento]] | **UC:** [[00 AFD1]]

> [!ABSTRACT] Referência Rápida para Exame e Laboratório
> Fórmulas de geometria, comandos `hdparm` para deteção de áreas escondidas (`HPA`/`DCO`), tabelas comparativas e lista de exercícios práticos do Capítulo 4.

---

## 1. Geometria HDD (`CHS` $\leftrightarrow$ `LBA`)

- **Limites `CHS`:** `504 MB` (original) $\rightarrow$ `8,1 GB` (com tradução por geometria falsa).
- **Conversão `CHS` $\rightarrow$ `LBA`:**
  $$\text{LBA} = (C \times \max_H + H) \times \max_S + (S - 1)$$
  *(Onde $C \in [0, \max_C]$, $H \in [0, \max_H]$, $S \in [1, \max_S]$).*

---

## 2. Áreas Escondidas em ATA (`HPA` & `DCO`)

| Área | Norma | Visibilidade | Reversibilidade | Comando `hdparm` |
| :--- | :--- | :--- | :--- | :--- |
| **`HPA`** | ATA-4 | `IDENTIFY_DEVICE` devolve tamanho falso; `READ_NATIVE_MAX_ADDRESS` devolve tamanho real | Remoção pode ser temporária | `sudo hdparm -N /dev/sdX` (ver) / `-N pZZZZZ` (criar) |
| **`DCO`** | ATA-6 | BIOS e SO veem o mesmo tamanho reduzido; requer `DEVICE_CONFIGURATION_IDENTITY` | **Remoção permanente** (pode destruir dados!) | `sudo hdparm --dco-identify /dev/sdX` vs. `hdparm -Iv /dev/sdX` |

```bash
# Verificar HPA nos logs de arranque
dmesg | grep -i "Host Protected Area"

# Remover DCO (PERIGO: permanente, pode destruir dados)
sudo hdparm --yes-i-know-what-i-am-doing --dco-restore /dev/sdX
```

---

## 3. `HDD` vs. `SSD` (`NAND`) — Pontos Críticos Forenses

- **Unidade mínima de escrita:** `HDD` = 1 setor (`512 B`) \| `SSD` = 1 setor (`512 B` ou `2 048 B`).
- **Unidade mínima de apagamento / *bad block*:** `HDD` = 1 setor (`512 B`) \| `SSD` = **1 bloco inteiro** (`16`, `32` ou `64` setores, típ. `128 KB`).
- **Flash `NOR` vs. `NAND`:** `NOR` (`< 16 MB`, BIOS, execução local sem RAM, escrita até 5 s) vs. `NAND` (alta densidade, SSD/USB, escrita até 4 ms, acesso por blocos).
- **Regra de Ouro Forense em SSD:** Um ***write blocker* NÃO bloqueia *garbage collection* nem *wear leveling*** — basta haver alimentação elétrica para o processador interno do SSD apagar blocos livres e mudar setores físicos de lugar.

---

## 4. Camadas `M.2` (`NGFF`) e Chaves

- **Layer 1 (Conetor):** `M.2` \| **Layer 2 (Link):** `SATA` ou `PCIe` \| **Layer 3 (Transporte):** `SATA`, `AHCI` ou `NVMe`.
- **Chaves:** `B key` (6 contactos), `M key` (5 contactos — `PCIe x4 NVMe`), `B & M key`.

---

## 5. Exercícios Práticos do Capítulo 4

- **`04-Lab 1`:** Adicionar um disco `RAW` a uma máquina virtual.
- **`04.2-Lab 1`:** Comparar especificações e preços de SSDs (`SATA`, `M.2 SATA`, `M.2 NVMe`).
- **`04.2-Lab 2`:** Análise de saúde e atributos de discos com **`smartmontools`** (`smartctl`).
