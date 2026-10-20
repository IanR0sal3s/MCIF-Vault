---
title: Aquisição e Montagem em Linux - Formato EWF (ewf-tools, ewfmount e xmount)
tipo: procedimento
mestrado: Cibersegurança e Informática Forense
uc: Análise Forense Digital I
sigla_uc: AFD1
capitulo: 2
bloco: 5
fonte_aula: MCIF – Digital Forensic Analysis 1 - Forensic Boot.pdf
tags:
  - afd1
  - forense
  - aquisicao
  - linux
  - ewf
  - e01
  - ewf-tools
  - ewfacquire
  - ewfmount
  - xmount
  - udisksctl
  - cftt
aliases:
  - Expert Witness Format
  - EWF
  - E01
  - ewf-tools
  - ewfacquire
  - ewfmount
  - xmount
atualizado: 2026-10-20
---

# Aquisição e Montagem em Linux — Formato EWF (`ewf-tools`, `ewfmount` e `xmount`)

As ferramentas de aquisição de dados dividem-se entre utilitários gráficos para Windows (**FTK Imager**, **Tableau Imager**) e Linux (**Guymager**) e ferramentas de linha de comandos em Linux (**`ewf-tools`**, **`dd`** e derivados), todas avaliadas pelo projeto **CFTT (*Computer Forensic Tool Testing*)**. O formato **Expert Witness Format (EWF — `.E01`, `.E02`)**, originalmente proprietário do EnCase, pode ser manipulado em Linux através da suite aberta **`ewf-tools`** (`ewfacquire`, `ewfverify`, `ewfinfo`, `ewfexport`, `ewfmount`) e montado em 2 passos quer com privilégios `sudo` (`ewfmount` + `mount`) quer de forma segura por um utilizador regular (`xmount --cache` + `udisksctl`).

---

## 1. Panorama de Ferramentas de Aquisição e Projeto CFTT

### Ferramentas por Sistema Operativo
* **Windows (com interface gráfica GUI)**: `FTK Imager`, `Tableau Imager`, entre outros.
* **Linux**:
  * **Interface Gráfica (GUI)**: `Guymager`, `Paladin Toolbox`.
  * **Linha de Comandos (CMD)**: `ewf-tools`, `dd` e ferramentas derivadas (`dcfldd`, `dc3dd`, `ddrescue`, `dd_rescue`, `rdd`, ...).

### Projeto *Computer Forensic Tool Testing (CFTT)*
* Desenvolvido pelo NIST, o projeto **CFTT**:
  * Desenvolve **casos de teste (*test-cases*)** padronizados para ferramentas de informática forense.
  * Testa rigorosamente as ferramentas e **publica os resultados oficiais** para consulta pela comunidade pericial e pelos tribunais.

---

## 2. O Formato *Expert Witness Format (EWF)* e a Suite `ewf-tools`

* **Características do formato EWF**:
  * Formato originalmente proprietário da ferramenta **EnCase**, que **suporta compressão** e metadados embutidos.
  * Extensões de ficheiro segmentadas: **`.E01`**, **`.E02`**, etc.
* **Instalação da suite *open source* em Linux (Debian/Ubuntu)**:
  ```bash
  sudo apt install ewf-tools
  ```

### Utilitários da Suite `ewf-tools`

| Comando | Função Forense |
| :--- | :--- |
| **`ewfacquire`** | Adquire dados de uma unidade de armazenamento **localmente** (*acquire drive data locally*). |
| **`ewfacquirestream`** | Adquire dados de uma unidade **remotamente** a partir de um fluxo/stream (*acquire drive data remotely*). |
| **`ewfmount`** | Monta imagens EWF (a imagem passa a ser vista pelo sistema como um ficheiro bruto `RAW`). |
| **`ewfexport`** | Converte formatos de ficheiros de imagem (ex.: converter EnCase `.E01` para `.raw`: `ewfexport -f raw filename.E??`). |
| **`ewfinfo`** | Extrai e exibe os metadados embutidos num ficheiro de imagem EWF (ex.: `ewfinfo nps-2008-jean.E0*`). |
| **`ewfrecover`** | Tenta recuperar ficheiros EWF corrompidos (*tries to recover corrupted EWF files*). |
| **`ewfverify`** | **Valida a integridade do ficheiro EWF** $\rightarrow$ **muito importante antes de iniciar qualquer análise!** |

---

## 3. Exemplo Prático de Aquisição Interativa com `ewfacquire`

Ao executar `ewfacquire` apontando para o dispositivo de bloco (`/dev/sdd`), a ferramenta deteta automaticamente os metadados de hardware (fabricante, modelo, número de série, capacidade e bytes por setor) e solicita interativamente os dados de cadeia de custódia e nível de compressão:

```text
ewfacquire /dev/sdd                  # comando emitido
ewfacquire 20130416                  # informação gerada pela ferramenta

Device information:
Bus type:
Vendor:                              ATA
Model:                               VMware Virtual I
Serial:                              00000000000000000001

Storage media information:
Type:                                Device
Media type:                          Fixed
Media size:                          53 MB (53477376 bytes)
Bytes per sector:                    512

Acquiry parameters required, please provide the necessary input
Image path and filename without extension: example    # parte interativa
Case number: 001
Description: This is just a test
Evidence number: 000001
Examiner name: Miguel Frade                           # quem realizou a aquisição
Notes: Virtual disc drive
(...)
Compression level (none, empty-block, fast, best) [none]: best   # opção de compressão
(...)
```

---

## 4. Montagem de Imagens EWF em Linux (Processo em 2 Passos)

Montar uma imagem EWF para navegar no sistema de ficheiros contido no seu interior é sempre um **processo de 2 etapas**:
1. **Passo 1**: Montar o contentor `EWF` para que seja visto como um disco bruto (`RAW disk`).
2. **Passo 2**: Montar o sistema de ficheiros contido no disco `RAW`.

### Comparação das Opções de Montagem
* **Em Windows**: **FTK Imager** (extremamente simples e direto).
* **Em Linux**:
  * **Opção A (`ewfmount` ou `xmount` + `mount`)**: Requer privilégios **`sudo`**, mas **permite ver a `$MFT` diretamente como um ficheiro** (graças à opção `show_sys_files`).
  * **Opção B (`xmount` + `udisksctl`)**: É a **opção mais segura (*the safest option*)**, podendo ser executada por um **utilizador regular (sem `sudo`)** e suportando emulação de escrita via ficheiro de *cache*.

---

### Opção A: Montagem com `ewfmount` + `mount` (Com `sudo`)

**Passo 1** — Mapear os segmentos `.E01/.E02` como um ficheiro `RAW` (`/mnt/raw/ewf1`):
```bash
sudo ewfmount nps-2008-jean.E?? /mnt/raw
```
* Mapeia a imagem como um ficheiro `RAW`.
* É estritamente **só de leitura (*read only*)**, não sendo possível emular operações de escrita.

**Passo 2** — Montar o sistema de ficheiros NTFS contido na imagem `RAW`:
```bash
sudo mount -t ntfs -o ro,loop,show_sys_files,streams_interface=windows,offset=$[63*512] /mnt/raw/ewf1 /mnt/loop/
```
* **`ro,loop`**: Monta em modo só de leitura através de um dispositivo de *loop*.
* **`show_sys_files`**: Permite visualizar estruturas internas do sistema de ficheiros NTFS (como `$MFT`, `$LogFile`, `$BitMap`) como ficheiros normais.
* **`streams_interface=windows`**: Permite aceder aos dados de **Alternate Data Streams (ADS)** usando a sintaxe nativa do Windows (`ficheiro:stream`).
* **`offset=$[63*512]`**: Deslocamento (*offset*) em bytes até ao início da partição a montar (neste exemplo, a partição começa no setor `63` e cada setor tem `512 bytes`, resultando no byte `32256`).

---

### Opção B: Montagem com `xmount` + `udisksctl` (Sem `sudo` / Mais Segura)

**Pré-requisito de configuração única no sistema** (o utilizador precisa de pertencer aos grupos `fuse` e `disk`, podendo exigir reinício da sessão):
```bash
sudo groupadd fuse
sudo usermod -a -G fuse $USER
sudo usermod -a -G disk $USER
echo "user_allow_other" | sudo tee -a /etc/fuse.conf
```

**Passo 1** — Mapear a imagem EWF como ficheiro `RAW` com emulação de escrita em *cache*:
```bash
xmount --in ewf nps-2008-jean.E?? --out raw --cache cachefile /mnt
```
* Mapeia os ficheiros EWF como uma imagem `RAW` (`/mnt/nps-2008-jean.dd`).
* O argumento `--cache cachefile` faz com que o `xmount` **emule operações de escrita utilizando um ficheiro de cache separado**, mantendo a evidência original 100% intocada.

**Passo 2** — Criar dispositivos de *loop* para cada partição identificada na imagem `RAW`:
```bash
udisksctl loop-setup -f /mnt/nps-2008-jean.dd
```
* Cria um dispositivo `/dev/loop0pX` para cada partição existente no disco.
* Para verificar quantas partições foram identificadas: `ls /dev/loop0*`.

**Passo 3** — Montar a primeira partição sem privilégios de `root`:
```bash
udisksctl mount -b /dev/loop0p1
```

---

## Implicações Forenses

* **Verificação Antes da Análise (`ewfverify`)**: O passo `ewfverify` antes de iniciar o exame pericial garante que os *checksums* CRC por bloco e o resumo MD5/SHA1 embutidos no `.E01` coincidem com o momento da aquisição (cumprindo o Princípio 3 de Manuseamento da Evidência estudado em [[Princípios e Rota do Manuseamento de Evidência Digital]]).
* **Porquê escolher `mount` com `show_sys_files` vs. `xmount + udisksctl`?**: Se o objetivo do perito for extrair os meta-ficheiros ocultos do NTFS (`$MFT`, `$UsnJrnl`) ou inspecionar *Alternate Data Streams (ADS)* diretamente na árvore montada, a Opção A (`mount -o ro,loop,show_sys_files,streams_interface=windows`) é ideal. Se o objetivo for montar uma partição sem correr o risco de executar comandos como `root` ou quando uma ferramenta exige permissões de escrita simuladas (como abrir uma base de dados SQLite/ESE que precisa de criar ficheiros temporários de bloqueio), a Opção B (`xmount --cache` + `udisksctl`) é a mais segura.

---

## Além da aula

* **Ponte com a Catalogação LabCIF e Artefactos do Windows em [[00 ASSI|ASSI]]**:
  * Os metadados extraídos automaticamente pelo `ewfacquire` (`Vendor`, `Model`, `Serial`, `Media size`) e os parâmetros inseridos (`Case number`, `Evidence number`, `Examiner name`) alimentam diretamente a tabela de catalogação de dispositivos exigida pelas regras do laboratório em [[Registo, Etiquetagem e Fotografia Pericial (Regras LabCIF)]] e [[Exercício de Projeto - Catalogação e Etiquetagem de Dispositivos e Serviços]].
  * Uma vez montada a partição NTFS em `/mnt/loop/` ou `/media/$USER/...`, o perito pode apontar as ferramentas estudadas em **ASSI** diretamente para os ficheiros extraídos da imagem:
    * Hives do Registry em `Windows/System32/config/` e `Users/<user>/NTUSER.DAT` ([[Estrutura e Hives do Windows Registry]], [[Ferramentas de Análise e Extração do Registry]], [[AmCache - Arquitetura, Hives e Evolução para SQLite]]).
    * Ficheiros `.pf` em `Windows/Prefetch/` ([[Análise Forense e Criação a Pedido do Prefetch]]).
    * Base ESE do SRUM em `Windows/System32/sru/SRUDB.dat` ([[System Resource Usage Monitor (SRUM) - Arquitetura e Base ESE]]).

---

## Perguntas de revisão

- Qual é a finalidade de cada uma das sete ferramentas que compõem o pacote `ewf-tools` (`ewfacquire`, `ewfacquirestream`, `ewfmount`, `ewfexport`, `ewfinfo`, `ewfrecover` e `ewfverify`)?
- Porque é que a montagem de uma imagem EWF em Linux é um processo de dois passos?
- No comando `sudo mount -t ntfs -o ro,loop,show_sys_files,streams_interface=windows,offset=$[63*512]`, qual é o efeito específico das opções `show_sys_files`, `streams_interface=windows` e `offset=$[63*512]`?
- Quais são as duas grandes vantagens periciais de utilizar a combinação `xmount --cache` + `udisksctl` face à montagem tradicional com `sudo mount`?

## Notas relacionadas

- [[Aquisição em Linha de Comandos no Linux - dcfldd e Derivados do dd]]
- [[Ferramentas Gráficas de Aquisição Forense (Guymager, Paladin Toolbox, Tableau Imager e FTK Imager)]]
- [[Armazenamento da Aquisição - Clonagem vs Imagem, Formatos, Aquisição Remota e Assinatura de Hashes]]
- [[Princípios e Rota do Manuseamento de Evidência Digital]]
- [[Registo, Etiquetagem e Fotografia Pericial (Regras LabCIF)]]
- [[Estrutura e Hives do Windows Registry]]
- [[Análise Forense e Criação a Pedido do Prefetch]]
- [[System Resource Usage Monitor (SRUM) - Arquitetura e Base ESE]]
- [[Capítulo 2 - Arranque e Aquisição Forense]]
