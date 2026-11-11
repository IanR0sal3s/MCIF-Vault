---
title: Dispositivos de Arranque Forense - Disquetes DOS, Live CDs Linux, WinFE e USB
tipo: procedimento
mestrado: Cibersegurança e Informática Forense
uc: Análise Forense Digital I
sigla_uc: AFD1
capitulo: 2
bloco: 2
fonte_aula: MCIF – Digital Forensic Analysis 1 - Forensic Boot.pdf
tags:
  - afd1
  - forense
  - forensic-boot
  - msdos
  - paladin
  - deft
  - winfe
  - ventoy
  - rufus
  - dd
aliases:
  - Forensic Boot Tools
  - Bootable Diskette
  - WinFE
  - Windows Forensic Environment
  - Paladin Linux
  - DEFT Linux
  - Ventoy
  - Bootable USB Devices
atualizado: 2026-11-11
---

# Dispositivos de Arranque Forense — Disquetes DOS, Live CDs Linux, WinFE e USB

Os dispositivos de arranque forense evoluíram das disquetes MS-DOS para Live CDs Linux (**Paladin**, **DEFT**), ambientes Windows (**WinFE**, **SAFE**) e pens USB com **Ventoy**, **Rufus** ou `dd`.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema / Método)**: Arrancar o computador suspeito a partir de um sistema operativo de confiança externo impede que o sistema instalado no disco interno inicie e altere registos, metadados ou espaço não alocado durante a aquisição.
> * **Porque importa (Forense)**: Sistemas *Live* comuns montam automaticamente partições NTFS ou ativam partições de *swap* (alterando a evidência); ambientes forenses dedicados (**Paladin**, **DEFT**, **WinFE**) desativam o *automount* de discos internos e garantem acesso controlado ou só de leitura.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **3 Ficheiros Obrigatórios MS-DOS**: `IO.SYS` (referido nos slides como `O.SYS`), `MSDOS.SYS` e `COMMAND.COM` — ficheiros extra como `DRVSPACE.BIN`, `CONFIG.SYS` e `AUTOEXEC.BAT` têm de ser limpos com `attrib -H -R -S` após `format a: /U /S`.
>   * **WinFE vs. Linux Live CD**: O **WinFE** (Brett Shavers) corre software Windows nativo (`FTK Imager`, `RegRipper`), mas exige construção prévia e licença Windows; **Paladin**/**DEFT** dispensam licença, mas exigem familiaridade com Linux.
>   * **Gravação USB com `dd`**: `sudo dd bs=4M if=input.iso of=/dev/sdx conv=fdatasync` garante a sincronização física dos *buffers* antes do fecho do comando.

---

## Quadro Comparativo Rápido: DOS vs. Linux Live CD vs. WinFE vs. Ventoy

| Ambiente / Suporte | Base / Sistema | Ferramentas e Utilização | Preparação e Licença | Limitações / Cuidados Forenses |
| :--- | :--- | :--- | :--- | :--- |
| **Disquete MS-DOS** | MS-DOS (`O.SYS`/`IO.SYS`, `MSDOS.SYS`, `COMMAND.COM`) | Utilitários DOS e *write-blockers* em máquinas industriais/legadas | `format a: /U /S` + limpeza `attrib -H -R -S` (ou *HP USB Tool*) | Obsoleto para hardware atual; requer remoção manual de ficheiros de arranque extra |
| **Linux Live CD (`Paladin`, `DEFT`)** | Linux (*Ubuntu Live* / forense) | GUI forenses (Autopsy, *Paladin Toolbox*) e CLI | Descarregar `.iso` e gravar em CD ou USB; gratuito | Nem todos os *first responders* se sentem confortáveis a usar Linux |
| **WinFE** | *Windows PE* modificado | Software nativo Windows (`FTK Imager`, `RegRipper`) | Gratuito, mas exige **construção prévia** e licença válida de Windows | Requer configuração antecipada antes da intervenção em campo |
| **Ventoy** | Gestor USB multi-imagem (*Open Source*) | Arranca diretamente múltiplas imagens `ISO`, `WIM`, `IMG`, `VHD(x)` e `EFI` | Instalação única na pen USB seguida de cópia direta das ISOs | Exige que as imagens colocadas na pen sejam ambientes forenses validados |

---

## 1. Disquete de Arranque Forense em MS-DOS

Embora obsoleto, um disco de arranque MS-DOS ainda é ocasionalmente necessário na perícia de máquinas industriais ou sistemas antigos:

* **3 Ficheiros Obrigatórios** para arrancar um computador em MS-DOS:
  * `IO.SYS` (referido nos diapositivos como `O.SYS`)
  * `MSDOS.SYS`
  * `COMMAND.COM`
* **Ficheiros Opcionais Processados no Arranque** (se estiverem presentes na disquete, são também utilizados durante o *boot*, devendo ser controlados ou removidos):
  * `DRVSPACE.BIN` ou `DBLSPACE.BIN` (drivers de compressão de disco)
  * `CONFIG.SYS` e `AUTOEXEC.BAT` (ficheiros de configuração e execução automática)

### Procedimento de Criação num Sistema Windows 98

**1.** Na linha de comandos do Windows 98, formatar a disquete transferindo os ficheiros de sistema:

```bat
format a: /U /S
```

* `/U` (*unconditional format*): formatação incondicional (apaga todos os dados existentes).
* `/S`: copia os ficheiros de sistema necessários para a disquete de modo a torná-la um disco de arranque.

**2. Tornar a disquete "Forense" (Limpeza):**

* Remover todos os ficheiros da disquete **exceto os três ficheiros obrigatórios** (`O.SYS` / `IO.SYS`, `MSDOS.SYS` e `COMMAND.COM`).
* Para conseguir apagar ficheiros protegidos (como `DRVSPACE.BIN`), remover previamente os atributos especiais de Oculto (`H`), Só de Leitura (`R`) e Sistema (`S`):

```bat
attrib -H -R -S filename
```

**3. Personalização Posterior:**

* Adicionar ficheiros `CONFIG.SYS` e `AUTOEXEC.BAT` próprios e controlados pelo perito.
* Adicionar utilitários de bloqueio de escrita (*write-blocking utilities*) e outras ferramentas forenses para DOS.

### Alternativa sem Windows 98 Instalado

* Utilizar o utilitário gratuito **HP USB Disk Format Tool**, que inclui a opção *"Create a DOS Startup Disk"*:
  * Utilitário: [HP USB Disk Format Tool v2.1.8](http://www.19systems.net/HP-USB-Tool-v2.1.8.exe)
  * Ficheiros de arranque do Windows 98/DOS: [Win98 Boot Files](http://www.19systems.net/Win98-Boot-Files.zip)
* Uma vez criada a disquete de arranque, aplicam-se exatamente os mesmos passos descritos acima para a tornar "forense" (remover todos os ficheiros exceto `O.SYS`/`IO.SYS`, `MSDOS.SYS` e `COMMAND.COM` e personalizar com `CONFIG.SYS`, `AUTOEXEC.BAT`, *write-blockers* e ferramentas periciais).

---

## 2. CD-ROMs de Arranque Baseados em Linux

Existem várias distribuições Linux em formato *Live CD* pré-configuradas para análise forense (que não montam automaticamente os discos internos ou os montam estritamente em modo *read-only*):

| Distribuição Forense | Características Principais |
| :--- | :--- |
| **Paladin** ([Sumuri](https://www.sumuri.com)) | Distribuição Linux forense equipada com inúmeras ferramentas de interface gráfica (GUI), incluindo o **Autopsy** e a *Paladin Toolbox*. |
| **DEFT** (*Digital Evidence & Forensic Toolkit* — [Launchpad](https://launchpad.net/deft)) | Distribuição personalizada baseada no *Ubuntu Live Linux CD* vocacionada para recolha de evidência digital e resposta a incidentes. |

* **Como criar o CD-ROM de arranque**:
  1. Procurar e descarregar o ficheiro de imagem `.iso` (ex.: `Paladin-6.1.iso`).
  2. Utilizar um programa de gravação de discos óticos para gravar a imagem `ISO` no CD.
* **Desvantagem dos Live CDs baseados em Linux**:
  * **Nem todos os agentes de primeira intervenção (*first responders*) se sentem confortáveis a utilizar Linux**.

---

## 3. CD-ROMs e Ambientes de Arranque Baseados em Windows

Para colmatar a barreira de utilização do Linux e permitir correr ferramentas nativas de Windows sem iniciar o sistema operativo instalado no disco suspeito, existem ambientes de arranque baseados em Windows (*Windows Preinstallation Environment* modificado para não montar/escrever em discos locais):

| Ferramenta / Ambiente | Licença / Modelo | Descrição |
| :--- | :---: | :--- |
| **WinFE (*Windows Forensic Environment*)** | Gratuito | Criado por **Brett Shavers**; ambiente Windows forense de referência (requer uma licença válida do Windows para construção). |
| **SAFE (*System Acquisition Forensic Environment*) Boot Disk** | Comercial | Desenvolvido pela *Forensic Soft*. |
| **Gargoyle Investigator** | Comercial | Desenvolvido pela *Wetstone*. |
| **Ventoy** | *Open Source* | Ferramenta de código aberto para criar uma pen USB de arranque multi-imagem capaz de iniciar diretamente ficheiros `ISO`, `WIM`, `IMG`, `VHD(x)` e `EFI`. |

### Análise do WinFE (*Windows Forensic Environment*)

* **Vantagens**:
  * É gratuito (embora exija que o utilizador possua uma licença de Windows).
  * Executa **software nativo de Windows**, como o **FTK Imager**, **RegRipper**, entre outros.
  * Pode ser amplamente personalizado.
* **Desvantagens**:
  * Exige configuração prévia por parte do utilizador antes da utilização.
  * Tem de ser **construído previamente** para incluir o conjunto específico de ferramentas do perito.

---

## 4. Dispositivos USB de Arranque

Como a grande maioria dos computadores atuais já não possui unidades leitoras de CD/DVD, as imagens forenses (`ISO`) são instaladas em dispositivos USB de arranque através das seguintes ferramentas:

### Em Sistemas Windows

* [UNetBootIn](https://unetbootin.github.io/)
* [Rufus](http://rufus.akeo.ie/)

### Em Sistemas Linux

* **Gnome Multi-Writer**
* **Etcher**
* **UNetBootIn for Linux**

**Ferramenta de linha de comandos `dd`:**

```bash
sudo dd bs=4M if=input.iso of=/dev/sdx conv=fdatasync
```

*(Nota: substituir `sdx` pela letra identificadora do dispositivo de bloco correspondente à pen USB; `bs=4M` define blocos de escrita de 4 MB e `conv=fdatasync` garante a sincronização física dos buffers antes de o comando terminar).*

---

## Implicações Forenses

* **Validação Prévia do Suporte de Arranque**: Um Ubuntu ou Windows PE comum **não é um ambiente de arranque forense** por omissão (pode ativar partições de *swap* existentes ou montar volumes NTFS em leitura/escrita para reproduzir o *journal* `$LogFile`). O perito deve usar exclusivamente distribuições forenses dedicadas (**Paladin**, **DEFT**, **WinFE**) onde o *automount* está desativado ao nível do kernel/registo.
* **Versatilidade do Ventoy em Campo**: O uso do **Ventoy** numa pen USB pericial permite transportar na mesma unidade tanto imagens Linux (`Paladin.iso`) como imagens Windows (`WinFE.iso` / `.wim`) e arrancar em modo BIOS legado ou UEFI com suporte a *Secure Boot*.

---

## Além da aula

* **Ligação aos Ficheiros Legados de Inicialização e Ferramentas de Registry em [[00 ASSI|ASSI]]**:
  * Os ficheiros `CONFIG.SYS` e `AUTOEXEC.BAT` estudados no arranque por disquete MS-DOS são exatamente os ficheiros de configuração legados cuja substituição no Windows 95 deu origem ao [[Estrutura e Hives do Windows Registry|Windows Registry]], conforme estudado no Bloco 05 de ASSI.
  * A grande vantagem apontada para o **WinFE** — poder executar ferramentas Windows como o **RegRipper** e o **FTK Imager** — articula-se diretamente com as notas [[Ferramentas de Análise e Extração do Registry]] e [[Extração da AmCache e Comparação Forense com a ShimCache]] de ASSI, permitindo ao perito correr plugins de extração sobre os hives do disco suspeito a partir de um ambiente *live* seguro sem iniciar o Windows comprometido.

---

## Perguntas de revisão

1. **Quais são os três ficheiros obrigatórios para arrancar um computador em MS-DOS e porque se devem apagar ficheiros como `DRVSPACE.BIN`, `CONFIG.SYS` e `AUTOEXEC.BAT` ao preparar uma disquete forense?**

> [!success]- Ver Resposta
> Os três ficheiros obrigatórios são **`IO.SYS`** (referido nos slides como `O.SYS`), **`MSDOS.SYS`** e **`COMMAND.COM`**. Os ficheiros opcionais como `DRVSPACE.BIN`, `CONFIG.SYS` e `AUTOEXEC.BAT` são processados durante o arranque caso existam na disquete; por isso, devem ser eliminados na limpeza inicial para evitar comportamentos imprevistos e substituídos apenas por configurações controladas pelo perito.

2. **Que significado têm os parâmetros `/U` e `/S` no comando `format a: /U /S` e os parâmetros `-H -R -S` no comando `attrib`?**

> [!success]- Ver Resposta
> No comando `format a: /U /S`, **`/U`** executa uma formatação incondicional (apagando dados anteriores) e **`/S`** transfere os ficheiros de sistema necessários para tornar a disquete arrancável. No comando `attrib -H -R -S filename`, removem-se os atributos especiais de **Oculto (`H`)**, **Só de Leitura (`R`)** e **Sistema (`S`)** para permitir apagar ficheiros protegidos como o `DRVSPACE.BIN`.

3. **Compare as vantagens e desvantagens de utilizar um Live CD baseado em Linux (como o Paladin ou o DEFT) face ao ambiente WinFE baseado em Windows.**

> [!success]- Ver Resposta
> As distribuições Linux (**Paladin**, **DEFT**) são gratuitas, prontas a usar a partir da imagem `.iso` e incluem ferramentas GUI (como o *Autopsy* e a *Paladin Toolbox*), mas têm a desvantagem de nem todos os *first responders* dominarem o Linux. O **WinFE** permite correr **software nativo de Windows** (`FTK Imager`, `RegRipper`) e é altamente personalizável, mas exige **construção e configuração prévia** pelo perito bem como uma **licença válida de Windows**.

4. **Que comando de terminal permite gravar uma imagem `.iso` numa pen USB em Linux garantindo a escrita física integral antes do fecho do comando?**

> [!success]- Ver Resposta
> O comando `sudo dd bs=4M if=input.iso of=/dev/sdx conv=fdatasync`, onde `bs=4M` define blocos de `4 MB`, `of=/dev/sdx` aponta para o dispositivo de bloco da pen USB e **`conv=fdatasync`** força a descarga física integral dos *buffers* para a memória flash antes de o comando terminar.

## Notas relacionadas

- [[Arranque Forense e Processo de Boot (BIOS e Código Máquina)]]
- [[Processo de Arranque UEFI, Secure Boot e Fluxo do Windows]]
- [[Ferramentas Portáteis de Triagem, Pesquisa e FTK Imager Lite]]
- [[Ferramentas Gráficas de Aquisição Forense (Guymager, Paladin Toolbox, Tableau Imager e FTK Imager)]]
- [[Exercícios Práticos e de Projeto - WinFE e Aquisição Forense com FTK Imager]]
- [[Estrutura e Hives do Windows Registry]]
- [[Ferramentas de Análise e Extração do Registry]]
- [[Extração da AmCache e Comparação Forense com a ShimCache]]
- [[Capítulo 2 - Arranque e Aquisição Forense]]
