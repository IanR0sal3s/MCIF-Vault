---
title: Interfaces de Disco - ATA (IDE-PATA-SATA) e Áreas Protegidas (HPA e DCO)
tipo: nota
mestrado: Cibersegurança e Informática Forense
uc: Análise Forense Digital I
sigla_uc: AFD1
capitulo: 4
bloco: 1
tags:
  - afd1
  - forense
  - ata
  - sata
  - hpa
  - dco
  - hdparm
atualizado: 2026-11-16
---

# Interfaces de Disco - ATA (IDE-PATA-SATA) e Áreas Protegidas (HPA e DCO)

**Capítulo:** [[Capítulo 4 - Dispositivos de Armazenamento]]

> [!TIP] Lógica de Funcionamento e Valor Forense
> Um perito que confia cegamente no tamanho de disco reportado pelo sistema operativo (`IDENTIFY_DEVICE`) pode deixar de adquirir dezenas de megabytes ou gigabytes escondidos no final do disco. Em interfaces `ATA`/`SATA`, tanto a **`HPA`** (*Host Protected Area*) como a **`DCO`** (*Device Configuration Overlay*) permitem ocultar setores ao SO — servindo tanto para recuperação de fabricante como para esconder ficheiros ilegais ou *rootkits* persistentes.

## 1. Evolução da Interface ATA (*Advanced Technology Attachment*)

| Norma (Ano) | Sinónimos | Débito Máx. (Mbps) | Observações Técnicas |
| :--- | :--- | :---: | :--- |
| **ATA-1 (1994)** | `IDE` | 8,3 | Cabo de **40 fios**, comunicação paralela de 16 bits. |
| **ATA-2 (1996)** | `EIDE` | 16,7 | Suporte para **2 dispositivos por cabo**. |
| **ATA-3 (1997)** | — | 16,7 | Adiciona **SMART** e suporte de **passwords** no disco. |
| **ATA/ATAPI-4 (1998)** | — | 33,3 | Suporte a dispositivos removíveis (`CD-ROM`, `DVD`, ...) e introduz **`HPA`**. |
| **ATA/ATAPI-5 (2000)** | — | 66,7 | Cabo de **80 fios** para reduzir interferências eletromagnéticas. |
| **ATA/ATAPI-6 (2001)** | — | 100 | Endereçamento **LBA de 48 bits** e introduz **`DCO`**. |
| **ATA/ATAPI-7 (2002)** | — | 133 | Última grande revisão paralela (`PATA`). |
| **SATA 1.0 (2003)** | — | 1 500 | Cabo **série** (*serial*), transmitindo 1 bit após outro. |
| **SATA 2.0 (2004)** | — | 3 000 | — |
| **SATA 3.0 (2009)** | — | 6 000 | — |
| **SATA 3.1 (2011)** | — | 6 000 | Adiciona **`mini-SATA` (`mSATA`)** para SSDs. |
| **SATA 3.2 (2013)** | `SATA Express` | 16 000 | Integra barramento **`PCI Express`**. |

## 2. Host Protected Area (`HPA`)

Introduzida no **ATA-4**, a **HPA** é uma área especial reservada no **final do disco** para armazenar dados do fabricante, cuja capacidade pode ser de zero bytes e que **não é apagada por uma formatação normal** (persistência garantida). Requer reconfiguração do controlador para se tornar acessível.

- **Usos legítimos:** reduzir o tamanho visível do disco para BIOS antigas o reconhecerem, guardar ferramentas de diagnóstico, sistemas pré-carregados (botões dedicados), partições de recuperação (`IBM`, `LG`, ...) ou software anti-roubo.
- **Usos maliciosos/forenses:** ocultar ficheiros ilegais, alojar **rootkits** invisíveis ao antivírus (e *exploits* documentados da NSA que garantem persistência).

### Mecanismo ATA (`IDENTIFY_DEVICE` vs. `READ_NATIVE_MAX_ADDRESS`)
1. Sem HPA, `IDENTIFY_DEVICE` e `READ_NATIVE_MAX_ADDRESS` devolvem o mesmo tamanho real do disco.
2. O comando `SET_MAX_ADDRESS` altera o registo visível, criando a HPA no fim do disco.
3. Depois disso, `IDENTIFY_DEVICE` passa a devolver um tamanho reduzido (*fake size*), mas **`READ_NATIVE_MAX_ADDRESS` continua a devolver a capacidade nativa real**.

### Deteção e Criação em Linux (`dmesg` e `hdparm`)
```bash
# Verificar deteção pelo kernel no arranque
dmesg | less
# Exemplo: "hdb: Host Protected Area detected. current capacity is 12000 sectors (6 MB), native capacity is 120103200 sectors (61492 MB)"

# Comparar setores atuais vs. nativos com hdparm
sudo hdparm -N /dev/sdX
# Se mostrar: max sectors = 976773168/976773168 -> HPA está desativada

# Criar (ou alterar temporariamente) uma HPA definindo ZZZZZ setores visíveis
sudo hdparm -N pZZZZZ /dev/sdX
```

## 3. Device Configuration Overlay (`DCO`)

Introduzida no **ATA-6**, a **DCO** permite ocultar a capacidade real do disco de forma mais profunda do que a HPA:
- Com `DCO`, **tanto a BIOS como o SO veem exatamente o mesmo tamanho reduzido**.
- Permite aos fabricantes de PC comprar discos de marcas/tamanhos diferentes e configurá-los para apresentarem exatamente a mesma capacidade.
- **Coexistência no mesmo disco:** Um disco pode ter simultaneamente área normal + `HPA` + `DCO` no fim:
  - `IDENTIFY_DEVICE` $\rightarrow$ fim dos *User Addressable Sectors*
  - `READ_NATIVE_MAX_ADDRESS` $\rightarrow$ fim da `HPA`
  - `DEVICE_CONFIGURATION_IDENTITY` $\rightarrow$ fim real absoluto (após a `DCO`)
- **Remoção permanente:** Ao contrário da HPA (cuja remoção pode ser temporária), **a remoção da DCO é permanente** e **pode destruir dados** se não for feita com extremo cuidado forense. Não é possível criar uma nova DCO com `hdparm`, apenas removê-la.

### Deteção e Remoção de DCO em Linux e Ferramentas Windows
```bash
# 1. Consultar a DCO real
sudo hdparm --dco-identify /dev/sdX
# Observar: "Real max sectors: 976773168"

# 2. Comparar com os setores endereçáveis reportados ao SO
sudo hdparm -Iv /dev/sdX
# Observar: "LBA48 user addressable sectors: 976773168" (se for menor, existe DCO!)

# 3. Remover DCO e restaurar o tamanho real (CUIDADO: PODE DESTRUIR DADOS PERMANENTEMENTE)
sudo hdparm --yes-i-know-what-i-am-doing --dco-restore /dev/sdX
```
- **Ferramentas Windows:** `TAFT` (*The ATA Forensics Tool* — antiga, menciona disquetes) e `SAFE-Block` (deteta `HPA` e `DCO` e permite repô-las).

*(Ver também [[Procedimentos de Aquisição - Post-Mortem vs Live, Erros de Disco, HPA-DCO e Write Blockers]].)*

## Além da aula

> [!NOTE] Conteúdo Complementar (Além da aula)
> Cuidado pericial essencial com `HPA`/`DCO` e *write blockers*:

- **Write Blockers e Comandos ATA:** Nem todos os *write blockers* permitem que `hdparm --dco-restore` ou `SET_MAX_ADDRESS` sejam executados (pois são comandos que alteram registos de configuração da drive), ou podem bloquear a leitura além do limite reportado se não suportarem desbloqueio temporário de HPA. Em aquisições forenses rigorosas, verifique primeiro se o *write blocker* (ex.: Tableau) reporta HPA/DCO e documente os valores de `hdparm -N` e `--dco-identify` antes de qualquer alteração.

## Perguntas de revisão

1. **Qual a diferença fundamental entre `HPA` e `DCO` quanto à visibilidade e reversibilidade?**
   > [!success]- Ver Resposta
   > Na `HPA` (ATA-4), `READ_NATIVE_MAX_ADDRESS` revela o tamanho real atrás da HPA e a sua remoção pode ser temporária; na `DCO` (ATA-6), tanto a BIOS como o SO veem o tamanho reduzido (sendo necessário `DEVICE_CONFIGURATION_IDENTITY` / `--dco-identify` para ver o máximo real) e a sua remoção com `hdparm --dco-restore` é **permanente**.

2. **Se `hdparm -N /dev/sdX` devolver `max sectors = 976773168/976773168`, o que podemos concluir?**
   > [!success]- Ver Resposta
   > Como os setores atuais visíveis coincidem com os setores nativos máximos (`976773168/976773168`), a `HPA` está desativada (embora ainda se deva verificar separadamente se existe uma `DCO` com `hdparm --dco-identify`).

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Acesso a Discos (BIOS vs Direto) e Geometria de Discos Rígidos (CHS vs LBA)]] | `mesmo bloco` |
| **Seguinte** | [[Interface SCSI, SAS e Comparação SCSI vs ATA]] | `mesmo bloco` |
| **Índice** | [[Capítulo 4 - Dispositivos de Armazenamento]] · [[00 AFD1]] | `Bloco 01` |

### Conceitos Relacionados

* [[Procedimentos de Aquisição - Post-Mortem vs Live, Erros de Disco, HPA-DCO e Write Blockers]] · `Cap. 2`
