---
title: Interface SCSI, SAS e Comparação SCSI vs ATA
tipo: nota
mestrado: Cibersegurança e Informática Forense
uc: Análise Forense Digital I
sigla_uc: AFD1
capitulo: 4
bloco: 1
tags:
  - afd1
  - forense
  - scsi
  - sas
  - ata
atualizado: 2026-11-16
---

# Interface SCSI, SAS e Comparação SCSI vs ATA

**Capítulo:** [[Capítulo 4 - Dispositivos de Armazenamento]]

> [!TIP] Lógica de Funcionamento e Valor Forense
> Em servidores empresariais, sistemas NAS e infraestruturas de alta disponibilidade, o perito encontra frequentemente discos **`SCSI`** ou **`SAS`** em vez de `SATA` doméstico. Reconhecer os múltiplos conectores físicos, o funcionamento em barramento direto e a ausência de áreas `HPA`/`DCO` em SCSI evita erros de compatibilidade e de aquisição no terreno.

## 1. Small Computer Systems Interface (`SCSI`)

- **Capacidade de ligação:** Permite ligar até **8 ou 16 dispositivos** no mesmo cabo (e até **65 535** em arquitetura `SAS`).
- **Controlo de erros nos comandos:** Utiliza paridade (`SCSI-1`, `SCSI-2`) ou `CRC32` (`SCSI-3`).
- **Aplicações típicas:** Servidores e sistemas de elevado desempenho:
  - **`FCP` (*SCSI-over-Fibre Channel Protocol*):** Sistemas `NAS`/`SAN`.
  - **`SAS` (*Serial Attached SCSI*):** Cabos série; permite ligar também dispositivos **`SATA-2+`**.
  - **`UAS` (*USB Attached SCSI*):** Discos externos USB com protocolo SCSI.
- **Desvantagens práticas:** Mais caros do que discos ATA e grande variedade de conectores (`DB25m` Mac-SCSI, `C50m`, `IDC50m`/`IDC50f` SCSI-1, `HD50m` SCSI-2, `HD68m`/`HD68f` SCSI-3), o que gera frequentemente confusão na escolha de adaptadores.

### Evolução da Interface SCSI / SAS

| Versão | Comp. Máx. Cabo | Débito Máximo | N.º Máx. Dispositivos |
| :--- | :---: | :---: | :---: |
| **SCSI-1** | 6 m | 5 MBps | 8 |
| **Fast SCSI** | 3 m | 10 MBps | 8 |
| **Fast Wide SCSI** | 3 m | 20 MBps | 16 |
| **Ultra SCSI** | 3 m | 20 MBps | 4 |
| **Wide Ultra SCSI** | 1,5 m / 3 m | 40 MBps | 8 / 4 |
| **Ultra2 SCSI** | 4 m | 40 MBps | 8 |
| **Wide Ultra2 SCSI** | 4 m | 80 MBps | 16 |
| **Ultra160 SCSI** | 4 m | 160 MBps | 16 |
| **Ultra320 SCSI** | 4 m | 320 MBps | 16 |
| **SAS (2006 / 2009 / 2013)** | — | 3 Gbps / 6 Gbps / **12 Gbps** | **65 535** |

## 2. Comparação Direta: `ATA` vs. `SCSI`

| Característica | ATA | SCSI |
| :--- | :--- | :--- |
| **Dispositivos por cabo** | Até 2 | Até 8 (ou 16) |
| **Comunicação** | Por controlador (*by controller*) | Direta por barramento (*direct by bus*) |
| **Comunicação paralela** | Sim, 16 bits | Sim, 8 ou 16 bits |
| **Fios por cabo paralelo** | 40 ou 80 | 50 ou 68 |
| **Comunicação série** | $\ge$ SATA-1 | *Serial Attached SCSI* (`SAS`) |
| **Disponibilidade** | Comum / consumo | Sistemas de alta disponibilidade |
| **Tolerância a falhas** | — | Fonte de alimentação (*power supply*) / redundância |
| **Tamanho de disco** | Limitado nas versões antigas | `LBA` de **32 ou 64 bits** |
| **Rotações por minuto (RPM)** | 4,5k / 7,2k / 10k | 10k / 15k |
| **Áreas escondidas** | **`HPA`**, **`DCO`** | — (não possui HPA/DCO) |

## Além da aula

> [!NOTE] Conteúdo Complementar (Além da aula)
> Nota prática de laboratório pericial:

- **Compatibilidade assimétrica `SAS` vs. `SATA`:** Uma controladora/backplane **`SAS`** aceita discos `SATA-2+` (como referido nos slides), mas uma controladora **`SATA`** doméstica **não** lê um disco **`SAS`** — algo crucial ao preparar *write blockers* e estações de aquisição para discos extraídos de servidores empresariais.

## Perguntas de revisão

1. **Porque é que a verificação de áreas `HPA` e `DCO` se aplica a discos `ATA`/`SATA`, mas não a discos `SCSI`?**
   > [!success]- Ver Resposta
   > Porque as áreas protegidas `HPA` (ATA-4) e `DCO` (ATA-6) são funcionalidades específicas do conjunto de comandos `ATA`, não existindo na arquitetura `SCSI`.

2. **Um disco `SATA-3` pode ser ligado a uma controladora `SAS`? E o inverso?**
   > [!success]- Ver Resposta
   > Um disco `SATA-2+` pode ser ligado a uma controladora `SAS` (que mantém retrocompatibilidade), mas o inverso não é possível: uma controladora `SATA` não suporta discos `SAS`.

## Notas relacionadas
- [[Interfaces de Disco - ATA (IDE-PATA-SATA) e Áreas Protegidas (HPA e DCO)]]
- [[Acesso a Discos (BIOS vs Direto) e Geometria de Discos Rígidos (CHS vs LBA)]]
- [[Arquitetura SSD vs Pen USB, Conetores M.2, PCIe e Apple SSD]]
