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
atualizado: 2026-11-11
---

# Aquisição e Montagem em Linux — Formato EWF (`ewf-tools`, `ewfmount` e `xmount`)

No Linux, o formato EWF (`.E01`) é adquirido e validado pela suite `ewf-tools` (`ewfacquire`, `ewfverify`) e montado em dois passos via `ewfmount + mount` ou `xmount --cache + udisksctl`.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema / Método)**: O formato **Expert Witness Format (`EWF` / `.E01`)** encapsula dados comprimidos, *checksums* CRC e metadados de cadeia de custódia; por ser um contentor estruturado, o kernel Linux requer primeiro a exposição do contentor como disco bruto (`RAW`) antes de montar a partição interna.
> * **Porque importa (Forense)**: Validar o `.E01` com `ewfverify` antes da análise garante a integridade desde a aquisição; escolher corretamente entre `ewfmount + sudo mount` (acesso a `$MFT` e fluxos ADS) e `xmount --cache + udisksctl` (sem privilégios `root` e com emulação segura de escrita) preserva a evidência intacta.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Projeto CFTT (NIST)**: Desenvolve casos de teste padronizados e publica resultados de conformidade para ferramentas forenses.
>   * **7 Utilitários `ewf-tools`**: `ewfacquire` (local), `ewfacquirestream` (remoto), `ewfmount` (expõe como RAW), `ewfexport` (converte ex. `.E01` $\rightarrow$ `.raw`), `ewfinfo` (metadados), `ewfrecover` (recuperação) e `ewfverify` (validação obrigatória).
>   * **Montagem NTFS em 2 Passos**: `show_sys_files` expõe `$MFT`/`$LogFile`; `streams_interface=windows` expõe fluxos **ADS**; `offset=$[63*512]` posiciona no byte `32256`.

---

## 1. Panorama de Ferramentas de Aquisição e Projeto CFTT

### Ferramentas por Sistema Operativo

* **Windows (com interface gráfica GUI)**: `FTK Imager`, `Tableau Imager`, entre outros.
* **Linux**:
  * **Interface Gráfica (GUI)**: `Guymager`, `Paladin Toolbox`.
  * **Linha de Comandos (CMD)**: `ewf-tools`, `dd` e ferramentas derivadas (`dcfldd`, `dc3dd`, `ddrescue`, `dd_rescue`, `rdd`, ...).

### Projeto *Computer Forensic Tool Testing (CFTT)*

* Desenvolvido pelo NIST, o projeto **CFTT**:
  * Desenvolve **casos de teste** padronizados para ferramentas de informática forense.
  * Testa rigorosamente as ferramentas e **publica os resultados oficiais** para consulta pela comunidade pericial e pelos tribunais.

---

## 2. O Formato *Expert Witness Format (EWF)* e a Suite `ewf-tools`

* **Características do formato EWF**:
  * Formato originalmente proprietário da ferramenta **EnCase**, que **suporta compressão** e metadados embutidos.
  * Extensões de ficheiro segmentadas: **`.E01`**, **`.E02`**, etc.

**Instalação da suite *open source* em Linux (Debian/Ubuntu):**

```bash
sudo apt install ewf-tools
```

### Anatomia Completa dos 7 Utilitários da Suite `ewf-tools`

| Comando | Sintaxe / Exemplo Típico | Função Forense e Contexto de Uso |
| :--- | :--- | :--- |
| **`ewfacquire`** | `ewfacquire /dev/sdd` | Adquire dados de uma unidade de armazenamento **localmente** em formato EWF, recolhendo metadados de cadeia de custódia e compressão. |
| **`ewfacquirestream`** | *via pipe/stream de rede* | Adquire dados de uma unidade **remotamente** a partir de um fluxo (*stream*) de entrada padrão. |
| **`ewfmount`** | `sudo ewfmount img.E?? /mnt/raw` | Monta contentores EWF de modo a que a imagem seja exposta pelo sistema como um ficheiro bruto **`RAW`** (`/mnt/raw/ewf1`). |
| **`ewfexport`** | `ewfexport -f raw filename.E??` | Converte formatos de ficheiros de imagem (ex.: converter segmentos `.E01/.E02` para imagem bruta `.raw`). |
| **`ewfinfo`** | `ewfinfo nps-2008-jean.E0*` | Extrai e exibe os metadados embutidos no cabeçalho EWF (caso, perito, notas, geometria, compressão e *hashes*). |
| **`ewfrecover`** | `ewfrecover corrupted.E01` | Tenta recuperar dados de ficheiros EWF corrompidos ou truncados. |
| **`ewfverify`** | `ewfverify nps-2008-jean.E0*` | **Valida a integridade criptográfica do ficheiro EWF** $\rightarrow$ **passo essencial antes de iniciar qualquer análise!** |

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

*(Nota: Em Windows, a montagem de imagens `.E01` é feita diretamente com o **FTK Imager**, de forma simples e imediata).*

### Comparação Técnica: `ewfmount + sudo mount` vs. `xmount --cache + udisksctl`

| Critério Técnico | Opção A: `ewfmount + sudo mount` | Opção B: `xmount --cache + udisksctl` |
| :--- | :--- | :--- |
| **Privilégios Executados** | Requer **`sudo`** (`root`) em ambos os passos. | **Não requer `sudo` na montagem** (utilizador regular nos grupos `fuse` e `disk`, com `user_allow_other` em `/etc/fuse.conf`). |
| **Visibilidade da `$MFT` e Meta-Ficheiros** | **Sim** — a opção **`show_sys_files`** expõe `$MFT`, `$LogFile` e `$BitMap` diretamente como ficheiros. | **Não expostos por omissão** na montagem padrão gerida pelo `udisksctl`. |
| **Acesso a *Alternate Data Streams* (ADS)** | **Sim** — a opção **`streams_interface=windows`** permite ler fluxos ADS na sintaxe `ficheiro:stream`. | Montagem padrão sem ativação explícita de `streams_interface=windows`. |
| **Emulação de Escrita (*Cache*)** | Estritamente **só de leitura (*read-only*)**; não emula operações de escrita. | **Sim (`--cache cachefile`)** — simula escritas num ficheiro de *cache* separado, mantendo a evidência original intacta. |
| **Descoberta de Partições** | Exige especificar manualmente o deslocamento em bytes (`offset=$[63*512]`). | **`udisksctl loop-setup`** deteta automaticamente a tabela de partições e cria `/dev/loop0pX` para cada partição. |
| **Quando Escolher** | Extração direta de `$MFT`, `$UsnJrnl` ou fluxos **ADS** (`Zone.Identifier`). | **Opção mais segura** para utilizador regular e para ferramentas que necessitam de escrita simulada (SQLite/ESE). |

---

### Opção A: Montagem com `ewfmount` + `mount` (Com `sudo`)

**Passo 1** — Mapear os segmentos `.E01/.E02` como um ficheiro `RAW` (`/mnt/raw/ewf1`):

```bash
sudo ewfmount nps-2008-jean.E?? /mnt/raw
```

* Mapeia a imagem como um ficheiro `RAW`.
* É estritamente **só de leitura**, não sendo possível emular operações de escrita.

**Passo 2** — Montar o sistema de ficheiros NTFS contido na imagem `RAW`:

```bash
sudo mount -t ntfs -o ro,loop,show_sys_files,streams_interface=windows,offset=$[63*512] /mnt/raw/ewf1 /mnt/loop/
```

* **`ro,loop`**: Monta em modo só de leitura através de um dispositivo de *loop*.
* **`show_sys_files`**: Permite visualizar estruturas internas do sistema de ficheiros NTFS (como `$MFT`, `$LogFile`, `$BitMap`) como ficheiros normais.
* **`streams_interface=windows`**: Permite aceder aos dados de **Alternate Data Streams (ADS)** usando a sintaxe nativa do Windows (`ficheiro:stream`).
* **`offset=$[63*512]`**: Deslocamento em bytes até ao início da partição a montar (neste exemplo, a partição começa no setor `63` e cada setor tem `512 bytes`, resultando no byte `32256`).

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
    * *Alternate Data Streams (ADS)* e proveniência Web (`Zone.Identifier`) expostas pela opção `streams_interface=windows` ([[Alternate Data Streams (ADS) no NTFS - Arquitetura, Manipulação em CMD e PowerShell]], [[Mark of the Web (MOTW) e Zone.Identifier - Formato, Zonas URLZONE e Verbosidade dos Browsers]] e [[Exceções à MOTW (Ficheiros Compactados, 7-Zip, certutil LOLBin) e Microsoft Defender SmartScreen]]).
    * Varrimento offline da partição montada com [[Conceito de Strings e Comando strings em Unix-Linux|strings]], [[YARA - Introdução, Estrutura de Regras, Metadados e Condições|YARA]], [[YARA-X (Reimplementação em Rust) e Ferramenta CLI yr|YARA-X]] e [[Loki-RS (Versão Rust) - Compilação, Atualização e Parâmetros CLI|Loki-RS]].

---

## Perguntas de revisão

1. **Qual é a finalidade de cada uma das sete ferramentas que compõem o pacote `ewf-tools` (`ewfacquire`, `ewfacquirestream`, `ewfmount`, `ewfexport`, `ewfinfo`, `ewfrecover` e `ewfverify`)?**

> [!success]- Ver Resposta
> * **`ewfacquire`**: adquire discos localmente para formato EWF.
> * **`ewfacquirestream`**: adquire dados remotamente a partir de um *stream*.
> * **`ewfmount`**: monta imagens EWF expondo-as como um ficheiro `RAW`.
> * **`ewfexport`**: converte imagens EWF para outros formatos (ex.: `.raw`).
> * **`ewfinfo`**: exibe os metadados embutidos na imagem EWF.
> * **`ewfrecover`**: tenta recuperar ficheiros EWF corrompidos.
> * **`ewfverify`**: valida a integridade da imagem EWF antes da análise.

2. **Porque é que a montagem de uma imagem EWF em Linux é um processo de dois passos?**

> [!success]- Ver Resposta
> Porque o ficheiro `.E01/.E02` é um contentor comprimido e estruturado com metadados; o sistema operativo precisa primeiro de um tradutor (`ewfmount` ou `xmount`) que exponha o contentor como um disco bruto (`RAW`), para só no segundo passo montar o sistema de ficheiros contido numa partição desse disco (`mount` ou `udisksctl`).

3. **No comando `sudo mount -t ntfs -o ro,loop,show_sys_files,streams_interface=windows,offset=$[63*512]`, qual é o efeito específico das opções `show_sys_files`, `streams_interface=windows` e `offset=$[63*512]`?**

> [!success]- Ver Resposta
> * **`show_sys_files`**: expõe os ficheiros de sistema internos do NTFS (`$MFT`, `$LogFile`, `$BitMap`) como ficheiros acessíveis.
> * **`streams_interface=windows`**: permite ler *Alternate Data Streams (ADS)* usando a sintaxe `ficheiro:stream`.
> * **`offset=$[63*512]`**: indica o deslocamento inicial em bytes (`32256 bytes`) onde começa a partição dentro da imagem de disco completo.

4. **Quais são as duas grandes vantagens periciais de utilizar a combinação `xmount --cache` + `udisksctl` face à montagem tradicional com `sudo mount`?**

> [!success]- Ver Resposta
> Permite realizar a montagem sem privilégios **`sudo`** (utilizador regular nos grupos `fuse` e `disk`, reduzindo riscos de segurança) e suporta **emulação de escrita (`--cache cachefile`)** num ficheiro de *cache* separado, deixando a imagem forense original 100% intacta.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Armazenamento da Aquisição - Clonagem vs Imagem, Formatos, Aquisição Remota e Assinatura de Hashes]] | `Bloco 04` |
| **Seguinte** | [[Aquisição em Linha de Comandos no Linux - dcfldd e Derivados do dd]] | `mesmo bloco` |
| **Índice** | [[Capítulo 2 - Arranque e Aquisição Forense]] · [[00 AFD1]] | `Bloco 05` |

### Conceitos Relacionados

* [[Ferramentas Gráficas de Aquisição Forense (Guymager, Paladin Toolbox, Tableau Imager e FTK Imager)]] · `mesmo bloco`
* [[Princípios e Rota do Manuseamento de Evidência Digital]] · `Cap. 1`
* [[Registo, Etiquetagem e Fotografia Pericial (Regras LabCIF)]] · `Cap. 1`
* [[Estrutura e Hives do Windows Registry]] · `ASSI · Cap. 1`
* [[Análise Forense e Criação a Pedido do Prefetch]] · `ASSI · Cap. 1`
* [[System Resource Usage Monitor (SRUM) - Arquitetura e Base ESE]] · `ASSI · Cap. 1`
