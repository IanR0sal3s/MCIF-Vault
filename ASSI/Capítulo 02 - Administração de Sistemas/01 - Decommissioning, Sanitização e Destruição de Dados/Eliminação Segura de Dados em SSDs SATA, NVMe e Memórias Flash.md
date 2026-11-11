---
title: Eliminação Segura de Dados em SSDs SATA, NVMe e Memórias Flash
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
  - ssd
  - nvme
  - nand-flash
  - secure-erase
  - cryptographic-erasure
  - photorec
  - scalpel
aliases:
  - Secure Erase SSD
  - Secure Erase NVMe
  - nvme sanitize
  - Cryptographic Erasure
  - Format NVM
  - Sanitização de Memória Flash
atualizado: 2026-11-11
---

# Eliminação Segura de Dados em SSDs SATA, NVMe e Memórias Flash

Memórias **NAND Flash** (SSDs SATA/NVMe e pens USB) são imunes ao *degaussing* e resistem ao *overwriting* por terem 5%–10% de *over-provisioning* e *wear leveling*, exigindo cifragem ou comandos de firmware.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: As células NAND Flash não permitem sobrescrita direta no mesmo local antes de um ciclo prévio de apagamento de bloco. Para otimizar desempenho e longevidade, o controlador (*Flash Translation Layer — FTL*) distribui as escritas por múltiplos chips (*wear leveling*), redireciona modificações para blocos limpos e mantém **5% a 10% de capacidade reservada (*over-provisioning*)** oculta ao sistema operativo.
> * **Porque importa (Segurança / Forense)**: Ferramentas clássicas de *wiping* ao nível do sistema operativo (como `DoD 5220.22-M`) não alcançam células remapeadas nem o *over-provisioning*, permitindo recuperar centenas ou milhares de ficheiros com *file carving* (`PhotoRec`, `Scalpel` — estudo de Alnaqbi et al., 2025). Em forense digital, esta retenção explica porque é que ficheiros apagados sobrevivem em páginas antigas até à atuação do `TRIM`, *garbage collection* ou comandos de firmware.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Imunidade magnética**: o *degaussing* não tem **qualquer efeito** em NAND Flash (armazenamento por carga elétrica, não magnético);
>   * **Estudo Alnaqbi et al. (2025)**: após 3 passagens `DoD 5220.22-M` numa pen USB de `16 GB`, o `PhotoRec` recuperou **`391` ficheiros** e o `Scalpel` **`1946` ficheiros**;
>   * **`nvme sanitize` vs. `Format NVM`**: o `Sanitize` atua em toda a NAND física e **não pode ser interrompido** (retoma automaticamente após corte de energia); no comando `nvme sanitize -a 2 /dev/nvme1`, `-a 2` indica **Block Erase**.

---

## 1. Ineficácia do *Overwriting* Clássico em Memórias Flash (Estudo de Alnaqbi et al., 2025 — Slide 21)

No estudo empírico de **Alnaqbi, M. M., Alblooshi, S. T., Alshamsi, E. A., Seghid, N., & Iqbal, F. (2025, Abril)** — *"An Empirical Analysis of Security and Privacy Issues Associated with Selling and Purchasing of Secondhand Storage Devices"* (*2025 13th International Symposium on Digital Forensics and Security — ISDFS*):

* Os autores analisaram uma **pen USB de `16 GB` adquirida em segunda mão**;
* Aplicaram sobreposição de dados com a norma **`DoD 5220.22-M` (3 passagens)**;
* **Resultados forenses obtidos após as 3 passagens**:
  * **`391` ficheiros recuperados** com a ferramenta de *file carving* **`PhotoRec`**;
  * **`1946` ficheiros recuperados** com a ferramenta de *file carving* **`Scalpel`**.
* **Conclusão**: os utilitários tradicionais de *overwriting* desenhados para discos magnéticos **não são adequados para dispositivos baseados em memória flash**.

---

## 2. Arquitetura NAND Flash: Imunidade ao *Degaussing* e Persistência de Dados (Slides 22–24)

### 2.1. Imunidade ao *Degaussing* (Slide 23)
Os SSDs e pens USB empregam memória **NAND Flash**, que armazena bits através de carga elétrica em células semicondutoras e não de domínios magnéticos. Por essa razão, **o *degaussing* não tem qualquer efeito sobre memórias NAND Flash**.

### 2.2. *Over-provisioning*, *Wear Leveling* e Células Não Endereçáveis (Slides 23–24)

* **5% a 10% de blocos ocultos ao SO (*Over-provisioning*)**: todo o SSD reserva entre **5% e 10%** de blocos físicos indisponíveis ao sistema operativo para gestão interna e substituição de blocos gastos — áreas que **nunca são tocadas por ferramentas de *wiping* do SO**;
* **Organização em páginas e blocos**: os dados são gravados em **páginas (*pages*)** agrupadas em **blocos (*blocks*)** e **espalhados por todos os chips do SSD** pelo controlador através da *Flash Translation Layer* (*FTL*) e do mecanismo de *wear leveling*;
* **Escrita em blocos limpos e *Garbage Collection***: quando um ficheiro é alterado ou sobrescrito, o controlador **escreve os novos dados em blocos previamente limpos**, marcando as páginas antigas apenas como inválidas para posterior recolha de lixo (*garbage collection*);
* **Consequência crítica**: dados supostamente eliminados ou sobrescritos podem permanecer intactos em **células de memória não endereçáveis pelo sistema operativo (*non-addressable memory cells*)**.

---

## 3. Como Apagar um SSD com Segurança Sem o Destruir Fisicamente (Slides 23–24)

### 3.1. Apagamento Criptográfico (*Cryptographic Erasure*)
Consiste em **cifrar previamente todo o conteúdo da unidade** (por exemplo, com **`VeraCrypt`** ou com a cifragem interna de hardware de um *Self-Encrypting Drive — SED*) usando uma chave forte aleatória. No abate, elimina-se apenas a chave de encriptação (*Master Encryption Key*), tornando todos os blocos físicos — incluindo os 5%–10% de *over-provisioning* — instantaneamente indecifráveis.

### 3.2. Limpeza Segura de SSDs SATA (*SATA SSD Secure Erase* — Slide 24)
Aciona diretamente o controlador do SSD para executar a descarga elétrica interna de todas as células NAND, incluindo áreas ocultas ao SO:

1. **Função `"Secure Erase"` integrada na BIOS/UEFI** da *motherboard*;
2. **Comando SATA `"Secure Erase"` do firmware**, invocado através do utilitário oficial do fabricante (ex.: **`Samsung Magician`**).

### 3.3. Limpeza Segura de Unidades NVMe (`Format NVM` vs. `Sanitize` — Slide 24)
O protocolo **NVMe (*Non-Volatile Memory Express*)** fornece dois comandos nativos de administração do controlador:

* **`Format NVM`**: formata o *namespace* NVMe a baixo nível. Em unidades compatíveis com a opção **`Cryptographic Erase`**, elimina a chave de encriptação interna do controlador e gera uma nova chave, invalidando instantaneamente todos os dados.
* **`Sanitize`**: operação profunda de sanitização executada diretamente pelo firmware sobre toda a memória NAND física da unidade (incluindo *over-provisioning* e caches). **Não pode ser interrompida**: mesmo após um corte de energia ou reinício, o controlador NVMe retoma automaticamente a operação `Sanitize` no arranque até à conclusão.

### Anatomia Didática do Comando Linux `nvme sanitize`

```text
nvme sanitize -a 2 /dev/nvme1
│    │        │  │  └─ Dispositivo de blocos alvo (controlador/unidade NVMe 1)
│    │        │  └──── Código de ação 2 = Block Erase ("block sanitize": limpa eletricamente todos os blocos NAND)
│    │        └─────── Flag -a (--sanact): especifica a ação de sanitização do controlador
│    └──────────────── Subcomando administrativo que inicia operação persistente no firmware (não interrompível)
└───────────────────── Utilitário CLI do pacote nvme-cli em Linux
```

---

## 4. Tabelas Comparativas: HDD vs. SSD/Flash e Comandos de Sanitização

### 4.1. HDD Magnético vs. SSD / Memória NAND Flash

| Critério Técnico | Disco Magnético (HDD) | SSD / Memória NAND Flash |
| :--- | :--- | :--- |
| **Meio físico de gravação** | Domínios magnéticos em pratos rotativos | Carga elétrica em células NAND (páginas/blocos) |
| **Efeito do *Degaussing*** | Destrói dados e `tracks` (inutiliza o HDD) | **Zero efeito** (imune a campos magnéticos) |
| **Efeito do *Overwriting* pelo SO** | Eficaz nos setores endereçáveis; permite reutilização | **Insuficiente** (deixa dados em *over-provisioning* e células remapeadas) |
| **Zonas ocultas ao SO** | Eventual HPA/DCO ou setores realocados | **5%–10% de *over-provisioning*** + páginas antigas antes de *garbage collection* |
| **Método seguro reutilizável** | *Wiping* completo (`Eraser`, `DBAN`, `KillDisk`) | **Cryptographic Erasure**, **SATA `Secure Erase`**, **NVMe `Format NVM` / `Sanitize`** |

### 4.2. SATA `Secure Erase` vs. NVMe `Format NVM` vs. NVMe `Sanitize`

| Método de Firmware | Protocolo / Camada | Mecanismo Interno | Cobertura de Áreas Ocultas | Comportamento após Corte de Energia |
| :--- | :--- | :--- | :--- | :--- |
| **SATA `Secure Erase`** | ATA/SATA (via BIOS/UEFI ou ex.: `Samsung Magician`) | Descarga elétrica ou reset interno pelo controlador SATA | Inclui blocos físicos e *over-provisioning* | Depende da implementação do firmware; normalmente exige reinício do procedimento |
| **NVMe `Format NVM`** | NVMe (*Namespace*) | Formatação lógica/baixo nível ou **`Cryptographic Erase`** (rotação de chave) | Depende da opção; com *Crypto Erase* invalida toda a NAND cifrada | Comando de conclusão rápida na variante criptográfica |
| **NVMe `Sanitize`** | NVMe (Controlador global) | Limpeza física global (ex.: `-a 2` *Block Erase*) sobre toda a NAND | **Cobertura total** (NAND completa, caches e *over-provisioning*) | **Não pode ser parado**: o controlador retoma automaticamente no arranque seguinte |

---

## Além da aula

* **Implicações na Aquisição Forense de SSDs e Comandos `TRIM` (`AFD1` Cap. 2)**: A arquitetura em páginas/blocos e a recolha de lixo (*garbage collection* / `TRIM`) explicam porque é que, na aquisição forense de computadores modernos com SSDs soldados à *motherboard* (exigindo [[Arranque Forense e Processo de Boot (BIOS e Código Máquina)]] e os procedimentos de [[Procedimentos de Aquisição - Post-Mortem vs Live, Erros de Disco, HPA-DCO e Write Blockers]]), arrancar o sistema operativo alvo pode provocar a destruição automática de evidência apagada. Enquanto `Secure Erase` ou `TRIM` não atuam, a retenção em células não endereçáveis explica a recuperação maciça por *carving* demonstrada por Alnaqbi et al. (2025) — comparável à análise em [[Ferramentas Gráficas de Aquisição Forense (Guymager, Paladin Toolbox, Tableau Imager e FTK Imager)]].
* **Ligação com Políticas `VeraCrypt` (`ASSI` Cap. 2 Bloco 02)**: O princípio do *Cryptographic Erasure* apoia-se diretamente na obrigatoriedade de cifragem integral de dispositivos e suportes amovíveis definida em [[Gestão de Ativos (Asset Management) e Políticas de Armazenamento Amovível (VeraCrypt)]].

---

## Perguntas de revisão

1. **O que demonstrou o estudo de Alnaqbi et al. (2025) após aplicar 3 passagens da norma `DoD 5220.22-M` numa pen USB usada de 16 GB?**

> [!success]- Ver Resposta
> Mesmo após 3 passagens de sobreposição `DoD 5220.22-M`, a ferramenta de *file carving* **`PhotoRec`** conseguiu recuperar **`391` ficheiros** e o **`Scalpel`** recuperou **`1946` ficheiros**, provando que ferramentas de *overwriting* concebidas para discos magnéticos são ineficazes em memórias flash.

2. **Apresente as razões técnicas pelas quais o *degaussing* e o *overwriting* ao nível do sistema operativo falham nos SSDs.**

> [!success]- Ver Resposta
> Primeiro, a memória NAND Flash armazena dados através de cargas elétricas e não de campos magnéticos, tornando o *degaussing* totalmente ineficaz. Segundo, os SSDs reservam **5% a 10% de blocos de *over-provisioning*** ocultos ao SO e utilizam *wear leveling* para escrever alterações em blocos limpos, deixando os dados antigos em **células de memória não endereçáveis pelo SO** até ocorrer *garbage collection*.

3. **Quais são os três métodos seguros para sanitizar um SSD mantendo-o funcional?**

> [!success]- Ver Resposta
> (1) **Cryptographic Erasure** (cifrar todo o disco previamente com `VeraCrypt` ou hardware SED e destruir a chave de encriptação); (2) **SATA `Secure Erase`** (invocado via função integrada na BIOS/UEFI ou utilitário do fabricante como o `Samsung Magician`); e (3) **Comandos nativos NVMe** (`Format NVM` com `Cryptographic Erase` ou `Sanitize`).

4. **O que distingue o `Format NVM` do comando `Sanitize` em NVMe e o que significa cada componente de `nvme sanitize -a 2 /dev/nvme1`?**

> [!success]- Ver Resposta
> O `Format NVM` formata o *namespace* NVMe (podendo executar *Cryptographic Erase* ao eliminar a chave interna), enquanto o `Sanitize` executa uma sanitização física global sobre toda a memória NAND do controlador que **não pode ser interrompida** (retoma automaticamente após corte de energia). Em `nvme sanitize -a 2 /dev/nvme1`: `nvme` é o utilitário CLI Linux, `sanitize` inicia a sanitização persistente no firmware, `-a 2` define a ação `2 = block sanitize` (*Block Erase* em todos os blocos NAND) e `/dev/nvme1` identifica o dispositivo alvo.

---

## Notas relacionadas

- [[Capítulo 2 - Administração de Sistemas]]
- [[Sanitização e Destruição de Discos Magnéticos (HDDs) - Wiping, Degaussing e Destruição Física]]
- [[Certificação de Sanitização, Audit Trail e Guia NCSC para Dispositivos Usados]]
- [[Decommissioning de Equipamentos, Destruição de Papel (P-1 a P-7) e Enquadramento Legal UE]]
- [[Gestão de Ativos (Asset Management) e Políticas de Armazenamento Amovível (VeraCrypt)]]
- [[System e OS Hardening e Vulnerabilidade BitLocker YellowKey (CVE-2026-45585)]]
- [[Arranque Forense e Processo de Boot (BIOS e Código Máquina)]]
- [[Procedimentos de Aquisição - Post-Mortem vs Live, Erros de Disco, HPA-DCO e Write Blockers]]
