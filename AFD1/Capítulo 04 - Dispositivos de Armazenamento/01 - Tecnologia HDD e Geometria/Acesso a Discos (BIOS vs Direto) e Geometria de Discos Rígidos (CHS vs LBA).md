---
title: Acesso a Discos (BIOS vs Direto) e Geometria de Discos Rígidos (CHS vs LBA)
tipo: nota
mestrado: Cibersegurança e Informática Forense
uc: Análise Forense Digital I
sigla_uc: AFD1
capitulo: 4
bloco: 1
tags:
  - afd1
  - forense
  - hdd
  - geometria
  - chs
  - lba
  - bios
atualizado: 2026-11-16
---

# Acesso a Discos (BIOS vs Direto) e Geometria de Discos Rígidos (CHS vs LBA)

**Capítulo:** [[Capítulo 4 - Dispositivos de Armazenamento]]

> [!TIP] Lógica de Funcionamento e Valor Forense
> Os discos rígidos magnéticos (`HDD`) constituem historicamente a principal forma de armazenamento não volátil e a fonte primária de evidência digital (embora progressivamente substituídos por `SSD`). Compreender como o sistema operativo acede ao controlador e como os setores são endereçados (`CHS` vs. `LBA`) é essencial para interpretar partições, sistemas de ficheiros antigos e imagens forenses brutas.

## 1. Acesso Direto vs. Acesso via BIOS

| Modo de Acesso | Mecanismo | Vantagens e Limitações | Uso Atual |
| :--- | :--- | :--- | :--- |
| **Acesso Direto (sem BIOS)** | O software comunica diretamente com o controlador do disco, enviando códigos de comando (`read`, `write`, consulta de tipo/tamanho). | Mais complexo de programar, mas **muito mais rápido** e sem restrições herdadas da BIOS. | Utilizado por **todos os sistemas operativos modernos** após o arranque. |
| **Acesso via BIOS** | O software invoca serviços da BIOS (`INT 13h` e `extended INT 13h`) para comunicar com o hardware. | Mais simples (a BIOS trata do baixo nível), mas **mais lento**. | Hoje em dia restringe-se praticamente ao **processo de arranque (*boot*)**. |

## 2. Estrutura Física e Formatação de Baixo Nível (*Low-Level Format*)

No interior de um `HDD` encontram-se pratos (*platters*) revestidos a **liga de cobalto**, lidos e escritos por cabeças magnéticas. Embora alguns sistemas de ficheiros usem valores de geometria, os discos atuais escondem a geometria física real por trás do controlador.

A formatação de baixo nível cria as estruturas físicas básicas:
- **Pistas (*Tracks*):** Anéis concêntricos numa superfície de prato, numerados a partir do exterior.
- **Cilindros (*Cylinders*):** Conjunto de todas as pistas na mesma posição radial em todos os pratos: $C \in [0, \max_C]$.
- **Cabeças (*Heads*):** Selecionam a superfície/pista respetiva: $H \in [0, \max_H]$.
- **Setores (*Sectors*):** Subdivisão das pistas, tipicamente com **512 bytes** de dados úteis, numerados a partir de **1**: $S \in [1, \max_S]$. Cada setor físico inclui informação de sincronização, cabeçalho (*header*), dados, código de correção de erros (*ECC* — *Error-Correcting Code*) e *trailer*, separados por *intersector* e *intertrack gaps*.
- ***Cluster* / *Block*:** Agrupamento lógico de setores utilizado pelo sistema de ficheiros (em sistemas Unix/Linux usa-se o termo *block* com o mesmo significado de *cluster*).

### Distribuição de Setores (*Zone Bit Recording*)
Nos discos antigos, todas as pistas tinham o mesmo número de setores geométricos (desperdiçando espaço nas pistas exteriores mais longas). Nos discos modernos, as pistas são agrupadas em **zonas** (ex.: Zona 0 exterior com 15 setores/pista até Zona 4 interior com 6 setores/pista), permitindo maior densidade de armazenamento.

## 3. Esquemas de Endereçamento: `CHS` vs. `LBA`

- **CHS (*Cylinder, Head, Sector*):** Usado apenas em sistemas antigos; endereça cada setor pelo terno $(C, H, S)$.
  - Capacidade máxima endereçável original: **504 MB**.
  - Com tradução por **geometria falsa** (*fake geometry*), conseguiu-se contornar o limite inicial até ao máximo de **8,1 GB**.
- **LBA (*Logical Block Addressing*):** Cada setor possui um único endereço linear sequencial (a partir de `0`), eliminando a necessidade de o software conhecer a geometria física do disco.
  - Usado diretamente em sistemas de ficheiros Linux, BSD, macOS, etc. (enquanto `FAT` e `NTFS` mantêm campos `CHS` legados nas suas estruturas).

### Conversão `CHS` $\rightarrow$ `LBA`
$$\text{LBA} = (C \times \max_H + H) \times \max_S + (S - 1)$$

*(Nota: $C$ e $H$ começam em `0`, enquanto $S$ começa em `1`, daí o termo $S - 1$.)*

## Além da aula

> [!NOTE] Conteúdo Complementar (Além da aula)
> Ligação prática à análise forense de partições:

- **Limites 504 MB vs. 8,1 GB em Análise Forense:** Quando se analisam tabelas de partições `MBR` legadas (ver [[Capítulo 3 - Organização de Dados]]), campos `CHS` saturados no valor máximo (`1023 / 254 / 63`, equivalente a ~8,1 GB) indicam que o particionamento passou a depender exclusivamente dos campos `LBA` de 32 bits (que suportam até $2^{32} \times 512\text{ B} = 2\text{ TiB}$).

## Perguntas de revisão

1. **Porque é que na fórmula de conversão `CHS` $\rightarrow$ `LBA` aparece `(S - 1)`?**
   > [!success]- Ver Resposta
   > Porque a numeração de cilindros ($C$) e cabeças ($H$) é baseada em zero ($0$), enquanto os setores ($S$) são numerados a partir de $1$ ($S \in [1, \max_S]$).

2. **Qual a diferença entre o acesso ao disco via `INT 13h` da BIOS e o acesso direto utilizado pelos sistemas operativos modernos?**
   > [!success]- Ver Resposta
   > O acesso via `INT 13h` delega na BIOS a comunicação com o hardware, sendo mais simples mas lento e limitado (usado hoje apenas durante o *boot*); o acesso direto envia comandos diretamente ao controlador do disco, sendo mais complexo mas substancialmente mais rápido.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Capítulo 4 - Dispositivos de Armazenamento]] | Início do capítulo |
| **Seguinte** | [[Interfaces de Disco - ATA (IDE-PATA-SATA) e Áreas Protegidas (HPA e DCO)]] | `mesmo bloco` |
| **Índice** | [[Capítulo 4 - Dispositivos de Armazenamento]] · [[00 AFD1]] | `Bloco 01` |

### Conceitos Relacionados

* [[Interface SCSI, SAS e Comparação SCSI vs ATA]] · `mesmo bloco`
* [[Camadas de Organização de Dados e Análise de Sistemas de Ficheiros]] · `Cap. 3`
